import os
import subprocess

OUTPUT_DIR = os.path.expanduser("~/Desktop/KidsRide/KidsRide_アンケート資料")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================================================================
# PDF 1: 【保育園・幼稚園アプローチ用 1分トークスクリプト】
# ==============================================================================
html_script = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>三鷹市 保育園・幼稚園アプローチ用 1分トークスクリプト</title>
<style>
  @page {
    size: A4 portrait;
    margin: 12mm 15mm 12mm 15mm;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    line-height: 1.5;
    font-size: 8.8pt;
    margin: 0;
    padding: 0;
  }
  .header-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    color: #ffffff;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header-title {
    font-size: 13pt;
    font-weight: 800;
    margin: 0 0 3px 0;
  }
  .header-sub {
    font-size: 8pt;
    color: #93c5fd;
  }
  .badge {
    background: #0284c7;
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 7.5pt;
    font-weight: 700;
  }
  .section-title {
    font-size: 10pt;
    font-weight: 800;
    color: #0369a1;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 3px;
    margin: 10px 0 6px 0;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .box-card {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 8px;
    background: #ffffff;
  }
  .script-box {
    background: #f8fafc;
    border-left: 4px solid #0284c7;
    padding: 8px 12px;
    border-radius: 0 6px 6px 0;
    font-size: 8.5pt;
    line-height: 1.5;
    color: #0f172a;
    margin: 4px 0 6px 0;
  }
  .qa-card {
    background: #fafafa;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 6px 10px;
    margin-bottom: 6px;
  }
  .qa-q {
    font-weight: 800;
    color: #b91c1c;
    font-size: 8.3pt;
    margin-bottom: 2px;
  }
  .qa-a {
    font-size: 8.2pt;
    color: #1e293b;
    line-height: 1.45;
  }
  .checklist-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    font-size: 8.2pt;
  }
  .check-item {
    background: #f1f5f9;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: 600;
  }
</style>
</head>
<body>

<div class="header-box">
  <div>
    <div class="header-title">【園長先生・窓口突破マニュアル】保育園・幼稚園 1分トークスクリプト</div>
    <div class="header-sub">三鷹市内全園（約60〜70施設）向け 不審者扱いを防止し配架を即決させる実践ガイド</div>
  </div>
  <span class="badge">現場即戦マニュアル</span>
</div>

<div class="section-title">■ 1. 現場心理を突破する3原則</div>
<div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:6px; margin-bottom:8px; font-size:8pt;">
  <div class="box-card" style="border-top:3px solid #0284c7; margin:0;">
    <strong style="color:#0369a1; display:block; margin-bottom:2px;">① 営業の言葉を完全排除</strong>
    「サービス案内」ではなく「三鷹市の子育て環境改善のための実態調査」として依頼。
  </div>
  <div class="box-card" style="border-top:3px solid #10b981; margin:0;">
    <strong style="color:#047857; display:block; margin-bottom:2px;">② 三鷹市役所事前相談の冠</strong>
    「子ども育成課と事前相談済み」を伝え、公的信頼を一瞬で担保。
  </div>
  <div class="box-card" style="border-top:3px solid #f59e0b; margin:0;">
    <strong style="color:#b45309; display:block; margin-bottom:2px;">③ 先生方の作業負担ゼロ</strong>
    「プリント配布や折り込みは不要、打刻機横に置くだけ」を冒頭で断言。
  </div>
</div>

<div class="section-title">■ 2. 【電話編】受付の先生から園長先生につないでもらうトーク（30秒）</div>
<div class="script-box">
  「お忙しい時間帯に大変恐縮です。私、三鷹市下連雀で子育て支援の調査を行っております、一般社団法人KidsRideの七夕（たなばた）と申します。<br>
  実は、<strong>三鷹市役所の子ども育成課様ともご相談をさせていただきながら、市内の保護者様が夕方の通園やお迎えで直面している困りごとに関する実態調査</strong>を行っております。<br>
  先生方にお手間を取らせない形での簡単なアンケート配架のご相談でして、<strong>園長先生または主任の先生に1分だけ</strong>お取り次ぎいただくことは可能でしょうか？」
