import os
import subprocess
import base64
import urllib.request

OUTPUT_DIR = os.path.expanduser("~/Desktop/KidsRide/KidsRide_アンケート資料")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. QRコード画像を取得してbase64エンコード
qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://www.kidsride.jp/%23survey"
try:
    with urllib.request.urlopen(qr_url) as response:
        qr_bytes = response.read()
    qr_base64 = base64.b64encode(qr_bytes).decode('utf-8')
except Exception as e:
    print(f"QRコード取得エラー: {e}")
    qr_base64 = ""

# ==============================================================================
# PDF 1: 【園長先生向け 公式依頼状】（A4・ジャスト1ページ）
# ==============================================================================
html_request_letter = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>園長先生・施設長様向け アンケート調査協力依頼状</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 11mm 15mm 10mm 15mm;
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    line-height: 1.45;
    font-size: 8.5pt;
    margin: 0;
    padding: 0;
  }}
  .header-meta {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 6px;
    font-size: 8.2pt;
  }}
  .doc-title {{
    font-size: 11.5pt;
    font-weight: 800;
    text-align: center;
    color: #0f172a;
    margin: 6px 0 8px 0;
    padding: 5px 0;
    border-top: 2px solid #0284c7;
    border-bottom: 2px solid #0284c7;
    background: #f0f9ff;
    letter-spacing: 0.5px;
  }}
  p {{
    margin: 3px 0;
    text-align: justify;
    line-height: 1.42;
  }}
  .box-card {{
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 6px 10px;
    margin: 5px 0;
    background: #ffffff;
  }}
  .box-title {{
    font-weight: 800;
    font-size: 8.6pt;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 4px;
  }}
  table.details-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 2px 0;
    font-size: 8pt;
  }}
  table.details-table th, table.details-table td {{
    border: 1px solid #cbd5e1;
    padding: 3px 6px;
    vertical-align: top;
  }}
  table.details-table th {{
    background: #f1f5f9;
    color: #334155;
    width: 20%;
    text-align: left;
    font-weight: 700;
  }}
  .profile-grid {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 2px;
    font-size: 7.9pt;
    line-height: 1.38;
    color: #334155;
  }}
  .footer-contact {{
    margin-top: 6px;
    padding-top: 5px;
    border-top: 1px solid #cbd5e1;
    display: flex;
    justify-content: space-between;
    font-size: 7.6pt;
    color: #64748b;
  }}
</style>
</head>
<body>

<div class="header-meta">
  <div>
    <div style="font-size:7.8pt; color:#64748b;">三鷹市内 就学前教育・保育施設 各位</div>
    <div style="font-size:10.5pt; font-weight:800; color:#0f172a; margin-top:1px;">園長・施設長 先生</div>
  </div>
  <div style="text-align:right; font-size:7.8pt; line-height:1.35;">
    <div>2026年10月吉日</div>
    <div style="font-weight:800; color:#0f172a; font-size:8.6pt;">一般社団法人KidsRide（キッズライド）</div>
    <div>代表理事 七夕 光明（三鷹市下連雀在住・保護者）</div>
    <div>Web: https://www.kidsride.jp/</div>
  </div>
</div>

<div class="doc-title">
  【ご協力のお願い】子どもの通園・送迎に関する保護者実態調査の実施について
</div>

<p>拝啓　貴園におかれましては、三鷹市の子どもたちの健やかな成長と安心・安全な保育環境の充実に尽力され、心より敬意と感謝を申し上げます。</p>
<p>私ども「一般社団法人KidsRide」は、三鷹市在住の保護者有志が立ち上げた法人です。現在、急な残業やきょうだいの発熱、悪天候などにより保護者の送迎負担が増大する一方、<strong style="color:#0f172a;">園の先生方におかれましても夕方の延長保育対応や遅延連絡への対応など、多大なご負担が生じている</strong>ことと拝察いたします。</p>
<p>当法人では2026年10月、三鷹市役所子ども育成課と事前相談を実施し、地域における送迎課題や一時預かり施設への送迎ニーズ等について意見交換を行っております。</p>
<p>そこで、三鷹市への政策提言および安全な地域送迎互助プラットフォーム設計の基礎資料として、貴園の保護者様を対象とするアンケート調査への周知・配架ご協力をお願い申し上げます。敬具</p>

