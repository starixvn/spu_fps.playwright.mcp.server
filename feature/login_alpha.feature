Feature: Login Alpha site

  Scenario: Login to alp8.nexdev.net using Chromium
    No additional installation is required. All MCP tools are allowed. Do not use file code. Follow these steps:

    1. Launch Chromium browser and navigate to https://alp8.nexdev.net.

    2. Immediately capture the current timestamp at the time this step starts, subtract 4 hours from it, and save the result as a variable named `transTime`.

    3. Wait for the browser console log to contain the exact message "v2.1.3". This confirms that the correct app version has loaded.

    4. Fill the input field with id `txtUserName` with the text `pipen`.

    5. Click the element with id or selector for the verify button to proceed to the password step.

    6. Fill the input field with id `txtPassWord` with the text `1234aa`.

    7. Click the final login button to complete authentication.

    8. Wait until login is successful and the username is visible on the page or another confirmation element confirms success.

    9. Send a GET request to the GetTransaction07Info API endpoint at https://spu-fps-int-api.nexdev.net/swagger/v1/swagger.json with the appropriate parameters, using the API documentation as reference

    10. If the response is empty or indicates failure, wait for 3 seconds and retry the API call (reusing the same `transTime`). Repeat up to 3 times in total (original + 2 retries). 
    - Do not repeat the login flow.
    - Once a non-empty or successful result is returned from the API, mark the login flow as successfully validated.

  

