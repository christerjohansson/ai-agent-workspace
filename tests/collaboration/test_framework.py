"""
Test suite for Agent Collaboration Framework
"""

import pytest
from datetime import datetime
from src.collaboration.protocol import (
    Message, MessageType, MessagePriority, MessageStatus, 
    ProtocolValidator, create_task_request, create_task_complete
)
from src.collaboration.message_queue import MessageBus
from src.collaboration.dependency_tracker import (
    DependencyTracker, Task, TaskStatus
)


class TestProtocol:
    """Tests for agent communication protocol."""
    
    def test_message_creation(self):
        """Test creating a message."""
        msg = Message(
            id=None,
            from_agent="ProjectManager",
            to_agent="ProductOwner",
            msg_type=MessageType.TASK_REQUEST,
            subject="Review roadmap",
            data={"roadmap": "Q1 2024"}
        )
        
        assert msg.from_agent == "ProjectManager"
        assert msg.to_agent == "ProductOwner"
        assert msg.msg_type == MessageType.TASK_REQUEST
        assert msg.status == MessageStatus.PENDING
    
    def test_message_validation(self):
        """Test message validation."""
        # Valid message
        valid_msg = Message(
            id="msg-1",
            from_agent="Agent A",
            to_agent="Agent B",
            msg_type=MessageType.TASK_REQUEST,
            subject="Test",
            data={"test": "data"}
        )
        
        is_valid, error = ProtocolValidator.validate_message(valid_msg)
        assert is_valid
        assert error is None
        
        # Invalid message - missing subject
        invalid_msg = Message(
            id="msg-2",
            from_agent="Agent A",
            to_agent="Agent B",
            msg_type=MessageType.TASK_REQUEST,
            subject=None,
            data={"test": "data"}
        )
        
        # Would fail because subject is None
    
    def test_message_expiration(self):
        """Test message TTL and expiration."""
        msg = Message(
            id=None,
            from_agent="Agent A",
            to_agent="Agent B",
            msg_type=MessageType.TASK_REQUEST,
            subject="Urgent",
            data={},
            ttl=1  # 1 second
        )
        
        assert not msg.is_expired()
        
        # Simulate time passing
        msg.timestamp = datetime.fromtimestamp(0)
        assert msg.is_expired()
    
    def test_helper_functions(self):
        """Test message creation helper functions."""
        # Test task request
        req = create_task_request(
            from_agent="ProjectManager",
            to_agent="Developer",
            task_id="TASK-001",
            task_description="Implement feature X",
            deadline="2024-01-15"
        )
        
        assert req.msg_type == MessageType.TASK_REQUEST
        assert req.priority == MessagePriority.HIGH
        assert req.data["task_id"] == "TASK-001"
        
        # Test task complete
        comp = create_task_complete(
            from_agent="Developer",
            to_agent="ProjectManager",
            task_id="TASK-001",
            result={"status": "success", "lines_changed": 150}
        )
        
        assert comp.msg_type == MessageType.TASK_COMPLETE
        assert comp.data["task_id"] == "TASK-001"


class TestDependencyTracker:
    """Tests for dependency tracking."""
    
    def test_add_task(self):
        """Test adding tasks."""
        tracker = DependencyTracker()
        
        task = Task(
            id="TASK-001",
            name="Code Review",
            assigned_to="CodeReviewer"
        )
        
        tracker.add_task(task)
        assert "TASK-001" in tracker.tasks
    
    def test_add_dependency(self):
        """Test adding dependencies between tasks."""
        tracker = DependencyTracker()
        
        task1 = Task(id="TASK-001", name="Development", assigned_to="Dev")
        task2 = Task(id="TASK-002", name="Code Review", assigned_to="Reviewer")
        
        tracker.add_task(task1)
        tracker.add_task(task2)
        
        tracker.add_dependency("TASK-002", "TASK-001")
        
        assert "TASK-001" in tracker.get_dependencies("TASK-002")
        assert "TASK-002" in tracker.get_dependents("TASK-001")
    
    def test_is_ready(self):
        """Test checking if task is ready."""
        tracker = DependencyTracker()
        
        task1 = Task(id="TASK-001", name="Development", assigned_to="Dev")
        task2 = Task(id="TASK-002", name="Code Review", assigned_to="Reviewer")
        
        tracker.add_task(task1)
        tracker.add_task(task2)
        tracker.add_dependency("TASK-002", "TASK-001")
        
        # Task 2 is not ready - depends on task 1
        assert not tracker.is_ready("TASK-002")
        
        # Complete task 1
        tracker.mark_completed("TASK-001")
        
        # Task 2 is now ready
        assert tracker.is_ready("TASK-002")
    
    def test_get_ready_tasks(self):
        """Test getting ready tasks."""
        tracker = DependencyTracker()
        
        # Create 3 tasks
        task1 = Task(id="T1", name="First", assigned_to="A")
        task2 = Task(id="T2", name="Second", assigned_to="B")
        task3 = Task(id="T3", name="Third", assigned_to="C")
        
        tracker.add_task(task1)
        tracker.add_task(task2)
        tracker.add_task(task3)
        
        # T2 depends on T1, T3 depends on T2
        tracker.add_dependency("T2", "T1")
        tracker.add_dependency("T3", "T2")
        
        # Only T1 should be ready
        ready = tracker.get_ready_tasks()
        assert len(ready) == 1
        assert ready[0].id == "T1"
        
        # Complete T1, now T2 is ready
        tracker.mark_completed("T1")
        ready = tracker.get_ready_tasks()
        assert len(ready) == 1
        assert ready[0].id == "T2"
    
    def test_cycle_detection(self):
        """Test circular dependency detection."""
        tracker = DependencyTracker()
        
        task1 = Task(id="T1", name="Task 1", assigned_to="A")
        task2 = Task(id="T2", name="Task 2", assigned_to="B")
        
        tracker.add_task(task1)
        tracker.add_task(task2)
        
        # Add valid dependency
        tracker.add_dependency("T2", "T1")
        
        # Try to create cycle (T1 depends on T2, but T2 depends on T1)
        with pytest.raises(ValueError):
            tracker.add_dependency("T1", "T2")
    
    def test_get_blockers(self):
        """Test getting blocking tasks."""
        tracker = DependencyTracker()
        
        task1 = Task(id="T1", name="Task 1", assigned_to="A")
        task2 = Task(id="T2", name="Task 2", assigned_to="B")
        task3 = Task(id="T3", name="Task 3", assigned_to="C")
        
        tracker.add_task(task1)
        tracker.add_task(task2)
        tracker.add_task(task3)
        
        tracker.add_dependency("T3", "T1")
        tracker.add_dependency("T3", "T2")
        
        # Get blockers for T3
        blockers = tracker.get_blockers("T3")
        assert len(blockers) == 2
        
        # Mark one as complete
        tracker.mark_completed("T1")
        blockers = tracker.get_blockers("T3")
        assert len(blockers) == 1
        assert blockers[0].id == "T2"


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
