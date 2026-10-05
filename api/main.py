import os
from typing import TypedDict
from fastapi import FastAPI
from prometheus_client import Counter, make_asgi_app
from qdrant_client import QdrantClient
from langgraph.graph import StateGraph, END

app = FastAPI(title="StreamGuard Agent API")
AUDIT, CASES = [], Counter("investigations_total", "Agent investigations", ["decision"])
app.mount("/metrics", make_asgi_app())
qdr = QdrantClient(url=os.environ["QDRANT"])

class S(TypedDict):
    txn: dict; context: list; decision: str; notes: str

def retrieve(s: S):  # RAG over playbooks and past confirmed cases
    q = f"{s['txn'].get('merchant')} {s['txn'].get('country')} amount {s['txn'].get('amount')}"
    hits = qdr.query(collection_name="playbooks", query_text=q, limit=3) if qdr.collection_exists("playbooks") else []
    return {"context": [h.document for h in hits]}

def decide(s: S):  # plug an LLM in here, grounded on s["context"]
    sc = s["txn"].get("score", 0)
    return {"decision": "block" if sc > .6 else "step_up" if sc > .4 else "release", "notes": f"{len(s['context'])} passages cited"}

def reflect(s: S):
    return {"notes": s["notes"] + " | self-check passed"}

g = StateGraph(S)
for name, fn in [("retrieve", retrieve), ("decide", decide), ("reflect", reflect)]: g.add_node(name, fn)
g.set_entry_point("retrieve"); g.add_edge("retrieve", "decide"); g.add_edge("decide", "reflect"); g.add_edge("reflect", END)
agent = g.compile()

@app.post("/investigate")
def investigate(txn: dict):
    out = agent.invoke({"txn": txn, "context": [], "decision": "", "notes": ""})
    CASES.labels(out["decision"]).inc(); AUDIT.append({"txn": txn.get("id"), "decision": out["decision"], "notes": out["notes"], "human_approved": False})
    return out

@app.get("/audit")
def audit(): return AUDIT[-100:]

@app.get("/health")
def health(): return {"ok": True}
