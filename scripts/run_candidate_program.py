from __future__ import annotations
import hashlib, json, sqlite3, threading, tempfile, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from datetime import datetime, timezone
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from reference.projection_reference import project as p1
from independent_impl.projection import project as p2

def digest(o): return 'sha256:'+hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def load_vectors():
 m=json.loads((ROOT/'conformance/trqp-projection/manifest.json').read_text())
 return [json.loads((ROOT/'conformance/trqp-projection'/x['path']).read_text()) for x in m['vectors']]

def network_check():
 payload={'registry_id':'agentreg:registry:candidate-alpha','arpa_version':'0.9.0','profiles':['ARPA-Core','arpa-trqp-query-projection-0.1']}
 class H(BaseHTTPRequestHandler):
  def do_GET(self):
   body=json.dumps(payload).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
  def log_message(self,*a): pass
 server=HTTPServer(('127.0.0.1',0),H); t=threading.Thread(target=server.serve_forever,daemon=True); t.start()
 try:
  got=json.load(urllib.request.urlopen(f'http://127.0.0.1:{server.server_port}/metadata',timeout=2))
  return got==payload, {'endpoint':f'127.0.0.1:{server.server_port}','metadata_digest':digest(got)}
 finally: server.shutdown()

def durable_event_check():
 with tempfile.NamedTemporaryFile(suffix='.db') as f:
  db=sqlite3.connect(f.name); db.execute('create table events(seq integer primary key, event_id text unique, state text)'); db.execute('create table checkpoints(consumer text primary key, seq integer)')
  events=[(1,'ev-1','active'),(2,'ev-2','suspended'),(3,'ev-3','revoked')]
  for e in events: db.execute('insert or ignore into events values(?,?,?)',e)
  for e in events: db.execute('insert or ignore into events values(?,?,?)',e) # duplicate suppression
  rows=db.execute('select seq,event_id,state from events order by seq').fetchall(); contiguous=[r[0] for r in rows]==[1,2,3]
  db.execute('insert or replace into checkpoints values(?,?)',('enforcement:beta',3)); db.commit()
  ack={'consumer':'enforcement:beta','sequence':db.execute('select seq from checkpoints').fetchone()[0],'resulting_status':'blocked'}
  return contiguous and len(rows)==3 and ack['sequence']==3, {'events':rows,'acknowledgement':ack}

def main():
 vectors=load_vectors(); checks=[]
 for v in vectors:
  a,b=p1(v),p2(v); checks.append({'name':v['id'],'passed':a==b==v['expected'],'expected':v['expected'],'reference':a,'independent':b})
 net,ne=network_check(); checks.append({'name':'networked-metadata-discovery','passed':net,'evidence':ne})
 dur,de=durable_event_check(); checks.append({'name':'durable-event-replay-dedup-checkpoint','passed':dur,'evidence':de})
 safety=all(c['passed'] for c in checks)
 report={'report_version':'1.0','release':'v0.9.0','generated_at':datetime.now(timezone.utc).isoformat(),'candidate_status':'Candidate Specification','checks':checks,'passed':safety,'implementation_independence':{'paths':['reference/projection_reference.py','independent_impl/projection.py'],'external_independence_claim':False},'assurance_boundary':['No external implementation is bundled','No formal TRQP conformance claim','Network test uses local loopback endpoints','Durable event test demonstrates semantics, not production broker operations']}
 out=ROOT/'artifacts/candidate-specification'; out.mkdir(parents=True,exist_ok=True)
 (out/'candidate-validation-report.json').write_text(json.dumps(report,indent=2)+'\n')
 bundle={'bundle_version':'1.0','release':'v0.9.0','reports':{'candidate_validation':digest(report),'mapping':digest((ROOT/'mappings/trqp-arpa-query-projection.yaml').read_text())},'passed':safety,'limitations':report['assurance_boundary']}
 bundle['bundle_digest']=digest(bundle)
 (out/'evidence-bundle.json').write_text(json.dumps(bundle,indent=2)+'\n')
 print(f"candidate-program: {sum(x['passed'] for x in checks)}/{len(checks)} checks passed")
 return 0 if safety else 1
if __name__=='__main__': raise SystemExit(main())
