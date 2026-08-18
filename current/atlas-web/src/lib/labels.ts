const labels: Record<string, string> = {
  vehicle: "Veículo", vehicle_instance: "Exemplar", organization: "Organização",
  brand: "Marca", person: "Pessoa", technology: "Tecnologia", component: "Componente",
  facility: "Instalação", place: "Lugar", competition: "Competição", season: "Temporada",
  team: "Equipe", circuit: "Circuito", circuit_layout: "Traçado", regulation: "Regulamento",
  event: "Evento", entry: "Inscrição", accepted: "aceito", disputed: "disputado",
  unresolved: "não resolvido", needs_reconciliation: "requer conciliação", rejected: "rejeitado",
  high: "alta", medium: "média", low: "baixa", unknown: "desconhecida",
};
export function label(value: unknown): string {
  const raw = String(value ?? "");
  return labels[raw] ?? raw.replaceAll("_", " ");
}
export function safeJsonForHtml(value: unknown): string {
  return JSON.stringify(value).replaceAll("<", "\\u003c");
}
