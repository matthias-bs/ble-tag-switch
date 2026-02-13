# Scripts

This directory contains utility scripts for managing the ble-tag-switch project.

## Creating Issues from Implementation Plan

There are multiple ways to create GitHub issues from `IMPLEMENTATION_PLAN.md`:

### Method 1: Using the Shell Script (Recommended)

The easiest way is to use the provided shell script which handles label creation and authentication:

```bash
# Preview issues without creating them
bash scripts/create_issues.sh --dry-run

# Create the issues
bash scripts/create_issues.sh
```

**Prerequisites:**
- [GitHub CLI (gh)](https://cli.github.com/) installed and authenticated
- Run `gh auth login` if not already authenticated

### Method 2: Using GitHub CLI Directly

If you prefer to use the Python script with gh CLI:

```bash
# Preview
python scripts/create_issues.py --dry-run

# Create issues
python scripts/create_issues.py
```

**Prerequisites:**
- Python 3.6 or higher
- [GitHub CLI (gh)](https://cli.github.com/) installed and authenticated

### Method 3: Using GitHub API Directly

For environments where gh CLI is not available or you prefer API access:

```bash
# Preview
python scripts/create_issues_api.py --dry-run

# Create issues with token from gh
GH_TOKEN=$(gh auth token) python scripts/create_issues_api.py

# Or with explicit token
export GITHUB_TOKEN="your_github_token_here"
python scripts/create_issues_api.py
```

**Prerequisites:**
- Python 3.6 or higher
- GitHub Personal Access Token with `repo` scope

### What Issues Are Created?

The script creates 8 GitHub issues, one for each implementation stage:

1. **Stage 1: Discovery & Baseline Capture** - Initial BLE scanning and tag identification
2. **Stage 2: Fast Pair Service Analysis** - Deep-dive into Fast Pair advertising patterns
3. **Stage 3: MAC Rotation & Pattern Tracking** - MAC address rotation verification
4. **Stage 4: Multi-Tag Discrimination** - Distinguish between multiple tags
5. **Stage 5: Find Hub Network (0xFEAA) Detection** - Capture Find Hub Network advertisements
6. **Stage 6: RSSI Proximity Thresholding** - Calibrate RSSI-based proximity detection
7. **Stage 7: Relay Control Logic (Simulation)** - Test relay activation/deactivation logic
8. **Stage 8: Final Hardware Integration** - Production-ready implementation

Each issue includes:
- Clear title with stage number
- Sketch filename
- Purpose statement
- Implementation details
- User guidance steps
- Expected output format
- Success criteria
- Labels: `implementation`, `stage-N` (and `good first issue` for Stage 1)

### Issue Labels

The script automatically applies the following labels:
- `implementation` - Applied to all issues
- `stage-N` - Applied to each issue (where N is 1-8)
- `good first issue` - Applied to Stage 1 only

**Note**: The labels must exist in your repository before running the script. If they don't exist, the script will fail. You can create labels manually or use the GitHub CLI:

```bash
# Create required labels
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

### Troubleshooting

**Error: "GitHub CLI (gh) not found"**

Install the GitHub CLI from https://cli.github.com/ and authenticate:

```bash
gh auth login
```

**Error: "Could not find IMPLEMENTATION_PLAN.md"**

Make sure you're running the script from the repository root:

```bash
cd /path/to/ble-tag-switch
python scripts/create_issues.py
```

**Error: "Label does not exist"**

Create the required labels first (see "Issue Labels" section above).
