import os
import subprocess
import base64

OUTPUT_DIR = os.path.expanduser("~/Desktop/01_KidsRide/KidsRide_アンケート資料")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. 画像ファイルを読み込んでBase64エンコード
def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

workspace_dir = os.path.dirname(__file__)
logo_path = os.path.join(workspace_dir, "logo.png")
symbol_path = os.path.join(workspace_dir, "logo-symbol.png")
qr_path = os.path.join(workspace_dir, "qr_web_card.png")

logo_b64 = get_base64_image(logo_path)
symbol_b64 = get_base64_image(symbol_path)
qr_b64 = get_base64_image(qr_path)

# ==============================================================================
# PDF 01: 【園長先生向け 公式依頼状】（A4・ジャスト1ページ）
# ==============================================================================
html_01_request_letter = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>園長先生・施設長様向け アンケート調査協力依頼状</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 11mm 15mm 10mm 15mm;
  }}
  * {{ box-sizing: border-box; }}
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
    font-weight: 700;
  }}
  table.details-table td {{
    background: #ffffff;
    color: #0f172a;
  }}
  .profile-grid {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 3px;
    font-size: 7.8pt;
    line-height: 1.35;
  }}
  .footer-contact {{
    margin-top: 6px;
    padding-top: 4px;
    border-top: 1px solid #cbd5e1;
    font-size: 7.5pt;
    color: #475569;
    display: flex;
    justify-content: space-between;
  }}
</style>
</head>
<body>

<div class="header-meta">
  <div>
    <div style="font-size:9pt; color:#475569;">三鷹市内 保育園・幼稚園・認定こども園</div>
    <div style="font-size:11pt; font-weight:800; color:#0f172a; margin-top:1px;">園長・施設長 各位</div>
  </div>
  <div style="text-align:right; font-size:7.8pt; line-height:1.35;">
    <div>2026年11月吉日</div>
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
<p>そこで、地域の実態把握および安全な地域送迎互助プラットフォーム設計の基礎資料として、貴園の保護者様を対象とするアンケート調査への周知・配架ご協力をお願い申し上げます。敬具</p>

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
      <td>「無料実証実験（モニター体験）」への優先案内（ご希望の方のみ）</td>
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
    <div>✔ <strong>集計結果サマリーの無償提供</strong>：貴園の保護者ニーズを分析したレポートを後日無償提供（今後の園運営検討に活用可能）。</div>
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
  <div>【お問い合わせ・POPお届け窓口】一般社団法人KidsRide 代表理事 七夕 光明 / TEL: 070-2251-1896 / Email: info@kids-ride.jp</div>
  <div style="text-align:right;">回答URL: https://www.kidsride.jp/#survey</div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 02: 【園長面談用 事業概要・安全対策・実証実験説明シート】（A4・見開き2ページ）
# ==============================================================================
html_02_presentation_sheet = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>園長面談用 事業概要・安全管理・実態調査説明シート</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #0f172a;
    line-height: 1.45;
    font-size: 8.6pt;
    margin: 0;
    padding: 0;
  }}
  .page-break {{ page-break-before: always; }}

  .header {{
    background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
    color: white;
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 6px rgba(234, 88, 12, 0.2);
  }}
  .header-title {{
    font-size: 13pt;
    font-weight: 800;
    margin: 0 0 2px 0;
  }}
  .header-sub {{
    font-size: 8pt;
    opacity: 0.95;
  }}
  .header-tag {{
    background: rgba(255,255,255,0.22);
    border: 1px solid rgba(255,255,255,0.45);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 7.8pt;
    font-weight: 700;
    text-align: right;
  }}

  .sec-title {{
    font-size: 10pt;
    font-weight: 800;
    color: #c2410c;
    border-left: 4px solid #ea580c;
    padding-left: 8px;
    margin: 8px 0 5px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 6px;
  }}

  .card {{
    border: 1px solid #fed7aa;
    border-radius: 6px;
    padding: 7px 10px;
    background: #ffffff;
  }}
  .card-h {{
    font-size: 9pt;
    font-weight: 800;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
  }}

  table.comp-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8pt;
    margin: 4px 0;
  }}
  table.comp-table th, table.comp-table td {{
    border: 1px solid #fed7aa;
    padding: 4px 6px;
    text-align: left;
  }}
  table.comp-table th {{
    background: #fffaf5;
    color: #43302b;
    font-weight: 700;
  }}

  .page-footer {{
    border-top: 1px solid #fed7aa;
    padding-top: 4px;
    margin-top: 8px;
    font-size: 7.5pt;
    color: #85726b;
    display: flex;
    justify-content: space-between;
  }}
</style>
</head>
<body>

<!-- ==================== 1ページ目 ==================== -->
<div class="header">
  <div>
    <div class="header-title">地域送迎相互支援プラットフォーム「KidsRide」事業概要</div>
    <div class="header-sub">三鷹市における保育・教育現場の負担軽減と、保護者間の安心な共助インフラ構築</div>
  </div>
  <div class="header-tag">
    一般社団法人KidsRide<br>面談説明用資料（1/2）
  </div>
</div>

<div class="sec-title">
  <span>1. 背景：保護者とお迎え現場（園）が直面する課題</span>
</div>
<div class="grid-2">
  <div class="card" style="border-top: 3px solid #ef4444; background:#fffafb;">
    <div class="card-h" style="color:#b91c1c;">保護者側の課題：日常の突発的ピンチ</div>
    <ul style="margin:0; padding-left:16px; font-size:7.8pt; color:#334155; line-height:1.4;">
      <li><strong>急な残業・電車の遅延</strong>：「今日どうしてもお迎えに間に合わない」焦り</li>
      <li><strong>きょうだいの急な発熱・通院</strong>：受診と重なり園へのお迎えが物理的に困難</li>
      <li><strong>悪天候時の送迎危険</strong>：大雨・猛暑の中での危険な子ども乗せ自転車送迎</li>
      <li><strong>既存サービスの壁</strong>：ファミサポ等は事前調整が必須／知らない人に預ける不安</li>
    </ul>
  </div>
  <div class="card" style="border-top: 3px solid #f59e0b; background:#fffdfa;">
    <div class="card-h" style="color:#b45309;">園・保育士側のリアルな3大負担・リスク</div>
    <ul style="margin:0; padding-left:16px; font-size:7.8pt; color:#334155; line-height:1.4;">
      <li><strong>居残り残業・配置維持</strong>：少数の遅延児対応のため保育士2名体制を拘束</li>
      <li><strong>代理引き渡しの確認緊張</strong>：降園ラッシュ時の電話確認・誤認防止の極度の神経負担</li>
      <li><strong>事故時の巻き込まれ不安</strong>：保護者同士の勝手な預かり合いで事故があった際の責任懸念</li>
      <li><strong>先生方の心理的負荷</strong>：保護者を責められない中で現場保育士にかかる残業・疲弊</li>
    </ul>
  </div>
</div>

<div class="sec-title">
  <span>2. 解決策：KidsRideが提供する「顔の見える保護者間互助」</span>
</div>
<div class="card" style="border-left: 4px solid #ea580c; margin-bottom:6px; background:#fffaf5;">
  <div style="font-size:8.6pt; line-height:1.48;">
    <strong>「同じ園に通う身元確認済みの保護者同士」</strong>が、日頃のお迎えの「ついで」に助け合うWebプラットフォームです。見知らぬ他人に預ける不安を解消し、園コミュニティの絆の中で安心・安全・低負担な送迎インフラを構築します。
  </div>
</div>

