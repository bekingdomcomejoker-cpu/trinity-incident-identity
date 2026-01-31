"""
Trinity Incident-Identity Engine
Validation & Enforcement Module

Enforces:
- Append-only constraints
- No-agency rules
- No-prediction rules
- No-prescription rules
"""

from typing import List, Dict, Any, Tuple
import re


class SafetyValidator:
    """
    Validates that system maintains safety invariants.
    
    INVARIANTS:
    - Nothing acts
    - Nothing predicts
    - Nothing decides
    - Everything witnesses
    """
    
    # Forbidden patterns (predictive/prescriptive language)
    FORBIDDEN_PATTERNS = [
        r'\bwill\s+(do|be|happen|occur)',
        r'\bshould\s+(do|be)',
        r'\bmust\s+(do|be)',
        r'\bpredict',
        r'\boptimize',
        r'\brecommend',
        r'\bshould\s+',
        r'\bwill\s+',
        r'\bdestiny',
        r'\bfate',
        r'\bmeant\s+to',
        r'\bsupposed\s+to',
        r'\bwill\s+happen',
        r'\bwill\s+occur',
        r'\bwill\s+be',
        r'\bwill\s+do',
        r'\bshould\s+happen',
        r'\bshould\s+occur',
        r'\bshould\s+be',
        r'\bshould\s+do',
        r'\bmust\s+happen',
        r'\bmust\s+occur',
        r'\bmust\s+be',
        r'\bmust\s+do',
    ]
    
    @classmethod
    def validate_fact(cls, fact: str) -> Tuple[bool, str]:
        """
        Validate that a fact is observable/attestable, not predictive/prescriptive.
        
        Returns: (is_valid, error_message)
        """
        fact_lower = fact.lower()
        
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, fact_lower):
                return False, f"Fact contains forbidden pattern: {pattern}"
        
        return True, ""
    
    @classmethod
    def validate_definition(cls, definition: str) -> Tuple[bool, str]:
        """
        Validate that a definition is descriptive, not prescriptive.
        
        Returns: (is_valid, error_message)
        """
        definition_lower = definition.lower()
        
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, definition_lower):
                return False, f"Definition contains forbidden pattern: {pattern}"
        
        return True, ""
    
    @classmethod
    def validate_no_agency(cls, text: str) -> Tuple[bool, str]:
        """
        Validate that text does not imply agency or action.
        
        Returns: (is_valid, error_message)
        """
        agency_patterns = [
            r'\bshould\s+',
            r'\bmust\s+',
            r'\bwill\s+',
            r'\bcommand',
            r'\bcontrol',
            r'\binfluence',
            r'\boptimize',
            r'\bmanipulate',
        ]
        
        text_lower = text.lower()
        
        for pattern in agency_patterns:
            if re.search(pattern, text_lower):
                return False, f"Text implies agency: {pattern}"
        
        return True, ""
    
    @classmethod
    def validate_no_prediction(cls, text: str) -> Tuple[bool, str]:
        """
        Validate that text does not make predictions.
        
        Returns: (is_valid, error_message)
        """
        prediction_patterns = [
            r'\bwill\s+',
            r'\bwill\s+happen',
            r'\bwill\s+occur',
            r'\bpredict',
            r'\bforecast',
            r'\bdestiny',
            r'\bfate',
            r'\bfuture',
            r'\bwill\s+be',
        ]
        
        text_lower = text.lower()
        
        for pattern in prediction_patterns:
            if re.search(pattern, text_lower):
                return False, f"Text makes prediction: {pattern}"
        
        return True, ""


