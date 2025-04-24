import asyncio
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            temperature=0.2,
            max_tokens=2048,
            convert_system_message_to_human=True
        )

    # async def connect_to_server(self, server_script_path: str):
    #     """Connect to an MCP server"""
    #     is_python = server_script_path.endswith('.py')
    #     is_js = server_script_path.endswith('.js')
    #     if not (is_python or is_js):
    #         raise ValueError("Server script must be a .py or .js file")

    #     command = "python" if is_python else "node"
    #     server_params = StdioServerParameters(
    #         command=command,
    #         args=[server_script_path],
    #         env=None
    #     )

    #     stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
    #     self.stdio, self.write = stdio_transport
    #     self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

    #     await self.session.initialize()

    #     response = await self.session.list_tools()
    #     tools = response.tools
    #     print("\n✅ Connected to server with tools:", [tool.name for tool in tools])
    
    
    async def connect_to_server(self, server_script_path: str):
    
        try:
            """Connect to an MCP server"""
            is_python = server_script_path.endswith('.py')
            is_js = server_script_path.endswith('.js')
            if not (is_python or is_js):
                raise ValueError("Server script must be a .py or .js file")
    
            command = "python" if is_python else "node"
            server_params = StdioServerParameters(
                command=command,
                args=[server_script_path],
                env=None
            )
            
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            self.stdio, self.write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
            await self.session.initialize()

            response = await self.session.list_tools()
            tools = response.tools
            print("\n✅ Connected to server with tools:", [tool.name for tool in tools])
        except GeneratorExit:
            print("🔁 Generator was closed unexpectedly (Streamlit rerun or shutdown)")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise


    async def process_query(self, query: str) -> str:
        """Process a query using Gemini and MCP tools"""
        messages = [HumanMessage(content=query)]

        response = await self.session.list_tools()
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            for tool in response.tools
        ]

        # First response from Gemini
        ai_response = await self.llm.ainvoke(messages, tool_choice="auto", tools=available_tools)

        tool_results = []
        final_text = []
        total_tool_calls = []

        if isinstance(ai_response, AIMessage) and ai_response.tool_calls:
            for tool_call in ai_response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                total_tool_calls.append(tool_name)

                result = await self.session.call_tool(tool_name, tool_args)
                print(f"🛠️ Tool '{tool_name}' called with args: {tool_args} -> Result: {result.content}")

                messages.append(ai_response)
                messages.append(ToolMessage(tool_call_id=tool_call["id"], content=result.content))

                # Second call after tool usage
                ai_followup = await self.llm.ainvoke(messages)
                final_text.append(ai_followup.content)

        else:
            final_text.append(ai_response.content)

        return "\n".join(final_text),total_tool_calls

    async def chat_loop(self):
        """Interactive chat loop"""
        print("\n🤖 MCP Client Started — type your queries or 'quit' to exit.")
        while True:
            try:
                query = input("\n📝 Query: ").strip()
                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n💬 Response:\n", response)

            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
