"""
Context Manager

Manages shared context and state between agents.
Provides mechanisms for context propagation, sharing, and synchronization.
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional, List, Set
from datetime import datetime, timedelta
import json
from enum import Enum


class ContextType(Enum):
    """Types of context that can be shared."""
    
    PROJECT = "project"          # Project-level context
    SPRINT = "sprint"            # Sprint-level context
    TASK = "task"                # Task-level context
    DECISION = "decision"        # Decision/discussion context
    KNOWLEDGE = "knowledge"      # General knowledge base
    WORKFLOW = "workflow"        # Workflow state


class AccessLevel(Enum):
    """Access control levels for context."""
    
    PUBLIC = "public"            # Accessible to all agents
    TEAM = "team"                # Accessible to team members
    ROLE = "role"                # Accessible to specific roles
    PRIVATE = "private"          # Only accessible to owner


@dataclass
class ContextMetadata:
    """Metadata about a piece of context."""
    
    context_id: str
    context_type: ContextType
    owner: str                    # Agent that created this context
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    access_level: AccessLevel = AccessLevel.TEAM
    tags: Set[str] = field(default_factory=set)
    version: int = 1
    ttl: Optional[int] = None     # Time to live in seconds
    related_contexts: List[str] = field(default_factory=list)  # Related context IDs
    
    def is_expired(self) -> bool:
        """Check if context has expired."""
        if self.ttl is None:
            return False
        elapsed = (datetime.utcnow() - self.created_at).total_seconds()
        return elapsed > self.ttl
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['context_type'] = self.context_type.value
        data['access_level'] = self.access_level.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data


@dataclass
class Context:
    """
    Represents shared context between agents.
    
    Attributes:
        metadata: Context metadata
        data: The actual context data
        access_permissions: Dict of agent_name -> can_access
    """
    
    metadata: ContextMetadata
    data: Dict[str, Any]
    access_permissions: Dict[str, bool] = field(default_factory=dict)
    
    def has_access(self, agent_name: str) -> bool:
        """Check if an agent has access to this context."""
        # Check explicit permissions
        if agent_name in self.access_permissions:
            return self.access_permissions[agent_name]
        
        # Check access level
        if self.metadata.access_level == AccessLevel.PUBLIC:
            return True
        
        if self.metadata.access_level == AccessLevel.PRIVATE:
            return agent_name == self.metadata.owner
        
        # TEAM and ROLE require explicit permissions or similar role
        return False
    
    def grant_access(self, agent_name: str) -> None:
        """Grant access to an agent."""
        self.access_permissions[agent_name] = True
    
    def revoke_access(self, agent_name: str) -> None:
        """Revoke access from an agent."""
        self.access_permissions[agent_name] = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'metadata': self.metadata.to_dict(),
            'data': self.data,
            'access_permissions': self.access_permissions
        }


class ContextManager:
    """
    Manages shared context between agents.
    
    Provides:
    - Context creation and storage
    - Context sharing and propagation
    - Access control
    - Version tracking
    - Context lifecycle management
    """
    
    def __init__(self, persistence_enabled: bool = True):
        """
        Initialize context manager.
        
        Args:
            persistence_enabled: Whether to persist context to storage
        """
        self.contexts: Dict[str, Context] = {}
        self.persistence_enabled = persistence_enabled
        self.context_history: Dict[str, List[Context]] = {}  # Track versions
        self.subscriptions: Dict[str, Set[str]] = {}  # context_id -> subscribed agents
    
    def create_context(
        self,
        context_id: str,
        context_type: ContextType,
        owner: str,
        data: Dict[str, Any],
        access_level: AccessLevel = AccessLevel.TEAM,
        tags: Set[str] = None,
        ttl: Optional[int] = None
    ) -> Context:
        """
        Create a new context.
        
        Args:
            context_id: Unique identifier for context
            context_type: Type of context
            owner: Agent that owns this context
            data: Context data
            access_level: Access control level
            tags: Optional tags for categorization
            ttl: Optional time to live in seconds
        
        Returns:
            Created Context object
        """
        if context_id in self.contexts:
            raise ValueError(f"Context {context_id} already exists")
        
        metadata = ContextMetadata(
            context_id=context_id,
            context_type=context_type,
            owner=owner,
            access_level=access_level,
            tags=tags or set(),
            ttl=ttl
        )
        
        context = Context(metadata=metadata, data=data)
        self.contexts[context_id] = context
        self.context_history[context_id] = [context]
        
        return context
    
    def get_context(self, context_id: str, agent_name: str) -> Optional[Context]:
        """
        Get context if agent has access.
        
        Args:
            context_id: Context identifier
            agent_name: Agent requesting access
        
        Returns:
            Context if accessible, None otherwise
        """
        if context_id not in self.contexts:
            return None
        
        context = self.contexts[context_id]
        
        # Check expiration
        if context.metadata.is_expired():
            self.delete_context(context_id)
            return None
        
        # Check access
        if not context.has_access(agent_name):
            return None
        
        return context
    
    def update_context(
        self,
        context_id: str,
        agent_name: str,
        new_data: Dict[str, Any]
    ) -> bool:
        """
        Update context data.
        
        Args:
            context_id: Context identifier
            agent_name: Agent performing update
            new_data: New data to merge
        
        Returns:
            True if successful, False otherwise
        """
        if context_id not in self.contexts:
            return False
        
        context = self.contexts[context_id]
        
        # Only owner or agents with write permission can update
        if agent_name != context.metadata.owner:
            return False
        
        # Store old version
        if context_id not in self.context_history:
            self.context_history[context_id] = []
        
        # Create versioned copy
        old_context = Context(
            metadata=context.metadata,
            data=context.data.copy(),
            access_permissions=context.access_permissions.copy()
        )
        self.context_history[context_id].append(old_context)
        
        # Update data and metadata
        context.data.update(new_data)
        context.metadata.updated_at = datetime.utcnow()
        context.metadata.version += 1
        
        # Notify subscribed agents
        self._notify_subscribers(context_id, agent_name)
        
        return True
    
    def share_context(
        self,
        context_id: str,
        agent_names: List[str],
        access_level: str = "read"
    ) -> bool:
        """
        Share context with other agents.
        
        Args:
            context_id: Context identifier
            agent_names: List of agent names to share with
            access_level: "read" or "write"
        
        Returns:
            True if successful, False otherwise
        """
        if context_id not in self.contexts:
            return False
        
        context = self.contexts[context_id]
        
        for agent_name in agent_names:
            context.grant_access(agent_name)
            self._subscribe_agent(context_id, agent_name)
        
        return True
    
    def subscribe(self, context_id: str, agent_name: str) -> bool:
        """
        Subscribe agent to context updates.
        
        Args:
            context_id: Context identifier
            agent_name: Agent name
        
        Returns:
            True if successful, False otherwise
        """
        if context_id not in self.contexts:
            return False
        
        return self._subscribe_agent(context_id, agent_name)
    
    def unsubscribe(self, context_id: str, agent_name: str) -> bool:
        """Unsubscribe agent from context updates."""
        if context_id not in self.subscriptions:
            return False
        
        self.subscriptions[context_id].discard(agent_name)
        return True
    
    def get_subscribed_agents(self, context_id: str) -> List[str]:
        """Get list of agents subscribed to context."""
        return list(self.subscriptions.get(context_id, set()))
    
    def find_contexts(
        self,
        agent_name: str,
        context_type: Optional[ContextType] = None,
        tags: Optional[Set[str]] = None
    ) -> List[Context]:
        """
        Find contexts accessible to an agent.
        
        Args:
            agent_name: Agent name
            context_type: Optional type filter
            tags: Optional tags filter (any match)
        
        Returns:
            List of accessible contexts
        """
        results = []
        
        for context in self.contexts.values():
            # Check access
            if not context.has_access(agent_name):
                continue
            
            # Check type
            if context_type and context.metadata.context_type != context_type:
                continue
            
            # Check tags
            if tags and not context.metadata.tags.intersection(tags):
                continue
            
            # Check expiration
            if context.metadata.is_expired():
                continue
            
            results.append(context)
        
        return results
    
    def get_context_history(self, context_id: str, limit: int = 10) -> List[Context]:
        """Get version history of a context."""
        history = self.context_history.get(context_id, [])
        return history[-limit:]
    
    def link_contexts(self, context_id1: str, context_id2: str) -> bool:
        """Link two contexts as related."""
        if context_id1 not in self.contexts or context_id2 not in self.contexts:
            return False
        
        self.contexts[context_id1].metadata.related_contexts.append(context_id2)
        self.contexts[context_id2].metadata.related_contexts.append(context_id1)
        
        return True
    
    def get_related_contexts(self, context_id: str, depth: int = 1) -> List[Context]:
        """Get contexts related to the given context."""
        if context_id not in self.contexts:
            return []
        
        related = []
        visited = {context_id}
        queue = [(self.contexts[context_id], 0)]
        
        while queue:
            current, current_depth = queue.pop(0)
            
            if current_depth >= depth:
                continue
            
            for related_id in current.metadata.related_contexts:
                if related_id not in visited:
                    visited.add(related_id)
                    if related_id in self.contexts:
                        related_context = self.contexts[related_id]
                        related.append(related_context)
                        queue.append((related_context, current_depth + 1))
        
        return related
    
    def delete_context(self, context_id: str) -> bool:
        """Delete a context."""
        if context_id in self.contexts:
            del self.contexts[context_id]
            return True
        return False
    
    def cleanup_expired(self) -> int:
        """
        Remove expired contexts.
        
        Returns:
            Number of contexts cleaned up
        """
        expired = [
            cid for cid, ctx in self.contexts.items()
            if ctx.metadata.is_expired()
        ]
        
        for context_id in expired:
            self.delete_context(context_id)
        
        return len(expired)
    
    def get_context_stats(self) -> Dict[str, Any]:
        """Get statistics about contexts."""
        total = len(self.contexts)
        by_type = {}
        by_access_level = {}
        
        for context in self.contexts.values():
            ctype = context.metadata.context_type.value
            by_type[ctype] = by_type.get(ctype, 0) + 1
            
            alevel = context.metadata.access_level.value
            by_access_level[alevel] = by_access_level.get(alevel, 0) + 1
        
        return {
            "total_contexts": total,
            "by_type": by_type,
            "by_access_level": by_access_level,
            "subscriptions": {cid: len(agents) for cid, agents in self.subscriptions.items()}
        }
    
    def _subscribe_agent(self, context_id: str, agent_name: str) -> bool:
        """Internal method to subscribe agent."""
        if context_id not in self.subscriptions:
            self.subscriptions[context_id] = set()
        
        self.subscriptions[context_id].add(agent_name)
        return True
    
    def _notify_subscribers(self, context_id: str, updater: str) -> None:
        """Notify subscribed agents of context update."""
        agents = self.subscriptions.get(context_id, set())
        # In a real implementation, this would send notifications
        # through the message bus to subscribed agents
