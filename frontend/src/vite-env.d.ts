/// <reference types="vite/client" />
interface ImportMetaEnv {
  readonly VITE_SERVICE_MODE?: "mock" | "api";
  readonly VITE_API_BASE_URL?: string;
}
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
