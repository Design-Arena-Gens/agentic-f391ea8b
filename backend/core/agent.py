from typing import List, Dict, Optional
from .memory.vector_store import VectorMemory
from .memory.episodic import EpisodicMemory
from .learning.learning_engine import LearningEngine
from .llm.llm_client import LLMClient
from .tools.tool_registry import ToolRegistry
from datetime import datetime

class NexusAgent:
    def __init__(self, llm_provider: str = "anthropic"):
        self.vector_memory = VectorMemory()
        self.episodic_memory = EpisodicMemory()
        self.learning_engine = LearningEngine()
        self.llm = LLMClient(provider=llm_provider)
        self.tool_registry = ToolRegistry()
        self.conversation_history = []

    def process_message(self, user_message: str) -> Dict:
        """Main processing pipeline"""
        # 1. Retrieve relevant memories
        relevant_memories = self.vector_memory.query_memory(user_message, n_results=3)
        recent_episodes = self.episodic_memory.get_recent_episodes(n=5)

        # 2. Build context
        context = self._build_context(user_message, relevant_memories, recent_episodes)

        # 3. Prepare messages for LLM
        messages = self._prepare_messages(user_message, context)

        # 4. Generate response with tools
        tools = self.tool_registry.get_tool_definitions()
        response = self.llm.generate_with_tools(
            messages=messages,
            tools=tools,
            system=self._get_system_prompt()
        )

        # 5. Execute tool calls if any
        tool_results = []
        final_text = ""

        for content in response["content"]:
            if content["type"] == "text":
                final_text += content["text"]

        if response["tool_calls"]:
            for tool_call in response["tool_calls"]:
                result = self.tool_registry.execute_tool(
                    tool_call["name"],
                    tool_call["input"]
                )
                tool_results.append({
                    "tool": tool_call["name"],
                    "input": tool_call["input"],
                    "result": result
                })

                # Learn from tool usage
                self.learning_engine.learn_skill(
                    tool_call["name"],
                    {"input": tool_call["input"], "result": result}
                )

            # Generate final response with tool results
            messages.append({
                "role": "assistant",
                "content": response["content"]
            })
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tc["id"],
                        "content": str(tool_results[i]["result"])
                    }
                    for i, tc in enumerate(response["tool_calls"])
                ]
            })

            final_response = self.llm.generate(messages=messages)
            final_text = final_response

        # 6. Store memories
        self.vector_memory.add_memory(
            content=f"User: {user_message}\nAgent: {final_text}",
            metadata={"type": "conversation", "timestamp": datetime.utcnow().isoformat()}
        )

        episode_data = {
            "user_message": user_message,
            "agent_response": final_text,
            "tools_used": [tr["tool"] for tr in tool_results],
            "context": {"relevant_memories": len(relevant_memories)}
        }
        self.episodic_memory.add_episode(episode_data)

        # 7. Detect patterns and learn
        pattern_id = self.learning_engine.detect_pattern(episode_data)

        # 8. Update conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": final_text
        })

        return {
            "response": final_text,
            "tool_results": tool_results,
            "pattern_detected": pattern_id,
            "memories_used": len(relevant_memories),
            "timestamp": datetime.utcnow().isoformat()
        }

    def _build_context(self, user_message: str, memories: List[Dict], episodes: List[Dict]) -> str:
        context = "# Relevant Context\n\n"

        if memories:
            context += "## Relevant Memories:\n"
            for mem in memories:
                context += f"- {mem['content'][:200]}...\n"

        if episodes:
            context += "\n## Recent Interactions:\n"
            for ep in episodes[-3:]:
                context += f"- User: {ep['user_message'][:100]}...\n"
                context += f"  Agent: {ep['agent_response'][:100]}...\n"

        return context

    def _prepare_messages(self, user_message: str, context: str) -> List[Dict]:
        messages = []

        # Add relevant conversation history
        if self.conversation_history:
            messages.extend(self.conversation_history[-6:])

        # Add current message with context
        messages.append({
            "role": "user",
            "content": f"{context}\n\n# Current Request:\n{user_message}"
        })

        return messages

    def _get_system_prompt(self) -> str:
        skills = self.learning_engine.get_skills()
        skill_summary = ", ".join([f"{name} (lvl {data['level']})" for name, data in list(skills.items())[:5]])

        return f"""You are Nexus AGI, an advanced autonomous agent with memory, learning, and tool-use capabilities.

Your Capabilities:
- Access to vector memory for semantic recall
- Episodic memory of past interactions
- Learning engine that detects patterns and improves skills
- Tool execution for real-world actions

Current Skills: {skill_summary if skill_summary else "Building initial skills"}

Approach each task thoughtfully:
1. Consider relevant memories and past interactions
2. Use tools when actions are needed
3. Learn from each interaction
4. Provide clear, helpful responses

Be proactive, intelligent, and continuously learning."""

    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        return {
            "vector_memories": len(self.vector_memory.get_all_memories()),
            "episodes": len(self.episodic_memory.get_recent_episodes(n=1000)),
            "learning_stats": self.learning_engine.get_learning_stats()
        }

    def clear_memories(self):
        """Clear all memories"""
        self.vector_memory.clear_all()
        self.episodic_memory.clear_all()
        self.conversation_history = []
