#!/usr/bin/env python3
"""Markdown の参照グラフを数えて、1枚の HTML（外部通信なし）にする。

使い方: python -I workflow-kit/tools/mdgraph.py [リポジトリのルート] [--out 出力.html] [--start AGENTS.md ...]
既定: ルート = この files の 2 つ上（リポジトリのトップ）、起点 = AGENTS.md README.md docs/log.md、
出力 = 一時フォルダの md-link-graph.html（コミットしない。都度生成）。辺の種類: wiki（[[名前]]）、md（[](x.md)）、include（行頭の @x.md）、tick（`x.md`）。
"""
import argparse, collections, html, json, re, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
ap = argparse.ArgumentParser()
ap.add_argument("root", nargs="?", default=str(HERE.parents[2]))
ap.add_argument("--out", default=None)
ap.add_argument("--start", nargs="*", default=["AGENTS.md", "README.md", "docs/log.md"])
ap.add_argument("--kinds", nargs="*", default=["wiki", "md", "include", "tick"], help="数える辺の種類（wiki md include tick）")
a = ap.parse_args()
root = Path(a.root).resolve()
out = Path(a.out) if a.out else Path(tempfile.gettempdir()) / "md-link-graph.html"

SKIP = {".git", "node_modules", ".obsidian"}
def is_unlinked_by_design(p):
    """辿って読まれないファイル。雛形（templates/）と、`@AGENTS.md` だけの CLAUDE.md（Claude Code が自動で取り込む）。2026-10-25 ユーザーの決定。"""
    r = p.relative_to(root).as_posix()
    if "/templates/" in "/" + r:
        return True
    return p.name == "CLAUDE.md" and re.fullmatch(r"@\S+\.md\s*", p.read_text(encoding="utf-8", errors="replace")) is not None


files = [p for p in root.rglob("*.md") if not (SKIP & set(p.relative_to(root).parts)) and not is_unlinked_by_design(p)]
rel = {p: p.relative_to(root).as_posix() for p in files}
by_rel = {r: p for p, r in rel.items()}
by_name = collections.defaultdict(list)
for r in by_rel:
    by_name[Path(r).stem].append(r)

WIKI = re.compile(r"\[\[([^\]|#]+)")
MDL = re.compile(r"\]\(([^)#\s]+\.md)")
INC = re.compile(r"^@(\S+\.md)", re.M)
TICK = re.compile(r"`([^`\s]+\.md)`")


def resolve(src, tgt):
    t = tgt.strip().replace("\\", "/")
    base = Path(rel[src]).parent
    for c in ((base / t).as_posix(), t):
        parts = []
        for seg in c.split("/"):
            if seg == "..":
                if parts:
                    parts.pop()
            elif seg != ".":
                parts.append(seg)
        c = "/".join(parts)
        if c in by_rel:
            return c
    m = by_name.get(Path(t).stem, [])
    if len(m) == 1:
        return m[0]
    s = [r for r in by_rel if r == t or r.endswith("/" + t)]
    return s[0] if len(s) == 1 else None


edges = collections.defaultdict(lambda: collections.defaultdict(set))  # src -> dst -> kinds
for p in files:
    text = p.read_text(encoding="utf-8", errors="replace")
    for rx, k in ((WIKI, "wiki"), (MDL, "md"), (INC, "include"), (TICK, "tick")):
        if k not in a.kinds:
            continue
        for m in rx.finditer(text):
            t = resolve(p, m.group(1))
            if t and t != rel[p]:
                edges[rel[p]][t].add(k)

nodes = sorted(rel.values())
nid = {n: i for i, n in enumerate(nodes)}
adj = {n: sorted(edges[n]) for n in nodes}
indeg = collections.Counter(t for n in nodes for t in adj[n])
dist = {}
q = collections.deque()
for s in a.start:
    if s in nid:
        dist[s] = 0
        q.append(s)
while q:
    n = q.popleft()
    for t in adj[n]:
        if t not in dist:
            dist[t] = dist[n] + 1
            q.append(t)

