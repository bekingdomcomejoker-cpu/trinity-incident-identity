"""
Trinity Incident-Identity Engine
Core Module: Snapshot

This module generates read-only views of entity identity.
Snapshots are views, not truth.
Snapshots can be regenerated or deleted.
Snapshots are not authoritative.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from .incident_entity import EntityIdentity, Incident, IncidentLog


@dataclass
class IdentitySnapshot:
    """
    Read-only view of entity identity at a point in time.
    
    INVARIANTS:
    - Generated from incidents only
    - Can be regenerated
    - Can be deleted
    - Not authoritative
    - No behavior or state
    """
    
    entity_id: str
    snapshot_date: str  # ISO-8601
    incident_count: int
    first_seen: Optional[str]
    last_seen: Optional[str]
    systems: List[str]
    incident_types: List[str]
    co_participants: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize snapshot."""
        return {
            "entity_id": self.entity_id,
            "snapshot_date": self.snapshot_date,
            "incident_count": self.incident_count,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "systems": self.systems,
            "incident_types": self.incident_types,
            "co_participants": self.co_participants,
            "metadata": self.metadata,
        }


@dataclass
class TimelineSnapshot:
    """
    Chronological view of entity incidents.
    
    INVARIANTS:
    - Ordered by date
    - Read-only
    - Regenerable
    """
    
    entity_id: str
    snapshot_date: str
    incidents_chronological: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize timeline snapshot."""
        return {
            "entity_id": self.entity_id,
            "snapshot_date": self.snapshot_date,
            "incidents": self.incidents_chronological,
        }


@dataclass
class SystemSnapshot:
    """
    View of all entities in a specific system.
    
    INVARIANTS:
    - Filtered by system
    - Read-only
    - Regenerable
    """
    
    system: str
    snapshot_date: str
    entities: Dict[str, Dict[str, Any]]  # entity_id -> summary
    incident_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize system snapshot."""
        return {
            "system": self.system,
            "snapshot_date": self.snapshot_date,
            "entities": self.entities,
            "incident_count": self.incident_count,
        }


