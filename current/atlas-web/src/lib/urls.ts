const normalizedBase = import.meta.env.BASE_URL.endsWith('/')
  ? import.meta.env.BASE_URL
  : `${import.meta.env.BASE_URL}/`;

export const baseUrl = normalizedBase;

export function withBase(path = ''): string {
  return `${normalizedBase}${path.replace(/^\/+/, '')}`;
}
