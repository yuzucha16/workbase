# 次のステップ: 大きなトピックを進める型

背景と決定は [[topic-workflow-handover]]。案の詳細（窓口の見出し、予算、ゴールの測り方）は [[topic-workflow-proposal]] の 2〜4。

**着手の条件**: ai-workspace-boundary の PC での動作確認が終わってから。[[kit-growth-handover]] の順番（改名 → kit-growth の経路の整備）と合わせて進める。kit の変更は、ユーザーの承認を得てから。

## TODO（済んだら `[x]`）

- [x] 1. `mobile-session/` を `topics/` に改名した（Q1。2026-10-15）。ルートの `AGENTS.md` の構成表、index のファイル名、各文書の参照を合わせる。index は1トピック1行（状態は書かず、窓口へのリンクと「あなた待ち」の件数）
- [x] 2. （2026-10-15 済）improvement-methods を新しい型で close する（Q5）。残りの「`start` のモードを2〜3セッションで試す」を、kit-growth か `review` の対象に移し、ディレクトリを消す。出口の手順を1回通すのが目的
- [x] 3. （2026-10-15 済。窓口 1.4KB・`docs/log.md` 2.7KB・decisions・log-history・`notes/`。再開の試行は未）ai-workspace-boundary を docs の型に組み替える（Q2・Q3）。13ファイル → 窓口（README、2KB）・`docs/log.md`（状態の正本、4KB）・`docs/decisions.md`・`docs/log-history.md`・詳細ノート。状態の写しを消す。初版（roadmap 1〜7）で close
- [x] 4. （2026-10-15 済。進める側を選んだ。窓口 1.4KB・`docs/log.md` 2.0KB・decisions・`notes/`。log-history は経緯が無いので作らない）dotfiles-boundary を新しい型で進めるか close する。型の2回目の使用
- [ ] 5. （2026-10-15 ユーザーの決定: 型は2回使えたが、再開を2回試してから取り込む。2026-10-15 に `again`・`gap` を廃止したので、数える条件は外れた。取り込みの時機は要再判断）2回使えたら kit に取り込む。足す: docs-rules に「トピック」の節1つと窓口の雛形1つ。畳む: index の「使い方」、`session-handoff` の3行の依頼文の型、docs-rules と `exmem/AGENTS.md` の「引継ぎは lessons の Open Questions」の記述。足した字数 ≦ 畳んだ字数（規模の凍結。判定日 2026-11-08）
- [x] 6. （2026-10-15 済。本トピックの決定（kit-growth が Area の担い手）を採った）handover の「食い違い」（Area の担い手）を kit-growth と合わせて決める
- [x] 7. （2026-10-15 済）改善ネタ（名前の分かりやすさ）を、kit-growth の inbox に移す
- [ ] 反映が終わったら、このディレクトリを削除し、index の行を消す

## 追加の TODO（Q6 から。2026-10-15）

- [x] 窓口の雛形を kit の `templates/` に足した（2026-10-15）: トピック用 `templates/topic/start-here.template.md`、Project 用は `templates/project/README.template.md` に「いま / あなた待ち / 次の一手」を足して README が窓口を兼ねる。足した字数に見合う畳みは、5（2回使えてから）で行う。Area の README への展開は未
- [x] （2026-10-15 済。決定は kit-growth の `docs/decisions.md`。kit は `hooks.md` の「起動する場所（cwd）」ほか）**cwd（作業を始める場所）を明確にする**（2026-10-15 ユーザーの指摘。kit にはほぼ明文化が無い。`improvements.md` の古い1行のみ）。決めること: ① どこで Claude を起動するか（トピック / Project / Area の各ディレクトリか、Vault のトップか、リポジトリのトップか）、② cwd によって AI が自動で読むもの（`CLAUDE.md` / `AGENTS.md` は cwd から上へ、下は必要時）が変わるので、窓口・`AGENTS.md` を置く階層、③ 「<名前> の続き」が効く条件（cwd がそのトピック・Project のとき。トップから始めるなら名前を言う）、④ 部屋（AI 作業部屋）では cwd = `/mnt/room/<Project>` で固定されること、⑤ 書き込み先の既定（`wrap` の「対象を特定する」は cwd を使う）。成果は `docs-rules.md` か `hooks.md` の契約に1節
- [x] （2026-10-15 済。窓口 → `log.md` にそろえた）各 Project / Area の `AGENTS.md`（雛形）の「読む順番」に窓口を入れるか決める。現状の雛形は `docs/log.md` → README → `decisions.md` で、README が窓口の役を担う
- [ ] 短いセッションを多く回す前提での測定: 再開ごとの開始時の読み込み字数（`sessions`）

## 確かめること（仮説）

- 窓口 2KB・30秒で読める、は目安。3 の組み替えのあと、再開を2回試して確かめる（`again`・`gap` の件数は 2026-10-15 に廃止）。
