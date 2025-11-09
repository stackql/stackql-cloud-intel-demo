"""
StackQL MCP Client
A Python client for interacting with StackQL's Model Context Protocol (MCP) server.
"""

import requests
import json
from typing import Dict, List, Any, Optional


class StackQLMCPClient:
    """Client for communicating with StackQL MCP server."""

    def __init__(self, base_url: str = "http://127.0.0.1:9912"):
        """
        Initialize the StackQL MCP client.

        Args:
            base_url: The base URL of the StackQL MCP server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def _call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            The tool's response
        """
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }

        try:
            response = self.session.post(
                f"{self.base_url}/",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()

            # Try to parse JSON response
            try:
                result = response.json()
            except json.JSONDecodeError as e:
                raise Exception(f"MCP server returned invalid JSON. Response: {response.text[:200]}")

            if "error" in result:
                error_detail = result['error']
                if isinstance(error_detail, dict):
                    error_msg = error_detail.get('message', str(error_detail))
                else:
                    error_msg = str(error_detail)
                raise Exception(f"MCP Error: {error_msg}")

            return result.get("result", {})

        except requests.exceptions.ConnectionError as e:
            raise Exception(f"Cannot connect to StackQL MCP server at {self.base_url}. Is the server running?")
        except requests.exceptions.Timeout as e:
            raise Exception(f"Request to StackQL MCP server timed out after 30 seconds")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP Error {response.status_code} from MCP server: {response.text[:200]}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to call MCP tool '{tool_name}': {str(e)}")

    def greet(self, name: str) -> str:
        """
        Test the MCP connection with a simple greeting.

        Args:
            name: Name to greet

        Returns:
            Greeting message
        """
        result = self._call_tool("greet", {"name": name})
        return result.get("content", [{}])[0].get("text", "")

    def list_providers(self) -> List[str]:
        """
        List all available StackQL providers.

        Returns:
            List of provider names
        """
        result = self._call_tool("list_providers")
        content = result.get("content", [{}])[0].get("text", "")

        # Parse the response to extract provider names
        try:
            # The response is typically a formatted string with provider names
            providers = [line.strip() for line in content.split('\n') if line.strip()]
            return providers
        except Exception:
            return [content]

    def list_services(self, provider: str) -> List[str]:
        """
        List services available in a provider.

        Args:
            provider: Provider name (e.g., 'google', 'aws', 'azure')

        Returns:
            List of service names
        """
        result = self._call_tool("list_services", {"provider": provider})
        content = result.get("content", [{}])[0].get("text", "")

        try:
            services = [line.strip() for line in content.split('\n') if line.strip()]
            return services
        except Exception:
            return [content]

    def list_resources(self, provider: str, service: str) -> List[str]:
        """
        List resources in a provider service.

        Args:
            provider: Provider name
            service: Service name

        Returns:
            List of resource names
        """
        result = self._call_tool("list_resources", {
            "provider": provider,
            "service": service
        })
        content = result.get("content", [{}])[0].get("text", "")

        try:
            resources = [line.strip() for line in content.split('\n') if line.strip()]
            return resources
        except Exception:
            return [content]

    def list_methods(self, provider: str, service: str, resource: str) -> List[str]:
        """
        List methods available for a resource.

        Args:
            provider: Provider name
            service: Service name
            resource: Resource name

        Returns:
            List of method names
        """
        result = self._call_tool("list_methods", {
            "provider": provider,
            "service": service,
            "resource": resource
        })
        content = result.get("content", [{}])[0].get("text", "")

        try:
            methods = [line.strip() for line in content.split('\n') if line.strip()]
            return methods
        except Exception:
            return [content]

    def query(self, sql: str) -> str:
        """
        Execute a StackQL query.

        Args:
            sql: The StackQL query to execute

        Returns:
            Query results as a string
        """
        result = self._call_tool("query_v2", {"sql": sql})
        content = result.get("content", [{}])[0].get("text", "")
        return content

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools from the MCP server.

        Returns:
            List of tool definitions
        """
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }

        try:
            response = self.session.post(
                f"{self.base_url}/",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if "error" in result:
                raise Exception(f"MCP Error: {result['error']}")

            return result.get("result", {}).get("tools", [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get available tools: {str(e)}")


if __name__ == "__main__":
    # Simple test
    client = StackQLMCPClient()

    try:
        # Test greeting
        print("Testing connection...")
        greeting = client.greet("World")
        print(f"✓ Greeting: {greeting}")

        # Test listing providers
        print("\nListing providers...")
        providers = client.list_providers()
        print(f"✓ Found {len(providers)} providers")
        for provider in providers[:5]:  # Show first 5
            print(f"  - {provider}")

    except Exception as e:
        print(f"✗ Error: {e}")
