       #include <Arduino.h>
#include <ESP32Servo.h>
#include <HTTPClient.h>
#include <ESPAsyncWebServer.h>
#include <Arduino_JSON.h>
#include <RTClib.h>
#include <SPIFFS.h>
#include <WiFi.h>
#include <FirebaseESP32.h>
#include <Adafruit_Sensor.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>
#include "SPIFFS.h"
#include "DHT.h"

#ifdef ARDUINO_ARCH_ESP32
#include <WiFi.h>
#else
#include <ESP8266WiFi.h>
#endif

#define DHT_SENSOR_PIN 21
#define DHT_SENSOR_TYPE DHT11
#define ADC_RESOLUTION 4096.0

#define WIFI_SSID "FABY_PORTUGAL"
#define WIFI_PASSWORD "Lpv2452911"
const String toke = "6224012918:AAHcb5GvGQY95p3KoyXciKoKJy1iV5VgO0s";

#define API_KEY "AIzaSyAI5AE_Wl8cbj7teLhCHwAJTQ4EaB1XUco"
#define DATABASE_URL "iot-proyecto-final-be8fa.firebaseapp.com"

#define USER_EMAIL "proy.tecweb@gmail.com"
#define USER_PASSWORD "tecnos_web"

//String ssid = "FABY_PORTUGAL";
//String password = "Lpv2452911";

const char* ssid = "FABY_PORTUGAL";         
const char* password =  "Lpv2452911";

String databaseSecret = "dHw9FVXZOBHgMdy0TlBTmsvjp1WlQrV757IME30u";

FirebaseData fbdo;
FirebaseJson json;
FirebaseAuth auth;
FirebaseConfig config;
    
AsyncWebServer server(80);
AsyncEventSource events("/events");

DHT dht_sensor(DHT_SENSOR_PIN, DHT_SENSOR_TYPE);

int ledRC1 = 15;
int ledGC1 = 2;
int ledRC2 = 22;
int ledGC2 = 23;
int ledRC3 = 13;
int ledGC3 = 12;
int ledRSA = 32;
int ledGSA = 33;
int ventilador1 = 27;

int page = 0;
int flag=0;
int fla=0;
int mode1=0;
int boton=0;
int band =0;
int value_pwm = 0;
boolean flag_mode=true;
String pwmValue1;
int s_foco = 0;
int s_foco1 = 0;
int s_foco2 = 0;
int s_foco3 = 0;
int page_current = 0;
int page_current1 = 0;
int page_current2 = 0;
int page_current3 = 0;

bool estadoFoco1 = LOW;
bool estadoFoco2 = LOW;
bool estadoFoco3 = LOW;
bool estadoFocoSala = LOW;
bool estadoVentilador = LOW;

String s_rssi = "";
String s_ip = "";
String s_hostname = "";
String s_wifiStatus ="";
String s_ssid ="";
String s_psk = "";
String s_bssid = ""; 

float tempC = dht_sensor.readTemperature();
float humi = dht_sensor.readHumidity();

JSONVar readings;

String getSensorReadings(){
  readings["temperature"] = String(getTemperatura().toInt()/30);
  String jsonString = JSON.stringify(readings);
  return jsonString;
}
void initFS() {
 // Iniciamos  SPIFFS
  if(!SPIFFS.begin())
     { Serial.println("ha ocurrido un error al montar SPIFFS");
       return; }
}
String getPressure() {
    float rssi = WiFi.RSSI();
    Serial.println(rssi);
    return String(rssi);
}

String getIP() {
    Serial.println(WiFi.localIP());
    return String(WiFi.localIP());
}
String getHost() {
    Serial.println(WiFi.getHostname());
    return String(WiFi.getHostname());
}
String getSSID() {
    Serial.println(WiFi.SSID());
    return String(WiFi.SSID());
}
String getStat() {
    Serial.println(WiFi.status());
    return String(WiFi.status());
}

String getPSK() {
    return String(WiFi.psk());
}

String automatico(const String& var){
  if(var == "IP"){
    return WiFi.localIP().toString();
  }else if(var == "HOSTNAME"){
    return String(WiFi.getHostname());
  }else if(var == "STATUS"){
    return String(WiFi.status());
  }else if(var == "PSK"){
    return String(WiFi.psk());
  }else if(var == "RSSI"){
    return String(WiFi.RSSI());
  }else if(var == "SSID"){
    return String(WiFi.SSID());
  }
  return var;
}
void initWiFi() {
// conectamos al Wi-Fi
  WiFi.begin(ssid, password);
  // Mientras no se conecte, mantenemos un bucle con reintentos sucesivos
  while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      // Esperamos un segundo
      Serial.println("Conectando a la red WiFi..");
    }
  Serial.println();
  Serial.println(WiFi.SSID());
  Serial.print("Direccion IP:\t");
  // Imprimimos la ip que le ha dado nuestro router
  Serial.println(WiFi.localIP());
  
  s_ip = WiFi.localIP().toString().c_str();
  s_rssi = String(String(WiFi.RSSI()).toInt()*-1);
  s_hostname = WiFi.getHostname();
  s_wifiStatus =WiFi.status();
  s_ssid =WiFi.SSID().c_str();
  s_psk = WiFi.psk().c_str();
  s_bssid = WiFi.BSSIDstr().c_str(); 
  
}

