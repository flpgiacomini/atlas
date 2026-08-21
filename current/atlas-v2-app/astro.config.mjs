import { defineConfig } from "astro/config";
import react from "@astrojs/react";

export default defineConfig({
  site: "https://flpgiacomini.github.io",
  base: "/atlas",
  output: "static",
  trailingSlash: "always",
  build: { format: "directory" },
  integrations: [react()],
});
