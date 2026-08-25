import test from "node:test";
import assert from "node:assert/strict";
import { normalizeSearch, periodForYear, publicUrl, searchEntities, storyForYear, yearUrl } from "../src/lib/atlas-data.js";

test("normalizes accents and casing", () => {
  assert.equal(normalizeSearch("  Citroën DS  "), "citroen ds");
});

test("searches names, aliases and respects selected year", () => {
  const items = [
    { id: "1", name: "Citroën DS", aliases: ["DS 19"], type: "Vehicle", region: "França", yearStart: 1955 },
    { id: "2", name: "Toyota Prius", aliases: [], type: "Vehicle", region: "Japão", yearStart: 1997 },
    { id: "3", name: "Marca sem cronologia", aliases: [], type: "Brand", region: "Global", yearStart: null },
  ];
  assert.deepEqual(searchEntities(items, "citroen", 1960).map((item) => item.id), ["1"]);
  assert.deepEqual(searchEntities(items, "prius", 1960), []);
  assert.deepEqual(searchEntities(items, "japao", 2000).map((item) => item.id), ["2"]);
  assert.deepEqual(searchEntities(items, "sem cronologia", 1769).map((item) => item.id), ["3"]);
});

test("maps every boundary year to its publication period", () => {
  assert.equal(periodForYear(1769), "1769-1885");
  assert.equal(periodForYear(1886), "1886-1918");
  assert.equal(periodForYear(1955), "1940-1959");
  assert.equal(periodForYear(2026), "2020-2026");
});

test("builds base-aware public and annual URLs", () => {
  assert.equal(publicUrl("/data/v2/manifest.json", "/atlas/"), "/atlas/data/v2/manifest.json");
  assert.equal(yearUrl(1969, "/atlas/"), "/atlas/1969/");
});

test("uses only exact-year chapters and exposes editorial gaps", () => {
  const chapters = [{ year: 1769, title: "Cugnot", coverageState: "authored" }];
  const journeys = [{ year: 1886, title: "Benz", coverageState: "connected" }];
  assert.equal(storyForYear(1769, chapters, journeys).title, "Cugnot");
  const gap = storyForYear(1770, chapters, journeys);
  assert.equal(gap.coverageState, "editorial-gap");
  assert.match(gap.copy, /sem deslocar.*1769/);
});
