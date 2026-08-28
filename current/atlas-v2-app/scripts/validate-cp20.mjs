import { access, readdir, readFile, stat, writeFile } from "node:fs/promises";
import { basename, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const dist = resolve(root, "dist");
const v2 = resolve(root, "../atlas-v2");
const baselinePath = resolve(root, "gates/published-baseline.json");
const promote = process.argv.includes("--promote");

const baseline = JSON.parse(await readFile(baselinePath, "utf8"));
const home = await readFile(resolve(dist, "index.html"), "utf8");
const pkg = JSON.parse(await readFile(resolve(root, "package.json"), "utf8"));
const geography = JSON.parse(await readFile(resolve(dist, "data/v2/geography.json"), "utf8"));
const c18 = JSON.parse(await readFile(resolve(v2, "reports/c18-semantic-audit.json"), "utf8"));
const journeys = JSON.parse(await readFile(resolve(dist, "data/v2/journeys.json"), "utf8"));

// Invariantes: valem em qualquer tamanho do acervo e não dependem do baseline.
if (!pkg.dependencies?.["maplibre-gl"] || !pkg.dependencies?.cesium) throw new Error("MapLibre and Cesium must be locally packaged");
if (geography.count !== geography.features.length) throw new Error(`Geography bundle is inconsistent: count ${geography.count} vs ${geography.features.length} features`);
if (c18.status !== "PASS" || c18.failed !== 0) throw new Error("C18 semantic gate is not green");
if (journeys.count !== journeys.items.length) throw new Error(`Journeys bundle is inconsistent: count ${journeys.count} vs ${journeys.items.length} items`);
if (journeys.items.some((item) => item.coverageState !== "connected")) throw new Error("Required journeys are not connected");
await access(resolve(dist, "cesium/Workers"));

const yearRoutes = (await readdir(dist, { withFileTypes: true }))
  .filter((entry) => entry.isDirectory() && /^\d{4}$/.test(entry.name)).length;

// Gates de não-regressão. Expandir o acervo nunca pode quebrar o build; o que
// o gate protege é a perda silenciosa do que já foi publicado.
const observed = {
  geographyFeatures: geography.features.length,
  c18AuditedDecisions: c18.passed,
  journeys: journeys.count,
  yearRoutes,
};
const regressions = Object.entries(baseline.minimums)
  .filter(([key, floor]) => observed[key] < floor)
  .map(([key, floor]) => `${key}: ${observed[key]} publicado agora, ${floor} no baseline`);
if (regressions.length && !promote) {
  throw new Error(`Regressão contra o baseline publicado:\n  ${regressions.join("\n  ")}\nSe a redução for deliberada, promova o baseline com \`npm run gates:promote\`.`);
}

const scriptMatches = [
  ...[...home.matchAll(/<script[^>]+src="([^"]+\.js)"/g)].map((match) => basename(match[1])),
  ...[...home.matchAll(/(?:component-url|renderer-url)="([^"]+\.js)"/g)].map((match) => basename(match[1])),
];
const initialScripts = [...new Set(scriptMatches)];
const initialJsBytes = (await Promise.all(initialScripts.map(async (file) => (await stat(resolve(dist, "_astro", file))).size))).reduce((sum, size) => sum + size, 0);
if (initialJsBytes > baseline.budgets.initialJsBytes) throw new Error(`Initial JavaScript budget exceeded: ${initialJsBytes} > ${baseline.budgets.initialJsBytes}`);

const astroFiles = await readdir(resolve(dist, "_astro"), { withFileTypes: true });
const jsFiles = astroFiles.filter((item) => item.isFile() && item.name.endsWith(".js"));
const jsText = (await Promise.all(jsFiles.map((item) => readFile(resolve(dist, "_astro", item.name), "utf8")))).join("\n");
for (const marker of baseline.specializedViewMarkers) {
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

const growth = Object.fromEntries(Object.entries(observed).map(([key, value]) => [key, value - baseline.minimums[key]]));

if (promote) {
  const next = { ...baseline, recordedAt: new Date().toISOString().slice(0, 10), minimums: observed };
  await writeFile(baselinePath, `${JSON.stringify(next, null, 2)}\n`);
}

console.log(JSON.stringify({
  status: "PASS", checkpoint: "CP20", baseline: baseline.recordedAt,
  promoted: promote, observed, growthSinceBaseline: growth,
  initialJsBytes, initialScriptCount: initialScripts.length,
  cesiumLazyChunkBytes: cesiumChunkBytes, distBytes: await directorySize(dist),
}, null, 2));
