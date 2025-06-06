#include <DHT.h>

// Configurações
#define DHTPIN 2            // Pino do sensor DHT22
#define DHTTYPE DHT22       // Tipo do sensor
#define RELE_PIN 4          // Pino do relé
#define TEMP_LIMITE 30.0    // Temperatura limite para ligar o relé (em °C)

DHT dht(DHTPIN, DHTTYPE);
bool releOn = false;     // Flag de controle

struct DHT22Data {
  float temperature;
  float humidity;
};

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  pinMode(RELE_PIN, OUTPUT);
  digitalWrite(RELE_PIN, HIGH); // Mantém o relé desligado no início (caso seja ativo em LOW)
  
  delay(2000); 
}

void flag_controller(float temperature, float humidity) {
  if (temperature >= TEMP_LIMITE && !releOn) {
    Serial.println("Temperatura alta! Ligando o relé...");
    digitalWrite(RELE_PIN, LOW);  // Liga o relé (ajuste para seu módulo: LOW = ligado, HIGH = desligado)
    releOn = true;
  }
  else if (temperature < TEMP_LIMITE && releOn) {
    Serial.println("Temperatura normal. Desligando o relé...");
    digitalWrite(RELE_PIN, HIGH); // Desliga o relé
    releOn = false;
  }
}

// para imprimir os valores
void print_values(float temperature, float humidity) {
  Serial.print("Temperatura: ");
  Serial.print(temperature);
  Serial.print(" °C\tUmidade: ");
  Serial.print(humidity);
  Serial.println(" %");
}

// para ler os valores
DHTData get_temperature_and_humidity() {
  DHT22Data data;
  data.temperature = dht.readTemperature();
  data.humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Erro ao ler dados do sensor DHT!");
    data.temperature = -1;
    data.humidity = -1;
  }

  return data;
}

// loop principal
void loop() {
  DHTData data = get_temperature_and_humidity();

  if (data.temperature != -1 && data.humidity != -1) {
    print_values(temperature, humidity);
    flag_controller(temperature, humidity);
  }

  delay(2000); 
}
