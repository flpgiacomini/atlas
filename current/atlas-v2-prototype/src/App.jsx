import { useEffect, useMemo, useState } from "react";

const fallbackStory = {
  year: 1969,
  label: "Carregando o acervo",
  eyebrow: "Documentos canônicos v2",
  title: "A história está sendo conectada",
  copy: "O Atlas prepara o capítulo, suas relações e evidências.",
  place: "Atlas",
  asset: "/assets/porsche-917-1969-hero.png",
  claims: [],
  sources: [],
  coverageState: "loading",
};

const fixedMilestones = [
  { year: 1769, label: "Cugnot" },
  { year: 1997, label: "Prius" },
  { year: 2026, label: "Agora" },
];
const modes = ["História", "Mapa/Globo", "Marcas", "Veículos", "Competições", "Tecnologias"];
const chapterLayers = ["Narrativa", "Cronologia", "Relações", "Fontes"];

function publicUrl(path) {
  const clean = path.startsWith("/") ? path.slice(1) : path;
  return `${import.meta.env.BASE_URL}${clean}`;
}

function nearestJourney(year, journeys) {
  if (!journeys.length) return fallbackStory;
  return journeys.reduce((best, item) => Math.abs(item.year - year) < Math.abs(best.year - year) ? item : best, journeys[0]);
}

function claimText(claim) {
  const object = claim.object;
  if (typeof object === "string" || typeof object === "number") return String(object);
  if (object?.type === "EntityReference") return object.id;
  if (object?.value !== undefined) return `${object.value}${object.unit ? ` ${object.unit}` : ""}`;
  return "Relação documentada no acervo";
}

function ChapterContent({ layer, story, year }) {
  if (layer === "Cronologia") {
    return <div className="chapter-body"><div><p><strong>{story.claims.length} afirmações conectadas</strong></p>{story.claims.length ? story.claims.map((claim) => <p key={claim.id}>{claim.validity?.from || year} · {claimText(claim)}</p>) : <p>O capítulo ainda não possui claims temporais suficientes.</p>}</div></div>;
  }
  if (layer === "Relações") {
    return <div className="chapter-body"><p><strong>{story.record?.name || story.label}</strong> está registrado como {story.record?.type || "história editorial"}, com {story.record?.claimCount || 0} claims e {story.record?.sourceCount || story.sources.length} fontes distintas.</p><blockquote>{story.record?.id || "Conexão editorial em revisão"}</blockquote></div>;
  }
  if (layer === "Fontes") {
    return <div className="chapter-body"><div><p><strong>Fontes recuperáveis</strong></p>{story.sources.length ? story.sources.map((source) => <p key={source.id}><a href={source.url} target="_blank" rel="noreferrer">{source.title}</a><br /><small>{source.publisher || source.trust}</small></p>) : <p>Nenhuma fonte publicada neste recorte.</p>}</div></div>;
  }
  return <div className="chapter-body"><p>Este capítulo combina contexto editorial com os documentos canônicos disponíveis até {year}. A camada carregada registra a entidade, suas afirmações e as evidências recuperáveis.</p><blockquote>“{story.place}” conecta pessoas, técnica, indústria e competição como partes da mesma história.</blockquote></div>;
}

