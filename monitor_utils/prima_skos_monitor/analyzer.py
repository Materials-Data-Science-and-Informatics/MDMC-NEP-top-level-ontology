"""
Parse and analyze SKOS vocabulary.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import SKOS, RDF, DCTERMS, RDFS
from collections import defaultdict


@dataclass
class SKOSConcept:
    """Represents a SKOS concept with its properties."""

    uri: str
    pref_label: Dict[str, str] = field(default_factory=dict)  # lang -> label
    definition: Dict[str, str] = field(default_factory=dict)  # lang -> definition
    broader: Set[str] = field(default_factory=set)
    narrower: Set[str] = field(default_factory=set)
    related: Set[str] = field(default_factory=set)
    alt_labels: Dict[str, List[str]] = field(
        default_factory=lambda: defaultdict(list)
    )  # lang -> [labels]
    contributors: List[str] = field(default_factory=list)
    created: Optional[str] = None
    modified: Optional[str] = None
    history_notes: Dict[str, str] = field(default_factory=dict)  # lang -> note
    close_matches: Set[str] = field(default_factory=set)
    exact_matches: Set[str] = field(default_factory=set)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "uri": self.uri,
            "pref_label": self.pref_label,
            "definition": self.definition,
            "broader": sorted(list(self.broader)),
            "narrower": sorted(list(self.narrower)),
            "related": sorted(list(self.related)),
            "alt_labels": {
                lang: labels for lang, labels in self.alt_labels.items()
            },
            "contributors": self.contributors,
            "created": self.created,
            "modified": self.modified,
            "history_notes": self.history_notes,
            "close_matches": sorted(list(self.close_matches)),
            "exact_matches": sorted(list(self.exact_matches)),
        }

    def get_primary_label(self, lang: str = "en") -> str:
        """Get the preferred label in the specified language, or any language."""
        if lang in self.pref_label:
            return self.pref_label[lang]
        if self.pref_label:
            return next(iter(self.pref_label.values()))
        # Fallback to URI fragment
        return self.uri.split("/")[-1] if "/" in self.uri else self.uri

    def get_primary_definition(self, lang: str = "en") -> str:
        """Get the definition in the specified language, or any language."""
        if lang in self.definition:
            return self.definition[lang]
        if self.definition:
            return next(iter(self.definition.values()))
        return ""


def parse_skos(rdf_content: bytes, format: str = "xml") -> Dict[str, SKOSConcept]:
    """
    Parse SKOS vocabulary from RDF content.

    Args:
        rdf_content: RDF content as bytes
        format: RDF format ("xml" for RDF/XML, "turtle" for Turtle)

    Returns:
        Dictionary mapping concept URIs to SKOSConcept objects
    """
    graph = Graph()
    graph.parse(data=rdf_content, format=format)

    concepts: Dict[str, SKOSConcept] = {}

    # Find all SKOS concepts
    for concept_uri in graph.subjects(RDF.type, SKOS.Concept):
        concept_uri_str = str(concept_uri)
        concept = SKOSConcept(uri=concept_uri_str)

        # Preferred labels
        for label_obj in graph.objects(concept_uri, SKOS.prefLabel):
            if isinstance(label_obj, Literal):
                lang = str(label_obj.language) if label_obj.language else "en"
                concept.pref_label[lang] = str(label_obj)

        # Definitions
        for def_obj in graph.objects(concept_uri, SKOS.definition):
            if isinstance(def_obj, Literal):
                lang = str(def_obj.language) if def_obj.language else "en"
                concept.definition[lang] = str(def_obj)

        # Broader concepts
        for broader_obj in graph.objects(concept_uri, SKOS.broader):
            concept.broader.add(str(broader_obj))

        # Narrower concepts
        for narrower_obj in graph.objects(concept_uri, SKOS.narrower):
            concept.narrower.add(str(narrower_obj))

        # Related concepts
        for related_obj in graph.objects(concept_uri, SKOS.related):
            concept.related.add(str(related_obj))

        # Alternative labels
        for alt_label_obj in graph.objects(concept_uri, SKOS.altLabel):
            if isinstance(alt_label_obj, Literal):
                lang = str(alt_label_obj.language) if alt_label_obj.language else "en"
                concept.alt_labels[lang].append(str(alt_label_obj))

        # Contributors
        for contrib_obj in graph.objects(concept_uri, DCTERMS.contributor):
            if isinstance(contrib_obj, URIRef):
                concept.contributors.append(str(contrib_obj))
            elif isinstance(contrib_obj, Literal):
                concept.contributors.append(str(contrib_obj))

        # Created date
        for created_obj in graph.objects(concept_uri, DCTERMS.created):
            if isinstance(created_obj, Literal):
                concept.created = str(created_obj)

        # Modified date
        for modified_obj in graph.objects(concept_uri, DCTERMS.modified):
            if isinstance(modified_obj, Literal):
                concept.modified = str(modified_obj)

        # History notes
        for note_obj in graph.objects(concept_uri, SKOS.historyNote):
            if isinstance(note_obj, Literal):
                lang = str(note_obj.language) if note_obj.language else "en"
                concept.history_notes[lang] = str(note_obj)

        # Close matches
        for match_obj in graph.objects(concept_uri, SKOS.closeMatch):
            concept.close_matches.add(str(match_obj))

        # Exact matches
        for match_obj in graph.objects(concept_uri, SKOS.exactMatch):
            concept.exact_matches.add(str(match_obj))

        concepts[concept_uri_str] = concept

    return concepts


def load_skos_from_file(file_path: Path, format: str = "xml") -> Dict[str, SKOSConcept]:
    """
    Load and parse SKOS from a file.

    Args:
        file_path: Path to RDF file
        format: RDF format ("xml" for RDF/XML, "turtle" for Turtle)

    Returns:
        Dictionary mapping concept URIs to SKOSConcept objects
    """
    content = file_path.read_bytes()
    return parse_skos(content, format=format)

