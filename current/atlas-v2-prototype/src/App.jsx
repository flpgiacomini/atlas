import { useEffect, useMemo, useState } from "react";

const journeys = [
  { year: 1886, label: "Benz Patent-Motorwagen", eyebrow: "A origem documentada", title: "A máquina aprende a caminhar", copy: "Em Mannheim, patente, oficina e demonstração pública se unem para transformar uma experiência mecânica em um novo meio de transporte.", place: "Mannheim", asset: "/assets/geography.webp" },
  { year: 1908, label: "Ford Model T", eyebrow: "Escala e mobilidade", title: "O automóvel encontra a multidão", copy: "O Model T reorganiza produto, fábrica e preço. O automóvel deixa de ser exceção e passa a redesenhar trabalho, cidade e distância.", place: "Detroit", asset: "/assets/people-industry.webp" },
  { year: 1955, label: "Origens do Motorsport", eyebrow: "Inovação e consequência", title: "Um ano, duas verdades", copy: "A técnica encanta nas ruas e cobra seu preço nas pistas. Desempenho e segurança passam a pertencer à mesma história.", place: "Paris · Le Mans", asset: "/assets/motorsport.webp" },
  { year: 1958, label: "Volvo PV544", eyebrow: "Segurança em série", title: "Proteger também é avançar", copy: "A Volvo transforma pesquisa de segurança em equipamento cotidiano e ajuda a redefinir o que significa progresso no automóvel.", place: "Gotemburgo", asset: "/assets/technology.webp" },
  { year: 1963, label: "Porsche 911", eyebrow: "Uma forma persistente", title: "A linhagem encontra sua identidade", copy: "Motor traseiro, silhueta precisa e evolução contínua criam uma família capaz de atravessar décadas sem perder sua origem.", place: "Zuffenhausen", asset: "/assets/vehicles.webp" },
  { year: 1969, label: "Porsche 917", eyebrow: "Ambição e resistência", title: "A velocidade encontra uma nova forma", copy: "O Porsche 917 transforma ambição, aerodinâmica e resistência em uma nova linguagem para o automobilismo.", place: "Zuffenhausen · Le Mans", asset: "/assets/porsche-917-1969-hero.png" },
];

const milestones = [
  { year: 1769, label: "Cugnot" }, { year: 1886, label: "Benz" }, { year: 1908, label: "Model T" },
  { year: 1955, label: "DS · Le Mans" }, { year: 1958, label: "PV544" }, { year: 1963, label: "911" },
  { year: 1969, label: "917" }, { year: 1997, label: "Prius" }, { year: 2026, label: "Agora" },
];

const modes = ["História", "Mapa/Globo", "Marcas", "Veículos", "Competições", "Tecnologias"];

function nearestJourney(year) {
  return journeys.reduce((best, item) => Math.abs(item.year - year) < Math.abs(best.year - year) ? item : best, journeys[0]);
}

export function App() {
  const [year, setYear] = useState(1969);
  const [mode, setMode] = useState("História");
  const [mapKind, setMapKind] = useState("Mapa");
  const [chapterOpen, setChapterOpen] = useState(false);
  const [discoverOpen, setDiscoverOpen] = useState(false);
  const story = useMemo(() => nearestJourney(year), [year]);

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
    <main className="atlas-shell" style={{ "--hero": `url('${story.asset}')` }}>
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
        <img className="map-trace" src="/assets/zuffenhausen-le-mans-map.png" alt="" />
        <article className="story-copy" aria-live="polite">
          <p className="story-year">{year}</p>
          <div className="ornament" />
          <p className="eyebrow">{story.eyebrow}</p>
          <h1>{story.title}</h1>
          <p className="dek">{story.copy}</p>
          <div className="story-actions">
            <button className="primary" onClick={() => setChapterOpen(true)}>ABRIR CAPÍTULO {year}</button>
            <button className="secondary" onClick={() => setMode("Mapa/Globo")}>VER NO MAPA HISTÓRICO</button>
          </div>
        </article>

        <div className="map-switch" aria-label="Tipo de visualização geográfica">
          {['Mapa', 'Globo'].map((item) => <button key={item} className={mapKind === item ? "active" : ""} onClick={() => { setMapKind(item); setMode("Mapa/Globo"); }}>{item.toUpperCase()}</button>)}
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
          {milestones.map((item) => <button key={item.year} className={Math.abs(item.year - year) < 2 ? "active" : ""} onClick={() => setYear(item.year)}><strong>{item.year}</strong><span>{item.label}</span></button>)}
        </div>
      </section>

      {chapterOpen && (
        <div className="modal-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && setChapterOpen(false)}>
          <article className="chapter-modal" role="dialog" aria-modal="true" aria-labelledby="chapter-title">
            <button className="close" onClick={() => setChapterOpen(false)} aria-label="Fechar capítulo">FECHAR</button>
            <p className="modal-kicker">CAPÍTULO {year} · {story.label}</p>
            <h2 id="chapter-title">{story.title}</h2>
            <p className="lead">{story.copy}</p>
            <div className="chapter-tabs"><button className="active">NARRATIVA</button><button>CRONOLOGIA</button><button>RELAÇÕES</button><button>FONTES</button></div>
            <div className="chapter-body">
              <p>Este protótipo demonstra a leitura em camadas: contexto editorial primeiro, entidades e evidências a seguir. Tudo permanece limitado ao conhecimento disponível em {year}.</p>
              <blockquote>“{story.place}” torna-se um ponto de partida para compreender pessoas, técnica, indústria e competição como partes da mesma história.</blockquote>
            </div>
          </article>
        </div>
      )}

      {discoverOpen && (
        <div className="modal-backdrop discover" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && setDiscoverOpen(false)}>
          <section className="discover-panel" role="dialog" aria-modal="true" aria-label="Central de descoberta">
            <button className="close" onClick={() => setDiscoverOpen(false)}>FECHAR</button>
            <p className="modal-kicker">SEIS PERCURSOS DO PROTÓTIPO</p>
            <h2>Onde a história começa?</h2>
            <div className="journey-list">{journeys.map((item) => <button key={item.label} onClick={() => chooseJourney(item)}><span>{item.year}</span><strong>{item.label}</strong><small>{item.eyebrow}</small></button>)}</div>
          </section>
        </div>
      )}
    </main>
  );
}
