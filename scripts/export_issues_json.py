#!/usr/bin/env python3
"""
Script to export issues as JSON for batch creation.
This creates a JSON file that can be used with GitHub CLI or API.
"""

import json
import re
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
    
    def to_dict(self):
        """Convert to dictionary for JSON export."""
        return {
            "title": self.to_issue_title(),
            "body": self.to_issue_body(),
            "labels": self.to_labels()
        }


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


def main():
    """Main function."""
    # Find the IMPLEMENTATION_PLAN.md file
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    plan_file = repo_root / "IMPLEMENTATION_PLAN.md"
    
    if not plan_file.exists():
        print(f"✗ Could not find IMPLEMENTATION_PLAN.md at {plan_file}")
        return 1
    
    print(f"Parsing {plan_file}...")
    stages = parse_implementation_plan(plan_file)
    print(f"Found {len(stages)} stages\n")
    
    # Export as JSON
    issues_data = [stage.to_dict() for stage in stages]
    
    output_file = repo_root / "scripts" / "issues.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(issues_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Exported {len(issues_data)} issues to {output_file}")
    print(f"\nYou can now create these issues using:")
    print(f"  - The GitHub Actions workflow (recommended)")
    print(f"  - GitHub CLI: cat scripts/issues.json | jq -r '.[] | @json' | while read issue; do gh issue create --title \"$(echo $issue | jq -r '.title')\" --body \"$(echo $issue | jq -r '.body')\" --label \"$(echo $issue | jq -r '.labels | join(\",\")')\"; done")
    print(f"  - The provided Python scripts: python scripts/create_issues_api.py")
    
    return 0


if __name__ == "__main__":
    exit(main())
