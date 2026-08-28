import { isCatalogOnly } from "../lib/atlas-data.js";

const COMPETITION_PATTERN = /prix|rally|rali|race|racing|le mans|zeltweg|motorsport|championship|corrida|prova/i;
const TECHNOLOGY_PATTERN = /turbo|hybrid|h[ií]brid|electric|el[eé]tric|motor|engine|radar|safety|seguran|aero|battery|bateria|fuel|combust|transmission|tra[cç][aã]o/i;
const RELATION_LABELS = {
  "succeeded-by": "continuidade",
  "market-transition-to": "transição de identidade",
  "acquired-by": "mudança de controle",
  "rights-acquired-by": "direitos da marca",
  "merged-into": "fusão corporativa",
  "renamed-to": "renome",
  "spun-off-to": "cisão",
  "joined-lineage-of": "integração de linhagem",
  "became-subbrand-of": "transformação em submarca",
};

function datedUntil(items, year) {
  return items.filter((item) => item.yearStart != null && item.yearStart <= year)
    .sort((a, b) => b.yearStart - a.yearStart || a.name.localeCompare(b.name, "pt-BR"));
}

function EmptyEvidence({ children }) {
  return <p className="projection-empty">{children}</p>;
}

function AccessibleRecords({ title, items }) {
  return <details className="projection-records"><summary>Resumo textual — {title}</summary>
    {items.length ? <ol>{items.map((item) => <li key={item.id}><strong>{item.yearStart || "sem data"}</strong> — {item.name}</li>)}</ol> : <p>Nenhum registro temporalmente verificável neste recorte.</p>}
  </details>;
}

function BrandRiver({ items, milestones, relations, year }) {
  const catalog = items.filter(isCatalogOnly);
  const regions = [...new Set(catalog.map((item) => item.region))].sort((a, b) => a.localeCompare(b, "pt-BR")).slice(0, 6);
  const names = new Map(items.map((item) => [item.id, item.name]));
  const lifecycle = milestones.filter((item) => item.year <= year);
  const visibleLifecycle = lifecycle.slice(-10);
  const documentedBrands = new Set(milestones.map((item) => item.brand));
  const undocumentedCount = Math.max(0, items.length - documentedBrands.size);
  const evidence = lifecycle.map((item) => ({ ...item, id: item.id, yearStart: item.year, name: `${names.get(item.brand) || item.brand} — ${item.label}` }));
  const activeRelations = relations.filter((item) => Number(item.validFrom.slice(0, 4)) <= year).slice(-6);
  const relationEvidence = activeRelations.map((item) => ({ id: item.id, yearStart: Number(item.validFrom.slice(0, 4)), name: `${item.fromLabel} → ${item.toLabel}: ${item.label}` }));
  return <section className="projection brand-river" aria-labelledby="brand-river-title">
    <header><p>RIO GENEALÓGICO</p><h2 id="brand-river-title">Marcas conhecidas até {year}</h2><span>{lifecycle.length} marcos documentados · exibindo {visibleLifecycle.length} recentes · {items.length - catalog.length} com trabalho editorial · {catalog.length} apenas catalogadas · {undocumentedCount} sem marco</span></header>
    <div className="river-canvas" aria-hidden="true">{regions.map((region, index) => <div className="river-lane" key={region} style={{ "--lane": index }}><i /><span>{region}</span><b>{catalog.filter((item) => item.region === region).length}</b></div>)}</div>
    {visibleLifecycle.length ? <div className="projection-cards">{visibleLifecycle.map((item) => <article key={item.id}><time>{item.year}</time><strong>{names.get(item.brand) || item.brand}</strong><small>{item.label} · {item.scope === "operator" ? "organização operadora" : "identidade da marca"}</small></article>)}</div> : <EmptyEvidence>A genealogia não pode ser desenhada ainda: nenhum marco com fonte ocorre antes deste ano.</EmptyEvidence>}
    {activeRelations.length ? <div className="projection-cards brand-relations" aria-label="Relações corporativas conhecidas"><h3>Conexões corporativas</h3>{activeRelations.map((item) => <article key={item.id} data-kind={item.kind}><time>{item.validFrom.slice(0, 4)} · {RELATION_LABELS[item.kind] || item.kind}</time><strong>{item.fromLabel} → {item.toLabel}</strong><small>{item.label}</small></article>)}</div> : null}
    <AccessibleRecords title="marcas" items={[...evidence, ...relationEvidence]} />
  </section>;
}

