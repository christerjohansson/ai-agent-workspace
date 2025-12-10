"""
Conflict Resolver

Handles conflicts in agent decisions using various strategies.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from enum import Enum


class ConflictType(Enum):
    """Types of conflicts that can occur."""
    
    RESOURCE_CONFLICT = "resource_conflict"      # Competing for same resource
    DECISION_CONFLICT = "decision_conflict"      # Different opinions on decision
    PRIORITY_CONFLICT = "priority_conflict"      # Different priorities
    SCHEDULE_CONFLICT = "schedule_conflict"      # Conflicting timelines
    DESIGN_CONFLICT = "design_conflict"          # Different design approaches
    PROCESS_CONFLICT = "process_conflict"        # Different process preferences


class ResolutionStrategy(Enum):
    """Strategies for resolving conflicts."""
    
    MAJORITY_VOTE = "majority_vote"              # Decide by vote
    PRIORITY_BASED = "priority_based"            # Based on agent priority/role
    ESCALATE = "escalate"                        # Escalate to human
    CONSENSUS = "consensus"                      # Require agreement
    TIME_BASED = "time_based"                    # First come, first served
    RANDOM = "random"                            # Random selection
    WEIGHTED_VOTE = "weighted_vote"              # Vote weighted by role


class ConflictStatus(Enum):
    """Status of a conflict."""
    
    OPEN = "open"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    ABANDONED = "abandoned"


@dataclass
class ConflictOption:
    """An option in a conflict."""
    
    option_id: str
    proposed_by: str                 # Agent that proposed this option
    description: str
    rationale: str
    data: Dict[str, Any] = field(default_factory=dict)
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    votes: List[str] = field(default_factory=list)  # Agents who voted for this
    
    def get_vote_count(self) -> int:
        """Get number of votes for this option."""
        return len(self.votes)


@dataclass
class Conflict:
    """
    Represents a conflict between agents.
    
    Attributes:
        conflict_id: Unique identifier
        conflict_type: Type of conflict
        agents_involved: List of agent names in conflict
        topic: Topic of conflict
        options: Dict of option_id -> ConflictOption
        status: Current status
        created_at: When conflict was created
        resolved_at: When conflict was resolved
        resolution: Final resolution if resolved
        escalation_reason: If escalated, why?
    """
    
    conflict_id: str
    conflict_type: ConflictType
    agents_involved: List[str]
    topic: str
    options: Dict[str, ConflictOption] = field(default_factory=dict)
    status: ConflictStatus = ConflictStatus.OPEN
    created_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    resolution: Optional[str] = None                    # Selected option ID
    escalation_reason: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)  # Additional context
    
    def add_option(self, option: ConflictOption) -> None:
        """Add an option to the conflict."""
        self.options[option.option_id] = option
    
    def vote(self, agent_name: str, option_id: str) -> bool:
        """Record a vote for an option."""
        if option_id not in self.options:
            return False
        
        if agent_name not in self.options[option_id].votes:
            self.options[option_id].votes.append(agent_name)
        
        return True
    
    def get_winning_option(self) -> Optional[str]:
        """Get the option with most votes."""
        if not self.options:
            return None
        
        return max(
            self.options.items(),
            key=lambda x: x[1].get_vote_count()
        )[0]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['conflict_type'] = self.conflict_type.value
        data['status'] = self.status.value
        data['created_at'] = self.created_at.isoformat()
        if self.resolved_at:
            data['resolved_at'] = self.resolved_at.isoformat()
        return data


class ConflictResolver:
    """
    Resolves conflicts between agents using various strategies.
    
    Supports multiple resolution strategies and can escalate to humans.
    """
    
    def __init__(self):
        """Initialize conflict resolver."""
        self.conflicts: Dict[str, Conflict] = {}
        self.resolution_history: List[Dict[str, Any]] = []
        self.escalation_handler: Optional[Callable] = None
    
    def create_conflict(
        self,
        conflict_id: str,
        conflict_type: ConflictType,
        agents_involved: List[str],
        topic: str,
        options: List[ConflictOption],
        context: Optional[Dict[str, Any]] = None
    ) -> Conflict:
        """
        Create a new conflict.
        
        Args:
            conflict_id: Unique identifier
            conflict_type: Type of conflict
            agents_involved: Agents involved in conflict
            topic: Topic of conflict
            options: Available options for resolution
            context: Additional context
        
        Returns:
            Created Conflict object
        """
        conflict = Conflict(
            conflict_id=conflict_id,
            conflict_type=conflict_type,
            agents_involved=agents_involved,
            topic=topic,
            context=context or {}
        )
        
        for option in options:
            conflict.add_option(option)
        
        self.conflicts[conflict_id] = conflict
        return conflict
    
    def resolve(
        self,
        conflict_id: str,
        strategy: ResolutionStrategy = ResolutionStrategy.MAJORITY_VOTE
    ) -> Optional[str]:
        """
        Resolve a conflict using specified strategy.
        
        Args:
            conflict_id: Conflict identifier
            strategy: Resolution strategy to use
        
        Returns:
            Selected option ID if resolved, None if escalated
        """
        if conflict_id not in self.conflicts:
            return None
        
        conflict = self.conflicts[conflict_id]
        
        if strategy == ResolutionStrategy.MAJORITY_VOTE:
            result = self._resolve_by_majority(conflict)
        elif strategy == ResolutionStrategy.PRIORITY_BASED:
            result = self._resolve_by_priority(conflict)
        elif strategy == ResolutionStrategy.CONSENSUS:
            result = self._resolve_by_consensus(conflict)
        elif strategy == ResolutionStrategy.TIME_BASED:
            result = self._resolve_by_time(conflict)
        elif strategy == ResolutionStrategy.WEIGHTED_VOTE:
            result = self._resolve_by_weighted_vote(conflict)
        elif strategy == ResolutionStrategy.RANDOM:
            result = self._resolve_by_random(conflict)
        else:
            result = None
        
        if result:
            conflict.resolution = result
            conflict.status = ConflictStatus.RESOLVED
            conflict.resolved_at = datetime.utcnow()
            self._record_resolution(conflict, strategy, result)
            return result
        
        return None
    
    def escalate_conflict(
        self,
        conflict_id: str,
        reason: str = "Unable to resolve automatically"
    ) -> bool:
        """
        Escalate conflict to human decision maker.
        
        Args:
            conflict_id: Conflict identifier
            reason: Reason for escalation
        
        Returns:
            True if escalated, False otherwise
        """
        if conflict_id not in self.conflicts:
            return False
        
        conflict = self.conflicts[conflict_id]
        conflict.status = ConflictStatus.ESCALATED
        conflict.escalation_reason = reason
        
        # Call escalation handler if configured
        if self.escalation_handler:
            self.escalation_handler(conflict)
        
        return True
    
    def set_escalation_handler(self, handler: Callable) -> None:
        """Set handler for escalated conflicts."""
        self.escalation_handler = handler
    
    def suggest_resolution(
        self,
        conflict_id: str
    ) -> Dict[str, Any]:
        """
        Suggest a resolution for a conflict.
        
        Returns detailed analysis and recommendation.
        """
        if conflict_id not in self.conflicts:
            return {}
        
        conflict = self.conflicts[conflict_id]
        
        suggestions = {
            "conflict_id": conflict_id,
            "topic": conflict.topic,
            "options": {},
            "recommendation": None,
            "reasoning": []
        }
        
        # Analyze each option
        for option_id, option in conflict.options.items():
            suggestions["options"][option_id] = {
                "description": option.description,
                "proposed_by": option.proposed_by,
                "votes": option.get_vote_count(),
                "pros": option.pros,
                "cons": option.cons
            }
        
        # Get winning option
        winning = conflict.get_winning_option()
        if winning:
            suggestions["recommendation"] = winning
            suggestions["reasoning"].append(
                f"Option '{winning}' has most support ({conflict.options[winning].get_vote_count()} votes)"
            )
        
        return suggestions
    
    def get_conflict_status(self, conflict_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a conflict."""
        if conflict_id not in self.conflicts:
            return None
        
        conflict = self.conflicts[conflict_id]
        
        return {
            "conflict_id": conflict_id,
            "status": conflict.status.value,
            "topic": conflict.topic,
            "agents": conflict.agents_involved,
            "options_count": len(conflict.options),
            "votes_per_option": {
                oid: opt.get_vote_count()
                for oid, opt in conflict.options.items()
            },
            "resolution": conflict.resolution,
            "created_at": conflict.created_at.isoformat()
        }
    
    def get_resolution_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get history of resolved conflicts."""
        return self.resolution_history[-limit:]
    
    # Resolution strategy implementations
    
    def _resolve_by_majority(self, conflict: Conflict) -> Optional[str]:
        """Resolve by majority vote."""
        if not conflict.options:
            return None
        
        return conflict.get_winning_option()
    
    def _resolve_by_priority(self, conflict: Conflict) -> Optional[str]:
        """Resolve based on proposer priority."""
        # This would require role information
        # For now, prioritize by proposal order
        for option_id in conflict.options.keys():
            return option_id
        return None
    
    def _resolve_by_consensus(self, conflict: Conflict) -> Optional[str]:
        """Resolve by consensus (all agents must agree)."""
        # Check if any option has all agents voting for it
        for option in conflict.options.values():
            if len(option.votes) == len(conflict.agents_involved):
                return option.option_id
        
        return None
    
    def _resolve_by_time(self, conflict: Conflict) -> Optional[str]:
        """Resolve by first option proposed."""
        if conflict.options:
            return next(iter(conflict.options.keys()))
        return None
    
    def _resolve_by_weighted_vote(self, conflict: Conflict) -> Optional[str]:
        """Resolve by weighted votes (would require role info)."""
        # Simplified: same as majority for now
        return self._resolve_by_majority(conflict)
    
    def _resolve_by_random(self, conflict: Conflict) -> Optional[str]:
        """Resolve by random selection."""
        import random
        if conflict.options:
            return random.choice(list(conflict.options.keys()))
        return None
    
    def _record_resolution(
        self,
        conflict: Conflict,
        strategy: ResolutionStrategy,
        resolution: str
    ) -> None:
        """Record resolution in history."""
        record = {
            "conflict_id": conflict.conflict_id,
            "topic": conflict.topic,
            "strategy": strategy.value,
            "resolution": resolution,
            "agents": conflict.agents_involved,
            "resolved_at": datetime.utcnow().isoformat()
        }
        self.resolution_history.append(record)
