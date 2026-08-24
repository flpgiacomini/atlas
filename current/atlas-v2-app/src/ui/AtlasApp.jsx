import { useEffect, useMemo, useRef, useState } from "react";
import { loadBundle, periodForYear, publicUrl, searchEntities, storyForYear, yearUrl } from "../lib/atlas-data.js";
import SpecializedView from "./SpecializedView.jsx";

const MODES = ["História", "Mapa/Globo", "Marcas", "Veículos", "Competições", "Tecnologias"];
const CATEGORY = { Marcas: "brand", Veículos: "vehicle", Competições: "series", Tecnologias: "technology" };
const LAYERS = ["Narrativa", "Cronologia", "Relações", "Mídia", "Fontes"];
const FALLBACK = { year: 1969, label: "Atlas v2", eyebrow: "Acervo em carregamento", title: "A história está sendo conectada", copy: "Preparando documentos, fontes e relações.", place: "Atlas", asset: "/assets/porsche-917-1969-hero.png", claims: [], sources: [], coverageState: "loading" };

function objectText(object) {
  if (typeof object === "string" || typeof object === "number") return String(object);
  if (object?.type === "EntityReference") return object.id;
  if (object?.value != null) return `${object.value}${object.unit ? ` ${object.unit}` : ""}`;
  return "Relação documentada";
}

function ChapterLayer({ layer, story, year }) {
  if (layer === "Cronologia") return <div className="chapter-body"><div><strong>{story.claims?.length || 0} afirmações conectadas</strong>{story.claims?.map((claim) => <p key={claim.id}>{claim.validity?.from || year} · {objectText(claim.object)}</p>)}</div></div>;
  if (layer === "Relações") return <div className="chapter-body"><p><strong>{story.record?.name || story.label}</strong> · {story.record?.type || "Story"}<br />{story.record?.claimCount || 0} claims · {story.record?.sourceCount || story.sources?.length || 0} fontes</p><blockquote>{story.record?.id || "atlas:story:editorial"}</blockquote></div>;
  if (layer === "Mídia") return <div className="chapter-body media-layer">{story.media?.length ? story.media.map((item) => <figure key={item.id}><img src={publicUrl(item.file)} alt={item.alt} /><figcaption>{item.credit} · <a href={item.licenseUrl} target="_blank" rel="noreferrer">{item.license}</a>{item.historicalDocument ? " · documento histórico" : " · apresentação ilustrativa"}</figcaption></figure>) : <p>Este percurso ainda não possui mídia licenciada no manifesto editorial.</p>}</div>;
  if (layer === "Fontes") return <div className="chapter-body"><div><strong>Fontes recuperáveis</strong>{story.sources?.length ? story.sources.map((source) => <p key={source.id}><a href={source.url} target="_blank" rel="noreferrer">{source.title}</a><br /><small>{source.publisher || source.trust}</small></p>) : <p>Nenhuma fonte disponível neste recorte.</p>}</div></div>;
  return <div className="chapter-body"><p>{story.copy}</p><blockquote>“{story.place}” funciona como ponto de partida para conectar pessoas, indústria, técnica e competição dentro do conhecimento disponível em {year}.</blockquote></div>;
}

