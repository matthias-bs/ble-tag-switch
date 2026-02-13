#!/usr/bin/env python3
"""
Script to create GitHub issues from IMPLEMENTATION_PLAN.md using GitHub API.

This script uses the GITHUB_TOKEN environment variable for authentication.

Usage:
    export GITHUB_TOKEN="your_token_here"
    python scripts/create_issues_api.py [--dry-run]

Or with gh CLI:
    GH_TOKEN=$(gh auth token) python scripts/create_issues_api.py
"""

import re
import sys
import os
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


class Stage:
    """Represents a single implementation stage."""
    
    def __init__(self, number, title, sketch, purpose, content):
        self.number = number
        self.title = title
        self.sketch = sketch
        self.purpose = purpose
        self.content = content
    
    def to_issue_title(self):
        """Generate issue title."""
        return f"Stage {self.number}: {self.title}"
    
    def to_issue_body(self):
        """Generate issue body in markdown format."""
        body = f"## {self.title}\n\n"
        body += f"**Sketch**: `{self.sketch}`\n\n"
        body += f"**Purpose**: {self.purpose}\n\n"
        body += "---\n\n"
        body += self.content.strip()
        body += "\n\n---\n\n"
        body += f"*This issue is part of the implementation plan. See [IMPLEMENTATION_PLAN.md](../blob/main/IMPLEMENTATION_PLAN.md) for full context.*"
        return body
    
    def to_labels(self):
        """Generate labels for the issue."""
        labels = ["implementation", f"stage-{self.number}"]
        if self.number == 1:
            labels.append("good first issue")
        return labels


def parse_implementation_plan(file_path):
    """Parse IMPLEMENTATION_PLAN.md and extract stages."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the Implementation Stages section
    stages_match = re.search(r'## Implementation Stages\n\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not stages_match:
        raise ValueError("Could not find 'Implementation Stages' section")
    
    stages_content = stages_match.group(1)
    
    # Split by stage markers (### Stage N:)
    stage_pattern = r'### Stage (\d+): ([^\n]+)\n\*\*Sketch: `([^`]+)`\*\*\n\n\*\*Purpose\*\*: ([^\n]+)\n(.*?)(?=\n---\n\n### Stage |\n---\n\n## |\Z)'
    
    stages = []
    for match in re.finditer(stage_pattern, stages_content, re.DOTALL):
        stage_num = int(match.group(1))
        title = match.group(2).strip()
        sketch = match.group(3).strip()
        purpose = match.group(4).strip()
        stage_content = match.group(5).strip()
        
        stages.append(Stage(stage_num, title, sketch, purpose, stage_content))
    
    return stages


def create_issue_with_api(stage, owner, repo, token, dry_run=False):
    """Create a GitHub issue using REST API."""
    title = stage.to_issue_title()
    body = stage.to_issue_body()
    labels = stage.to_labels()
    
    if dry_run:
        print(f"\n{'='*80}")
        print(f"ISSUE {stage.number}: {title}")
        print(f"{'='*80}")
        print(f"Labels: {', '.join(labels)}")
        print(f"\n{body}")
        return True
    
    # Create issue using GitHub REST API
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    data = {
        "title": title,
        "body": body,
        "labels": labels
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    try:
        request = Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        with urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✓ Created issue for Stage {stage.number}: {title}")
            print(f"  URL: {result['html_url']}")
            return True
    except HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"✗ Failed to create issue for Stage {stage.number}: {e}")
        print(f"  Error: {error_body}")
        return False
    except Exception as e:
        print(f"✗ Failed to create issue for Stage {stage.number}: {e}")
        return False


def main():
    """Main function."""
    # Parse command line arguments
    dry_run = "--dry-run" in sys.argv
    
    # Get GitHub token from environment
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN') or os.environ.get('github_mcp_pat')
    
    if not token and not dry_run:
        print("✗ GITHUB_TOKEN or GH_TOKEN environment variable not set")
        print("\nTo use this script, set the token:")
        print("  export GITHUB_TOKEN='your_token_here'")
        print("\nOr use gh CLI:")
        print("  GH_TOKEN=$(gh auth token) python scripts/create_issues_api.py")
        print("\nOr run in dry-run mode:")
        print("  python scripts/create_issues_api.py --dry-run")
        sys.exit(1)
    
    # Find the IMPLEMENTATION_PLAN.md file
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    plan_file = repo_root / "IMPLEMENTATION_PLAN.md"
    
    if not plan_file.exists():
        print(f"✗ Could not find IMPLEMENTATION_PLAN.md at {plan_file}")
        sys.exit(1)
    
    # Parse owner and repo from git config
    owner = "matthias-bs"  # Default owner
    repo = "ble-tag-switch"  # Default repo
    
    print(f"Parsing {plan_file}...")
    stages = parse_implementation_plan(plan_file)
    print(f"Found {len(stages)} stages")
    print(f"Target repository: {owner}/{repo}\n")
    
    if dry_run:
        print("DRY RUN MODE - No issues will be created")
    
    # Create issues for each stage
    success_count = 0
    for stage in stages:
        if create_issue_with_api(stage, owner, repo, token, dry_run):
            success_count += 1
    
    print(f"\n{'='*80}")
    if dry_run:
        print(f"Dry run complete. {success_count}/{len(stages)} stages ready to be created as issues.")
        print("\nTo create the issues, run:")
        print("  GH_TOKEN=$(gh auth token) python scripts/create_issues_api.py")
    else:
        print(f"Created {success_count}/{len(stages)} issues successfully.")
    
    sys.exit(0 if success_count == len(stages) else 1)


if __name__ == "__main__":
    main()
