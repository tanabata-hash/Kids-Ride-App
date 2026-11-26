import os
import subprocess
import base64

OUTPUT_DIR = os.path.expanduser("~/Desktop/01_KidsRide/00_【明日持参・印刷用】地域協働・NPO・社協面談資料一式")
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
# 00. 【必読ガイドテキスト】訪問面談ガイド＆相談スクリプト
# ==============================================================================
guide_txt_content = """================================================================================
  三鷹市市民協働センター・子育てコンビニ・三鷹市社協 訪問面談ガイド ＆ 相談実践マニュアル
================================================================================
一般社団法人KidsRide（代表理事 七夕 光明）
作成日: 2026年11月26日

明日以降予定している、三鷹市内の主要な地域協働・子育て支援3機関へのご挨拶、
アンケート調査協力依頼、およびサービス推進アドバイスヒアリングのための実践ガイドです。

--------------------------------------------------------------------------------
【1. 今回の訪問先3機関の特徴とアプローチの要点】
--------------------------------------------------------------------------------

① 三鷹市市民協働センター（下連雀4-17-23）
  【役割・特徴】
    三鷹市内のNPO・市民活動・ボランティア団体の立ち上げや運営、協働を総合支援する拠点。
    市役所の市民協働推進課とも深く連携しています。
  【相手の関心事】
    ・地域課題を解決するための市民活動としての新規性・公共性・継続性
    ・市民協働事業提案制度や各種助成金制度への適合性
    ・他団体（シニア、自治会、他NPO）とのネットワーキング
  【お願いしたいこと & アドバイスを受けたいこと】
    1. センター内（情報コーナー・ラック等）へのアンケートチラシ・ポスターの配架
    2. メールマガジンや協働センターだより等での市民向け周知協力
    3. 「一般社団法人」として地域に根ざした活動を展開するための信頼形成や行政連携のアドバイス
    4. 三鷹市市民活動助成金や協働事業提案制度への応募に向けたアドバイス

② NPO法人 子育てコンビニ（下連雀3丁目・みたかスペースあい等）
  【役割・特徴】
    20年以上にわたり三鷹市で親と子の居場所（子育てサロン）、一時預かり、子育て情報誌発行を
    行ってきた、三鷹市で最も影響力と現場知見を持つ子育て支援NPOの草分け。
  【相手の関心事】
    ・現役の子育て世代がリアルに何に困っているか（当事者目線）
    ・安全性が本当に確保されているか（子どもの命を預かることの重み）
    ・母親や父親が孤立せず、地域で支え合える温かいコミュニティになっているか
  【お願いしたいこと & アドバイスを受けたいこと】
    1. 子育てサロン・広場等でのアンケートチラシ・名刺QRカードの配架・手渡し協力
    2. 子育てコンビニのSNS・ブログ・Webサイトでのアンケート回答呼びかけ
    3. 現場で耳にする「保育園・学童・習い事の送迎の困りごと」のリアルな実態のヒアリング
    4. 保護者が「互助送迎」を利用する際、どんな点に最も不安を感じ、どうすれば安心できるかのアドバイス

③ 社会福祉法人 三鷹市社会福祉協議会（社協）（新川6-37-1 元気創造プラザ内）
  【役割・特徴】
    地域福祉の推進役であり、みたかボランティアセンターの運営や、三鷹市ファミリーサポートセンター
    （ファミサポ）の事業等にも深く関わる公的福祉の中核。
  【相手の関心事】
    ・既存の公的福祉制度（ファミサポ、有償家事援助等）との関係性（競合ではなく補完か？）
    ・事故防止体制、保険の適用範囲、トラブル発生時の責任の所在
    ・地域ボランティア（シニア、育児卒業世代等）の育成や活動環境
  【お願いしたいこと & アドバイスを受けたいこと】
    1. ボランティアセンター等の掲示板へのアンケート告知ポスター・チラシ配架
    2. 既存のファミサポ等でカバーしきれない「日常の隙間（急な残業、ついで送迎）」のニーズ確認
    3. 今後地域サポーター（シニア等）を募る際の安全講習や巻き込み方へのアドバイス
    4. あいおいニッセイ同和損保（最高2億円）等の安全体制に対する専門的ご意見

--------------------------------------------------------------------------------
【2. 面談の流れ（黄金4ステップ・所要時間 約15〜20分）】
--------------------------------------------------------------------------------

保育園長への「営業・許可取り」とは異なり、今回は「地域の先輩・専門家へのご相談とアドバイスの依頼」
という誠実かつ協働的なスタンスが最も響きます。

◆ STEP 1：ご挨拶・自己紹介（開始2分）
  ・お渡し資料：【01_アンケート調査協力・情報提供依頼状】＋法人の名刺
  ・トーク要旨：
    「三鷹市内で自身も子育てをしております、一般社団法人KidsRideの七夕と申します。
      本日は、日頃から三鷹市の地域づくり・子育て支援に尽力されている皆様に、
      私どもの活動をご紹介し、現在進めております『三鷹市の子育て送迎実態調査アンケート』への
      ご協力と、今後の事業推進に関する専門的なご助言をいただきたくお伺いいたしました。」

◆ STEP 2：事業背景・地域課題の共有（3〜8分）
  ・お渡し資料：【02_事業概要・地域課題・安全対策説明シート】
  ・トーク要旨：
    「三鷹市は子育て環境が素晴らしい一方で、共働き世帯の増加や、第一希望園に入れず自宅から遠い園に
      通うケース、小学生の『のびのび広場（トワイライトステイ）』のお迎えの壁など、送迎に関する
      親御さんの負担や孤立化が深刻化しています。
      私たちは、国土交通省の適法基準（無償互助・実費精算のみ）と、あいおいニッセイ同和損保との
      最高2億円の包括保険を土台に、近隣の顔見知り保護者同士が『ついで』に助け合える仕組みを
      民間主導で準備しております。」

◆ STEP 3：アンケート協力のお願い（9〜12分）
  ・お渡し資料：【03_市民向けアンケート告知チラシ兼ポスター】
              【04_持ち帰り用_名刺サイズQRカード】
              【05_保護者アンケート設問見本票】
  ・トーク要旨：
    「机上の空論ではなく、三鷹市内の子育て当事者の生の声（本当の困りごとやニーズ）をしっかりと把握した上で
      モデル設計を行いたいと考えており、現在Webアンケートを実施しております。
      完全無記名で個人情報は一切取得せず、3分程度で回答できるものです。
      ぜひ施設内でのチラシ配架や、掲示板へのポスター掲示、可能であればSNS等での告知にご協力を
      いただけないでしょうか。」

◆ STEP 4：アドバイスのヒアリング・情報交換（13〜20分）★ここが最も重要！
  ・お渡し資料：【07_地域協働・サービス推進アドバイス_ヒアリング相談シート】
  ・トーク要旨：
    「また、本日一番お伺いしたかったこととして、長年三鷹市の地域現場を支えてこられた皆様から見て、
      このような保護者間の送迎互助を進めるにあたり、どのような課題や留意点があるか、
      率直なアドバイスやご意見をぜひご教示いただきたいと考えております。」

--------------------------------------------------------------------------------
【3. 相手から想定される質問と回答のポイント（Q&A）】
--------------------------------------------------------------------------------

Q1: 「三鷹市にはファミリーサポートセンターがありますが、どう違うのですか？」
A1: 「ファミサポは大変素晴らしい公的制度ですが、事前のマッチングや面談手続きが必要で、
      『今日急に残業になった』『雨の日だけ同じ方向の友達と一緒に連れて帰ってほしい』という
      突発的・日常的な“ついで”の移動には使いづらい側面があります。
      KidsRideはファミサポを代替するものではなく、日常の隙間を埋め、地域のセーフティネットを
      二重三重に厚くする補完関係を目指しています。」

Q2: 「事故が起きたときの補償や責任はどうなっていますか？」
A2: 「最も重視している部分です。あいおいニッセイ同和損保と包括特約を締結し、自動車送迎だけでなく
      自転車・徒歩送迎中も含め、対人・対物最高2億円（免責0円）の賠償責任保険を完備しています。
      また、送迎者本人のケガに対する傷害保険も付帯し、万が一の事故受付はKidsRide本部が窓口となり、
      個人の当事者同士に重い負担を負わせない仕組みを構築しています。」

Q3: 「お金のやり取りはどうなっていますか？いわゆる白タク行為になりませんか？」
A3: 「国土交通省（東京運輸支局）の通達に厳格に準拠しております。送迎による『報酬（運送利益）』は
      一切発生せず、ガソリン代等の実費精算（1回数百円程度）のみを認めるボランティア互助設計です。
      営利事業ではなく、地域の支え合い活動として設計しています。」

Q4: 「どんなアドバイスを求めているのですか？」
A4: 「主に3点ございます。
      ① 三鷹市の子育て世帯が送迎や預かりで実際に直面している現場のリアルな声
      ② 将来的に地域の元気なシニアや子育て卒業世代にもサポーターとして参加いただくための工夫
      ③ 行政（子ども政策部等）や他団体との適切な連携ルートや、市民活動助成金の活用可能性
      ぜひ皆様のお知恵をお借りできれば幸いです。」

--------------------------------------------------------------------------------
【4. 持参資料一覧とファイル構成】
--------------------------------------------------------------------------------
00_【必読】地域協働・NPO・社協_訪問面談ガイド＆相談スクリプト.txt
01_アンケート調査協力・情報提供依頼状（地域支援機関・NPO・社協向け）.pdf
02_事業概要・地域課題・安全対策説明シート（地域協働版・A4見開き2P）.pdf
03_市民向けアンケート告知チラシ兼ポスター（A4カラー）.pdf
04_持ち帰り用_名刺サイズQRカード_10面シート.pdf
05_保護者アンケート設問見本票（A4_2P）.pdf
07_地域協働・サービス推進アドバイス_ヒアリング相談シート.pdf
================================================================================
"""

