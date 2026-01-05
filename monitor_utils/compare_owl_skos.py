"""
Compare PRIMA OWL ontology with SKOS vocabulary.
"""

import sys
from pathlib import Path

# Add monitor_utils to path
_script_file = Path(__file__).resolve()
_monitor_utils_dir = _script_file.parent
if str(_monitor_utils_dir) not in sys.path:
    sys.path.insert(0, str(_monitor_utils_dir))

from rdflib import Graph, URIRef, RDF, RDFS, SKOS, OWL, BNode
from prima_skos_monitor.analyzer import load_skos_from_file, parse_skos
from collections import defaultdict


def load_owl_modules(base_path: Path):
    """Load all PRIMA OWL modules and extract classes with SKOS mappings."""
    modules = {
        "core": base_path / "PRIMA/core/ver_2_0/prima-core.owl",
        "experiment": base_path / "PRIMA/experiment/ver_2_0/prima-experiment.owl",
        "dataset": base_path / "PRIMA/dataset/ver_2_0/prima-dataset.owl",
        "data-analysis-lifecycle": base_path / "PRIMA/data-analysis-lifecycle/ver_2_0/prima-data-analysis-lifecycle.owl",
        "computational": base_path / "PRIMA/computational/ver_2_0/prima-computational.owl",
    }
    
    # First, parse all modules into a single graph to get all mappings
    combined_graph = Graph()
    for module_name, owl_path in modules.items():
        if owl_path.exists():
            combined_graph.parse(str(owl_path), format="xml")
    
    owl_classes = {}
    
    for module_name, owl_path in modules.items():
        if not owl_path.exists():
            print(f"⚠️  Module {module_name} not found: {owl_path}")
            continue
            
        print(f"Loading {module_name} module...")
        graph = Graph()
        graph.parse(str(owl_path), format="xml")
        
        # Find all OWL classes (both owl:Class and rdfs:Class)
        owl_classes_found = set()
        for class_uri in graph.subjects(RDF.type, OWL.Class):
            owl_classes_found.add(class_uri)
        for class_uri in graph.subjects(RDF.type, RDFS.Class):
            owl_classes_found.add(class_uri)
        
        for class_uri in owl_classes_found:
            # Skip blank nodes (they have auto-generated identifiers)
            if isinstance(class_uri, BNode):
                continue
            
            class_uri_str = str(class_uri)
            
            # Skip identifiers that look like auto-generated blank node names
            # (they start with 'N' followed by hex characters and no URI scheme)
            if class_uri_str.startswith('N') and len(class_uri_str) > 10 and '://' not in class_uri_str:
                continue
            
            # Skip if we've already processed this class
            if class_uri_str in owl_classes:
                continue
            
            # Ensure class_uri is a URIRef for proper querying
            if not isinstance(class_uri, URIRef):
                class_uri = URIRef(class_uri)
            
            # Get SKOS mappings from combined graph (to catch mappings from any module)
            skos_mappings = []
            for mapping_uri in combined_graph.objects(class_uri, RDFS.isDefinedBy):
                mapping_str = str(mapping_uri)
                # Only include SKOS mappings (not other isDefinedBy)
                if "skosmos/prima" in mapping_str:
                    skos_mappings.append(("isDefinedBy", mapping_str))
            for mapping_uri in combined_graph.objects(class_uri, SKOS.exactMatch):
                mapping_str = str(mapping_uri)
                if "skosmos/prima" in mapping_str:
                    skos_mappings.append(("exactMatch", mapping_str))
            
            # Get label
            label = None
            for label_obj in combined_graph.objects(class_uri, RDFS.label):
                if isinstance(label_obj, str) or (hasattr(label_obj, 'value')):
                    label = str(label_obj)
                    break
            
            owl_classes[class_uri_str] = {
                "module": module_name,
                "label": label or class_uri_str.split("#")[-1],
                "skos_mappings": skos_mappings,
                "uri": class_uri_str,
            }
    
    return owl_classes


def extract_skos_uris(skos_concepts):
    """Extract all SKOS concept URIs."""
    return set(skos_concepts.keys())


def compare_owl_skos(owl_classes, skos_concepts):
    """Compare OWL classes with SKOS concepts."""
    skos_uris = extract_skos_uris(skos_concepts)
    
    # Build mapping from SKOS URI to OWL class
    skos_to_owl = {}
    owl_to_skos = {}
    
    for owl_uri, owl_info in owl_classes.items():
        for mapping_type, mapping_uri in owl_info["skos_mappings"]:
            if mapping_uri in skos_uris:
                skos_to_owl[mapping_uri] = owl_uri
                owl_to_skos[owl_uri] = mapping_uri
    
    # Find OWL classes without SKOS mappings
    owl_without_skos = []
    for owl_uri, owl_info in owl_classes.items():
        if owl_uri not in owl_to_skos:
            owl_without_skos.append(owl_info)
    
    # Find SKOS concepts without OWL classes
    skos_without_owl = []
    for skos_uri in skos_uris:
        if skos_uri not in skos_to_owl:
            skos_without_owl.append(skos_uri)
    
    # Find OWL classes with SKOS mappings
    owl_with_skos = []
    for owl_uri, owl_info in owl_classes.items():
        if owl_uri in owl_to_skos:
            owl_with_skos.append({
                **owl_info,
                "skos_uri": owl_to_skos[owl_uri],
            })
    
    return {
        "owl_with_skos": owl_with_skos,
        "owl_without_skos": owl_without_skos,
        "skos_without_owl": skos_without_owl,
        "total_owl_classes": len(owl_classes),
        "total_skos_concepts": len(skos_uris),
        "mapped_count": len(owl_with_skos),
    }


