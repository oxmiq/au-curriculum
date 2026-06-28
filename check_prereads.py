#!/usr/bin/env python3
"""
Check pre-read references in lesson files.
- Each module lesson should have a "Pre-reading:" field at the top
- Each module lesson should have a "Pre-read for tomorrow" section at the end
- The pre-read at end of Day N should match the Pre-reading at beginning of Day N+1
"""

import re
import os
from pathlib import Path

LESSONS_DIR = Path("/Users/shiva/Documents/vscode/oxmiq/projects/au-curriculum/docs/lessons")

def get_pre_reading_top(content):
    """Extract the Pre-reading field from the top of the lesson."""
    # Look for > **Pre-reading:** <citation> or "none"
    match = re.search(r'> \*\*Pre-reading:\*\* (.+)', content)
    if match:
        return match.group(1).strip()
    return None

def get_pre_read_bottom(content):
    """Extract the Pre-read for tomorrow section from the bottom."""
    # Look for ### Pre-read for tomorrow (Day NN · <Topic>)
    # followed by - **Resource:** <citation>
    match = re.search(r'### Pre-read for tomorrow.*?\n.*?\*\*Resource:\*\* (.+)', content, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Also check for legacy format without Resource label
    match = re.search(r'### Pre-read for tomorrow.*?\n(.*?)(?:\n## |\Z)', content, re.DOTALL)
    if match:
        lines = match.group(1).strip().split('\n')
        # Look for a line that looks like a resource/citation
        for line in lines:
            if '**Resource:**' in line:
                continue
            if line.strip() and not line.startswith('#') and not line.startswith('- '):
                return line.strip()
            # Handle bullet points with resource
            if line.strip().startswith('- '):
                text = line.strip()[2:]
                if text and not text.startswith('**'):
                    return text
    return None

def get_next_day_info(content):
    """Extract the next day info from Pre-read for tomorrow section."""
    match = re.search(r'### Pre-read for tomorrow \(Day (\d+)', content)
    if match:
        return int(match.group(1))
    return None

def get_module_info(path):
    """Extract week and module from path."""
    # path looks like: docs/lessons/week-01/module-1/index.md
    parts = path.relative_to(LESSONS_DIR).parts
    if len(parts) >= 2:
        week = parts[0]  # week-01
        module = parts[1]  # module-1
        return week, module
    return None, None

def parse_module_num(module_str):
    """Extract module number from module-N string."""
    match = re.search(r'module-(\d+)', module_str)
    if match:
        return int(match.group(1))
    return None

def main():
    issues = []

    # Get all module index files (not week overviews)
    module_files = sorted(LESSONS_DIR.glob("week-*/module-*/index.md"))

    # Build a map of (week, module_num) -> {top_preread, bottom_preread, next_day}
    module_data = {}

    for f in module_files:
        week, module = get_module_info(f)
        if not week or not module:
            continue

        module_num = parse_module_num(module)
        if not module_num:
            continue

        content = f.read_text()

        top_preread = get_pre_reading_top(content)
        bottom_preread = get_pre_read_bottom(content)
        next_day = get_next_day_info(content)

        key = (week, module_num)
        module_data[key] = {
            'file': str(f),
            'top_preread': top_preread,
            'bottom_preread': bottom_preread,
            'next_day': next_day,
            'week': week,
            'module': module,
            'module_num': module_num
        }

    # Check each module
    for key, data in sorted(module_data.items()):
        week, module_num = key

        # Check 1: Has Pre-reading at top
        if not data['top_preread']:
            issues.append(f"❌ {data['week']}/{data['module']}: Missing Pre-reading at top")

        # Check 2: Has Pre-read for tomorrow at bottom
        if not data['bottom_preread']:
            issues.append(f"❌ {data['week']}/{data['module']}: Missing 'Pre-read for tomorrow' at bottom")

        # Check 3: Cross-reference with next day
        if data['next_day']:
            next_key = (week, data['next_day'])
            if next_key in module_data:
                next_data = module_data[next_key]
                current_bottom = data['bottom_preread']
                next_top = next_data['top_preread']

                if current_bottom and next_top:
                    # Normalize for comparison (lowercase, strip)
                    curr_norm = current_bottom.lower().strip()
                    next_norm = next_top.lower().strip()

                    # Check if they match (or are both "none")
                    if curr_norm != next_norm:
                        # Check if both indicate "none"
                        if not ("none" in curr_norm and "none" in next_norm):
                            issues.append(f"⚠️  {data['week']}/{data['module']} -> {next_key[0]}/module-{next_key[1]}: Mismatch")
                            issues.append(f"    Bottom: {current_bottom}")
                            issues.append(f"    Top: {next_top}")

    # Also check week transitions
    # Module 4 in week N should point to Module 1 in week N+1
    for week_num in range(1, 10):
        current_week = f"week-{week_num:02d}"
        next_week = f"week-{week_num+1:02d}"

        current_key = (current_week, 4)
        next_key = (next_week, 1)

        if current_key in module_data and next_key in module_data:
            curr_data = module_data[current_key]
            next_data = module_data[next_key]

            curr_bottom = curr_data['bottom_preread']
            next_top = next_data['top_preread']

            if curr_bottom and next_top:
                curr_norm = curr_bottom.lower().strip()
                next_norm = next_top.lower().strip()

                if curr_norm != next_norm:
                    if not ("none" in curr_norm and "none" in next_norm):
                        issues.append(f"⚠️  {current_week}/module-4 -> {next_week}/module-1: Week transition mismatch")
                        issues.append(f"    Bottom: {curr_bottom}")
                        issues.append(f"    Top: {next_top}")

    # Report results
    print("=" * 60)
    print("PRE-READ REFERENCE AUDIT")
    print("=" * 60)

    if issues:
        print(f"\nFound {len(issues)} issues:\n")
        for issue in issues:
            print(issue)
    else:
        print("\n✅ All pre-read references are consistent!")

    # Summary stats
    total_modules = len(module_data)
    with_top = sum(1 for d in module_data.values() if d['top_preread'])
    with_bottom = sum(1 for d in module_data.values() if d['bottom_preread'])

    print(f"\n--- Summary ---")
    print(f"Total modules: {total_modules}")
    print(f"Modules with Pre-reading at top: {with_top}/{total_modules}")
    print(f"Modules with Pre-read for tomorrow at bottom: {with_bottom}/{total_modules}")

if __name__ == "__main__":
    main()