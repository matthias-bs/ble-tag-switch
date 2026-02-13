# Issue Creation Testing Guide

This document describes how to test and verify the issue creation scripts.

## Prerequisites Check

Before running any scripts, verify you have the necessary tools:

```bash
# Check Python version (need 3.6+)
python --version

# Check if GitHub CLI is installed (optional, for Method 2)
gh --version

# Check if required environment variables are set
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:-(not set)}"
echo "GH_TOKEN: ${GH_TOKEN:-(not set)}"
echo "github_mcp_pat: ${github_mcp_pat:-(not set)}"
```

## Testing Methods

### Method 1: Dry Run Test (Always Run This First)

Test all scripts in dry-run mode to preview what will be created:

```bash
# Test the shell script
bash scripts/create_issues.sh --dry-run

# Test the Python CLI script
python scripts/create_issues.py --dry-run

# Test the API script
python scripts/create_issues_api.py --dry-run

# Test the JSON export
python scripts/export_issues_json.py
python scripts/create_issues_from_json.py  # Will fail without token but shows format
```

### Method 2: Using GitHub Actions Workflow

**This is the recommended method for actually creating the issues.**

1. Push your changes to GitHub
2. Go to: https://github.com/matthias-bs/ble-tag-switch/actions
3. Select "Create Implementation Issues" workflow
4. Click "Run workflow"
5. Choose `dry_run: true` for a test run
6. Review the workflow logs
7. If everything looks good, run again with `dry_run: false`

### Method 3: Using GitHub CLI Locally

If you have `gh` CLI installed and authenticated:

```bash
# Authenticate if needed
gh auth login

# Run the shell script (it will create labels and issues)
bash scripts/create_issues.sh

# Or use Python script directly
python scripts/create_issues.py
```

### Method 4: Using API with Token

If you have a GitHub Personal Access Token:

```bash
# Set the token
export GITHUB_TOKEN="your_token_here"

# Or if using gh CLI
export GITHUB_TOKEN=$(gh auth token)

# Run the API script
python scripts/create_issues_api.py

# Or use the JSON-based script
python scripts/create_issues_from_json.py
```

### Method 5: Manual Creation

If all automated methods fail, use the manual guide:

```bash
# View the manual guide
cat scripts/MANUAL_ISSUE_CREATION.md

# Then manually create issues by copy-pasting from the guide
```

## Verification Steps

After creating issues (by any method), verify:

```bash
# List all issues in the repository
gh issue list --limit 100

# Or check on GitHub web:
# https://github.com/matthias-bs/ble-tag-switch/issues
```

Expected results:
- 8 issues created
- Each titled "Stage N: [Stage Name]"
- Each with appropriate labels (implementation, stage-N)
- Stage 1 should also have "good first issue" label

## Troubleshooting

### "No GitHub token found"

**Solution:**
- Use the GitHub Actions workflow (Method 2) - it has built-in authentication
- Or set a token: `export GITHUB_TOKEN="your_token"`
- Or use gh CLI: `export GITHUB_TOKEN=$(gh auth token)`

### "GitHub CLI not found"

**Solution:**
- Install gh: https://cli.github.com/
- Or use Method 2 (GitHub Actions)
- Or use Method 4 (API with token)

### "Label does not exist"

**Solution:**
The shell script (Method 3) automatically creates labels. For other methods:

```bash
# Create labels manually
bash scripts/create_issues.sh --dry-run  # This creates labels even in dry-run
```

Or create them via API:

```bash
# Create implementation label
gh label create "implementation" --color "0e8a16" --description "Implementation tasks"

# Create stage labels
for i in {1..8}; do
  gh label create "stage-$i" --color "d4c5f9" --description "Stage $i"
done
```

### "Permission denied"

**Solution:**
- Ensure your token has `repo` scope
- Ensure scripts are executable: `chmod +x scripts/*.py scripts/*.sh`

## Success Criteria

✅ All 8 issues created successfully
✅ Each issue has correct title format
✅ Each issue has correct labels
✅ Issue bodies contain stage details
✅ Links to IMPLEMENTATION_PLAN.md work

## Cleaning Up Test Issues

If you created test issues and want to clean them up:

```bash
# List issues
gh issue list

# Close an issue
gh issue close <issue_number>

# Or close all implementation issues
gh issue list --label "implementation" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {}
```

## Notes

- All scripts support `--dry-run` for testing
- The GitHub Actions workflow is the most reliable method
- Manual creation is always available as a fallback
- The JSON export creates `scripts/issues.json` for batch operations
