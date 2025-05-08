@echo off
setlocal

REM Get environment variables with defaults
if "%TEST_USERNAME%"=="" set TEST_USERNAME=pipen
if "%TEST_PASSWORD%"=="" set TEST_PASSWORD=1234aa
if "%TEST_APP_VERSION%"=="" set TEST_APP_VERSION=v2.1.3

echo Starting all tests on multiple browsers...

echo Running tests with Chromium...
set BROWSER_TYPE=chromium
call npx playwright test %*

echo Running tests with Firefox...
set BROWSER_TYPE=firefox
call npx playwright test %*

echo Running tests with WebKit...
set BROWSER_TYPE=webkit
call npx playwright test %*

echo All tests completed!
endlocal