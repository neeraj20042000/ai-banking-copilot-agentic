"""
Long-term / Persistent Memory Module

Stores user preferences, key takeaways, and important information
across agent cycles. Persists to JSON file for durability.
"""

import json
import os
from typing import Dict, Any
from datetime import datetime

class LongTermMemory:
    """Persistent memory - stores user profile and preferences"""
    
    def __init__(self, storage_path: str = "memory/user_memory.json"):
        self.storage_path = storage_path
        self.data: Dict[str, Any] = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load memory from file"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._default_structure()
        return self._default_structure()
    
    def _default_structure(self) -> Dict[str, Any]:
        """Return default memory structure"""
        return {
            "user_id": "default",
            "profile": {
                "loan_interest": None,
                "income": None,
                "risk_level": None,
                "preferences": []
            },
            "key_takeaways": [],
            "important_keywords": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def save(self) -> None:
        """Persist memory to file"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_session_memory(self, keywords: list = None, takeaway: str = None) -> None:
        """Add keywords and takeaway from a session in a single call."""
        if keywords:
            if "important_keywords" not in self.data:
                self.data["important_keywords"] = []
            for kw in keywords:
                if kw not in self.data["important_keywords"]:
                    self.data["important_keywords"].append(kw)
        
        if takeaway:
            if "key_takeaways" not in self.data:
                self.data["key_takeaways"] = []
            if takeaway not in self.data["key_takeaways"]:
                self.data["key_takeaways"].append(takeaway)
        
        if keywords or takeaway:
            self.save()
    
    def get_profile(self) -> Dict[str, Any]:
        """Get user profile"""
        return self.data.get("profile", {})
    
    def get_keywords(self) -> list:
        """Get important keywords"""
        return self.data.get("important_keywords", [])

    def get_takeaways(self) -> list:
        """Get key takeaways"""
        return self.data.get("key_takeaways", [])
    
    def get_formatted_profile(self) -> str:
        """Get profile as formatted string for LLM context"""
        profile = self.get_profile()
        if not profile or all(v is None or v == [] for v in profile.values()):
            return "No user profile data available."
        
        lines = ["User Profile:"]
        for key, value in profile.items():
            if value is not None:
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)
    
    def get_formatted_keywords(self) -> str:
        """Get keywords as formatted string"""
        keywords = self.get_keywords()
        if not keywords:
            return ""
        return f"Important Keywords: {', '.join(keywords)}"

    def get_formatted_takeaways(self) -> str:
        """Get key takeaways as formatted string"""
        takeaways = self.get_takeaways()
        if not takeaways:
            return ""
        return "Key Takeaways:\n" + "\n".join(f"- {item}" for item in takeaways)
    

# Global instance for shared persistent memory
_global_memory = LongTermMemory()


def add_session_memory(keywords: list = None, takeaway: str = None) -> None:
    """Convenience function to add keywords and takeaway in a single call."""
    _global_memory.add_session_memory(keywords=keywords, takeaway=takeaway)


def get_persistent_context() -> str:
    """Get formatted persistent context for LLM injection"""
    profile = _global_memory.get_formatted_profile()
    keywords = _global_memory.get_formatted_keywords()
    takeaways = _global_memory.get_formatted_takeaways()
    
    parts = [p for p in [profile, keywords, takeaways] if p]
    return "\n".join(parts) if parts else ""
