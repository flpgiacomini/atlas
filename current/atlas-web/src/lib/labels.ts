const labels: Record<string, string> = {
  vehicle: "Veículo", vehicle_instance: "Exemplar", organization: "Organização",
  brand: "Marca", person: "Pessoa", technology: "Tecnologia", component: "Componente",
  facility: "Instalação", place: "Lugar", competition: "Competição", season: "Temporada",
  team: "Equipe", circuit: "Circuito", circuit_layout: "Traçado", regulation: "Regulamento",
  event: "Evento", entry: "Inscrição", accepted: "aceito", disputed: "disputado",
  unresolved: "não resolvido", needs_reconciliation: "requer conciliação", rejected: "rejeitado",
  high: "alta", medium: "média", low: "baixa", unknown: "desconhecida",
  catalog: "catalogado", editorial: "editorial", dossier: "dossiê",
  editorial_level: "nível editorial", editorial_batch: "lote editorial", catalog_source: "fonte catalográfica",
  region_cluster: "região", wave: "onda", brand_status: "estado da marca", candidate_kind: "categoria candidata",
  candidate_year: "ano candidato", associated_brand: "marca associada", contribution_tracks: "eixos de contribuição",
  relevance_score: "pontuação de relevância", promotion_state: "estado de promoção", queued: "na fila editorial",
  priority_editorial: "prioridade editorial",
  verification_state: "estado de verificação", source_backed: "verificado por fonte",
  verified_at: "verificado em", verification_batch: "lote de verificação",
  waiting_media_and_second_source: "aguardando mídia e segunda fonte",
  marketed_under: "comercializado sob",
};
export function label(value: unknown): string {
  const raw = String(value ?? "");
  return labels[raw] ?? raw.replaceAll("_", " ");
}
export function safeJsonForHtml(value: unknown): string {
  return JSON.stringify(value).replaceAll("<", "\\u003c");
}
