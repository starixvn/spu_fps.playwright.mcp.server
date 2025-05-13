
# Document:
https://github.com/microsoft/playwright-mcp

# Run script:
 - npm i


# Turtorial:
Add new MCP server to get-scenario:

    "mcp-scenario": {
        "command": "uv",
        "args": [
            "--directory",
            "<your-path>\\fps.playwright.mcp.server\\mcp-scenario",
            "run",
            "main.py"
        ]
    }

# Prompt:
Get scenario:

    using #get_scenario Get scenario for licensee site

Execute scenario:

    using #browser_navigate to execute this scenario

