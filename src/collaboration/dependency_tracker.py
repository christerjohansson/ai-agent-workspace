"""
Dependency Tracker

Tracks task dependencies and validates execution readiness.
"""

from dataclasses import dataclass, field
from typing import Dict, Set, List, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Status of a task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class Task:
    """Represents a task that can have dependencies."""
    
    id: str
    name: str
    assigned_to: str
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 2
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class Dependency:
    """Represents a dependency between tasks."""
    
    dependent_task_id: str  # Task that depends
    blocking_task_id: str   # Task that must complete first
    dependency_type: str = "blocks"  # blocks, triggers, precedes
    created_at: datetime = field(default_factory=datetime.utcnow)


class DependencyTracker:
    """
    Tracks and manages task dependencies.
    
    Ensures tasks are only executed when their dependencies are met.
    """
    
    def __init__(self):
        """Initialize dependency tracker."""
        self.tasks: Dict[str, Task] = {}
        self.dependencies: Dict[str, Set[str]] = {}  # task_id -> set of blocking task_ids
        self.dependents: Dict[str, Set[str]] = {}    # task_id -> set of dependent task_ids
    
    def add_task(self, task: Task) -> None:
        """Add a task to the tracker."""
        self.tasks[task.id] = task
        if task.id not in self.dependencies:
            self.dependencies[task.id] = set()
        if task.id not in self.dependents:
            self.dependents[task.id] = set()
    
    def add_dependency(
        self,
        dependent_task_id: str,
        blocking_task_id: str,
        dependency_type: str = "blocks"
    ) -> None:
        """
        Add a dependency between tasks.
        
        Args:
            dependent_task_id: Task that depends on another
            blocking_task_id: Task that must complete first
            dependency_type: Type of dependency
        """
        # Validate tasks exist
        if dependent_task_id not in self.tasks:
            raise ValueError(f"Task {dependent_task_id} not found")
        if blocking_task_id not in self.tasks:
            raise ValueError(f"Task {blocking_task_id} not found")
        
        # Check for circular dependencies
        if self._would_create_cycle(dependent_task_id, blocking_task_id):
            raise ValueError(
                f"Adding dependency would create cycle: "
                f"{dependent_task_id} -> {blocking_task_id}"
            )
        
        # Add dependency
        self.dependencies[dependent_task_id].add(blocking_task_id)
        self.dependents[blocking_task_id].add(dependent_task_id)
    
    def remove_dependency(
        self,
        dependent_task_id: str,
        blocking_task_id: str
    ) -> None:
        """Remove a dependency between tasks."""
        self.dependencies[dependent_task_id].discard(blocking_task_id)
        self.dependents[blocking_task_id].discard(dependent_task_id)
    
    def get_dependencies(self, task_id: str) -> Set[str]:
        """Get all tasks that must complete before this task."""
        return self.dependencies.get(task_id, set()).copy()
    
    def get_dependents(self, task_id: str) -> Set[str]:
        """Get all tasks that depend on this task."""
        return self.dependents.get(task_id, set()).copy()
    
    def get_blockers(self, task_id: str) -> List[Task]:
        """
        Get tasks that are blocking the given task.
        
        Returns only blockers that haven't completed yet.
        """
        blocker_ids = self.dependencies.get(task_id, set())
        blockers = []
        
        for blocker_id in blocker_ids:
            task = self.tasks.get(blocker_id)
            if task and task.status != TaskStatus.COMPLETED:
                blockers.append(task)
        
        return blockers
    
    def is_ready(self, task_id: str) -> bool:
        """
        Check if a task is ready to execute.
        
        A task is ready if all its dependencies have been completed.
        """
        blockers = self.get_blockers(task_id)
        return len(blockers) == 0
    
    def validate_ready(self, task_id: str) -> tuple[bool, Optional[str]]:
        """
        Validate if a task is ready and return detailed status.
        
        Returns:
            Tuple of (is_ready, error_message)
        """
        if task_id not in self.tasks:
            return False, f"Task {task_id} not found"
        
        blockers = self.get_blockers(task_id)
        
        if blockers:
            blocker_names = [f"{t.id}({t.status.value})" for t in blockers]
            return False, f"Blocked by: {', '.join(blocker_names)}"
        
        return True, None
    
    def mark_completed(self, task_id: str) -> None:
        """Mark a task as completed."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
    
    def mark_failed(self, task_id: str) -> None:
        """Mark a task as failed."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.FAILED
    
    def update_task_status(self, task_id: str, status: TaskStatus) -> None:
        """Update task status."""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
    
    def get_ready_tasks(self) -> List[Task]:
        """Get all tasks that are ready to execute."""
        ready_tasks = []
        
        for task_id, task in self.tasks.items():
            if task.status == TaskStatus.PENDING and self.is_ready(task_id):
                ready_tasks.append(task)
        
        # Sort by priority (lower number = higher priority)
        ready_tasks.sort(key=lambda t: t.priority)
        
        return ready_tasks
    
    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """Get the full dependency graph."""
        graph = {}
        for task_id, blockers in self.dependencies.items():
            graph[task_id] = list(blockers)
        
        return graph
    
    def _would_create_cycle(self, from_task: str, to_task: str) -> bool:
        """Check if adding an edge would create a cycle."""
        # DFS to check if to_task can reach from_task
        visited = set()
        
        def can_reach(current: str, target: str) -> bool:
            if current == target:
                return True
            
            if current in visited:
                return False
            
            visited.add(current)
            
            for dependent in self.dependents.get(current, set()):
                if can_reach(dependent, target):
                    return True
            
            return False
        
        return can_reach(to_task, from_task)
