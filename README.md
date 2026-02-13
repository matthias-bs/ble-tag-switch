# BLE Tag Switch

[![CI](https://github.com/matthias-bs/ble-tag-switch/actions/workflows/CI.yml/badge.svg)](https://github.com/matthias-bs/ble-tag-switch/actions/workflows/CI.yml)
[![Arduino Lint](https://github.com/matthias-bs/ble-tag-switch/actions/workflows/arduino-lint.yml/badge.svg)](https://github.com/matthias-bs/ble-tag-switch/actions/workflows/arduino-lint.yml)

BLE-based tag detection and switching system for ESP32 microcontrollers.

## Description

This project provides functionality for scanning Bluetooth Low Energy (BLE) tags and performing automated switching operations based on tag detection. It is designed for ESP32 microcontrollers.

## Features

- BLE device scanning
- Tag detection and identification
- Automated switching based on tag presence
- Compatible with ESP32 boards

## Examples

The project includes example sketches in the `examples/` directory:

- **BLE_Tag_Switch_Basic**: Basic BLE scanning and tag detection example

## Requirements

- ESP32 board
- Arduino IDE or PlatformIO
- BLE-enabled tags for testing

## Installation

### Arduino IDE

1. Download this repository as a ZIP file
2. In Arduino IDE, go to Sketch > Include Library > Add .ZIP Library
3. Select the downloaded ZIP file
4. The library will be installed and available in your sketches

### PlatformIO

Add to your `platformio.ini`:

```ini
lib_deps = 
    https://github.com/matthias-bs/ble-tag-switch.git
```

## Usage

See the examples in the `examples/` directory for usage instructions.

## Development

This project uses agent-based development with continuous integration:

- **CI Pipeline**: Automatically compiles sketches for multiple ESP32 boards
- **Arduino Lint**: Validates library structure and compliance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Matthias Prinke