#!/usr/bin/env python3
from __future__ import annotations
import json, os, socket, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/typescript/network-interoperability-report.json'

def port():
    s=socket.socket(); s.bind(('127.0.0.1',0)); p=s.getsockname()[1]; s.close(); return p

def request(base,path,method='GET',payload=None):
    data=None if payload is None else json.dumps(payload).encode()
    req=urllib.request.Request(base+path,data=data,method=method,headers={'content-type':'application/json'})
    with urllib.request.urlopen(req,timeout=5) as r: return r.status,json.load(r)

def wait(base):
    for _ in range(50):
        try:
            if request(base,'/health')[0]==200:return
        except Exception: pass
        time.sleep(.1)
    raise RuntimeError(f'server did not become ready: {base}')

def main():
    py_port,ts_port=port(),port()
    py=f'http://127.0.0.1:{py_port}'; ts=f'http://127.0.0.1:{ts_port}'
    env=os.environ.copy(); env['PYTHONPATH']=str(ROOT)
    py_proc=subprocess.Popen([sys.executable,'-m','uvicorn','reference.app:app','--host','127.0.0.1','--port',str(py_port),'--log-level','warning'],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    ts_env=env.copy(); ts_env['ARPA_TS_PORT']=str(ts_port)
    ts_proc=subprocess.Popen(['node','typescript/dist/src/server.js'],cwd=ROOT,env=ts_env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    checks=[]
    try:
        wait(py); wait(ts)
        checks.append({'name':'both-services-healthy','passed':True})
        core=json.load(open(ROOT/'examples/valid/agent-core.json'))
        desc=json.load(open(ROOT/'examples/valid/agent-description-reference.json'))
        # Seed both runtimes through their public HTTP contract.
        for base in (py,ts):
            request(base,'/agents','POST',core)
            request(base,'/records','POST',desc)
        py_list=request(py,'/agents')[1]; ts_list=request(ts,'/agents')[1]
        checks.append({'name':'a2a-discovery-non-authority','passed':bool(py_list['items'] and ts_list['items']) and py_list['items'][0]['authority_implication'] is False and ts_list['items'][0]['authority_implication'] is False})
        checks.append({'name':'canonical-resolution-over-http','passed':request(py,'/agents/'+urllib.parse.quote(core['agent_id'],safe=''))[1]['agent']['record_id']==request(ts,'/agents/'+urllib.parse.quote(core['agent_id'],safe=''))[1]['agent']['record_id']})
        vector=json.load(open(ROOT/'conformance/test-vectors/TV-B-01-allow-in-scope.json'))
        py_dec=request(py,'/authority/evaluate','POST',vector['input'])[1]
        ts_dec=request(ts,'/authority/evaluate','POST',vector['input'])[1]
        checks.append({'name':'authority-decision-over-http','passed':py_dec['decision']==ts_dec['decision']==vector['expected_outcome'],'python':py_dec['decision'],'typescript':ts_dec['decision']})
        checks.append({'name':'decision-receipts-over-http','passed':py_dec['decision_receipt']['record_type']=='decision-receipt' and ts_dec['decision_receipt']['record_type']=='decision-receipt'})
        client_env=env.copy(); client_env['ARPA_PY_URL']=py; client_env['ARPA_TS_URL']=ts
        client=subprocess.run(['node','typescript/dist/src/network-client-check.js'],cwd=ROOT,env=client_env,text=True,capture_output=True,check=False)
        try: client_result=json.loads(client.stdout.strip().splitlines()[-1])
        except Exception: client_result={}
        checks.append({'name':'typescript-client-to-python-registry','passed':client.returncode==0 and client_result.get('typescript_client_to_python') is True})
        checks.append({'name':'typescript-client-to-typescript-registry','passed':client.returncode==0 and client_result.get('typescript_client_to_typescript') is True})
    finally:
        for proc in (py_proc,ts_proc):
            proc.terminate()
        for proc in (py_proc,ts_proc):
            try: proc.wait(timeout=3)
            except subprocess.TimeoutExpired: proc.kill()
    report={
      'report_type':'arpa-typescript-network-interoperability-report',
      'arpa_baseline':'0.9.4','typescript_implementation_version':'0.3.0',
      'transport':'HTTP loopback','checks':checks,
      'summary':{'total':len(checks),'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks)},
      'assurance_boundary':['Both services are repository-controlled implementations.','Loopback HTTP interoperability is implementation evidence, not external certification or organisational independence.','Production persistence, key custody, cryptographic proof verification and federation remain outside this harness.']
    }
    ART.parent.mkdir(parents=True,exist_ok=True); ART.write_text(json.dumps(report,indent=2)+'\n')
    print(f"TypeScript network interoperability: {report['summary']['passed']}/{report['summary']['total']} checks passed")
    return 1 if report['summary']['failed'] else 0
if __name__=='__main__': raise SystemExit(main())
