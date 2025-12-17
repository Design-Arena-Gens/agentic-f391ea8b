from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
import os
from datetime import datetime

app = FastAPI(title="Nexus AGI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
memory_store = []
episodes_store = []
patterns_store = []
skills_store = {}

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str
    tool_results: List[Dict]
    pattern_detected: Optional[str]
    memories_used: int
    timestamp: str

class MemoryQuery(BaseModel):
    query: str
    n_results: int = 5

@app.get("/")
async def root():
    return {
        "name": "Nexus AGI Backend",
        "version": "1.0.0",
        "status": "running",
        "capabilities": ["memory", "learning", "tools", "reasoning"]
    }

@app.post("/chat")
async def chat(request: MessageRequest):
    """Simplified chat endpoint for Vercel deployment"""
    response_text = f"Echo: {request.message} (Running on Vercel serverless)"

    # Store in memory
    memory_store.append({
        "content": f"User: {request.message}\nAgent: {response_text}",
        "timestamp": datetime.utcnow().isoformat()
    })

    episodes_store.append({
        "id": str(len(episodes_store)),
        "user_message": request.message,
        "agent_response": response_text,
        "timestamp": datetime.utcnow().isoformat(),
        "tools_used": []
    })

    return {
        "response": response_text,
        "tool_results": [],
        "pattern_detected": None,
        "memories_used": 0,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/memory/stats")
async def get_memory_stats():
    return {
        "vector_memories": len(memory_store),
        "episodes": len(episodes_store),
        "learning_stats": {
            "total_patterns": len(patterns_store),
            "total_skills": len(skills_store),
            "avg_skill_level": 0,
            "patterns": [],
            "top_skills": []
        }
    }

@app.post("/memory/query")
async def query_memory(request: MemoryQuery):
    return {"memories": memory_store[-request.n_results:]}

@app.get("/memory/episodes")
async def get_episodes(n: int = 10):
    return {"episodes": episodes_store[-n:]}

@app.get("/learning/patterns")
async def get_patterns():
    return {"patterns": patterns_store}

@app.get("/learning/skills")
async def get_skills():
    return {"skills": skills_store}

@app.get("/tools")
async def get_tools():
    return {
        "tools": [
            {
                "name": "echo",
                "description": "Echo back the input",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"}
                    }
                }
            }
        ]
    }

@app.delete("/memory/clear")
async def clear_memory():
    memory_store.clear()
    episodes_store.clear()
    return {"status": "success", "message": "All memories cleared"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Vercel serverless function handler
from mangum import Mangum
handler = Mangum(app)
