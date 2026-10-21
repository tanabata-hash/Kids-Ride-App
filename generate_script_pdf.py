import os
import subprocess

OUTPUT_DIR = os.path.expanduser("~/Desktop/KidsRide/市役所説明資料")
os.makedirs(OUTPUT_DIR, exist_ok=True)

html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>三鷹市役所 事前相談 15分トークスクリプト（完全カンペ）</title>
<style>
  @page {
    size: A4 portrait;
    margin: 12mm 14mm 12mm 14mm;
    @bottom-right {
      content: counter(page);
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
  }

  .page-break {
    page-break-before: always;
  }

  /* タイトルヘッダー */
  .header-box {
    background: linear-gradient(135deg, #1e3a8a 0%, #0369a1 100%);
    color: #ffffff;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
  }
  .header-title {
    font-size: 14pt;
    font-weight: 800;
    margin: 0 0 4px 0;
  }
  .header-meta {
    font-size: 8.5pt;
    opacity: 0.95;
    display: flex;
    justify-content: space-between;
  }

  /* 持ち物＆タイムテーブル */
  .meta-grid {
    display: grid;
    grid-template-columns: 1.1fr 1.3fr;
    gap: 10px;
    margin-bottom: 12px;
  }
  .meta-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 8.5pt;
  }
  .meta-card strong {
    color: #1e3a8a;
    display: block;
    margin-bottom: 4px;
    font-size: 9pt;
  }

  /* セクション見出し */
  .section-title {
    font-size: 11pt;
    font-weight: 800;
    color: #1e3a8a;
    border-left: 4px solid #0284c7;
    padding-left: 8px;
    margin: 12px 0 6px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .time-badge {
    background: #e0f2fe;
    color: #0369a1;
    font-size: 8pt;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 12px;
  }

  /* セリフ吹き出しボックス */
  .script-box {
    background: #ffffff;
    border: 1.5px solid #93c5fd;
    border-left: 5px solid #2563eb;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 10px;
    font-size: 9.2pt;
    line-height: 1.6;
    color: #0f172a;
  }
  .script-box p {
    margin: 0 0 6px 0;
  }
  .script-box p:last-child {
    margin-bottom: 0;
  }
  .action-note {
    font-size: 8.3pt;
    color: #c2410c;
    font-weight: 700;
    margin-bottom: 4px;
  }

  /* Q&Aカード */
  .qa-card {
    background: #fdfefe;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 7px 10px;
    margin-bottom: 6px;
    font-size: 8.6pt;
    line-height: 1.5;
  }
  .qa-q {
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 3px;
  }
  .qa-a {
    color: #334155;
  }

  .highlight {
    background: #fef08a;
    font-weight: 700;
    padding: 0 2px;
  }
</style>
</head>
<body>

<!-- ページ 1 -->
<div class="header-box">
  <div class="header-title">📋 三鷹市役所 子ども育成課 事前相談（15分トークスクリプト・完全カンペ）</div>
  <div class="header-meta">
    <span><strong>日時：</strong> 2026年10月20日（火）10:00〜10:30（実質15分説明＋質疑）</span>
    <span><strong>お相手：</strong> 子ども政策部 子ども育成課 波照間（はてるま）様</span>
  </div>
</div>

<div class="meta-grid">
  <div class="meta-card">
    <strong>🎒 本日の持ち物チェック</strong>
    ・印刷した説明資料（カラー4枚ホチキス留め）× 3〜4部<br>
    ・ご自身の名刺　・筆記用具・メモ帳
  </div>
  <div class="meta-card">
    <strong>⏱ タイム配分目安（全体15分）</strong>
    ・00:00〜01:30（1.5分）：挨拶・自己紹介（のぞみ園保護者）<br>
    ・01:30〜06:30（5.0分）：表紙サマリーを見せながら要点説明<br>
    ・06:30〜13:30（7.0分）：相談・アドバイス伺い（広報連携含む）<br>
    ・13:30〜15:00（1.5分）：締めくくり・庁内回覧のお願い
  </div>
</div>

<div class="section-title">
  <span>1. 冒頭の挨拶・繁忙期への配慮・自己紹介</span>
  <span class="time-badge">00:00 〜 01:30</span>
</div>
<div class="script-box">
  <div class="action-note">【アクション】名刺をお渡しし、相手の繁忙期（4月選考直前）を気遣う姿勢を示します。</div>
  <p>
    「波照間様、おはようございます。一般社団法人KidsRideの七夕（たなばた）でございます。<br>
    本日は4月の入所選考直前という大変お忙しい時期に、貴重なお時間をいただき誠にありがとうございます。<br>
    お約束通り、ご説明は10分〜15分程度で簡潔にまとめ、波照間様から課長様や課内で情報共有していただくための要点をお伝えできればと存じます。どうぞよろしくお願いいたします」
  </p>
</div>

<div class="section-title">
  <span>2. 表紙のエグゼクティブ・サマリーを見せながら要点説明</span>
  <span class="time-badge">01:30 〜 06:30</span>
</div>
<div class="script-box">
  <div class="action-note">【アクション】資料は開かず、表紙の枠線囲み（エグゼクティブ・サマリー①〜⑥）を指差しながらテンポよく説明。</div>
  <p>
    「まず、お手元の資料の表紙にございます<strong>【エグゼクティブ・サマリー】</strong>の6項目に沿って、事業の骨子をご説明いたします。<br>
    <strong>① 事業趣旨（地域共助）：</strong> 私自身、三鷹市在住で<span class="highlight">三鷹のぞみ幼稚園に子どもを通わせる現役の父親</span>です。毎日の送り迎えの調整や雨の日の大変さを当事者として痛感し、『同じ園に通う身元の確かな保護者同士が助け合える仕組み』を作りたいという志から本法人を立ち上げました。<br>
    <strong>② 園選び・保活支援：</strong> ちょうど今の時期、多くの保護者が『自宅から遠く送迎が困難』という理由で第一希望の園を諦めています。互助送迎により広域通園を可能にし、就労継続と理想の教育選択を支援します。<br>
    <strong>③ 適法性（道路運送法）：</strong> 国土交通省（東京運輸支局）へ正式確認済で、ガソリン実費（11円/km）のみで利益を完全排除した『許可・登録不要（合法）』の設計です。<br>
    <strong>④ 万全の安全管理・補償：</strong> あいおいニッセイ同和損保様と<span class="highlight">最高2億円の包括賠償保険および傷害保険</span>を完備。出庫前点検、アルコール検知（0.00mg/L）、リアルタイムGPS追跡、顔写真照合による引き渡し確認を義務化しています。<br>
    <strong>⑤ 行政負担・予算ゼロ：</strong> 市への予算要求は一切ございません。事前予約型である三鷹市ファミサポ様の手が届きにくい『当日の急な残業』や『園へのラストワンマイル』を補完する関係性です。<br>
    <strong>⑥ 実証実験とアンケート：</strong> 対象園は恣意的に選ばず、<span class="highlight">保護者アンケート調査でニーズ最上位の先行3園から客観的にスタート</span>し、1ヶ月毎に6園、10園へと段階的に拡大（ロールアウト）します。スマホWeb回答のため<span class="highlight">先生方の集計負担はゼロ</span>です。集計データは三鷹市様へ無償還元いたします」
  </p>
</div>

<div class="page-break"></div>

<!-- ページ 2 -->
<div class="section-title">
  <span>3. 本日のご相談・アドバイス伺い（広報連携の布石含む）</span>
  <span class="time-badge">06:30 〜 13:30</span>
</div>
<div class="script-box">
  <div class="action-note">【アクション】ここから相手にボールを渡し、アドバイスを傾聴・メモします。</div>
  <p>
    「本日、波照間様からぜひアドバイスをいただきたい点、およびご相談したい事項が3点ございます。<br><br>
    <strong>【相談1：庁内回覧・共有に向けたアドバイス】</strong><br>
    『今後、課長様や関連部署（保育課様など）へ本件を情報共有・回覧していただくにあたり、<strong>資料の表現や事前に補足しておくべき点</strong>などがございましたら、ぜひご教示いただきたいです』<br><br>
    <strong>【相談2：アンケート協力園の選定に関するご示唆】</strong><br>
    『公平性を期すため、送迎課題が本当に大きい園から先行3園を選びたいと考えております。市役所様からご覧になって、<strong>“駅から遠い”“バス本数が少ない”など、特に送迎の壁が大きい地域や園の傾向</strong>について、差し支えない範囲でアドバイスをいただけますでしょうか？』<br><br>
    <strong>【相談3：将来的な行政連携・広報連携に向けた相談（★重要）】</strong><br>
    『もう1点、将来的なご相談なのですが、私どもの最終目標は、三鷹市の子育て世帯の誰もが安心して使える地域インフラになることです。実証実験で事故ゼロの安全実績を積み重ねた上で、来年4月の本格運用時には<strong>三鷹市様の後援名義をいただいたり、広報みたか等の市の媒体で市民の皆様へご案内できれば</strong>と考えております。そうした行政連携や広報掲載を目指すにあたり、<strong>事前に満たすべき要件や、どのような実績・手続きを踏むべきか</strong>についてアドバイスをいただけますでしょうか？』」
  </p>
</div>

<div class="section-title">
  <span>4. 締めくくり・次回のコンタクト取り付け</span>
  <span class="time-badge">13:30 〜 15:00</span>
</div>
<div class="script-box">
  <div class="action-note">【アクション】一度きりで終わらせず、次回のレポート持参アポ（11月中旬）を口頭で取り付けます。</div>
  <p>
    「大変具体的で貴重なご助言をいただき、誠にありがとうございます。いただいたアドバイスを踏まえ、無理のない形で丁寧に進めてまいります。<br>
    私どもとしては、本日を一度きりのご相談で終わらせるのではなく、<strong>三鷹市の子育て環境を民間の立場から支えるパートナーとして、今後も継続的に情報共有やご相談をさせていただきたい</strong>と考えております。<br>
    まずは11月中旬に保護者アンケートの集計が完了いたしましたら、<span class="highlight">『三鷹市の子ども送迎実態調査レポート』としてまとめ、波照間様に真っ先にご持参・ご報告にあがりたい</span>と存じます。<br>
    その節は、ぜひまた15分ほどお時間をいただき、データをご覧いただきながら先行3園の選定についてご意見を伺えますと幸いです。今後とも末永くよろしくお願い申し上げます」
  </p>
</div>

<div class="section-title">
  <span>■ 想定問答集（質問された場合のショートアンサー）</span>
</div>
<div class="qa-card">
  <div class="qa-q">Q1. 万が一、事故が起きた場合の責任はどうなるのですか？</div>
  <div class="qa-a">
    <strong>A1.</strong> 事故時は警察（110番）届出を義務化し、損保会社との示談代行・窓口はKidsRide本部が一本化して担います。あいおいニッセイ同和損保様と最高2億円の包括賠償保険およびドライバー・児童の傷害保険を完備しており、サポーター個人の任意保険を使わせない手厚い補償体制です。
  </div>
</div>
<div class="qa-card">
  <div class="qa-q">Q2. 保育園や幼稚園の先生方の手間や負担は増えませんか？</div>
  <div class="qa-a">
    <strong>A2.</strong> 一切増えません。アンケートはスマホWeb回答（所要2〜3分）でお便り同封または掲示のみです。回収・集計の手間はゼロです。また送迎時の引き渡し確認もアプリの顔写真照合で行うため、現場の混乱を防ぎます。
  </div>
</div>
<div class="qa-card">
  <div class="qa-q">Q3. 三鷹市のファミリー・サポート・センターとどう違うのですか？</div>
  <div class="qa-a">
    <strong>A3.</strong> 競合ではなく相互補完です。ファミサポ様はボランティアによる『事前予約型の定期的な支援（習い事等）』です。一方、KidsRideは同じ園に通う保護者同士による『当日の急な残業や発熱などの突発的ピンチ』にアプリで即時対応するラストワンマイルの互助です。
  </div>
</div>

</body>
</html>
"""

html_path = os.path.join(OUTPUT_DIR, "三鷹市事前相談_本日の15分トークスクリプト.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

pdf_path = os.path.join(OUTPUT_DIR, "三鷹市事前相談_本日の15分トークスクリプト.pdf")

# Google Chrome headless で PDF 出力
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
    print(f"PDF saved to: {pdf_path}")
else:
    print(f"Failed to generate PDF: {res.stderr}")
