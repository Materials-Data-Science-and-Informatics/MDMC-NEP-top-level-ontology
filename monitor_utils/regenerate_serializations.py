#!/usr/bin/env python3
"""
Unified script to regenerate TTL, JSON-LD serializations and pyLODE HTML documentation
from OWL files for all PRIMA modules.
Run this script after making changes to any PRIMA OWL file.

Usage:
    python regenerate_serializations.py [module_name]
    
    If module_name is provided, only that module will be regenerated.
    If no module_name is provided, all modules will be regenerated.

    Add --vowl to also regenerate the WebVOWL diagram JSON via OWL2VOWL
    (slower; requires Java and network access to resolve owl:imports):
        python regenerate_serializations.py core_v3 --vowl

    Available modules: core, core_v3, dal, dal_v3, dataset, dataset_v3, experiment, experiment_v3, computational, computational_v3, complete, complete_v3
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from rdflib import Graph
from pylode import OntPub


# OWL2VOWL (WebVOWL diagram JSON) -------------------------------------------
# OWL2VOWL publishes no runnable fat jar, so we resolve it (+ its dependencies)
# with the pinned Coursier launcher (monitor_utils/cs) and run it on the local
# JVM. The old OWL API/Guice it uses needs java.base opened on Java 17+.
# Note: OWL2VOWL resolves owl:imports (network needed) and produces an
# auto-layout diagram (manually-arranged node positions are not reproduced).
OWL2VOWL_COORD = "org.visualdataweb.vowl.owl2vowl:OWL2VOWL:0.3.1"
OWL2VOWL_MAIN = "de.uni_stuttgart.vis.vowl.owl2vowl.ConsoleMain"
JAVA_ADD_OPENS = [
    "--add-opens=java.base/java.lang=ALL-UNNAMED",
    "--add-opens=java.base/java.util=ALL-UNNAMED",
]
CS_LAUNCHER = Path(__file__).resolve().parent / "cs"


# Module configuration
MODULES = {
    "core": {
        "path": "PRIMA/core/ver_2_0",
        "owl_file": "prima-core.owl",
        "ttl_file": "prima-core.ttl",
        "jsonld_file": "prima-core.jsonld"
    },
    "core_v3": {
        "path": "PRIMA/core/ver_3_0",
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
    "dal_v3": {
        "path": "PRIMA/data-analysis-lifecycle/ver_3_0",
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
    "dataset_v3": {
        "path": "PRIMA/dataset/ver_3_0",
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
    "experiment_v3": {
        "path": "PRIMA/experiment/ver_3_0",
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
    "computational_v3": {
        "path": "PRIMA/computational/ver_3_0",
        "owl_file": "prima-computational.owl",
        "ttl_file": "prima-computational.ttl",
        "jsonld_file": "prima-computational.jsonld"
    },
    "complete": {
        "path": "PRIMA/complete/ver_2_0",
        "owl_file": "prima-complete.owl",
        "ttl_file": "prima-complete.ttl",
        "jsonld_file": "prima-complete.jsonld"
    },
    "complete_v3": {
        "path": "PRIMA/complete/ver_3_0",
        "owl_file": "prima-complete.owl",
        "ttl_file": "prima-complete.ttl",
        "jsonld_file": "prima-complete.jsonld"
    }
}


def inject_webvowl_overview(html: str, ontology_id: str) -> str:
    """Re-inject the WebVOWL overview into pyLODE-generated HTML.

    pyLODE (OntPub) does not emit the WebVOWL diagram, so after each regeneration
    we re-insert the hand-authored Overview section (an <iframe> embedding the local
    WebVOWL viewer) and its CSS, keeping the documentation consistent with what was
    committed. Insertion is idempotent and a no-op if the markers are already present.

    Args:
        html: The HTML produced by pyLODE.
        ontology_id: WebVOWL ontology id / hash fragment, e.g. "prima-core".

    Returns:
        The HTML with the WebVOWL overview re-injected.
    """
    # 1) CSS rule for the overview image, appended to the <style> block.
    overview_css = (
        "        section#overview img {\n"
        "            max-width: 1000px;\n"
        "        }\n"
    )
    if "section#overview img" not in html and "</style>" in html:
        html = html.replace("</style>", overview_css + "    </style>", 1)

    # 2) Overview section with the WebVOWL iframe, inserted before the Classes
    #    section (fallback: the Object Properties section for modules without classes).
    overview_section = (
        '      <section class="section" id="overview">\n'
        '        <h2>Overview</h2>\n'
        '        <div class="figure">\n'
        f'            <iframe width="100%" height ="800px" src="webvowl/index.html#{ontology_id}"></iframe>\n'
        '            <div class="caption"><strong>Figure 1:</strong> Ontology overview</div>\n'
        '        </div>\n'
        '    </section>\n'
    )
    if 'id="overview"' not in html:
        for anchor in (
            '<div class="section" id="classes">',
            '<div class="section" id="objectproperties">',
        ):
            if anchor in html:
                html = html.replace(anchor, overview_section + anchor, 1)
                break
    return html


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

        # Generate pyLODE HTML documentation (OntPub profile), then re-inject the
        # WebVOWL overview that pyLODE does not produce. Generated from the TTL so the
        # entity ordering matches the committed docs (rdflib's Turtle subject order).
        html_path = module_path / "index.html"
        module_folder = Path(config["path"]).parts[1]  # e.g. 'core', 'data-analysis-lifecycle'
        ontology_id = f"prima-{module_folder}"
        html = OntPub(ontology=str(ttl_path)).make_html()
        html = inject_webvowl_overview(html, ontology_id)
        html_path.write_text(html, encoding="utf-8")
        print(f"  ✓ Generated docs: index.html (with WebVOWL overview)")

        return True
        
    except Exception as e:
        print(f"  ✗ Error processing {module_name}: {e}")
        return False


def regenerate_vowl(module_name: str, base_path: Path) -> bool:
    """Regenerate the WebVOWL diagram JSON for a module using OWL2VOWL.

    Runs OWL2VOWL (resolved via the pinned Coursier launcher) on the module's OWL
    file and writes the VOWL JSON to webvowl/data/<id>.json, keeping the module-root
    <name>.owl.json copy in sync. Requires Java + network (for owl:imports).
    Produces an auto-layout diagram; hand-arranged node positions are not preserved.

    Args:
        module_name: Name of the module to regenerate.
        base_path: Base path of the repository.

    Returns:
        True if successful, False otherwise.
    """
    if module_name not in MODULES:
        print(f"Error: Unknown module '{module_name}'")
        return False

    config = MODULES[module_name]
    module_path = base_path / config["path"]
    owl_file = module_path / config["owl_file"]

    if not owl_file.exists():
        print(f"Error: OWL file not found: {owl_file}")
        return False
    if shutil.which("java") is None:
        print("  ✗ 'java' not found on PATH; skipping WebVOWL JSON")
        return False
    if not CS_LAUNCHER.exists():
        print(f"  ✗ Coursier launcher missing: {CS_LAUNCHER}; skipping WebVOWL JSON")
        return False

    ontology_id = f"prima-{Path(config['path']).parts[1]}"
    print(f"\n[{module_name.upper()}] OWL2VOWL -> WebVOWL JSON ({ontology_id})...")

    try:
        # Resolve OWL2VOWL + dependencies to a classpath (cached by Coursier).
        classpath = subprocess.check_output(
            [str(CS_LAUNCHER), "fetch", "-p", OWL2VOWL_COORD], text=True
        ).strip()

        data_dir = module_path / "webvowl" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        out_json = data_dir / f"{ontology_id}.json"

        subprocess.run(
            ["java", *JAVA_ADD_OPENS, "-cp", classpath, OWL2VOWL_MAIN,
             "-file", str(owl_file), "-output", str(out_json)],
            check=True,
        )

        # Keep the module-root copy (e.g. prima-core.owl.json) identical.
        owl_json = module_path / f"{Path(config['owl_file']).stem}.owl.json"
        shutil.copy2(out_json, owl_json)

        print(f"  ✓ Generated WebVOWL JSON: webvowl/data/{ontology_id}.json (+ {owl_json.name})")
        return True
    except subprocess.CalledProcessError as exc:
        print(f"  ✗ OWL2VOWL failed for {module_name}: {exc}")
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
    
    # Parse command line arguments. The optional --vowl flag additionally
    # regenerates the WebVOWL diagram JSON via OWL2VOWL (slower; Java + network).
    args = sys.argv[1:]
    with_vowl = "--vowl" in args
    positionals = [a for a in args if not a.startswith("-")]
    target = positionals[0].lower() if positionals else "all"

    if target == "all":
        success = regenerate_all(base_path)
        if with_vowl:
            for module_name in MODULES:
                regenerate_vowl(module_name, base_path)
    else:
        success = regenerate_module(target, base_path)
        if success:
            print(f"\n✓ Module '{target}' regenerated successfully!")
            if with_vowl:
                regenerate_vowl(target, base_path)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

