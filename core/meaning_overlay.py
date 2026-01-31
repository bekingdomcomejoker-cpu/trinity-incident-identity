"""
Trinity Incident-Identity Engine
Core Module: Meaning Overlay

This module provides descriptive semantic layers.
Meaning annotates, never modifies.
Meaning interprets, never prescribes.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class MeaningSource(Enum):
    """Sources of meaning (descriptive only)."""
    ETYMOLOGY = "etymology"
    CULTURAL_USAGE = "cultural_usage"
    GEOGRAPHIC_CONTEXT = "geographic_context"
    NARRATIVE_ROLE = "narrative_role"
    TECHNICAL_DEFINITION = "technical_definition"
    HISTORICAL_CONTEXT = "historical_context"


@dataclass
class MeaningEntry:
    """
    Single meaning annotation.
    
    INVARIANTS:
    - Descriptive only (never prescriptive)
    - Non-causal (never implies action)
    - Read-only after creation
    - Annotates, never modifies
    """
    
    term: str
    source: MeaningSource
    definition: str
    usage_examples: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    related_terms: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate meaning entry."""
        if not self.term:
            raise ValueError("term cannot be empty")
        if not self.definition:
            raise ValueError("definition cannot be empty")
        
        # Validate no prescriptive language
        forbidden_phrases = [
            "should", "must", "will", "predict", "optimize",
            "must do", "will do", "should be", "ought to"
        ]
        
        for phrase in forbidden_phrases:
            if phrase in self.definition.lower():
                raise ValueError(
                    f"Definition contains prescriptive language: {phrase}"
                )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize meaning entry."""
        return {
            "term": self.term,
            "source": self.source.value,
            "definition": self.definition,
            "usage_examples": self.usage_examples,
            "context": self.context,
            "constraints": self.constraints,
            "related_terms": self.related_terms,
        }


@dataclass
class MeaningLayer:
    """
    Collection of meaning entries for a specific source.
    
    INVARIANTS:
    - Read-only after creation
    - Annotates incidents and entities
    - Never modifies source data
    """
    
    source: MeaningSource
    entries: Dict[str, MeaningEntry] = field(default_factory=dict)
    
    def add_entry(self, entry: MeaningEntry) -> None:
        """Add meaning entry to layer."""
        if entry.source != self.source:
            raise ValueError(
                f"Entry source {entry.source} does not match layer source {self.source}"
            )
        self.entries[entry.term] = entry
    
    def get_entry(self, term: str) -> Optional[MeaningEntry]:
        """Retrieve meaning entry."""
        return self.entries.get(term)
    
    def get_all_entries(self) -> List[MeaningEntry]:
        """Get all entries in layer."""
        return list(self.entries.values())
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize meaning layer."""
        return {
            "source": self.source.value,
            "entries": {k: v.to_dict() for k, v in self.entries.items()},
        }


class MeaningOverlay:
    """
    Multi-source semantic annotation system.
    
    INVARIANTS:
    - Descriptive only
    - Non-causal
    - Non-executing
    - Answers "How can this be understood?" never "What will happen?"
    """
    
    def __init__(self):
        """Initialize meaning overlay."""
        self.layers: Dict[MeaningSource, MeaningLayer] = {
            source: MeaningLayer(source) for source in MeaningSource
        }
    
    def add_meaning(self, entry: MeaningEntry) -> None:
        """Add meaning entry to appropriate layer."""
        self.layers[entry.source].add_entry(entry)
    
    def get_meanings_for_term(self, term: str) -> Dict[str, MeaningEntry]:
        """Get all meanings for a term across all sources."""
        meanings = {}
        for source, layer in self.layers.items():
            entry = layer.get_entry(term)
            if entry:
                meanings[source.value] = entry
        return meanings
    
    def get_layer(self, source: MeaningSource) -> MeaningLayer:
        """Get specific meaning layer."""
        return self.layers[source]
    
    def annotate_incident(self, incident_id: str, term: str, meaning: MeaningEntry) -> Dict[str, Any]:
        """
        Annotate incident with meaning.
        
        CONSTRAINT: Returns annotation, does not modify incident.
        """
        return {
            "incident_id": incident_id,
            "annotated_term": term,
            "meaning_source": meaning.source.value,
            "definition": meaning.definition,
            "usage_examples": meaning.usage_examples,
            "note": "This annotation is descriptive only and does not modify the incident record."
        }
    
    def annotate_entity(self, entity_id: str, term: str, meaning: MeaningEntry) -> Dict[str, Any]:
        """
        Annotate entity with meaning.
        
        CONSTRAINT: Returns annotation, does not modify entity.
        """
        return {
            "entity_id": entity_id,
            "annotated_term": term,
            "meaning_source": meaning.source.value,
            "definition": meaning.definition,
            "usage_examples": meaning.usage_examples,
            "note": "This annotation is descriptive only and does not modify the entity record."
        }
    
    def interpret_pattern(self, pattern_description: str, meanings: List[MeaningEntry]) -> Dict[str, Any]:
        """
        Interpret a pattern using meanings.
        
        CONSTRAINT: Answers "How can this be understood?" never "What will happen?"
        """
        return {
            "pattern": pattern_description,
            "interpretations": [m.to_dict() for m in meanings],
            "note": "This is a descriptive interpretation. It does not predict, prescribe, or influence outcomes."
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize entire meaning overlay."""
        return {
            "layers": {source.value: layer.to_dict() for source, layer in self.layers.items()}
        }


class EtymologyLayer(MeaningLayer):
    """Specialized layer for etymological meanings."""
    
    def __init__(self):
        """Initialize etymology layer."""
        super().__init__(MeaningSource.ETYMOLOGY)
    
    def add_etymology(self, term: str, origin: str, historical_usage: List[str]) -> MeaningEntry:
        """Add etymological entry."""
        entry = MeaningEntry(
            term=term,
            source=MeaningSource.ETYMOLOGY,
            definition=f"Etymology: {origin}",
            usage_examples=historical_usage,
            context={"type": "historical_linguistic"}
        )
        self.add_entry(entry)
        return entry


class CulturalLayer(MeaningLayer):
    """Specialized layer for cultural meanings."""
    
    def __init__(self):
        """Initialize cultural layer."""
        super().__init__(MeaningSource.CULTURAL_USAGE)
    
    def add_cultural_meaning(self, term: str, cultures: List[str], meaning: str) -> MeaningEntry:
        """Add cultural meaning entry."""
        entry = MeaningEntry(
            term=term,
            source=MeaningSource.CULTURAL_USAGE,
            definition=meaning,
            context={"cultures": cultures}
        )
        self.add_entry(entry)
        return entry


class GeographicLayer(MeaningLayer):
    """Specialized layer for geographic meanings."""
    
    def __init__(self):
        """Initialize geographic layer."""
        super().__init__(MeaningSource.GEOGRAPHIC_CONTEXT)
    
    def add_geographic_meaning(self, term: str, regions: List[str], meaning: str) -> MeaningEntry:
        """Add geographic meaning entry."""
        entry = MeaningEntry(
            term=term,
            source=MeaningSource.GEOGRAPHIC_CONTEXT,
            definition=meaning,
            context={"regions": regions}
        )
        self.add_entry(entry)
        return entry


# FINAL INVARIANT
"""
Meaning overlays:
- Annotate, never modify
- Interpret, never prescribe
- Describe, never predict
- Answer "How?" never "What will?"
"""
