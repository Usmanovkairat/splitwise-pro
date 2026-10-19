# Browser QA runtime provisioning

Playwright library is provided by the primary Node runtime. Initial default `chromium.launch()` failed because the bundled browser executable was absent. `playwright install chromium` attempted five downloads, each returned a truncated/empty archive, and failed. No default browser execution is claimed.

Fallback: `npm install --prefix /tmp/splitwise-qa-browser @sparticuz/chromium` installed version 153.0.0. Its bundled Brotli archives were decompressed with Node zlib; tar archives extracted with `tar --no-same-owner` because package extraction attempted an unsupported chown. Runtime Chromium executable is `/tmp/chromium`, launch args come from the package default export.

Actual launch verification executed:

```js
const c = (await import('/tmp/splitwise-qa-browser/node_modules/@sparticuz/chromium/build/index.js')).default;
const { chromium } = require('playwright');
const browser = await chromium.launch({ executablePath: '/tmp/chromium', args: c.args, headless: true });
const page = await browser.newPage();
await page.setContent('<title>QA runtime</title><h1>Browser ready</h1>');
console.log(await page.title());
await browser.close();
```

Result: exit 0; title `QA runtime`. This verifies browser availability, not application acceptance. Application workflows and screenshots are recorded separately after iteration handoff.