def generate_report(comparison_result, output_path: Path):
    """Generate a comparison report."""
    lines = []
    lines.append("# PRIMA OWL-SKOS Alignment Report")
    lines.append("")
    lines.append("This report compares PRIMA OWL ontology classes with SKOS vocabulary concepts.")
    lines.append("")
    
    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Total OWL Classes | {comparison_result['total_owl_classes']} |")
    lines.append(f"| Total SKOS Concepts | {comparison_result['total_skos_concepts']} |")
    lines.append(f"| OWL Classes with SKOS Mappings | {comparison_result['mapped_count']} |")
    lines.append(f"| OWL Classes without SKOS Mappings | {len(comparison_result['owl_without_skos'])} |")
    lines.append(f"| SKOS Concepts without OWL Classes | {len(comparison_result['skos_without_owl'])} |")
    lines.append("")
    
    # OWL classes with SKOS mappings
    if comparison_result["owl_with_skos"]:
        lines.append("## OWL Classes with SKOS Mappings")
        lines.append("")
        lines.append(f"✅ **{len(comparison_result['owl_with_skos'])} OWL classes are mapped to SKOS concepts.**")
        lines.append("")
        lines.append("| OWL Class | Module | SKOS Concept |")
        lines.append("|-----------|--------|--------------|")
        for item in sorted(comparison_result["owl_with_skos"], key=lambda x: x["module"]):
            skos_name = item["skos_uri"].split("/")[-1]
            lines.append(f"| `{item['label']}` | {item['module']} | [{skos_name}]({item['skos_uri']}) |")
        lines.append("")
    
    # OWL classes without SKOS mappings
    if comparison_result["owl_without_skos"]:
        lines.append("## OWL Classes without SKOS Mappings")
        lines.append("")
        lines.append(f"⚠️  **{len(comparison_result['owl_without_skos'])} OWL classes do not have SKOS mappings.**")
        lines.append("")
        for item in sorted(comparison_result["owl_without_skos"], key=lambda x: x["module"]):
            lines.append(f"- **{item['label']}** (`{item['uri']}`) - Module: {item['module']}")
        lines.append("")
    
    # SKOS concepts without OWL classes
    if comparison_result["skos_without_owl"]:
        lines.append("## SKOS Concepts without OWL Classes")
        lines.append("")
        lines.append(f"⚠️  **{len(comparison_result['skos_without_owl'])} SKOS concepts do not have corresponding OWL classes.**")
        lines.append("")
        for skos_uri in sorted(comparison_result["skos_without_owl"]):
            skos_name = skos_uri.split("/")[-1]
            lines.append(f"- [{skos_name}]({skos_uri})")
        lines.append("")
    
    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    if comparison_result["owl_without_skos"]:
        lines.append("1. **Add SKOS mappings** to OWL classes that are missing them using `rdfs:isDefinedBy` and `skos:exactMatch`.")
    if comparison_result["skos_without_owl"]:
        lines.append("2. **Review SKOS concepts** without OWL classes to determine if OWL classes should be added or if the SKOS concepts should be removed.")
    if not comparison_result["owl_without_skos"] and not comparison_result["skos_without_owl"]:
        lines.append("✅ **Perfect alignment!** All OWL classes have SKOS mappings and all SKOS concepts have corresponding OWL classes.")
    lines.append("")
    
    report_text = "\n".join(lines)
    output_path.write_text(report_text)
    return report_text


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Compare PRIMA OWL ontology with SKOS vocabulary")
    parser.add_argument(
        "--skos-file",
        default="prima.rdf",
        help="Path to SKOS RDF file (default: prima.rdf)",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root directory (default: current directory)",
    )
    parser.add_argument(
        "--output",
        default="owl_skos_alignment_report.md",
        help="Output report file (default: owl_skos_alignment_report.md)",
    )
    
    args = parser.parse_args()
    
    repo_root = Path(args.repo_root).resolve()
    skos_file = Path(args.skos_file)
    output_path = Path(args.output)
    
    print("=" * 80)
    print("PRIMA OWL-SKOS Alignment Comparison")
    print("=" * 80)
    print()
    
    # Load SKOS
    print("Loading SKOS vocabulary...")
    if not skos_file.exists():
        print(f"✗ SKOS file not found: {skos_file}")
        print("  Downloading from SKOSMOS...")
        from prima_skos_monitor.downloader import download_skos
        content, _ = download_skos()
        skos_concepts = parse_skos(content, format="xml")
    else:
        skos_concepts = load_skos_from_file(skos_file, format="xml")
    print(f"✓ Loaded {len(skos_concepts)} SKOS concepts")
    print()
    
    # Load OWL modules
    print("Loading PRIMA OWL modules...")
    owl_classes = load_owl_modules(repo_root)
    print(f"✓ Loaded {len(owl_classes)} OWL classes")
    print()
    
    # Compare
    print("Comparing OWL classes with SKOS concepts...")
    comparison_result = compare_owl_skos(owl_classes, skos_concepts)
    print()
    
    # Generate report
    print(f"Generating report: {output_path}")
    generate_report(comparison_result, output_path)
    print(f"✓ Report saved to {output_path}")
    print()
    
    # Print summary
    print("Summary:")
    print(f"  - OWL classes with SKOS mappings: {comparison_result['mapped_count']}")
    print(f"  - OWL classes without SKOS mappings: {len(comparison_result['owl_without_skos'])}")
    print(f"  - SKOS concepts without OWL classes: {len(comparison_result['skos_without_owl'])}")


if __name__ == "__main__":
    main()

