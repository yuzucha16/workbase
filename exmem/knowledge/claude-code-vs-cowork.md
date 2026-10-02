---
type: knowledge
title: Claude CodeとCoworkの使い分け（Windows）とExcelスキル
status: active
tags:
  - ai/claude
  - tool/wsl
  - tool/excel
  - windows
  - office
aliases:
  - Claude Code vs Cowork
  - excel-aggregationスキル
  - CoworkのWindows要件
created: 2026-10-02
updated: 2026-10-02
sources:
  - Claude conversation "Claude Code と Cowork の使い分け(Windows環境)とExcelスキル" (2026-10-02)
  - "%USERPROFILE%\\.claude\\skills と OS情報（2026-10-02 に確認）"
---

# Claude CodeとCoworkの使い分け（Windows）とExcelスキル

## Purpose

Claude CodeをWSL2で使うかWindowsネイティブで使うかの基準、Coworkとの使い分け、Excel / CSVを扱うClaude Code用スキル（`excel-aggregation`）の方針をまとめる。

## Principles

- 扱うファイルがある側で動かす。Excel / CSVはWindows側にあるので、Windowsネイティブで動かす。
- 環境を増やさない。まずCodeに寄せ、Coworkは必要になってから足す。
- 「エラーがない」は「数式が正しい」ではない。独立した計算で突き合わせる。
- Windows Homeでは Cowork は使えない前提で計画する（要件は後述）。

## Decisions

### Excel / CSVを扱うClaude Codeは、WSLではなくWindowsネイティブで始める（2026-10-02）

- 根拠: コードはLinux、資料作成はWindowsという分担で、扱うファイルはWindows側にある。WSLから `/mnt/c` 越しに触ると遅く、パスの扱いも面倒。
- 却下案: WSL2でExcel / CSVも扱う。

### まずCodeに寄せ、Coworkは後から検討する

- 根拠: 環境が1つで済み、設定の二重管理を避けられる。学習コストも低い。Zedなどのエディタ運用とも一貫する。定期実行やGUIが欲しくなった作業だけCoworkに切り出す。
- 却下案: 最初からCodeとCoworkを併用する。

### Excel用スキルは公式xlsxスキルをベースに自作する（`excel-aggregation`）

- 根拠: 公式の `recalc.py` はLibreOffice前提で、Windowsネイティブにそのままは合わない。再計算をLibreOfficeかExcel COM（pywin32）に置き換え、CSVの文字コード（`cp932` / `utf-8-sig`）とMaster / view分離、作業記録を足した。
- 却下案: 公式スキルをそのまま使う。
- 方針は [[office-ai-workspace]]（公式スキルを書き換えず拡張する）と同じ。

## Facts

メモがWeb検索で確認した内容（公式ドキュメントと第三者の記事が混在）。

- CodeとCoworkは別アプリ。「CodeはWSL、CoworkはWindowsネイティブ」の併用は可能。
- CoworkのWindows版は2026年2月10日にリリースされ、4月9日に一般提供（GA）になったと報じられている。
- Coworkを使う条件: 有料プラン（Pro / Max / Team / Enterprise）、フルのHyper-V（Windows Home不可、Pro / Enterprise / Education）、.msix版のClaude Desktop、管理者権限。リリース時点ではWindows ARM64は非対応。
- Coworkの特徴: Claude Desktopの「Cowork」タブから使う。許可したフォルダだけにアクセスし、VMで隔離される。標準スキルでWord・スプレッドシート・スライド・PDFを作れる。サブエージェント並列実行、プラグイン、MCPコネクタ、定期実行に対応。定期実行はPCが起動し、Claude Desktopが開いているときだけ動く。通常のチャットより利用枠を多く消費する。
- Coworkのネットワークegress設定は、Web検索やMCPには適用されない（公式サポート記事）。
- Office内のアドイン（Claude in Excel / PowerPoint）は別物で、Coworkを組み込むものではない。
- openpyxlは数式を文字列で書くだけで、計算結果（キャッシュ値）を持たない。再計算しないと、pandasなどでは数式セルが空に見える。動的配列関数（`XLOOKUP`、`FILTER`、`SORT`、`UNIQUE` など）はspill情報を書けない。2007以降の関数（`MAXIFS` など）は `_xlfn.` の接頭辞が要る。

