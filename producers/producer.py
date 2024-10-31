from kafka import KafkaProducer
import json
import random
import time

# Configure le producteur Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_sensor_data():
    """Simule les données de capteurs."""
    data = {
        "sensor_id": random.randint(1, 10),
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 60.0), 2),
        "timestamp": time.time()
    }
    return data

try:
    print("Envoi des données de capteurs au topic 'sensor-data'...")
    while True:
        sensor_data = generate_sensor_data()
        producer.send('sensor-data', value=sensor_data)
        print(f"Données envoyées : {sensor_data}")
        time.sleep(1)  # Envoie des données toutes les secondes
except KeyboardInterrupt:
    print("Arrêt du producteur.")
finally:
    producer.close()
