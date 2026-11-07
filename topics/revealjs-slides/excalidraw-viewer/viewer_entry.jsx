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
createRoot(document.getElementById("root")).render(<App />);
