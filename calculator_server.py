from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Calculator Server")

# Define tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

# Run the MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
