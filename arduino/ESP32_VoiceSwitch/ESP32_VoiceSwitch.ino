#include <WiFi.h>
#include <WebServer.h>
#include <PubSubClient.h>

//=============================
// WiFi Credentials
//=============================

const char* ssid = "WIFI-USERNAME";
const char* password = "WIFI-PASSWORD";

//=============================
// MQTT Broker
//=============================
WebServer server(80);


// Your PC running Mosquitto
const char* mqtt_server = "192.168.47.243";

WiFiClient espClient;
PubSubClient client(espClient);

//=============================
// LED
//=============================

const int LED_PIN = 2;
bool ledState = false;

//====================================================
// Connect WiFi
//====================================================

void setup_wifi()
{
  Serial.println();
  Serial.print("Connecting to WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());
}

//====================================================
// MQTT Callback
//====================================================

void callback(char* topic, byte* payload, unsigned int length)
{
  String message = "";

  for (int i = 0; i < length; i++)
  {
    message += (char)payload[i];
  }

  Serial.print("Message Received: ");
  Serial.println(message);

  if(message == "ON")
  {
      digitalWrite(LED_PIN,HIGH);
      ledState = true;
       client.publish("iot/status","ON");
      Serial.println("LED ON");
  }

  if(message == "OFF")
  {
      digitalWrite(LED_PIN,LOW);
      ledState = false;
      client.publish("iot/status","OFF");
      Serial.println("LED OFF");
  }
}

//====================================================
// MQTT Reconnect
//====================================================

void reconnect()
{
  Serial.print("MQTT Broker: ");
  Serial.println(mqtt_server);
  
  while (!client.connected())
  {
    Serial.print("Connecting to MQTT...");

    if (client.connect("ESP32Client"))
    {
      Serial.println(" Connected");

      client.subscribe("iot/switch");

      Serial.println("Subscribed to topic:");
      Serial.println("iot/switch");
    }
    else
    {
    Serial.print("MQTT Connection Failed. State = ");
    Serial.println(client.state());

    Serial.println("Retrying in 5 seconds...");
    delay(5000);
    }
  }
}

void handleRoot()
{
    String html = R"rawliteral(

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1">

<title>IoT Voice Switch</title>

<style>

body{
font-family:Arial;
background:#eef3f8;
text-align:center;
padding-top:40px;
}

.card{
background:white;
width:90%;
max-width:700px;
margin:auto;
padding:30px;
border-radius:15px;
box-shadow:0 5px 20px rgba(0,0,0,.15);
}

.status{
font-size:42px;
margin:25px;
font-weight:bold;
}

button{
padding:18px 40px;
font-size:20px;
margin:10px;
border:none;
border-radius:12px;
cursor:pointer;
}

.on{
background:#28a745;
color:white;
}

.off{
background:#dc3545;
color:white;
}

</style>

</head>

<body>

<div class="card">

<h1>🎤 IoT Voice Controlled Switch</h1>

<p><b>ESP32 Dashboard</b></p>

<div id="status" class="status">

Loading...

</div>

<button class="on" onclick="fetch('/on')">
Turn ON
</button>

<button class="off" onclick="fetch('/off')">
Turn OFF
</button>

</div>

<script>

function updateStatus(){

fetch('/status')

.then(r=>r.text())

.then(state=>{

if(state=="ON"){

document.getElementById("status").innerHTML="🟢 LED ON";

}else{

document.getElementById("status").innerHTML="🔴 LED OFF";

}

});

}

updateStatus();

setInterval(updateStatus,500);

</script>

</body>

</html>

)rawliteral";

server.send(200,"text/html",html);
}

void handleOn()
{
    ledState=true;

    digitalWrite(LED_PIN,HIGH);

    client.publish("iot/status","ON");

    server.send(200,"text/plain","OK");
}

void handleOff()
{
    ledState=false;

    digitalWrite(LED_PIN,LOW);

    client.publish("iot/status","OFF");

    server.send(200,"text/plain","OK");
}

void handleStatus()
{
    if(ledState)
        server.send(200,"text/plain","ON");
    else
        server.send(200,"text/plain","OFF");
}
//====================================================
// Setup
//====================================================

void setup()
{
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);

  digitalWrite(LED_PIN, LOW);

  setup_wifi();

  client.setServer(mqtt_server,1883);

  client.setCallback(callback);
  server.on("/", handleRoot);

server.on("/on", handleOn);

server.on("/off", handleOff);

server.on("/status", handleStatus);

server.begin();

Serial.println("Web Server Started");
}

//====================================================
// Loop
//====================================================

void loop()
{
  if(!client.connected())
  {
      reconnect();
  }

  client.loop();
  server.handleClient();
}
