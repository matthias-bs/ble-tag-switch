/*
  BLE Tag Switch - Basic Example
  
  This is a basic example sketch for the BLE Tag Switch project.
  It demonstrates BLE scanning and basic tag detection.
  
  This sketch is compatible with ESP32 boards.
*/

#include <Arduino.h>

#ifdef ESP32
#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#endif

// BLE scan parameters
#define SCAN_TIME 5 // seconds

#ifdef ESP32
BLEScan* pBLEScan;

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      Serial.printf("Advertised Device: %s \n", advertisedDevice.toString().c_str());
    }
};
#endif

void setup() {
  Serial.begin(115200);
  Serial.println("BLE Tag Switch - Basic Example");
  Serial.println("Starting...");

#ifdef ESP32
  // Initialize BLE
  BLEDevice::init("BLE_Tag_Switch");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
  // Set scan interval to 100ms and window to 99ms (99% duty cycle)
  // This provides a good balance between scan responsiveness and power consumption
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);
  
  Serial.println("BLE initialized successfully");
#else
  Serial.println("ERROR: This sketch requires an ESP32 board");
#endif
}

void loop() {
#ifdef ESP32
  Serial.println("Scanning for BLE devices...");
  BLEScanResults foundDevices = pBLEScan->start(SCAN_TIME, false);
  Serial.print("Devices found: ");
  Serial.println(foundDevices.getCount());
  Serial.println("Scan done!");
  pBLEScan->clearResults();
  
  delay(2000);
#else
  Serial.println("Waiting... (ESP32 required)");
  delay(5000);
#endif
}
