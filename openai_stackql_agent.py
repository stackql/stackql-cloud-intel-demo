"""
OpenAI StackQL Agent
Integrates OpenAI's GPT models with StackQL's MCP server for cloud infrastructure intelligence.
"""

import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from stackql_mcp_client import StackQLMCPClient


class OpenAIStackQLAgent:
    """Agent that uses OpenAI to interact with StackQL via MCP."""

    # Define the tools available to OpenAI in OpenAI function calling format
    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "greet",
                "description": "Test the StackQL MCP connection with a simple greeting",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name to greet"
                        }
                    },
                    "required": ["name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_providers",
                "description": "List all available StackQL cloud providers (e.g., google, aws, azure, github, okta, etc.)",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_services",
                "description": "List services available in a specific cloud provider",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "provider": {
                            "type": "string",
                            "description": "The provider name (e.g., 'google', 'aws', 'azure')"
                        }
                    },
                    "required": ["provider"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_resources",
                "description": "List resources available in a provider's service",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "provider": {
                            "type": "string",
                            "description": "The provider name"
                        },
                        "service": {
                            "type": "string",
                            "description": "The service name"
                        }
                    },
                    "required": ["provider", "service"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_methods",
                "description": "List methods available for a specific resource",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "provider": {
                            "type": "string",
                            "description": "The provider name"
                        },
                        "service": {
                            "type": "string",
                            "description": "The service name"
                        },
                        "resource": {
                            "type": "string",
                            "description": "The resource name"
                        }
                    },
                    "required": ["provider", "service", "resource"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "query_stackql",
                "description": "Execute a StackQL query to retrieve information about cloud resources. Use SQL-like syntax to query cloud infrastructure across multiple providers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "The StackQL query to execute (e.g., 'SELECT * FROM google.compute.instances WHERE project = \"myproject\"')"
                        }
                    },
                    "required": ["sql"]
                }
            }
        }
    ]

    def __init__(self, openai_api_key: str, stackql_mcp_url: str = "http://127.0.0.1:9912", model: str = "gpt-4o-mini"):
        """
        Initialize the OpenAI StackQL Agent.

        Args:
            openai_api_key: OpenAI API key
            stackql_mcp_url: URL of the StackQL MCP server
            model: OpenAI model to use
        """
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.stackql_client = StackQLMCPClient(base_url=stackql_mcp_url)
        self.model = model
        self.conversation_history: List[Dict[str, Any]] = []

    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute a StackQL tool.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            Tool execution result as a string
        """
        try:
            if tool_name == "greet":
                return self.stackql_client.greet(arguments.get("name", "World"))

            elif tool_name == "list_providers":
                providers = self.stackql_client.list_providers()
                return "\n".join(providers)

            elif tool_name == "list_services":
                services = self.stackql_client.list_services(arguments["provider"])
                return "\n".join(services)

            elif tool_name == "list_resources":
                resources = self.stackql_client.list_resources(
                    arguments["provider"],
                    arguments["service"]
                )
                return "\n".join(resources)

            elif tool_name == "list_methods":
                methods = self.stackql_client.list_methods(
                    arguments["provider"],
                    arguments["service"],
                    arguments["resource"]
                )
                return "\n".join(methods)

            elif tool_name == "query_stackql":
                return self.stackql_client.query(arguments["sql"])

            else:
                return f"Unknown tool: {tool_name}"

        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"

    def chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a chat message and get a response.

        Args:
            user_message: The user's message
            system_prompt: Optional system prompt to guide the assistant

        Returns:
            The assistant's response
        """
        # Initialize conversation with system prompt if this is the first message
        if not self.conversation_history and system_prompt:
            self.conversation_history.append({
                "role": "system",
                "content": system_prompt
            })

        # Add user message to conversation
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        max_iterations = 10  # Prevent infinite loops
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Get response from OpenAI
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=self.TOOLS,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            # Add assistant's response to conversation
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": assistant_message.tool_calls
            })

            # Check if the assistant wants to call tools
            if assistant_message.tool_calls:
                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Execute the tool
                    tool_result = self._execute_tool(function_name, function_args)

                    # Add tool result to conversation
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": tool_result
                    })

                # Continue the loop to get the final response
                continue

            # No more tool calls, return the assistant's message
            return assistant_message.content or "I apologize, but I couldn't generate a response."

        return "I apologize, but I reached the maximum number of iterations while processing your request."

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        return self.conversation_history


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)

    # Create agent
    agent = OpenAIStackQLAgent(
        openai_api_key=api_key,
        model="gpt-4o-mini"
    )

    # Test the agent
    system_prompt = """You are a helpful cloud infrastructure assistant powered by StackQL.
You can help users query and analyze their cloud resources across multiple cloud providers including
Google Cloud, AWS, Azure, and many others. Use the available tools to answer questions about
cloud infrastructure, resources, and configurations."""

    print("Testing OpenAI StackQL Agent...")
    print("-" * 50)

    # Test query
    response = agent.chat(
        "What cloud providers are available?",
        system_prompt=system_prompt
    )
    print(f"Response: {response}")
