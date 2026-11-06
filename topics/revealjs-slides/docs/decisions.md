# 判断の記録（decisions）

## Decisions

### 【この件】トピック `revealjs-slides` を Project 型で起こす（2026-11-06）
- ユーザーの発言: 「トピックを起こしましょう。pc1でも初めての試みでまだ立ち上げ状態です。」「進んでください。」
- 決めたこと: 簡易スライド（Quarto → revealjs）の図解レイアウトを、新しいトピックで育てる。完了条件は、inv 型の成果物に revealjs の HTML スライドを作る土台ができること。正式な pptx は `office-output-types` で別に扱う。
- 根拠: 確定ではなく拡張していく土台で、経緯と部品（見本・CSS）を置く場所が要るため。

### 【この件】置き場: 型・原則は lessons、見本と CSS はトピックの records（2026-11-06）
- ユーザーの発言: 「その案にします。」「コミットします。」
- 決めたこと: 型・原則・落とし穴を `exmem/lessons/revealjs-diagram-layout-output.md` に統合し、見本と CSS は `records/` に置いたままにする。写真フォルダはユーザーが削除した。
- 根拠: 部品（約 20KB の見本）を lessons に入れると読み込みが重くなる。

