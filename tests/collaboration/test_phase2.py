"""
Tests for Phase 2: Context, Conflict Resolution, and Auditing
"""

import pytest
from datetime import datetime, timedelta
from src.collaboration.context_manager import (
    ContextManager, Context, ContextType, AccessLevel, ContextMetadata
)
from src.collaboration.conflict_resolver import (
    ConflictResolver, Conflict, ConflictType, ConflictOption,
    ResolutionStrategy, ConflictStatus
)
from src.collaboration.audit_logger import AuditLogger, AuditEventType


class TestContextManager:
    """Tests for context management."""
    
    def test_create_context(self):
        """Test creating a context."""
        manager = ContextManager()
        
        context = manager.create_context(
            context_id="project-roadmap",
            context_type=ContextType.PROJECT,
            owner="ProductOwner",
            data={"q1": "goals", "q2": "goals"},
            access_level=AccessLevel.TEAM
        )
        
        assert context.metadata.context_id == "project-roadmap"
        assert context.metadata.owner == "ProductOwner"
        assert context.metadata.access_level == AccessLevel.TEAM
    
    def test_context_access_control(self):
        """Test context access control."""
        manager = ContextManager()
        
        context = manager.create_context(
            context_id="private-notes",
            context_type=ContextType.TASK,
            owner="Developer",
            data={"notes": "private"},
            access_level=AccessLevel.PRIVATE
        )
        
        # Owner should have access
        retrieved = manager.get_context("private-notes", "Developer")
        assert retrieved is not None
        
        # Others should not have access
        retrieved = manager.get_context("private-notes", "ProductOwner")
        assert retrieved is None
    
    def test_share_context(self):
        """Test sharing context with other agents."""
        manager = ContextManager()
        
        manager.create_context(
            context_id="sprint-plan",
            context_type=ContextType.SPRINT,
            owner="ProjectLeader",
            data={"sprint": "25", "goal": "feature"},
            access_level=AccessLevel.TEAM
        )
        
        # Share with agents
        manager.share_context("sprint-plan", ["Developer", "Reviewer"])
        
        # Developers should now have access
        dev_context = manager.get_context("sprint-plan", "Developer")
        assert dev_context is not None
    
    def test_update_context(self):
        """Test updating context."""
        manager = ContextManager()
        
        manager.create_context(
            context_id="config",
            context_type=ContextType.PROJECT,
            owner="Admin",
            data={"setting1": "value1"}
        )
        
        # Update context
        success = manager.update_context(
            "config",
            "Admin",
            {"setting2": "value2"}
        )
        
        assert success
        
        # Retrieve and verify
        context = manager.get_context("config", "Admin")
        assert context.data["setting1"] == "value1"
        assert context.data["setting2"] == "value2"
    
    def test_context_versioning(self):
        """Test context version history."""
        manager = ContextManager()
        
        manager.create_context(
            context_id="versioned",
            context_type=ContextType.TASK,
            owner="Owner",
            data={"version": 1}
        )
        
        # Make multiple updates
        manager.update_context("versioned", "Owner", {"version": 2})
        manager.update_context("versioned", "Owner", {"version": 3})
        
        # Check version
        context = manager.get_context("versioned", "Owner")
        assert context.metadata.version == 3
        
        # Get history
        history = manager.get_context_history("versioned")
        assert len(history) >= 2  # At least the 2 updates
    
    def test_context_expiration(self):
        """Test context TTL and expiration."""
        manager = ContextManager()
        
        # Create context with 1 second TTL
        context = manager.create_context(
            context_id="temp-context",
            context_type=ContextType.TASK,
            owner="Owner",
            data={"temp": "data"},
            ttl=1  # 1 second
        )
        
        # Should be accessible initially
        retrieved = manager.get_context("temp-context", "Owner")
        assert retrieved is not None
        
        # Simulate expiration
        context.metadata.created_at = datetime.utcnow() - timedelta(seconds=10)
        
        # Should not be accessible now
        retrieved = manager.get_context("temp-context", "Owner")
        assert retrieved is None
    
    def test_find_contexts(self):
        """Test finding contexts by type and tags."""
        manager = ContextManager()
        
        # Create contexts with tags
        manager.create_context(
            context_id="ctx1",
            context_type=ContextType.PROJECT,
            owner="Owner",
            data={},
            tags={"important", "milestone"}
        )
        
        manager.create_context(
            context_id="ctx2",
            context_type=ContextType.TASK,
            owner="Owner",
            data={},
            tags={"urgent"}
        )
        
        # Find by type
        projects = manager.find_contexts(
            "Owner",
            context_type=ContextType.PROJECT
        )
        assert len(projects) == 1
        assert projects[0].metadata.context_id == "ctx1"
        
        # Find by tags
        important = manager.find_contexts(
            "Owner",
            tags={"important"}
        )
        assert len(important) == 1
    
    def test_context_linking(self):
        """Test linking related contexts."""
        manager = ContextManager()
        
        manager.create_context("ctx1", ContextType.PROJECT, "Owner", {})
        manager.create_context("ctx2", ContextType.SPRINT, "Owner", {})
        
        # Link contexts
        manager.link_contexts("ctx1", "ctx2")
        
        # Get related
        related = manager.get_related_contexts("ctx1")
        assert len(related) == 1
        assert related[0].metadata.context_id == "ctx2"


