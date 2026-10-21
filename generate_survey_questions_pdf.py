import os
import subprocess

OUTPUT_DIR = os.path.expanduser("~/Desktop/KidsRide/KidsRide_アンケート資料")
os.makedirs(OUTPUT_DIR, exist_ok=True)

html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>三鷹市 保護者送迎実態調査 調査票（設問一覧）</title>
<style>
  @page {
    size: A4 portrait;
    margin: 12mm 15mm 12mm 15mm;
  }
  * {
    box-sizing: border-box;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    line-height: 1.45;
    font-size: 8.5pt;
    margin: 0;
    padding: 0;
  }
  .header {
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .doc-title {
    font-size: 12.5pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 0.5px;
  }
  .doc-subtitle {
    font-size: 8.5pt;
    color: #0284c7;
    font-weight: 700;
    margin-top: 2px;
  }
  .meta-info {
    text-align: right;
    font-size: 7.8pt;
    color: #475569;
    line-height: 1.4;
    white-space: nowrap;
  }
  .intro-box {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 6px;
    padding: 7px 12px;
    margin-bottom: 10px;
    font-size: 8pt;
    line-height: 1.45;
  }
  .section-badge {
    display: inline-block;
    background: #0284c7;
    color: #ffffff;
    font-weight: 800;
    font-size: 8pt;
    padding: 2px 8px;
    border-radius: 3px;
    margin-top: 8px;
    margin-bottom: 5px;
  }
  .q-card {
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 6px 10px;
    margin-bottom: 6px;
    background: #ffffff;
    page-break-inside: avoid;
  }
  .q-title {
    font-weight: 700;
    font-size: 8.3pt;
    color: #0f172a;
    margin-bottom: 3px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .q-tag {
    font-size: 7pt;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    background: #e0f2fe;
    color: #0369a1;
  }
  .opt-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2px 10px;
    font-size: 7.9pt;
    color: #334155;
    margin-top: 2px;
  }
  .opt-item {
    display: flex;
    align-items: flex-start;
    gap: 4px;
  }
  .page-footer {
    border-top: 1px solid #e2e8f0;
    margin-top: 8px;
    padding-top: 5px;
    font-size: 7.5pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
  }
  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

<!-- ==================== 1ページ目 ==================== -->
<div class="header">
  <div>
    <div class="doc-title">【三鷹市・子育て世帯対象】子どもの通園・送迎に関する実態調査</div>
    <div class="doc-subtitle">Webアンケート設問一覧・調査票設計書（完全無記名方式・所要時間約2分）</div>
  </div>
  <div class="meta-info">
    <div>実施主体: 一般社団法人KidsRide</div>
    <div>代表理事: 七夕 光明（三鷹市下連雀在住）</div>
    <div>回答URL: https://www.kidsride.jp/#survey</div>
  </div>
</div>

<div class="intro-box">
  <strong>【調査趣旨および市役所へのデータ共有について】</strong><br>
  本アンケートは、三鷹市における保育園・幼稚園・学童等の通園・送迎の実態と保護者ニーズを把握し、地域での安全な送迎互助体制の構築および三鷹市役所子ども育成課への政策提案基礎資料として活用するために実施するものです。個人情報の入力は一切不要（完全無記名）であり、統計処理の上で市役所子ども育成課へもデータを共有いたします。
</div>

<div class="section-badge">1. 基本属性</div>

<div class="q-card">
  <div class="q-title">
    <span>Q1. お子様の年齢（学年）を教えてください（複数いらっしゃる場合はすべて選択）</span>
    <span class="q-tag">必須 / 複数選択</span>
  </div>
  <div class="opt-grid">
    <div class="opt-item">□ 0〜1歳（乳児）</div>
    <div class="opt-item">□ 2〜3歳（年少少・年少）</div>
    <div class="opt-item">□ 4〜5歳（年中・年長）</div>
    <div class="opt-item">□ 小学校低学年（1〜3年生）</div>
    <div class="opt-item">□ 小学校高学年（4〜6年生）</div>
  </div>
</div>

<div class="q-card">
  <div class="q-title">
    <span>Q2. 普段の主な送迎・通園手段は何ですか？</span>
    <span class="q-tag">必須 / 複数選択可</span>
  </div>
  <div class="opt-grid">
    <div class="opt-item">□ 自転車（子ども乗せ・電動アシスト含む）</div>
    <div class="opt-item">□ 徒歩</div>
    <div class="opt-item">□ 自家用車</div>
    <div class="opt-item">□ バス・公共交通機関</div>
    <div class="opt-item">□ その他（自由記述）</div>
  </div>
</div>

<div class="section-badge">2. 園選び・保活における「送迎の壁」</div>

<div class="q-card">
  <div class="q-title">
    <span>Q3. 園選び（保活等）の際、「毎日の送迎が難しい」という理由で第一希望の園を諦めたり外した経験はありますか？</span>
    <span class="q-tag">必須 / 単一選択</span>
  </div>
  <div style="font-size:7.9pt; color:#334155; line-height:1.4; margin-top:2px;">
    <div>○ <strong>ある</strong>（送迎の距離や手段・時間の都合で、第一希望を諦めて別の園にした）</div>
    <div>○ <strong>諦めはしなかったが非常に迷った</strong>・現在も無理をして通わせている</div>
    <div>○ <strong>なかった</strong>（通いやすい園が第一希望だった）</div>
    <div>○ その他（自由記述）</div>
  </div>
</div>

<div class="q-card">
  <div class="q-title">
    <span>Q3-付問. （上記で「ある」「非常に迷った」方へ）具体的にどのような点がネックになりましたか？</span>
    <span class="q-tag" style="background:#f1f5f9; color:#475569;">任意 / 自由記述</span>
  </div>
  <div style="font-size:7.8pt; color:#64748b; margin-top:1px;">
    （例：自宅からの距離、坂道、雨の日の移動、勤務先の始業・終業時間との兼ね合い 等）
  </div>
</div>

<div class="section-badge">3. 日頃の送迎のお困りごと・潜在ニーズ</div>

<div class="q-card">
  <div class="q-title">
    <span>Q4. 日頃の通園・送迎において、「調整が大変だ」「困った」と感じる頻度はどれくらいですか？</span>
    <span class="q-tag">必須 / 単一選択</span>
  </div>
  <div class="opt-grid">
    <div class="opt-item">○ ほぼ毎日感じる</div>
    <div class="opt-item">○ 週に1〜2回程度感じる</div>
    <div class="opt-item">○ 月に数回程度感じる</div>
    <div class="opt-item">○ 年に数回・ごく稀にある</div>
    <div class="opt-item">○ 困ったことはほとんどない</div>
  </div>
</div>

<div class="q-card">
  <div class="q-title">
    <span>Q5. 特に送迎で「困る・助けてほしい」と感じるシチュエーションは何ですか？</span>
    <span class="q-tag">必須 / 複数選択可（最大3つ）</span>
  </div>
  <div class="opt-grid">
    <div class="opt-item">□ 急な仕事の残業、突発的な会議や外出</div>
    <div class="opt-item">□ きょうだいの急な発熱・通院・看病</div>
    <div class="opt-item">□ 雨・雪・強風・猛暑などの悪天候</div>
    <div class="opt-item">□ 保護者自身の体調不良・ケガ・通院</div>
    <div class="opt-item">□ 習い事の開始時間とお迎え時間の重複</div>
    <div class="opt-item">□ 朝の出勤時間と登園時間のスケジュール調整</div>
  </div>
</div>

<div class="q-card">
  <div class="q-title">
    <span>Q6. 送迎に困った際、これまでにどのように対処・解決してきましたか？</span>
    <span class="q-tag">必須 / 複数選択可</span>
  </div>
  <div class="opt-grid">
    <div class="opt-item">□ 仕事を無理に切り上げて急いで対応した</div>
    <div class="opt-item">□ 祖父母・親族に急遽お願いした</div>
    <div class="opt-item">□ 園のママ友・パパ友にお願いした</div>
    <div class="opt-item">□ ファミリー・サポート・センターを利用した</div>
    <div class="opt-item">□ ベビーシッター・民間送迎サービスを利用</div>
    <div class="opt-item">□ タクシー等を利用した</div>
    <div class="opt-item">□ 解決できず、園に謝罪して遅れて迎えに行った</div>
  </div>
</div>

<div class="page-footer">
  <div>一般社団法人KidsRide（三鷹市下連雀）/ お問い合わせ: info@kids-ride.jp</div>
  <div>1 / 2 ページ（※三鷹市子ども育成課へのデータ共有を前提とした完全無記名調査）</div>
</div>

<!-- ==================== 2ページ目 ==================== -->
<div class="page-break"></div>

<div class="header">
  <div>
    <div class="doc-title">【三鷹市・子育て世帯対象】子どもの通園・送迎に関する実態調査（続き）</div>
    <div class="doc-subtitle">Webアンケート設問一覧・調査票設計書（Q7〜Q12）</div>
  </div>
  <div class="meta-info">
    <div>一般社団法人KidsRide（三鷹市下連雀）</div>
    <div>https://www.kidsride.jp/#survey</div>
  </div>
</div>

<div class="section-badge">4. 送迎助け合い・地域連携サービスへの受容度</div>

<div class="q-card">
  <div class="q-title">
    <span>Q7. もし「同じ園の身元確認済み保護者同士」で送迎を助け合える仕組み（※損保補償付き）があれば利用したいですか？</span>
    <span class="q-tag">必須 / 単一選択</span>
  </div>
  <div class="opt-grid">
    <div class="opt-item">○ ぜひ定期的に利用したい</div>
    <div class="opt-item">○ 急な残業や困った時だけ単発で利用したい</div>
    <div class="opt-item">○ 条件や相手（顔見知りか等）次第で検討</div>
    <div class="opt-item">○ あまり利用したいとは思わない / わからない</div>
  </div>
</div>

<div class="q-card">
  <div class="q-title">
    <span>Q8. 【三鷹駅前一時預かり連携】子ども家庭支援センター「のびのびひろば（最大夜22時まで）」等への送迎連携があれば利用したいですか？</span>
    <span class="q-tag">必須 / 単一選択</span>
  </div>
  <div style="font-size:7.9pt; color:#334155; line-height:1.4; margin-top:2px;">
    <div>○ <strong>ぜひ利用したい</strong>（急な残業や夜遅くなる日に非常に助かる）</div>
    <div>○ <strong>状況によっては利用したい</strong>（数か月に数回程度、残業や通院時など）</div>
    <div>○ そもそも最大夜22時まで預けられる制度（のびのびひろば・トワイライトステイ）を<strong>知らなかった</strong></div>
    <div>○ 利用しない（現在の園の延長保育や家庭内で対応できている）</div>
  </div>
</div>

<div class="q-card">
  <div class="q-title">
    <span>Q9. 他の保護者にお子様の送迎をお願いする場合、どのような手段であれば安心できますか？</span>
    <span class="q-tag">必須 / 複数選択可</span>
  </div>
  <div class="opt-grid">
    <div class="opt-item">□ 徒歩での引率（手つなぎ・見守り歩行）</div>
    <div class="opt-item">□ 自転車での送迎（幼児同乗器・ヘルメット）</div>
    <div class="opt-item">□ 自家用車での送迎（適合チャイルドシート）</div>
    <div class="opt-item">□ 同じクラスや顔見知りの保護者であれば安心</div>
    <div class="opt-item">□ リアルタイムで現在地がGPS追跡できれば安心</div>
    <div class="opt-item">□ どのような手段であっても不安がある</div>
  </div>
</div>

<div class="section-badge">5. 送迎サポーター（助け手）としての関心・自由記述</div>

<div class="q-card">
  <div class="q-title">
    <span>Q10. ご自身のお子様を送迎する「ついで」に、同じ園のお子様を一緒に送迎することに関心はありますか？</span>
    <span class="q-tag">必須 / 単一選択</span>
  </div>
  <div class="opt-grid">
    <div class="opt-item">○ ついでであれば協力したい（困った時はお互い様）</div>
    <div class="opt-item">○ タイミングや都合が合う日なら引き受けてもよい</div>
    <div class="opt-item">○ 興味はあるが責任や事故が心配</div>
    <div class="opt-item">○ 自分は「頼む側」専任で利用したい / 余裕はない</div>
  </div>
</div>

<div class="q-card">
  <div class="q-title">
    <span>Q11. 子どもの通園・送迎に関して「こんなサポートがあったら助かる」というご要望や日頃のお悩み（自由記述）</span>
    <span class="q-tag" style="background:#f1f5f9; color:#475569;">任意 / 自由記述</span>
  </div>
  <div style="height:36px; border:1px dashed #cbd5e1; border-radius:4px; margin-top:3px; background:#f8fafc; padding:4px; font-size:7.5pt; color:#94a3b8;">
    （自由記入欄：日頃感じている送迎の負担や、行政・地域に求めるサポートについてご自由にお書きください）
  </div>
</div>

<div class="q-card">
  <div class="q-title">
    <span>Q12. 今後実施予定の「無料実証実験（モニター体験）」の優先案内を希望される方の連絡先</span>
    <span class="q-tag" style="background:#f1f5f9; color:#475569;">任意</span>
  </div>
  <div style="font-size:7.8pt; color:#64748b; margin-top:2px;">
    メールアドレス記入欄（※ご記入いただいたアドレスは実証実験の案内のみに使用し、アンケート回答の統計処理とは完全に分離管理されます）
  </div>
</div>

<div class="page-footer">
  <div>一般社団法人KidsRide（三鷹市下連雀）/ お問い合わせ: info@kids-ride.jp</div>
  <div>2 / 2 ページ（※三鷹市子ども育成課へのデータ共有を前提とした完全無記名調査）</div>
</div>

</body>
</html>
"""

html_path = os.path.join(OUTPUT_DIR, "三鷹市_保護者送迎実態調査_アンケート設問一覧.html")
pdf_path = os.path.join(OUTPUT_DIR, "三鷹市_保護者送迎実態調査_アンケート設問一覧.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print(f"成功: {pdf_path}")
else:
    print(f"失敗: {res.stderr}")
