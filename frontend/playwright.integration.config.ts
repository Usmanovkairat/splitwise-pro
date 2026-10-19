import {defineConfig} from '@playwright/test';
export default defineConfig({
 testDir:'./e2e',testMatch:'integration.spec.ts',workers:1,reporter:'list',timeout:60000,
 use:{baseURL:'http://127.0.0.1:5173',headless:true,launchOptions:process.env.QA_CHROMIUM_PATH?{executablePath:process.env.QA_CHROMIUM_PATH,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']}:{}},
 webServer:[
 {command:`${process.env.QA_PYTHON||(process.platform==='win32'?'../.venv/Scripts/python.exe':'../.venv/bin/python')} e2e/api-server.py`,url:'http://127.0.0.1:8000/api/health',reuseExistingServer:false,timeout:60000},
 {command:'npm run dev -- --host 127.0.0.1',env:{VITE_SERVICE_MODE:'api'},url:'http://127.0.0.1:5173',reuseExistingServer:false,timeout:60000}
 ]
});
