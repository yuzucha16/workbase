// excalidraw_view.py から呼ぶ。閲覧用の JS を 1 つ（CSS も内包）に束ねる。
import { build } from "esbuild";
import { readFileSync, writeFileSync, rmSync } from "node:fs";

const out = process.argv[2];
await build({
  entryPoints: ["viewer_entry.jsx"],
  bundle: true,
  minify: true,
  format: "iife",
  conditions: ["production"],
  loader: { ".js": "jsx", ".woff2": "dataurl", ".woff": "dataurl", ".ttf": "dataurl" },
  define: { "process.env.NODE_ENV": '"production"', "process.env.IS_PREACT": '"false"' },
  outdir: out + ".tmp",
});
const js = readFileSync(out + ".tmp/viewer_entry.js", "utf8");
const css = readFileSync(out + ".tmp/viewer_entry.css", "utf8");
// CSS は JS から <style> として差し込む（HTML を 1 本のスクリプトで済ませるため）
writeFileSync(
  out,
  `(function(){var s=document.createElement("style");s.textContent=${JSON.stringify(css)};document.head.appendChild(s);})();\n` + js
);
rmSync(out + ".tmp", { recursive: true, force: true });
