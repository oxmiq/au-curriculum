#!/usr/bin/env python3
"""
Check pre-read references in lesson files (improved version).

Categories:
- Regular days (weeks 1-9, modules 1-4): SHOULD have Pre-reading at top AND Pre-read for tomorrow at bottom
- Consolidation days (weeks 1-9, module 5): Should NOT have Pre-reading (review day)
- Capstone days (week 10): Different format (Source template), no pre-reads expected
"""

import re
import os
from pathlib import Path

LESSONS_DIR = Path("/Users/shiva/Documents/vscode/oxmiq/projects/au-curriculum/docs/lessons")

def get_pre_reading_top(content):
    """Extract the Pre-reading field from the top of the lesson.

    Checks for two formats:
    1. Separate line: > **Pre-reading:** <citation>
    2. Embedded in concept: **Pre-reading:** <citation> embedded in concept line
    """
    # Format 1: Separate line
    match = re.search(r'> \*\*Pre-reading:\*\* (.+)', content)
    if match:
        return match.group(1).strip()

    # Format 2: Embedded in concept line
    match = re.search(r'\*\*Pre-reading:\*\* (.+?)(?:\.|$)', content)
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

def get_module_type(week_num, module_num):
    """Determine what type of module this is."""
    if week_num == 10:
        return "capstone"
    elif module_num == 5:
        return "consolidation"
    else:
        return "regular"

