import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/enterprise": "http://127.0.0.1:8000",
      "/reconcile": "http://127.0.0.1:8000",
      "/review-queue": "http://127.0.0.1:8000",
      "/export": "http://127.0.0.1:8000",
      "/benchmark": "http://127.0.0.1:8000",
      "/curation": "http://127.0.0.1:8000",
      "/standards": "http://127.0.0.1:8000",
      "/data": {
        target: "http://127.0.0.1:8000",
        rewrite: (p) => p.replace(/^\/data/, ""),
      },
    },
  },
});
