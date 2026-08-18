import sharp from "sharp";
import { readdir } from "node:fs/promises";
import { join, parse } from "node:path";
import { fileURLToPath } from "node:url";

const directory = new URL("../public/media/editorial/", import.meta.url);
for (const file of await readdir(directory)) {
  if (!file.endsWith(".png")) continue;
  const source = new URL(file, directory);
  const target = new URL(`${parse(file).name}.webp`, directory);
  await sharp(fileURLToPath(source)).resize(1536, 1024, { fit: "cover" }).webp({ quality: 82, effort: 5 }).toFile(fileURLToPath(target));
  console.log(join("public/media/editorial", file), "->", join("public/media/editorial", parse(file).name + ".webp"));
}
