# Manual Guide: Creating Issues from IMPLEMENTATION_PLAN.md

If the automated scripts don't work for you, here's how to manually create the 8 issues for each implementation stage.

## Issue Templates

### Stage 1: Discovery & Baseline Capture

**Labels**: `implementation`, `stage-1`, `good first issue`

**Title**: Stage 1: Discovery & Baseline Capture

**Body**:
```markdown
## Discovery & Baseline Capture

**Sketch**: `01_discovery_baseline.ino`

**Purpose**: Identify both tags and establish baseline characteristics

---

- Continuous BLE scanning with no filtering
- Display all detected devices with raw advertisement data
- **User guidance**: 
  1. Power ESP32 with no tags in range (capture baseline noise)
  2. Bring Tag-1 into range during pairing mode
  3. Observe: Model ID, device name, manufacturer data, RSSI
  4. Replace Tag-1 with Tag-2 in pairing mode
  5. Compare characteristics between the two tags
- **Output format**: Table with MAC, RSSI, Service UUIDs, device name, mfg data (hex)
- **Success criteria**: Both tags identified with Fast Pair (0xFE2C) advertisements

---

*This issue is part of the implementation plan. See [IMPLEMENTATION_PLAN.md](../blob/main/IMPLEMENTATION_PLAN.md) for full context.*
```

---

### Stage 2: Fast Pair Service Analysis

**Labels**: `implementation`, `stage-2`

**Title**: Stage 2: Fast Pair Service Analysis

**Body**:
```markdown
## Fast Pair Service Analysis

**Sketch**: `02_fastpair_analysis.ino`

**Purpose**: Deep-dive into Fast Pair advertising patterns

---

- Filter for service UUID 0xFE2C only
- Parse and display:
  - Frame type (discoverable vs non-discoverable)
  - Model ID (first 3 bytes)
  - Account Key Filter / Bloom filter (if non-discoverable)
  - TX power
  - Manufacturer-specific data
- Track timing: advertising interval between packets
- **User guidance**:
  1. Put Tag-1 in pairing mode
  2. Observe Frame Type 0x00 (should see Model ID)
  3. Press button/move tag to trigger mode changes
  4. Wait for tag to enter non-discoverable mode (Frame Type 0x00 with Bloom filter instead of Model ID)
  5. Repeat with Tag-2
- **Output format**: 
  ```
  [PAIRING MODE]
  Tag Address: AC:DE:48:XX:XX:XX
  Frame Type: DISCOVERABLE (0x00)
  Model ID: 0xAABBCC
  Device Name: "Atuvos-1234"
  RSSI: -45 dBm
  Advertising Interval: 92 ms
  ```
- **Success criteria**: Both tags show consistent Model ID, capture Bloom filter hash when switching to non-discoverable

---

*This issue is part of the implementation plan. See [IMPLEMENTATION_PLAN.md](../blob/main/IMPLEMENTATION_PLAN.md) for full context.*
```

---

### Stage 3: MAC Rotation & Pattern Tracking

**Labels**: `implementation`, `stage-3`

**Title**: Stage 3: MAC Rotation & Pattern Tracking

**Body**:
```markdown
## MAC Rotation & Pattern Tracking

**Sketch**: `03_mac_rotation_tracking.ino`

**Purpose**: Verify MAC address rotation and establish fingerprinting

---

- Track same tag across multiple MAC address changes
- Store: Bloom filter hash, manufacturer data, RSSI pattern
- **User guidance**:
  1. Maintain Tag-1 in range at fixed distance (~1 meter from ESP32)
  2. Log all advertisements for 20 minutes
  3. Look for MAC address changes (should happen ~every 17 minutes)
  4. Verify same Bloom filter hash persists across MAC changes
  5. Compare RSSI consistency from fixed position
- **Output format**:
  ```
  === TAG FINGERPRINT ANALYSIS ===
  
  [TAG-1 Session]
  Duration: 20 minutes
  MAC Addresses Seen: 5 unique
    - AC:DE:48:AA:AA:AA (0-5 min)
    - AC:DE:48:BB:BB:BB (5-10 min)
    - AC:DE:48:CC:CC:CC (10-15 min)
    - AC:DE:48:DD:DD:DD (15-20 min)
  
  Bloom Filter Hash (consistent): 0xDEADBEEF
  RSSI Range: -48 to -52 dBm (stable)
  Manufacturer Data: 0x0A 0x1B 0x2C 0x3D 0x4E (constant)
  
  ✓ MAC Rotation Confirmed
  ✓ Fingerprint Stability: PASS
  ```
- **Success criteria**: Demonstrate MAC rotation with persistent fingerprint

---

*This issue is part of the implementation plan. See [IMPLEMENTATION_PLAN.md](../blob/main/IMPLEMENTATION_PLAN.md) for full context.*
```

---

### Stage 4: Multi-Tag Discrimination

