import pages from "../data/generated/entity-pages.json";
const site = "https://flpgiacomini.github.io/atlas/";
export function GET() {
  const routes = ["", "brands/", "timeline/", "graph/", "map/", "compare/", ...pages.map((page:any) => `e/${page.id}/`)];
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${routes.map(route => `<url><loc>${site}${route}</loc></url>`).join("")}</urlset>`;
  return new Response(body, { headers: { "Content-Type": "application/xml" } });
}
