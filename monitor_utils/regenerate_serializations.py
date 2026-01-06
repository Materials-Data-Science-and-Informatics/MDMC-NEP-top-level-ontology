#!/usr/bin/env python3
"""
Unified script to regenerate TTL and JSON-LD serializations from OWL files for all PRIMA modules.
Run this script after making changes to any PRIMA OWL file.

Usage:
    python regenerate_serializations.py [module_name]
    
    If module_name is provided, only that module will be regenerated.
    If no module_name is provided, all modules will be regenerated.
    
    Available modules: core, dal, dataset, experiment, computational, complete
"""

import os
import sys
from pathlib import Path
from rdflib import Graph


# Module configuration
MODULES = {
    "core": {
        "path": "PRIMA/core/ver_2_0",
        "owl_file": "prima-core.owl",
        "ttl_file": "prima-core.ttl",
        "jsonld_file": "prima-core.jsonld"
    },
    "dal": {
        "path": "PRIMA/data-analysis-lifecycle/ver_2_0",
        "owl_file": "prima-data-analysis-lifecycle.owl",
        "ttl_file": "prima-data-analysis-lifecycle.ttl",
        "jsonld_file": "prima-data-analysis-lifecycle.jsonld"
    },
    "dataset": {
        "path": "PRIMA/dataset/ver_2_0",
        "owl_file": "prima-dataset.owl",
        "ttl_file": "prima-dataset.ttl",
        "jsonld_file": "prima-dataset.jsonld"
    },
    "experiment": {
        "path": "PRIMA/experiment/ver_2_0",
        "owl_file": "prima-experiment.owl",
        "ttl_file": "prima-experiment.ttl",
        "jsonld_file": "prima-experiment.jsonld"
    },
    "computational": {
        "path": "PRIMA/computational/ver_2_0",
        "owl_file": "prima-computational.owl",
        "ttl_file": "prima-computational.ttl",
        "jsonld_file": "prima-computational.jsonld"
    },
    "complete": {
        "path": "PRIMA/complete/ver_2_0",
        "owl_file": "prima-complete.owl",
        "ttl_file": "prima-complete.ttl",
        "jsonld_file": "prima-complete.jsonld"
    }
}


def regenerate_module(module_name: str, base_path: Path) -> bool:
    """
    Regenerate TTL and JSON-LD serializations for a specific module.
    
    Args:
        module_name: Name of the module to regenerate
        base_path: Base path of the repository
        
    Returns:
        True if successful, False otherwise
    """
    if module_name not in MODULES:
        print(f"Error: Unknown module '{module_name}'")
        print(f"Available modules: {', '.join(MODULES.keys())}")
        return False
    
    config = MODULES[module_name]
    module_path = base_path / config["path"]
    owl_file = module_path / config["owl_file"]
    
    if not owl_file.exists():
        print(f"Error: OWL file not found: {owl_file}")
        return False
    
    print(f"\n[{module_name.upper()}] Processing {config['owl_file']}...")
    print(f"  Path: {module_path}")
    
    try:
        # Parse OWL file
        g = Graph()
        g.parse(str(owl_file))
        print(f"  ✓ Successfully parsed OWL file")
        
        # Generate TTL
        ttl_path = module_path / config["ttl_file"]
        g.serialize(destination=str(ttl_path), format='turtle')
        print(f"  ✓ Generated TTL: {config['ttl_file']}")
        
        # Generate JSON-LD
        jsonld_path = module_path / config["jsonld_file"]
        g.serialize(destination=str(jsonld_path), format='json-ld')
        print(f"  ✓ Generated JSON-LD: {config['jsonld_file']}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error processing {module_name}: {e}")
        return False


def regenerate_all(base_path: Path) -> bool:
    """
    Regenerate serializations for all modules.
    
    Args:
        base_path: Base path of the repository
        
    Returns:
        True if all successful, False otherwise
    """
    print("=" * 60)
    print("Regenerating serializations for all PRIMA modules")
    print("=" * 60)
    
    success_count = 0
    failed_modules = []
    
    for module_name in MODULES.keys():
        if regenerate_module(module_name, base_path):
            success_count += 1
        else:
            failed_modules.append(module_name)
    
    print("\n" + "=" * 60)
    print(f"Summary: {success_count}/{len(MODULES)} modules regenerated successfully")
    
    if failed_modules:
        print(f"Failed modules: {', '.join(failed_modules)}")
        return False
    
    print("✓ All serializations regenerated successfully!")
    return True


def main():
    """Main entry point."""
    # Get base path (parent of monitor_utils)
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent
    
    # Change to base directory
    os.chdir(base_path)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        module_name = sys.argv[1].lower()
        if module_name == "all":
            success = regenerate_all(base_path)
        else:
            success = regenerate_module(module_name, base_path)
            if success:
                print(f"\n✓ Module '{module_name}' regenerated successfully!")
    else:
        # No arguments - regenerate all
        success = regenerate_all(base_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

