import os
import subprocess
import base64

BASE_DIR = os.path.expanduser("~/Desktop/01_KidsRide/00_【明日持参・印刷用】地域協働・NPO・社協面談資料一式")
os.makedirs(BASE_DIR, exist_ok=True)

workspace_dir = os.path.dirname(__file__)
logo_path = os.path.join(workspace_dir, "logo.png")
symbol_path = os.path.join(workspace_dir, "logo-symbol.png")
qr_path = os.path.join(workspace_dir, "qr_web_card.png")

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

logo_b64 = get_base64_image(logo_path)
symbol_b64 = get_base64_image(symbol_path)
qr_b64 = get_base64_image(qr_path)

chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
os.makedirs("/tmp/chrome-pdf-profile", exist_ok=True)

def render_pdf(html_content, output_pdf_path):
    html_temp = output_pdf_path.replace(".pdf", ".html")
    with open(html_temp, "w", encoding="utf-8") as f:
        f.write(html_content)
    cmd = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--user-data-dir=/tmp/chrome-pdf-profile",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_pdf_path}",
        html_temp
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(html_temp):
        os.remove(html_temp)
    if res.returncode == 0 and os.path.exists(output_pdf_path):
        print(f"  [成功] {os.path.basename(output_pdf_path)}")
    else:
        print(f"  [失敗] {os.path.basename(output_pdf_path)}: {res.stderr}")

# ==============================================================================
# 1. アンケート調査協力・情報提供依頼状（フッターを左右ではなく上下に配置）
# ==============================================================================
def get_request_letter_html(target_org_name, target_org_sub):
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>アンケート調査協力および地域協働に関するご相談状</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 12mm 15mm 12mm 15mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    line-height: 1.6;
    letter-spacing: 0.02em;
    font-size: 8.8pt;
    margin: 0;
    padding: 0;
  }}
  .header-meta {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;
    font-size: 8.5pt;
  }}
  .doc-title {{
    font-size: 12.5pt;
    font-weight: 800;
    text-align: center;
    color: #0f172a;
    margin: 10px 0 12px 0;
    padding: 7px 0;
    border-top: 2px solid #0284c7;
    border-bottom: 2px solid #0284c7;
    letter-spacing: 0.05em;
  }}
  .lead {{
    margin-bottom: 12px;
    text-indent: 1em;
    font-size: 8.8pt;
    line-height: 1.65;
    color: #334155;
  }}
  .box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 12px;
  }}
  .box-title {{
    font-weight: 800;
    color: #0369a1;
    font-size: 9.3pt;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  table.summary-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 6px;
    font-size: 8.4pt;
  }}
  table.summary-table th, table.summary-table td {{
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    vertical-align: top;
    line-height: 1.5;
  }}
  table.summary-table th {{
    background: #f1f5f9;
    color: #334155;
    font-weight: 700;
    width: 25%;
    text-align: left;
  }}
  .footer-sign {{
    margin-top: 14px;
    padding-top: 8px;
    border-top: 1px dashed #cbd5e1;
  }}
  .footer-upper {{
    text-align: right;
    font-size: 8.5pt;
    color: #334155;
    font-weight: 600;
    margin-bottom: 6px;
    line-height: 1.5;
  }}
  .footer-lower {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 8.2pt;
    color: #475569;
    flex-wrap: nowrap;
  }}
  .footer-lower-left {{
    white-space: nowrap;
    flex-shrink: 0;
  }}
  .footer-lower-right {{
    white-space: nowrap;
    font-size: 7.8pt;
    color: #64748b;
  }}
</style>
</head>
<body>

<div class="header-meta">
  <div>
    <div style="font-size:11.5pt; font-weight:800; color:#0f172a; letter-spacing:0.03em;">{target_org_name} 御中</div>
    <div style="font-size:8.5pt; color:#64748b; margin-top:3px;">{target_org_sub}</div>
  </div>
  <div style="text-align:right;">
    <div>2026年11月吉日</div>
    <div style="font-weight:700; color:#0f172a; margin-top:2px;">一般社団法人KidsRide</div>
    <div>代表理事 七夕 光明（三鷹市在住）</div>
    <div style="font-size:7.5pt; color:#64748b;">公式Web: https://www.kidsride.jp/</div>
  </div>