function VehicleLineage({ items, year }) {
  const evidence = datedUntil(items, year).slice(0, 10).reverse();
  return <section className="projection vehicle-lineage" aria-labelledby="vehicle-lineage-title">
    <header><p>LINHAGENS DE VEÍCULOS</p><h2 id="vehicle-lineage-title">Evolução documentada até {year}</h2><span>{evidence.length} marcos recentes no horizonte selecionado</span></header>
    {evidence.length ? <div className="lineage-track" aria-hidden="true">{evidence.map((item, index) => <article key={item.id} style={{ "--node": index }}><time>{item.yearStart}</time><strong>{item.name}</strong><small>{item.claimCount} claims</small></article>)}</div> : <EmptyEvidence>Nenhum veículo possui data verificável antes deste ano.</EmptyEvidence>}
    <AccessibleRecords title="linhagens de veículos" items={evidence} />
  </section>;
}

function CompetitionSeason({ items, periodItems, year }) {
  const events = periodItems.filter((item) => item.type === "Event" && item.yearStart <= year && COMPETITION_PATTERN.test(item.name)).sort((a, b) => a.yearStart - b.yearStart).slice(-10);
  return <section className="projection competition-season" aria-labelledby="competition-title">
    <header><p>TEMPORADAS E SÉRIES</p><h2 id="competition-title">Competição no recorte de {year}</h2><span>{events.length} eventos datados · {items.length} séries catalogadas</span></header>
    {events.length ? <div className="season-grid">{events.map((item) => <article key={item.id}><time>{item.yearStart}</time><i /><strong>{item.name}</strong><small>{item.region}</small></article>)}</div> : <EmptyEvidence>Nenhuma etapa ou prova datada foi recuperada neste período.</EmptyEvidence>}
    <AccessibleRecords title="competições" items={events} />
  </section>;
}

function TechnologyFlow({ items, periodItems, year }) {
  const technologies = datedUntil(items, year);
  const events = periodItems.filter((item) => item.yearStart <= year && TECHNOLOGY_PATTERN.test(item.name));
  const evidence = [...technologies, ...events].sort((a, b) => a.yearStart - b.yearStart).slice(-12);
  return <section className="projection technology-flow" aria-labelledby="technology-title">
    <header><p>FLUXOS DE DIFUSÃO</p><h2 id="technology-title">Tecnologias até {year}</h2><span>{evidence.length} marcos recuperados · {items.filter((item) => item.yearStart == null).length} conceitos ainda sem data</span></header>
    {evidence.length ? <div className="flow-canvas" aria-hidden="true">{evidence.map((item, index) => <article key={item.id} className={`flow-${index % 3}`}><time>{item.yearStart}</time><strong>{item.name}</strong></article>)}</div> : <EmptyEvidence>Nenhum marco tecnológico verificável foi recuperado neste horizonte.</EmptyEvidence>}
    <AccessibleRecords title="difusão tecnológica" items={evidence} />
  </section>;
}

export default function SpecializedView({ mode, year, modeItems, periodItems, brandMilestones, brandRelations, story, mapKind, geographyFeatures }) {
  if (mode === "Marcas") return <BrandRiver items={modeItems} milestones={brandMilestones} relations={brandRelations} year={year} />;
  if (mode === "Veículos") return <VehicleLineage items={modeItems} year={year} />;
  if (mode === "Competições") return <CompetitionSeason items={modeItems} periodItems={periodItems} year={year} />;
  if (mode === "Tecnologias") return <TechnologyFlow items={modeItems} periodItems={periodItems} year={year} />;
  return <GeographicView mapKind={mapKind} story={story} year={year} features={geographyFeatures} />;
}
import GeographicView from "./GeographicView.jsx";