# 強連結成分（反復 Tarjan）
index, low, on, st, comp_of, comps, cnt = {}, {}, set(), [], {}, [], [0]
for v0 in nodes:
    if v0 in index:
        continue
    index[v0] = low[v0] = cnt[0]; cnt[0] += 1; st.append(v0); on.add(v0)
    work = [(v0, iter(adj[v0]))]
    while work:
        n, it = work[-1]
        for w in it:
            if w not in index:
                index[w] = low[w] = cnt[0]; cnt[0] += 1; st.append(w); on.add(w)
                work.append((w, iter(adj[w])))
                break
            elif w in on:
                low[n] = min(low[n], index[w])
        else:
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[n])
            if low[n] == index[n]:
                c = []
                while True:
                    w = st.pop(); on.discard(w); c.append(w)
                    if w == n:
                        break
                for w in c:
                    comp_of[w] = len(comps)
                comps.append(c)
big = max(comps, key=len)

kind_count = collections.Counter(k for n in nodes for t in adj[n] for k in edges[n][t])
data = {
    "nodes": [{"id": n, "dir": n.split("/")[0] if "/" in n else ".", "depth": dist.get(n, -1),
               "in": indeg[n], "out": len(adj[n]), "scc": len(comps[comp_of[n]]) > 1} for n in nodes],
    "edges": [[nid[n], nid[t], "".join(sorted(k[0] for k in edges[n][t]))] for n in nodes for t in adj[n]],
    "start": a.start,
    "stats": {
        "files": len(nodes), "edges": sum(len(adj[n]) for n in nodes), "kinds": dict(kind_count),
        "reach": len(dist), "unreach": len(nodes) - len(dist),
        "depth": dict(sorted(collections.Counter(dist.values()).items())),
        "scc_big": len(big), "scc_count": sum(1 for c in comps if len(c) > 1),
        "orphans": sorted(n for n in nodes if indeg[n] == 0),
        "unreached": sorted(n for n in nodes if n not in dist),
    },
}

