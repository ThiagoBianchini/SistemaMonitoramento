#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // Endereço LCD I2C

const int sensorMovimento = 2;
const int pinoLDR = A0;
const int ledInterno = 13;

void setup() {
  pinMode(sensorMovimento, INPUT);
  pinMode(ledInterno, OUTPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Inicializando...");
  delay(2000);
  lcd.clear();

  Serial.begin(9600);

  lcd.setCursor(0, 0);
  lcd.print("Sistema Pronto");
  delay(1500);
  lcd.clear();
}

void loop() {
  unsigned long tempo = millis();

  // Leitura dos sensores
  int movimento = digitalRead(sensorMovimento);
  int valorLDR = analogRead(pinoLDR);

  // Atualiza o LED
  digitalWrite(ledInterno, movimento);

  // Atualiza LCD
  lcd.setCursor(0, 0);
  lcd.print("Movimento: ");
  lcd.print(movimento == HIGH ? "SIM " : "NAO");

  lcd.setCursor(0, 1);
  lcd.print("LDR: ");
  lcd.print(valorLDR);
  lcd.print("     "); // limpa excesso à direita

  // Mostra no Serial Monitor
  Serial.print("Tempo(ms): ");
  Serial.print(tempo);
  Serial.print(" | Movimento: ");
  Serial.print(movimento);
  Serial.print(" | LDR: ");
  Serial.println(valorLDR);

  delay(100); // intervalo de amostragem
}
