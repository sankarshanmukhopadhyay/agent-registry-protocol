from __future__ import annotations
import json, sqlite3
from datetime import datetime, timezone
from pathlib import Path

class Store:
    def __init__(self, path: str = ':memory:'):
        self.db=sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory=sqlite3.Row
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS records(record_id TEXT PRIMARY KEY, record_type TEXT NOT NULL, subject TEXT NOT NULL, issued_at TEXT NOT NULL, body TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS events(sequence INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT UNIQUE NOT NULL, subject TEXT NOT NULL, event_type TEXT NOT NULL, effective_at TEXT NOT NULL, body TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS aliases(alias TEXT NOT NULL, canonical_id TEXT NOT NULL, status TEXT NOT NULL, effective_from TEXT NOT NULL, effective_until TEXT, body TEXT NOT NULL);
        """)
    def put_record(self, record):
        subject=record.get('agent_id') or record.get('subject')
        if isinstance(subject,dict): subject=json.dumps(subject,sort_keys=True)
        self.db.execute('INSERT OR REPLACE INTO records VALUES(?,?,?,?,?)',(record['record_id'],record['record_type'],subject,record['issued_at'],json.dumps(record,sort_keys=True)))
        self.db.commit()
    def get_record(self, record_id):
        row=self.db.execute('SELECT body FROM records WHERE record_id=?',(record_id,)).fetchone(); return json.loads(row[0]) if row else None
    def records_for_subject(self, subject, at=None):
        rows=self.db.execute('SELECT body FROM records WHERE subject=? ORDER BY issued_at',(subject,)).fetchall()
        records=[json.loads(r[0]) for r in rows]
        if at: records=[r for r in records if r.get('effective_from','')<=at and (r.get('effective_until') is None or at<=r['effective_until'])]
        return records
    def add_event(self,event):
        self.db.execute('INSERT INTO events(event_id,subject,event_type,effective_at,body) VALUES(?,?,?,?,?)',(event['event_id'],event['subject'],event['event_type'],event['effective_at'],json.dumps(event,sort_keys=True)))
        self.db.commit()
        return self.db.execute('SELECT sequence FROM events WHERE event_id=?',(event['event_id'],)).fetchone()[0]
    def events(self, subject=None, after=0):
        if subject: rows=self.db.execute('SELECT sequence,body FROM events WHERE subject=? AND sequence>? ORDER BY sequence',(subject,after)).fetchall()
        else: rows=self.db.execute('SELECT sequence,body FROM events WHERE sequence>? ORDER BY sequence',(after,)).fetchall()
        out=[]
        for r in rows:
            e=json.loads(r['body']); e['sequence']=r['sequence']; out.append(e)
        return out
    def add_alias(self,record):
        self.db.execute('INSERT INTO aliases VALUES(?,?,?,?,?,?)',(record['alias'],record['canonical_id'],record['alias_status'],record['effective_from'],record.get('effective_until'),json.dumps(record,sort_keys=True))); self.db.commit()
    def resolve_alias(self,alias,at):
        rows=self.db.execute('SELECT body FROM aliases WHERE alias=?',(alias,)).fetchall(); active=[]
        for row in rows:
            r=json.loads(row[0])
            if r['alias_status']=='active' and r['effective_from']<=at and (r.get('effective_until') is None or at<=r['effective_until']): active.append(r)
        return active
