import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://flpgiacomini.github.io',
  base: '/atlas',
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