</div>

<div class="doc-title">
  三鷹市内における子育て世帯の通園・送迎実態調査へのご協力<br>および地域協働に関するご相談について
</div>

<div class="lead">
  拝啓　時下ますますご清祥のこととお慶び申し上げます。日頃より三鷹市における地域コミュニティの醸成、子育て支援、ならびに地域福祉の向上に多大なるご尽力を賜り、心より敬意と感謝を申し上げます。<br>
  さて、三鷹市におきましては共働き世帯の増加に伴い、保育園・幼稚園への遠距離通園や、小学校放課後の「のびのび広場（トワイライトステイ）」へのお迎えなど、<strong>「子どもの移動・送迎の壁」</strong>が保護者の就労制限や精神的孤立を招く大きな課題となっております。<br>
  私ども一般社団法人KidsRideは、同じ地域や同じ園に通う保護者同士が「通勤・送迎のついで」に助け合える民間主導の近隣送迎互助プラットフォームを準備しております。このたび、当事者のリアルな実情に基づいた施策設計を行うため、<strong>「三鷹市 子育て世帯の通園・送迎実態調査アンケート」</strong>を実施することといたしました。<br>
  つきましては、地域の現場を熟知された貴機関におかれまして、本調査への周知ご協力と、今後の事業推進に関する専門的なご助言を賜りたく、下記のとおりご相談申し上げます。
</div>

<div class="box">
  <div class="box-title">■ 本調査の概要および貴機関へのお願い事項</div>
  <table class="summary-table">
    <tr>
      <th>調査目的</th>
      <td>三鷹市内の未就学児〜小学生の保護者が抱える送迎の困りごと、第一希望園の断念実態、放課後預かり（のびのび広場等）の利用意向、および近隣互助へのニーズを客観的に把握し、地域に必要な支援モデルを設計するため。</td>
    </tr>
    <tr>
      <th>調査形式</th>
      <td>Webアンケート（スマートフォン等で回答可能・所要時間 約3分・全12問）<br>
      <strong>【完全無記名方式】</strong> 氏名・電話番号・住所・個人の特定につながる情報は一切収集いたしません。（モニター案内希望者のみ任意でメールアドレス受付）</td>
    </tr>
    <tr>
      <th>お願いしたい<br>ご協力内容</th>
      <td>
        <strong>① 施設内での広報協力：</strong> 館内のチラシ配架ラックへの案内チラシ設置、または掲示板へのポスター掲示<br>
        <strong>② 登録会員・利用者へのご案内：</strong> 可能であれば、貴機関のメルマガ、SNS、Webサイト等での告知紹介<br>
        <strong>③ 現場目線でのご助言：</strong> 三鷹市内の送迎事情の実態、事業推進にあたっての留意点や行政連携に関するアドバイス
      </td>
    </tr>
    <tr>
      <th>調査データの還元</th>
      <td>集計結果（統計レポート）は、三鷹市の子育て環境向上や地域福祉施策の検討に資するよう、ご協力いただいた貴機関にもご共有・フィードバックさせていただきます。</td>
    </tr>
  </table>
</div>

<div class="box" style="background:#f0fdf4; border-color:#bbf7d0;">
  <div class="box-title" style="color:#166534;">■ KidsRideが目指す「地域共生型互助モデル」の3大原則</div>
  <div style="font-size:8.3pt; line-height:1.6; color:#14532d;">
    <strong>1. 既存の公的福祉（ファミサポ等）との補完関係：</strong> 事前手続きが重い公的制度では対応が難しい「急な残業」「雨の日だけのついで送迎」を近隣住民間で補い、二重三重のセーフティネットを構築します。<br>
    <strong>2. 最高2億円の包括損害保険完備：</strong> あいおいニッセイ同和損保と包括特約を締結。自動車のみならず自転車・徒歩送迎中の事故も対人対物最高2億円で補償し、個人間トラブルを完全防止します。<br>
    <strong>3. 国土交通省（東京運輸支局）確認済みの適法性：</strong> 利益を伴わないガソリン代等の実費精算のみに限定した「無償互助ボランティアモデル」として適法性を確認済みです。
  </div>