def main():
    issues = []
    correct = []

    # Get all module index files (not week overviews)
    module_files = sorted(LESSONS_DIR.glob("week-*/module-*/index.md"))

    # Build a map of (week, module_num) -> {top_preread, bottom_preread, next_day}
    module_data = {}

    for f in module_files:
        # Extract week and module from path
        parts = f.relative_to(LESSONS_DIR).parts
        if len(parts) < 2:
            continue

        week = parts[0]  # week-01
        module = parts[1]  # module-1

        # Parse week number
        week_match = re.search(r'week-(\d+)', week)
        if not week_match:
            continue
        week_num = int(week_match.group(1))

        # Parse module number
        module_match = re.search(r'module-(\d+)', module)
        if not module_match:
            continue
        module_num = int(module_match.group(1))

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
            'module_num': module_num,
            'week_num': week_num,
            'type': get_module_type(week_num, module_num)
        }

    # Check each module against its expected type
    for key, data in sorted(module_data.items()):
        week_num = data['week_num']
        module_num = data['module_num']
        module_type = data['type']

        if module_type == "regular":
            # Regular days should have both top and bottom pre-reads
            if not data['top_preread']:
                issues.append(f"❌ {data['week']}/{data['module']} (regular): Missing Pre-reading at top")
            else:
                correct.append(f"✅ {data['week']}/{data['module']}: Has Pre-reading at top")

            if not data['bottom_preread']:
                issues.append(f"❌ {data['week']}/{data['module']} (regular): Missing 'Pre-read for tomorrow' at bottom")
            else:
                correct.append(f"✅ {data['week']}/{data['module']}: Has Pre-read for tomorrow at bottom")

        elif module_type == "consolidation":
            # Consolidation days should NOT have pre-reads (they're review days)
            if data['top_preread']:
                issues.append(f"⚠️  {data['week']}/{data['module']} (consolidation): Should NOT have Pre-reading at top (it's a review day)")
            else:
                correct.append(f"✅ {data['week']}/{data['module']} (consolidation): Correctly has no Pre-reading")

            if data['bottom_preread']:
                issues.append(f"⚠️  {data['week']}/{data['module']} (consolidation): Should NOT have 'Pre-read for tomorrow' (it's a review day)")
            else:
                correct.append(f"✅ {data['week']}/{data['module']} (consolidation): Correctly has no Pre-read for tomorrow")

        elif module_type == "capstone":
            # Capstone days have different format
            if data['top_preread']:
                issues.append(f"⚠️  {data['week']}/{data['module']} (capstone): Has Pre-reading but should use Source template format")
            else:
                correct.append(f"✅ {data['week']}/{data['module']} (capstone): Correct format (no Pre-reading)")

    # Check cross-references for regular days
    print("\n" + "=" * 60)
    print("CROSS-REFERENCE CHECKS (matching pre-reads between days)")
    print("=" * 60)

    cross_ref_issues = []
    for key, data in sorted(module_data.items()):
        if data['type'] != "regular":
            continue

        week = data['week']
        week_num = data['week_num']
        module_num = data['module_num']

        # Determine next day
        if module_num < 4:
            next_key = (week, module_num + 1)
        elif module_num == 4:
            # Next week, module 1
            next_week = f"week-{week_num + 1:02d}"
            next_key = (next_week, 1)
        else:
            continue

        if next_key in module_data:
            next_data = module_data[next_key]
            curr_bottom = data['bottom_preread']
            next_top = next_data['top_preread']

            if curr_bottom and next_top:
                # Extract just the URL/citation part for comparison
                # Remove reflection questions etc that might be at the bottom
                curr_clean = curr_bottom.split('**Reflection')[0].split('---')[0].strip()
                next_clean = next_top.strip()

                # Simple comparison - just check if they reference the same source
                curr_lower = curr_clean.lower()
                next_lower = next_clean.lower()

                # Check if URLs match
                curr_urls = re.findall(r'href="([^"]+)"', curr_clean)
                next_urls = re.findall(r'href="([^"]+)"', next_clean)

                if curr_urls and next_urls:
                    if curr_urls[0] != next_urls[0]:
                        cross_ref_issues.append(f"⚠️  {week}/module-{module_num} -> {next_key[0]}/module-{next_key[1]}: URL mismatch")
                        cross_ref_issues.append(f"    Bottom URL: {curr_urls[0]}")
                        cross_ref_issues.append(f"    Top URL: {next_urls[0]}")
                elif curr_clean != next_clean:
                    # Text comparison as fallback
                    if curr_lower != next_lower:
                        # Allow for minor differences like "(~20 min)" vs "(~20 min, read the X section)"
                        if not (curr_lower.split('(')[0] == next_lower.split('(')[0]):
                            cross_ref_issues.append(f"⚠️  {week}/module-{module_num} -> {next_key[0]}/module-{next_key[1]}: Content mismatch")
                            cross_ref_issues.append(f"    Bottom: {curr_clean[:100]}...")
                            cross_ref_issues.append(f"    Top: {next_clean[:100]}...")

    if cross_ref_issues:
        issues.extend(cross_ref_issues)
    else:
        print("✅ All cross-references are consistent!")

    # Report results
    print("\n" + "=" * 60)
    print("PRE-READ REFERENCE AUDIT RESULTS")
    print("=" * 60)

    if issues:
        print(f"\nFound {len(issues)} issues:\n")
        for issue in issues:
            print(issue)
    else:
        print("\n✅ All pre-read references are consistent!")

    # Summary stats
    regular_modules = [d for d in module_data.values() if d['type'] == 'regular']
    consolidation_modules = [d for d in module_data.values() if d['type'] == 'consolidation']
    capstone_modules = [d for d in module_data.values() if d['type'] == 'capstone']

    print(f"\n--- Summary ---")
    print(f"Total modules: {len(module_data)}")
    print(f"  Regular days (need pre-reads): {len(regular_modules)}")
    print(f"  Consolidation days (no pre-reads): {len(consolidation_modules)}")
    print(f"  Capstone days (different format): {len(capstone_modules)}")

    regular_with_top = sum(1 for d in regular_modules if d['top_preread'])
    regular_with_bottom = sum(1 for d in regular_modules if d['bottom_preread'])

    print(f"\n--- Regular Days Analysis ---")
    print(f"Have Pre-reading at top: {regular_with_top}/{len(regular_modules)}")
    print(f"Have Pre-read for tomorrow at bottom: {regular_with_bottom}/{len(regular_modules)}")

if __name__ == "__main__":
    main()