<div class="box-card" style="border-left: 4px solid #0284c7;">
  <div class="box-title" style="color:#0369a1;">■ 調査概要</div>
  <table class="details-table">
    <tr>
      <th>調査名</th>
      <td>【三鷹市】子どもの通園・送迎に関する保護者実態調査（所要時間：約2分）</td>
    </tr>
    <tr>
      <th>対象・形式</th>
      <td>貴園の保護者様 / スマートフォンによるWeb回答（<strong>完全無記名方式</strong>・統計集計のみ）</td>
    </tr>
    <tr>
      <th>回答特典</th>
      <td>今秋実施予定の「無料実証実験（モニター体験）」への優先案内（ご希望の方のみ）</td>
    </tr>
  </table>
</div>

<div class="box-card" style="border-left: 4px solid #10b981;">
  <div class="box-title" style="color:#059669;">■ 貴園へのお願い事項（先生方の作業負担ゼロの徹底）</div>
  <p style="font-size:7.9pt; margin:1px 0;">先生方の日常業務にご負担をおかけしないよう、以下のいずれか可能な範囲でご協力いただけますと幸いです。</p>
  <div style="font-size:7.9pt; margin-top:2px; line-height:1.4;">
    <div><strong>①【推奨・置くだけ】登降園打刻機・下駄箱上の卓上POP＆カード設置</strong>：<br>
    　当方が持参する「A5卓上POP」および「名刺サイズQRカード」を置かせていただくだけです（※プリント折り・連絡帳挟み込みは不要です）。</div>
    <div><strong>② 玄関掲示板へのA4ポスター掲示</strong>（ポスター1枚掲示のみ）</div>
    <div><strong>③ 園連絡アプリでのご案内</strong>（コドモン・マチコミ・<strong>れんらくアプリ</strong>等での案内文1回配信 / 文面は当方で用意）</div>
  </div>
</div>

<div class="box-card" style="border-left: 4px solid #f59e0b;">
  <div class="box-title" style="color:#d97706;">■ 貴園へのメリットとお約束事項</div>
  <div style="font-size:7.9pt; line-height:1.4;">
    <div>✔ <strong>集計結果サマリーの無償提供</strong>：貴園の保護者ニーズを分析したレポートを後日無償提供（園運営や市への要望資料に活用可能）。</div>
    <div>✔ <strong>三鷹市子ども育成課へのデータ共有</strong>：公立園タクシー送迎課題や、一時預かり（のびのびひろば）への送迎連携策に役立てます。</div>
    <div>✔ <strong>営利営業・勧誘の完全排除</strong>：純粋な実態調査であり、特定の商材販売や個人情報の収集・流用は一切行いません。</div>
  </div>
</div>

<div class="box-card" style="border-left: 4px solid #6366f1; background:#f8fafc;">
  <div class="box-title" style="color:#4338ca;">■ 発起人略歴・設立背景（より身近で安心いただける取り組みを目指して）</div>
  <div class="profile-grid">
    <div><strong>【代表理事：七夕 光明（たなばた みつあき）】</strong> 三鷹市下連雀在住。自身も市内の園に子どもを通わせる現役の父親。</div>
    <div><strong>【略歴・企業背景】</strong> Apple Japanにて19年間にわたり旗艦店（Apple銀座）創業やAPAC製品ローンチのオペレーション統括を担当。その後、Amazon Ads Japanにて広告審査・運用組織（マネージャー陣・最大40名）の統括責任者を歴任。</div>
    <div><strong>【設立への想い】</strong> グローバルIT企業で培った「徹底した安全管理・運用の規律」を地域の子育て支援に結集し、地元・三鷹市の保護者同士が同じ園の仲間として安心して助け合える環境をつくるため、本法人を設立いたしました。</div>
  </div>
</div>

<div class="footer-contact">
  <div>【お問い合わせ・POPお届け窓口】一般社団法人KidsRide 代表理事 七夕 光明 / 直通: 070-XXXX-XXXX / Email: info@kids-ride.jp</div>
  <div style="text-align:right;">回答URL: https://www.kidsride.jp/#survey</div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 2: 【保護者向け 掲示チラシ兼卓上POP】（A4フルカラー・見切れ・シャドウゼロ設計）
