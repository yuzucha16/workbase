# 共有知の写しを部屋へ入れる: PC への引き継ぎ（2026-10-13）

ロードマップ2番（方式 A）を実装した。**単体テスト（40件）まで。実際の WSL では未確認**。

## できたもの

- `room start` が、マウントの前に `<Vault>/resources/` の `AGENTS.md`、`workflow-kit/`、`exmem/{AGENTS.md,README.md,tags.md,lessons/}`、`guides/` を tar.gz にして、部屋の一般ユーザーの `~/shared` へ送る。読み取り専用（`chmod -R a-w`）。次の起動で入れ替える（先に `u+w` に戻して消す）。
- 基準コミットと「未コミットの変更の有無」を、`ai/records/manifest.json` の `shared` に記録。`~/shared/ROOM.md` に、基準コミットと読む場所の案内、`stock` の下書きの書き方（`ai/out/stock/`、ヘッダーに基準コミットと観測日）を置く。
- `resources/` が無い Vault では、送らずに続ける。

## PC で確認すること

1. 実際の部屋で `room start` → 部屋の AI が `~/shared/ROOM.md` と `~/shared/workflow-kit/hooks.md` を読めるか。書き込めないか。
2. 送る時間とサイズ（`guides/` と `lessons/` が増えたとき）。遅ければ、範囲を絞るか差分にする。
3. `resources/` の位置が、PC の Vault（`$HOME\works\resources`）と合っているか。
4. 部屋の `~/CLAUDE.md` などから `~/shared/ROOM.md` へ案内する（部屋の作成手順に足す。未実施）。
5. 部屋の AI が、合言葉（`start` `wrap` など）で `~/shared/workflow-kit/*-hook.md` を読んで動けるか（`pwsh` 製の道具は動かない）。

## 未決（変わらず）

下書きのヘッダー項目と `check-inbox.ps1` の整合、`review` の記録の置き場、下書きの回収（ロードマップ4番）。