</div>
<div style="font-size:7.8pt; color:#64748b; margin-top:-2px; margin-bottom:8px;">
  ※電話推奨時間帯：送迎ピークや給食・午睡を避けた <strong>10:00〜11:00</strong> または <strong>14:30〜16:00</strong>
</div>

<div class="section-title">■ 3. 【園長先生編】電話または対面訪問での1分即決トーク（60秒）</div>
<div class="script-box" style="border-left-color: #10b981;">
  「園長先生、お時間をいただき誠にありがとうございます。一般社団法人KidsRideの七夕です。私自身も三鷹市で子どもを育てている保護者です。<br>
  本日ご連絡いたしましたのは、日頃先生方が直面されている<strong>『夕方のお迎え遅延や、急な残業時の延長保育対応』における先生方のご負担を少しでも減らすため、保護者の送迎のリアルな実態調査</strong>を行っているためです。<br>
  先日、三鷹市役所の子ども育成課様とも協議を行い、<strong>地域における送迎課題や一時預かりへの送迎連携についてご相談</strong>させていただいております。<br>
  そこで貴園にお願いしたいのは、先生方にプリントを折って配っていただくような作業では一切ございません。<strong>登降園の打刻機や下駄箱の上に、当方が用意した小さな卓上POPと名刺サイズのQRカードを置かせていただくだけ</strong>で結構です。<br>
  集計結果のサマリーレポートは<strong>貴園にも無償でご提供</strong>いたしますので、今後の園運営や市へのご要望資料としてもご活用いただけます。先生方のお手間は一切取らせませんので、ぜひ玄関に置かせていただけないでしょうか？」
</div>

<div class="section-title">■ 4. 想定される反論への切り返し（Q&A）</div>
<div class="qa-card">
  <div class="qa-q">Q1. 「特定の民間企業やサービスの宣伝は、園のルールで置けないことになっているのですが…」</div>
  <div class="qa-a"><strong>A1.</strong> 「おっしゃる通りでございます。私どもは営利企業ではなく『一般社団法人』でございます。今回はサービスの加入勧誘ではなく、市役所にも共有する『送迎環境の実態把握アンケート（無記名）』でございます。営業活動や個人情報の収集は一切行いませんので、ご安心ください。」</div>
</div>
<div class="qa-card">
  <div class="qa-q">Q2. 「今は行事などで忙しくて対応する余裕がないのですが…」</div>
  <div class="qa-a"><strong>A2.</strong> 「先生、本当に毎日お忙しいところ恐れ入ります。ですので先生方にやっていただく作業は本当に何もございません。案内POPとカードをお届け（または郵送）いたしますので、玄関の隅に置いていただくだけで結構です。回収・集計もすべてWeb上で完了いたします。」</div>
</div>
<div class="qa-card">
  <div class="qa-q">Q3. 「他の園はどうしているんですか？」</div>
  <div class="qa-a"><strong>A3.</strong> 「はい、市内公立保育園や私立園、認定こども園、駅前の『のびのびひろば』など、三鷹市全域の就学前施設にお声がけを進めております。市役所子ども育成課様へも全園横断のデータとしてご報告いたしますので、ぜひ貴園の保護者様の声も反映させていただければ幸いです。」</div>
</div>

<div class="section-title">■ 5. 窓口訪問（突撃・挨拶）時の持ち物チェックリスト</div>
<div class="checklist-grid">
  <div class="check-item">✔ 園長先生宛の公式依頼状（印刷物）</div>
  <div class="check-item">✔ 組み立て済みの「A5卓上三角POP」実物</div>
  <div class="check-item">✔ 持ち帰り用「名刺サイズQRカード」束</div>
  <div class="check-item">✔ 法人名刺（代表理事 七夕 光明）</div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 2: 【保護者アンケート配布物 設計仕様書】