# ==============================================================================
html_flyer_pop = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>三鷹市 保護者送迎アンケート 掲示チラシ・卓上POP</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 12mm 16mm 10mm 16mm;
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #0f172a;
    line-height: 1.45;
    margin: 0;
    padding: 0;
  }}
  .hero-box {{
    background: #0284c7;
    color: #ffffff;
    padding: 16px 16px;
    border-radius: 10px;
    text-align: center;
    box-shadow: none !important;
    margin-bottom: 12px;
    width: 100%;
  }}
  .hero-subtitle {{
    font-size: 10pt;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
    color: #e0f2fe;
    text-shadow: none !important;
  }}
  .hero-title {{
    font-size: 16pt;
    font-weight: 800;
    line-height: 1.35;
    margin: 0;
    color: #ffffff;
    text-shadow: none !important;
    letter-spacing: 0.3px;
  }}
  .hero-highlight {{
    color: #fef08a;
    display: inline-block;
    text-shadow: none !important;
  }}
  .check-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin: 12px 0;
  }}
  .check-item {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #ef4444;
    padding: 8px 10px;
    border-radius: 6px;
    font-size: 8.8pt;
    font-weight: 600;
    color: #334155;
    box-shadow: none;
  }}
  .concept-card {{
    background: #f0fdf4;
    border: 1.5px solid #86efac;
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 12px;
    font-size: 8.8pt;
    color: #14532d;
    box-shadow: none;
  }}
  .concept-title {{
    font-weight: 800;
    font-size: 10pt;
    color: #166534;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .cta-container {{
    display: grid;
    grid-template-columns: 140px 1fr;
    gap: 16px;
    align-items: center;
    background: #fffbeb;
    border: 2px dashed #f59e0b;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    box-shadow: none;
  }}
  .qr-box {{
    text-align: center;
    background: #ffffff;
    padding: 8px;
    border-radius: 8px;
    border: 1px solid #fed7aa;
    box-shadow: none;
  }}
  .qr-img {{
    width: 120px;
    height: 120px;
    display: block;
    margin: 0 auto;
  }}
  .cta-content {{
    font-size: 9pt;
  }}
  .cta-badge {{
    display: inline-block;
    background: #ea580c;
    color: #ffffff;
    font-weight: 800;
    font-size: 8.5pt;
    padding: 2px 8px;
    border-radius: 12px;
    margin-bottom: 4px;
    box-shadow: none;
  }}
  .cta-heading {{
    font-size: 12pt;
    font-weight: 800;
    color: #9a3412;
    margin: 2px 0 6px 0;
  }}
  .meta-footer {{
    font-size: 7.6pt;
    color: #64748b;
    border-top: 1px solid #e2e8f0;
    padding-top: 6px;
    display: flex;
    justify-content: space-between;
  }}
</style>
</head>
<body>

<div class="hero-box">
  <div class="hero-subtitle">【三鷹市で子育て中のパパ・ママへ緊急実態調査】</div>
  <div class="hero-title">
    「今日、お迎え間に合わないかも…！」と<br>
    <span class="hero-highlight">焦った経験はありませんか？</span>
  </div>
</div>

<div style="font-size:9pt; font-weight:700; color:#475569; margin-bottom:4px; text-align:center;">
  雨の日の自転車送迎・下の子の発熱・急な残業…こんな瞬間に直面したことはありませんか？
</div>

<div class="check-grid">
  <div class="check-item">✔ 急な残業で延長保育の時間に間に合わない…</div>
  <div class="check-item">✔ 下の子が突然発熱！上の子のお迎えどうしよう…</div>
  <div class="check-item">✔ 大雨や台風の日、子乗せ自転車が本当に怖い…</div>
  <div class="check-item">✔ のびのび広場(〜22時)まで園から連れていけない…</div>
</div>

<div class="concept-card">
  <div class="concept-title">💡 同じ園の保護者同士で「ついでに送迎」を助け合える仕組みへ</div>
  <div style="line-height:1.45;">
    「知らないシッターは不安」「ファミサポは事前の面談や調整が大変」という声に応え、<br>
    <strong>【同じ園の身元確認済み保護者同士 ＋ 万全の安心包括補償制度（大手損保引受）】</strong>で支え合う新しい仕組み「KidsRide」の実証実験を三鷹市で準備しています。万が一の事故にも安心・安全な補償体制を整え、皆様のリアルな声を三鷹市役所への政策提案にも活かします！
  </div>
</div>

