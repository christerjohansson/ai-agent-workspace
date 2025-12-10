"""
Phase 3: Example Multi-Agent Workflows
======================================

Demonstrates real-world scenarios where agents collaborate using the framework.
Shows how to integrate messaging, dependencies, context, conflict resolution,
and auditing into practical workflows.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

from src.collaboration.protocol import Message, MessageType, ProtocolValidator
from src.collaboration.message_queue import MessageBus
from src.collaboration.dependency_tracker import DependencyTracker, Task, TaskStatus
from src.collaboration.context_manager import (
    ContextManager, ContextType, AccessLevel
)
from src.collaboration.conflict_resolver import (
    ConflictResolver, ConflictType, ConflictOption, ResolutionStrategy
)
from src.collaboration.audit_logger import AuditLogger, AuditEventType


@dataclass
class AgentRole:
    """Base class for agent roles."""
    name: str
    role_type: str
    
    def __init__(self, name: str, role_type: str):
        self.name = name
        self.role_type = role_type


class ProductOwnerAgent(AgentRole):
    """Manages product roadmap and priorities."""
    
    def __init__(self, name: str = "ProductOwner"):
        super().__init__(name, "ProductOwner")


class DeveloperAgent(AgentRole):
    """Implements features and manages technical tasks."""
    
    def __init__(self, name: str = "Developer"):
        super().__init__(name, "Developer")


class CodeReviewerAgent(AgentRole):
    """Reviews code and ensures quality standards."""
    
    def __init__(self, name: str = "CodeReviewer"):
        super().__init__(name, "CodeReviewer")


class DesignerAgent(AgentRole):
    """Handles UI/UX design and component design."""
    
    def __init__(self, name: str = "Designer"):
        super().__init__(name, "Designer")


class DevOpsAgent(AgentRole):
    """Manages deployment and infrastructure."""
    
    def __init__(self, name: str = "DevOps"):
        super().__init__(name, "DevOps")


class ProjectLeaderAgent(AgentRole):
    """Coordinates team and manages timeline."""
    
    def __init__(self, name: str = "ProjectLeader"):
        super().__init__(name, "ProjectLeader")


class WorkflowCoordinator:
    """
    Coordinates multi-agent workflows using the collaboration framework.
    Manages message passing, dependency tracking, and conflict resolution.
    """
    
    def __init__(self, use_message_queue: bool = False):
        """
        Initialize workflow coordinator.
        
        Args:
            use_message_queue: Whether to use message queue (Redis/RabbitMQ)
        """
        self.message_bus = MessageBus("memory") if not use_message_queue else MessageBus("redis")
        self.dependency_tracker = DependencyTracker()
        self.context_manager = ContextManager()
        self.conflict_resolver = ConflictResolver()
        self.audit_logger = AuditLogger()
        self.agents: Dict[str, AgentRole] = {}
    
    def register_agent(self, agent: AgentRole) -> None:
        """Register an agent with the workflow."""
        self.agents[agent.name] = agent
        self.audit_logger.log_event(
            event_type=AuditEventType.WORKFLOW_STARTED,
            agent=agent.name,
            subject=f"{agent.role_type}_registered",
            action=f"Registered {agent.role_type} agent"
        )
    
    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        msg_type: MessageType,
        subject: str,
        data: Dict = None
    ) -> Message:
        """Send a message between agents."""
        message = Message(
            from_agent=from_agent,
            to_agent=to_agent,
            msg_type=msg_type,
            subject=subject,
            data=data or {}
        )
        
        # Validate message
        validator = ProtocolValidator()
        if not validator.validate_message(message):
            raise ValueError(f"Invalid message: {message}")
        
        # Send via message bus
        self.message_bus.send_message(message)
        
        # Audit
        self.audit_logger.log_message_sent(
            from_agent,
            to_agent,
            msg_type.value,
            subject
        )
        
        return message


# =============================================================================
# EXAMPLE 1: Roadmap Planning Workflow
# =============================================================================

class RoadmapPlanningWorkflow:
    """
    Scenario: ProjectLeader coordinates with ProductOwner on Q1 roadmap.
    
    Flow:
    1. ProductOwner creates initial roadmap context
    2. ProjectLeader requests roadmap via message
    3. Context is shared and ProductOwner provides feedback
    4. Potential conflict on priorities is resolved
    """
    
    def __init__(self, coordinator: WorkflowCoordinator):
        self.coordinator = coordinator
    
    def execute(self):
        """Execute the roadmap planning workflow."""
        
        # Step 1: ProductOwner creates roadmap context
        roadmap = self.coordinator.context_manager.create_context(
            context_id="q1-roadmap",
            context_type=ContextType.PROJECT,
            owner="ProductOwner",
            data={
                "quarter": "Q1",
                "features": [
                    {"name": "Auth System", "priority": "High"},
                    {"name": "Dashboard", "priority": "Medium"},
                    {"name": "Analytics", "priority": "Low"}
                ],
                "timeline": "12 weeks"
            },
            access_level=AccessLevel.TEAM
        )
        
        # Audit context creation
        self.coordinator.audit_logger.log_context_created(
            "ProductOwner",
            "q1-roadmap",
            "roadmap"
        )
        
        # Step 2: ProjectLeader requests roadmap
        msg = self.coordinator.send_message(
            from_agent="ProjectLeader",
            to_agent="ProductOwner",
            msg_type=MessageType.CONTEXT_SHARE,
            subject="Request Q1 Roadmap",
            data={"context": "q1-roadmap"}
        )
        
        # Step 3: ProductOwner shares roadmap with team
        self.coordinator.context_manager.share_context(
            "q1-roadmap",
            ["ProjectLeader", "Developer", "Designer", "DevOps"]
        )
        
        self.coordinator.audit_logger.log_context_shared(
            "ProductOwner",
            "q1-roadmap",
            ["ProjectLeader", "Developer", "Designer", "DevOps"]
        )
        
        # Step 4: Simulate priority conflict
        options = [
            ConflictOption(
                option_id="prioritize-auth",
                proposed_by="Developer",
                description="Auth first",
                rationale="Blocks other work"
            ),
            ConflictOption(
                option_id="prioritize-dashboard",
                proposed_by="ProductOwner",
                description="Dashboard first",
                rationale="Customer visibility"
            )
        ]
        
        conflict = self.coordinator.conflict_resolver.create_conflict(
            conflict_id="q1-priority-conflict",
            conflict_type=ConflictType.PRIORITY_CONFLICT,
            agents_involved=["Developer", "ProductOwner", "ProjectLeader"],
            topic="Q1 feature priorities",
            options=options
        )
        
        # Vote
        conflict.vote("Developer", "prioritize-auth")
        conflict.vote("ProductOwner", "prioritize-dashboard")
        conflict.vote("ProjectLeader", "prioritize-auth")
        
        # Resolve by majority
        resolution = self.coordinator.conflict_resolver.resolve(
            "q1-priority-conflict",
            ResolutionStrategy.MAJORITY_VOTE
        )
        
        self.coordinator.audit_logger.log_conflict_resolved(
            "ProjectLeader",
            "q1-priority-conflict",
            resolution,
            "majority_vote"
        )
        
        return {
            "roadmap_context": roadmap,
            "priority_resolution": resolution,
            "sharing_message": msg
        }


# =============================================================================
# EXAMPLE 2: Feature Development & Code Review Handoff
# =============================================================================

class FeatureDevelopmentWorkflow:
    """
    Scenario: Developer implements feature, Designer reviews design,
    CodeReviewer ensures quality, DevOps prepares deployment.
    
    Flow:
    1. Developer creates task and marks dependencies
    2. Designer provides UI components
    3. Developer marks design review dependency as complete
    4. Developer works on implementation
    5. CodeReviewer reviews code
    6. DevOps prepares deployment
    """
    
    def __init__(self, coordinator: WorkflowCoordinator):
        self.coordinator = coordinator
    
    def execute(self):
        """Execute the feature development workflow."""
        
        # Step 1: Create tasks with dependencies
        designer_task = self.coordinator.dependency_tracker.add_task(
            "design-task",
            "Create UI components",
            "Designer",
            priority=1
        )
        
        dev_task = self.coordinator.dependency_tracker.add_task(
            "dev-task",
            "Implement feature",
            "Developer",
            priority=2
        )
        
        review_task = self.coordinator.dependency_tracker.add_task(
            "review-task",
            "Review code",
            "CodeReviewer",
            priority=3
        )
        
        deploy_task = self.coordinator.dependency_tracker.add_task(
            "deploy-task",
            "Deploy to production",
            "DevOps",
            priority=4
        )
        
        # Define dependencies
        self.coordinator.dependency_tracker.add_dependency(dev_task, designer_task)
        self.coordinator.dependency_tracker.add_dependency(review_task, dev_task)
        self.coordinator.dependency_tracker.add_dependency(deploy_task, review_task)
        
        # Audit task creation
        self.coordinator.audit_logger.log_event(
            AuditEventType.TASK_CREATED,
            "Developer",
            "dev-task",
            "Created feature development task"
        )
        
        # Step 2: Designer creates UI components context
        design_context = self.coordinator.context_manager.create_context(
            context_id="feature-ui-design",
            context_type=ContextType.TASK,
            owner="Designer",
            data={
                "components": ["Button", "Form", "Modal"],
                "design_spec": "Material Design v3",
                "status": "complete"
            },
            access_level=AccessLevel.TEAM
        )
        
        # Step 3: Designer completes task
        self.coordinator.dependency_tracker.mark_completed(designer_task)
        self.coordinator.audit_logger.log_task_completed(
            "Designer",
            "design-task",
            {"status": "complete"}
        )
        
        # Step 4: Developer starts implementation
        self.coordinator.dependency_tracker.mark_in_progress(dev_task)
        
        # Check ready state
        ready_tasks = self.coordinator.dependency_tracker.get_ready_tasks()
        
        # Developer creates implementation context
        impl_context = self.coordinator.context_manager.create_context(
            context_id="feature-implementation",
            context_type=ContextType.TASK,
            owner="Developer",
            data={
                "branch": "feature/new-component",
                "status": "in-progress",
                "design_ref": "feature-ui-design"
            },
            access_level=AccessLevel.TEAM,
            tags={"feature", "active"}
        )
        
        # Share with reviewer
        self.coordinator.context_manager.share_context(
            "feature-implementation",
            ["CodeReviewer", "Designer"]
        )
        
        # Step 5: Developer completes and requests review
        self.coordinator.dependency_tracker.mark_completed(dev_task)
        
        review_msg = self.coordinator.send_message(
            from_agent="Developer",
            to_agent="CodeReviewer",
            msg_type=MessageType.TASK_REQUEST,
            subject="Review implementation",
            data={
                "context": "feature-implementation",
                "branch": "feature/new-component"
            }
        )
        
        # Step 6: CodeReviewer completes review
        self.coordinator.dependency_tracker.mark_completed(review_task)
        
        self.coordinator.send_message(
            from_agent="CodeReviewer",
            to_agent="DevOps",
            msg_type=MessageType.TASK_COMPLETE,
            subject="Code review passed",
            data={"approved": True, "branch": "feature/new-component"}
        )
        
        # Step 7: DevOps prepares deployment
        self.coordinator.dependency_tracker.mark_in_progress(deploy_task)
        
        deploy_context = self.coordinator.context_manager.create_context(
            context_id="deployment-config",
            context_type=ContextType.TASK,
            owner="DevOps",
            data={
                "environment": "production",
                "branch": "feature/new-component",
                "strategy": "canary",
                "status": "scheduled"
            },
            access_level=AccessLevel.TEAM
        )
        
        self.coordinator.dependency_tracker.mark_completed(deploy_task)
        
        return {
            "tasks": [designer_task, dev_task, review_task, deploy_task],
            "contexts": [design_context, impl_context, deploy_context],
            "workflow_message": review_msg
        }


# =============================================================================
# EXAMPLE 3: Design Decision Conflict Resolution
# =============================================================================

class DesignConflictResolutionWorkflow:
    """
    Scenario: Developer and Designer disagree on component implementation.
    Uses conflict resolution to reach agreement.
    
    Flow:
    1. Designer proposes component design
    2. Developer proposes alternative approach
    3. Both are shared as context
    4. Conflict is created with options
    5. Team votes and resolves
    """
    
    def __init__(self, coordinator: WorkflowCoordinator):
        self.coordinator = coordinator
    
    def execute(self):
        """Execute the design conflict resolution workflow."""
        
        # Step 1: Designer proposes design
        design_context = self.coordinator.context_manager.create_context(
            context_id="form-component-design",
            context_type=ContextType.DECISION,
            owner="Designer",
            data={
                "component": "FormInput",
                "approach": "Controlled component",
                "state_management": "React hooks",
                "validation": "Real-time"
            },
            access_level=AccessLevel.TEAM,
            tags={"design", "form"}
        )
        
        # Step 2: Developer proposes alternative
        self.coordinator.send_message(
            from_agent="Developer",
            to_agent="Designer",
            msg_type=MessageType.REQUEST_FEEDBACK,
            subject="Alternative form component approach",
            data={
                "approach": "Uncontrolled component",
                "rationale": "Better performance"
            }
        )
        
        # Step 3: Create decision context
        decision_context = self.coordinator.context_manager.create_context(
            context_id="form-component-decision",
            context_type=ContextType.DECISION,
            owner="Designer",
            data={
                "options": ["controlled", "uncontrolled"],
                "pros_cons": {
                    "controlled": {
                        "pros": ["Full control", "Validation", "State visibility"],
                        "cons": ["More boilerplate", "Performance overhead"]
                    },
                    "uncontrolled": {
                        "pros": ["Simpler", "Better performance"],
                        "cons": ["Less validation", "State management unclear"]
                    }
                }
            },
            access_level=AccessLevel.TEAM
        )
        
        # Share context with team
        self.coordinator.context_manager.share_context(
            "form-component-decision",
            ["Developer", "CodeReviewer", "ProjectLeader"]
        )
        
        # Step 4: Create conflict with options
        options = [
            ConflictOption(
                option_id="controlled-component",
                proposed_by="Designer",
                description="Controlled component with React hooks",
                rationale="Full control over form state and validation",
                pros=["Full validation", "Predictable state"],
                cons=["More code", "Performance overhead"]
            ),
            ConflictOption(
                option_id="uncontrolled-component",
                proposed_by="Developer",
                description="Uncontrolled component with DOM refs",
                rationale="Simpler implementation with better performance",
                pros=["Less boilerplate", "Better performance"],
                cons=["Limited validation", "State not visible"]
            )
        ]
        
        conflict = self.coordinator.conflict_resolver.create_conflict(
            conflict_id="form-component-design-conflict",
            conflict_type=ConflictType.DESIGN_CONFLICT,
            agents_involved=["Designer", "Developer", "CodeReviewer"],
            topic="Form component implementation approach",
            options=options
        )
        
        self.coordinator.audit_logger.log_event(
            AuditEventType.CONFLICT_CREATED,
            "Designer",
            "form-component-design-conflict",
            "Design conflict: component approach"
        )
        
        # Step 5: Team votes
        conflict.vote("Designer", "controlled-component")
        conflict.vote("Developer", "uncontrolled-component")
        conflict.vote("CodeReviewer", "controlled-component")
        
        # Step 6: Resolve by majority
        resolution = self.coordinator.conflict_resolver.resolve(
            "form-component-design-conflict",
            ResolutionStrategy.MAJORITY_VOTE
        )
        
        self.coordinator.audit_logger.log_conflict_resolved(
            "Designer",
            "form-component-design-conflict",
            resolution,
            "majority_vote"
        )
        
        # Update decision context with resolution
        self.coordinator.context_manager.update_context(
            "form-component-decision",
            "Designer",
            {"resolution": resolution, "resolved_at": datetime.utcnow().isoformat()}
        )
        
        # Notify all agents
        self.coordinator.send_message(
            from_agent="Designer",
            to_agent="Developer",
            msg_type=MessageType.TASK_UPDATE,
            subject="Form component design decision",
            data={"resolution": resolution, "approach": resolution}
        )
        
        return {
            "conflict": conflict,
            "resolution": resolution,
            "contexts": [design_context, decision_context]
        }


# =============================================================================
# Example Usage
# =============================================================================

def demonstrate_workflows():
    """Demonstrate all example workflows."""
    
    # Initialize coordinator
    coordinator = WorkflowCoordinator(use_message_queue=False)
    
    # Register agents
    coordinator.register_agent(ProductOwnerAgent())
    coordinator.register_agent(DeveloperAgent())
    coordinator.register_agent(CodeReviewerAgent())
    coordinator.register_agent(DesignerAgent())
    coordinator.register_agent(DevOpsAgent())
    coordinator.register_agent(ProjectLeaderAgent())
    
    print("=" * 80)
    print("MULTI-AGENT WORKFLOW EXAMPLES")
    print("=" * 80)
    
    # Example 1: Roadmap Planning
    print("\n[Example 1] Roadmap Planning Workflow")
    print("-" * 80)
    roadmap_workflow = RoadmapPlanningWorkflow(coordinator)
    roadmap_result = roadmap_workflow.execute()
    print(f"✓ Roadmap created: {roadmap_result['roadmap_context'].metadata.context_id}")
    print(f"✓ Priority conflict resolved: {roadmap_result['priority_resolution']}")
    
    # Example 2: Feature Development
    print("\n[Example 2] Feature Development & Handoff Workflow")
    print("-" * 80)
    dev_workflow = FeatureDevelopmentWorkflow(coordinator)
    dev_result = dev_workflow.execute()
    print(f"✓ Created {len(dev_result['tasks'])} interdependent tasks")
    print(f"✓ Created {len(dev_result['contexts'])} shared contexts")
    print(f"✓ HandOff message: {dev_result['workflow_message'].subject}")
    
    # Example 3: Design Conflict
    print("\n[Example 3] Design Conflict Resolution Workflow")
    print("-" * 80)
    design_workflow = DesignConflictResolutionWorkflow(coordinator)
    design_result = design_workflow.execute()
    print(f"✓ Conflict created: {design_result['conflict'].conflict_id}")
    print(f"✓ Resolution: {design_result['resolution']}")
    
    # Show audit trail
    print("\n" + "=" * 80)
    print("AUDIT TRAIL")
    print("=" * 80)
    report = coordinator.audit_logger.generate_report("form-component-decision")
    print(f"Subject: form-component-decision")
    print(f"Total events: {report['total_events']}")
    print(f"Agents involved: {', '.join(report['agents_involved'])}")
    
    print("\n" + "=" * 80)
    print("✓ All workflows completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_workflows()
