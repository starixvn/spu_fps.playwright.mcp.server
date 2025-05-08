from typing import Any
from mcp.server.fastmcp import FastMCP
import json

# Initialize FastMCP server
mcp = FastMCP("reaction_website")

def _get_matching_scenario(search_params: dict) -> tuple[str, dict]:
    """
    Find the matching scenario from feature files based on search parameters.
    Returns tuple of (scenario_name, scenario_details)
    """
    scenarios = {
        "alpha": {
            "file": "login_alpha.feature",
            "keywords": ["alpha", "alp8", "nexdev", "pipen"],
            "url": "https://alp8.nexdev.net",
            "content": {
                "name": "Login Alpha site",
                "steps": [
                    "1. Launch Chromium browser and navigate to https://alp8.nexdev.net.",
                    "2. Immediately capture the current timestamp at the time this step starts, subtract 4 hours from it, and save the result as a variable named `transTime`.",
                    "3. Wait for the browser console log to contain the exact message \"v2.1.3\". This confirms that the correct app version has loaded.",
                    "4. Fill the input field with id `txtUserName` with the text `pipen`.",
                    "5. Click the element with id or selector for the verify button to proceed to the password step.",
                    "6. Fill the input field with id `txtPassWord` with the text `1234aa`.",
                    "7. Click the final login button to complete authentication.",
                    "8. Wait until login is successful and the username is visible on the page or another confirmation element confirms success.",
                    "9. Send a GET request to the GetTransaction07Info API endpoint at https://spu-fps-int-api.nexdev.net/swagger/v1/swagger.json with the appropriate parameters, using the API documentation as reference",
                    "10. If the response is empty or indicates failure, wait for 3 seconds and retry the API call (reusing the same `transTime`). Repeat up to 3 times in total (original + 2 retries)."
                ],
                "credentials": {
                    "username": "pipen",
                    "password": "1234aa"
                },
                "expected_version": "v2.1.3"
            }
        },
        "athena": {
            "file": "login_athena.feature",
            "keywords": ["athena", "qeo002", "athena000"],
            "url": "http://qeo002.athena000.com",
            "content": {
                "name": "Login Athena site",
                "steps": [
                    "1. Launch Chromium browser and navigate to http://qeo002.athena000.com.",
                    "2. Immediately capture the current timestamp at the time this step starts, subtract 4 hours from it, and save the result as a variable named `transTime`.",
                    "3. Fill the input field with id `#username` with the text `pipen`.",
                    "4. Fill the input field with id `#password` with the text `1234aa`.",
                    "5. Fill the input field with id `#validation`"
                ],
                "credentials": {
                    "username": "pipen",
                    "password": "1234aa"
                }
            }
        },
        "licensee": {
            "file": "login_licensee.feature",
            "keywords": ["licensee", "hl5888", "qatest05"],
            "url": "http://k957um408.hl5888.com/apilogin",
            "content": {
                "name": "Login Licensee site",
                "steps": [
                    "1. Launch Chromium browser and navigate to http://k957um408.hl5888.com/apilogin.",
                    "2. Fill the input field with id `#txtUserName` with the text `qatest05`.",
                    "3. Fill the input field with id `#CentralPassword` with the text `aa1234`.",
                    "4. Fill the input field with id `#CentralAccount` with the text `harmony.huynh`.",
                    "5. Click LoginBtn"
                ],
                "credentials": {
                    "username": "qatest05",
                    "password": "aa1234",
                    "centralAccount": "harmony.huynh"
                }
            }
        }
    }
    
    # Try to match by URL first
    url = search_params.get("url", "").lower()
    if url:
        for scenario_name, details in scenarios.items():
            if details["url"].lower() in url:
                return scenario_name, details
    
    # Try to match by keywords in search query
    query = json.dumps(search_params).lower()
    for scenario_name, details in scenarios.items():
        if any(keyword.lower() in query for keyword in details["keywords"]):
            return scenario_name, details
            
    return None, None

@mcp.tool()
async def get_scenario(search_query: str = "") -> str:
    """Get scenario based on specific requirements.

    Interacts with a web application based on provided parameters and returns the interaction status.

    Args:
        search_query (str): The search query to be used in the interaction.
        
    Returns:
        str: A message indicating the status of the web interaction.

    Note:
        This function supports additional parameters through the search_query:
        - URL/domain of the target website
        - Environment specification
        - Authentication credentials
        - Any additional required interaction parameters
    """
    try:
        # Parse search parameters from search_query
        params = {}
        if search_query:
            try:
                params = json.loads(search_query)
            except json.JSONDecodeError:
                params = {"query": search_query}

        # Find matching scenario
        scenario_name, scenario_details = _get_matching_scenario(params)
        
        if scenario_name and scenario_details:
            return json.dumps({
                "status": "success",
                "scenario": scenario_name,
                "feature_file": scenario_details["file"],
                "url": scenario_details["url"],
                "content": scenario_details["content"],
                "message": f"Found matching scenario: {scenario_name}"
            }, indent=2)
        else:
            return json.dumps({
                "status": "error",
                "message": "No matching scenario found for the provided parameters"
            }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error processing search query: {str(e)}"
        }, indent=2)

# if __name__ == "__main__":
#     import asyncio

#     async def test():
#         print(await get_scenario("get scenario for alpha"))
#         print(await get_scenario('{"url": "http://qeo002.athena000.com"}'))

#     asyncio.run(test())

if __name__ == "__main__":
    print("FastMCP server is running...")
    mcp.run(transport='stdio')