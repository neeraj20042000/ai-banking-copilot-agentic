"""
Short-term / Conversational Memory Module

Maintains ephemeral conversation history for the current agent cycle.
Keeps track of the last 3 conversations to limit token usage.
"""

from typing import List, Dict
from datetime import datetime


class ShortTermMemory:
    """Ephemeral conversational memory - tracks recent dialogue history"""
    
    def __init__(self, max_conversations: int = 3):
        self.max_conversations = max_conversations
        self.conversations: List[Dict[str, str]] = []
    
    def add(self, role: str, content: str) -> None:
        """Add a conversation turn to memory"""
        self.conversations.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last N conversations
        if len(self.conversations) > self.max_conversations:
            self.conversations = self.conversations[-self.max_conversations:]
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversations
    

# Global instance for shared conversational memory
_global_memory = ShortTermMemory()


def add_conversation(role: str, content: str) -> None:
    """Convenience function to add to global memory"""
    _global_memory.add(role, content)


def get_conversation_history() -> List[Dict[str, str]]:
    """Convenience function to get raw conversation history."""
    return _global_memory.get_history()