PAGE = r"""<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Markdown 参照グラフ</title>
<style>
body{font:14px/1.5 system-ui,"Yu Gothic UI",sans-serif;margin:0;color:#222;background:#fafafa}
header{padding:10px 16px;background:#24292f;color:#fff}header small{opacity:.7;margin-left:8px}
main{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:12px;padding:12px}
@media(max-width:900px){main{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid #d0d7de;border-radius:6px;padding:10px 12px;margin-bottom:12px}
h2{font-size:14px;margin:0 0 6px}table{border-collapse:collapse;width:100%}td,th{padding:2px 6px;border-bottom:1px solid #eee;text-align:left;font-size:13px}
td.n{text-align:right}canvas{width:100%;height:640px;background:#fff;border:1px solid #d0d7de;border-radius:6px;display:block;touch-action:none}
.bar{display:inline-block;height:10px;background:#4c78a8;vertical-align:middle}
label{margin-right:10px;font-size:13px}#info{font-size:13px;word-break:break-all}
.leg span{display:inline-block;margin-right:8px;font-size:12px}.leg i{display:inline-block;width:10px;height:10px;border-radius:5px;margin-right:3px}
code{font-size:12px}ul{margin:4px 0;padding-left:18px}
</style>
<header><b>Markdown 参照グラフ</b><small id="gen"></small></header>
<main><div>
<div class="card"><label><input type="checkbox" id="fScc"> 大きな循環に入る点だけ強調</label>
<label>辺の種類: <select id="fKind"><option value="">すべて</option><option value="w">wikilink</option><option value="t">バッククォート内パス</option><option value="i">@取り込み</option><option value="m">md リンク</option></select></label>
<label>最小の次数 <input type="number" id="fMin" value="0" min="0" style="width:4em"></label>
<div class="leg" id="leg"></div></div>
<canvas id="cv"></canvas>
<p style="font-size:12px;color:#666">点の大きさ = 入次数。ドラッグで動かし、クリックで詳細。ホイールで拡大縮小。</p></div>
<div><div class="card" id="sum"></div><div class="card"><h2>選んだ点</h2><div id="info">点をクリックしてください。</div></div>
<div class="card"><h2>出次数の上位（ハブ）</h2><table id="hubOut"></table></div>
<div class="card"><h2>入次数の上位</h2><table id="hubIn"></table></div>
<div class="card"><h2>どこからも参照されない</h2><div id="orph"></div></div>
<div class="card"><h2>起点から未到達</h2><div id="unr"></div></div></div></main>
<script>
const D=__DATA__;const S=D.stats,N=D.nodes,E=D.edges;
document.getElementById('gen').textContent='起点: '+D.start.join(', ');
const esc=s=>s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const dirs=[...new Set(N.map(n=>n.dir))].sort();
const pal=['#4c78a8','#f58518','#54a24b','#e45756','#b279a2','#9d755d','#72b7b2','#eeca3b','#bab0ac','#ff9da6'];
const col=d=>pal[dirs.indexOf(d)%pal.length];
document.getElementById('leg').innerHTML=dirs.map(d=>`<span><i style="background:${col(d)}"></i>${esc(d)}</span>`).join('');
const maxd=Math.max(...Object.values(S.depth));
document.getElementById('sum').innerHTML=`<h2>要約</h2><table>
<tr><td>ファイル</td><td class=n>${S.files}</td></tr><tr><td>辺</td><td class=n>${S.edges}</td></tr>
<tr><td>辺の種類</td><td class=n>${Object.entries(S.kinds).map(([k,v])=>k+' '+v).join(' / ')}</td></tr>
<tr><td>起点から到達 / 未到達</td><td class=n>${S.reach} / ${S.unreach}</td></tr>
<tr><td>最大の深さ</td><td class=n>${maxd}</td></tr>
<tr><td>最大の循環の大きさ</td><td class=n>${S.scc_big}（全体の ${Math.round(100*S.scc_big/S.files)}%）</td></tr></table>
<h2 style="margin-top:8px">深さ別の件数</h2><table>${Object.entries(S.depth).map(([d,c])=>`<tr><td>${d}</td><td class=n>${c}</td><td><span class=bar style="width:${Math.round(c/S.files*220)}px"></span></td></tr>`).join('')}</table>`;
const topN=(k)=>N.map((n,i)=>[n,i]).sort((a,b)=>b[0][k]-a[0][k]).slice(0,10).map(([n,i])=>`<tr><td>${esc(n.id)}</td><td class=n>${n[k]}</td></tr>`).join('');
hubOut.innerHTML=topN('out');hubIn.innerHTML=topN('in');
const lst=a=>a.length?'<ul>'+a.map(x=>`<li><code>${esc(x)}</code></li>`).join('')+'</ul>':'なし';
orph.innerHTML=lst(S.orphans);unr.innerHTML=lst(S.unreached);
// force layout
const cv=document.getElementById('cv'),cx=cv.getContext('2d');let W,H,dpr=devicePixelRatio||1;
function size(){W=cv.clientWidth;H=cv.clientHeight;cv.width=W*dpr;cv.height=H*dpr}size();addEventListener('resize',()=>{size()});
N.forEach((n,i)=>{const a=i*2.399,r=8*Math.sqrt(i+1);n.x=Math.cos(a)*r*6;n.y=Math.sin(a)*r*6;n.vx=n.vy=0});
let zoom=1,ox=0,oy=0,sel=-1,drag=-1,alpha=1;
function visEdges(){const k=fKind.value;return E.filter(e=>(!k||e[2].includes(k)))}
function step(){const ed=visEdges();
 for(let i=0;i<N.length;i++){const a=N[i];for(let j=i+1;j<N.length;j++){const b=N[j];let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+.01;if(d2>90000)continue;const f=900/d2*alpha;a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f}}
 for(const [s,t] of ed){const a=N[s],b=N[t];const dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy)+.01,f=(d-70)*.004*alpha;a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f}
 for(const n of N){n.vx-=n.x*.002*alpha;n.vy-=n.y*.002*alpha;n.vx*=.85;n.vy*=.85;if(n.i!==drag){n.x+=n.vx;n.y+=n.vy}}
 alpha=Math.max(.02,alpha*.995)}
N.forEach((n,i)=>n.i=i);
function draw(){const min=+fMin.value,only=fScc.checked,ed=visEdges();cx.setTransform(dpr,0,0,dpr,0,0);cx.clearRect(0,0,W,H);
 cx.translate(W/2+ox,H/2+oy);cx.scale(zoom,zoom);
 const hi=new Set();if(sel>=0)for(const [s,t] of E){if(s===sel)hi.add(t);if(t===sel)hi.add(s)}
 const show=n=>n.in+n.out>=min;
 cx.lineWidth=.5/zoom;
 for(const [s,t] of ed){const a=N[s],b=N[t];if(!show(a)||!show(b))continue;const h=sel>=0&&(s===sel||t===sel);
  cx.strokeStyle=h?'#d62728':'rgba(120,130,140,.18)';cx.lineWidth=(h?1.4:.5)/zoom;cx.beginPath();cx.moveTo(a.x,a.y);cx.lineTo(b.x,b.y);cx.stroke()}
 for(const n of N){if(!show(n))continue;const r=2.5+Math.sqrt(n.in)*1.6;cx.globalAlpha=only&&!n.scc?.15:1;
  cx.fillStyle=col(n.dir);cx.beginPath();cx.arc(n.x,n.y,r,0,7);cx.fill();
  if(n.i===sel||hi.has(n.i)||n.in>=20){cx.fillStyle='#222';cx.font=11/zoom+'px sans-serif';cx.fillText(n.id.split('/').pop(),n.x+r+2,n.y+3)}
  if(n.i===sel){cx.strokeStyle='#d62728';cx.lineWidth=2/zoom;cx.stroke()}}
 cx.globalAlpha=1}
function loop(){step();draw();requestAnimationFrame(loop)}loop();
const pt=e=>{const r=cv.getBoundingClientRect();return [(e.clientX-r.left-W/2-ox)/zoom,(e.clientY-r.top-H/2-oy)/zoom]};
function pick(x,y){let b=-1,bd=1e9;for(const n of N){const d=(n.x-x)**2+(n.y-y)**2,r=2.5+Math.sqrt(n.in)*1.6+3;if(d<r*r&&d<bd){bd=d;b=n.i}}return b}
let pan=null,moved=false;
cv.onpointerdown=e=>{cv.setPointerCapture(e.pointerId);const [x,y]=pt(e);drag=pick(x,y);moved=false;if(drag<0)pan=[e.clientX-ox,e.clientY-oy]};
cv.onpointermove=e=>{moved=true;if(drag>=0){const [x,y]=pt(e);N[drag].x=x;N[drag].y=y;alpha=.3}else if(pan){ox=e.clientX-pan[0];oy=e.clientY-pan[1]}};
cv.onpointerup=e=>{if(!moved){const [x,y]=pt(e);sel=pick(x,y);info()}drag=-1;pan=null};
cv.onwheel=e=>{e.preventDefault();zoom=Math.min(6,Math.max(.2,zoom*(e.deltaY<0?1.15:.87)))};
function info(){if(sel<0){infoEl.textContent='点をクリックしてください。';return}
 const n=N[sel],o=E.filter(e=>e[0]===sel).map(e=>N[e[1]].id),i=E.filter(e=>e[1]===sel).map(e=>N[e[0]].id);
 infoEl.innerHTML=`<b>${esc(n.id)}</b><br>深さ ${n.depth<0?'未到達':n.depth} / 入 ${n.in} / 出 ${n.out}${n.scc?' / 大きな循環に入る':''}<br>出（${o.length}）${lst(o.slice(0,30))}入（${i.length}）${lst(i.slice(0,30))}`}
const infoEl=document.getElementById('info');
[fScc,fKind,fMin].forEach(el=>el.onchange=()=>{alpha=.6});
</script></html>"""

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(PAGE.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8", newline="\n")
s = data["stats"]
print(f"出力: {out}")
print(f"{len(nodes)} ファイル / {s['edges']} 辺 / 到達 {s['reach']} / 最大の循環 {s['scc_big']} / 深さ {s['depth']}")
print(f"未到達 {s['unreach']} / 入次数 0 {len(s['orphans'])} / 最大の循環の割合 {round(100 * s['scc_big'] / s['files'])}%")
for label, key in (("未到達", "unreached"), ("入次数 0", "orphans")):
    print(f"{label}: {' '.join(data["stats"][key]) or 'なし'}")
print(f"出力: {out}")
