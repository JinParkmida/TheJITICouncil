import json
import hashlib
import os
from pathlib import Path

class Holocron:
    """
    The Holocron is the persistent memory of the Council.
    It stores the generated implementations of functions to avoid
    re-convening the Council for every call.
    """
    CACHE_FILE = Path("holocron.json")

    @classmethod
    def _load_cache(cls):
        if not cls.CACHE_FILE.exists():
            return {}
        try:
            with open(cls.CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    @classmethod
    def _save_cache(cls, cache):
        with open(cls.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)

    @staticmethod
    def _generate_key(func_name, signature):
        # Create a unique key based on name and signature
        # We could also include the docstring hash to invalidate if docs change
        content = f"{func_name}:{signature}"
        return hashlib.sha256(content.encode()).hexdigest()

    @classmethod
    def retrieve(cls, func_name, signature):
        """
        Retrieves the cached code for a function if it exists.
        """
        cache = cls._load_cache()
        key = cls._generate_key(func_name, signature)
        return cache.get(key)

    @classmethod
    def archive(cls, func_name, signature, code):
        """
        Saves the generated code to the Holocron.
        """
        cache = cls._load_cache()
        key = cls._generate_key(func_name, signature)
        cache[key] = code
        cls._save_cache(cache)