# ==============================================================================
html_design_doc = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>三鷹市 保護者アンケート配布物 設計仕様書</title>
<style>
  @page {
    size: A4 portrait;
    margin: 12mm 15mm 12mm 15mm;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    line-height: 1.5;
    font-size: 8.8pt;
    margin: 0;
    padding: 0;
  }
  .header-box {
    background: linear-gradient(135deg, #0284c7 0%, #1e40af 100%);
    color: #ffffff;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header-title {
    font-size: 13pt;
    font-weight: 800;
    margin: 0 0 3px 0;
  }
  .header-sub {
    font-size: 8pt;
    color: #bae6fd;
  }
  .badge {
    background: #f59e0b;
    color: #78350f;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 7.5pt;
    font-weight: 800;
  }
  .section-title {
    font-size: 10pt;
    font-weight: 800;
    color: #0369a1;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 3px;
    margin: 10px 0 6px 0;
  }
  .spec-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 8px;
    font-size: 8.2pt;
  }
  .spec-table th, .spec-table td {
    border: 1px solid #cbd5e1;
    padding: 5px 8px;
  }
  .spec-table th {
    background: #f1f5f9;
    color: #334155;
    text-align: left;
    font-weight: 700;
    width: 25%;
  }
  .copy-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #ef4444;
    padding: 8px 12px;
    border-radius: 0 6px 6px 0;
    font-size: 8.3pt;
    margin-bottom: 8px;
  }
  .card-wireframe {
    border: 1px dashed #94a3b8;
    background: #ffffff;
    padding: 8px 12px;
    border-radius: 6px;
    margin-bottom: 8px;
    font-size: 8pt;
  }
</style>
</head>
<body>

<div class="header-box">
  <div>
    <div class="header-title">【保護者アンケート配布物 設計仕様書】A4チラシ・卓上POP・名刺カード</div>
    <div class="header-sub">三鷹市全域（認可・私立保育園・幼稚園・子育て施設・小児科）配布用ツールの設計統合原稿</div>
  </div>
  <span class="badge">制作仕様書</span>
</div>

<div class="section-title">■ 1. 媒体別 制作仕様サマリー</div>
<table class="spec-table">
  <tr>
    <th>① A4掲示チラシ / ポスター</th>
    <td>園内掲示板、玄関壁面、小児科クリニック待合室に掲示。遠くからでも目を引くキャッチコピー（大文字見出し）。</td>
  </tr>
  <tr>
    <th>② A5卓上三角POP</th>
    <td>登降園の打刻機横、下駄箱上、受付カウンターに自立設置。教員の手間ゼロで保護者の視線誘導。</td>
  </tr>
  <tr>
    <th>③ 持ち帰り用名刺カード</th>
    <td>卓上POP前に平積み（91×55mm）。急いでいる保護者が「1枚取って後で電車・自宅で回答」できる動線。</td>
  </tr>
  <tr>
    <th>回答先URL / 特典</th>
    <td><strong>https://www.kidsride.jp/#survey</strong> / 無料実証実験モニターへの優先案内（ご希望の方のみ）</td>
  </tr>
</table>

<div class="section-title">■ 2. コピーライティング設計（保護者の共感を呼ぶ4大要素）</div>
<div class="copy-box">
  <div style="font-weight:800; font-size:9.5pt; color:#991b1b; margin-bottom:4px;">
    「今日、お迎え間に合わないかも…！」と焦った経験はありませんか？
  </div>
  <div style="color:#475569; line-height:1.45;">
    ✔ <strong>急な残業</strong>が入ったけれど、お迎えの延長時間にどうしても間に合わない…<br>
    ✔ <strong>下の子が突然発熱</strong>！上の子の園へのお迎え、どうやって連れて行こう…<br>
    ✔ 雨や台風の日、子どもを乗せての<strong>自転車送迎が本当に怖くて大変</strong>…<br>
    ✔ 三鷹駅前の『<strong>のびのびひろば（夜22時までトワイライトステイ）</strong>』を使いたいが、園からの送迎手段がない…
  </div>
