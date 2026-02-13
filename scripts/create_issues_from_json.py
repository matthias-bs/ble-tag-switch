#!/usr/bin/env python3
"""
Simple script to create GitHub issues from the exported JSON file.
This reads issues.json and creates them one by one.
"""

import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def create_issue(owner, repo, token, issue_data):
    """Create a single GitHub issue."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    try:
        request = Request(url, data=json.dumps(issue_data).encode('utf-8'), headers=headers, method='POST')
        with urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            return True, result['html_url'], result['number']
    except HTTPError as e:
        error_body = e.read().decode('utf-8')
        return False, f"HTTP {e.code}: {error_body}", None
    except Exception as e:
        return False, str(e), None


def main():
    """Main function."""
    # Get GitHub token from environment
    token = (os.environ.get('GITHUB_TOKEN') or 
             os.environ.get('GH_TOKEN') or 
             os.environ.get('github_mcp_pat') or
             os.environ.get('GITHUB_PAT'))
    
    if not token:
        print("✗ No GitHub token found in environment variables")
        print("\nTried: GITHUB_TOKEN, GH_TOKEN, github_mcp_pat, GITHUB_PAT")
        print("\nPlease set one of these environment variables:")
        print("  export GITHUB_TOKEN='your_token_here'")
        print("\nOr use the GitHub Actions workflow instead:")
        print("  Go to Actions → Create Implementation Issues → Run workflow")
        return 1
    
    # Find the issues JSON file
    script_dir = Path(__file__).parent
    json_file = script_dir / "issues.json"
    
    if not json_file.exists():
        print(f"✗ Could not find issues.json at {json_file}")
        print("\nRun this first to generate the JSON:")
        print("  python scripts/export_issues_json.py")
        return 1
    
    # Load issues
    with open(json_file, 'r', encoding='utf-8') as f:
        issues = json.load(f)
    
    owner = "matthias-bs"
    repo = "ble-tag-switch"
    
    print(f"Creating {len(issues)} issues in {owner}/{repo}...\n")
    
    created_issues = []
    failed_issues = []
    
    for issue_data in issues:
        title = issue_data['title']
        print(f"Creating: {title}...", end=" ")
        
        success, result, number = create_issue(owner, repo, token, issue_data)
        
        if success:
            print(f"✓ Created #{number}")
            print(f"  {result}")
            created_issues.append((number, title, result))
        else:
            print(f"✗ Failed")
            print(f"  {result}")
            failed_issues.append((title, result))
    
    # Summary
    print(f"\n{'='*80}")
    print(f"Summary:")
    print(f"  Created: {len(created_issues)}/{len(issues)}")
    print(f"  Failed: {len(failed_issues)}/{len(issues)}")
    
    if created_issues:
        print(f"\n✓ Successfully created issues:")
        for number, title, url in created_issues:
            print(f"  #{number}: {title}")
    
    if failed_issues:
        print(f"\n✗ Failed to create:")
        for title, error in failed_issues:
            print(f"  - {title}")
            print(f"    Error: {error}")
    
    return 0 if len(failed_issues) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
