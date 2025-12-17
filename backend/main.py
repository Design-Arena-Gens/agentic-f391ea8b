from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from core.agent import NexusAgent
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Nexus AGI Backend", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = NexusAgent(llm_provider=os.getenv("LLM_PROVIDER", "anthropic"))

# Request/Response models
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

@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    """Main chat endpoint"""
    try:
        result = agent.process_message(request.message)
        return MessageResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/stats")
async def get_memory_stats():
    """Get memory and learning statistics"""
    try:
        stats = agent.get_memory_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/query")
async def query_memory(request: MemoryQuery):
    """Query vector memory"""
    try:
        memories = agent.vector_memory.query_memory(request.query, request.n_results)
        return {"memories": memories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/episodes")
async def get_episodes(n: int = 10):
    """Get recent episodes"""
    try:
        episodes = agent.episodic_memory.get_recent_episodes(n)
        return {"episodes": episodes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/patterns")
async def get_patterns():
    """Get learned patterns"""
    try:
        patterns = agent.learning_engine.get_patterns()
        return {"patterns": patterns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/skills")
async def get_skills():
    """Get learned skills"""
    try:
        skills = agent.learning_engine.get_skills()
        return {"skills": skills}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools")
async def get_tools():
    """Get available tools"""
    try:
        tools = agent.tool_registry.get_tool_definitions()
        return {"tools": tools}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/memory/clear")
async def clear_memory():
    """Clear all memories"""
    try:
        agent.clear_memories()
        return {"status": "success", "message": "All memories cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