with open(os.path.join(OUTPUT_DIR, "00_【必読】地域協働・NPO・社協_訪問面談ガイド＆相談スクリプト.txt"), "w", encoding="utf-8") as f:
    f.write(guide_txt_content)


# ==============================================================================
# PDF 01: 【地域支援機関・NPO・社協向け 公式依頼・相談状】（A4・ジャスト1P）
# ==============================================================================
html_01_request_letter = f"""<!DOCTYPE html>
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
    line-height: 1.5;
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
    padding: 6px 0;
    border-top: 2px solid #0284c7;
    border-bottom: 2px solid #0284c7;
    letter-spacing: 0.05em;
  }}
  .lead {{
    margin-bottom: 12px;
    text-indent: 1em;
    font-size: 9pt;
    line-height: 1.6;
  }}
  .box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 12px;
  }}
  .box-title {{
    font-weight: 700;
    color: #0369a1;
    font-size: 9.5pt;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  table.summary-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 6px;
    font-size: 8.5pt;
  }}
  table.summary-table th, table.summary-table td {{
    border: 1px solid #cbd5e1;
    padding: 6px 10px;
    vertical-align: top;
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
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 8pt;
    color: #475569;
  }}
</style>
</head>
<body>

<div class="header-meta">
  <div>
    <div style="font-size:9.5pt; font-weight:700; color:#334155;">各 位</div>
    <div style="font-size:8.5pt; color:#64748b; margin-top:2px;">（三鷹市市民協働センター 様 ／ NPO法人子育てコンビニ 様 ／ 三鷹市社会福祉協議会 様）</div>
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
  拝啓　時下ますますご清祥のこととお慶び申し上げます。日頃より三鷹市における地域コミュニティの醸成、子育て支援、ならびに福祉の向上に多大なるご尽力を賜り、心より敬意と感謝を申し上げます。<br>
  さて、三鷹市におきましては共働き世帯の増加に伴い、保育園・幼稚園への遠距離通園や、小学校放課後の「のびのび広場（トワイライトステイ）」へのお迎えなど、<strong>「子どもの移動・送迎の壁」</strong>が保護者の深刻な就労制限や精神的孤立を招く大きな課題となっております。<br>
  私ども一般社団法人KidsRideは、同じ地域や同じ園に通う保護者同士が「通勤・送迎のついで」に助け合える民間主導の近隣送迎互助プラットフォームを準備しております。このたび、机上の空論ではなく当事者のリアルな実情に基づいた施策設計を行うため、<strong>「三鷹市 子育て世帯の通園・送迎実態調査アンケート」</strong>を実施することといたしました。<br>
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
  <div style="font-size:8.2pt; line-height:1.55; color:#14532d;">
    <strong>1. 既存の公的福祉（ファミサポ等）との補完関係：</strong> 事前手続きが重い公的制度では対応が難しい「急な残業」「雨の日だけのついで送迎」を近隣住民間で補い、二重三重のセーフティネットを構築します。<br>
    <strong>2. 最高2億円の包括損害保険完備：</strong> あいおいニッセイ同和損保と包括特約を締結。自動車のみならず自転車・徒歩送迎中の事故も対人対物最高2億円で補償し、個人間トラブルを完全防止します。<br>
    <strong>3. 国土交通省（東京運輸支局）確認済みの適法性：</strong> 利益を伴わないガソリン代等の実費精算のみに限定した「無償互助ボランティアモデル」として適法性を確認済みです。
  </div>
</div>

<div class="footer-sign">
  <div>
    <strong>一般社団法人KidsRide</strong>　代表理事：七夕 光明<br>
    所在地：東京都三鷹市　連絡先：info@kidsride.jp / 公式サイト：https://www.kidsride.jp/
  </div>
  <div style="text-align:right;">
    ご多忙の折、大変恐縮に存じますが、何卒温かいご指導・ご協力を賜りますようお願い申し上げます。
  </div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 02: 【事業概要・地域課題・安全対策説明シート（地域協働版）】（A4見開き2P）
# ==============================================================================
html_02_presentation_sheet = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>事業概要・地域課題・安全対策説明シート（地域協働版）</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
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
  .page-container {{
    page-break-after: always;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .page-container:last-child {{
    page-break-after: auto;
  }}
  .top-banner {{
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
    color: white;
    padding: 10px 14px;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }}
  .section-card {{
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 9px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }}
  .section-header {{
    font-size: 9.8pt;
    font-weight: 800;
    color: #0369a1;
    border-bottom: 2px solid #bae6fd;
    padding-bottom: 4px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }}
  .grid-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
  }}
  .sub-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 7px 9px;
    font-size: 8.2pt;
  }}
  .badge {{
    background: #0284c7;
    color: white;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 7pt;
    font-weight: 700;
  }}
  .highlight-text {{
    color: #b91c1c;
    font-weight: 700;
  }}
</style>
</head>
<body>

<!-- PAGE 1: 三鷹市の送迎課題とKidsRideの理念・共生モデル -->
<div class="page-container">
  <div>
    <div class="top-banner">
      <div>
        <span style="font-size:8pt; opacity:0.9; letter-spacing:0.05em;">三鷹市地域協働・子育て支援パートナーシップ説明資料 【1/2】</span>
        <div style="font-size:13pt; font-weight:800; margin-top:2px;">子育て送迎の壁を解消する「地域近隣互助モデル」のご案内</div>
      </div>
      <div style="text-align:right; font-size:8pt;">
        一般社団法人KidsRide<br>https://www.kidsride.jp/
      </div>
    </div>

    <!-- 課題提起 -->
    <div class="section-card">
      <div class="section-header">
        <span>1. 三鷹市の子育て世帯が直面する「送迎の壁」と孤立化の実態</span>
      </div>
      <div class="grid-3">
        <div class="sub-box" style="border-left:4px solid #ef4444; background:#fef2f2;">
          <strong style="color:#991b1b; display:block; margin-bottom:3px;">① 第一希望園の断念・遠距離通園</strong>
          三鷹市内でも希望園に入園できず、自宅から離れた保育園に通う世帯が多数存在。雨天時や体調不良時の送迎が過酷を極め、就労継続の危機に直結しています。
        </div>
        <div class="sub-box" style="border-left:4px solid #f59e0b; background:#fffbeb;">
          <strong style="color:#92400e; display:block; margin-bottom:3px;">② 学童・のびのび広場のお迎えの壁</strong>
          小学生になっても、低学年の夕方帰宅や「のびのびひろば（トワイライトステイ〜22時）」利用時の夜間送迎に親が対応できず、民間託児サービスに頼らざるを得ない現状があります。
        </div>
        <div class="sub-box" style="border-left:4px solid #8b5cf6; background:#f5f3ff;">
          <strong style="color:#6d28d9; display:block; margin-bottom:3px;">③ 近隣コミュニティの希薄化と孤立</strong>
          「近所に知り合いや頼れる実家がいない」「少し預かってほしいと言えない」という心理的孤立から、夕方の育児がワンオペパニックに陥る構造的課題があります。
        </div>
      </div>
    </div>

    <!-- 既存制度との補完関係 -->
    <div class="section-card">
      <div class="section-header">
        <span>2. 公的ファミリーサポートセンター等とKidsRideの共存補完関係</span>
      </div>
      <div style="font-size:8.3pt; margin-bottom:6px; color:#475569;">
        KidsRideは既存の福祉制度やファミサポを代替・競合するものではなく、<strong>「日常の隙間（急な残業、ついで送迎）」を埋める相互補完の枠組み</strong>です。
      </div>
      <table style="width:100%; border-collapse:collapse; font-size:8pt;">
        <thead>
          <tr style="background:#f1f5f9; color:#334155;">
            <th style="border:1px solid #cbd5e1; padding:6px; width:22%;">比較項目</th>
            <th style="border:1px solid #cbd5e1; padding:6px; width:39%;">公的ファミリーサポートセンター等</th>
            <th style="border:1px solid #cbd5e1; padding:6px; width:39%; background:#e0f2fe; color:#0369a1;">KidsRide（近隣保護者間互助モデル）</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="border:1px solid #cbd5e1; padding:6px; font-weight:700;">マッチング方式</td>
            <td style="border:1px solid #cbd5e1; padding:6px;">コーディネーターを介した事前対面面談・調整が必要</td>
            <td style="border:1px solid #cbd5e1; padding:6px; background:#f0f9ff; font-weight:700; color:#0284c7;">同じ園・近所の保護者同士による「通勤・送迎のついで」マッチング</td>
          </tr>
          <tr>
            <td style="border:1px solid #cbd5e1; padding:6px; font-weight:700;">急な突発ニーズ</td>
            <td style="border:1px solid #cbd5e1; padding:6px;">数日前からの予約が基本（当日の急な残業には対応困難）</td>
            <td style="border:1px solid #cbd5e1; padding:6px; background:#f0f9ff; font-weight:700; color:#0284c7;">アプリ上でリアルタイムに「今日お迎え行ける人」を募集・承諾</td>
          </tr>
          <tr>
            <td style="border:1px solid #cbd5e1; padding:6px; font-weight:700;">担い手（サポーター）</td>
            <td style="border:1px solid #cbd5e1; padding:6px;">登録協力会員（シニア層が中心、担い手不足が慢性化）</td>
            <td style="border:1px solid #cbd5e1; padding:6px; background:#f0f9ff; font-weight:700; color:#0284c7;">「自分の子どもの送迎に行くついで」の現役保護者同士＋地域協力者</td>
          </tr>
          <tr>
            <td style="border:1px solid #cbd5e1; padding:6px; font-weight:700;">謝礼・費用体系</td>
            <td style="border:1px solid #cbd5e1; padding:6px;">時間単位の有償謝礼（1時間800〜1,000円程度）</td>
            <td style="border:1px solid #cbd5e1; padding:6px; background:#f0f9ff; font-weight:700; color:#0284c7;">ガソリン実費等の精算のみ（1回数百円・運送対価ゼロの完全互助）</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 今回のアンケート調査の目的 -->
    <div class="section-card">
      <div class="section-header">
        <span>3. 今回の実態調査アンケートの狙いとデータ活用の展望</span>
      </div>
      <div class="grid-2">
        <div class="sub-box">
          <strong style="color:#0369a1; display:block; margin-bottom:3px;">◆ 客観的データの可視化</strong>
          「第一希望園を諦めた割合」「送迎で仕事を休んだ頻度」「のびのび広場の送迎があれば使いたいか」等、三鷹市独自の実態数値を集計し、真に必要な子育てインフラを導き出します。
        </div>
        <div class="sub-box">
          <strong style="color:#0369a1; display:block; margin-bottom:3px;">◆ 地域支援機関との協働モデル構築</strong>
          集計結果は協力機関にも還元。行政やNPO、社協が推進する地域見守り活動や孤立防止施策と連携し、三鷹市発の先駆的な互助インフラモデルへ昇華させます。
        </div>
      </div>
    </div>
  </div>

  <div style="text-align:right; font-size:7.5pt; color:#64748b; border-top:1px solid #e2e8f0; padding-top:4px;">
    KidsRide 地域協働説明資料 | 1 / 2 ページ
  </div>
</div>

<!-- PAGE 2: 安全対策・適法性・地域協働アプローチ -->
<div class="page-container">
  <div>
    <div class="top-banner">
      <div>
        <span style="font-size:8pt; opacity:0.9; letter-spacing:0.05em;">三鷹市地域協働・子育て支援パートナーシップ説明資料 【2/2】</span>
        <div style="font-size:13pt; font-weight:800; margin-top:2px;">最高峰の安全補償体制・適法性と今後の協働ステップ</div>
      </div>
      <div style="text-align:right; font-size:8pt;">
        一般社団法人KidsRide<br>安全対策推進室
      </div>
    </div>

    <!-- 安全対策の4重シールド -->
    <div class="section-card">
      <div class="section-header">
        <span>4. 子どもの命と安心を守る「4重の安全管理体制」</span>
      </div>
      <div class="grid-2">
        <div class="sub-box" style="border-left:4px solid #10b981; background:#ecfdf5;">
          <strong style="color:#065f46; display:block; margin-bottom:2px;">① あいおいニッセイ同和損保 包括保険（最高2億円）</strong>
          自動車送迎のみならず、自転車・徒歩送迎時も「対人・対物賠償責任保険 最高2億円（免責0円）」を完備。サポーター本人の傷害保険も付帯し、個人間での賠償争いを完全に防止します。
        </div>
        <div class="sub-box" style="border-left:4px solid #0284c7; background:#f0f9ff;">
          <strong style="color:#0369a1; display:block; margin-bottom:2px;">② リアルタイムGPS ＆ 引渡ワンタイムコード</strong>
          送迎中は保護者のスマホ画面上に子どもの現在位置がリアルタイム表示。園や施設での引き渡し時は「顔写真付き身元証」と「1分間有効のワンタイム暗証コード」で誤認・連れ去りを防止します。
        </div>
        <div class="sub-box" style="border-left:4px solid #f59e0b; background:#fffbeb;">
          <strong style="color:#92400e; display:block; margin-bottom:2px;">③ 国土交通省（東京運輸支局）確認済みの適法性</strong>
          送迎の対価（運送報酬）は一切発生せず、ガソリン代等の実費のみを按分精算する仕組み。道路運送法上の「白タク行為」に該当しない無償互助モデルとしての適法性を確認済みです。
        </div>
        <div class="sub-box" style="border-left:4px solid #8b5cf6; background:#f5f3ff;">
          <strong style="color:#6d28d9; display:block; margin-bottom:2px;">④ サポーターの厳格な事前審査・安全講習</strong>
          運転免許証・本人確認書類の審査に加え、無事故無違反歴の確認、車両点検、チャイルドシート装着の義務化、および子どもの救急救護に関する安全マニュアルを整備しています。
        </div>
      </div>
    </div>

    <!-- 貴機関へアドバイスをいただきたい論点 -->
    <div class="section-card">
      <div class="section-header">
        <span>5. 今後、地域支援機関・NPO・社協の皆様からご助言をいただきたい事項</span>
      </div>
      <div class="sub-box" style="background:#fafafa; border:1.5px dashed #0284c7; padding:9px 12px; margin-bottom:6px;">
        <div style="font-weight:700; color:#0369a1; margin-bottom:4px; font-size:8.8pt;">★ 私たちが専門家・先駆者である皆様に教えていただきたいこと：</div>
        <ul style="margin:0; padding-left:18px; line-height:1.6; font-size:8.2pt; color:#334155;">
          <li><strong>地域のリアルな現場ニーズ：</strong> 日頃の相談窓口やサロン等で耳にする「親御さんの移動・送迎の本当の困りごと」はどこにあるか？</li>
          <li><strong>担い手・サポーターの確保：</strong> 親同士だけでなく、地域のアクティブシニアや子育て卒業世代を安全に巻き込むための工夫や研修ノウハウ。</li>
          <li><strong>安全管理・信頼形成のポイント：</strong> 不安感を払拭し、地域社会から信頼される仕組みにするために不足している視点や強化すべき点。</li>
          <li><strong>行政・他団体との協働推進：</strong> 三鷹市子ども政策部等への提案や、市民協働事業提案制度、市民活動助成金の活用可能性。</li>
        </ul>
      </div>
    </div>

    <!-- ロードマップ -->
    <div class="section-card">
      <div class="section-header">
        <span>6. 地域協働に向けた推進ステップ</span>
      </div>
      <div style="display:flex; justify-content:space-between; gap:6px; font-size:7.8pt; text-align:center;">
        <div style="flex:1; background:#f1f5f9; padding:6px 4px; border-radius:6px; border:1px solid #cbd5e1;">
          <strong style="color:#0f172a; display:block;">STEP 1: 実態把握（現在）</strong>
          市内保護者アンケート調査<br>地域支援機関へのご相談・助言受取
        </div>
        <div style="display:flex; align-items:center; color:#cbd5e1; font-weight:bold;">▶</div>
        <div style="flex:1; background:#e0f2fe; padding:6px 4px; border-radius:6px; border:1px solid #7dd3fc;">
          <strong style="color:#0369a1; display:block;">STEP 2: モデル精緻化</strong>
          いただいた助言を反映<br>三鷹市特化型安全ガイド策定
        </div>
        <div style="display:flex; align-items:center; color:#cbd5e1; font-weight:bold;">▶</div>
        <div style="flex:1; background:#dcfce7; padding:6px 4px; border-radius:6px; border:1px solid #86efac;">
          <strong style="color:#166534; display:block;">STEP 3: 限定実証実験</strong>
          市内特定エリア・園にて<br>モニター体験（無料運用検証）
        </div>
        <div style="display:flex; align-items:center; color:#cbd5e1; font-weight:bold;">▶</div>
        <div style="flex:1; background:#fef3c7; padding:6px 4px; border-radius:6px; border:1px solid #fde68a;">
          <strong style="color:#92400e; display:block;">STEP 4: 本格展開・地域連携</strong>
          社協・NPO・行政と協働し<br>持続可能な市民互助インフラへ
        </div>
      </div>
    </div>
  </div>

  <div style="text-align:right; font-size:7.5pt; color:#64748b; border-top:1px solid #e2e8f0; padding-top:4px;">
    KidsRide 地域協働説明資料 | 2 / 2 ページ
  </div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 03: 【市民向けアンケート告知チラシ兼ポスター】（A4・ジャスト1P・カラー）
# ==============================================================================
html_03_citizen_flyer = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>三鷹市 子育て世帯の通園・送迎アンケート</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    margin: 0;
    padding: 0;
    background: white;
  }}
  .flyer-border {{
    border: 3px solid #0284c7;
    border-radius: 12px;
    padding: 12px 16px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .header {{
    text-align: center;
    border-bottom: 2px dashed #bae6fd;
    padding-bottom: 8px;
    margin-bottom: 8px;
  }}
  .badge-top {{
    display: inline-block;
    background: #0284c7;
    color: white;
    font-weight: 700;
    font-size: 9.5pt;
    padding: 3px 14px;
    border-radius: 20px;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
  }}
  .main-title {{
    font-size: 17pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.35;
    margin: 4px 0;
  }}
  .sub-title {{
    font-size: 10pt;
    color: #0369a1;
    font-weight: 700;
  }}
  .trouble-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 10px;
  }}
  .trouble-card {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 10px;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 8.5pt;
    line-height: 1.4;
  }}
  .trouble-icon {{
    background: #fee2e2;
    color: #ef4444;
    font-size: 11pt;
    font-weight: bold;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}
  .center-action {{
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border: 2px solid #0284c7;
    border-radius: 10px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 10px;
  }}
  .qr-box {{
    text-align: center;
    background: white;
    padding: 8px;
    border-radius: 8px;
    border: 1px solid #bae6fd;
    flex-shrink: 0;
  }}
  .qr-box img {{
    width: 100px;
    height: 100px;
    display: block;
  }}
  .action-text {{
    flex: 1;
  }}
  .features-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
    text-align: center;
    margin-bottom: 8px;
  }}
  .feat-box {{
    background: #f1f5f9;
    border-radius: 6px;
    padding: 6px;
    font-size: 7.8pt;
  }}
  .feat-box strong {{
    display: block;
    color: #0369a1;
    font-size: 8.5pt;
    margin-bottom: 2px;
  }}
  .footer-note {{
    border-top: 1px solid #e2e8f0;
    padding-top: 6px;
    font-size: 7.2pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
</style>
</head>
<body>

<div class="flyer-border">
  <div>
    <div class="header">
      <div class="badge-top">三鷹市 子育て世帯実態調査</div>
      <div class="main-title">子どもの「通園・送迎」で<br>困った経験はありませんか？</div>
      <div class="sub-title">毎日の登降園や放課後の移動に関する、パパ・ママのリアルな声をお聞かせください</div>
    </div>

    <!-- よくあるお悩みカード -->
    <div class="trouble-grid">
      <div class="trouble-card">
        <div class="trouble-icon">！</div>
        <div>
          <strong style="color:#0f172a; display:block;">雨や強風の日の送迎が大変…</strong>
          自転車送迎がつらい、下の子を連れての悪天候の移動で毎日ぐったりしてしまう
        </div>
      </div>
      <div class="trouble-card">
        <div class="trouble-icon">！</div>
        <div>
          <strong style="color:#0f172a; display:block;">急な仕事の残業でお迎えが…</strong>
          電車遅延や突発残業で園のお迎え時間に間に合わない、頼れる実家も近くにない
        </div>
      </div>
      <div class="trouble-card">
        <div class="trouble-icon">！</div>
        <div>
          <strong style="color:#0f172a; display:block;">通えなくて第一希望園を諦めた…</strong>
          本当は通わせたかった園があったのに、送迎距離の壁で別の園を選ばざるを得なかった
        </div>
      </div>
      <div class="trouble-card">
        <div class="trouble-icon">！</div>
        <div>
          <strong style="color:#0f172a; display:block;">のびのび広場のお迎えどうする？</strong>
          学童やトワイライトステイ（夜間預かり）を使いたいが、夕方以降の送迎がネックに
        </div>
      </div>
    </div>

    <!-- QRコード回答エリア -->
    <div class="center-action">
      <div class="action-text">
        <div style="font-size:11pt; font-weight:800; color:#0369a1; margin-bottom:4px;">
          スマホで簡単回答！所要時間は約3分です
        </div>
        <div style="font-size:8.3pt; color:#334155; line-height:1.5;">
          右のQRコードをカメラで読み取ってご回答ください。<br>
          皆様からいただいたご意見は、三鷹市内で安心・安全に助け合える「新しい子育て送迎サポート」の実現に大切に役立たせていただきます。
        </div>
        <div style="margin-top:6px; font-size:7.5pt; color:#0284c7; font-weight:700;">
          URL: https://www.kidsride.jp/#survey
        </div>
      </div>
      <div class="qr-box">
        <img src="data:image/png;base64,{qr_b64}" alt="アンケートQRコード">
        <span style="font-size:7pt; color:#64748b; display:block; margin-top:3px; font-weight:700;">カメラで読取</span>
      </div>
    </div>

    <!-- 3つの安心ポイント -->
    <div class="features-grid">
      <div class="feat-box">
        <strong>完全無記名方式</strong>
        氏名・電話番号・住所不要<br>個人情報は一切取得しません
      </div>
      <div class="feat-box">
        <strong>選択式でサクサク</strong>
        全12問・タップするだけ<br>すきま時間にすぐ答えられます
      </div>
      <div class="feat-box">
        <strong>民間保護者主導</strong>
        営利勧誘は一切ありません<br>三鷹市在住の保護者による調査
      </div>
    </div>

    <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:6px; padding:6px 10px; font-size:7.8pt; color:#14532d; text-align:center;">
      <strong>【ご協力】</strong> 本アンケートは、三鷹市内の子育て支援団体・地域協働機関等と連携し、地域全体の課題解決を目指して実施されています。
    </div>
  </div>

  <div class="footer-note">
    <div>
      <strong>実施主体：一般社団法人KidsRide</strong>（三鷹市） 代表理事 七夕 光明<br>
      お問い合わせ：info@kidsride.jp　公式サイト：https://www.kidsride.jp/
    </div>
    <div style="text-align:right;">
      ※本アンケート結果は統計処理され、地域のより良い子育て環境設計のために活用されます。
    </div>
  </div>
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 07: 【地域協働・サービス推進アドバイス_ヒアリング相談シート】（A4・ジャスト1P）
# ==============================================================================
html_07_hearing_sheet = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>地域協働・サービス推進アドバイス ヒアリング相談シート</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 12mm 14mm 12mm 14mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    line-height: 1.45;
    font-size: 8.8pt;
    margin: 0;
    padding: 0;
  }}
  .header-box {{
    background: #0284c7;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .topic-card {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 9px 12px;
    margin-bottom: 9px;
  }}
  .topic-title {{
    font-weight: 800;
    color: #0369a1;
    font-size: 9.5pt;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .memo-space {{
    background: white;
    border: 1px dashed #94a3b8;
    border-radius: 4px;
    height: 48px;
    margin-top: 5px;
    padding: 4px;
    font-size: 7.5pt;
    color: #94a3b8;
  }}
  ul.question-list {{
    margin: 0;
    padding-left: 18px;
    line-height: 1.55;
    font-size: 8.3pt;
    color: #334155;
  }}
</style>
</head>
<body>

<div class="header-box">
  <div>
    <div style="font-size:7.5pt; opacity:0.9;">三鷹市市民協働センター・子育てコンビニ・三鷹市社協 面談用</div>
    <div style="font-size:12pt; font-weight:800;">地域協働・子育て送迎互助 推進アドバイス相談シート</div>
  </div>
  <div style="text-align:right; font-size:7.5pt;">
    一般社団法人KidsRide<br>代表理事 七夕 光明
  </div>
</div>

<div style="font-size:8.3pt; color:#475569; margin-bottom:10px; line-height:1.5;">
  三鷹市において地域の現場を支えてこられた皆様の専門的知見や現場感覚から、率直なご意見・アドバイスを賜りたく存じます。（面談時のメモや論点整理としてご活用いただけます）
</div>

<!-- 論点1 -->
<div class="topic-card">
  <div class="topic-title">論点 1. 三鷹市内における「子育て世帯の送迎・移動課題」の現場実態</div>
  <ul class="question-list">
    <li>日頃の相談窓口や子育てサロン等で、保護者から「送迎」「通園」「学童のお迎え」に関してどのような生の声や苦労話が届いていますでしょうか？</li>
    <li>特に負担感が強いエリア（交通不便地域、坂の多いエリア）や、年齢層（未就学児、低学年、のびのび広場利用者等）についてどう感じられますか？</li>
  </ul>
  <div class="memo-space">【ご意見・メモ欄】</div>
</div>

<!-- 論点2 -->
<div class="topic-card">
  <div class="topic-title">論点 2. 既存の公的福祉制度（ファミサポ等）との役割分担と共存</div>
  <ul class="question-list">
    <li>既存のファミリーサポートセンターや一時預かり事業において、「カバーしきれていない隙間のニーズ（急な残業、雨天時のみ等）」はございますか？</li>
    <li>KidsRideのような「近隣保護者同士のついで送迎」が、公的制度と競合せず良い形で補完し合うために配慮すべき点は何でしょうか？</li>
  </ul>
  <div class="memo-space">【ご意見・メモ欄】</div>
</div>

<!-- 論点3 -->
<div class="topic-card">
  <div class="topic-title">論点 3. 安心・安全管理と「地域の信頼獲得」に向けた留意点</div>
  <ul class="question-list">
    <li>あいおい損保（最高2億円）やGPS追跡、ワンタイムコード等を導入しておりますが、保護者や地域住民が「安心して利用する」ためにさらに必要な工夫は何でしょうか？</li>
    <li>事故防止やトラブル防止、および保護者間のマナー啓発に関して、地域支援の先駆者としてのアドバイスをいただけますでしょうか。</li>
  </ul>
  <div class="memo-space">【ご意見・メモ欄】</div>
</div>

<!-- 論点4 -->
<div class="topic-card">
  <div class="topic-title">論点 4. 行政連携（子ども政策部等）や市民活動助成金等の活用可能性</div>
  <ul class="question-list">
    <li>三鷹市役所（子ども政策部・子ども育成課等）への効果的なアプローチや、市民協働事業提案制度、市民活動助成金の活用に向けたアドバイスはございますか？</li>
    <li>今後、限定エリアでの「無料実証実験」を実施するにあたり、アドバイザーや協力団体として連携させていただく可能性についてご意見をいただけますでしょうか。</li>
  </ul>
  <div class="memo-space">【ご意見・メモ欄】</div>
</div>

<div style="text-align:right; font-size:7.5pt; color:#64748b; margin-top:6px;">
  一般社団法人KidsRide（info@kidsride.jp） 本日の貴重なお時間を心より感謝申し上げます。
</div>

</body>
</html>
"""

