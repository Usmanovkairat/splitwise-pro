import { defineConfig } from '@playwright/test';
export default defineConfig({
 testDir:'./e2e', fullyParallel:false, workers:1, reporter:'list',
 use:{baseURL:'http://127.0.0.1:5173',headless:true,launchOptions:process.env.QA_CHROMIUM_PATH?{executablePath:process.env.QA_CHROMIUM_PATH,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']}:{}},
 webServer:{command:'npm run dev -- --host 127.0.0.1',url:'http://127.0.0.1:5173',reuseExistingServer:!process.env.CI},
});
