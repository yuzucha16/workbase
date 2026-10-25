# リポジトリ間の整合の基準（alignment-baseline）

workbase（`resources/`）、works、dotfiles の運用を揃えるための基準。正は workbase（祖）。`review` の入力 8（`workflow-kit/review-hook.md`）が、各行を今の状態と比べ、違う行だけを見直しとして挙げる。見直しの後は、この表を更新し、基準日を直す。

works は PARA の作業場、workbase は共有ナレッジ、dotfiles は設定で、目的が違う。同じ項目でも、ゴールの違いから差が出てよい行がある。それは「違ってよい行」に分け、ギャップに数えない。

基準日: 2026-10-25（works の `docs/alignment-baseline.md` から移した。移す前の基準日は 2026-10-16）

## 共通の項目（揃える）

| 項目 | 期待 | works | workbase | dotfiles |
|---|---|---|---|---|
| `CLAUDE.md` が `@AGENTS.md` の1行 | 3つとも | ○ | ○ | ○ |
| 共通ルールのポインタ | `workflow-kit` を指す | ○ | ○ | ○ |
| 窓口 `README.md` | あり | ○ | ○ | ○（16KB 目安） |
| 直下の `docs/log.md` | あり。4KB 目安（`docs-rules.md`） | 2.8KB | 18KB（超過。ギャップ 9） | 1.0KB |
| 読む順番 | 3段（README、log、検索のみ） | ○ | ○ | ○ |
| 「〜の続き」の扱い | `docs-rules.md` を参照する1行 | ○ | ○ | ○ |
| 期日の節 | `docs/log.md` に置く（項目が無ければ「なし」） | ○ | ○ | ○ |
| `settings.local.json` を追跡しない | 3つとも | ○ | ○ | ○ |
| 公開範囲 | 公開（PUBLIC）。変えるときはユーザーの決定 | PUBLIC | PUBLIC | PUBLIC |
| push の許可リスト | `main` を許可 | ○ | ○ | ○ |
| `main` と `origin/main` | 同じ（作業中の未 push は除く） | 同じ | 2 先 | 3 先 |

## 違ってよい行（ゴールの違い。ギャップに数えない）

| 項目 | works | workbase | dotfiles |
|---|---|---|---|
| 目的 | PARA の作業場（この PC のローカルの作業） | 共有ナレッジと共通機能（祖） | 設定の置き場 |
| 下位の単位 | `projects/` `areas/` `archives/` | `exmem/` `workflow-kit/` `guides/` `topics/` | なし |
| `.claude/` | `settings.json`（deny）を追跡 | 追跡するものなし | 追跡するものなし |
| AI 作業部屋の扱い | 使う。`projects/` `areas/` `archives/` は部屋の中で扱う | 部屋の道具（`room`）を持つ | － |
| 振り返りのゴール | この PC の作業の進め方 | 仕組み（kit）の改善 | 設定の維持 |

## 点検の対象

`review` の入力 3（`exmem/inbox/` の未統合メモ、`decisions.md` の `→` の無い【汎用】項目）、入力 4（トピックの点検）、入力 6（機密の点検）が、どのリポジトリから起動しても見る対象（2026-10-16 ユーザーの決定）。パスは、works のトップから見た相対パス。`git -C <パス>` で検索する。

| リポジトリ | パス（works から） | 公開範囲 |
|---|---|---|
| works | `.` | PUBLIC |
| workbase | `resources` | PUBLIC |
| dotfiles | `repos/github.com/yuzucha16/dotfiles` | PUBLIC |

works が無い環境（workbase だけを clone したとき）は、workbase だけを対象にし、他は「無い」と報告する。

## ギャップ

| # | 内容 | 状態 | 影響 | リスク |
|---|---|---|---|---|
| 1 | workbase に `docs/log.md` がない | 解消 | 中 | 低 |
| 2 | 読む順番の形が3通り | 解消 | 高 | 低 |
| 3 | 「〜の続き」の規則が `topics/AGENTS.md` にしかない | 解消（kit に1か所） | 高 | 低 |
| 4 | `guides` と `handson` が `CLAUDE.md` だけ | 解消（2026-10-16） | 低 | 低 |
| 5 | 期日の節が works にしかない | 解消（2026-10-16） | 低 | 低 |
| 6 | `.claude/` の扱いの違い、works に deny がない | 解消 | 中 | 中 |
| 7 | works の `AGENTS.md` と雛形のずれ | 解消 | 低 | 低 |
| 8 | 公開リポジトリの git 履歴にユーザー名を含むパスが残っている | 未着手（書き換えは force push が要り、禁止） | 中 | 高 |
| 9 | workbase の `docs/log.md` が 18KB で、4KB 目安の約 4.5 倍 | 残す（次の `wrap` で縮める。ユーザーの指示、2026-10-25） | 中 | 低 |
| 10 | dotfiles の `docs/log.md` から期日の節が無くなった | 解消（2026-10-25。節を戻した） | 低 | 低 |
| 11 | works の `docs/metrics/README.md` が、削除済みの `init-hook.md` を名指ししている | 解消（2026-10-25。廃止と注記した） | 低 | 低 |
| 12 | 基準が works にあり、workbase の `review` が単独で入力 8 を行えない | 解消（2026-10-25。この文書へ移した。ユーザーの決定） | 高 | 低 |