export function App() {
  const [year, setYear] = useState(1969);
  const [mode, setMode] = useState("História");
  const [mapKind, setMapKind] = useState("Mapa");
  const [chapterOpen, setChapterOpen] = useState(false);
  const [chapterLayer, setChapterLayer] = useState("Narrativa");
  const [discoverOpen, setDiscoverOpen] = useState(false);
  const [journeys, setJourneys] = useState([]);
  const [bundleState, setBundleState] = useState("loading");

  useEffect(() => {
    const controller = new AbortController();
    fetch(publicUrl("data/v2/journeys.json"), { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`Bundle ${response.status}`);
        return response.json();
      })
      .then((payload) => {
        setJourneys(payload.items);
        setBundleState(payload.items.every((item) => item.coverageState === "connected") ? "connected" : "partial");
      })
      .catch((error) => {
        if (error.name !== "AbortError") setBundleState("error");
      });
    return () => controller.abort();
  }, []);

  const story = useMemo(() => nearestJourney(year, journeys), [year, journeys]);
  const milestones = useMemo(() => [...fixedMilestones, ...journeys.map(({ year: itemYear, label }) => ({ year: itemYear, label: label.replace("Porsche ", "").replace("Ford ", "") }))].sort((a, b) => a.year - b.year), [journeys]);

  useEffect(() => {
    const onKey = (event) => {
      if (event.key === "Escape") { setChapterOpen(false); setDiscoverOpen(false); }
      if (!chapterOpen && !discoverOpen && event.key === "ArrowLeft") setYear((value) => Math.max(1769, value - 1));
      if (!chapterOpen && !discoverOpen && event.key === "ArrowRight") setYear((value) => Math.min(2026, value + 1));
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [chapterOpen, discoverOpen]);

  const chooseJourney = (item) => {
    setYear(item.year);
    setMode("História");
    setDiscoverOpen(false);
  };

  return (
    <main className="atlas-shell" style={{ "--hero": `url('${publicUrl(story.asset)}')` }}>
      <header className="masthead">
        <button className="brand" onClick={() => { setYear(1969); setMode("História"); }} aria-label="Voltar ao prólogo do Atlas">
          <span className="brand-name">ATLAS <i>v2</i></span>
          <span className="brand-subtitle">HISTÓRIA INTERATIVA DO AUTOMÓVEL</span>
        </button>
        <nav aria-label="Modos de visualização">
          {modes.map((item) => <button key={item} className={mode === item ? "active" : ""} onClick={() => setMode(item)}>{item}</button>)}
        </nav>
        <button className="discover-trigger" onClick={() => setDiscoverOpen(true)}>DESCOBRIR</button>
      </header>

      <section className={`hero mode-${mode.replace("/", "-").toLowerCase()}`}>
        <div className="hero-shade" />
        <img className="map-trace" src={publicUrl("assets/zuffenhausen-le-mans-map.png")} alt="" />
        <article className="story-copy" aria-live="polite">
          <p className="story-year">{year}</p>
          <div className="ornament" />
          <p className="eyebrow">{story.eyebrow}</p>
          <h1>{story.title}</h1>
          <p className="dek">{story.copy}</p>
          <div className="story-actions">
            <button className="primary" onClick={() => { setChapterLayer("Narrativa"); setChapterOpen(true); }}>ABRIR CAPÍTULO {year}</button>
            <button className="secondary" onClick={() => setMode("Mapa/Globo")}>VER NO MAPA HISTÓRICO</button>
          </div>
        </article>

        <div className="map-switch" aria-label="Tipo de visualização geográfica">
          {["Mapa", "Globo"].map((item) => <button key={item} className={mapKind === item ? "active" : ""} onClick={() => { setMapKind(item); setMode("Mapa/Globo"); }}>{item.toUpperCase()}</button>)}
        </div>

        {mode !== "História" && (
          <aside className="mode-context">
            <p>{mode}</p>
            <h2>{mode === "Mapa/Globo" ? `${mapKind} histórico · ${year}` : `${mode} em ${year}`}</h2>
            <span>{mode === "Mapa/Globo" ? `Roteiro editorial: ${story.place}.` : "A visualização permanece sincronizada com a linha do tempo."}</span>
          </aside>
        )}
      </section>

      <section className="timeline-panel" aria-label="Linha do tempo de 1769 a 2026" style={{ "--progress": `${((year - 1769) / 257) * 100}%` }}>
        <div className="century-scale" aria-hidden="true"><span>1769</span><span>1850</span><span>1900</span><span>1950</span><span>2000</span><span>2026</span></div>
        <input aria-label="Selecionar ano" type="range" min="1769" max="2026" value={year} onChange={(event) => setYear(Number(event.target.value))} />
        <output>{year}</output>
        <div className="milestone-row">
          {milestones.map((item) => <button key={`${item.year}-${item.label}`} className={Math.abs(item.year - year) < 2 ? "active" : ""} onClick={() => setYear(item.year)}><strong>{item.year}</strong><span>{item.label}</span></button>)}
        </div>
      </section>

      {chapterOpen && (
        <div className="modal-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && setChapterOpen(false)}>
          <article className="chapter-modal" role="dialog" aria-modal="true" aria-labelledby="chapter-title">
            <button className="close" onClick={() => setChapterOpen(false)} aria-label="Fechar capítulo">FECHAR</button>
            <p className="modal-kicker">CAPÍTULO {year} · {story.label} · ACERVO {bundleState === "connected" ? "CONECTADO" : bundleState.toUpperCase()}</p>
            <h2 id="chapter-title">{story.title}</h2>
            <p className="lead">{story.copy}</p>
            <div className="chapter-tabs">{chapterLayers.map((layer) => <button key={layer} className={chapterLayer === layer ? "active" : ""} onClick={() => setChapterLayer(layer)}>{layer.toUpperCase()}</button>)}</div>
            <ChapterContent layer={chapterLayer} story={story} year={year} />
          </article>
        </div>
      )}

      {discoverOpen && (
        <div className="modal-backdrop discover" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && setDiscoverOpen(false)}>
          <section className="discover-panel" role="dialog" aria-modal="true" aria-label="Central de descoberta">
            <button className="close" onClick={() => setDiscoverOpen(false)}>FECHAR</button>
            <p className="modal-kicker">SEIS PERCURSOS · DADOS CANÔNICOS V2</p>
            <h2>Onde a história começa?</h2>
            {bundleState === "error" ? <p role="alert">Não foi possível carregar o acervo. Tente novamente após atualizar a página.</p> : <div className="journey-list">{journeys.map((item) => <button key={item.label} onClick={() => chooseJourney(item)}><span>{item.year}</span><strong>{item.label}</strong><small>{item.eyebrow} · {item.record?.claimCount || 0} claims</small></button>)}</div>}
          </section>
        </div>
      )}
    </main>
  );
}
