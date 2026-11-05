const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    // เปลี่ยนเว็บที่จะทดสอบได้ที่นี่ หรือรัน: npx cypress run --config baseUrl=https://www.saucedemo.com
    baseUrl: 'http://localhost:8000',
    supportFile: false,
  },
})
