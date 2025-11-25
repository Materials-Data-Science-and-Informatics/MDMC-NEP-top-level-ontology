"""
Compare SKOS vocabulary versions and detect changes.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set
from prima_skos_monitor.analyzer import SKOSConcept


@dataclass
class ConceptChange:
    """Represents a change to a single concept."""

    uri: str
    change_type: str  # "new", "deleted", "modified"
    fields_changed: List[str] = field(default_factory=list)
    old_value: Dict = field(default_factory=dict)
    new_value: Dict = field(default_factory=dict)


@dataclass
class ChangeReport:
    """Report of changes between two SKOS versions."""

    new_concepts: List[str] = field(default_factory=list)
    deleted_concepts: List[str] = field(default_factory=list)
    modified_concepts: List[ConceptChange] = field(default_factory=list)
    total_concepts_baseline: int = 0
    total_concepts_new: int = 0

    def has_changes(self) -> bool:
        """Check if there are any changes."""
        return (
            len(self.new_concepts) > 0
            or len(self.deleted_concepts) > 0
            or len(self.modified_concepts) > 0
        )

    def get_summary(self) -> dict:
        """Get summary statistics."""
        return {
            "new_concepts": len(self.new_concepts),
            "deleted_concepts": len(self.deleted_concepts),
            "modified_concepts": len(self.modified_concepts),
            "total_changes": len(self.new_concepts)
            + len(self.deleted_concepts)
            + len(self.modified_concepts),
            "total_concepts_baseline": self.total_concepts_baseline,
            "total_concepts_new": self.total_concepts_new,
        }


def compare_versions(
    baseline: Dict[str, SKOSConcept],
    new_version: Dict[str, SKOSConcept],
) -> ChangeReport:
    """
    Compare two SKOS vocabulary versions and detect changes.

    Args:
        baseline: Dictionary of concepts from baseline version
        new_version: Dictionary of concepts from new version

    Returns:
        ChangeReport with detected changes
    """
    report = ChangeReport()
    report.total_concepts_baseline = len(baseline)
    report.total_concepts_new = len(new_version)

    baseline_uris = set(baseline.keys())
    new_uris = set(new_version.keys())

    # Find new concepts
    report.new_concepts = sorted(list(new_uris - baseline_uris))

    # Find deleted concepts
    report.deleted_concepts = sorted(list(baseline_uris - new_uris))

    # Find modified concepts
    common_uris = baseline_uris & new_uris
    for uri in common_uris:
        baseline_concept = baseline[uri]
        new_concept = new_version[uri]

        change = _compare_concept(baseline_concept, new_concept)
        if change:
            report.modified_concepts.append(change)

    return report


def _compare_concept(
    baseline: SKOSConcept, new_concept: SKOSConcept
) -> ConceptChange | None:
    """
    Compare two concepts and return a ConceptChange if differences are found.

    Args:
        baseline: Baseline concept
        new_concept: New concept

    Returns:
        ConceptChange if changes detected, None otherwise
    """
    change = ConceptChange(uri=baseline.uri, change_type="modified")
    has_changes = False

    # Compare preferred labels
    if baseline.pref_label != new_concept.pref_label:
        change.fields_changed.append("pref_label")
        change.old_value["pref_label"] = baseline.pref_label
        change.new_value["pref_label"] = new_concept.pref_label
        has_changes = True

    # Compare definitions
    if baseline.definition != new_concept.definition:
        change.fields_changed.append("definition")
        change.old_value["definition"] = baseline.definition
        change.new_value["definition"] = new_concept.definition
        has_changes = True

    # Compare broader relationships
    if baseline.broader != new_concept.broader:
        change.fields_changed.append("broader")
        change.old_value["broader"] = sorted(list(baseline.broader))
        change.new_value["broader"] = sorted(list(new_concept.broader))
        has_changes = True

    # Compare narrower relationships
    if baseline.narrower != new_concept.narrower:
        change.fields_changed.append("narrower")
        change.old_value["narrower"] = sorted(list(baseline.narrower))
        change.new_value["narrower"] = sorted(list(new_concept.narrower))
        has_changes = True

    # Compare related relationships
    if baseline.related != new_concept.related:
        change.fields_changed.append("related")
        change.old_value["related"] = sorted(list(baseline.related))
        change.new_value["related"] = sorted(list(new_concept.related))
        has_changes = True

    # Compare alternative labels
    baseline_alt = {
        lang: sorted(labels) for lang, labels in baseline.alt_labels.items()
    }
    new_alt = {
        lang: sorted(labels) for lang, labels in new_concept.alt_labels.items()
    }
    if baseline_alt != new_alt:
        change.fields_changed.append("alt_labels")
        change.old_value["alt_labels"] = baseline_alt
        change.new_value["alt_labels"] = new_alt
        has_changes = True

    # Compare contributors
    if sorted(baseline.contributors) != sorted(new_concept.contributors):
        change.fields_changed.append("contributors")
        change.old_value["contributors"] = sorted(baseline.contributors)
        change.new_value["contributors"] = sorted(new_concept.contributors)
        has_changes = True

    # Compare created date
    if baseline.created != new_concept.created:
        change.fields_changed.append("created")
        change.old_value["created"] = baseline.created
        change.new_value["created"] = new_concept.created
        has_changes = True

    # Compare modified date
    if baseline.modified != new_concept.modified:
        change.fields_changed.append("modified")
        change.old_value["modified"] = baseline.modified
        change.new_value["modified"] = new_concept.modified
        has_changes = True

    # Compare history notes
    if baseline.history_notes != new_concept.history_notes:
        change.fields_changed.append("history_notes")
        change.old_value["history_notes"] = baseline.history_notes
        change.new_value["history_notes"] = new_concept.history_notes
        has_changes = True

    # Compare close matches
    if baseline.close_matches != new_concept.close_matches:
        change.fields_changed.append("close_matches")
        change.old_value["close_matches"] = sorted(list(baseline.close_matches))
        change.new_value["close_matches"] = sorted(list(new_concept.close_matches))
        has_changes = True

    # Compare exact matches
    if baseline.exact_matches != new_concept.exact_matches:
        change.fields_changed.append("exact_matches")
        change.old_value["exact_matches"] = sorted(list(baseline.exact_matches))
        change.new_value["exact_matches"] = sorted(list(new_concept.exact_matches))
        has_changes = True

    return change if has_changes else None

