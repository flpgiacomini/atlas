import { access, readdir, readFile, stat } from "node:fs/promises";
import { basename, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const dist = resolve(root, "dist");
const v2 = resolve(root, "../atlas-v2");
const home = await readFile(resolve(dist, "index.html"), "utf8");
const pkg = JSON.parse(await readFile(resolve(root, "package.json"), "utf8"));
const geography = JSON.parse(await readFile(resolve(dist, "data/v2/geography.json"), "utf8"));
const c18 = JSON.parse(await readFile(resolve(v2, "reports/c18-semantic-audit.json"), "utf8"));
const journeys = JSON.parse(await readFile(resolve(dist, "data/v2/journeys.json"), "utf8"));

if (!pkg.dependencies?.["maplibre-gl"] || !pkg.dependencies?.cesium) throw new Error("MapLibre and Cesium must be locally packaged");
if (geography.count !== 97 || geography.features.length !== 97) throw new Error("CP20 requires all 97 temporal geometries");
if (c18.status !== "PASS" || c18.passed !== 522 || c18.failed !== 0) throw new Error("C18 semantic gate is not green");
if (journeys.count !== 6 || journeys.items.some((item) => item.coverageState !== "connected")) throw new Error("Six required journeys are not connected");
await access(resolve(dist, "cesium/Workers"));

const scriptMatches = [
  ...[...home.matchAll(/<script[^>]+src="([^"]+\.js)"/g)].map((match) => basename(match[1])),
  ...[...home.matchAll(/(?:component-url|renderer-url)="([^"]+\.js)"/g)].map((match) => basename(match[1])),
];
const initialScripts = [...new Set(scriptMatches)];
const initialJsBytes = (await Promise.all(initialScripts.map(async (file) => (await stat(resolve(dist, "_astro", file))).size))).reduce((sum, size) => sum + size, 0);
if (initialJsBytes > 400_000) throw new Error(`Initial JavaScript budget exceeded: ${initialJsBytes}`);

const astroFiles = await readdir(resolve(dist, "_astro"), { withFileTypes: true });
const jsFiles = astroFiles.filter((item) => item.isFile() && item.name.endsWith(".js"));
const jsText = (await Promise.all(jsFiles.map((item) => readFile(resolve(dist, "_astro", item.name), "utf8")))).join("\n");
for (const marker of ["MAPA LOCAL", "GLOBO LOCAL", "RIO GENEALÓGICO", "LINHAGENS DE VEÍCULOS", "TEMPORADAS E SÉRIES", "FLUXOS DE DIFUSÃO"]) {
  if (!jsText.includes(marker)) throw new Error(`Missing specialized-view marker: ${marker}`);
}
const cesiumRuntime = resolve(dist, "cesium/Cesium.js");
await access(cesiumRuntime);
if (home.includes("cesium/Cesium.js")) throw new Error("Cesium must not be eager-loaded by the home page");
const cesiumChunkBytes = (await stat(cesiumRuntime)).size;

async function directorySize(directory) {
  let bytes = 0;
  for (const item of await readdir(directory, { withFileTypes: true })) {
    const path = resolve(directory, item.name);
    bytes += item.isDirectory() ? await directorySize(path) : (await stat(path)).size;
  }
  return bytes;
}

console.log(JSON.stringify({
  status: "PASS", checkpoint: "CP20", c18Audited: c18.passed,
  journeys: journeys.count, geographyFeatures: geography.count,
  initialJsBytes, initialScriptCount: initialScripts.length,
  cesiumLazyChunkBytes: cesiumChunkBytes, distBytes: await directorySize(dist),
}, null, 2));
