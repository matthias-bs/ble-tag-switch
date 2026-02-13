/*
  ATUVOS Tag Detection - Stage 1: Discovery & Baseline Capture
  
  Purpose: Identify both tags and establish baseline characteristics
  
  User Guidance:
  1. Power ESP32 with no tags in range (capture baseline noise)
  2. Bring Tag-1 into range during pairing mode
  3. Observe: Model ID, device name, manufacturer data, RSSI
  4. Replace Tag-1 with Tag-2 in pairing mode
  5. Compare characteristics between the two tags
  
  Success Criteria:
  - Both tags identified with Fast Pair (0xFE2C) advertisements
  - Model IDs captured
  - Device names match tag labels
*/

#include <Arduino.h>

#ifdef ESP32
#include <NimBLEDevice.h>
#else
#error "This sketch requires an ESP32 board"
#endif

// Scan parameters
#define SCAN_TIME 5 // seconds
#define SCAN_INTERVAL 0x50 // 50ms
#define SCAN_WINDOW 0x30   // 30ms

// UUID for Fast Pair service
static NimBLEUUID fastPairServiceUUID("FE2C");

// Scan counter
uint32_t advertisementCount = 0;
uint32_t scanStartTime = 0;

// Forward declarations
void printHeader();
void printDeviceInfo(const NimBLEAdvertisedDevice* advertisedDevice);
void printHexData(const uint8_t* data, size_t length);
String rssiToStrength(int8_t rssi);

class MyAdvertisedDeviceCallbacks: public NimBLEScanCallbacks {
  void onResult(const NimBLEAdvertisedDevice* advertisedDevice) override {
    advertisementCount++;
    printDeviceInfo(advertisedDevice);
  }
};

// Create an instance of the callback class
MyAdvertisedDeviceCallbacks scanCallbacks;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  printHeader();
  
  Serial.println("\n[INITIALIZING BLE]");
  NimBLEDevice::init("BLE_Tag_Scanner");
  
  // Get the scan object
  NimBLEScan* pBLEScan = NimBLEDevice::getScan();
  pBLEScan->setScanCallbacks(&scanCallbacks, false);
  pBLEScan->setActiveScan(true); // Active scan for more information
  pBLEScan->setInterval(SCAN_INTERVAL);
  pBLEScan->setWindow(SCAN_WINDOW);
  
  Serial.println("✓ BLE initialized successfully");
  Serial.println("\n╔═══════════════════════════════════════════════════════════╗");
  Serial.println("║            USER GUIDANCE - STAGE 1                       ║");
  Serial.println("╚═══════════════════════════════════════════════════════════╝");
  Serial.println();
  Serial.println("Step 1: Observe baseline (no tags nearby)");
  Serial.println("        Wait 10 seconds to see background BLE devices");
  Serial.println();
  Serial.println("Step 2: Press tag button to enter pairing mode (Tag-1)");
  Serial.println("        Look for service UUID 0xFE2C (Fast Pair)");
  Serial.println();
  Serial.println("Step 3: Note the Model ID, device name, and RSSI");
  Serial.println();
  Serial.println("Step 4: Remove Tag-1, repeat with Tag-2");
  Serial.println();
  Serial.println("Step 5: Compare characteristics between tags");
  Serial.println();
  Serial.println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  Serial.println();
  
  scanStartTime = millis();
}

void loop() {
  Serial.printf("\n[SCAN ACTIVE] %lu seconds elapsed | %lu advertisements received\n\n", 
                (millis() - scanStartTime) / 1000, advertisementCount);
  
  // Start scanning
  NimBLEScanResults foundDevices = NimBLEDevice::getScan()->getResults(SCAN_TIME * 1000, false);
  
  Serial.println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  Serial.printf("Scan complete. Devices found: %d\n", foundDevices.getCount());
  Serial.println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
  
  delay(2000);
}

void printHeader() {
  Serial.println("\n\n");
  Serial.println("╔═══════════════════════════════════════════════════════════╗");
  Serial.println("║         ATUVOS TAG DETECTION - STAGE 1                   ║");
  Serial.println("║         Discovery & Baseline Capture                     ║");
  Serial.println("╚═══════════════════════════════════════════════════════════╝");
}

void printDeviceInfo(const NimBLEAdvertisedDevice* advertisedDevice) {
  Serial.println("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  Serial.printf("DEVICE DETECTED: %s\n", advertisedDevice->getAddress().toString().c_str());
  Serial.println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  
  // RSSI
  int8_t rssi = advertisedDevice->getRSSI();
  Serial.printf("  RSSI:              %d dBm (%s)\n", rssi, rssiToStrength(rssi).c_str());
  
  // Device Name
  if (advertisedDevice->haveName()) {
    Serial.printf("  Device Name:       \"%s\"\n", advertisedDevice->getName().c_str());
  } else {
    Serial.println("  Device Name:       <not advertised>");
  }
  
  // Service UUIDs
  if (advertisedDevice->haveServiceUUID()) {
    Serial.print("  Service UUIDs:     ");
    NimBLEUUID devUUID = advertisedDevice->getServiceUUID();
    Serial.print("0x");
    Serial.print(devUUID.toString().c_str());
    
    // Highlight Fast Pair service
    if (devUUID.equals(fastPairServiceUUID)) {
      Serial.print(" ★ FAST PAIR ★");
    }
    Serial.println();
  } else {
    Serial.println("  Service UUIDs:     <none>");
  }
  
  // TX Power
  if (advertisedDevice->haveTXPower()) {
    Serial.printf("  TX Power:          %d dBm\n", advertisedDevice->getTXPower());
  }
  
  // Manufacturer Data
  if (advertisedDevice->haveManufacturerData()) {
    std::string mfgData = advertisedDevice->getManufacturerData();
    Serial.print("  Manufacturer Data: ");
    printHexData((uint8_t*)mfgData.data(), mfgData.length());
    Serial.println();
  }
  
  // Service Data (for Fast Pair analysis)
  if (advertisedDevice->haveServiceData()) {
    Serial.print("  Service Data:      ");
    std::string serviceData = advertisedDevice->getServiceData();
    printHexData((uint8_t*)serviceData.data(), serviceData.length());
    Serial.println();
    
    // Try to parse Fast Pair data if present
    if (advertisedDevice->isAdvertisingService(fastPairServiceUUID)) {
      std::string fpData = advertisedDevice->getServiceData(fastPairServiceUUID);
      if (!fpData.empty()) {
        Serial.print("  Fast Pair Data:    ");
        printHexData((uint8_t*)fpData.data(), fpData.length());
        Serial.println();
        
        // Parse Model ID from first 3 bytes if in discoverable mode
        if (fpData.length() >= 3) {
          uint8_t* data = (uint8_t*)fpData.data();
          Serial.printf("  Model ID (raw):    0x%02X%02X%02X\n", data[0], data[1], data[2]);
        }
      }
    }
  }
  
  Serial.println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
}

void printHexData(const uint8_t* data, size_t length) {
  for (size_t i = 0; i < length; i++) {
    Serial.printf("%02X ", data[i]);
  }
}

String rssiToStrength(int8_t rssi) {
  if (rssi > -50) return "Excellent";
  if (rssi > -60) return "Good";
  if (rssi > -70) return "Fair";
  if (rssi > -80) return "Weak";
  return "Very Weak";
}
