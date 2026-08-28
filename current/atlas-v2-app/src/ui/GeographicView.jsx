import { useEffect, useMemo, useRef, useState } from "react";
import "maplibre-gl/dist/maplibre-gl.css";
import { loadBundle, publicUrl } from "../lib/atlas-data.js";

let cesiumPromise;
function loadCesium() {
  if (window.Cesium) return Promise.resolve(window.Cesium);
  if (!cesiumPromise) {
    window.CESIUM_BASE_URL = publicUrl("cesium/");
    if (!document.querySelector("link[data-atlas-cesium]")) {
      const style = document.createElement("link");
      style.rel = "stylesheet";
      style.href = publicUrl("cesium/Widgets/widgets.css");
      style.dataset.atlasCesium = "true";
      document.head.append(style);
    }
    cesiumPromise = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = publicUrl("cesium/Cesium.js");
      script.async = true;
      script.onload = () => resolve(window.Cesium);
      script.onerror = () => reject(new Error("Falha ao carregar o módulo local do Cesium"));
      document.head.append(script);
    });
  }
  return cesiumPromise;
}

function yearOf(value, fallback) {
  const match = String(value || "").match(/^\d{4}/);
  return match ? Number(match[0]) : fallback;
}

// Cumulative, like every other projection in the Atlas: the map shows the
// geography known up to the selected year. Filtering to geometries valid *in*
// that exact year left 109 of the 258 years with nothing at all on screen, and
// left almost nothing to connect in the years that had anything.
function visibleAt(feature, year) {
  return yearOf(feature.properties?.validity?.from, 1769) <= year;
}

function coordinatePairs(geometry) {
  if (!geometry) return [];
  const walk = (value) => typeof value?.[0] === "number" ? [value] : (value || []).flatMap(walk);
  return walk(geometry.coordinates);
}

function GeographicOverlay({ collection }) {
  const pairs = collection.features.flatMap((feature) => coordinatePairs(feature.geometry));
  if (!pairs.length) return null;
  const longitudes = pairs.map(([longitude]) => longitude);
  const latitudes = pairs.map(([, latitude]) => latitude);
  const minLongitude = Math.min(...longitudes);
  const maxLongitude = Math.max(...longitudes);
  const minLatitude = Math.min(...latitudes);
  const maxLatitude = Math.max(...latitudes);
  const project = ([longitude, latitude]) => [
    8 + ((longitude - minLongitude) / (maxLongitude - minLongitude || 1)) * 84,
    88 - ((latitude - minLatitude) / (maxLatitude - minLatitude || 1)) * 76,
  ];
  return <svg className="geographic-overlay" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
    {collection.features.map((feature) => {
      const featurePairs = coordinatePairs(feature.geometry);
      if (feature.geometry?.type === "Point") {
        const [x, y] = project(featurePairs[0]);
        return <circle key={feature.id} cx={x} cy={y} r="1.7" vectorEffect="non-scaling-stroke" />;
      }
      const points = featurePairs.map((pair) => project(pair).join(",")).join(" ");
      return <polyline key={feature.id} points={points} vectorEffect="non-scaling-stroke" />;
    })}
  </svg>;
}

function MapCanvas({ collection }) {
  const element = useRef(null);
  const map = useRef(null);
  const [state, setState] = useState("loading");
  useEffect(() => {
    let cancelled = false;
    Promise.all([import("maplibre-gl"), loadBundle("basemap.json")]).then(([module, basemap]) => {
      const maplibregl = module.default || module;
      if (cancelled || !element.current) return;
      const instance = new maplibregl.Map({
        container: element.current,
        style: { version: 8, sources: {}, layers: [{ id: "background", type: "background", paint: { "background-color": "rgba(16,21,16,0.78)" } }] },
        center: [8, 34], zoom: 1.2, attributionControl: false,
      });
      map.current = instance;
      instance.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
      instance.on("load", () => {
        instance.addSource("land", { type: "geojson", data: basemap });
        instance.addLayer({ id: "land-fill", type: "fill", source: "land", paint: { "fill-color": "#243329", "fill-outline-color": "#41573f" } });
        instance.addLayer({ id: "land-edge", type: "line", source: "land", paint: { "line-color": "#5d7a5c", "line-width": .7 } });
        instance.addSource("atlas", { type: "geojson", data: collection });
        instance.addLayer({ id: "atlas-lines", type: "line", source: "atlas", filter: ["==", "$type", "LineString"], paint: { "line-color": "#d9a45f", "line-width": 3, "line-opacity": .85 } });
        instance.addLayer({ id: "atlas-points", type: "circle", source: "atlas", filter: ["==", "$type", "Point"], paint: { "circle-radius": 6, "circle-color": "#d23630", "circle-stroke-color": "#f4e5c8", "circle-stroke-width": 1.5 } });
        const pairs = collection.features.flatMap((feature) => coordinatePairs(feature.geometry));
        if (pairs.length) {
          const bounds = pairs.reduce((box, pair) => box.extend(pair), new maplibregl.LngLatBounds(pairs[0], pairs[0]));
          instance.fitBounds(bounds, { padding: 54, maxZoom: 7, duration: 0 });
        }
        setState("ready");
      });
      instance.on("error", (event) => { console.error("Atlas MapLibre", event.error); setState("error"); });
    }).catch((error) => { console.error("Atlas MapLibre", error); setState("error"); });
    return () => { cancelled = true; map.current?.remove(); map.current = null; };
  }, [collection]);
  return <div className="spatial-canvas"><div ref={element} className="maplibre-canvas" aria-hidden="true" /><GeographicOverlay collection={collection} /><span className={`spatial-state ${state}`}>{state === "ready" ? "MAPA LOCAL" : state === "error" ? "FALLBACK TEXTUAL" : "CARREGANDO MAPA"}</span></div>;
}

