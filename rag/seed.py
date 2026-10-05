import glob, os
from qdrant_client import QdrantClient
c = QdrantClient(url=os.getenv("QDRANT", "http://localhost:6333"))
docs = [open(f).read() for f in glob.glob("rag/playbooks/*.md")]
c.add(collection_name="playbooks", documents=docs)
print(f"indexed {len(docs)} playbooks")
