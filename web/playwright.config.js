const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  timeout: 30 * 1000,
  use: {
    baseURL: 'http://localhost:5173',
    headless: true,
  },
});