class AppendOnlyValidator:
    """
    Enforces append-only constraints.
    
    INVARIANTS:
    - No overwrites
    - No deletes
    - Only append operations
    """
    
    @staticmethod
    def validate_append_only_operation(operation: str) -> Tuple[bool, str]:
        """
        Validate that operation is append-only.
        
        Returns: (is_valid, error_message)
        """
        forbidden_operations = [
            "delete",
            "remove",
            "update",
            "modify",
            "edit",
            "overwrite",
            "replace",
            "truncate",
            "clear",
            "reset",
        ]
        
        operation_lower = operation.lower()
        
        for forbidden_op in forbidden_operations:
            if forbidden_op in operation_lower:
                return False, f"Operation violates append-only constraint: {forbidden_op}"
        
        return True, ""
    
    @staticmethod
    def validate_incident_immutability(incident_id: str, original_data: Dict[str, Any], modified_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate that incident has not been modified.
        
        Returns: (is_valid, error_message)
        """
        if original_data == modified_data:
            return True, ""
        
        # Check what changed
        changed_keys = []
        for key in original_data:
            if original_data[key] != modified_data.get(key):
                changed_keys.append(key)
        
        return False, f"Incident {incident_id} was modified. Changed keys: {changed_keys}"


class NoAgencyValidator:
    """
    Validates that system maintains no-agency invariant.
    
    INVARIANTS:
    - No prediction
    - No prescription
    - No optimization
    - No feedback loops
    - No control
    """
    
    @staticmethod
    def validate_no_feedback_loops(component_name: str, outputs: List[str]) -> Tuple[bool, str]:
        """
        Validate that component does not create feedback loops.
        
        Returns: (is_valid, error_message)
        """
        feedback_patterns = [
            "adjust",
            "optimize",
            "improve",
            "refine",
            "enhance",
            "modify based on",
            "respond to",
            "react to",
        ]
        
        for output in outputs:
            output_lower = output.lower()
            for pattern in feedback_patterns:
                if pattern in output_lower:
                    return False, f"Component {component_name} creates feedback loop: {pattern}"
        
        return True, ""
    
    @staticmethod
    def validate_no_control(component_name: str, capabilities: List[str]) -> Tuple[bool, str]:
        """
        Validate that component does not exert control.
        
        Returns: (is_valid, error_message)
        """
        control_capabilities = [
            "command",
            "control",
            "influence",
            "manipulate",
            "decide",
            "determine",
            "choose",
            "select",
            "execute action",
        ]
        
        for capability in capabilities:
            capability_lower = capability.lower()
            for control_cap in control_capabilities:
                if control_cap in capability_lower:
                    return False, f"Component {component_name} exerts control: {control_cap}"
        
        return True, ""


class IntegrityValidator:
    """
    Validates system integrity.
    
    INVARIANTS:
    - Incidents are immutable
    - Entities are derived only
    - Meaning is descriptive only
    - Snapshots are views only
    """
    
    @staticmethod
    def validate_incident_integrity(incident: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate incident integrity.
        
        Returns: (is_valid, error_message)
        """
        required_fields = [
            "incident_id",
            "date",
            "system",
            "participants",
            "facts",
        ]
        
        for field in required_fields:
            if field not in incident:
                return False, f"Incident missing required field: {field}"
        
        # Validate facts
        for fact in incident.get("facts", []):
            is_valid, error = SafetyValidator.validate_fact(fact)
            if not is_valid:
                return False, f"Incident contains invalid fact: {error}"
        
        return True, ""
    
    @staticmethod
    def validate_entity_is_derived(entity: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate that entity is derived from incidents only.
        
        Returns: (is_valid, error_message)
        """
        # Entity should only have entity_id and incidents
        allowed_keys = {"entity_id", "incidents"}
        actual_keys = set(entity.keys())
        
        extra_keys = actual_keys - allowed_keys
        if extra_keys:
            return False, f"Entity has extra keys (not derived): {extra_keys}"
        
        return True, ""
    
    @staticmethod
    def validate_meaning_is_descriptive(meaning: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate that meaning is descriptive only.
        
        Returns: (is_valid, error_message)
        """
        definition = meaning.get("definition", "")
        
        is_valid, error = SafetyValidator.validate_definition(definition)
        if not is_valid:
            return False, f"Meaning contains prescriptive language: {error}"
        
        return True, ""
    
    @staticmethod
    def validate_snapshot_is_view(snapshot: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate that snapshot is marked as a view.
        
        Returns: (is_valid, error_message)
        """
        metadata = snapshot.get("metadata", {})
        note = metadata.get("note", "")
        
        if "view" not in note.lower() or "not authoritative" not in note.lower():
            return False, "Snapshot is not marked as a view"
        
        return True, ""


class SystemValidator:
    """
    Master validator for entire system.
    
    Runs all validators and reports violations.
    """
    
    @staticmethod
    def validate_system_state(system_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate entire system state.
        
        Returns: validation report
        """
        report = {
            "valid": True,
            "violations": [],
            "warnings": [],
        }
        
        # Validate incidents
        for incident in system_state.get("incidents", []):
            is_valid, error = IntegrityValidator.validate_incident_integrity(incident)
            if not is_valid:
                report["valid"] = False
                report["violations"].append(f"Incident {incident.get('incident_id')}: {error}")
        
        # Validate entities
        for entity in system_state.get("entities", []):
            is_valid, error = IntegrityValidator.validate_entity_is_derived(entity)
            if not is_valid:
                report["valid"] = False
                report["violations"].append(f"Entity {entity.get('entity_id')}: {error}")
        
        # Validate meanings
        for meaning in system_state.get("meanings", []):
            is_valid, error = IntegrityValidator.validate_meaning_is_descriptive(meaning)
            if not is_valid:
                report["valid"] = False
                report["violations"].append(f"Meaning {meaning.get('term')}: {error}")
        
        # Validate snapshots
        for snapshot in system_state.get("snapshots", []):
            is_valid, error = IntegrityValidator.validate_snapshot_is_view(snapshot)
            if not is_valid:
                report["valid"] = False
                report["violations"].append(f"Snapshot {snapshot.get('entity_id')}: {error}")
        
        return report


# FINAL INVARIANT
"""
Validation enforces:
- Append-only constraints
- No-agency rules
- No-prediction rules
- No-prescription rules
- Integrity constraints

Violations are fatal.
"""
