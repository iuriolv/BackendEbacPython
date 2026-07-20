from kafka import KafkaProducer
import json
import os

KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'kafka:9092')

producer = None

def get_prducer():
    global producer
    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    return producer


def enviar_evento(topico: str, evento: dict):
    prod = get_prducer()
    prod.send(topico, evento)
    prod.flush()