# exmem の定義から漏れるものの洗い出し（叩き台）

> 注記（2026-10-26）: 置き場の名前は `ledger/` ではなく **`logbook/`** に決まった（仮決め）。この記録は議論の途中の版で、決定は `../docs/decisions.md` が正本。

- 日付: 2026-10-26。対象: `exmem/lessons/` の 69 ファイル（`exmem/inbox/` は空）。
- 方法: ファイル名・title・節の構成・「時点」「確認: 日付」「Next Actions」の数・サイズで仕分けた。**全文は読んでいない**。疑いの高い 5 件は節の見出しまで確認。ほかは title からの推測を含むので、移すときに本文を見て確かめる。
- 判定の物差し（exmem の定義 + 今回の「期限のある」）: 次のどれかに当たると「漏れ」の候補にする。
  - T 時系列: 時間とともに値が変わる観察・測定・傾向
  - V 版依存: ツールの版・時点に縛られる事実で、古くなると誤りになる
  - P 個人の好み: ユーザー 個人の選定・好み（AI の今後の参考にする原則ではない）
  - W 作業中: Open Questions / Next Actions が主で、まだ知識になっていない
  - S 種・素材: 知識ではなく、ほかの道具に渡す元データ

## 1 漏れの候補（確度つき）

| 区分 | ファイル | サイズ | 理由 | 行き先の案 |
|---|---|---|---|---|
| T（高） | `user-thinking-habits.md` | 31KB | 思考の癖の分析の明細。分析のたびに増える。取扱説明書（`user-manual.md`）が原則を持つ | 明細を logbook へ降格。原則は user-manual |
| T（高）| `user-manual.md` の Facts | 18KB のうち一部 | 観察の積み上げ。Principles と Decisions は残す | Facts のみ降格 |
| T（高） | `ai-work-metrics.md` | 12KB | 指標の値と「終了のたびに1行記録」の運用。Next Actions 4 件が試行中 | 値と記録を logbook へ。指標の構成（決定）は残す |
| T（中） | `shell-command-usecases.md` | 27KB | 「傾向（2026-10-04 時点）」と履歴の種（約 400 行）。種は dotfiles の道具に渡す素材 | 傾向は logbook。種は S（下） |
| S（高） | 同上の「履歴の種」 | 約 15KB | 知識でなく元データ。dotfiles 側の履歴に入れる種 | 置き場の検討が別途要る（logbook 向きではない） |
| V（高） | `claude-code-storage.md` | 27KB | 「2026-10-01 時点で確認済み」、追記が 3 回（10-07、10-18）。Next Actions に確認待ちが 4 件。公式は「形式は版ごとに変わる」 | 版依存の事実は logbook（期限つき）、変わらない原則だけ残す |
| V（中） | `claude-code-auth-providers.md` | 29KB | 認証経路とモデル指定は版・契約で変わる。Next Actions 4 件 | 同上 |
| V（中） | `linux-distro-selection.md` | 7KB | 「2026年10月時点」のバージョン比較（Neovim、Fedora、Zed の apt）。選定の原則は残る | 比較表を logbook、判断基準は残す |
| V（中） | `obsidian-vault.md` | 56KB | 「時点」16 回、確認 11 回。サイズも大きい | 本文を見て仕分け（版依存の節を logbook） |
| V（中） | `ai-isolated-work-room.md` | 58KB | 「時点」15 回、確認 48 回、Next Actions 9 件。実装が動いていて、状態が変わり続ける | 決定・原則は残し、状態と実測を logbook |
| V（中） | `shell-script-testing-wsl.md` | 41KB | 確認 34 回。WSL の挙動の実測 | 実測の節を logbook |
| V（低〜中） | `workflow-kit.md` | 60KB | kit の説明が lessons に 60KB。正本は `workflow-kit/` 側のはず。「時点」6 回 | 正本との重複を先に点検（降格より削除の可能性） |
| P（中） | `keyboard-switches.md` | 9KB | 個人の好みと購入判断 | AI の参考になる原則が無ければ exmem 外。残すなら `guides/` かどちらも不要 |
| P（中） | `linux-multiboot-setup.md` | 6KB | 256GB SSD の特定構成のインストール記録 | 1 回きりの記録。`guides/howto` か削除 |
| P（低） | `fonts.md`、`notepad-plus-plus.md`、`zed-vim.md`、`zed-dotfiles.md`、`scoop-app-management.md` | 8〜17KB | 個人の環境設定の判断。dotfiles 側の判断と重なる | 本文を見て、dotfiles との重なりを確認 |
| W（中） | `para-operations.md` | 16KB | Next Actions 5 件、「2回目の Project を試す」など運用試行の途中 | 試行が済んだら原則だけ残す。経緯は logbook か削除 |
| W（中） | `session-handoff.md` | 19KB | Next Actions 4 件、確認 13 回 | 同上 |
| W（低） | `retrospective-method.md` | 25KB | 【仮】あり。試行中の手順書（`topics/kit-growth/records/` に記録も別にある） | 手順書としては残す。記録部分は既に kit-growth |
| 参考 | `ai-handson-framework.md` | 9.5KB | 「情報ダイジェスト」の設計。ダイジェスト部分は時事の可能性 | 本文を見る |

