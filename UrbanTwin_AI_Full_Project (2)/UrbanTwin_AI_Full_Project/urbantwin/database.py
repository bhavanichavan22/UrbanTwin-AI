"""SQLite persistence for scenario history."""
import sqlite3, json
from pathlib import Path
from datetime import datetime

DB_PATH=Path(__file__).resolve().parents[1]/"urbantwin.db"

def connect():
    con=sqlite3.connect(DB_PATH)
    con.row_factory=sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS scenarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, category TEXT NOT NULL,
            parameters TEXT NOT NULL, results TEXT NOT NULL,
            created_at TEXT NOT NULL)""")
        con.commit()

def save_scenario(name,category,parameters,results):
    with connect() as con:
        cur=con.execute("INSERT INTO scenarios(name,category,parameters,results,created_at) VALUES(?,?,?,?,?)",
            (name,category,json.dumps(parameters),json.dumps(results),datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        con.commit()
        return cur.lastrowid

def list_scenarios(limit=250):
    with connect() as con:
        rows=con.execute("SELECT * FROM scenarios ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
    return [dict(id=r["id"],name=r["name"],category=r["category"],params=json.loads(r["parameters"]),
                 result=json.loads(r["results"]),created_at=r["created_at"]) for r in rows]

def get_scenario(sid):
    with connect() as con:
        r=con.execute("SELECT * FROM scenarios WHERE id=?",(sid,)).fetchone()
    if not r: return None
    return dict(id=r["id"],name=r["name"],category=r["category"],params=json.loads(r["parameters"]),
                result=json.loads(r["results"]),created_at=r["created_at"])

def delete_scenario(sid):
    with connect() as con:
        con.execute("DELETE FROM scenarios WHERE id=?",(sid,))
        con.commit()
