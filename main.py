import speech_recognition as sr
import paho.mqtt.client as mqtt
import time

# ==========================================
# MQTT SETTINGS
# ==========================================

BROKER = "10.180.200.30"      # Your PC IP Address
PORT = 1883
TOPIC = "iot/switch"

# ==========================================
# MQTT CLIENT
# ==========================================

client = mqtt.Client()

print("Connecting to MQTT Broker...")

client.connect(BROKER, PORT, 60)

print("Connected to MQTT Broker!")

# ==========================================
# SPEECH RECOGNITION
# ==========================================

recognizer = sr.Recognizer()
microphone = sr.Microphone()

print("====================================")
print(" IoT Voice Controlled Switch")
print(" MQTT Mode")
print(" Say:")
print("   Turn on switch")
print("   Turn off switch")
print(" Press CTRL+C to exit")
print("====================================")

with microphone as source:

    recognizer.adjust_for_ambient_noise(source, duration=2)

    print("Microphone calibrated.")

while True:

    try:

        with microphone as source:

            print("\nListening...")

            audio = recognizer.listen(source)

        command = recognizer.recognize_google(audio)

        command = command.lower()

        print("You said:", command)

        # ------------------------------
        # TURN ON
        # ------------------------------

        if "turn on switch" in command:

            print("Publishing: ON")

            client.publish(TOPIC, "ON")

        # ------------------------------
        # TURN OFF
        # ------------------------------

        elif "turn off switch" in command:

            print("Publishing: OFF")

            client.publish(TOPIC, "OFF")

        else:

            print("Command not recognized.")

    except sr.UnknownValueError:

        print("Could not understand audio.")

    except sr.RequestError:

        print("Speech Recognition service unavailable.")

    except KeyboardInterrupt:

        print("\nProgram terminated.")

        break

    time.sleep(0.5)