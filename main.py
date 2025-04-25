from fastapi import FastAPI
from mcp_client import MCPClient
import uvicorn

app = FastAPI(title="MCP Server Demo", version="0.1.0")
client = MCPClient()
server_script_path = r"/media/hamzasidhu/New Volume/MCP Related/mcp-server-demo/calculator.py"  # Path to your server script

@app.on_event("startup")
async def startup_event():
    """Connect to the MCP server on startup"""
    await client.connect_to_server(server_script_path)
    print("✅ Connected to MCP server")
    
    
@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from the MCP server on shutdown"""
    await client.exit_stack.__aexit__(None, None, None)
    print("✅ Disconnected from MCP server")
    
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the MCP Server Demo!"}
@app.get("/tools")
async def get_tools():
    """Get the list of tools from the MCP server"""
    response = await client.session.list_tools()
    tools = response.tools
    return {"tools": [tool.name for tool in tools]}

@app.post("/chat")
async def chat_with_llm(prompt: str):
    """Chat with the LLM using the MCP server"""
    response, tool_name = await client.process_query(prompt)
    return {"answer": response, "tool_names": tool_name}

if __name__ == "__main__":

    uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="debug",
        )