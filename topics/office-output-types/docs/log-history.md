# 作業ログの経緯（log-history）

## Log

### 2026-11-06（Quarto の実機試験と init への追加）
- 経緯: NA 5 で、部屋 room-myenv に Quarto 1.11.9 の tarball を試験用に入れ、日本語と mermaid を含む `.qmd` を pptx にした。
- 結果: 通った。`.md` では mermaid が通らず `.qmd` が要る。Chromium は自動検出されず `QUARTO_CHROMIUM` の指定が要る。mermaid の日本語は正常。pptx のフォントは名前だけが入る。ee の決定で `init` に足し（`decisions.md` 11-04）、フォントは BIZ UDPGothic（フォールバックは pptx で効かないため）。
- 根拠: `fc46b75`（`room.py` の `quarto` 段、雛形と試験 pptx を `records/` に置いた）、`b81d927`（NA 6 を追加）。
- 閉じた項目: NA 5 の「入れ方・版・Chromium・日本語」の部分（一部済。残りは PC1 でのフォント確認と新しい部屋での `init --only quarto`）。

### 2026-11-04（markdown → pptx の叩き台。道具の調査）
- 経緯: NA が実機待ちだけになったため、ee が markdown → pptx を AI 活用に組み込む叩き台を選んだ。Marp とその類似ツールの比較と、2026 年の流行を調査した。
- 結果: Marp と Slidev の通常の pptx は画像。Quarto は編集できる pptx で、雛形を使える。ee の決定で主は Quarto、副は Marp（`decisions.md`）。理解ガイドを `guides/explain/markdown-to-pptx-quarto-explain.md` に出力し、`guides-index.md` に足した。
- 未確認: どの道具も実機は未試験。Quarto の部屋への入れ方、Chromium の検出、日本語の崩れ（NA 5）。

### 2026-11-02（公開 pptx 4 つの試行を取り下げた）
- omit（NA1）: ユーザーの方針転換(設計書風・組織目標風を AI に入力できなくなった)で、NA1 を omit。`decisions.md` の同日の項。テキスト出力の型の試し方は Area の internal/external の範囲で決め直す(未定)。公開 pptx 4 つの試行の元の記述は 10-30 の `decisions.md` の項に残る。
  - 元の項目: （omit 2026-11-02。公開 pptx 4 つの試行は、設計書・組織目標の類を AI に入力できなくなったため取り下げ。`decisions.md`）

### 2026-10-30（雑談: テキスト出力の型。試行の進め方）
- 経緯: ee が、Excel → テキスト（設計情報・会議録を Excel に残す習慣の分析、論点列挙・影響分析）と pptx → テキスト（設計・組織目標の分析）も、Excel → Excel と同じ型で、AI・人・スクリプトの分担を作り込めるかを問うた。
- AI の整理: 入力の読み取り定義表、検証の ID 紐づけ、分担の枠は使い回せる。違いは 2 点。契約の中心がマスターの列定義から出力 Markdown の構造に変わること、AI が実行時の主役になること（検証は網羅と根拠位置の実在までが決定論）。雛形は「共通部」と「出力別の固定部」に分ける案（Open Questions に記載）。
- ee の追加: 公開 pptx を入力にできるので、PC1 に頼らず試行を増やせる。入力は ee と AI が設計書風・組織目標風を 1 つずつ出し、計 4 つで行う。
- 反映: `docs/log.md` の Next Actions（1 に試行、旧 3 を 4 へ）と Open Questions、窓口の次の一手、`docs/decisions.md`。

### 2026-10-30（トピック作成。IR の議論から基準文書の雛形まで）
- 経緯: ee が PC1 の Excel マクロ作業（AI が .bas、人がレイアウト・組み込み・コンパイル・確認）の改善のため、別のエージェントと OOXML と IR を壁打ちした（`records/2026-10-30-office-ooxml-ai-artifact-workflow.md`）。token-cap の観点で、人・AI・スクリプトの役割分担を考えていた。
- 当てはめ（`records/2026-10-30-ir-fit-to-current-room.md`）: 部屋で決定論の検査・比較をし、AI は基準文書と差分だけを読む。openpyxl が部屋で使えるかは未確認。
- 議論の転換: ee の「出力の型」のアナロジー。成果物は集約ブックで、.bas は手段。ブックの構造は、データ 1 シートに可視化 12 シート（ピボット）。
- 成果: 基準文書の雛形（`records/2026-10-30-master-book-baseline-template.md`）。固定部 R1〜R6 は ee が確認。入力の読み取りは定義表で宣言する案（仮決め）。
- 確かめていないこと: 雛形を実物に当てる（PC1）。openpyxl の可否。Excel → テキストなど他の型。
- 作成・反映（同日）: トピックを作り main に push した（d4b10ef）。ee の指示は「トピックを作って main にコミット」。雛形の `exmem/lessons/` への昇格は、1 回回してから決める案（ee の回答は未）。最初の叩き台は、成果物を .bas と置いた時点のもので、`records/` に残した（最新は雛形と `docs/decisions.md`）。
