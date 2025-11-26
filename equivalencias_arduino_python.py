#!/usr/bin/env python3
"""
EQUIVALÊNCIAS PYTHON-RASPBERRY PI ↔ C++ ARDUINO/ESP32
====================================================

Este arquivo mostra as equivalências entre comandos do Arduino/ESP32 (C++)
e Python no Raspberry Pi usando a biblioteca RPi.GPIO
"""

import RPi.GPIO as GPIO
import time

# ==============================================================
# CONFIGURAÇÃO INICIAL (equivale ao setup() do Arduino)
# ==============================================================

def setup():
    """Equivale à função setup() do Arduino"""
    
    # Equivale a GPIO.begin() ou similar
    GPIO.setmode(GPIO.BCM)  # Usar numeração BCM
    GPIO.setwarnings(False)
    
    # pinMode(pin, OUTPUT) equivalências:
    GPIO.setup(20, GPIO.OUT)    # pinMode(20, OUTPUT) - LED Vermelho
    GPIO.setup(21, GPIO.OUT)    # pinMode(21, OUTPUT) - LED Verde
    
    # pinMode(pin, INPUT) equivalências:
    GPIO.setup(4, GPIO.IN)      # pinMode(4, INPUT) - DHT11 (configurado pela lib)
    GPIO.setup(24, GPIO.IN)     # pinMode(24, INPUT) - LDR
    
    # pinMode(pin, INPUT_PULLUP) equivalência:
    # GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # pinMode(16, INPUT_PULLUP)

# ==============================================================
# FUNÇÕES BÁSICAS DE GPIO
# ==============================================================

# digitalWrite(pin, HIGH/LOW) equivalências:
def digitalWrite(pin, value):
    """Equivale ao digitalWrite() do Arduino"""
    if value == "HIGH" or value == 1 or value == True:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)

# digitalRead(pin) equivalência:
def digitalRead(pin):
    """Equivale ao digitalRead() do Arduino"""
    return GPIO.input(pin)  # Retorna 1 (HIGH) ou 0 (LOW)

