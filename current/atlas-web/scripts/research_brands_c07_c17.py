#!/usr/bin/env python3
"""Resolve C07-C17 brand identities against individual Wikipedia/Wikidata records.

The output is a versioned research snapshot. Automatic acceptance requires an
automotive signal in the introduction or categories; ambiguous matches remain
explicitly unresolved and are never guessed.
"""

from __future__ import annotations

import json
import hashlib
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT.parent / "atlas-v2"
TARGET = ROOT / "data" / "imports" / "atlas-curation" / "brands-c07-c17.research.json"
API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "AtlasProject/2.0 (https://github.com/flpgiacomini/atlas)"
AUTOMOTIVE = re.compile(
    r"\b(automotive|automobile|automaker|car|cars|vehicle|vehicles|motor vehicle|"
    r"motor company|motorcycle|truck|coachbuilder|marque)\b", re.I
)
KNOWN_BAD_MATCHES = {
    ("ATS", "ATS Euromaster"), ("Aero", "Saab Aero"),
    ("Hyundai", "Hyundai Automotive South Africa"), ("Princess", "Little Princess (automobile)"),
    ("Star", "Red Star Auto"), ("Tesla", "Tesla US dealership disputes"),
}
TITLE_OVERRIDES = {
    "Aero": "Aero (automobile)", "Morris": "Morris Motors", "Singer": "Singer Motors",
    "Standard": "Standard Motor Company", "Triumph": "Triumph Motor Company",
    "AMC": "American Motors Corporation", "Avanti": "Avanti (car)", "Eagle": "Eagle (automobile)",
    "Hudson": "Hudson Motor Car Company", "Imperial": "Imperial (automobile)", "Karma": "Karma Automotive",
    "Lordstown": "Lordstown Motors", "Lucid": "Lucid Motors", "Tesla": "Tesla, Inc.",
    "ATS": "Automobili Turismo e Sport", "Ermini": "Ermini (car manufacturer)",
    "Giannini": "Giannini Automobili", "OM": "Officine Meccaniche", "OSCA": "O.S.C.A.",
    "Serenissima": "Scuderia Serenissima", "AC": "AC Cars", "Arrival": "Arrival (company)",
    "BAC": "Briggs Automotive Company", "Bond": "Bond Cars", "Caterham": "Caterham Cars",
    "Daimler (British marque)": "Daimler Company", "Healey": "Donald Healey Motor Company",
    "Panther": "Panther Westwinds", "Princess": "Princess (car)", "Radical": "Radical Motorsport",
    "Turner": "Turner Sports Cars", "Warwick": "Warwick (car)", "Buddy": "Buddy (electric car)",
    "Dome": "Dome (constructor)", "Eunos": "Eunos", "Hino": "Hino Motors",
    "Mitsubishi": "Mitsubishi Motors", "Tama": "Tama (electric car)", "Aito": "AITO (marque)",
    "Avatr": "Avatr Technology", "Brilliance": "Brilliance Auto", "Dongfeng": "Dongfeng Motor Corporation",
    "Genesis": "Genesis Motor", "KGM": "KG Mobility", "Ora": "Ora (marque)",
    "Skywell": "Skywell (marque)", "Bajaj": "Bajaj Auto", "Pravaig": "Pravaig Dynamics",
    "Premier": "Premier Automobiles", "Reva": "REVA", "VinFast": "VinFast",
    "Avia": "Avia Motors", "FSO": "Fabryka Samochodów Osobowych", "IZh": "Izh (vehicle brand)",
    "Zastava": "Zastava Automobiles", "Burton": "Burton Car Company", "DAF": "DAF Trucks",
    "Imperia": "Impéria Automobiles", "Santana": "Santana Motor", "Think": "Think Global",
    "Tramontana": "Tramontana (sports car)", "UMM": "UMM (company)", "Brasinca": "Brasinca",
    "FNM": "Fábrica Nacional de Motores", "Hofstetter": "Hofstetter Turbo",
    "IKA": "Industrias Kaiser Argentina", "Justicialista": "IAME Justicialista",
    "Miura": "Miura (Brazilian automobile)", "Vemag": "Vemag", "FPV": "Ford Performance Vehicles",
    "GSM": "GSM (car)", "HSV": "Holden Special Vehicles", "Hartnett": "Hartnett (car)",
    "Lightburn": "Lightburn Zeta", "Optimal Energy": "Optimal Energy Joule", "Purvis": "Purvis Eureka",
}


def request(params: dict, attempts: int = 5) -> dict:
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.load(response)
        except Exception:
            if attempt == attempts - 1:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


def automotive(page: dict) -> bool:
    if "disambiguation" in page.get("pageprops", {}):
        return False
    text = " ".join([page.get("title", ""), page.get("extract", "")]
                    + [item.get("title", "") for item in page.get("categories", [])])
    return bool(AUTOMOTIVE.search(text))


def direct(names: list[str]) -> tuple[dict[str, dict], list[str]]:
    accepted: dict[str, dict] = {}
    retry: list[str] = []
    for start in range(0, len(names), 40):
        chunk = names[start:start + 40]
        data = request({
            "action": "query", "format": "json", "formatversion": "2", "redirects": "1",
            "prop": "extracts|pageprops|categories|revisions", "rvprop": "ids|timestamp",
            "cllimit": "max", "exintro": "1", "explaintext": "1", "titles": "|".join(chunk),
        })
        query = data.get("query", {})
        normalized = {item["from"]: item["to"] for item in query.get("normalized", [])}
        redirects = {item["from"]: item["to"] for item in query.get("redirects", [])}
        pages = {item["title"]: item for item in query.get("pages", [])}
        for name in chunk:
            title = normalized.get(name, name)
            title = redirects.get(title, title)
            page = pages.get(title)
            if page and "missing" not in page and automotive(page):
                accepted[name] = page
            else:
                retry.append(name)
        time.sleep(0.35)
    return accepted, retry