<table class="comp-table">
  <thead>
    <tr>
      <th style="width:20%;">比較項目</th>
      <th style="width:40%;">一般的なベビーシッター・ファミサポ</th>
      <th style="width:40%; background:#fff7ed; color:#c2410c;">KidsRide（当事業モデル）</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>支援者と利用者の関係</th>
      <td>地域の協力会員や登録シッター（一般市民）</td>
      <td><strong>同じ保育園・幼稚園に通う顔見知りの保護者同士</strong></td>
    </tr>
    <tr>
      <th>マッチング形式</th>
      <td>事前調整・事前顔合わせが必須（数日前〜1週間前）</td>
      <td><strong>Webシステムによる即時・柔軟なマッチング</strong>（当日対応可）</td>
    </tr>
    <tr>
      <th>安心感・防犯面</th>
      <td>見知らぬ他人に子どもを預ける心理的ハードル</td>
      <td><strong>同一園の在園証明・身元審査済み</strong>で安心感が極めて高い</td>
    </tr>
    <tr>
      <th>対価・適法性</th>
      <td>有償運送・高額な時間報酬（時給1,000円〜2,500円）</td>
      <td><strong>ガソリン実費のみ（営利性なし）／東京運輸支局確認済</strong></td>
    </tr>
  </tbody>
</table>

<div class="sec-title">
  <span>3. 法令適合性と、園・現場の「3大負担ゼロ」の仕組み</span>
</div>
<div class="grid-2">
  <div class="card" style="border-left:3px solid #10b981;">
    <div class="card-h" style="color:#047857;">国土交通省（東京運輸支局）確認済み</div>
    <div style="font-size:7.7pt; line-height:1.38; color:#334155;">
      自家用車での送迎は「ガソリン代実費（11円/km）のみ」の精算に限定。東京運輸支局へ事前確認を行い、<strong>「道路運送法第78条の登録・許可は不要（完全合法）」</strong>である旨の正式回答を受領済みです。
    </div>
  </div>
  <div class="card" style="border-left:3px solid #ea580c;">
    <div class="card-h" style="color:#c2410c;">先生方の業務負担ゼロ ＆ リスク解消</div>
    <div style="font-size:7.7pt; line-height:1.38; color:#334155;">
      ① <strong>先生の仲介作業ゼロ</strong>：マッチングや連絡は保護者同士がアプリ完結。<br>
      ② <strong>引き渡し確認の不安解消</strong>：アプリの顔写真照合で誤認を徹底防止。<br>
      ③ <strong>園の責任巻き込まれゼロ</strong>：全送迎に包括保険完備＋KidsRide窓口対応。
    </div>
  </div>
</div>

<div class="page-footer">
  <div>一般社団法人KidsRide（代表理事 七夕 光明）</div>
  <div>1 / 2 ページ</div>
</div>

<!-- ==================== 2ページ目 ==================== -->
<div class="page-break"></div>

<div class="header" style="background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);">
  <div>
    <div class="header-title">安全管理体制 ＆ 実態調査・実証実験のロードマップ</div>
    <div class="header-sub">万全の事故補償体制と、園・地域に貢献する段階的ステップ</div>
  </div>
  <div class="header-tag">
    一般社団法人KidsRide<br>面談説明用資料（2/2）
  </div>
</div>

<div class="sec-title" style="color:#0f766e; border-left-color:#0f766e;">
  <span>4. 三重の安全運行管理システム（事故・誤認防止の徹底）</span>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:6px; margin-bottom:8px;">
  <div class="card" style="border-top: 3px solid #ea580c;">
    <div class="card-h" style="color:#c2410c; font-size:8.4pt;">① 厳格な身元・在園審査</div>
    <div style="font-size:7.6pt; line-height:1.35; color:#334155;">
      運転免許証等の公的身元確認に加え、<strong>在園証明書・保護者証等による同一園在籍確認</strong>を必須化。身元の確かな保護者のみが参加。
    </div>
  </div>
  <div class="card" style="border-top: 3px solid #10b981;">
    <div class="card-h" style="color:#047857; font-size:8.4pt;">② リアルタイムGPS＆認証</div>
    <div style="font-size:7.6pt; line-height:1.35; color:#334155;">
      送迎中は<strong>保護者スマホへ現在地を常時GPS配信</strong>。引き渡し時はアプリの<strong>顔写真照合コード認証</strong>により園児の取り違えを防止。
    </div>
  </div>
  <div class="card" style="border-top: 3px solid #f59e0b;">
    <div class="card-h" style="color:#b45309; font-size:8.4pt;">③ アルコール検知・点検</div>
    <div style="font-size:7.6pt; line-height:1.35; color:#334155;">
      車送迎時は<strong>出庫前アルコール検知（0.00mg/L）および日常点検記録</strong>を義務化。チャイルドシート（R129適合）を常設。
    </div>
  </div>
</div>

<div class="sec-title" style="color:#0f766e; border-left-color:#0f766e;">
  <span>5. 大手損保会社との「全送迎包括損害保険」を完備</span>
</div>
<div class="card" style="border: 1.5px solid #0f766e; background:#f0fdfa; margin-bottom:8px;">
  <div style="font-size:8.2pt; line-height:1.45; color:#134e4a;">
    万が一の事故時に個人間トラブルへ発展させないため、あいおいニッセイ同和損害保険様と連携し、<strong>団体包括保険を契約・完備</strong>しています。<br>
    ・<strong>自動車送迎</strong>：対人賠償 無制限 ／ 対物賠償 無制限 ／ 人身傷害 3,000万円（サポーターの個人保険を使わせずKidsRide保険を優先適用）<br>
    ・<strong>徒歩・自転車送迎</strong>：第三者賠償責任 最高2億円 ／ サポーター自身のケガ補償（入院・通院・死亡）<br>
    ※事故発生時の初期対応・損保会社対応・示談代行はすべてKidsRide事務局が窓口を一本化して対応します。
  </div>
</div>

<div class="sec-title" style="color:#0f766e; border-left-color:#0f766e;">
  <span>6. 今回のお願い：保護者向け実態調査（アンケート）の趣旨</span>
</div>
<table class="comp-table">
  <tr>
    <th style="width:25%;">調査の目的</th>
    <td>三鷹市内の保護者が直面する送迎課題（残業、発熱、悪天候）の深刻度と潜在ニーズを把握し、安全な仕組みづくりの基礎資料とするため。</td>
  </tr>
  <tr>
    <th>形式・保護者負担</th>
    <td>スマホでQRコードを読み取り<strong>約2分で回答完了（選択式中心・完全無記名方式）</strong>。個人情報の登録は不要。</td>
  </tr>
  <tr>
    <th>園へのお願い</th>
    <td><strong>登降園打刻機横や下駄箱の上に「A5卓上POP」と「名刺サイズQRカード」を置かせていただくだけ</strong>（先生方のプリント配架作業は不要）。</td>
  </tr>
  <tr>
    <th>貴園へのメリット</th>
    <td>
      ① <strong>「貴園の保護者の送迎実態分析レポート」を無償提供</strong>（園運営や次年度計画、保護者支援の根拠資料として）。<br>
      ② <strong>先生方の夕方負担（居残り残業・代理確認リスク）解消</strong>に向けた地域共助の先進事例として、今後の実証実験への優先参画が可能。
    </td>
  </tr>
</table>

<div class="sec-title" style="color:#0f766e; border-left-color:#0f766e;">
  <span>7. 今後のロードマップ（実態調査から無料実証実験へ）</span>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:6px;">
  <div class="card" style="background:#fffaf5; border-color:#fed7aa;">
    <div style="font-weight:800; color:#ea580c; font-size:8pt;">STEP 1（11月中旬）</div>
    <div style="font-weight:700; font-size:8.4pt; margin:1px 0;">保護者実態調査の実施</div>
    <div style="font-size:7.5pt; color:#475569;">市内園にてアンケート実施、ニーズ上位の園を把握。</div>
  </div>
  <div class="card" style="background:#f0fdf4; border:1px solid #86efac;">
    <div style="font-weight:800; color:#047857; font-size:8pt;">STEP 2（11月下旬〜）</div>
    <div style="font-weight:700; font-size:8.4pt; margin:1px 0;">無料実証実験（先行モニター）</div>
    <div style="font-size:7.5pt; color:#14532d;">希望保護者・希望園のみで小規模に安全運用を検証。</div>
  </div>
  <div class="card" style="background:#fffaf5; border-color:#fed7aa;">
    <div style="font-weight:800; color:#ea580c; font-size:8pt;">STEP 3（2027年春〜）</div>
    <div style="font-weight:700; font-size:8.4pt; margin:1px 0;">地域互助インフラ本格展開</div>
    <div style="font-size:7.5pt; color:#475569;">検証結果を踏まえ、安心して使える地域互助モデルへ。</div>
  </div>