</div>

<!-- フッター部分：上下分割レイアウト -->
<div class="footer-sign">
  <div class="footer-upper">
    ご多忙の折、大変恐縮に存じますが、何卒温かいご指導・ご協力を賜りますようお願い申し上げます。
  </div>
  <div style="border-top:1px dashed #cbd5e1; padding-top:6px; display:flex; justify-content:space-between; align-items:center; font-size:8pt; color:#475569;">
    <div style="white-space:nowrap;">
      <strong style="color:#0f172a; font-size:8.8pt;">一般社団法人KidsRide</strong>　代表理事：七夕 光明
    </div>
    <div style="font-size:7.8pt; color:#64748b; white-space:nowrap;">
      所在地：東京都三鷹市　連絡先：contact@kidsride.jp　公式サイト：https://www.kidsride.jp/
    </div>
  </div>
</div>

</body>
</html>
"""

# ==============================================================================
# 2. 事業概要・地域課題・安全対策説明シート（A4見開き2P）
# ==============================================================================
# （前回の洗練版をそのまま維持）
with open(os.path.join(workspace_dir, "generate_refined_kits.py"), "r", encoding="utf-8") as f:
    r_code = f.read()

import re
m_p2 = re.search(r'html_02_presentation_sheet = f"""(.*?)"""\n\n# ===', r_code, re.DOTALL)
html_02_presentation_sheet = m_p2.group(1) if m_p2 else ""

m_cards = re.search(r'html_04_cards_sheet = f"""(.*?)"""\n\n# ===', r_code, re.DOTALL)
html_04_cards_sheet = m_cards.group(1) if m_cards else ""

m_sample = re.search(r'html_05_survey_sample = f"""(.*?)"""\n\n# ===', r_code, re.DOTALL)
html_05_survey_sample = m_sample.group(1) if m_sample else ""

m_hearing = re.search(r'html_07_hearing_sheet = f"""(.*?)"""\n\n# ===', r_code, re.DOTALL)
html_07_hearing_sheet = m_hearing.group(1) if m_hearing else ""


# ==============================================================================
# 3. 市民向けアンケート告知チラシ兼ポスター（A4サイズ用紙いっぱいに拡大 ＆ フッター上下分割）
# ==============================================================================
html_03_citizen_flyer = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>三鷹市 子育て世帯の通園・送迎アンケート</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 8mm 9mm 8mm 9mm;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{
    height: 100%;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    background: white;
    letter-spacing: 0.03em;
  }}
  .flyer-border {{
    border: 4px solid #0284c7;
    border-radius: 16px;
    padding: 16px 20px;
    height: 100%;
    min-height: 279mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #ffffff;
    box-sizing: border-box;
  }}
  .logo-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2.5px solid #e0f2fe;
    padding-bottom: 10px;
    margin-bottom: 12px;
  }}
  .logo-img {{
    height: 48px;
    object-fit: contain;
  }}
  .badge-area {{
    background: #ea580c;
    color: white;
    font-weight: 800;
    font-size: 10pt;
    padding: 5px 16px;
    border-radius: 20px;
    letter-spacing: 0.05em;
  }}
  .title-section {{
    text-align: center;
    margin: 6px 0 16px 0;
  }}
  .main-catch {{
    font-size: 22.5pt;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.35;
    margin: 0 0 8px 0;
    letter-spacing: 0.02em;
  }}
  .main-catch span {{
    color: #0284c7;
  }}
  .sub-catch {{
    font-size: 11.2pt;
    color: #475569;
    font-weight: 700;
  }}
  .trouble-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
  }}
  .trouble-card {{
    background: #fff7ed;
    border: 2px solid #fed7aa;
    border-radius: 10px;
    padding: 13px 15px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 9.6pt;
    line-height: 1.5;
  }}
  .trouble-icon {{
    background: #ea580c;
    color: white;
    font-size: 13pt;
    font-weight: 900;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
  }}
  .action-box {{
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border: 3px solid #0284c7;
    border-radius: 14px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.1);
  }}
  .qr-wrapper {{
    background: white;
    padding: 10px;
    border-radius: 12px;
    border: 2.5px solid #bae6fd;
    text-align: center;
    flex-shrink: 0;
  }}
  .qr-wrapper img {{
    width: 120px;
    height: 120px;
    display: block;
  }}
  .action-content {{
    flex: 1;
  }}
  .action-lead {{
    font-size: 13.5pt;
    font-weight: 900;
    color: #0369a1;
    margin-bottom: 6px;
  }}
  .action-desc {{
    font-size: 9.4pt;
    color: #334155;
    line-height: 1.6;
  }}
  .pill-container {{
    display: flex;
    gap: 8px;
    margin-top: 8px;
  }}
  .pill {{
    background: #0284c7;
    color: white;
    font-size: 8.5pt;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 14px;
  }}
  .features-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    text-align: center;
    margin-bottom: 14px;
  }}
  .feat-card {{
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 10px;
    padding: 10px 8px;
    font-size: 8.4pt;
  }}
  .feat-card strong {{
    display: block;
    color: #0284c7;
    font-size: 9.8pt;
    margin-bottom: 4px;
  }}
  
  /* フッター：上下分割レイアウト */
  .footer-section {{
    border-top: 2px solid #e0f2fe;
    padding-top: 10px;
  }}
  .footer-notice {{
    text-align: center;
    font-size: 8.5pt;
    color: #475569;
    font-weight: 600;
    margin-bottom: 6px;
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: 6px;
    padding: 6px 10px;
  }}
  .footer-info {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 8.2pt;
    color: #64748b;
  }}
</style>
</head>
<body>

<div class="flyer-border">
  <!-- ロゴヘッダー -->
  <div class="logo-header">
    <div>
      {f'<img src="data:image/png;base64,{logo_b64}" class="logo-img" alt="KidsRide">' if logo_b64 else '<span style="font-size:20pt; font-weight:900; color:#0284c7;">KidsRide</span>'}
    </div>
    <div class="badge-area">三鷹市 子育て世帯実態調査</div>
  </div>

  <!-- メインキャッチ -->
  <div class="title-section">
    <div class="main-catch">子どもの<span>「通園・送迎」</span>で<br>困った経験はありませんか？</div>
    <div class="sub-catch">登降園や放課後の移動に関する、三鷹のパパ・ママのリアルな声をお聞かせください</div>
  </div>

  <!-- お悩み4選 -->
  <div class="trouble-grid">
    <div class="trouble-card">
      <div class="trouble-icon">！</div>
      <div>
        <strong style="color:#c2410c; display:block; margin-bottom:3px; font-size:10.2pt;">雨や悪天候の日の自転車送迎</strong>
        カッパを着せての雨中送迎がつらい…下の子も連れての移動で毎日本当にぐったりしてしまう
      </div>
    </div>
    <div class="trouble-card">
      <div class="trouble-icon">！</div>
      <div>
        <strong style="color:#c2410c; display:block; margin-bottom:3px; font-size:10.2pt;">急な残業でお迎えに間に合わない</strong>
        電車遅延や突発仕事で18時の迎えに遅れそう…近くに頼れる親族もおらず焦ってしまう
      </div>
    </div>
    <div class="trouble-card">
      <div class="trouble-icon">！</div>
      <div>
        <strong style="color:#c2410c; display:block; margin-bottom:3px; font-size:10.2pt;">送迎距離の壁で第一希望園を諦めた</strong>
        本当は通わせたかった認可園があったのに、毎日の送迎が無理で別の園を選ばざるを得なかった
      </div>
    </div>
    <div class="trouble-card">
      <div class="trouble-icon">！</div>
      <div>
        <strong style="color:#c2410c; display:block; margin-bottom:3px; font-size:10.2pt;">のびのび広場・習い事の送迎どうする？</strong>
        学童やトワイライトステイ（夜間預かり）を使いたいが、夕方以降のお迎えがネックになる
      </div>
    </div>
  </div>

  <!-- QRコード回答アクション -->
  <div class="action-box">
    <div class="action-content">
      <div class="action-lead">スマホで約3分！タップするだけで完了</div>
      <div class="action-desc">
        右のQRコードをカメラで読み取ってご回答ください。<br>
        皆様のリアルな声をもとに、三鷹市内で顔見知り同士が「ついで」に助け合える、安心・安全な新しい送迎サポートの実現を目指します。
      </div>
      <div class="pill-container">
        <span class="pill">完全無記名方式</span>
        <span class="pill">個人情報不要</span>
        <span class="pill">全12問・選択式</span>
      </div>
      <div style="font-size:8.5pt; color:#0284c7; font-weight:700; margin-top:8px;">
        https://www.kidsride.jp/#survey
      </div>
    </div>
    <div class="qr-wrapper">
      {f'<img src="data:image/png;base64,{qr_b64}" alt="QRコード">' if qr_b64 else 'QR'}
      <span style="font-size:8pt; color:#0284c7; font-weight:800; display:block; margin-top:4px;">カメラで読取</span>
    </div>
  </div>

  <!-- 特徴3点 -->
  <div class="features-grid">
    <div class="feat-card">
      <strong>完全無記名方式</strong>
      氏名・電話番号・住所不要<br>安心して本音を回答できます
    </div>
    <div class="feat-card">
      <strong>民間保護者有志</strong>
      営利勧誘は一切ありません<br>三鷹市在住の保護者による調査
    </div>
    <div class="feat-card">
      <strong>地域協働・還元</strong>
      集計結果は三鷹市のより良い<br>子育て環境づくりに活用します
    </div>
  </div>

  <!-- フッター：上下分割 -->
  <div class="footer-section">
    <div class="footer-notice">
      ※本アンケート結果は統計処理され、個人情報不要で地域のより良い子育て環境設計のために大切に活用されます。
    </div>
    <div class="footer-info">
      <div style="white-space:nowrap;">
        <strong>実施主体：一般社団法人KidsRide</strong>　代表理事：七夕 光明
      </div>
      <div style="white-space:nowrap; font-size:7.8pt;">
        お問い合わせ：contact@kidsride.jp　公式サイト：https://www.kidsride.jp/
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""

# 各団体の定義
targets = [
    {
        "folder_name": "01_三鷹市市民協働センター様_面談セット",
        "org_name": "三鷹市市民協働センター",
        "org_sub": "ご担当者様（市民活動・NPO支援窓口）"
    },
    {
        "folder_name": "02_NPO法人子育てコンビニ様_面談セット",
        "org_name": "特定非営利活動法人 子育てコンビニ",
        "org_sub": "代表理事・スタッフ・ご担当者様"
    },
    {
        "folder_name": "03_三鷹市社会福祉協議会様_面談セット",
        "org_name": "社会福祉法人 三鷹市社会福祉協議会",
        "org_sub": "ご担当者様（地域福祉課・ボランティアセンター）"
    }
]

print("=== 01依頼状フッター上下分割 ＆ 03ポスター全面拡大 再生成開始 ===")

for t in targets:
    org_folder = os.path.join(BASE_DIR, t["folder_name"])
    os.makedirs(org_folder, exist_ok=True)
    print(f"\n▼ フォルダ更新: {t['folder_name']}")
    
    # 01. 個別宛名入り公式依頼状（フッター上下分割）
    req_html = get_request_letter_html(t["org_name"], t["org_sub"])
    req_pdf = os.path.join(org_folder, f"01_アンケート調査協力・情報提供依頼状（{t['org_name']}様向け）.pdf")
    render_pdf(req_html, req_pdf)
    
    # 03. チラシ兼ポスター（A4全面拡大 ＆ フッター上下分割）
    p3_pdf = os.path.join(org_folder, "03_市民向けアンケート告知チラシ兼ポスター（A4カラー）.pdf")
    render_pdf(html_03_citizen_flyer, p3_pdf)

print("\n=== すべての再生成と配置が完了しました ===")
