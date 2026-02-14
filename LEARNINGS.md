# Learnings

## NimBLE-Arduino 2.3.7 API Usage

### Callback Implementation
- Use `NimBLEScanCallbacks` as the base class (not deprecated `NimBLEAdvertisedDeviceCallbacks`)
- Callback method signature: `void onResult(const NimBLEAdvertisedDevice* device) override`
- Use `const` pointer for advertised device parameter
- Mark callback methods with `override` keyword for clarity and compile-time checking
- Instantiate callback class as a named object (not with `new`): `MyCallbacks scanCallbacks;`
- Register callbacks: `pBLEScan->setScanCallbacks(&scanCallbacks);`

### Scan Operation
- Use `getResults(timeInMs, clearResults)` instead of deprecated `start()`
- Time parameter is in milliseconds (not seconds)
- Returns `NimBLEScanResults` directly

### Service UUID Access
- NimBLE-Arduino 2.3.7 only exposes primary service UUID via `getServiceUUID()` (singular)
- The `getServiceUUIDs()` (plural) method returning a vector is no longer available
- If device advertises multiple UUIDs, only the first is accessible through the API

### Removed Features
- Raw payload access (`getPayloadLength()`/`getPayload()`) is no longer available in 2.3.7
- Design implementations without depending on raw payload data

## Arduino Examples Best Practices

### Documentation
- Include comprehensive header comments describing purpose, usage, and success criteria
- Provide step-by-step user guidance in comments
- Document expected output format

### Code Structure
- Use clear, descriptive function names with Doxygen-style documentation
- Separate concerns: data formatting, printing, scanning logic
- Instantiate callback objects at global scope for clarity

### Output Formatting
- Use structured table formats for readability
- Provide both summary views (tables) and detailed views (expanded information)
- Include visual separators and headers to improve serial monitor readability

