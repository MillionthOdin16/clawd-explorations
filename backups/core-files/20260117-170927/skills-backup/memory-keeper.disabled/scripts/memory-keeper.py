#!/usr/bin/env python3
"""Memory Keeper CLI for Clawdbot - Persistent context storage."""

import argparse
import json
import os

# Memory storage path
DEFAULT_PATH = os.path.expanduser("~/.clawdbot/memory-keeper/memories.json")

def ensure_storage():
    """Ensure storage directory exists."""
    os.makedirs(os.path.dirname(DEFAULT_PATH), exist_ok=True)

def load_memories():
    """Load memories from storage."""
    ensure_storage()
    if os.path.exists(DEFAULT_PATH):
        with open(DEFAULT_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_memories(memories):
    """Save memories to storage."""
    ensure_storage()
    with open(DEFAULT_PATH, 'w') as f:
        json.dump(memories, f, indent=2)

def cmd_store(key, value):
    """Store a memory."""
    memories = load_memories()
    memories[key] = {
        "value": value,
        "created_at": json.dumps({"$date": os.path.getmtime(DEFAULT_PATH) if os.path.exists(DEFAULT_PATH) else None})
    }
    save_memories(memories)
    return {"status": "stored", "key": key, "value": value[:100]}

def cmd_retrieve(key):
    """Retrieve a memory."""
    memories = load_memories()
    if key in memories:
        return {"status": "found", "key": key, "value": memories[key]}
    return {"status": "not_found", "key": key}

def cmd_search(query):
    """Search memories."""
    memories = load_memories()
    results = []
    for key, data in memories.items():
        if query.lower() in key.lower() or query.lower() in str(data).lower():
            results.append({"key": key, "value": data.get("value", "")[:200]})
    return {"status": "success", "query": query, "results": results, "count": len(results)}

def cmd_list():
    """List all memories."""
    memories = load_memories()
    return {
        "status": "success", 
        "memories": list(memories.keys()), 
        "count": len(memories)
    }

def cmd_delete(key):
    """Delete a memory."""
    memories = load_memories()
    if key in memories:
        del memories[key]
        save_memories(memories)
        return {"status": "deleted", "key": key}
    return {"status": "not_found", "key": key}

def main():
    parser = argparse.ArgumentParser(description="Memory Keeper - Persistent context")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    store_parser = subparsers.add_parser("store", help="Store a memory")
    store_parser.add_argument("key")
    store_parser.add_argument("value")
    
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve a memory")
    retrieve_parser.add_argument("key")
    
    search_parser = subparsers.add_parser("search", help="Search memories")
    search_parser.add_argument("query")
    
    subparsers.add_parser("list", help="List all memories")
    
    delete_parser = subparsers.add_parser("delete", help="Delete a memory")
    delete_parser.add_argument("key")
    
    args = parser.parse_args()
    
    if args.command == "store":
        result = cmd_store(args.key, args.value)
    elif args.command == "retrieve":
        result = cmd_retrieve(args.key)
    elif args.command == "search":
        result = cmd_search(args.query)
    elif args.command == "list":
        result = cmd_list()
    elif args.command == "delete":
        result = cmd_delete(args.key)
    else:
        result = {"error": "Unknown command"}
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