String getHumedad(){
  float hume = dht_sensor.readHumidity(); 
  Serial.println(hume);
  return String(hume);
}

String getTemperatura(){
  float temp = dht_sensor.readTemperature(true);
  Serial.println(temp);
  return String(temp);
}


void setup() {
  Serial.begin(115200);

  pinMode(ledRC1, OUTPUT);
  pinMode(ledGC1, OUTPUT);
  pinMode(ledRC2, OUTPUT);
  pinMode(ledGC2, OUTPUT);
  pinMode(ledRC3, OUTPUT);
  pinMode(ledGC3, OUTPUT);
  pinMode(ledRSA, OUTPUT);
  pinMode(ledGSA, OUTPUT);
  pinMode(ventilador1, OUTPUT);

  dht_sensor.begin();

  initWiFi();
  initFS();

  String apiKey = API_KEY;
  String databaseURL = DATABASE_URL;
  String userEmail = USER_EMAIL;
  String userPassword = USER_PASSWORD;

  config.api_key = apiKey.c_str();
  auth.user.email = userEmail.c_str();
  auth.user.password = userPassword.c_str();
  config.database_url = databaseURL.c_str();

  Firebase.reconnectWiFi(true);
  Firebase.setDoubleDigits(5);
  fbdo.setResponseSize(4096);
  Firebase.begin(databaseURL, databaseSecret);

  if (Firebase.ready()) {
    Serial.println("Firebase connected");
  } else {
    Serial.println("Firebase not connected");
  }

  server.on("/", HTTP_GET, [](AsyncWebServerRequest * request){
    page = 0;
    request-> send(SPIFFS, "/login.html", String(), false, automatico);
  });
  server.on("/home.html", HTTP_GET, [](AsyncWebServerRequest * request){
    page = 1;
    request->send(SPIFFS,"/home.html", String(), false, automatico);
  });
  server.on("/temperature.html", HTTP_GET, [](AsyncWebServerRequest * request){
    page = 2;
    request->send(SPIFFS,"/temperature.html", String(), false, automatico);
  });
  server.on("/readings", HTTP_GET, [](AsyncWebServerRequest *request){
        String json = getSensorReadings();
        request->send(200, "application/json", json);
        json = String();
     });
      server.on("/TURNC1", HTTP_PUT, [](AsyncWebServerRequest *request) {
      String val = request->arg("VALUE");
      String val2 = request->arg("PAGE");
      Serial.println("val get: " +val);
      Serial.println(val2);
       s_foco1 = val.toInt();
       page_current1 = val2.toInt();
       if(s_foco1 == 1){
        digitalWrite(ledGC1,HIGH);
        digitalWrite(ledRC1,LOW);
       }else{
        digitalWrite(ledRC1,HIGH);
        digitalWrite(ledGC1,LOW);
       }
       Serial.println(s_foco1);
       Serial.println(page_current1);
        });

       server.on("/TURNC2", HTTP_PUT, [](AsyncWebServerRequest *request) {
      String val = request->arg("VALUE");
      String val2 = request->arg("PAGE");
      Serial.println("val get: " +val);
      Serial.println(val2);
       s_foco2 = val.toInt();
       page_current2 = val2.toInt();
       if(s_foco2 == 1){
        digitalWrite(ledGC2,HIGH);
        digitalWrite(ledRC2,LOW);
       }else{
        digitalWrite(ledRC2,HIGH);
        digitalWrite(ledGC2,LOW);
       }
       Serial.println(s_foco2);
       Serial.println(page_current2);
        });

        server.on("/TURNC3", HTTP_PUT, [](AsyncWebServerRequest *request) {
      String val = request->arg("VALUE");
      String val2 = request->arg("PAGE");
      Serial.println("val get: " +val);
      Serial.println(val2);
       s_foco3 = val.toInt();
       page_current3 = val2.toInt();
       if(s_foco3 == 1){
        digitalWrite(ledGC3,HIGH);
        digitalWrite(ledRC3,LOW);
       }else{
        digitalWrite(ledRC3,HIGH);
        digitalWrite(ledGC3,LOW);
       }
       Serial.println(s_foco3);
       Serial.println(page_current3);
        });

        server.on("/TURNC4", HTTP_PUT, [](AsyncWebServerRequest *request) {
      String val = request->arg("VALUE");
      String val2 = request->arg("PAGE");
      Serial.println("val get: " +val);
      Serial.println(val2);
       s_foco = val.toInt();
       page_current = val2.toInt();
       if(s_foco == 1){
        digitalWrite(ledGSA,HIGH);
        digitalWrite(ledRSA,LOW);
       }else{
        digitalWrite(ledRSA,HIGH);
        digitalWrite(ledGSA,LOW);
       }
       Serial.println(s_foco);
       Serial.println(page_current);
      
    });
    server.serveStatic("/", SPIFFS, "/");
    server.on("/SLIDERR", HTTP_POST, [](AsyncWebServerRequest *request){
              pwmValue1= request->arg("pwmValue1");
              band=1;
              Serial.print("setpoint:\t");
              Serial.println(pwmValue1);
              if(tempC>pwmValue1.toFloat()){
                digitalWrite(ventilador1, HIGH);
              }else{
                digitalWrite(ventilador1,LOW);
              }
              request->redirect("/");     
              });
    server.on("/HUME", HTTP_GET, [](AsyncWebServerRequest *request){
      
      if(flag_mode){request->send_P(200, "text/plain", getHumedad().c_str());}
    });

    server.on("/TEMP", HTTP_GET, [](AsyncWebServerRequest *request){
      
      if(flag_mode){request->send_P(200, "text/plain", getTemperatura().c_str());}
    });
   
 events.onConnect([](AsyncEventSourceClient *client){
    if(client->lastId()){
      Serial.printf("Client reconnected! Last message ID that it got is: %u\n", client->lastId());
    }
    // send event with message "hello!", id current millis
    // and set reconnect delay to 1 second
    client->send("hello!", NULL, millis(), 10000);
  });
  server.addHandler(&events);
  server.begin();
}

