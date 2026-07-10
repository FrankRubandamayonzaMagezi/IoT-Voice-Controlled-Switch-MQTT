import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/switch"

client = mqtt.Client()

client.connect(BROKER, PORT, 60)

print("Connected to MQTT Broker")

while True:

    command = input("Enter ON or OFF: ").upper()

    if command in ["ON", "OFF"]:

        client.publish(TOPIC, command)

        print("Published:", command)