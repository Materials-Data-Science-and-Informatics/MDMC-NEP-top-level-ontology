"""
Generate change reports in markdown format.
"""

from pathlib import Path
from typing import Optional, Dict
from prima_skos_monitor.comparator import ChangeReport, ConceptChange
from prima_skos_monitor.analyzer import SKOSConcept


def generate_report(
    report: ChangeReport,
    baseline_concepts: Optional[Dict[str, SKOSConcept]] = None,
    new_concepts: Optional[Dict[str, SKOSConcept]] = None,
    output_path: Optional[Path] = None,
) -> str:
    """
    Generate a markdown report of changes.

    Args:
        report: ChangeReport with detected changes
        baseline_concepts: Optional baseline concepts dict for context
        new_concepts: Optional new concepts dict for context
        output_path: Optional path to save the report

    Returns:
        Markdown report as string
    """
    lines = []
    lines.append("# PRIMA SKOS Vocabulary Change Report")
    lines.append("")
    lines.append(f"**Generated:** {_get_timestamp()}")
    lines.append("")

    # Summary
    summary = report.get_summary()
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| New Concepts | {summary['new_concepts']} |")
    lines.append(f"| Deleted Concepts | {summary['deleted_concepts']} |")
    lines.append(f"| Modified Concepts | {summary['modified_concepts']} |")
    lines.append(f"| **Total Changes** | **{summary['total_changes']}** |")
    lines.append("")
    lines.append(f"| Baseline Concepts | {summary['total_concepts_baseline']} |")
    lines.append(f"| New Version Concepts | {summary['total_concepts_new']} |")
    lines.append("")

    if not report.has_changes():
        lines.append("✅ **No changes detected.**")
        lines.append("")
        report_text = "\n".join(lines)
        if output_path:
            output_path.write_text(report_text)
        return report_text

    # New Concepts
    if report.new_concepts:
        lines.append("## New Concepts")
        lines.append("")
        for uri in report.new_concepts:
            concept_name = _get_concept_name(uri, new_concepts)
            lines.append(f"### {concept_name}")
            lines.append("")
            lines.append(f"- **URI:** `{uri}`")
            if new_concepts and uri in new_concepts:
                concept = new_concepts[uri]
                if concept.definition:
                    def_text = concept.get_primary_definition()
                    if def_text:
                        lines.append(f"- **Definition:** {def_text}")
            lines.append("")
            lines.append(f"- **SKOSMOS Link:** {_get_skosmos_link(uri)}")
            lines.append("")

    # Deleted Concepts
    if report.deleted_concepts:
        lines.append("## Deleted Concepts")
        lines.append("")
        for uri in report.deleted_concepts:
            concept_name = _get_concept_name(uri, baseline_concepts)
            lines.append(f"- **{concept_name}** (`{uri}`)")
            if baseline_concepts and uri in baseline_concepts:
                concept = baseline_concepts[uri]
                if concept.definition:
                    def_text = concept.get_primary_definition()
                    if def_text:
                        lines.append(f"  - *Previous definition:* {def_text}")
            lines.append("")

    # Modified Concepts
    if report.modified_concepts:
        lines.append("## Modified Concepts")
        lines.append("")
        for change in report.modified_concepts:
            concept_name = _get_concept_name(change.uri, new_concepts or baseline_concepts)
            lines.append(f"### {concept_name}")
            lines.append("")
            lines.append(f"- **URI:** `{change.uri}`")
            lines.append(f"- **SKOSMOS Link:** {_get_skosmos_link(change.uri)}")
            lines.append(f"- **Fields Changed:** {', '.join(change.fields_changed)}")
            lines.append("")

            # Show detailed changes for each field
            for field in change.fields_changed:
                lines.append(f"#### {field.replace('_', ' ').title()}")
                lines.append("")

                old_val = change.old_value.get(field)
                new_val = change.new_value.get(field)

                if field == "definition":
                    lines.append("**Old Definition:**")
                    if isinstance(old_val, dict):
                        for lang, text in old_val.items():
                            lines.append(f"- [{lang}] {text}")
                    else:
                        lines.append(f"- {old_val}")
                    lines.append("")
                    lines.append("**New Definition:**")
                    if isinstance(new_val, dict):
                        for lang, text in new_val.items():
                            lines.append(f"- [{lang}] {text}")
                    else:
                        lines.append(f"- {new_val}")
                elif field in ("broader", "narrower", "related", "close_matches", "exact_matches"):
                    lines.append("**Removed:**")
                    removed = set(old_val or []) - set(new_val or [])
                    if removed:
                        for item in sorted(removed):
                            lines.append(f"- `{item}`")
                    else:
                        lines.append("- *(none)*")
                    lines.append("")
                    lines.append("**Added:**")
                    added = set(new_val or []) - set(old_val or [])
                    if added:
                        for item in sorted(added):
                            lines.append(f"- `{item}`")
                    else:
                        lines.append("- *(none)*")
                elif field == "pref_label":
                    lines.append("**Old Labels:**")
                    if isinstance(old_val, dict):
                        for lang, label in old_val.items():
                            lines.append(f"- [{lang}] {label}")
                    else:
                        lines.append(f"- {old_val}")
                    lines.append("")
                    lines.append("**New Labels:**")
                    if isinstance(new_val, dict):
                        for lang, label in new_val.items():
                            lines.append(f"- [{lang}] {label}")
                    else:
                        lines.append(f"- {new_val}")
                else:
                    lines.append("**Old Value:**")
                    lines.append(f"```json")
                    lines.append(f"{_format_value(old_val)}")
                    lines.append(f"```")
                    lines.append("")
                    lines.append("**New Value:**")
                    lines.append(f"```json")
                    lines.append(f"{_format_value(new_val)}")
                    lines.append(f"```")

                lines.append("")

    # Recommendations
    lines.append("## Recommended Actions")
    lines.append("")
    if report.new_concepts:
        lines.append(
            "1. **Review new concepts** and determine if corresponding OWL classes need to be added or updated."
        )
    if report.deleted_concepts:
        lines.append(
            "2. **Review deleted concepts** and determine if corresponding OWL classes should be deprecated."
        )
    if report.modified_concepts:
        lines.append(
            "3. **Review modified concepts** and update OWL class definitions, relationships, or annotations as needed."
        )
    lines.append(
        "4. **Update OWL mappings** (`rdfs:isDefinedBy` and `skos:exactMatch`) if concept URIs have changed."
    )
    lines.append("")

    report_text = "\n".join(lines)
    if output_path:
        output_path.write_text(report_text)

    return report_text


def _get_timestamp() -> str:
    """Get current timestamp as string."""
    from datetime import datetime

    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def _get_concept_name(uri: str, concepts: Optional[Dict[str, SKOSConcept]]) -> str:
    """Get concept name from URI or concepts dict."""
    if concepts and uri in concepts:
        return concepts[uri].get_primary_label()
    # Extract from URI
    if "/" in uri:
        return uri.split("/")[-1]
    return uri


def _get_skosmos_link(uri: str) -> str:
    """Generate SKOSMOS link for a concept URI."""
    # Extract concept ID from URI
    # URI format: https://purls.helmholtz-metadaten.de/skosmos/prima/{concept}
    if "skosmos/prima/" in uri:
        concept_id = uri.split("skosmos/prima/")[-1]
        return f"https://matwerk.datamanager.kit.edu/skosmos/prima/en/page/{concept_id}"
    return uri


def _format_value(value) -> str:
    """Format a value for JSON display."""
    import json

    return json.dumps(value, indent=2, ensure_ascii=False)

