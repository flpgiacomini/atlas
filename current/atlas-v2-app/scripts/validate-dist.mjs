import { access, readdir, readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const dist = resolve(root, "dist");
const baseline = JSON.parse(await readFile(resolve(root, "gates/published-baseline.json"), "utf8"));

await access(resolve(dist, "index.html"));
await access(resolve(dist, "404.html"));
await access(resolve(dist, "data/v2/manifest.json"));
await access(resolve(dist, "data/v2/geography.json"));
await access(resolve(dist, "cesium/Workers"));
for (const year of baseline.anchorYears) await access(resolve(dist, String(year), "index.html"));

const yearDirectories = (await readdir(dist, { withFileTypes: true }))
  .filter((entry) => entry.isDirectory() && /^\d{4}$/.test(entry.name));

// Piso, não igualdade: publicar mais anos é expansão editorial, publicar menos
// é perda do que já estava no ar.
if (yearDirectories.length < baseline.minimums.yearRoutes) {
  throw new Error(`Year routes regressed: ${yearDirectories.length} built, ${baseline.minimums.yearRoutes} in the published baseline`);
}

// Cada capítulo do acervo precisa ter rota; um capítulo novo sem página é uma
// falha de build, não uma expansão.
const chapters = JSON.parse(await readFile(resolve(dist, "data/v2/annual-chapters.json"), "utf8"));
const built = new Set(yearDirectories.map((entry) => entry.name));
const unrouted = chapters.items.map((item) => String(item.year)).filter((year) => !built.has(year));
if (unrouted.length) throw new Error(`Chapters without a published route: ${unrouted.join(", ")}`);

const home = await readFile(resolve(dist, "index.html"), "utf8");
if (!home.includes("Atlas v2") || !home.includes("<astro-island")) throw new Error("Atlas shell missing from prerendered home");
console.log(JSON.stringify({ status: "PASS", yearRoutes: yearDirectories.length, chapters: chapters.count ?? chapters.items.length, requiredAssets: "present" }));
