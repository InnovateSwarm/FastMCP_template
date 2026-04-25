import asyncio
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

async def main():
    await mcp.run_async()

if __name__ == "__main__":
    print("🚀 InnovateSwarm MCP Server starting...")
    
    # Force the standard MCP path
    import asyncio
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=8080,           # Railway often uses 8080
            path="/mcp"
        )
    )
    