class TestConflictResolver:
    """Tests for conflict resolution."""
    
    def test_create_conflict(self):
        """Test creating a conflict."""
        resolver = ConflictResolver()
        
        options = [
            ConflictOption(
                option_id="opt1",
                proposed_by="Developer",
                description="Approach A",
                rationale="Better performance"
            ),
            ConflictOption(
                option_id="opt2",
                proposed_by="Designer",
                description="Approach B",
                rationale="Better UX"
            )
        ]
        
        conflict = resolver.create_conflict(
            conflict_id="design-conflict",
            conflict_type=ConflictType.DESIGN_CONFLICT,
            agents_involved=["Developer", "Designer"],
            topic="Component design",
            options=options
        )
        
        assert len(conflict.options) == 2
        assert conflict.status == ConflictStatus.OPEN
    
    def test_resolve_by_majority(self):
        """Test majority vote resolution."""
        resolver = ConflictResolver()
        
        options = [
            ConflictOption("opt1", "A", "Option A", "Rationale A"),
            ConflictOption("opt2", "B", "Option B", "Rationale B")
        ]
        
        conflict = resolver.create_conflict(
            "conflict1",
            ConflictType.DECISION_CONFLICT,
            ["A", "B", "C"],
            "Decision topic",
            options
        )
        
        # Vote
        conflict.vote("A", "opt1")
        conflict.vote("B", "opt1")
        conflict.vote("C", "opt2")
        
        # Resolve
        result = resolver.resolve("conflict1", ResolutionStrategy.MAJORITY_VOTE)
        
        assert result == "opt1"  # Has 2 votes
        assert resolver.conflicts["conflict1"].status == ConflictStatus.RESOLVED
    
    def test_resolve_by_consensus(self):
        """Test consensus resolution."""
        resolver = ConflictResolver()
        
        options = [
            ConflictOption("opt1", "A", "Option A", "Rationale A"),
        ]
        
        conflict = resolver.create_conflict(
            "consensus-conflict",
            ConflictType.DECISION_CONFLICT,
            ["A", "B"],
            "Need consensus",
            options
        )
        
        # Not all agree yet
        conflict.vote("A", "opt1")
        result = resolver.resolve("consensus-conflict", ResolutionStrategy.CONSENSUS)
        assert result is None
        
        # All agree
        conflict.vote("B", "opt1")
        result = resolver.resolve("consensus-conflict", ResolutionStrategy.CONSENSUS)
        assert result == "opt1"
    
    def test_escalate_conflict(self):
        """Test escalating conflict."""
        resolver = ConflictResolver()
        
        options = [ConflictOption("opt1", "A", "Option A", "Reason")]
        conflict = resolver.create_conflict(
            "escalated",
            ConflictType.PRIORITY_CONFLICT,
            ["A", "B"],
            "Cannot decide",
            options
        )
        
        # Escalate
        escalated = resolver.escalate_conflict(
            "escalated",
            "Unable to reach agreement"
        )
        
        assert escalated
        assert resolver.conflicts["escalated"].status == ConflictStatus.ESCALATED
    
    def test_suggest_resolution(self):
        """Test getting resolution suggestions."""
        resolver = ConflictResolver()
        
        options = [
            ConflictOption("opt1", "A", "Option A", "Rationale A"),
            ConflictOption("opt2", "B", "Option B", "Rationale B")
        ]
        
        conflict = resolver.create_conflict(
            "suggest",
            ConflictType.DECISION_CONFLICT,
            ["A", "B"],
            "Topic",
            options
        )
        
        conflict.vote("A", "opt1")
        conflict.vote("B", "opt1")
        
        suggestion = resolver.suggest_resolution("suggest")
        
        assert suggestion["recommendation"] == "opt1"
        assert len(suggestion["options"]) == 2


