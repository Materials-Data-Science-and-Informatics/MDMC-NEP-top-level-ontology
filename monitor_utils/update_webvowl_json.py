#!/usr/bin/env python3
"""
Script to update WebVOWL folder with a JSON file exported from WebVOWL website.

This script:
1. Copies the JSON file to the correct location in webvowl/data/
2. Optionally sets up the webvowl folder structure if it doesn't exist
3. Optionally updates the menu in webvowl/index.html

Usage:
    python update_webvowl_json.py <json_file> [--module <module>] [--webvowl-dir <dir>] [--ontology-id <id>] [--ontology-name <name>]
    
Examples:
    # Simple usage - auto-detects module and version
    python update_webvowl_json.py exported-ontology.json --module core
    
    # For ver_3_0 modules (default)
    python update_webvowl_json.py exported-ontology.json --module core --version 3_0
    
    # Explicit path
    python update_webvowl_json.py exported-ontology.json --webvowl-dir PRIMA/core/ver_3_0/webvowl --ontology-id prima-core
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional


def setup_webvowl_structure(
    webvowl_dir: Path,
    reference_webvowl: Optional[Path] = None
) -> bool:
    """
    Set up the webvowl folder structure.
    
    If reference_webvowl is provided, copy static files from there.
    Otherwise, create minimal structure.
    
    Args:
        webvowl_dir: Target webvowl directory
        reference_webvowl: Optional reference webvowl folder to copy from
        
    Returns:
        True if successful
    """
    webvowl_dir.mkdir(parents=True, exist_ok=True)
    
    # Create data directory
    data_dir = webvowl_dir / "data"
    data_dir.mkdir(exist_ok=True)
    
    # If reference folder provided, copy static files
    if reference_webvowl and reference_webvowl.exists():
        print(f"Copying WebVOWL static files from {reference_webvowl}...")
        
        # Copy CSS, JS, and other static files (but not data folder)
        static_files = [
            "css",
            "js",
            "favicon.ico",
            "license.txt",
            "index.html"
        ]
        
        for item in static_files:
            src = reference_webvowl / item
            dst = webvowl_dir / item
            
            if src.exists():
                if src.is_dir():
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
                print(f"  ✓ Copied {item}")
        return True
    
    return False


def update_webvowl_index(
    webvowl_dir: Path,
    ontology_name: str,
    ontology_id: str
) -> bool:
    """
    Update webvowl/index.html to include the ontology in the menu.
    
    Args:
        webvowl_dir: Path to webvowl directory
        ontology_name: Display name for the ontology
        ontology_id: ID for the ontology (e.g., "prima-core", "mno-core")
        
    Returns:
        True if successful
    """
    index_file = webvowl_dir / "index.html"
    
    if not index_file.exists():
        print(f"Warning: {index_file} not found, skipping menu update")
        return False
    
    try:
        # Read the file
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace (not append) the first ontology menu entry in WebVOWL's menu.
        # This avoids accumulating duplicates each time the script is run.
        menu_start = '<ul id="m_select" class="toolTipMenu noselect">'
        # We use the same identifier as the data file/hash fragment: prima-{module}
        # (no "mno-" namespace).
        first_entry_prefix = '                    <li><a href="#'
        new_entry = f'                    <li><a href="#{ontology_id}" id="{ontology_id}">{ontology_name}</a></li>'

        if menu_start not in content:
            print("  Warning: Could not find ontology menu (<ul id=\"m_select\">) in index.html")
            return False

        menu_pos = content.find(menu_start)
        first_li_pos = content.find(first_entry_prefix, menu_pos)
        if first_li_pos == -1:
            print("  Warning: Could not find first ontology <li> entry to update in index.html")
            return False

        line_end = content.find("\n", first_li_pos)
        if line_end == -1:
            print("  Warning: Unexpected index.html format (no newline after first menu entry)")
            return False

        existing_line = content[first_li_pos:line_end]
        # Replace first entry if needed (but even if it's already correct, we still do cleanup below).
        replaced = False
        if existing_line != new_entry:
            content = content[:first_li_pos] + new_entry + content[line_end:]
            replaced = True

        # Remove any additional duplicate occurrences of the same entry (from older script runs),
        # even if indentation differs.
        lines = content.splitlines(keepends=False)
        kept: list[str] = []
        seen = 0
        marker = f'href="#{ontology_id}" id="{ontology_id}"'
        for line in lines:
            if marker in line:
                seen += 1
                if seen > 1:
                    continue
            kept.append(line)
        cleaned = "\n".join(kept) + ("\n" if content.endswith("\n") else "")
        cleaned_changed = (cleaned != content)
        content = cleaned

        if replaced or cleaned_changed:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  ✓ Updated menu in index.html")
        else:
            print("  Menu entry already up-to-date")
        return True
        
    except Exception as e:
        print(f"  Error updating index.html: {e}")
        return False


def infer_ontology_info(json_file: Path, webvowl_dir: Path) -> tuple[str, str]:
    """
    Try to infer ontology name and ID from context.
    
    Args:
        json_file: Path to JSON file
        webvowl_dir: Path to webvowl directory
        
    Returns:
        Tuple of (ontology_name, ontology_id)
    """
    # Try to infer from JSON file name
    json_stem = json_file.stem
    
    # Try to infer from directory structure
    # e.g., PRIMA/core/ver_2_0/webvowl -> prima-core
    # e.g., PRIMA/core/ver_3_0/webvowl -> prima-core
    webvowl_parent = webvowl_dir.parent
    if webvowl_parent.name.startswith('ver_'):
        module_dir = webvowl_parent.parent
        module_name = module_dir.name
        version = webvowl_parent.name  # ver_2_0 or ver_3_0
        
        # Map directory names to ontology IDs
        module_map = {
            'core': 'prima-core',
            'experiment': 'prima-experiment',
            'dataset': 'prima-dataset',
            'data-analysis-lifecycle': 'prima-data-analysis-lifecycle',
            'computational': 'prima-computational',
            'complete': 'prima-complete'
        }
        
        ontology_id = module_map.get(module_name, json_stem)
        # Include version in name if it's ver_3_0
        if version == 'ver_3_0':
            ontology_name = f"PRIMA Ontology - {module_name.replace('-', ' ').title()} (v3.0)"
        else:
            ontology_name = f"PRIMA Ontology - {module_name.replace('-', ' ').title()}"
        
        return ontology_name, ontology_id
    
    # Fallback to JSON filename
    ontology_id = json_stem.replace('_', '-')
    ontology_name = json_stem.replace('_', ' ').title()
    
    return ontology_name, ontology_id


def main():
    """Main entry point."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(
        description="Update WebVOWL folder with JSON file exported from WebVOWL website"
    )
    parser.add_argument(
        "json_file",
        type=Path,
        help="Path to JSON file exported from WebVOWL website"
    )
    parser.add_argument(
        "--module",
        choices=["core", "experiment", "dataset", "data-analysis-lifecycle", "computational", "complete"],
        help="PRIMA module name (auto-detects webvowl directory in ver_3_0)"
    )
    parser.add_argument(
        "--version",
        default="3_0",
        help="Version directory (default: 3_0 for ver_3_0)"
    )
    parser.add_argument(
        "--webvowl-dir",
        type=Path,
        help="Path to webvowl directory (default: infer from --module or JSON file location)"
    )
    parser.add_argument(
        "--ontology-id",
        help="ID for the ontology (e.g., 'prima-core'). Default: inferred from filename or directory"
    )
    parser.add_argument(
        "--ontology-name",
        help="Display name for the ontology. Default: inferred from directory or filename"
    )
    parser.add_argument(
        "--reference-webvowl",
        type=Path,
        help="Reference webvowl folder to copy static files from (if webvowl dir doesn't exist)"
    )
    parser.add_argument(
        "--no-menu-update",
        action="store_true",
        help="Skip updating the menu in index.html"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not args.json_file.exists():
        print(f"Error: JSON file not found: {args.json_file}")
        sys.exit(1)
    
    # Validate JSON file
    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✓ Validated JSON file: {args.json_file}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file: {e}")
        sys.exit(1)
    
    # Determine webvowl directory
    if args.webvowl_dir:
        webvowl_dir = args.webvowl_dir
    elif args.module:
        # Build path from module name and version
        base_path = Path(__file__).parent.parent
        version_dir = f"ver_{args.version}"
        webvowl_dir = base_path / "PRIMA" / args.module / version_dir / "webvowl"
        print(f"Using module path: PRIMA/{args.module}/{version_dir}/webvowl")
    else:
        # Try to infer from JSON file location
        json_parent = args.json_file.parent
        if json_parent.name == "data" and (json_parent.parent / "index.html").exists():
            webvowl_dir = json_parent.parent
        else:
            # Default to current directory
            webvowl_dir = Path.cwd() / "webvowl"
    
    # Ensure webvowl_dir is absolute
    webvowl_dir = webvowl_dir.resolve()
    
    print(f"\nWebVOWL directory: {webvowl_dir}")
    
    # Set up webvowl structure if it doesn't exist
    if not webvowl_dir.exists() or not (webvowl_dir / "index.html").exists():
        print("WebVOWL folder structure not found. Setting up...")
        
        reference = args.reference_webvowl
        if not reference:
            # Try to find a reference webvowl folder in the repository
            # Focus on ver_3_0, fallback to ver_2_0 if needed
            base_path = Path(__file__).parent.parent
            
            # Build reference paths, prefer ver_3_0
            ref_paths = []
            # Try ver_3_0 first
            for module in ["core", "experiment", "data-analysis-lifecycle", "dataset", "complete"]:
                ref_paths.append(base_path / "PRIMA" / module / "ver_3_0" / "webvowl")
            # Fallback to ver_2_0
            for module in ["core", "experiment", "data-analysis-lifecycle", "dataset", "complete"]:
                ref_paths.append(base_path / "PRIMA" / module / "ver_2_0" / "webvowl")
            
            for ref in ref_paths:
                if ref.exists():
                    reference = ref
                    break
        
        if not setup_webvowl_structure(webvowl_dir, reference):
            print("Warning: Could not set up webvowl structure. You may need to copy static files manually.")
    
    # Determine ontology name and ID
    if args.ontology_id:
        ontology_id = args.ontology_id
    else:
        _, ontology_id = infer_ontology_info(args.json_file, webvowl_dir)
    
    if args.ontology_name:
        ontology_name = args.ontology_name
    else:
        ontology_name, _ = infer_ontology_info(args.json_file, webvowl_dir)
    
    print(f"Ontology name: {ontology_name}")
    print(f"Ontology ID: {ontology_id}")
    
    # Copy JSON file to data directory
    data_dir = webvowl_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine target filename
    target_json = data_dir / f"{ontology_id}.json"

    # Avoid SameFileError if the provided JSON is already in the target location.
    try:
        if args.json_file.resolve() == target_json.resolve():
            print(f"✓ JSON file already in place: {target_json}")
        else:
            shutil.copy2(args.json_file, target_json)
            print(f"✓ Copied JSON file to: {target_json}")
    except FileNotFoundError:
        # resolve() can fail if a path component doesn't exist; fall back to copy
        shutil.copy2(args.json_file, target_json)
        print(f"✓ Copied JSON file to: {target_json}")
    
    # Update menu if requested
    if not args.no_menu_update:
        update_webvowl_index(webvowl_dir, ontology_name, ontology_id)
    
    print("\n" + "=" * 60)
    print("✓ WebVOWL folder updated successfully!")
    print(f"  JSON file: {target_json}")
    print(f"  To view: Open {webvowl_dir / 'index.html'}#{ontology_id}")
    print("=" * 60)
    
    # Also check if main index.html needs updating
    main_index = webvowl_dir.parent / "index.html"
    if main_index.exists():
        print(f"\nNote: Main index.html found at {main_index}")
        print(f"  Make sure it embeds: webvowl/index.html#{ontology_id}")


if __name__ == "__main__":
    main()
