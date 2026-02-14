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

- **01_discovery_baseline**: Stage 1 - Discovery & Baseline Capture sketch for identifying tags and establishing baseline characteristics. Displays all detected BLE devices with MAC addresses, RSSI, Service UUIDs, device names, and manufacturer data. Special handling for Fast Pair (0xFE2C) advertisements.
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

### Implementation Plan

The project follows a structured 8-stage implementation plan documented in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). Each stage builds upon the previous one to create a complete BLE tag detection and relay control system.

### Creating GitHub Issues from Implementation Plan

To track progress on each implementation stage, you can automatically create GitHub issues from the plan:

#### Using GitHub Actions (Easiest)

1. Go to the **Actions** tab in your repository
2. Select **"Create Implementation Issues"** workflow
3. Click **"Run workflow"** and choose dry run or actual creation

#### Using Command Line

```bash
# Preview issues without creating them
bash scripts/create_issues.sh --dry-run

# Create the issues (requires GitHub CLI)
bash scripts/create_issues.sh
```

For more details, see [scripts/README.md](scripts/README.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Matthias Prinke