class TestAuditLogger:
    """Tests for audit logging."""
    
    def test_log_event(self):
        """Test logging an event."""
        logger = AuditLogger()
        
        event = logger.log_event(
            event_type=AuditEventType.MESSAGE_SENT,
            agent="Agent A",
            subject="msg-123",
            action="Sent message",
            details={"recipient": "Agent B"}
        )
        
        assert event.event_type == AuditEventType.MESSAGE_SENT
        assert event.agent == "Agent A"
        assert event.status == "success"
    
    def test_get_events_for_subject(self):
        """Test retrieving events for a subject."""
        logger = AuditLogger()
        
        # Log multiple events for same subject
        logger.log_context_created("Agent A", "ctx1", "project")
        logger.log_context_created("Agent B", "ctx1", "sprint")
        logger.log_context_shared("Agent A", "ctx1", ["Agent C"])
        
        # Get events for ctx1
        events = logger.get_events_for_subject("ctx1")
        assert len(events) == 3
    
    def test_get_events_by_agent(self):
        """Test retrieving events by agent."""
        logger = AuditLogger()
        
        # Log events from different agents
        logger.log_event(AuditEventType.MESSAGE_SENT, "Agent A", "msg1", "sent")
        logger.log_event(AuditEventType.MESSAGE_SENT, "Agent B", "msg2", "sent")
        logger.log_event(AuditEventType.MESSAGE_SENT, "Agent A", "msg3", "sent")
        
        # Get Agent A's events
        events = logger.get_events_by_agent("Agent A")
        assert len(events) == 2
        assert all(e.agent == "Agent A" for e in events)
    
    def test_generate_report(self):
        """Test generating audit report."""
        logger = AuditLogger()
        
        # Log events
        logger.log_context_created("Agent A", "ctx1", "project")
        logger.log_context_shared("Agent B", "ctx1", ["Agent C"])
        logger.log_task_completed("Agent A", "ctx1", {"status": "done"})
        
        # Generate report
        report = logger.generate_report("ctx1")
        
        assert report["subject"] == "ctx1"
        assert report["total_events"] == 3
        assert "Agent A" in report["agents_involved"]
        assert "Agent B" in report["agents_involved"]
    
    def test_export_events(self):
        """Test exporting events as JSON."""
        logger = AuditLogger()
        
        logger.log_event(AuditEventType.MESSAGE_SENT, "A", "msg1", "sent")
        logger.log_event(AuditEventType.MESSAGE_SENT, "B", "msg2", "sent")
        
        json_str = logger.export_events()
        
        assert json_str is not None
        assert "Message" in json_str or "message" in json_str


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