def overrides(names: list[str]) -> dict[str, dict]:
    candidates = {name: TITLE_OVERRIDES[name] for name in names if name in TITLE_OVERRIDES}
    accepted = {}
    pairs = list(candidates.items())
    for start in range(0, len(pairs), 40):
        chunk = pairs[start:start + 40]
        data = request({
            "action": "query", "format": "json", "formatversion": "2", "redirects": "1",
            "prop": "extracts|pageprops|categories|revisions", "rvprop": "ids|timestamp", "cllimit": "max",
            "exintro": "1", "explaintext": "1", "titles": "|".join(title for _, title in chunk),
        })
        query = data.get("query", {})
        redirects = {item["from"]: item["to"] for item in query.get("redirects", [])}
        pages = {item["title"]: item for item in query.get("pages", [])}
        for name, title in chunk:
            page = pages.get(redirects.get(title, title))
            if page and "missing" not in page and automotive(page):
                accepted[name] = page
        time.sleep(0.35)
    return accepted


def search_one(name: str) -> tuple[str, dict | None]:
    try:
        data = request({
            "action": "query", "format": "json", "formatversion": "2", "generator": "search",
            "gsrsearch": f'"{name}" automobile manufacturer', "gsrnamespace": "0", "gsrlimit": "5",
            "prop": "extracts|pageprops|categories|revisions", "rvprop": "ids|timestamp",
            "cllimit": "max", "exintro": "1", "explaintext": "1",
        })
    except Exception:
        return name, None
    pages = data.get("query", {}).get("pages", [])
    tokens = set(re.findall(r"[a-z0-9]+", name.casefold())) - {"automobiles", "automotive", "cars", "car", "motors", "motor", "marque"}
    def name_match(page: dict) -> bool:
        title_tokens = set(re.findall(r"[a-z0-9]+", page.get("title", "").casefold()))
        found = tokens & title_tokens
        named = bool(tokens) and len(found) / len(tokens) >= (1.0 if len(tokens) == 1 else 0.5)
        categories = " ".join(item.get("title", "") for item in page.get("categories", []))
        category_signal = re.search(r"(car brands|car manufacturers|motor vehicle manufacturers|automobile manufacturers|coachbuilders)", categories, re.I)
        first = (page.get("extract") or "").split("\n", 1)[0]
        intro_signal = re.search(r"\b(manufacturer|automaker|automotive company|automobile company|car company|marque)\b", first, re.I)
        return named and bool(category_signal or intro_signal)
    ranked = [page for page in pages if automotive(page) and name_match(page)]
    ranked = [page for page in ranked if (name, page.get("title")) not in KNOWN_BAD_MATCHES]
    if not ranked:
        return name, None
    ranked.sort(key=lambda page: (
        -len(tokens & set(re.findall(r"[a-z0-9]+", page.get("title", "").casefold()))),
        page.get("index", 999), page.get("title", ""),
    ))
    return name, ranked[0]


def compact(name: str, page: dict, method: str) -> dict:
    revision = (page.get("revisions") or [{}])[0]
    qid = page.get("pageprops", {}).get("wikibase_item")
    title = page["title"]
    return {
        "candidateName": name, "status": "matched", "matchMethod": method,
        "title": title, "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
        "wikidataId": qid, "wikidataUrl": f"https://www.wikidata.org/wiki/{qid}" if qid else None,
        "pageId": page.get("pageid"), "revisionId": revision.get("revid"),
        "revisionTimestamp": revision.get("timestamp"),
        "extractSha256": hashlib.sha256(page.get("extract", "").strip().encode("utf-8")).hexdigest(),
        "categories": sorted(item["title"] for item in page.get("categories", [])),
        "verifiedAt": "2026-08-25",
    }


def main() -> None:
    queue = json.loads((V2 / "content" / "canonical-curation-decisions.json").read_text(encoding="utf-8"))["queue"]
    pending = sorted(item["candidateName"] for item in queue if item.get("wave") in {f"M{number:02d}" for number in range(2, 13)})
    accepted, retry = direct(pending)
    overridden = overrides(retry)
    retry = [name for name in retry if name not in overridden]
    searched: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        for name, page in pool.map(search_one, retry):
            if page:
                searched[name] = page
    records = []
    for name in pending:
        if name in accepted:
            records.append(compact(name, accepted[name], "direct-title"))
        elif name in overridden:
            records.append(compact(name, overridden[name], "reviewed-title-override"))
        elif name in searched:
            records.append(compact(name, searched[name], "automotive-search"))
        else:
            records.append({"candidateName": name, "status": "unresolved", "verifiedAt": "2026-08-25"})
    document = {
        "version": "1.0.0", "generatedAt": "2026-08-25", "provider": "MediaWiki API",
        "policy": "Automotive evidence required; unresolved names are not guessed. Full third-party extracts are not redistributed.",
        "count": len(records), "matched": sum(item["status"] == "matched" for item in records),
        "unresolved": sum(item["status"] == "unresolved" for item in records), "records": records,
    }
    TARGET.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: document[key] for key in ("count", "matched", "unresolved")}, sort_keys=True))


if __name__ == "__main__":
    main()
