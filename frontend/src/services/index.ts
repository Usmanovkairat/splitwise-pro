import type { Service } from "./types";
import { apiService } from "./apiService";
import { mockService } from "./mockService";
// Real SQLite-backed API by default. Explicit demo mode preserves iteration 1.
export const service: Service =
  import.meta.env.VITE_SERVICE_MODE === "mock" ? mockService : apiService;
