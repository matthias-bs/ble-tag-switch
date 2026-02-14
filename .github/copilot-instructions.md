<!--
#
# copilot-instructions.md - Basic project description and instructions for coding agents
#
-->

# Rules

## General

- The implementation must follow the best practices for good, sustainable, maintainable and understandable code.
- There are no quick fixes. The generated or adapted code must be high quality, industry standard code.
- The generated code must be documented well, so it can be comprehended and maintained by humans, too.
- Prefer VSCode tasks over shell commands when possible.
- For file manipulation (rename, move, delete, ...) prefer VSCode APIs over shell commands.

## Implementation

- Adhere to Arduino coding standards and file system structure
- NimBLE-Arduino will be used as BLE library

## Repository

- The repository name for this project is `https://github.com/matthias-bs/ble-tag-switch`.
- Before committing anything, ensure that all checks and tests pass successfully.

# Documentation

- The `doc` folder in the main project directory contains the general project manifest, guidelines and architecture descriptions.
- The `README.md` contains the user's documentations

# Tools

- Prefer tools over prompts whenever possible.
- Prefer VSCode tasks over shell commands when possible.
- The following tools are available in the project and can be used as needed.

|VSCode Task|Description|
|-----------|-----------|
| Arduino: Install ESP32 Core | Run to install a the Arduino ESP32 Core (on user's request) |
| Arduino: Install Libraries | Run to install the Arduino libraries (on user's request) | 
| Arduino: Compile All Examples | Run when new code has been created or existing code was changed |
| Arduino: Clean Build Artifacts | Run when compiled artifacts might be stale |
| Arduino: Setup Complete Environment | Run to set up arduino-cli (on user's request) |
