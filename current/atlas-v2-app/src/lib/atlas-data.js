const cache = new Map();

export function publicUrl(path, base = import.meta.env.BASE_URL) {
  const clean = path.startsWith("/") ? path.slice(1) : path;
  return `${base}${clean}`;
}

export function loadBundle(path) {
  if (!cache.has(path)) {
    cache.set(path, fetch(publicUrl(`data/v2/${path}`)).then((response) => {
      if (!response.ok) throw new Error(`Falha ao carregar ${path}: ${response.status}`);
      return response.json();
    }).catch((error) => {
      cache.delete(path);
      throw error;
    }));
  }
  return cache.get(path);
}

export function normalizeSearch(value) {
  return String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
}

export function searchEntities(items, query, year, limit = 18) {
  const needle = normalizeSearch(query);
  if (!needle) return [];
  return items.filter((item) => {
    // Undated identities stay discoverable, but the UI labels them as "s/d"
    // and must not place them inside the selected historical horizon.
    const temporal = item.yearStart == null || item.yearStart <= year;
    const haystack = normalizeSearch([item.name, ...(item.aliases || []), item.type, item.description, item.region].join(" "));
    return temporal && haystack.includes(needle);
  }).slice(0, limit);
}

export function periodForYear(year) {
  if (year <= 1885) return "1769-1885";
  if (year <= 1918) return "1886-1918";
  if (year <= 1939) return "1919-1939";
  if (year <= 1959) return "1940-1959";
  if (year <= 1979) return "1960-1979";
  if (year <= 1999) return "1980-1999";
  if (year <= 2009) return "2000-2009";
  if (year <= 2019) return "2010-2019";
  return "2020-2026";
}

export function yearUrl(year, base = import.meta.env.BASE_URL) {
  return `${base}${year}/`;
}

export function storyForYear(year, annualChapters, journeys) {
  const exact = annualChapters.find((item) => item.year === year) || journeys.find((item) => item.year === year);
  if (exact) return exact;
  const dated = [...annualChapters, ...journeys];
  const context = dated.length
    ? dated.reduce((best, item) => Math.abs(item.year - year) < Math.abs(best.year - year) ? item : best, dated[0])
    : { year: "ainda não determinado" };
  return {
    year,
    label: `Contexto de ${year}`,
    eyebrow: "Capítulo em pesquisa",
    title: "Um intervalo ainda está sendo documentado",
    copy: `Ainda não há um marco anual aprovado para ${year}. O Atlas preserva a continuidade do período sem deslocar para este ano uma história ocorrida em ${context.year}.`,
    place: "Acervo em revisão",
    asset: "/assets/people-industry.webp",
    claims: [], sources: [], record: null, coverageState: "editorial-gap",
  };
}
