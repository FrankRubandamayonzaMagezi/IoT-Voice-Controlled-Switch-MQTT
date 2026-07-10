import speech_recognition as sr
import paho.mqtt.client as mqtt
import pyttsx3
import time

# =====================================================
# MQTT SETTINGS
# =====================================================

BROKER = "localhost"        # Change if broker is on another PC
PORT = 1883
TOPIC = "iot/switch"

# =====================================================
# MQTT CLIENT
# =====================================================

client = mqtt.Client()

try:
    client.connect(BROKER, PORT, 60)
    print("Connected to MQTT Broker")
except Exception as e:
    print("Failed to connect to MQTT Broker.")
    print(e)
    exit()

# =====================================================
# TEXT TO SPEECH
# =====================================================

engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

def speak(message):
    print("Assistant:", message)
    engine.say(message)
    engine.runAndWait()

# =====================================================
# SPEECH RECOGNITION
# =====================================================

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

microphone = sr.Microphone()

# =====================================================
# STARTUP
# =====================================================

print("=" * 50)
print("      IoT Voice Controlled Switch (MQTT)")
print("=" * 50)
print("MQTT Broker :", BROKER)
print("Topic       :", TOPIC)
print("=" * 50)
print("Available Commands")
print(" • Turn on")
print(" • Turn off")
print("=" * 50)

speak("Hello Hassan. Voice control system is ready.")

# =====================================================
# MAIN LOOP
# =====================================================

while True:

    try:

        with microphone as source:

            print("\nListening...")

            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio).lower()

        print("You said:", text)

        # -----------------------------
        # TURN ON
        # -----------------------------

        if ("turn on" in text or
            "switch on" in text or
            "light on" in text or
            "led on" in text):

            client.publish(TOPIC, "ON")

            speak("Okay Hassan. Turning the switch on.")

            print("Published -> ON")

        # -----------------------------
        # TURN OFF
        # -----------------------------

        elif ("turn off" in text or
              "switch off" in text or
              "light off" in text or
              "led off" in text):

            client.publish(TOPIC, "OFF")

            speak("Okay Hassan. Turning the switch off.")

            print("Published -> OFF")

        # -----------------------------
        # UNKNOWN COMMAND
        # -----------------------------

        else:

            print("Command not recognized.")

            speak("Sorry Hassan. I did not understand that command.")

    except sr.UnknownValueError:

        print("Speech not understood.")

    except sr.RequestError as e:

        print("Speech Recognition Error:", e)

        speak("Speech recognition service is unavailable.")

    except KeyboardInterrupt:

        print("\nProgram terminated.")

        speak("Goodbye Hassan.")

        break

    except Exception as e:

        print("Unexpected Error:", e)

        time.sleep(1)