# analogRead(pin) - SIMULAÇÃO (Raspberry Pi não tem ADC nativo)
def analogRead(pin):
    """
    Simula analogRead() do Arduino usando método RC
    No Arduino real, analogRead() retorna 0-1023
    """
    count = 0
    
    # Descarregar capacitor
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    
    # Ler tempo de carga
    GPIO.setup(pin, GPIO.IN)
    while GPIO.input(pin) == GPIO.LOW:
        count += 1
        if count > 100000:  # Timeout
            break
    
    return min(count // 100, 1023)  # Normalizar para 0-1023

# delay() equivalência:
def delay(milliseconds):
    """Equivale ao delay() do Arduino"""
    time.sleep(milliseconds / 1000.0)

# ==============================================================
# EXEMPLOS PRÁTICOS
# ==============================================================

def exemplo_blink_led():
    """Equivale ao exemplo Blink do Arduino"""
    
    setup()  # setup()
    
    while True:  # loop()
        # digitalWrite(LED_VERDE_PIN, HIGH);
        digitalWrite(21, "HIGH")
        delay(1000)  # delay(1000);
        
        # digitalWrite(LED_VERDE_PIN, LOW);
        digitalWrite(21, "LOW")
        delay(1000)  # delay(1000);

def exemplo_leitura_sensor():
    """Exemplo de leitura de sensores como no Arduino"""
    
    setup()  # setup()
    
    while True:  # loop()
        # Ler LDR (equivale ao analogRead())
        ldr_value = analogRead(24)  # analogRead(LDR_PIN);
        print(f"LDR Value: {ldr_value}")  # Serial.println(ldr_value);
        
        # Controlar LEDs baseado no valor
        if ldr_value < 300:  # Escuro
            digitalWrite(20, "HIGH")  # LED Vermelho
            digitalWrite(21, "LOW")
        else:  # Claro
            digitalWrite(20, "LOW")
            digitalWrite(21, "HIGH")  # LED Verde
        
        delay(500)  # delay(500);

# ==============================================================
# DHT11 - EQUIVALÊNCIA MAIS COMPLEXA
# ==============================================================

def exemplo_dht11():
    """
    Leitura do DHT11 (mais complexa que Arduino devido ao protocolo)
    No Arduino: dht.readTemperature() e dht.readHumidity()
    """
    
    # No Python, usamos biblioteca específica:
    try:
        import adafruit_dht
        import board
        
        # Equivale a DHT dht(DHT_PIN, DHT11);
        dht = adafruit_dht.DHT11(board.D4)
        
        while True:  # loop()
            try:
                # float temp = dht.readTemperature();
                temperatura = dht.temperature
                
                # float hum = dht.readHumidity();
                umidade = dht.humidity
                
                if temperatura is not None and umidade is not None:
                    # Serial.print("Temp: "); Serial.println(temp);
                    print(f"Temperatura: {temperatura}°C")
                    print(f"Umidade: {umidade}%")
                else:
                    print("Erro na leitura do DHT11")
                    
            except RuntimeError as e:
                print(f"Erro DHT11: {e.args[0]}")
            
            delay(2000)  # delay(2000);
            
    except ImportError:
        print("Biblioteca adafruit_dht não instalada")

# ==============================================================
# COMPARAÇÃO DIRETA DE CÓDIGOS
# ==============================================================

"""
ARDUINO/ESP32 (C++)                    |  RASPBERRY PI (Python)
====================================== | ======================================
#include <DHT.h>                       | import adafruit_dht, board
                                       |
void setup() {                         | def setup():
  pinMode(LED_PIN, OUTPUT);            |   GPIO.setup(LED_PIN, GPIO.OUT)
  pinMode(BUTTON_PIN, INPUT_PULLUP);   |   GPIO.setup(BUTTON_PIN, GPIO.IN, 
  Serial.begin(9600);                  |              pull_up_down=GPIO.PUD_UP)
}                                      |
                                       |
void loop() {                          | while True:  # loop infinito
  digitalWrite(LED_PIN, HIGH);         |   GPIO.output(LED_PIN, GPIO.HIGH)
  delay(1000);                         |   time.sleep(1)
  digitalWrite(LED_PIN, LOW);          |   GPIO.output(LED_PIN, GPIO.LOW)
  delay(1000);                         |   time.sleep(1)
                                       |
  int sensorValue = analogRead(A0);    |   sensor_value = analogRead(24)
  Serial.println(sensorValue);         |   print(sensor_value)
                                       |
  if (digitalRead(BUTTON_PIN) == LOW) {|   if GPIO.input(BUTTON_PIN) == 0:
    // Botão pressionado                |     # Botão pressionado
  }                                    |
}                                      |
"""

# ==============================================================
# CÓDIGO PRINCIPAL PARA TESTE
# ==============================================================

if __name__ == "__main__":
    print("🔧 Teste das equivalências Arduino ↔ Raspberry Pi")
    print("Escolha um exemplo:")
    print("1. Blink LED")
    print("2. Leitura LDR")
    print("3. DHT11")
    
    try:
        opcao = input("Digite o número: ")
        
        if opcao == "1":
            print("🔴 Iniciando Blink LED (Ctrl+C para parar)")
            exemplo_blink_led()
        elif opcao == "2":
            print("💡 Iniciando leitura LDR (Ctrl+C para parar)")
            exemplo_leitura_sensor()
        elif opcao == "3":
            print("🌡️ Iniciando DHT11 (Ctrl+C para parar)")
            exemplo_dht11()
        else:
            print("Opção inválida")
            
    except KeyboardInterrupt:
        print("\n🛑 Programa interrompido")
    finally:
        GPIO.cleanup()  # Equivale ao reset do Arduino