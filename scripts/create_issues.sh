#!/bin/bash
# Script to create GitHub issues from IMPLEMENTATION_PLAN.md
# This script ensures labels exist and then creates the issues

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}✗ GitHub CLI (gh) is not installed${NC}"
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if gh is authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}✗ GitHub CLI is not authenticated${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

echo -e "${GREEN}GitHub CLI is ready${NC}\n"

# Create labels if they don't exist
echo "Creating labels (if they don't exist)..."

create_label() {
    local name=$1
    local color=$2
    local description=$3
    
    if gh label list | grep -q "^${name}"; then
        echo -e "${YELLOW}  - Label '${name}' already exists${NC}"
    else
        gh label create "$name" --color "$color" --description "$description"
        echo -e "${GREEN}  ✓ Created label '${name}'${NC}"
    fi
}

create_label "implementation" "0e8a16" "Implementation tasks from IMPLEMENTATION_PLAN.md"
create_label "stage-1" "d4c5f9" "Stage 1: Discovery & Baseline Capture"
create_label "stage-2" "d4c5f9" "Stage 2: Fast Pair Service Analysis"
create_label "stage-3" "d4c5f9" "Stage 3: MAC Rotation & Pattern Tracking"
create_label "stage-4" "d4c5f9" "Stage 4: Multi-Tag Discrimination"
create_label "stage-5" "d4c5f9" "Stage 5: Find Hub Network Detection"
create_label "stage-6" "d4c5f9" "Stage 6: RSSI Proximity Thresholding"
create_label "stage-7" "d4c5f9" "Stage 7: Relay Control Logic"
create_label "stage-8" "d4c5f9" "Stage 8: Final Hardware Integration"

echo -e "\n${GREEN}All labels are ready${NC}\n"

# Check if this is a dry run
if [ "$1" == "--dry-run" ]; then
    echo -e "${YELLOW}Running in DRY RUN mode...${NC}\n"
    python scripts/create_issues.py --dry-run
else
    echo "Creating GitHub issues..."
    echo -e "${YELLOW}Press Ctrl+C now if you want to cancel...${NC}"
    sleep 3
    echo ""
    python scripts/create_issues.py
fi
