#ifdef ARDUINO_ARCH_ESP32
#include <WiFi.h>
#else
#include <ESP8266WiFi.h>
#endif
#include <Espalexa.h>

// Prototypes
boolean connectWifi();

// Callback functions
void cuartoUno(uint8_t brightness);
void cuartoDos(uint8_t brightness);
void cuartoTres(uint8_t brightness);
void cuartoSala(uint8_t brightness);
void cuartoVenti(uint8_t brightness);

const char* ssid = "FABY_PORTUGAL";
const char* password = "Lpv2452911";

boolean wifiConnected = false;

EspalexaDevice* deviceUno;
EspalexaDevice* deviceDos;
EspalexaDevice* deviceTres;
EspalexaDevice* deviceSala;

int ledRC1 = 15;
int ledGC1 = 2;
int ledRC2 = 22;
int ledGC2 = 23;
int ledRC3 = 13;
int ledGC3 = 12;
int ledRSA = 32;
int ledGSA = 33;
int ventilador1 = 27;

Espalexa alexita;

void setup() {
  Serial.begin(115200);

  wifiConnected = connectWifi();

  if (wifiConnected) {
    deviceUno = new EspalexaDevice("Foco uno", cuartoUno);
    deviceDos = new EspalexaDevice("Foco dos", cuartoDos);
    deviceTres = new EspalexaDevice("Foco tres", cuartoTres);
    deviceSala = new EspalexaDevice("Foco Sala", cuartoSala);

    alexita.addDevice(deviceUno);
    alexita.addDevice(deviceDos);
    alexita.addDevice(deviceTres);
    alexita.addDevice(deviceSala);

    alexita.begin();
  } else {
    while (1) {
      Serial.println("Cannot connect to WiFi. Please check data and reset the ESP.");
      delay(2500);
    }
  }
}

void loop() {
  alexita.loop();
  delay(1);
}

void cuartoUno(uint8_t brightness) {
  if (brightness) {
    digitalWrite(ledGC1, HIGH);
    digitalWrite(ledRC1, LOW);
    Serial.println("Foco uno encendido");
  } else {
    digitalWrite(ledGC1, LOW);
    digitalWrite(ledRC1, HIGH);
    Serial.println("Foco uno apagado");
  }
}

void cuartoDos(uint8_t brightness) {
  if (brightness) {
    digitalWrite(ledGC2, HIGH);
    digitalWrite(ledRC2, LOW);
    Serial.println("Foco dos encendido");
  } else {
    digitalWrite(ledGC2, LOW);
    digitalWrite(ledRC2, HIGH);
    Serial.println("Foco dos apagado");
  }
}

void cuartoTres(uint8_t brightness) {
  if (brightness) {
    digitalWrite(ledGC3, HIGH);
    digitalWrite(ledRC3, LOW);
    Serial.println("Foco tres encendido");
  } else {
    digitalWrite(ledGC3, LOW);
    digitalWrite(ledRC3, HIGH);
    Serial.println("Foco tres apagado");
  }
}

void cuartoSala(uint8_t brightness) {
  if (brightness) {
    digitalWrite(ledGSA, HIGH);
    digitalWrite(ledRSA, LOW);
    Serial.println("Foco sala encendido");
  } else {
    digitalWrite(ledGSA, LOW);
    digitalWrite(ledRSA, HIGH);
    Serial.println("Foco sala apagado");
  }
}

boolean connectWifi() {
  boolean state = true;
  int i = 0;

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.println("Connecting to WiFi");

  Serial.print("Connecting...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (i > 20) {
      state = false;
      break;
    }
    i++;
  }
  Serial.println("");
  if (state) {
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Connection failed.");
  }
  return state;
}