</div>

<div class="section-title">■ 3. A4チラシ・卓上POP 構成レイアウト設計</div>
<table class="spec-table">
  <tr>
    <th>ヘッダー（帯）</th>
    <td>グラデーションブルー背景 ＋ 白文字「三鷹市パパ・ママ緊急実態調査」＋ 特典バッジ</td>
  </tr>
  <tr>
    <th>メインビジュアル</th>
    <td>「今日、お迎え間に合わないかも…！」大文字（18pt）＋ 共感チェックボックス4項目</td>
  </tr>
  <tr>
    <th>コンセプト提示</th>
    <td>同じ園の身元確認済み保護者同士 ＋ 万全の安心包括補償制度（大手損保引受）による「ついでに送迎」の安心・安全な環境</td>
  </tr>
  <tr>
    <th>CTA（アクション枠）</th>
    <td>QRコード（スマホ直接読み取り）＋「回答時間：たった2分・完全無記名」＋ 無料モニター優先案内</td>
  </tr>
  <tr>
    <th>フッター（信頼性）</th>
    <td>一般社団法人KidsRide（代表理事 七夕 光明・三鷹市在住保護者）/ 三鷹市役所子ども育成課へデータ共有</td>
  </tr>
</table>

<div class="section-title">■ 4. 持ち帰り用名刺カード（91mm × 55mm）表面・裏面設計</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px;">
  <div class="card-wireframe">
    <div style="font-weight:800; color:#0369a1; border-bottom:1px solid #e2e8f0; padding-bottom:2px; margin-bottom:4px;">【おもて面】キャッチ＆特典</div>
    <div>● 帯: 三鷹市パパママ通園・送迎SOSアンケート（約2分）</div>
    <div style="font-weight:700; margin:2px 0;">「お迎え間に合わない…」と焦ったことありませんか？</div>
    <div style="color:#64748b; font-size:7.5pt;">雨の日・残業・発熱時の助け合い仕組みづくりのための無記名調査</div>
    <div style="color:#0284c7; font-weight:800; margin-top:2px;">★無料実証実験モニター優先案内あり★</div>
  </div>
  <div class="card-wireframe">
    <div style="font-weight:800; color:#059669; border-bottom:1px solid #e2e8f0; padding-bottom:2px; margin-bottom:4px;">【うら面】QRコード＆公的背景</div>
    <div>● QRコード配置（28mm×28mm）＋ スマホカメラで2分</div>
    <div>● 短縮URL表記: kidsride.jp/#survey</div>
    <div style="color:#64748b; font-size:7.2pt; margin-top:2px;">※三鷹市役所子ども育成課へも集計結果を共有し、地域全体の送迎負担軽減に役立てます。個人情報なしで回答可能。</div>
  </div>
</div>

<div class="section-title">■ 5. 配架・展開チャネル一覧</div>
<div style="font-size:8.2pt; line-height:1.45; color:#334155;">
  1. <strong>公立・私立保育園・幼稚園（約60〜70園）</strong>：登降園打刻機横、玄関下駄箱上の卓上POP＆カード<br>
  2. <strong>三鷹市子育て支援施設</strong>：のびのびひろば（駅前）、すくすくひろば（上連雀）、市内各児童館<br>
  3. <strong>小児科クリニック・調剤薬局</strong>：三鷹駅周辺・連雀通りのクリニック受付（待ち時間のスマホ回答狙い）
</div>

</body>
</html>
"""

def generate_pdf(html_text, filename):
    html_file = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".html"))
    pdf_file = os.path.join(OUTPUT_DIR, filename)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_text)
    
    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"成功: {pdf_file}")
    else:
        print(f"失敗 ({filename}): {res.stderr}")

generate_pdf(html_script, "三鷹市_保育園窓口アプローチ_1分トークスクリプト.pdf")
generate_pdf(html_design_doc, "三鷹市_保護者アンケート配布物_設計仕様書.pdf")
print("Markdown設計書2種のPDF出力が完了しました。")
