import asyncio
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

async def main():
    await mcp.run_async()

if __name__ == "__main__":
    import asyncio
    print("🚀 InnovateSwarm MCP Server started!")
    print("MCP endpoint should be available at /mcp")
    
    # This is the recommended way for the Railway template
    asyncio.run(mcp.run_async(transport="streamable-http"))
    