**Labels**: `implementation`, `stage-4`

**Title**: Stage 4: Multi-Tag Discrimination

**Body**:
```markdown
## Multi-Tag Discrimination

**Sketch**: `04_multitag_discrimination.ino`

**Purpose**: Distinguish between Tag-1 and Tag-2

---

- Build database of both tag fingerprints
- Display which tag is detected and at what RSSI
- **User guidance**:
  1. Bring Tag-1 to fixed location (~1 meter)
  2. Verify detection shows: "TAG-1 DETECTED"
  3. Replace with Tag-2 at same location
  4. Verify detection shows: "TAG-2 DETECTED"
  5. Place both tags at different distances
  6. Verify correct identification of each
  7. Try MAC address changes (move tag away/back) - should maintain correct ID
- **Output format**:
  ```
  === REAL-TIME DETECTION ===
  
  TAG-1: DETECTED
    - Distance: ~1 m (-52 dBm)
    - Bloom Filter Hash: 0xDEADBEEF
    - Last Seen: 125 ms ago
    - Advertisement Count: 1,247
  
  TAG-2: OUT OF RANGE
    - Last Known: 5.2 minutes ago
    - Distance was: ~3 m
  
  Both Tags Status: TAG-1 ACTIVE
  ```
- **Success criteria**: Correctly identify and distinguish both tags across MAC rotations

---

*This issue is part of the implementation plan. See [IMPLEMENTATION_PLAN.md](../blob/main/IMPLEMENTATION_PLAN.md) for full context.*
```

---

### Stage 5: Find Hub Network (0xFEAA) Detection

**Labels**: `implementation`, `stage-5`

**Title**: Stage 5: Find Hub Network (0xFEAA) Detection

**Body**:
```markdown
## Find Hub Network (0xFEAA) Detection

**Sketch**: `05_findhuB_network_detection.ino`

**Purpose**: Capture and verify Find Hub Network advertisements

---

- Filter for service UUID 0xFEAA
- Parse ephemeral ID, frame type, hashed flags
- Compare against Fast Pair data
- **User guidance**:
  1. After pairing tag via Android app (or manual Android Fast Pair)
  2. Tag should advertise 0xFEAA frames
  3. Monitor for: advertising interval (~2 seconds)
  4. Track ephemeral ID changes
  5. Compare RSSI with Fast Pair frames
  6. Repeat with Tag-2
- **Output format**:
  ```
  === FIND HUB NETWORK ADVERTISEMENTS ===
  
  [TAG-1]
  Service UUID: 0xFEAA
  Frame Type: 0x40 (Normal)
  Ephemeral ID: 0xAABBCC...DDEEFF (32 bytes, encrypted)
  Hashed Flags: 0x45
  RSSI: -49 dBm
  Advertising Interval: ~2.0 seconds
  
  [TAG-2]
  Service UUID: 0xFEAA
  Frame Type: 0x40 (Normal)
  Ephemeral ID: 0x11223344...99AABB (32 bytes, encrypted)
  Hashed Flags: 0x42
  RSSI: -63 dBm (farther away)
  Advertising Interval: ~2.1 seconds
  
  ✓ Both tags found in Find Hub Network mode
  ✓ Ephemeral IDs differ (unique per tag)
  ```
- **Success criteria**: Capture 0xFEAA advertisements, confirm different ephemeral IDs per tag

---

*This issue is part of the implementation plan. See [IMPLEMENTATION_PLAN.md](../blob/main/IMPLEMENTATION_PLAN.md) for full context.*
```

---

### Stage 6: RSSI Proximity Thresholding

**Labels**: `implementation`, `stage-6`

**Title**: Stage 6: RSSI Proximity Thresholding

**Body**:
```markdown
## RSSI Proximity Thresholding

**Sketch**: `06_rssi_proximity_thresholding.ino`

**Purpose**: Calibrate RSSI-based proximity detection for relay control

---

- Test different RSSI thresholds
- **User guidance**:
  1. Place Tag-1 at reference distances: 10cm, 50cm, 1m, 2m, 3m
  2. Record RSSI at each distance
  3. Create RSSI vs distance curve
  4. Define relay activation threshold (e.g., -60 dBm = ~1 meter)
  5. Define relay deactivation threshold (e.g., -75 dBm = ~3 meters)
  6. Repeat with Tag-2 to verify consistency
  7. Test with both tags simultaneously at different distances
- **Output format**:
  ```
  === RSSI DISTANCE CALIBRATION ===
  
  [TAG-1 CALIBRATION]
  Distance    | RSSI (samples: min-avg-max)
  10 cm       | -28 (-30 to -27) dBm
  50 cm       | -42 (-44 to -41) dBm
  1 m         | -52 (-54 to -51) dBm ← Suggested ACTIVATE threshold
  2 m         | -62 (-65 to -60) dBm
  3 m         | -72 (-75 to -70) dBm ← Suggested DEACTIVATE threshold
  
  [RECOMMENDED THRESHOLDS]
  Relay Activate:   RSSI > -60 dBm
  Relay Deactivate: RSSI < -73 dBm
  Hysteresis: 13 dBm (prevents flickering)
  
  [TAG-2 CALIBRATION]
  (Similar results, verify consistency)
  
  ✓ Thresholds Calibrated
  ```
- **Success criteria**: Define reliable proximity thresholds with 13+ dBm hysteresis

---

*This issue is part of the implementation plan. See [IMPLEMENTATION_PLAN.md](../blob/main/IMPLEMENTATION_PLAN.md) for full context.*
```

