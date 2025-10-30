from kafka import KafkaConsumer, KafkaProducer
import json

# Producer for kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)

# Consumer for kafka
consumer = KafkaConsumer(
    "users",
    group_id="group",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
)
total_message_count = 0
running = True
while running:
    msg_pack = consumer.poll(timeout_ms=500)
    for tp, messages in msg_pack.items():
        for message in messages:
            producer.send("spark-consumer", message.value)
            total_message_count += 1
            print(f"Received message: {message.value}")
            print(f"Total message count: {total_message_count}")
