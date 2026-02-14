/*
 * Stage 1: Discovery & Baseline Capture
 * 
 * Purpose: Identify both tags and establish baseline characteristics
 * 
 * This sketch performs continuous BLE scanning with no filtering and displays
 * all detected devices with raw advertisement data.
 * 
 * User Guidance:
 * 1. Power ESP32 with no tags in range (capture baseline noise)
 * 2. Bring Tag-1 into range during pairing mode
 * 3. Observe: Model ID, device name, manufacturer data, RSSI
 * 4. Replace Tag-1 with Tag-2 in pairing mode
 * 5. Compare characteristics between the two tags
 * 
 * Success Criteria:
 * Both tags identified with Fast Pair (0xFE2C) advertisements
 * 
 * Output Format:
 * Table with MAC, RSSI, Service UUIDs, device name, manufacturer data (hex)
 */

#include <Arduino.h>
#include <NimBLEDevice.h>
#include <NimBLEAdvertisedDevice.h>

// Scan interval in milliseconds
const int scanTime = 5 * 1000;  // 5 seconds

NimBLEScan* pBLEScan;

// Fast Pair Service UUID
const uint16_t FAST_PAIR_SERVICE_UUID = 0xFE2C;

/**
 * @brief Convert byte array to hexadecimal string
 * 
 * @param data Pointer to byte array
 * @param length Length of byte array
 * @return String with hex representation
 */
String bytesToHex(const uint8_t* data, size_t length) {
    String result = "";
    for (size_t i = 0; i < length; i++) {
        char hex[3];
        sprintf(hex, "%02X", data[i]);
        result += hex;
        if (i < length - 1) {
            result += " ";
        }
    }
    return result;
}

/**
 * @brief Print table header for device information
 */
void printTableHeader() {
    Serial.println("\n================================================================================");
    Serial.println("| MAC Address       | RSSI | Device Name      | Service UUIDs    | Mfg Data   |");
    Serial.println("================================================================================");
}

/**
 * @brief Print table footer
 */
void printTableFooter() {
    Serial.println("================================================================================\n");
}

/**
 * @brief Callback class for BLE scan results
 */
class DiscoveryScanCallbacks : public NimBLEScanCallbacks {
    void onResult(const NimBLEAdvertisedDevice* advertisedDevice) override {
        // MAC Address
        String macAddress = advertisedDevice->getAddress().toString().c_str();
        Serial.printf("| %-17s | ", macAddress.c_str());
        
        // RSSI
        Serial.printf("%4d | ", advertisedDevice->getRSSI());
        
        // Device Name
        String deviceName = "";
        if (advertisedDevice->haveName()) {
            deviceName = advertisedDevice->getName().c_str();
            if (deviceName.length() > 16) {
                deviceName = deviceName.substring(0, 13) + "...";
            }
        }
        Serial.printf("%-16s | ", deviceName.c_str());
        
        // Service UUIDs
        String serviceUUIDs = "";
        if (advertisedDevice->haveServiceUUID()) {
            NimBLEUUID uuid = advertisedDevice->getServiceUUID();
            serviceUUIDs = uuid.toString().c_str();
            if (serviceUUIDs.length() > 16) {
                serviceUUIDs = serviceUUIDs.substring(0, 13) + "...";
            }
            
            // Check for Fast Pair Service
            if (uuid.equals(NimBLEUUID(FAST_PAIR_SERVICE_UUID))) {
                serviceUUIDs = "0xFE2C [FP]";  // FP = Fast Pair
            }
        }
        Serial.printf("%-16s | ", serviceUUIDs.c_str());
        
        // Manufacturer Data (abbreviated in table, full below)
        String mfgData = "";
        if (advertisedDevice->haveManufacturerData()) {
            std::string data = advertisedDevice->getManufacturerData();
            if (data.length() > 0) {
                // Show first few bytes in table
                mfgData = bytesToHex((const uint8_t*)data.data(), min((size_t)4, data.length()));
                if (data.length() > 4) {
                    mfgData += "...";
                }
            }
        }
        Serial.printf("%-10s |\n", mfgData.c_str());
        
        // If this is a Fast Pair device, print detailed information
        if (advertisedDevice->haveServiceUUID() && 
            advertisedDevice->getServiceUUID().equals(NimBLEUUID(FAST_PAIR_SERVICE_UUID))) {
            
            Serial.println("--------------------------------------------------------------------------------");
            Serial.println("*** FAST PAIR DEVICE DETECTED ***");
            Serial.printf("  MAC Address: %s\n", advertisedDevice->getAddress().toString().c_str());
            Serial.printf("  RSSI: %d dBm\n", advertisedDevice->getRSSI());
            
            if (advertisedDevice->haveName()) {
                Serial.printf("  Device Name: %s\n", advertisedDevice->getName().c_str());
            }
            
            // Print full manufacturer data
            if (advertisedDevice->haveManufacturerData()) {
                std::string data = advertisedDevice->getManufacturerData();
                Serial.printf("  Manufacturer Data (%d bytes): ", data.length());
                Serial.println(bytesToHex((const uint8_t*)data.data(), data.length()));
            }
            
            // Print service data if available
            if (advertisedDevice->haveServiceData()) {
                NimBLEUUID uuid(FAST_PAIR_SERVICE_UUID);
                std::string serviceData = advertisedDevice->getServiceData(uuid);
                if (serviceData.length() > 0) {
                    Serial.printf("  Service Data (%d bytes): ", serviceData.length());
                    Serial.println(bytesToHex((const uint8_t*)serviceData.data(), serviceData.length()));
                    
                    // Parse Fast Pair frame if possible
                    if (serviceData.length() >= 3) {
                        uint8_t frameType = serviceData[0];
                        Serial.printf("  Frame Type: 0x%02X", frameType);
                        
                        if ((frameType & 0xF0) == 0x00) {
                            Serial.println(" (Discoverable - Pairing Mode)");
                            if (serviceData.length() >= 3) {
                                Serial.printf("  Model ID: 0x%02X%02X%02X\n", 
                                            serviceData[0], serviceData[1], serviceData[2]);
                            }
                        } else if ((frameType & 0xF0) == 0x10) {
                            Serial.println(" (Non-discoverable)");
                        } else {
                            Serial.println();
                        }
                    }
                }
            }
            
            Serial.println("--------------------------------------------------------------------------------");
        }
    }
} scanCallbacks;