---

### Stage 7: Relay Control Logic (Simulation)

**Labels**: `implementation`, `stage-7`

**Title**: Stage 7: Relay Control Logic (Simulation)

**Body**:
```markdown
## Relay Control Logic (Simulation)

**Sketch**: `07_relay_control_logic.ino`

**Purpose**: Test relay activation/deactivation logic without actual relay

---

- Simulate relay pin (GPIO output)
- Test state transitions: OFF → ON → OFF
- Add debouncing logic
- **User guidance**:
  1. Tag-1 > -60 dBm → Relay activates (serial shows "RELAY ON")
  2. Move tag away to < -73 dBm → Relay deactivates (serial shows "RELAY OFF")
  3. Move tag in/out of threshold zone (between -60 and -73)
  4. Verify no flickering (debounce test: 2 second hold time)
  5. Repeat with Tag-2
  6. Place both tags in detection range
  7. Verify relay remains ON if ANY tag detected
- **Output format**:
  ```
  === RELAY CONTROL LOGIC TEST ===
  
  Current State: OFF
  TAG-1: -65 dBm (OUT OF RANGE)
  TAG-2: NOT DETECTED
  
  [Action] Move TAG-1 closer...
  
  Current State: ON (activated 125 ms ago)
  TAG-1: -58 dBm (IN RANGE) ← RELAY TRIGGER
  TAG-2: NOT DETECTED
  Relay Output: GPIO12 = HIGH
  
  [Action] Move TAG-1 away...
  
  Current State: ON (debouncing, 1.2 sec remaining)
  TAG-1: -75 dBm (OUT OF RANGE, debounce active)
  TAG-2: NOT DETECTED
  Relay Output: GPIO12 = HIGH
  
  [Debounce timeout reached]
  Current State: OFF (deactivated 45 ms ago)
  TAG-1: -78 dBm (OUT OF RANGE)
  TAG-2: NOT DETECTED
  Relay Output: GPIO12 = LOW
  
  ✓ Debouncing Works
  ✓ No False Triggers
  ```
- **Success criteria**: Smooth state transitions with no flickering

---

*This issue is part of the implementation plan. See [IMPLEMENTATION_PLAN.md](../blob/main/IMPLEMENTATION_PLAN.md) for full context.*
```

---

### Stage 8: Final Hardware Integration

**Labels**: `implementation`, `stage-8`

**Title**: Stage 8: Final Hardware Integration

**Body**:
```markdown
## Final Hardware Integration

**Sketch**: `08_final_relay_control.ino`

**Purpose**: Production-ready implementation with actual relay

---

- Configure GPIO pin for actual relay
- Store fingerprints in EEPROM or JSON config
- **User guidance**:
  1. Wire relay to GPIO (configure pin in sketch)
  2. Deploy sketch
  3. Test activation/deactivation with both tags
  4. Verify relay clicks when tag approaches
  5. Test with tags at actual deployment distance
- **Output format**: Minimal logging (only state changes)

---

*This issue is part of the implementation plan. See [IMPLEMENTATION_PLAN.md](../blob/main/IMPLEMENTATION_PLAN.md) for full context.*
```

---

## Quick Copy-Paste Instructions

1. Go to https://github.com/matthias-bs/ble-tag-switch/issues/new
2. Copy the **Title** for the stage you want to create
3. Copy the **Body** for that stage
4. Add the **Labels** listed for that stage
5. Click "Submit new issue"
6. Repeat for all 8 stages

## Creating Labels

Before creating issues, ensure these labels exist in your repository:

```bash
gh label create "implementation" --color "0e8a16" --description "Implementation tasks"
gh label create "stage-1" --color "d4c5f9" --description "Stage 1"
gh label create "stage-2" --color "d4c5f9" --description "Stage 2"
gh label create "stage-3" --color "d4c5f9" --description "Stage 3"
gh label create "stage-4" --color "d4c5f9" --description "Stage 4"
gh label create "stage-5" --color "d4c5f9" --description "Stage 5"
gh label create "stage-6" --color "d4c5f9" --description "Stage 6"
gh label create "stage-7" --color "d4c5f9" --description "Stage 7"
gh label create "stage-8" --color "d4c5f9" --description "Stage 8"
```
