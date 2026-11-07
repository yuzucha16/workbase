import React, { useState, useRef } from "react";
import { createRoot } from "react-dom/client";
import { Excalidraw, exportToSvg } from "@excalidraw/excalidraw";
import "@excalidraw/excalidraw/index.css";

const files = window.__EXV_FILES__ || [];

function App() {
  const [i, setI] = useState(0);
  const apiRef = useRef(null);
  const f = files[i];
  const data = f ? f.data : {};
  const saveSvg = async () => {
    const api = apiRef.current;
    if (!api) return;
    const svg = await exportToSvg({
      elements: api.getSceneElements(),
      appState: { ...api.getAppState(), exportBackground: true },
      files: api.getFiles(),
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([svg.outerHTML], { type: "image/svg+xml" }));
    a.download = (f ? f.name : "drawing").replace(/\.excalidraw$/, "") + ".svg";
    a.click();
  };
  const bg = (data.appState || {}).viewBackgroundColor || "#ffffff";
  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      <div style={{ padding: "6px 10px", font: "14px sans-serif", background: "#f1f3f5", display: "flex", gap: 10, alignItems: "center" }}>
        <select value={i} onChange={(e) => setI(+e.target.value)}>
          {files.map((x, k) => (<option key={k} value={k}>{x.name}</option>))}
        </select>
        <button onClick={saveSvg}>SVG を保存</button>
        <span style={{ color: "#666" }}>閲覧専用 ({files.length} 件)</span>
      </div>
      <div style={{ flex: 1 }}>
        <Excalidraw
          key={i}
          excalidrawAPI={(a) => (apiRef.current = a)}
          viewModeEnabled={true}
          initialData={{
            elements: data.elements || [],
            appState: { ...(data.appState || {}), viewBackgroundColor: bg },
            files: data.files || {},
            scrollToContent: true,
          }}
        />
      </div>
    </div>
  );
}
// 書き出しモード（excalidraw_view.py --export）: 画面を出さず、全ファイルの SVG を JSON にして <pre id="exv-out"> に入れる。
async function exportAll() {
  const out = [];
  for (const f of files) {
    const d = f.data || {};
    try {
      const svg = await exportToSvg({
        elements: (d.elements || []).filter((e) => !e.isDeleted),
        appState: { ...(d.appState || {}), exportBackground: true, viewBackgroundColor: (d.appState || {}).viewBackgroundColor || "#ffffff" },
        files: d.files || {},
        exportPadding: 20,
      });
      out.push({ name: f.name, svg: svg.outerHTML });
    } catch (e) {
      out.push({ name: f.name, error: String(e) });
    }
  }
  const pre = document.createElement("pre");
  pre.id = "exv-out";
  pre.textContent = JSON.stringify(out);
  document.body.appendChild(pre);
}

if (window.__EXV_EXPORT__) {
  exportAll();
} else {
  createRoot(document.getElementById("root")).render(<App />);
}
