#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

unsigned long read_interval = 1000;
unsigned long last_read_time = 10000;


Adafruit_BME280 bme; // I2C
//Adafruit_BME280 bme(BME_CS); // hardware SPI
//Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK); // software SPI

void setup() {
    Serial.begin(9600);
    while(!Serial);    // time to get serial running
    Serial.println("Started");

    unsigned status;

    status = bme.begin(0x76);
    if (!status) {
        Serial.println("Could not find a valid BME280 sensor, check wiring, address, sensor ID!");
        Serial.print("SensorID was: 0x"); Serial.println(bme.sensorID(),16);
        Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
        Serial.print("   ID of 0x56-0x58 represents a BMP 280,\n");
        Serial.print("        ID of 0x60 represents a BME 280.\n");
        Serial.print("        ID of 0x61 represents a BME 680.\n");
        while (1) delay(10);
    }
}


void loop() {
    if (millis() - last_read_time > read_interval) {
        last_read_time = millis();
        printValues();
    }
}


void printValues() {
    Serial.print("{");
    
    Serial.print("\"temperature\":");
    Serial.print(bme.readTemperature());

    Serial.print(",\"pressure\":");
    Serial.print(bme.readPressure());

    Serial.print(",\"altitude\":");
    Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));

    Serial.print(",\"humidity\":");
    Serial.print(bme.readHumidity());
    
    Serial.print("}\n");
}
