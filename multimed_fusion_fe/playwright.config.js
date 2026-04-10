import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/ui",
  timeout: 60000,
  fullyParallel: false,
  expect: {
    timeout: 10000,
  },
  workers: 1,
  use: {
    baseURL: process.env.UI_BASE_URL || "http://127.0.0.1:5173",
    headless: false,
    launchOptions: {
      slowMo: Number(process.env.PW_SLOW_MO || 0),
    },
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
});
