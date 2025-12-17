from typing import Dict, List, Callable, Any
import json
import os
import subprocess
from datetime import datetime

class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register default tools"""
        self.register_tool(
            name="execute_code",
            description="Execute Python code safely",
            parameters={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute"}
                },
                "required": ["code"]
            },
            function=self._execute_code
        )

        self.register_tool(
            name="search_web",
            description="Search the web for information",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            },
            function=self._search_web
        )

        self.register_tool(
            name="read_file",
            description="Read contents of a file",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to read"}
                },
                "required": ["path"]
            },
            function=self._read_file
        )

        self.register_tool(
            name="write_file",
            description="Write content to a file",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to write"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"]
            },
            function=self._write_file
        )

        self.register_tool(
            name="calculate",
            description="Perform mathematical calculations",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Mathematical expression to evaluate"}
                },
                "required": ["expression"]
            },
            function=self._calculate
        )

    def register_tool(self, name: str, description: str, parameters: Dict, function: Callable):
        self.tools[name] = {
            "name": name,
            "description": description,
            "input_schema": parameters,
            "function": function
        }

    def get_tool_definitions(self) -> List[Dict]:
        """Get tool definitions for LLM"""
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "input_schema": tool["input_schema"]
            }
            for tool in self.tools.values()
        ]

    def execute_tool(self, tool_name: str, parameters: Dict) -> Any:
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not found"}

        try:
            return self.tools[tool_name]["function"](**parameters)
        except Exception as e:
            return {"error": str(e)}

    def _execute_code(self, code: str) -> Dict:
        try:
            # Create a safe execution environment
            exec_globals = {"__builtins__": __builtins__}
            exec_locals = {}
            exec(code, exec_globals, exec_locals)
            return {"success": True, "result": str(exec_locals)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _search_web(self, query: str) -> Dict:
        # Placeholder for web search
        return {
            "success": True,
            "results": [
                {"title": f"Result for: {query}", "snippet": "This is a simulated search result."}
            ]
        }

    def _read_file(self, path: str) -> Dict:
        try:
            with open(path, 'r') as f:
                content = f.read()
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _write_file(self, path: str, content: str) -> Dict:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return {"success": True, "path": path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _calculate(self, expression: str) -> Dict:
        try:
            result = eval(expression, {"__builtins__": {}})
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