### 実物との照合（2026-10-02）

- このPCのWindowsエディションは Home（`Get-ComputerInfo` が "Windows 10 Home" と表示する。環境情報ではWindows 11 Home。表記は食い違うが、どちらもHome）。**Coworkの要件（フルのHyper-V）を満たさない**。ただし、メモの会話が想定する業務PCがこのPCかは未確認。
- `%USERPROFILE%\.claude\skills\` には `synced` というフォルダしかなく、`excel-aggregation` は配置されていない。

### 仮説・未確認

- CodeとCoworkで出力品質が同じか（システムプロンプト、ツール構成、標準スキルが違う）。
- Codeの設定資産（`~/.claude/skills/`、`CLAUDE.md`、hooks、MCP設定）がCoworkに自動共有されるか。ある解説記事は共有されると書くが、同じ記事に公式と食い違う記述がある。
- ZedからClaude CodeをACP経由で呼ぶ構成の細部。CoworkがWSL側のファイルを扱えるか（Windows側のフォルダに置くのが無難）。
- Coworkの Windows対応の詳細（エディション条件など）は一次情報で確認できていない部分がある。

## Gotchas

### WSLから `/mnt/c` を触ると遅い

- WSLを使うなら、リポジトリはWSL側に置くのが前提（[[wsl-file-placement]]）。

### WindowsネイティブにはLibreOffice前提の `recalc.py` がそのまま使えない

- 解決: LibreOffice（`soffice --headless --convert-to xlsx`）か、pywin32のExcel COM（`CalculateFull`）で再計算する。どちらも使えなければ、再計算できていないことを報告し、Excelで開いて保存してもらう。

### `data_only=True` で開いたブックを保存すると、数式がすべて値に置き換わる

- 解決: 値の読み取り専用にし、保存しない。

### CSVの文字コード

- Excel由来のCSVは `cp932` のことが多い。UTF-8（BOMなし）のCSVをExcelで開くと文字化けする。解決: 読み込みは `cp932`、書き出しは `utf-8-sig`。

### 先頭ゼロや長い数字が数値化されて崩れる

- 解決: `dtype=str` で読む。

### 範囲のずれはエラーなしで数字だけ狂う

- 解決: 数式を2〜3個書いた段階で、pandasなどの独立計算と突き合わせてから展開する。

## Open Questions

- 実際の業務環境にLibreOfficeとExcelのどちらが入っているか。Excel COM（pywin32）を会社の端末で使えるか。
- 現在のExcel集計表で、Master（データ羅列）とview（可視化）の分離がどこまでできているか。
- Coworkを使う場合、WSLのファイルやCode用スキル資産を共有できるか。Cowork標準スキルの品質は自作スキルで足りるか。
- Coworkを導入する場合のエディション、管理者権限、ネットワーク統制の条件を満たせるか。

## Next Actions

1. `excel-aggregation/SKILL.md` を `%USERPROFILE%\.claude\skills\excel-aggregation\` かプロジェクトの `.claude\skills\excel-aggregation\` に置く（現在は未配置）。
2. 実際の集計表のコピーを `work/` に置き、「viewシートに○○別の合計を数式で追加して」のような小さな依頼で試す。
3. 再計算の手段（LibreOffice / Excel COM）が動くか確認する。
4. Coworkを後で試す場合は、エディション（Hyper-V）、管理者権限、Claude Desktopの.msix版を先に確認する。
5. 公式xlsxスキルの更新を時々確認し、差分を反映する。

## Related

- [[office-ai-workspace]]
- [[ai-harness-concepts]]
- [[claude-code-storage]]
- [[ai-handson-framework]]