export default function AtlasApp({ initialYear }) {
  const [year, setYearState] = useState(initialYear);
  const [mode, setMode] = useState("História");
  const [mapKind, setMapKind] = useState("Mapa");
  const [journeys, setJourneys] = useState([]);
  const [annualChapters, setAnnualChapters] = useState([]);
  const [manifest, setManifest] = useState(null);
  const [periodItems, setPeriodItems] = useState([]);
  const [modeItems, setModeItems] = useState([]);
  const [brandMilestones, setBrandMilestones] = useState([]);
  const [brandRelations, setBrandRelations] = useState([]);
  const [loadState, setLoadState] = useState("loading");
  const [chapterOpen, setChapterOpen] = useState(false);
  const [layer, setLayer] = useState("Narrativa");
  const [discoverOpen, setDiscoverOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [searchIndex, setSearchIndex] = useState([]);
  const searchInput = useRef(null);

  const story = useMemo(() => annualChapters.length || journeys.length ? storyForYear(year, annualChapters, journeys) : FALLBACK, [year, annualChapters, journeys]);
  const results = useMemo(() => searchEntities(searchIndex, query, year), [searchIndex, query, year]);

  const setYear = (next, { history = "push" } = {}) => {
    const safe = Math.max(1769, Math.min(2026, Number(next)));
    setYearState(safe);
    if (typeof window !== "undefined" && history !== "none") window.history[history === "replace" ? "replaceState" : "pushState"]({ year: safe }, "", yearUrl(safe));
  };

  useEffect(() => {
    Promise.all([loadBundle("manifest.json"), loadBundle("journeys.json"), loadBundle("annual-chapters.json")])
      .then(([manifestDoc, journeyDoc, annualDoc]) => { setManifest(manifestDoc); setJourneys(journeyDoc.items); setAnnualChapters(annualDoc.items); setLoadState("ready"); })
      .catch(() => setLoadState("error"));
    const pop = (event) => {
      const match = window.location.pathname.match(/\/(\d{4})\/?$/);
      setYearState(event.state?.year || Number(match?.[1]) || 1969);
    };
    window.addEventListener("popstate", pop);
    return () => window.removeEventListener("popstate", pop);
  }, []);

  useEffect(() => {
    loadBundle(`periods/${periodForYear(year)}.json`).then((doc) => setPeriodItems(doc.items)).catch(() => setPeriodItems([]));
  }, [year]);

  useEffect(() => {
    const category = CATEGORY[mode];
    if (!category) { setModeItems([]); return; }
    loadBundle(`categories/${category}.json`).then((doc) => setModeItems(doc.items)).catch(() => setModeItems([]));
    if (mode === "Marcas" && !brandMilestones.length) loadBundle("brand-timeline.json").then((doc) => setBrandMilestones(doc.items)).catch(() => setBrandMilestones([]));
    if (mode === "Marcas" && !brandRelations.length) loadBundle("brand-relations.json").then((doc) => setBrandRelations(doc.items)).catch(() => setBrandRelations([]));
  }, [mode]);

  useEffect(() => {
    if (!searchOpen || searchIndex.length) return;
    loadBundle("index.json").then((doc) => setSearchIndex(doc.items)).catch(() => setLoadState("error"));
  }, [searchOpen, searchIndex.length]);

  useEffect(() => {
    if (searchOpen) searchInput.current?.focus();
  }, [searchOpen]);

  useEffect(() => {
    const keydown = (event) => {
      const target = event.target;
      const isInteractive = target instanceof HTMLElement && Boolean(target.closest("input, textarea, select, button, [contenteditable='true']"));
      if (event.key === "Escape") { setChapterOpen(false); setDiscoverOpen(false); setSearchOpen(false); }
      if (!isInteractive && !chapterOpen && !discoverOpen && !searchOpen && event.key === "ArrowLeft") setYear(year - 1);
      if (!isInteractive && !chapterOpen && !discoverOpen && !searchOpen && event.key === "ArrowRight") setYear(year + 1);
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") { event.preventDefault(); setSearchOpen(true); }
    };
    window.addEventListener("keydown", keydown);
    return () => window.removeEventListener("keydown", keydown);
  }, [year, chapterOpen, discoverOpen, searchOpen]);

  const timelineJourneys = journeys.map((item) => ({ year: item.year, label: item.label.replace("Porsche ", "").replace("Ford ", "") }));
  const milestones = [{ year: 1769, label: "Cugnot" }, ...timelineJourneys, { year: 1997, label: "Prius" }, { year: 2026, label: "Agora" }].sort((a, b) => a.year - b.year);

  return <main className="atlas-shell" style={{ "--hero": `url('${publicUrl(story.asset)}')` }}>
    <header className="masthead">
      <button className="brand" onClick={() => setYear(1969)} aria-label="Voltar ao prólogo do Atlas"><span className="brand-name">ATLAS <i>v2</i></span><span className="brand-subtitle">HISTÓRIA INTERATIVA DO AUTOMÓVEL</span></button>
      <nav aria-label="Modos de visualização">{MODES.map((item) => <button key={item} className={mode === item ? "active" : ""} onClick={() => setMode(item)}>{item}</button>)}</nav>
      <div className="header-actions"><button onClick={() => setSearchOpen(true)}>BUSCAR <kbd>⌘K</kbd></button><button onClick={() => setDiscoverOpen(true)}>DESCOBRIR</button></div>
    </header>

    <section className="hero">
      <div className="hero-shade" /><img className="map-trace" src={publicUrl("assets/zuffenhausen-le-mans-map.png")} alt="" />
      <article className="story-copy" aria-live="polite"><p className="story-year">{year}</p><div className="ornament" /><p className="eyebrow">{story.eyebrow}</p><h1>{story.title}</h1><p className="dek">{story.copy}</p><div className="story-actions"><button className="primary" onClick={() => { setLayer("Narrativa"); setChapterOpen(true); }}>ABRIR CAPÍTULO {year}</button><button className="secondary" onClick={() => setMode("Mapa/Globo")}>VER NO MAPA HISTÓRICO</button></div></article>
      <div className="map-switch" aria-label="Tipo de visualização geográfica">{["Mapa", "Globo"].map((item) => <button key={item} className={mapKind === item ? "active" : ""} onClick={() => { setMapKind(item); setMode("Mapa/Globo"); }}>{item.toUpperCase()}</button>)}</div>
      {mode !== "História" && <aside className="mode-context"><SpecializedView mode={mode} year={year} modeItems={modeItems} periodItems={periodItems} brandMilestones={brandMilestones} brandRelations={brandRelations} story={story} mapKind={mapKind} /></aside>}
      <div className={`data-state ${loadState}`}>{loadState === "ready" ? `${manifest?.entityCount || 0} entidades · ${periodItems.length} no período` : loadState === "error" ? "Falha ao carregar o acervo" : "Carregando acervo"}</div>
    </section>

    <section className="timeline-panel" aria-label="Linha do tempo de 1769 a 2026" style={{ "--progress": `${((year - 1769) / 257) * 100}%` }}><div className="century-scale" aria-hidden="true"><span>1769</span><span>1850</span><span>1900</span><span>1950</span><span>2000</span><span>2026</span></div><input aria-label="Selecionar ano" type="range" min="1769" max="2026" value={year} onChange={(event) => setYear(event.target.value, { history: "replace" })} /><output>{year}</output><div className="milestone-row">{milestones.map((item) => <button key={`${item.year}-${item.label}`} className={Math.abs(item.year - year) < 2 ? "active" : ""} onClick={() => setYear(item.year)}><strong>{item.year}</strong><span>{item.label}</span></button>)}</div></section>

    {chapterOpen && <div className="modal-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && setChapterOpen(false)}><article className="chapter-modal" role="dialog" aria-modal="true" aria-labelledby="chapter-title"><button className="close" onClick={() => setChapterOpen(false)} aria-label="Fechar capítulo">FECHAR</button><p className="modal-kicker">CAPÍTULO {year} · {story.label} · ACERVO CONECTADO</p><h2 id="chapter-title">{story.title}</h2><p className="lead">{story.copy}</p><div className="chapter-tabs">{LAYERS.map((item) => <button key={item} className={layer === item ? "active" : ""} onClick={() => setLayer(item)}>{item.toUpperCase()}</button>)}</div><ChapterLayer layer={layer} story={story} year={year} /></article></div>}

    {discoverOpen && <div className="modal-backdrop" role="presentation"><section className="discover-panel" role="dialog" aria-modal="true" aria-label="Central de descoberta"><button className="close" onClick={() => setDiscoverOpen(false)}>FECHAR</button><p className="modal-kicker">SEIS PERCURSOS CANÔNICOS</p><h2>Onde a história começa?</h2><div className="journey-list">{journeys.map((item) => <button key={item.entity} onClick={() => { setYear(item.year); setDiscoverOpen(false); }}><span>{item.year}</span><strong>{item.label}</strong><small>{item.eyebrow} · {item.record?.claimCount || 0} claims</small></button>)}</div></section></div>}

    {searchOpen && <div className="modal-backdrop search-backdrop" role="presentation"><section className="search-panel" role="dialog" aria-modal="true" aria-label="Central de busca"><button className="close" onClick={() => setSearchOpen(false)}>FECHAR</button><p className="modal-kicker">DESCOBERTA GLOBAL · CONHECIMENTO ATÉ {year}</p><h2>O que você procura?</h2><input ref={searchInput} type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Marcas, veículos, lugares, tecnologias…" aria-label="Buscar no Atlas" /><div className="search-results" aria-live="polite">{query && !results.length ? <p>Nenhum resultado neste recorte temporal.</p> : results.map((item) => <button key={item.id} onClick={() => { if (item.yearStart) setYear(item.yearStart); setSearchOpen(false); }}><span>{item.yearStart || "s/d"}</span><strong>{item.name}</strong><small>{item.type} · {item.claimCount} claims · {item.region}</small></button>)}</div></section></div>}
  </main>;
}