/**
 * @brief Arduino setup function
 */
void setup() {
    Serial.begin(115200);
    
    // Wait for serial port to initialize
    delay(1000);
    
    Serial.println("\n\n");
    Serial.println("================================================================================");
    Serial.println("  Stage 1: Discovery & Baseline Capture");
    Serial.println("================================================================================");
    Serial.println("\nPurpose: Identify both tags and establish baseline characteristics");
    Serial.println("\nUser Guidance:");
    Serial.println("  1. Power ESP32 with no tags in range (capture baseline noise)");
    Serial.println("  2. Bring Tag-1 into range during pairing mode");
    Serial.println("  3. Observe: Model ID, device name, manufacturer data, RSSI");
    Serial.println("  4. Replace Tag-1 with Tag-2 in pairing mode");
    Serial.println("  5. Compare characteristics between the two tags");
    Serial.println("\nSuccess Criteria:");
    Serial.println("  Both tags identified with Fast Pair (0xFE2C) advertisements");
    Serial.println("\n");
    
    // Initialize NimBLE
    Serial.println("Initializing BLE...");
    NimBLEDevice::init("ESP32-Discovery");
    
    // Configure scan
    pBLEScan = NimBLEDevice::getScan();
    pBLEScan->setScanCallbacks(&scanCallbacks);
    pBLEScan->setActiveScan(true);  // Active scan for scan response data
    pBLEScan->setInterval(100);     // Scan interval in ms
    pBLEScan->setWindow(99);        // Scan window in ms
    
    Serial.println("BLE initialized successfully!");
    Serial.println("Starting continuous scan...\n");
}

/**
 * @brief Arduino loop function
 */
void loop() {
    // Print timestamp
    Serial.printf("\n[%lu ms] Starting scan for %d seconds...\n", 
                  millis(), scanTime / 1000);
    
    printTableHeader();
    
    // Perform scan
    NimBLEScanResults results = pBLEScan->getResults(scanTime, false);
    
    printTableFooter();
    
    // Print summary
    Serial.printf("Scan complete. Devices found: %d\n", results.getCount());
    
    // Clear results to free memory
    pBLEScan->clearResults();
    
    // Wait before next scan
    Serial.println("Waiting 2 seconds before next scan...\n");
    delay(2000);
}
