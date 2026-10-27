# 作業ログの経緯（log-history）

## Log

### 2026-10-25（実機なしで進めた分: 診断ログ・run.py・ps1 版・原因の台帳）
- ユーザーの依頼「実機なしでできるアイテム」で、承認済みの範囲を進めた。`script-guide.md` に `run.py` の型と ps1 版（`verify.ps1` `release.ps1`）、「原因の台帳」の節を足し、`room-context.md` に1項、`check_py.py` `check-ps1.ps1` に結果ファイルと名前の点検を足した。診断ログは `diag.json` でなく `<名前>-result.json`（毎回出す）にした。台帳の実装はユーザーの承認（「今実装する」）を受けた。Linux の Python 3.13 と pwsh 7.4 で確認、Windows は未確認。コミット `483abea` `0c808b5` `f7e4d7a`（決定は root の `decisions.md` と、このトピックの `decisions.md`）。
- 触らなかった実機の項目: `verify.bat` / `verify.ps1` の Windows での実行、`mkworks` の実機確認、`stock` の `scope: area` の実機確認、旧名の注記の削除、dotfiles のスキルの入口。

### 2026-10-24（Windows 実行のデバッグのラリー）
- ユーザーの依頼で、room の機密性と Windows 作業の効率の妥協点を相談した。他エージェントのレビュー（案 A〜D）を公式文書と現行の room で照らし、`interop` の有効化は却下のまま、境界は変えないと整理した。ユーザーの回答（主因は環境の違い、COM は未使用、別ユーザー・Sandbox は不可）で、案をログ取りと原因の蓄積に絞った。works 共通の置き場は、`stock` の `scope: area` と公開の経路で足りるとして作らないことにした（弱点2つは許容）。仮決めして `review 消化` の待ち行列に置いた。決定は `docs/decisions.md` の同日の項。実装は未着手。
### 2026-10-24（`stock` の行き先）
- ユーザーの依頼で、PC1 の業務で出る、workbase に戻せない業務固有の知の置き場と `room stock` の変更を相談した。最初の叩き台（works 直下に Area を跨ぐ置き場を作る）は、ユーザーの「非公開の共有知は Area に閉じてよい。土台はすでにある」で取り下げ、第2版（`pull` `restore` `ai/out/knowledge/` を土台に、入口だけ統一）で仮決め4点がOKになった。実装した: 下書きの `scope: public | area`、`room stock` は `area` を運ばない。決定は `docs/decisions.md` の同日の項。`room pull --where` の仕様は変えるかもしれない（予告）。

### 2026-10-24
- ユーザーの依頼で、`room` の導入によって名前や工程が重なった `init` `open` `start` のフックを見直した。事実の表（フック ↔ `room` コマンド）を作り、論点と案を出した（[[hook-room-alignment-notes]]）。
- ユーザーが、`init` は人がやる操作なので `room` に取り込む（`room mkworks`、`--update`。将来 `--list` など引数で足す）、他リポジトリへの導入と履歴復元は廃止（`kit` は作らない）、`open` と `close` は畳む、`start` は改名してよい、と決めた。`start` の名前は `brief` で承認。
- 実装して push した: `a015bda`（`mkworks` とテスト 12 件）、`c771c01`（`init` `open` の廃止と文書の直し）、`45ee732`（`start` → `brief`）。単体テスト 137 件と `check_hook_outline` は通った。`mkworks` の実機は未確認。
- ユーザーが、過去の記録の旧名は、現在の仕様が回りだしたら読み替えごと消すと決めた。フックと `room` の調整は継続する。
- 残りのフックと `room` の整合を調べた。名前の重なりは `stock` と `room stock` だけで、同じ1件のメモの前半（AI の下書き）と後半（人の運搬）なので意図どおり。`integrate` `review` は部屋で行わず、重なりなし。抜けは `hooks.md` の room 表だけ。
- ユーザーが、表はフックと対のものだけに絞る（案A）、`stock` の行に `room stock` を足す、`wrap` のコミットは AI が行う（部屋では指示なしで部屋の git に。push はしない。works へのコミットは人の `room start` の回収）、と決めた。決定は root の `docs/decisions.md` の同日の項。
- ユーザーの指示で、`brief 変更`（別名「変更で始めて」。やり方は変更1だけなので選ばせず、前提チェックから）を `brief-hook.md` の引数つきモードに足した。あわせて、`brief-hook.md`（5,042 字）と `review-hook.md`（5,056 字）を、内容を変えずに言い回しだけ詰めて 5,000 字以下にした。
- 2026-10-27: ユーザーが、診断ログと原因の台帳の承認待ち、および `room mkworks --update` の試行を、実施済み・問題なしとして close した。仮決めを確定にし、窓口の「あなた待ち」を空にした。