# ==============================================================================
# PDF 04: 【名刺サイズQRカード_10面シート】（既存の高品質HTMLを流用）
# ==============================================================================
# generate_all_kindergarten_kit.py から名刺シートHTMLをそのまま流用
with open(os.path.join(workspace_dir, "generate_all_kindergarten_kit.py"), "r", encoding="utf-8") as f:
    k_script = f.read()

import re
m_cards = re.search(r'html_04_cards_sheet = f"""(.*?)"""\n\n# ===', k_script, re.DOTALL)
html_04_cards_sheet = m_cards.group(1) if m_cards else ""

m_sample = re.search(r'html_05_survey_sample = f"""(.*?)"""\n\n# ===', k_script, re.DOTALL)
html_05_survey_sample = m_sample.group(1) if m_sample else ""


# ==============================================================================
# PDF出力エンジン（Chrome Headless）
# ==============================================================================
os.makedirs("/tmp/chrome-pdf-profile", exist_ok=True)
chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

files_to_generate = [
    ("01_アンケート調査協力・情報提供依頼状（地域支援機関・NPO・社協向け）", html_01_request_letter),
    ("02_事業概要・地域課題・安全対策説明シート（地域協働版・A4見開き2P）", html_02_presentation_sheet),
    ("03_市民向けアンケート告知チラシ兼ポスター（A4カラー）", html_03_citizen_flyer),
    ("04_持ち帰り用_名刺サイズQRカード_10面シート", html_04_cards_sheet),
    ("05_保護者アンケート設問見本票（A4_2P）", html_05_survey_sample),
    ("07_地域協働・サービス推進アドバイス_ヒアリング相談シート", html_07_hearing_sheet)
]

print("=== 地域協働・NPO・社協向け PDF生成開始 ===")
for filename, html_content in files_to_generate:
    if not html_content:
        print(f"スキップ（HTML空）: {filename}")
        continue
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

print("=== すべての地域協働・NPO・社協向けPDF生成処理が完了しました ===")