</div>

<div class="page-footer">
  <div>一般社団法人KidsRide（代表理事 七夕 光明 / TEL: 070-2251-1896 / Email: info@kids-ride.jp）</div>
  <div>2 / 2 ページ</div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 03: 【園内掲示チラシ兼卓上三角POP】（A4・KidsRideブランドカラー＆ロゴ仕様）
# ==============================================================================
html_03_pop = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>保護者向け 掲示チラシ兼卓上POP</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 8mm 10mm 8mm 10mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1c1917;
    margin: 0;
    padding: 0;
    background: #ffffff;
  }}
  .poster-container {{
    border: 3.5px solid #ea580c;
    border-radius: 14px;
    padding: 12px 18px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #ffffff;
  }}
  .brand-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    border-bottom: 1.5px solid #fed7aa;
    margin-bottom: 8px;
  }}
  .brand-logo-img {{
    height: 54px;
    object-fit: contain;
  }}
  .header-badge {{
    background: #fff7ed;
    border: 1px solid #ea580c;
    color: #ea580c;
    font-size: 8.6pt;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.3px;
  }}
  .main-hero-banner {{
    background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
    color: white;
    text-align: center;
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 9px;
    box-shadow: 0 4px 12px rgba(234, 88, 12, 0.2);
  }}
  .hero-tag {{
    display: inline-block;
    background: rgba(255, 255, 255, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.45);
    color: #ffffff;
    font-size: 8.5pt;
    font-weight: 800;
    padding: 2px 10px;
    border-radius: 12px;
    margin-bottom: 5px;
    letter-spacing: 0.5px;
  }}
  .main-copy {{
    font-size: 15.5pt;
    font-weight: 900;
    line-height: 1.35;
    letter-spacing: 0.5px;
    margin: 0;
  }}
  .sub-copy {{
    font-size: 8.8pt;
    margin-top: 4px;
    color: #ffedd5;
  }}
  .troubles-box {{
    background: #fffaf5;
    border: 1px solid #fed7aa;
    border-radius: 8px;
    padding: 9px 13px;
    margin-bottom: 8px;
  }}
  .trouble-title {{
    font-size: 9.2pt;
    font-weight: 800;
    color: #c2410c;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 4px;
  }}
  .trouble-item {{
    font-size: 8.5pt;
    line-height: 1.45;
    color: #43302b;
    margin-bottom: 3px;
    display: flex;
    align-items: flex-start;
    gap: 6px;
  }}
  .check-icon {{
    color: #ea580c;
    font-weight: 900;
    font-size: 9.5pt;
  }}
  .solution-box {{
    background: #f0fdf4;
    border: 1.5px solid #86efac;
    border-radius: 8px;
    padding: 9px 13px;
    margin-bottom: 8px;
  }}
  .solution-title {{
    font-size: 9.5pt;
    font-weight: 800;
    color: #166534;
    margin-bottom: 3px;
  }}
  .solution-text {{
    font-size: 8.4pt;
    line-height: 1.42;
    color: #14532d;
  }}
  .cta-box {{
    background: #fff7ed;
    border: 2px dashed #ea580c;
    border-radius: 10px;
    padding: 11px 16px;
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 7px;
    overflow: hidden;
  }}
  .cta-qr {{
    width: 90px;
    height: 90px;
    background: #ffffff;
    padding: 4px;
    border-radius: 8px;
    border: 1px solid #fed7aa;
    flex-shrink: 0;
  }}
  .cta-qr img {{
    width: 100%;
    height: 100%;
    object-fit: contain;
  }}
  .cta-content {{
    flex: 1;
  }}
  .cta-badge {{
    background: #ea580c;
    color: white;
    font-size: 8pt;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 3px;
  }}
  .cta-heading {{
    font-size: 12.5pt;
    font-weight: 800;
    color: #1c1917;
    line-height: 1.3;
    margin-bottom: 3px;
  }}
  .meta-footer {{
    border-top: 1px solid #fed7aa;
    padding-top: 6px;
    font-size: 7.1pt;
    color: #85726b;
    display: flex;
    justify-content: space-between;
    align-items: center;
    white-space: nowrap;
    overflow: hidden;
  }}
</style>
</head>
<body>

<div class="poster-container">
  <div class="brand-header">
    <div>
      {f'<img src="data:image/png;base64,{logo_b64}" class="brand-logo-img" alt="KidsRide">' if logo_b64 else '<span style="font-size:16pt; font-weight:900; color:#ea580c;">KidsRide</span>'}
    </div>
    <div class="header-badge">三鷹市・子育て世帯対象アンケート（約2分・完全無記名）</div>
  </div>

  <div class="main-hero-banner">
    <div class="hero-tag">保護者アンケート実態調査</div>
    <h1 class="main-copy">「今日、お迎えに間に合わないかも…」<br>と焦った経験はありませんか？</h1>
    <div class="sub-copy">雨の日・急な残業・きょうだいの発熱…ピンチを助け合える仕組みを【当園で実現するため】のアンケートです</div>
  </div>

  <div class="troubles-box">
    <div class="trouble-title">こんなお悩みや困りごとはありませんか？</div>
    <div class="trouble-item"><span class="check-icon">✔</span> 突然の残業や会議が入ったが、お迎えの延長が難しく職場を飛び出したことがある</div>
    <div class="trouble-item"><span class="check-icon">✔</span> きょうだいが急に発熱し、もう一方の園へのお迎えとの両立に困り果てた</div>
    <div class="trouble-item"><span class="check-icon">✔</span> 大雨や猛暑の中、幼児2人を乗せた自転車での送迎に強い危険を感じている</div>
    <div class="trouble-item"><span class="check-icon">✔</span> ファミサポ等は事前予約が必要で当日の急用には使えず、全く知らない人に預けるのも不安</div>
  </div>

  <div class="solution-box">
    <div class="solution-title">同じ園の保護者同士で「ついでに」助け合える仕組みを目指して</div>
    <div class="solution-text">
      一般社団法人KidsRideは、<strong>「同じ保育園・幼稚園に通い、身元が確認された保護者同士」</strong>が日々の送迎やピンチの時に安心・安全に助け合える仕組み（GPS追跡・顔写真照合・包括損害保険完備）を準備しています。<strong>当園での実証実験・導入の実現に向けて、皆様のリアルな声をお聞かせください！</strong>
    </div>
  </div>

  <div class="cta-box">
    <div class="cta-qr">
      {f'<img src="data:image/png;base64,{qr_b64}" alt="アンケートQRコード">' if qr_b64 else '<div style="font-size:8pt; text-align:center; padding-top:30px;">QRコード</div>'}
    </div>
    <div class="cta-content">
      <span class="cta-badge">回答時間：約2分・完全無記名</span>
      <div class="cta-heading">スマホのカメラで読み取ってすぐ回答！</div>
      <div style="font-size:8.4pt; line-height:1.45; color:#334155; margin-bottom:4px;">
        個人情報の登録なしで選択肢をタップするだけ。「うちの園でも使いたい！」の声をぜひお寄せください。<br>
        ご希望の方には<strong style="color:#ea580c;">【無料実証実験モニター】</strong>の優先案内をお届けします！
      </div>
      <div style="font-size:8pt; color:#64748b;">
        Webから直接回答: <strong style="color:#ea580c;">https://www.kidsride.jp/#survey</strong>
      </div>
    </div>
  </div>

  <div class="meta-footer">
    <div style="white-space:nowrap;">実施主体: 一般社団法人KidsRide（代表理事 七夕 光明 / 三鷹市下連雀在住・保護者）</div>
    <div style="white-space:nowrap;">※回答データは統計処理され、個人情報の登録不要で回答いただけます</div>
  </div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 04: 【持ち帰り用 名刺サイズQRカード 面付け用】（A4 1枚に10枚・KidsRideブランド仕様）
