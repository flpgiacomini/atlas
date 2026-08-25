import { access, readdir, readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const dist = resolve(root, "dist");
const requiredYears = [1769, 1886, 1908, 1955, 1958, 1963, 1969, 1997, 2026];

await access(resolve(dist, "index.html"));
await access(resolve(dist, "404.html"));
await access(resolve(dist, "data/v2/manifest.json"));
await access(resolve(dist, "data/v2/geography.json"));
await access(resolve(dist, "cesium/Workers"));
for (const year of requiredYears) await access(resolve(dist, String(year), "index.html"));

const yearDirectories = (await readdir(dist, { withFileTypes: true }))
  .filter((entry) => entry.isDirectory() && /^\d{4}$/.test(entry.name));
if (yearDirectories.length !== 258) throw new Error(`Expected 258 year routes, found ${yearDirectories.length}`);

const home = await readFile(resolve(dist, "index.html"), "utf8");
if (!home.includes("Atlas v2") || !home.includes("<astro-island")) throw new Error("Atlas shell missing from prerendered home");
console.log(JSON.stringify({ status: "PASS", yearRoutes: yearDirectories.length, requiredAssets: "present" }));
