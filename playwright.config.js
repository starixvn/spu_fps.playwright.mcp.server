const browserType = process.env.BROWSER_TYPE || 'chromium';

module.exports = {
  testDir: './tests',
  timeout: 30000,
  expect: {
    timeout: 5000
  },
  fullyParallel: false,
  retries: 0,
  workers: 1,
  reporter: 'list',
  use: {
    headless: false,  // Explicitly set headless to false
    actionTimeout: 0,
    trace: 'on-first-retry',
    video: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  projects: [
    {
      name: browserType,
      use: {
        browserName: browserType,
        testUsername: process.env.TEST_USERNAME || 'test10y',
      },
    }
  ],
};