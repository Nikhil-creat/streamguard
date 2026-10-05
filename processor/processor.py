import json, os, collections, torch, torch.nn as nn, pandas as pd
from kafka import KafkaConsumer, KafkaProducer
from deltalake import write_deltalake

class FraudCNN(nn.Module):  # 8x8 feature image per card sequence
    def __init__(s):
        super().__init__()
        s.f = nn.Sequential(nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1),
                            nn.Flatten(), nn.Linear(32, 1), nn.Sigmoid())
    def forward(s, x): return s.f(x)

model = FraudCNN().eval()  # load trained weights in production
hist = collections.defaultdict(lambda: collections.deque(maxlen=64))
cons = KafkaConsumer("txn.raw", bootstrap_servers=os.environ["KAFKA"], value_deserializer=json.loads)
prod = KafkaProducer(bootstrap_servers=os.environ["KAFKA"], value_serializer=lambda v: json.dumps(v).encode())
buf = []
for m in cons:
    t = m.value; h = hist[t["card"]]
    h.append((min(t["amount"] / 1e5, 1) + (t["country"] != "IN") + (t["merchant"] == "cryptox")) / 3)
    img = torch.zeros(64); img[:len(h)] = torch.tensor(list(h))
    cnn = model(img.view(1, 1, 8, 8)).item()
    rule = 0.9 if t["amount"] > 50000 else 0.2
    t["score"] = round(.6 * cnn + .4 * rule, 3)
    prod.send("txn.alerts" if t["score"] > .6 else "txn.scored", t)
    buf.append(t)
    if len(buf) >= 500:
        write_deltalake(os.environ["DELTA_PATH"], pd.DataFrame(buf), mode="append"); buf.clear()
