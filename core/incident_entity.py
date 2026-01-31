"""
Trinity Incident-Identity Engine
Core Module: Incident & Entity Models

This module defines the source-of-truth models for incidents and derived identities.
No agency. No prediction. No optimization.
Everything witnesses.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum


class IncidentType(Enum):
    """Enumeration of incident types (descriptive only)."""
    OBSERVATION = "observation"
    INTERACTION = "interaction"
    STATE_CHANGE = "state_change"
    COMMUNICATION = "communication"
    SYSTEM_EVENT = "system_event"
    OTHER = "other"


@dataclass
class Incident:
    """
    Source-of-truth incident record.
    
    INVARIANTS:
    - Immutable after creation
    - Facts must be observable or attestable
    - No opinions, predictions, or prescriptions
    - Append-only in storage
    """
    
    incident_id: str
    date: str  # ISO-8601 format
    system: str  # System where incident occurred
    incident_type: IncidentType
    participants: List[str]  # entity_ids involved
    facts: List[str]  # Observable, attestable statements
    context: Dict[str, Any] = field(default_factory=dict)
    summary: str = ""  # Plain language description
    outcome: str = ""  # What actually occurred
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate incident structure."""
        if not self.incident_id:
            raise ValueError("incident_id cannot be empty")
        if not self.date:
            raise ValueError("date cannot be empty")
        if not self.system:
            raise ValueError("system cannot be empty")
        if not self.participants:
            raise ValueError("participants cannot be empty")
        if not self.facts:
            raise ValueError("facts cannot be empty")
        
        # Validate facts are not opinions
        forbidden_phrases = [
            "should", "will", "must", "predict", "optimize",
            "best", "worst", "good", "bad", "right", "wrong",
            "destiny", "fate", "meant to", "supposed to"
        ]
        
        for fact in self.facts:
            fact_lower = fact.lower()
            for phrase in forbidden_phrases:
                if phrase in fact_lower:
                    raise ValueError(
                        f"Fact contains prescriptive language '{phrase}': {fact}"
                    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize incident to dictionary."""
        return {
            "incident_id": self.incident_id,
            "date": self.date,
            "system": self.system,
            "incident_type": self.incident_type.value,
            "participants": self.participants,
            "facts": self.facts,
            "context": self.context,
            "summary": self.summary,
            "outcome": self.outcome,
            "metadata": self.metadata,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Incident":
        """Deserialize incident from dictionary."""
        return Incident(
            incident_id=data["incident_id"],
            date=data["date"],
            system=data["system"],
            incident_type=IncidentType(data.get("incident_type", "other")),
            participants=data["participants"],
            facts=data["facts"],
            context=data.get("context", {}),
            summary=data.get("summary", ""),
            outcome=data.get("outcome", ""),
            metadata=data.get("metadata", {}),
        )


@dataclass
class EntityIdentity:
    """
    Derived identity view.
    
    INVARIANTS:
    - Identity emerges from incidents only
    - No attributes beyond incidents
    - No behavior or state mutation
    - Retrospective only
    - Cannot predict or prescribe
    """
    
    entity_id: str
    incidents: List[Incident] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate entity structure."""
        if not self.entity_id:
            raise ValueError("entity_id cannot be empty")
    
    def add_incident(self, incident: Incident) -> None:
        """
        Add incident to entity identity.
        
        CONSTRAINT: Append-only operation.
        """
        if incident.entity_id not in incident.participants:
            raise ValueError(
                f"Incident does not involve entity {self.entity_id}"
            )
        self.incidents.append(incident)
    
    def get_incident_count(self) -> int:
        """Get total number of incidents."""
        return len(self.incidents)
    
    def get_first_incident(self) -> Optional[Incident]:
        """Get earliest incident."""
        if not self.incidents:
            return None
        return min(self.incidents, key=lambda i: i.date)
    
    def get_last_incident(self) -> Optional[Incident]:
        """Get most recent incident."""
        if not self.incidents:
            return None
        return max(self.incidents, key=lambda i: i.date)
    
    def get_systems(self) -> List[str]:
        """Get list of systems where entity appears."""
        return list(set(i.system for i in self.incidents))
    
    def get_incident_types(self) -> List[str]:
        """Get types of incidents involving this entity."""
        return list(set(i.incident_type.value for i in self.incidents))
    
    def get_co_participants(self) -> List[str]:
        """Get other entities that appear with this entity."""
        co_participants = set()
        for incident in self.incidents:
            for participant in incident.participants:
                if participant != self.entity_id:
                    co_participants.add(participant)
        return list(co_participants)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize entity identity to dictionary."""
        return {
            "entity_id": self.entity_id,
            "incident_count": self.get_incident_count(),
            "first_seen": self.get_first_incident().date if self.get_first_incident() else None,
            "last_seen": self.get_last_incident().date if self.get_last_incident() else None,
            "systems": self.get_systems(),
            "incident_types": self.get_incident_types(),
            "co_participants": self.get_co_participants(),
        }
    
    def to_full_dict(self) -> Dict[str, Any]:
        """Serialize entity with full incident history."""
        return {
            "entity_id": self.entity_id,
            "incidents": [i.to_dict() for i in self.incidents],
            "summary": self.to_dict(),
        }


class IncidentLog:
    """
    Append-only incident log.
    
    INVARIANTS:
    - No overwrites
    - No deletes
    - Only append operations
    """
    
    def __init__(self):
        """Initialize empty incident log."""
        self.incidents: List[Incident] = []
    
    def append(self, incident: Incident) -> None:
        """
        Append incident to log.
        
        CONSTRAINT: This is the only write operation.
        """
        self.incidents.append(incident)
    
    def get_all(self) -> List[Incident]:
        """Get all incidents (read-only view)."""
        return list(self.incidents)
    
    def get_by_entity(self, entity_id: str) -> List[Incident]:
        """Get incidents involving specific entity."""
        return [i for i in self.incidents if entity_id in i.participants]
    
    def get_by_system(self, system: str) -> List[Incident]:
        """Get incidents from specific system."""
        return [i for i in self.incidents if i.system == system]
    
    def get_by_date_range(self, start_date: str, end_date: str) -> List[Incident]:
        """Get incidents within date range (ISO-8601)."""
        return [i for i in self.incidents if start_date <= i.date <= end_date]
    
    def get_count(self) -> int:
        """Get total incident count."""
        return len(self.incidents)


# FINAL INVARIANT
"""
Nothing in this system acts.
Nothing predicts.
Nothing decides.
Everything witnesses.
"""
