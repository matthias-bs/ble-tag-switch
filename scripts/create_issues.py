#!/usr/bin/env python3
"""
Script to create GitHub issues from IMPLEMENTATION_PLAN.md stages.

This script parses the IMPLEMENTATION_PLAN.md file and creates GitHub issues
for each implementation stage using the GitHub CLI (gh).

Usage:
    python scripts/create_issues.py [--dry-run]

Options:
    --dry-run    Print issue content without creating actual issues
"""

import re
import sys
import subprocess
import os
from pathlib import Path


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


def create_issue_with_gh(stage, dry_run=False):
    """Create a GitHub issue using gh CLI."""
    title = stage.to_issue_title()
    body = stage.to_issue_body()
    labels = ",".join(stage.to_labels())
    
    if dry_run:
        print(f"\n{'='*80}")
        print(f"ISSUE {stage.number}: {title}")
        print(f"{'='*80}")
        print(f"Labels: {labels}")
        print(f"\n{body}")
        return True
    
    try:
        # Create issue using gh CLI
        cmd = [
            "gh", "issue", "create",
            "--title", title,
            "--body", body,
            "--label", labels
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Created issue for Stage {stage.number}: {title}")
        print(f"  URL: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create issue for Stage {stage.number}: {e}")
        print(f"  Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ GitHub CLI (gh) not found. Please install it first:")
        print("  https://cli.github.com/")
        return False


def main():
    """Main function."""
    # Parse command line arguments
    dry_run = "--dry-run" in sys.argv
    
    # Find the IMPLEMENTATION_PLAN.md file
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    plan_file = repo_root / "IMPLEMENTATION_PLAN.md"
    
    if not plan_file.exists():
        print(f"✗ Could not find IMPLEMENTATION_PLAN.md at {plan_file}")
        sys.exit(1)
    
    # Change to repo root for gh CLI
    os.chdir(repo_root)
    
    print(f"Parsing {plan_file}...")
    stages = parse_implementation_plan(plan_file)
    print(f"Found {len(stages)} stages\n")
    
    if dry_run:
        print("DRY RUN MODE - No issues will be created")
    
    # Create issues for each stage
    success_count = 0
    for stage in stages:
        if create_issue_with_gh(stage, dry_run):
            success_count += 1
    
    print(f"\n{'='*80}")
    if dry_run:
        print(f"Dry run complete. {success_count}/{len(stages)} stages ready to be created as issues.")
        print("\nTo create the issues, run:")
        print("  python scripts/create_issues.py")
    else:
        print(f"Created {success_count}/{len(stages)} issues successfully.")
    
    sys.exit(0 if success_count == len(stages) else 1)


if __name__ == "__main__":
    main()
