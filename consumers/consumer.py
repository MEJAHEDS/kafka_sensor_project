from kafka import KafkaConsumer
import json
import sqlite3

# Configure le consommateur Kafka
consumer = KafkaConsumer(
    'sensor-data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("En attente des messages de capteurs...")

# Définition du seuil de température
TEMPERATURE_THRESHOLD = 28.0

# Fonction pour insérer des données dans la base de données
def insert_data(sensor_id, temperature, humidity, timestamp):
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_data (sensor_id, temperature, humidity, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (sensor_id, temperature, humidity, timestamp))
    conn.commit()
    conn.close()

# Boucle pour lire les messages en continu
for message in consumer:
    sensor_data = message.value
    temperature = sensor_data.get("temperature")
    sensor_id = sensor_data.get("sensor_id")
    humidity = sensor_data.get("humidity")
    timestamp = sensor_data.get("timestamp")

    # Vérification de la température et détection d'anomalies
    if temperature > TEMPERATURE_THRESHOLD:
        print(f"⚠️ Alerte ! Capteur {sensor_id} - Température élevée détectée : {temperature}°C")
    
    # Insérer les données dans la base de données
    insert_data(sensor_id, temperature, humidity, timestamp)
    print(f"Données reçues et insérées : {sensor_data}")
