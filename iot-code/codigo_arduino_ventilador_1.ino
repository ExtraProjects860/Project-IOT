#include <DHT.h>

// Configurações
#define DHTPIN 2            // Pino do sensor DHT22
#define DHTTYPE DHT22       // Tipo do sensor
#define RELE_PIN 4          // Pino do relé
#define TEMP_LIMITE 25.0    // Temperatura limite para ligar o relé (em °C)

DHT dht(DHTPIN, DHTTYPE);
bool releLigado = false;     // Flag de controle

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  pinMode(RELE_PIN, OUTPUT);
  digitalWrite(RELE_PIN, HIGH); // Mantém o relé desligado no início (caso seja ativo em LOW)
  
  delay(2000); // Aguarda estabilização do sensor
}

void loop() {
  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();

  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Erro ao ler dados do sensor DHT!");
    return;
  }

  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.print(" °C\tUmidade: ");
  Serial.print(umidade);
  Serial.println(" %");

  // Controle com flag
  if (temperatura >= TEMP_LIMITE && !releLigado) {
    Serial.println("Temperatura alta! Ligando o relé...");
    digitalWrite(RELE_PIN, LOW);  // Liga o relé (ajuste para seu módulo: LOW = ligado, HIGH = desligado)
    releLigado = true;
  }
  else if (temperatura < TEMP_LIMITE && releLigado) {
    Serial.println("Temperatura normal. Desligando o relé...");
    digitalWrite(RELE_PIN, HIGH); // Desliga o relé
    releLigado = false;
  }

  delay(2000); // Espera 2 segundos antes da próxima leitura
}
