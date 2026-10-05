import json, random, time, uuid
from kafka import KafkaProducer
p = KafkaProducer(bootstrap_servers="kafka:9092", value_serializer=lambda v: json.dumps(v).encode())
while True:
    p.send("txn.raw", {"id": str(uuid.uuid4()), "card": random.randint(1, 5000),
        "amount": round(random.expovariate(1/1800), 2), "merchant": random.choice(["zomato", "amazon", "cryptox", "uber"]),
        "country": random.choices(["IN", "US", "NG", "AE"], [85, 8, 3, 4])[0], "ts": time.time()})
    time.sleep(0.05)