<div class="cta-container">
  <div class="qr-box">
    {f'<img src="data:image/png;base64,{qr_base64}" class="qr-img" alt="QRコード">' if qr_base64 else '<div style="width:120px;height:120px;background:#e2e8f0;display:flex;align-items:center;justify-content:center;">QR</div>'}
    <div style="font-size:7.5pt; font-weight:700; color:#0284c7; margin-top:4px;">スマホで読み取り</div>
  </div>
  <div class="cta-content">
    <span class="cta-badge">回答時間：約2分・完全無記名</span>
    <div class="cta-heading">スマホでサクッと回答完了！</div>
    <div style="font-size:8.8pt; line-height:1.45; color:#334155; margin-bottom:6px;">
      個人情報の登録なしで選択肢をタップするだけ。<br>
      ご希望の方には今秋実施予定の<strong style="color:#0284c7; font-size:9.5pt;">【無料実証実験モニター】</strong>の優先案内をお届けします！
    </div>
    <div style="font-size:8.2pt; color:#64748b;">
      Webから直接回答: <strong style="color:#0284c7;">https://www.kidsride.jp/#survey</strong>
    </div>
  </div>
</div>

<div class="meta-footer">
  <div>実施主体: 一般社団法人KidsRide / 代表理事 七夕 光明（三鷹市下連雀在住・保護者）</div>
  <div>※回答データは統計処理し、三鷹市役所子ども育成課へも共有されます。</div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 3: 【持ち帰り用 名刺サイズカード 面付け用】（A4 1枚に10枚面付け）
# ==============================================================================
html_cards_sheet = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>持ち帰り用 名刺サイズQRカード 面付けシート</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 8mm 17mm 8mm 17mm;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    margin: 0;
    padding: 0;
  }}
  .grid-container {{
    display: grid;
    grid-template-columns: 85mm 85mm;
    grid-template-rows: repeat(5, 50mm);
    gap: 2.5mm 6mm;
    justify-content: center;
  }}
  .card-item {{
    border: 1px dashed #94a3b8;
    border-radius: 6px;
    padding: 6px 8px;
    box-sizing: border-box;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
  }}
  .card-left {{
    width: 60%;
  }}
  .card-tag {{
    background: #0284c7;
    color: #ffffff;
    font-size: 6.5pt;
    font-weight: 800;
    padding: 1px 4px;
    border-radius: 3px;
    display: inline-block;
  }}
  .card-title {{
    font-size: 8.2pt;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.25;
    margin: 3px 0 2px 0;
  }}
  .card-desc {{
    font-size: 6.8pt;
    color: #475569;
    line-height: 1.2;
  }}
  .card-gift {{
    font-size: 6.8pt;
    color: #c2410c;
    font-weight: 800;
    margin-top: 3px;
  }}
  .card-right {{
    width: 38%;
    text-align: center;
  }}
  .mini-qr {{
    width: 62px;
    height: 62px;
    display: block;
    margin: 0 auto;
  }}
  .mini-url {{
    font-size: 6pt;
    color: #0284c7;
    font-weight: 700;
    margin-top: 2px;
  }}
</style>
</head>
<body>

<div class="grid-container">
  {''.join([f'''
  <div class="card-item">
    <div class="card-left">
      <span class="card-tag">三鷹市・約2分</span>
      <div class="card-title">「お迎え間に合わない…」と焦ったことありませんか？</div>
      <div class="card-desc">雨の日・残業・発熱時の助け合い仕組みづくりのための無記名アンケート</div>
      <div class="card-gift">★無料実証実験モニター優先案内★</div>
    </div>
    <div class="card-right">
      {f'<img src="data:image/png;base64,{qr_base64}" class="mini-qr" alt="QR">' if qr_base64 else 'QR'}
      <div class="mini-url">kidsride.jp/#survey</div>
    </div>
  </div>
  ''' for _ in range(10)])}
</div>

</body>
</html>
"""

# 出力実行関数
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

generate_pdf(html_request_letter, "三鷹市_園長先生向け_アンケート調査協力依頼状.pdf")
generate_pdf(html_flyer_pop, "三鷹市_保護者送迎アンケート_掲示チラシ兼卓上POP.pdf")
generate_pdf(html_cards_sheet, "三鷹市_保護者送迎アンケート_持ち帰り用名刺カード10面.pdf")
print("全PDFの生成が完了しました。")