# ==============================================================================
html_04_cards_sheet = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>持ち帰り用 名刺サイズQRカード 面付けシート</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 8mm 17mm 8mm 17mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    margin: 0;
    padding: 0;
    background: #ffffff;
  }}
  .grid-container {{
    display: grid;
    grid-template-columns: repeat(2, 91mm);
    grid-template-rows: repeat(5, 55mm);
    gap: 0;
    justify-content: center;
  }}
  .card-item {{
    width: 91mm;
    height: 55mm;
    border: 0.5px dashed #fed7aa;
    display: flex;
    background: #ffffff;
    overflow: hidden;
    position: relative;
  }}
  /* 左側オレンジピラー（KidsRideブランド） */
  .card-left-pillar {{
    width: 19.5mm;
    background: linear-gradient(180deg, #ea580c 0%, #f97316 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 3mm 1mm;
    text-align: center;
    color: white;
    flex-shrink: 0;
    gap: 5px;
  }}
  .card-symbol {{
    width: 33px;
    height: 33px;
    background: white;
    border-radius: 8px;
    padding: 2.5px;
    object-fit: contain;
  }}
  .card-pillar-text {{
    font-size: 7.2pt;
    font-weight: 900;
    color: white;
    line-height: 1.1;
    letter-spacing: -0.01em;
  }}

  /* 中央メインエリア */
  .card-main {{
    flex: 1;
    padding: 3.5mm 3.8mm 3.5mm 4.2mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .card-badge {{
    background: #fff7ed;
    border: 1px solid #ea580c;
    color: #ea580c;
    font-size: 5.3pt;
    font-weight: 800;
    padding: 1px 5px;
    border-radius: 3px;
    display: inline-block;
    width: fit-content;
    line-height: 1.2;
  }}
  .card-mid {{
    display: flex;
    flex-direction: column;
    gap: 1.1mm;
    margin: auto 0;
  }}
  .card-title {{
    font-size: 7.5pt;
    font-weight: 900;
    color: #1c1917;
    line-height: 1.28;
    letter-spacing: -0.01em;
  }}
  .card-concept {{
    background: #fffaf5;
    padding: 2.2px 3.5px;
    font-size: 4.35pt;
    line-height: 1.32;
    color: #334155;
    border-radius: 4px;
    letter-spacing: -0.025em;
    width: 100%;
    box-sizing: border-box;
  }}
  .card-concept strong {{
    color: #ea580c;
    font-weight: 800;
  }}
  .card-desc {{
    font-size: 4.4pt;
    color: #64748b;
    line-height: 1.3;
    letter-spacing: -0.02em;
  }}
  .card-gift {{
    font-size: 5.6pt;
    color: #ea580c;
    font-weight: 800;
    line-height: 1.2;
  }}
  .card-footer {{
    font-size: 4.8pt;
    color: #85726b;
    margin-top: 0.5mm;
    line-height: 1.2;
  }}

  /* 右側QRエリア */
  .card-right-qr {{
    width: 23mm;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2mm 1mm;
    border-left: 1px dashed #fed7aa;
    flex-shrink: 0;
  }}
  .mini-qr {{
    width: 52px;
    height: 52px;
    display: block;
    margin: 0 auto;
  }}
  .mini-url {{
    font-size: 5.2pt;
    color: #ea580c;
    font-weight: 800;
    margin-top: 2px;
    letter-spacing: -0.01em;
  }}
</style>
</head>
<body>

<div class="grid-container">
  {''.join([f'''
  <div class="card-item">
    <div class="card-left-pillar">
      {f'<img src="data:image/png;base64,{symbol_b64}" class="card-symbol" alt="Icon">' if symbol_b64 else ''}
      <div class="card-pillar-text">KidsRide</div>
    </div>
    <div class="card-main">
      <div class="card-top">
        <span class="card-badge">三鷹市・約2分・完全無記名</span>
      </div>
      <div class="card-mid">
        <div class="card-title">「お迎え間に合わない…！」と<br>焦った経験はありませんか？</div>
        <div class="card-concept">
          <strong>【KidsRideの目指すこと】</strong><br>
          <span style="white-space:nowrap;">同じ園の保護者同士で「ついで送迎」を助け合う、</span><br>
          <span style="white-space:nowrap;">安心・安全な地域互助の仕組みづくり</span>
        </div>
        <div class="card-desc">
          <span style="white-space:nowrap;">雨や残業時のピンチを助け合える仕組みを、</span><br>
          <span style="white-space:nowrap;">当園で実現するためのアンケート調査です。</span>
        </div>
      </div>
      <div class="card-bottom">
        <div class="card-gift">★無料実証実験モニター優先案内あり★</div>
        <div class="card-footer">一般社団法人KidsRide（三鷹市下連雀）</div>
      </div>
    </div>
    <div class="card-right-qr">
      {f'<img src="data:image/png;base64,{qr_b64}" class="mini-qr" alt="QR">' if qr_b64 else 'QR'}
      <div class="mini-url">kidsride.jp/#survey</div>
    </div>
  </div>
  ''' for _ in range(10)])}
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 05: 【保護者アンケート設問見本票】（A4・2ページ）
# ==============================================================================
html_05_survey_sample = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>保護者アンケート設問見本票</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    line-height: 1.4;
    font-size: 8.2pt;
    margin: 0;
    padding: 0;
  }}
  .page-break {{ page-break-before: always; }}
  .header {{
    background: #0f172a;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .doc-title {{ font-size: 11pt; font-weight: 800; margin: 0; }}
  .doc-sub {{ font-size: 7.5pt; color: #94a3b8; }}
  .intro-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 7.8pt;
    line-height: 1.4;
    margin-bottom: 8px;
  }}
  .sec-badge {{
    background: #ea580c;
    color: white;
    font-size: 8pt;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    margin: 6px 0 4px 0;
    display: inline-block;
  }}
  .q-card {{
    border: 1px solid #fed7aa;
    border-radius: 5px;
    padding: 5px 8px;
    margin-bottom: 5px;
    background: #ffffff;
  }}
  .q-title {{
    font-weight: 700;
    font-size: 8.2pt;
    color: #0f172a;
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
  }}
  .q-tag {{
    font-size: 6.8pt;
    padding: 1px 5px;
    border-radius: 3px;
    background: #fff7ed;
    color: #ea580c;
    font-weight: 700;
  }}
  .opt-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2px 8px;
    font-size: 7.6pt;
    color: #334155;
  }}
  .footer {{
    border-top: 1px solid #fed7aa;
    padding-top: 4px;
    margin-top: 6px;
    font-size: 7.2pt;
    color: #85726b;
    display: flex;
    justify-content: space-between;
  }}
</style>
</head>
<body>

<!-- 1ページ目 -->
<div class="header">
  <div>
    <div class="doc-title">【見本】子どもの通園・送迎に関する保護者実態調査（Q1〜Q6）</div>
    <div class="doc-sub">Webアンケート設問一覧・園長先生確認用見本票</div>
  </div>
  <div style="font-size:7.5pt; text-align:right;">一般社団法人KidsRide<br>https://www.kidsride.jp/#survey</div>
</div>

<div class="intro-box">
  <strong>【調査趣旨および個人情報の取り扱いについて】</strong><br>
  本アンケートは、三鷹市における保育園・幼稚園・学童等の通園・送迎の実態と保護者ニーズを把握し、地域での安全な送迎互助体制の構築のための基礎資料として実施するものです。個人情報の入力は一切不要（完全無記名方式）であり、統計的に集計処理いたします。
</div>

<div class="sec-badge">1. 基本属性</div>
<div class="q-card">
  <div class="q-title"><span>Q1. お子様の年齢（学年）を教えてください</span><span class="q-tag">複数選択可</span></div>
  <div class="opt-grid">
    <div>□ 0〜1歳（乳児）</div><div>□ 2〜3歳（年少少・年少）</div>
    <div>□ 4〜5歳（年中・年長）</div><div>□ 小学校低学年（1〜3年生）</div>
    <div>□ 小学校高学年（4〜6年生）</div>
  </div>
</div>
<div class="q-card">
  <div class="q-title"><span>Q2. 主にお住まいのエリア（町名）を教えてください</span><span class="q-tag">単一選択</span></div>
  <div class="opt-grid">
    <div>○ 下連雀</div><div>○ 上連雀</div><div>○ 新川・中原</div>
    <div>○ 北野・牟礼</div><div>○ 井の頭</div><div>○ 大沢・深大寺・野崎</div>
  </div>
</div>
<div class="q-card">
  <div class="q-title"><span>Q3. 現在お子様が通われている施設種別</span><span class="q-tag">複数選択可</span></div>
  <div class="opt-grid">
    <div>□ 認可保育園（公立・私立）</div><div>□ 私立幼稚園・認定こども園</div>
    <div>□ 認証保育所・企業主導型保育等</div><div>□ 学童保育所・放課後デイ等</div>
  </div>
</div>

<div class="sec-badge">2. 日常の送迎手段と距離・所要時間</div>
<div class="q-card">
  <div class="q-title"><span>Q4. 普段の主な送迎手段</span><span class="q-tag">複数選択可</span></div>
  <div class="opt-grid">
    <div>□ 徒歩（手つなぎ・ベビーカー）</div><div>□ 子ども乗せ自転車（電動含む）</div>
    <div>□ 自家用車</div><div>□ 路線バス・電車</div>
  </div>
</div>
<div class="q-card">
  <div class="q-title"><span>Q5. 自宅から園までの片道の移動時間</span><span class="q-tag">単一選択</span></div>
  <div class="opt-grid">
    <div>○ 徒歩5分未満</div><div>○ 徒歩5〜10分程度</div>
    <div>○ 徒歩10〜20分程度</div><div>○ 徒歩20分以上（または車・バス等で通園）</div>
  </div>
</div>

<div class="sec-badge">3. 送迎に関する困りごと・突発ピンチ</div>
<div class="q-card">
  <div class="q-title"><span>Q6. これまで送迎で「困った・焦った」経験（あてはまるものをすべて選択）</span><span class="q-tag">複数選択可</span></div>
  <div class="opt-grid">
    <div>□ 急な残業や仕事でお迎え時間に間に合わない</div><div>□ きょうだいの急な発熱・通院でお迎えに行けない</div>
    <div>□ 悪天候（大雨・台風・大雪・猛暑）時の移動が危険</div><div>□ 自身の体調不良や妊娠中・産後の送迎がつらい</div>
    <div>□ 園行事や保護者会時の送迎調整が難しい</div><div>□ 特に困った経験はない</div>
  </div>
</div>

<div class="footer">
  <div>一般社団法人KidsRide（三鷹市下連雀）/ お問い合わせ: info@kids-ride.jp</div>
  <div>1 / 2 ページ（※完全無記名による実態調査見本票）</div>
</div>

<!-- 2ページ目 -->
<div class="page-break"></div>
<div class="header">
  <div>
    <div class="doc-title">【見本】子どもの通園・送迎に関する保護者実態調査（Q7〜Q12）</div>
    <div class="doc-sub">Webアンケート設問一覧・園長先生確認用見本票（続き）</div>
  </div>
  <div style="font-size:7.5pt; text-align:right;">一般社団法人KidsRide<br>https://www.kidsride.jp/#survey</div>
</div>

<div class="sec-badge">4. 送迎助け合い・地域連携サービスへの受容度</div>
<div class="q-card">
  <div class="q-title"><span>Q7. もし「同じ園の身元確認済み保護者同士」で送迎を助け合える仕組み（※損保補償付き）があれば利用したいですか？</span><span class="q-tag">単一選択</span></div>
  <div class="opt-grid">
    <div>○ ぜひ定期的に利用したい</div><div>○ 急な残業や困った時だけ単発で利用したい</div>
    <div>○ 条件や相手（顔見知りか等）次第で検討</div><div>○ あまり利用したいとは思わない / わからない</div>
  </div>
</div>
<div class="q-card">
  <div class="q-title"><span>Q8. 急な残業等の際、三鷹駅前「のびのびひろば（夜22時まで）」等への送迎代行があれば利用したいですか？</span><span class="q-tag">単一選択</span></div>
  <div class="opt-grid">
    <div>○ ぜひ利用したい</div><div>○ 状況によっては利用したい</div>
    <div>○ 利用しない（園の延長等で対応可能）</div><div>○ 制度（トワイライトステイ）を知らなかった</div>
  </div>
</div>
<div class="q-card">
  <div class="q-title"><span>Q9. 他の保護者にお子様の送迎をお願いする場合、どのような手段であれば安心できますか？</span><span class="q-tag">複数選択可</span></div>
  <div class="opt-grid">
    <div>□ 徒歩での引率（見守り歩行）</div><div>□ 自転車での送迎（幼児同乗器・ヘルメット）</div>
    <div>□ 自家用車での送迎（適合チャイルドシート）</div><div>□ 同じクラスや顔見知りの保護者であれば安心</div>
    <div>□ リアルタイムで現在地がGPS追跡できれば安心</div><div>□ どのような手段であっても不安がある</div>
  </div>
</div>

<div class="sec-badge">5. 送迎サポーター（助け手）としての関心・自由記述</div>
<div class="q-card">
  <div class="q-title"><span>Q10. ご自身のお子様を送迎する「ついで」に、同じ園のお子様を一緒に送迎することに関心はありますか？</span><span class="q-tag">単一選択</span></div>
  <div class="opt-grid">
    <div>○ ついでであれば協力したい（困った時はお互い様）</div><div>○ タイミングや都合が合う日なら引き受けてもよい</div>
    <div>○ 興味はあるが責任や事故が心配</div><div>○ 自分は「頼む側」専任で利用したい / 余裕はない</div>
  </div>
</div>
<div class="q-card">
  <div class="q-title"><span>Q11. 子どもの通園・送迎に関して「こんなサポートがあったら助かる」というご要望や日頃のお悩み（自由記述）</span><span class="q-tag">任意</span></div>
  <div style="height:28px; border:1px dashed #cbd5e1; border-radius:3px; background:#f8fafc; padding:3px; font-size:7pt; color:#94a3b8;">
    （自由記入欄：日頃感じている送迎の負担や地域に求めるサポートについてご自由にお書きください）
  </div>
</div>
<div class="q-card">
  <div class="q-title"><span>Q12. 「無料実証実験（モニター体験）」の優先案内を希望される方の連絡先</span><span class="q-tag">任意</span></div>
  <div style="font-size:7.2pt; color:#64748b; margin-top:1px;">
    メールアドレス記入欄（※ご記入いただいたアドレスは実証実験の案内のみに使用し、アンケート回答の統計処理とは完全に分離管理されます）
  </div>
</div>

<div class="footer">
  <div>一般社団法人KidsRide（三鷹市下連雀）/ お問い合わせ: contact@kidsride.jp</div>
  <div>2 / 2 ページ（※完全無記名による実態調査見本票）</div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 06: 【園長アプローチ完全マニュアル アポ取り〜面談スクリプト】（A4・3ページ）
# ==============================================================================
html_06_manual_script = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>園長アプローチ完全マニュアル・アポ取り〜面談スクリプト</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #0f172a;
    line-height: 1.45;
    font-size: 8.5pt;
    margin: 0;
    padding: 0;
  }}
  .page-break {{ page-break-before: always; }}

  .header {{
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    color: white;
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .header-title {{ font-size: 12pt; font-weight: 800; margin: 0 0 2px 0; }}
  .header-sub {{ font-size: 7.8pt; color: #cbd5e1; }}
  .header-badge {{
    background: #ea580c;
    color: white;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: 700;
  }}

  .sec-h {{
    font-size: 9.8pt;
    font-weight: 800;
    color: #c2410c;
    border-left: 4px solid #ea580c;
    padding-left: 8px;
    margin: 10px 0 6px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .tag {{
    font-size: 7pt;
    padding: 1px 6px;
    border-radius: 3px;
    font-weight: 700;
  }}
  .tag-blue {{ background: #fff7ed; color: #ea580c; }}
  .tag-green {{ background: #dcfce7; color: #15803d; }}

  .script-box {{
    background: #ffffff;
    border: 1.5px solid #fed7aa;
    border-left: 5px solid #ea580c;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 8px;
    font-size: 8.4pt;
    line-height: 1.5;
  }}
  .script-box.green {{
    border-color: #86efac;
    border-left-color: #10b981;
  }}
  .hl {{ background: #fef08a; font-weight: 700; padding: 0 2px; }}

  .card {{
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 7px 10px;
    margin-bottom: 6px;
    background: #ffffff;
  }}

  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 6px;
  }}

  .page-footer {{
    border-top: 1px solid #e2e8f0;
    padding-top: 4px;
    margin-top: 8px;
    font-size: 7.2pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
  }}
</style>
</head>
<body>

<!-- ==================== 1ページ目 ==================== -->
<div class="header">
  <div>
    <div class="header-title">園長アプローチ完全マニュアル（アポ取りから面談実践まで）</div>
    <div class="header-sub">三鷹市内の保育園・幼稚園におけるアンケート配架＆実証実験参加に向けた実践ガイド</div>
  </div>
  <div class="header-badge">実践カンペ（1/3）</div>
</div>

<div class="sec-h">
  <span>1. アプローチ全体ロードマップ（幼稚園・保育園別の基本戦略）</span>
</div>
<div class="grid-2">
  <div class="card" style="border-top:3px solid #10b981;">
    <div style="font-weight:800; color:#047857; font-size:8.6pt; margin-bottom:2px;">【私立幼稚園】自園フラッグシップ展開</div>
    <div style="font-size:7.8pt; line-height:1.4; color:#334155;">
      ① <strong>三鷹のぞみ幼稚園（自園）</strong>：七夕自身が在園児の保護者として園長先生へ直接ご相談・第1号のPOP設置を承諾いただく。<br>
      ② <strong>他幼稚園への横展開</strong>：「のぞみ幼稚園の園長先生にもご相談・設置いただいている」という実績をフックに個別連絡。
    </div>
  </div>
  <div class="card" style="border-top:3px solid #ea580c;">
    <div style="font-weight:800; color:#c2410c; font-size:8.6pt; margin-bottom:2px;">【私立保育園】園長会フォロー型展開</div>
    <div style="font-size:7.8pt; line-height:1.4; color:#334155;">
      ① <strong>11/9園長会直後（11/10〜12）</strong>：会長先生からの口頭共有を受け、自発的に連絡をくださる園の問い合わせ対応に集中。<br>
      ② <strong>11/13以降のフォロー</strong>：未連絡の園へ「資料FAX/郵送の許可をもらう」低負荷フォロー連絡を実施。
    </div>
  </div>
</div>

<div class="sec-h">
  <span>2. アポ取り〜面談〜設置までの5ステップ</span>
</div>
<div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:5px; margin-bottom:8px; text-align:center;">
  <div class="card" style="padding:6px 4px; background:#f8fafc;">
    <div style="font-weight:800; color:#ea580c; font-size:7.5pt;">STEP 1</div>
    <div style="font-weight:700; font-size:8pt; margin:1px 0;">電話アポ</div>
    <div style="font-size:6.8pt; color:#64748b;">1分即決トークで資料送付または訪問約束</div>
  </div>
  <div class="card" style="padding:6px 4px; background:#f8fafc;">
    <div style="font-weight:800; color:#ea580c; font-size:7.5pt;">STEP 2</div>
    <div style="font-weight:700; font-size:8pt; margin:1px 0;">資料事前送付</div>
    <div style="font-size:6.8pt; color:#64748b;">依頼状・説明シートをFAX/メールで送信</div>
  </div>
  <div class="card" style="padding:6px 4px; background:#fff7ed; border:1px solid #ea580c;">
    <div style="font-weight:800; color:#c2410c; font-size:7.5pt;">STEP 3</div>
    <div style="font-weight:800; font-size:8pt; margin:1px 0;">園長面談</div>
    <div style="font-size:6.8pt; color:#c2410c;">5〜10分で想い・負担ゼロを伝えPOP提示</div>
  </div>
  <div class="card" style="padding:6px 4px; background:#f8fafc;">
    <div style="font-weight:800; color:#ea580c; font-size:7.5pt;">STEP 4</div>
    <div style="font-weight:700; font-size:8pt; margin:1px 0;">POP・カード設置</div>
    <div style="font-size:6.8pt; color:#64748b;">打刻機横・下駄箱上に置くだけ</div>
  </div>
  <div class="card" style="padding:6px 4px; background:#f8fafc;">
    <div style="font-weight:800; color:#ea580c; font-size:7.5pt;">STEP 5</div>
    <div style="font-weight:700; font-size:8pt; margin:1px 0;">レポート還元</div>
    <div style="font-size:6.8pt; color:#64748b;">集計結果を持参し実証実験を提案</div>
  </div>
</div>

<div class="sec-h">
  <span>3. 【電話編】受付突破スクリプト（30秒）</span>
  <span class="tag tag-blue">電話推奨：10:00〜11:00 または 14:30〜16:00</span>
</div>
<div class="script-box">
  「お忙しい時間帯に大変恐縮です。私、三鷹市下連雀で子育て支援の活動を行っております、一般社団法人KidsRide（キッズライド）の七夕（たなばた）と申します。私自身も三鷹市内で子どもを育てている保護者です。<br>
  実は、<span class="hl">市内の保護者様が夕方の通園やお迎えで直面している困りごとに関する実態調査アンケート</span>を行っておりまして、先生方にお手間を取らせない形での簡単なアンケート配架のご相談でございます。<br>
  <strong>園長先生または主任の先生に1分だけ</strong>お取り次ぎいただくことは可能でしょうか？」
</div>

<div class="sec-h">
  <span>4. 【電話編】園長先生へのアポ取りトーク（園種別）</span>
</div>
<div class="grid-2">
  <div class="card" style="border-left:4px solid #10b981;">
    <div style="font-weight:800; color:#047857; margin-bottom:3px;">パターンA：幼稚園向け（自園・紹介型）</div>
    <div style="font-size:7.9pt; line-height:1.45; color:#334155;">
      「園長先生、お忙しいところ恐れ入ります。一般社団法人KidsRideの七夕です。私自身、三鷹のぞみ幼稚園に子どもを通わせている現役の保護者です。<br>
      日頃先生方が直面されている<strong>夕方のお迎え遅延等のご負担を減らすため、保護者の送迎実態調査</strong>を行っております。先生方の作業は一切不要で、玄関に小さなPOPを置かせていただくだけのご相談です。<br>
      <strong>一度、概要をまとめたA4の資料をFAXまたはメールでお送りしてもよろしいでしょうか？</strong>（ご都合よろしければ見本を持参し5分だけご挨拶に伺えます）」
    </div>
  </div>
  <div class="card" style="border-left:4px solid #ea580c;">
    <div style="font-weight:800; color:#c2410c; margin-bottom:3px;">パターンB：保育園向け（園長会フォロー型）</div>
    <div style="font-size:7.9pt; line-height:1.45; color:#334155;">
      「園長先生、保育でお忙しいところ恐れ入ります。一般社団法人KidsRideの七夕と申します。<br>
      <span class="hl">先日の園長会にて会長先生より口頭でご紹介がございました、子どもの送迎に関する実態調査</span>の件でご連絡いたしました。会長先生からお聞き及びかと存じますが、先生方にお手間を取らせない形での調査となっております。<br>
      もしよろしければ、<strong>概要をまとめたA4・1枚の依頼資料をFAXまたはメールでお送りするだけでもよろしいでしょうか？</strong>」
    </div>
  </div>
</div>

<div class="page-footer">
  <div>一般社団法人KidsRide（代表理事 七夕 光明）</div>
  <div>1 / 3 ページ</div>
</div>

<!-- ==================== 2ページ目 ==================== -->
<div class="page-break"></div>

<div class="header">
  <div>
    <div class="header-title">園長面談（5〜10分）実践トークスクリプト（完全カンペ）</div>
    <div class="header-sub">訪問時に手元資料（依頼状・説明シート・卓上POP現物）を見せながら話す実戦スクリプト</div>
  </div>
  <div class="header-badge">面談カンペ（2/3）</div>
</div>

<div class="sec-h" style="margin-top:6px; margin-bottom:4px;">
  <span>1. 【最重要】お見せする資料の順番（黄金ステップ）＆ Web実演デモの極意</span>
</div>
<div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:5px; margin-bottom:6px;">
  <div class="card" style="border-top:3px solid #64748b; padding:4px 6px;">
    <div style="font-weight:800; color:#334155; font-size:7.5pt;">① 手渡し（開始1分）</div>
    <div style="font-weight:700; font-size:7.8pt; color:#0f172a;">01_公式依頼状</div>
    <div style="font-size:6.8pt; color:#64748b; line-height:1.3;">まず名刺と共にお渡しし、代表の身元と調査趣旨の誠意・透明性を提示</div>
  </div>
  <div class="card" style="border-top:3px solid #ea580c; padding:4px 6px; background:#fff7ed;">
    <div style="font-weight:800; color:#ea580c; font-size:7.5pt;">② メイン（2〜7分）</div>
    <div style="font-weight:700; font-size:7.8pt; color:#c2410c;">02_事業説明シート</div>
    <div style="font-size:6.8pt; color:#7c2d12; line-height:1.3;">見開き2Pを開き、仕組み・適法性・包括保険・現場の3大負担解消を解説</div>
  </div>
  <div class="card" style="border-top:3px solid #10b981; padding:4px 6px;">
    <div style="font-weight:800; color:#10b981; font-size:7.5pt;">③ 実物提示（8〜10分）</div>
    <div style="font-weight:700; font-size:7.8pt; color:#047857;">03_POP ＆ 04_名刺</div>
    <div style="font-size:6.8pt; color:#64748b; line-height:1.3;">「置くだけ」の実物を提示。打刻機横や下駄箱上の設置イメージを共有</div>
  </div>
  <div class="card" style="border-top:3px solid #94a3b8; padding:4px 6px;">
    <div style="font-weight:800; color:#64748b; font-size:7.5pt;">④ 質問時のみ</div>
    <div style="font-weight:700; font-size:7.8pt; color:#334155;">05_設問見本票</div>
    <div style="font-size:6.8pt; color:#64748b; line-height:1.3;">「どんな質問があるの？」と聞かれた時だけ出し、個人情報不要を証明</div>
  </div>
</div>

<div class="card" style="background:#f8fafc; border:1px dashed #64748b; padding:5px 8px; margin-bottom:6px; font-size:7.4pt; line-height:1.38; color:#334155;">
  <strong>💡【Webサイト・QRコードの10秒実演デモの極意】</strong><br>
  ・<strong>最初からスマホ画面を見せるのはNG</strong>（紙の公式資料の方が公的信頼感が高く、園長先生の警戒心を解きます）。<br>
  ・名刺カードを手に取ったタイミングで<strong>「先生、保護者様はスマホでこのように10秒で直感回答できます」</strong>とご自身のスマホカメラでQRを読み取り、実際のアンケート画面と公式サイトを<strong>10秒だけチラ見せ</strong>するのが最も信頼を獲得できます。
</div>

<div class="sec-h" style="margin-top:6px; margin-bottom:4px;">
  <span>2. 園長面談トークスクリプト（現場の3大負担に寄り添う構成）</span>
</div>

<div class="script-box green" style="padding:6px 10px; margin-bottom:5px; font-size:7.8pt; line-height:1.42;">
  <div style="font-weight:800; color:#047857; margin-bottom:1px;">【Step 1：挨拶と現役保護者としての共感】（所要：1分／01_依頼状を手渡し）</div>
  「園長先生、本日は大変ご多忙の折にお時間をいただき誠にありがとうございます。一般社団法人KidsRide代表の七夕でございます。私自身も三鷹市下連雀在住で、市内の園に通わせている現役の父親です。<br>
  本日伺いましたのは、日頃先生方が直面されている<span class="hl">『夕方の急なお迎え遅延による居残り残業や保育士配置の維持』など、先生方のご負担を少しでも減らしたい</span>という想いからでございます。<br>
  電車遅延や急な残業、きょうだいの発熱時、保護者も『早く迎えに行きたいのにどうしても行けない』という深い悩みを抱えております。」
</div>

<div class="script-box green" style="padding:6px 10px; margin-bottom:5px; font-size:7.8pt; line-height:1.42;">
  <div style="font-weight:800; color:#047857; margin-bottom:1px;">【Step 2：KidsRideの安心設計と先生の3大リスク解消】（所要：2分／02_説明シートを指差しながら）</div>
  「そこで私どもは、見知らぬ他人に預けるのではなく、<span class="hl">『同じ園に通う身元確認済みの保護者同士』が、お迎えのついでに助け合える仕組み</span>を準備しております。<br>
  特に先生方が心配される<strong>①夕方の居残り残業、②代理人引き渡し時の誤認・連れ去りリスク、③勝手な送迎で事故が起きた際の園の巻き込まれ懸念</strong>を根本から解消するため、<span class="hl">リアルタイムGPS追跡、顔写真照合ワンタイムコード、対人対物無制限・最高2億円の包括保険</span>を完備しております。<br>
  東京運輸支局へ自家用車実費運送として確認済みであり、万が一の事故窓口もKidsRideが一本化して対応いたします。」
</div>

<div class="script-box green" style="padding:6px 10px; margin-bottom:5px; font-size:7.8pt; line-height:1.42;">
  <div style="font-weight:800; color:#047857; margin-bottom:1px;">【Step 3：今回のお願いと先生方の作業負担ゼロ】（所要：1.5分／03_POP実物・04_カードを提示）</div>
  「本日貴園にお願いしたいのは、アプリ加入の勧誘ではなく、保護者の送迎実態を把握するための<span class="hl">『実態調査アンケート（約2分・完全無記名）』へのご協力</span>です。<br>
  先生方にプリントを配布していただく手間は一切ございません。こちらの<span class="hl">『卓上POP』と『名刺サイズのQRカード』を、登降園打刻機横や下駄箱上に置いていただくだけ</span>です。<br>
  保護者様はスマホでQRを読み取って選択肢をタップするだけで、個人情報の入力も不要です。」
</div>

<div class="script-box green" style="padding:6px 10px; margin-bottom:4px; font-size:7.8pt; line-height:1.42;">
  <div style="font-weight:800; color:#047857; margin-bottom:1px;">【Step 4：貴園へのメリットとクロージング】（所要：1分）</div>
  「集計完了後、<span class="hl">『貴園の保護者ニーズを分析した実態調査レポート』を無償でお届け</span>いたします。延長保育対策や次年度の運営計画にぜひご活用いただけます。先生方のお手間は一切取らせませんので、ぜひ玄関の隅に設置させていただけないでしょうか？」
</div>

<div class="page-footer">
  <div>一般社団法人KidsRide（代表理事 七夕 光明）</div>
  <div>2 / 3 ページ</div>
</div>

<!-- ==================== 3ページ目 ==================== -->
<div class="page-break"></div>

<div class="header">
  <div>
    <div class="header-title">想定問答・反論切り返し集（Q&A）＆ 面談チェックリスト</div>
    <div class="header-sub">園長先生からの懸念・質問に落ち着いて即答するための切り返しトーク（保育現場の負担解消）</div>
  </div>
  <div class="header-badge">実践カンペ（3/3）</div>
</div>

<div class="sec-h" style="margin-top:4px; margin-bottom:4px;">
  <span>よくある懸念・質問への切り返しトーク（Q&A）</span>
</div>

<div class="card" style="border-left: 4px solid #ef4444; margin-bottom:4px; padding:5px 8px;">
  <div style="font-weight:800; color:#b91c1c; font-size:7.8pt;">Q1. 「特定の民間企業やサービスの宣伝・チラシは、園のルールで置けないのですが…」</div>
  <div style="font-size:7.3pt; line-height:1.35; color:#334155; margin-top:2px;">
    <strong>【切り返し】</strong>「園長先生、おっしゃる通りです。営利チラシの配布ではなく、<span class="hl">三鷹市の保護者が直面する送迎実態を把握する完全無記名アンケート</span>です。個人情報の収集や営業活動は一切行いませんのでご安心ください。」
  </div>
</div>

<div class="card" style="border-left: 4px solid #f59e0b; margin-bottom:4px; padding:5px 8px;">
  <div style="font-weight:800; color:#b45309; font-size:7.8pt;">Q2. 「送迎中に万が一事故やトラブルが起きた場合、園に責任が及ぶことはありませんか？」</div>
  <div style="font-size:7.3pt; line-height:1.35; color:#334155; margin-top:2px;">
    <strong>【切り返し】</strong>「園に責任やご負担が及ぶことは一切ございません。<span class="hl">あいおいニッセイ同和損保様と最高2億円の包括賠償保険および対人対物無制限保険</span>を契約済みです。事故窓口もKidsRideが一本化して対応いたします。」
  </div>
</div>

<div class="card" style="border-left: 4px solid #ea580c; margin-bottom:4px; padding:5px 8px;">
  <div style="font-weight:800; color:#c2410c; font-size:7.8pt;">Q3. 「保護者の個人情報やプライバシーの扱いは大丈夫ですか？」</div>
  <div style="font-size:7.3pt; line-height:1.35; color:#334155; margin-top:2px;">
    <strong>【切り返し】</strong>「はい、今回のアンケートは<span class="hl">氏名・住所・電話番号などの個人情報は一切取得しない『完全無記名方式』</span>です。統計処理のみを行いますのでプライバシー侵害の心配はございません。」
  </div>
</div>

<div class="card" style="border-left: 4px solid #6366f1; margin-bottom:4px; padding:5px 8px;">
  <div style="font-weight:800; color:#4338ca; font-size:7.8pt;">Q4. 「今は行事や新年度準備などで忙しくて、対応する余裕がないのですが…」</div>
  <div style="font-size:7.3pt; line-height:1.35; color:#334155; margin-top:2px;">
    <strong>【切り返し】</strong>「先生、お忙しい時期に恐縮です。だからこそ先生方の作業は一切ございません。こちらのPOPとカードを<span class="hl">玄関の隅に置いていただくだけ</span>で、回収・集計もすべてWeb上で行われます。」
  </div>
</div>

<div class="card" style="border-left: 4px solid #10b981; margin-bottom:4px; padding:5px 8px; background:#f0fdf4;">
  <div style="font-weight:800; color:#047857; font-size:7.8pt;">Q5. 「保護者以外の代理引き渡しで、園児の誤認や連れ去りトラブルの心配はありませんか？」</div>
  <div style="font-size:7.3pt; line-height:1.35; color:#166534; margin-top:2px;">
    <strong>【切り返し】</strong>「極めて重要なご指摘です。KidsRideでは先生の目視確認だけに頼らず、<span class="hl">『顔写真付き身元確認証』と『ワンタイム認証照合』</span>をアプリで義務化しています。誰が迎えに来たかが事前に園・先生・保護者間で完全に共有・照合されるため、連れ去りや誤認リスクを徹底防止し、先生方の引き渡し時の極度の緊張負担を大幅に軽減します。」
  </div>
</div>

<div class="card" style="border-left: 4px solid #0284c7; margin-bottom:5px; padding:5px 8px; background:#f0f9ff;">
  <div style="font-weight:800; color:#0369a1; font-size:7.8pt;">Q6. 「先生たちの夕方の残業負担は本当に減るのですか？」</div>
  <div style="font-size:7.3pt; line-height:1.35; color:#0c4a6e; margin-top:2px;">
    <strong>【切り返し】</strong>「はい。電車遅延や急な残業で生じる『あと30分の居残り』が、同じ園の身元確かな保護者の助け合いで解消されます。<span class="hl">たった1名の居残りのために先生2名が残業拘束される事態を防止</span>でき、現場のシフト崩壊や疲弊を直接的に防ぐことができます。」
  </div>
</div>

<div class="sec-h" style="margin-top:4px; margin-bottom:3px;">
  <span>面談当日の持ち物チェックリスト</span>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px; font-size:7.2pt;">
  <div class="card" style="background:#fffaf5; border-color:#fed7aa; padding:4px 6px;">
    <div>✔ <strong>01_園長向け公式依頼状</strong>（印刷して手渡し）</div>
    <div>✔ <strong>02_事業概要・安全説明シート</strong>（カラー見開き2P）</div>
    <div>✔ <strong>05_設問見本票</strong>（質問があった時用・ホチキス留め）</div>
  </div>
  <div class="card" style="background:#fffaf5; border-color:#fed7aa; padding:4px 6px;">
    <div>✔ <strong>組み立て済み卓上POP</strong>（三角POP実物1個）</div>
    <div>✔ <strong>持ち帰り用名刺カード</strong>（束で20〜30枚）</div>
    <div>✔ <strong>KidsRide法人の名刺 ＆ スマホ</strong>（Web10秒実演用）</div>
  </div>
</div>

<div class="page-footer">
  <div>一般社団法人KidsRide（代表理事 七夕 光明 / TEL: 070-2251-1896 / Email: info@kids-ride.jp）</div>
  <div>3 / 3 ページ</div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF出力エンジン（Chrome Headless）
# ==============================================================================
os.makedirs("/tmp/chrome-pdf-profile", exist_ok=True)
chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

files_to_generate = [
    ("01_園長先生向け_アンケート調査協力依頼状", html_01_request_letter),
    ("02_園長面談用_事業概要・安全対策・実証実験説明シート", html_02_presentation_sheet),
    ("03_園内掲示ポスター兼卓上POP", html_03_pop),
    ("04_持ち帰り用_名刺サイズQRカード_10面シート", html_04_cards_sheet),
    ("05_保護者アンケート設問見本票", html_05_survey_sample),
    ("06_園長アプローチ完全マニュアル_アポ取りから面談スクリプト", html_06_manual_script)
]

print("=== PDF生成開始 ===")
for filename, html_content in files_to_generate:
    html_file = os.path.join(OUTPUT_DIR, f"{filename}.html")
    pdf_file = os.path.join(OUTPUT_DIR, f"{filename}.pdf")
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--user-data-dir=/tmp/chrome-pdf-profile",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(pdf_file):
        print(f"成功: {pdf_file}")
    else:
        print(f"失敗: {filename} - {res.stderr}")

print("=== すべてのPDF生成処理が完了しました ===")