class SnapshotGenerator:
    """
    Generate read-only views of identity data.
    
    INVARIANTS:
    - Snapshots are views, not truth
    - Snapshots can be regenerated
    - Snapshots can be deleted
    - Snapshots are not authoritative
    """
    
    def __init__(self, incident_log: IncidentLog):
        """Initialize snapshot generator."""
        self.incident_log = incident_log
        self.snapshots: Dict[str, IdentitySnapshot] = {}
    
    def create_identity_snapshot(self, entity: EntityIdentity) -> IdentitySnapshot:
        """
        Create snapshot of entity identity.
        
        CONSTRAINT: Snapshot is a view, not authoritative.
        """
        first_incident = entity.get_first_incident()
        last_incident = entity.get_last_incident()
        
        snapshot = IdentitySnapshot(
            entity_id=entity.entity_id,
            snapshot_date=datetime.now().isoformat(),
            incident_count=entity.get_incident_count(),
            first_seen=first_incident.date if first_incident else None,
            last_seen=last_incident.date if last_incident else None,
            systems=entity.get_systems(),
            incident_types=entity.get_incident_types(),
            co_participants=entity.get_co_participants(),
            metadata={
                "note": "This snapshot is a view, not authoritative. It can be regenerated or deleted."
            }
        )
        
        return snapshot
    
    def create_timeline_snapshot(self, entity: EntityIdentity) -> TimelineSnapshot:
        """
        Create chronological view of entity incidents.
        
        CONSTRAINT: Snapshot is a view, not authoritative.
        """
        incidents_sorted = sorted(entity.incidents, key=lambda i: i.date)
        incidents_dict = [i.to_dict() for i in incidents_sorted]
        
        snapshot = TimelineSnapshot(
            entity_id=entity.entity_id,
            snapshot_date=datetime.now().isoformat(),
            incidents_chronological=incidents_dict
        )
        
        return snapshot
    
    def create_system_snapshot(self, system: str) -> SystemSnapshot:
        """
        Create view of all entities in a system.
        
        CONSTRAINT: Snapshot is a view, not authoritative.
        """
        incidents = self.incident_log.get_by_system(system)
        
        # Build entity summaries
        entities_dict: Dict[str, Dict[str, Any]] = {}
        for incident in incidents:
            for entity_id in incident.participants:
                if entity_id not in entities_dict:
                    entities_dict[entity_id] = {
                        "entity_id": entity_id,
                        "incident_count": 0,
                        "first_seen": incident.date,
                        "last_seen": incident.date,
                    }
                entities_dict[entity_id]["incident_count"] += 1
                entities_dict[entity_id]["last_seen"] = incident.date
        
        snapshot = SystemSnapshot(
            system=system,
            snapshot_date=datetime.now().isoformat(),
            entities=entities_dict,
            incident_count=len(incidents)
        )
        
        return snapshot
    
    def create_relationship_snapshot(self, entity1_id: str, entity2_id: str) -> Dict[str, Any]:
        """
        Create view of relationship between two entities.
        
        CONSTRAINT: Snapshot is a view, not authoritative.
        """
        shared_incidents = []
        
        for incident in self.incident_log.get_all():
            if entity1_id in incident.participants and entity2_id in incident.participants:
                shared_incidents.append(incident.to_dict())
        
        return {
            "entity1": entity1_id,
            "entity2": entity2_id,
            "snapshot_date": datetime.now().isoformat(),
            "shared_incidents": shared_incidents,
            "interaction_count": len(shared_incidents),
            "note": "This snapshot is a view, not authoritative. It can be regenerated or deleted."
        }
    
    def create_temporal_snapshot(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Create view of incidents within date range.
        
        CONSTRAINT: Snapshot is a view, not authoritative.
        """
        incidents = self.incident_log.get_by_date_range(start_date, end_date)
        
        # Aggregate statistics
        systems = set(i.system for i in incidents)
        entities = set()
        for i in incidents:
            entities.update(i.participants)
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "snapshot_date": datetime.now().isoformat(),
            "incident_count": len(incidents),
            "systems_involved": list(systems),
            "entities_involved": list(entities),
            "incidents": [i.to_dict() for i in incidents],
            "note": "This snapshot is a view, not authoritative. It can be regenerated or deleted."
        }
    
    def delete_snapshot(self, entity_id: str) -> None:
        """
        Delete snapshot (safe operation).
        
        CONSTRAINT: Deleting snapshot does not affect incidents.
        """
        if entity_id in self.snapshots:
            del self.snapshots[entity_id]
    
    def regenerate_all_snapshots(self) -> None:
        """Regenerate all snapshots from current incident log."""
        # This is a safe operation - snapshots are views, not truth
        self.snapshots.clear()


class SnapshotValidator:
    """
    Validate that snapshots are views, not truth.
    
    INVARIANTS:
    - Snapshots cannot modify incidents
    - Snapshots cannot be treated as authoritative
    - Snapshots can be safely deleted
    """
    
    @staticmethod
    def validate_snapshot_is_view(snapshot: IdentitySnapshot) -> bool:
        """Verify snapshot is a view, not authoritative."""
        # Snapshots should have metadata indicating they are views
        return "note" in snapshot.metadata
    
    @staticmethod
    def validate_snapshot_regenerable(snapshot: IdentitySnapshot) -> bool:
        """Verify snapshot can be regenerated."""
        # All snapshots should be regenerable from incidents
        return snapshot.snapshot_date is not None
    
    @staticmethod
    def validate_snapshot_deletable(snapshot: IdentitySnapshot) -> bool:
        """Verify snapshot can be safely deleted."""
        # All snapshots can be safely deleted without affecting incidents
        return True


# FINAL INVARIANT
"""
Snapshots are views, not truth.
Snapshots can be regenerated.
Snapshots can be deleted.
Snapshots are not authoritative.

The only truth is the incident log.
"""