## 2 漏れではなさそうなもの（参考）

原則・判断基準が中心で、期限が来ても使えるもの: `accretion-without-pruning`、`human-ai-decision-loop`、`ai-output-consistency`、`layered-third-party-review`、`method-creation`、`change-method`、`improvement-*`、`problem-solving-*`、`research-method*`、`retrospective-method-2`、`reference-doc-types`、`app-config-placement`、`git-*`、`windows-cli-pitfalls`、`embedded-c-constraint-checks`、`excel-vba-ai-development`、`session-goal-modes` など。

## 3 例の外にある「期限のあるナレッジ」の種類（lessons の外も含む）

ユーザーの 4 例のほかに、今回見つかった型:

1. **版・時点に縛られる事実**（上の V）: ツールの仕様、バージョン比較、認証・保存場所。古くなると誤りになるので、期限（`review_by`）が最も効く。
2. **計測値・傾向**（T）: 指標、コマンドの利用傾向、引き当て率（`triggers_stats`）、heavy_sessions の結果。
3. **試行中の手順の記録**: 「3 回使うまで試験運用」の使った回数、品質チェックの run（`kit-growth/records/` にすでにある）。
4. **PC・環境ごとの確認結果**: 「PC2 で verify を 1 回」など実機確認の結果。
5. **素材**（S）: 履歴の種、dotfiles に渡す元データ。期限というより「消費したら消える」型。logbook とは別の扱いが要るかもしれない。
6. **docs 側の肥大物**: `docs/decisions.md`（195KB）、`docs/log-history.md`（181KB）。開始時に読まないだけで、畳む経路は無い。logbook の対象にするかは別判断。

## 4 気づき

- 全体の約 4 分の 1（20 件弱）に何らかの漏れの兆候がある。ただし多くは「ファイル全体」でなく「節」の問題なので、**降格の単位はファイルでなく節**になる。logbook 側のファイルは、元の lesson と同じ名前に `-log` を付けて対にする案（例: `claude-code-storage-log.md`）が、リンクを追いやすい。
- 「立ち上げフェーズで何でも stock した」ため、版依存と個人の好みが多い。`integrate` に「期限があるか」の判定（frontmatter `horizon` か `review_by` の有無）を足せば、入口で防げる。これは導入後の話。
- サイズ上位（workflow-kit 60KB、ai-isolated-work-room 58KB、obsidian-vault 56KB）は漏れというより別の問題（大きすぎ）かもしれない。降格で縮むかは本文を見ないと判断できない。

## 5 次に決めてほしいこと

1. この仕分けで、本文を見て確定させる範囲（全件か、確度「高」だけか）。
2. S（種・素材）を logbook に入れるか、別の扱いにするか。
3. 降格は承認プロセスの 3 段チェックに載せる（ユーザーの決定）。1 件ずつ載せると多いので、節単位でまとめて載せる単位を決める。
