import { cp, mkdir, rm } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const targets = [
  [resolve(root, "../atlas-v2/bundles"), resolve(root, "public/data/v2")],
  [resolve(root, "../atlas-v2-prototype/public/assets"), resolve(root, "public/assets")],
  [resolve(root, "node_modules/cesium/Build/Cesium"), resolve(root, "public/cesium")],
];

for (const [source, target] of targets) {
  await rm(target, { recursive: true, force: true });
  await mkdir(dirname(target), { recursive: true });
  await cp(source, target, { recursive: true });
}

console.log("Atlas v2 content and editorial assets synchronized.");