void loop() {

  if (Firebase.ready()) {
    Firebase.getString(fbdo, "/estadoFoco1");
    if (fbdo.stringData() == "1") {
      Firebase.setString(fbdo, "/estadoFoco1", "1");
      estadoFoco1 = HIGH;
    } else if (fbdo.stringData() == "0") {
      Firebase.setString(fbdo, "/estadoFoco1", "0");
      estadoFoco1 = LOW;
    }
    digitalWrite(ledRC1, !estadoFoco1);
    digitalWrite(ledGC1, estadoFoco1);

    Firebase.getString(fbdo, "/estadoFoco2");
    if (fbdo.stringData() == "1") {
      Firebase.setString(fbdo, "/estadoFoco2", "1");
      estadoFoco2 = HIGH;
    } else if (fbdo.stringData() == "0") {
      Firebase.setString(fbdo, "/estadoFoco2", "0");
      estadoFoco2 = LOW;
    }
    digitalWrite(ledRC2, !estadoFoco2);
    digitalWrite(ledGC2, estadoFoco2);

    Firebase.getString(fbdo, "/estadoFoco3");
    if (fbdo.stringData() == "1") {
      Firebase.setString(fbdo, "/estadoFoco3", "1");
      estadoFoco3 = HIGH;
    } else if (fbdo.stringData() == "0") {
      Firebase.setString(fbdo, "/estadoFoco13", "0");
      estadoFoco3 = LOW;
    }
    digitalWrite(ledRC3, !estadoFoco3);
    digitalWrite(ledGC3, estadoFoco3);

    Firebase.getString(fbdo, "/estadoFocoSala");
    if (fbdo.stringData() == "1") {
      Firebase.setString(fbdo, "/estadoFocoSala", "1");
      estadoFocoSala = HIGH;
    } else if (fbdo.stringData() == "0") {
      Firebase.setString(fbdo, "/estadoFocoSala", "0");
      estadoFocoSala = LOW;
    }
    digitalWrite(ledRSA, !estadoFocoSala);
    digitalWrite(ledGSA, estadoFocoSala);

    Firebase.getString(fbdo, "/estadoVentilador");
    if (fbdo.stringData() == "1") {
      estadoVentilador = HIGH;
    } else if (fbdo.stringData() == "0") {
      estadoVentilador = LOW;
    }
    digitalWrite(ventilador1, estadoVentilador);
  }

  float temperature = dht_sensor.readTemperature();
  float humidity = dht_sensor.readHumidity();

  if (!isnan(temperature) && !isnan(humidity)) {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C");
    Serial.print(" Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");

    Firebase.setFloat(fbdo, "/temperature", temperature);
    Firebase.setFloat(fbdo, "/humidity", humidity);
  }

  delay(5000);
}