function GlobeCanvas({ collection }) {
  const element = useRef(null);
  const viewer = useRef(null);
  const [state, setState] = useState("loading");
  useEffect(() => {
    let cancelled = false;
    Promise.all([loadCesium(), loadBundle("basemap.json")]).then(([Cesium, basemap]) => {
      if (cancelled || !element.current) return;
      const instance = new Cesium.Viewer(element.current, {
        animation: false, timeline: false, baseLayerPicker: false, geocoder: false,
        homeButton: false, sceneModePicker: false, navigationHelpButton: false,
        fullscreenButton: false, infoBox: false, selectionIndicator: false,
        baseLayer: false, terrainProvider: new Cesium.EllipsoidTerrainProvider(),
      });
      viewer.current = instance;
      instance.scene.backgroundColor = Cesium.Color.fromCssColorString("#080b08");
      instance.scene.globe.baseColor = Cesium.Color.fromCssColorString("#0d1b26");
      Cesium.GeoJsonDataSource.load(basemap, {
        fill: Cesium.Color.fromCssColorString("#243329"),
        stroke: Cesium.Color.fromCssColorString("#5d7a5c"),
        strokeWidth: 1,
      }).then((land) => { if (!instance.isDestroyed()) instance.dataSources.add(land); });
      for (const feature of collection.features) {
        const pairs = coordinatePairs(feature.geometry);
        const label = feature.properties?.label || feature.properties?.purpose || "Registro espacial";
        if (["Point", "MultiPoint"].includes(feature.geometry?.type)) {
          pairs.forEach((pair, index) => instance.entities.add({ id: `${feature.id}-${index}`, name: label, position: Cesium.Cartesian3.fromDegrees(pair[0], pair[1]), point: { pixelSize: 9, color: Cesium.Color.fromCssColorString("#d23630"), outlineColor: Cesium.Color.WHITE, outlineWidth: 1 } }));
        } else if (pairs.length > 1) {
          instance.entities.add({ id: String(feature.id), name: label, polyline: { positions: pairs.map((pair) => Cesium.Cartesian3.fromDegrees(pair[0], pair[1])), width: 3, material: Cesium.Color.fromCssColorString("#d9a45f") } });
        }
      }
      if (instance.entities.values.length) instance.zoomTo(instance.entities, new Cesium.HeadingPitchRange(0, -1.1, 12000000));
      setState("ready");
    }).catch((error) => { console.error("Atlas Cesium", error); setState("error"); });
    return () => { cancelled = true; if (viewer.current && !viewer.current.isDestroyed()) viewer.current.destroy(); viewer.current = null; };
  }, [collection]);
  return <div className="spatial-canvas"><div ref={element} className="cesium-canvas" aria-hidden="true" /><span className={`spatial-state ${state}`}>{state === "ready" ? "GLOBO LOCAL" : state === "error" ? "FALLBACK TEXTUAL" : "CARREGANDO GLOBO"}</span></div>;
}

export default function GeographicView({ mapKind, features, year, story }) {
  const visible = useMemo(() => features.filter((feature) => visibleAt(feature, year)), [features, year]);
  const collection = useMemo(() => ({ type: "FeatureCollection", features: visible }), [visible]);
  return <section className="projection geography-view" aria-labelledby="geography-title">
    <header><p>CARTOGRAFIA TEMPORAL</p><h2 id="geography-title">{mapKind} histórico · {year}</h2><span>{visible.length} geometrias válidas · {story.place}</span></header>
    {visible.length ? mapKind === "Globo" ? <GlobeCanvas collection={collection} /> : <MapCanvas collection={collection} /> : <p className="projection-empty">Nenhuma geometria possui validade neste ano; o capítulo permanece disponível como narrativa.</p>}
    <details className="projection-records"><summary>Resumo textual — geografia de {year}</summary>{visible.length ? <ol>{visible.map((feature) => <li key={feature.id}><strong>{feature.properties?.label || feature.properties?.purpose}</strong> — {feature.geometry?.type}; precisão {feature.properties?.precision}; confiança {feature.properties?.confidence}.</li>)}</ol> : <p>Nenhuma geometria temporal neste recorte.</p>}</details>
  </section>;
}
