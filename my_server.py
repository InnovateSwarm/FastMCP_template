from fastmcp import FastMCP
from pathlib import Path
from typing import Dict, Any
import os

mcp = FastMCP("InnovateSwarm")

TEMPLATES_DIR = Path("templates")

# Resource: List all templates
@mcp.resource("swarm://templates")
def list_templates() -> Dict[str, Any]:
    """List all InnovateSwarm templates"""
    templates = {}
    for folder in TEMPLATES_DIR.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            readme = folder / "README.md"
            if readme.exists():
                content = readme.read_text()
                templates[folder.name] = {
                    "name": folder.name.replace("-", " ").title(),
                    "slug": folder.name,
                    "description": content.split("\n\n")[0][:250] + "...",
                }
    return {"templates": templates, "repo": "https://github.com/InnovateSwarm/InnovateSwarm-Instructions"}

# Generic template loader
@mcp.prompt("swarm://get-template/{template_name}")
def get_swarm_template(template_name: str, **variables) -> str:
    slug = template_name.lower().replace(" ", "-").replace("_", "-")
    template_dir = TEMPLATES_DIR / slug
    if not template_dir.exists():
        available = [f.name for f in TEMPLATES_DIR.iterdir() if f.is_dir() and not f.name.startswith('.')]
        return f"Template '{template_name}' not found.\nAvailable: {available}"
    
    content = (template_dir / "README.md").read_text()
    for key, value in variables.items():
        upper = key.upper()
        content = content.replace(f"{{{{ {upper} }}}}", str(value))
        content = content.replace(f"{{{{{upper}}}}}", str(value))
    return content

# === Your InnovateSwarm Prompts ===
@mcp.prompt("swarm://swarm-tank")
def swarm_tank(idea: str, industry: str = "tech") -> str:
    return get_swarm_template("swarm-tank", IDEA=idea, INDUSTRY=industry)

@mcp.prompt("swarm://idea-rescue")
def idea_rescue(seed_idea: str) -> str:
    return get_swarm_template("idea-rescue", SEED_IDEA=seed_idea)

@mcp.prompt("swarm://idea-factory")
def idea_factory(seed_concept: str, quantity: int = 20) -> str:
    return get_swarm_template("idea-factory", SEED_CONCEPT=seed_concept, QUANTITY=quantity)

@mcp.prompt("swarm://cross-pollination-engine")
def cross_pollination(core_idea: str, domains: str = "biology, music, architecture") -> str:
    return get_swarm_template("cross-pollination-engine", CORE_IDEA=core_idea, DOMAINS=domains)

@mcp.prompt("swarm://mve")
def minimal_viable_experiment(idea: str, key_assumption: str = "") -> str:
    return get_swarm_template("mve", IDEA=idea, KEY_ASSUMPTION=key_assumption)

@mcp.prompt("swarm://future-backcasting")
def future_backcasting(desired_future: str, timeframe: str = "5 years") -> str:
    return get_swarm_template("future-backcasting", DESIRED_FUTURE=desired_future, TIMEFRAME=timeframe)

@mcp.prompt("swarm://innovation-critique")
def innovation_critique(idea: str, focus_areas: str = "all") -> str:
    return get_swarm_template("innovation-critique", IDEA=idea, FOCUS_AREAS=focus_areas)


if __name__ == "__main__":
    print("🚀 InnovateSwarm MCP Server is running!")
    import asyncio
    asyncio.run(mcp.run_async())
