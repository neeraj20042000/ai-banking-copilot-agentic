"""
Memory Module

Provides two types of memory:
- Short-term (conversational): Ephemeral history of recent conversations
- Long-term (persistent): User profile, preferences, and key takeaways
"""

from memory.short_term import (
    ShortTermMemory,
    add_conversation,
    get_conversation_history
)

from memory.long_term import (
    LongTermMemory,
    add_session_memory,
    get_persistent_context
)

__all__ = [
    # Short-term memory
    "ShortTermMemory",
    "add_conversation",
    "get_conversation_history",
    # Long-term memory
    "LongTermMemory",
    "add_session_memory",
    "get_persistent_context",
]
