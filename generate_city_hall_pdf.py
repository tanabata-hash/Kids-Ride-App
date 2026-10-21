import os
import subprocess

OUTPUT_DIR = os.path.expanduser("~/Desktop/KidsRide/市役所説明資料")
os.makedirs(OUTPUT_DIR, exist_ok=True)

html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>三鷹市 事前相談・事業概要説明書 - 一般社団法人KidsRide</title>
<style>
  @page {
    size: A4 portrait;
    margin: 14mm 14mm 14mm 14mm;
    @bottom-right {
      content: counter(page);
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #1e293b;
    line-height: 1.52;
    font-size: 9.2pt;
    margin: 0;
    padding: 0;
  }

  /* 印刷用改ページ制御 */
  .page-break {
    page-break-before: always;
  }

  /* 表紙 */
  .cover {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-top: 6px solid #1e3a8a;
    padding-top: 30px;
    box-sizing: border-box;
  }

  .cover-category {
    font-size: 12pt;
    font-weight: 700;
    color: #0284c7;
    margin-bottom: 8px;
  }

  .cover-title {
    font-size: 22pt;
    font-weight: 800;
    color: #1e3a8a;
    line-height: 1.35;
    margin: 0 0 14px 0;
  }

  .cover-subtitle {
    font-size: 11.5pt;
    color: #334155;
    margin-bottom: 20px;
    font-weight: 600;
    border-left: 4px solid #ea580c;
    padding-left: 10px;
  }

  .cover-meta {
    margin-top: auto;
    padding: 16px 20px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 9.5pt;
    line-height: 1.7;
  }

  .cover-meta strong {
    color: #0f172a;
  }

  /* 本文セクション */
  h2 {
    font-size: 11.5pt;
    color: #1e3a8a;
    border-left: 4px solid #1e3a8a;
    padding-left: 8px;
    margin-top: 14px;
    margin-bottom: 6px;
    background: #f1f5f9;
    padding-top: 4px;
    padding-bottom: 4px;
  }

  h3 {
    font-size: 10pt;
    color: #0f172a;
    margin-top: 10px;
    margin-bottom: 4px;
    font-weight: 700;
  }

  p {
    margin: 0 0 6px 0;
    text-align: justify;
  }

  /* 強調ボックス */
  .highlight-box {
    background: #f0fdf4;
    border: 1.5px solid #86efac;
    border-radius: 6px;
    padding: 7px 12px;
    margin: 6px 0;
    font-size: 8.6pt;
  }

  .highlight-box strong {
    color: #15803d;
  }

  .accent-box {
    background: #fff7ed;
    border: 1.5px solid #fed7aa;
    border-radius: 6px;
    padding: 7px 12px;
    margin: 6px 0;
    font-size: 8.6pt;
  }

  .accent-box strong {
    color: #c2410c;
  }

  /* テーブル */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0 10px 0;
    font-size: 8.3pt;
  }

  th, td {
    border: 1px solid #cbd5e1;
    padding: 5px 8px;
    vertical-align: top;
  }

  th {
    background: #1e3a8a;
    color: white;
    font-weight: 700;
    text-align: left;
  }

  tr:nth-child(even) td {
    background: #f8fafc;
  }

  ul {
    margin: 3px 0 6px 18px;
    padding: 0;
  }

  li {
    margin-bottom: 2px;
  }

  .badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 8pt;
    font-weight: 700;
  }
  .cover-summary {
    background: #ffffff;
    border: 1.5px solid #0284c7;
    border-radius: 8px;
    padding: 12px 14px;
    margin-top: 14px;
    margin-bottom: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
  }
  .cover-summary-title {
    font-size: 9.5pt;
    font-weight: 800;
    color: #0369a1;
    display: flex;
    align-items: center;
    gap: 6px;
    border-bottom: 1px solid #e0f2fe;
    padding-bottom: 4px;
    margin-bottom: 8px;
  }
  .cover-summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 12px;
    font-size: 8pt;
    line-height: 1.5;
  }
  .cover-summary-item strong {
    color: #0f172a;
    display: inline-block;
  }
</style>
</head>
<body>

<!-- 表紙 -->
<div class="cover">
  <div class="cover-category">三鷹市 子ども政策部 子ども育成課 事前相談資料（公式面談版）</div>
  <h1 class="cover-title" style="font-size: 19pt; margin-bottom: 10px;">三鷹市における保育園・幼稚園・学童<br>子ども送迎相互支援プラットフォーム<br>（KidsRide）事業概要説明書</h1>
  <div class="cover-subtitle" style="font-size: 10pt; margin-bottom: 12px; padding-left: 8px;">
    同一園の保護者互助 × 東京運輸支局確認済の適法設計 × 手厚い包括保険制度（最高2億円）
  </div>

  <!-- 庁内回覧用 エグゼクティブ・サマリー（1分でわかる要約シート） -->
  <div class="cover-summary">
    <div class="cover-summary-title">
      <span>📋 【エグゼクティブ・サマリー（庁内回覧・共有用要約）】</span>
    </div>
    <div class="cover-summary-grid">
      <div class="cover-summary-item">
        <strong>① 事業趣旨（地域共助）：</strong><br>
        同一の保育園・幼稚園・学童に通う身元確認済の保護者同士が、送り迎えをついでに助け合う非営利の地域互助インフラ。
      </div>
      <div class="cover-summary-item">
        <strong>② 園選び・4月入所支援：</strong><br>
        「自宅から遠く送迎が困難」という理由で希望園を諦める保護者の課題を解消。広域通園を可能にし就労継続を支援。
      </div>
      <div class="cover-summary-item">
        <strong>③ 適法性（道路運送法）：</strong><br>
        国土交通省（東京運輸支局）へ正式確認済。利益を完全排除し、実費精算（11円/km）のみの「許可・登録不要（合法）」設計。
      </div>
      <div class="cover-summary-item">
        <strong>④ 万全の安全管理・補償：</strong><br>
        損保会社と包括保険契約を締結（最高2億円賠償＋傷害補償）。全走行GPSリアルタイム追跡＆アルコール検知義務化。
      </div>
      <div class="cover-summary-item">
        <strong>⑤ 行政負担・予算ゼロ：</strong><br>
        市への予算要求・公的負担は一切なし（民間非営利完結）。既存のファミリー・サポート・センターを補完する関係性。
      </div>
      <div class="cover-summary-item">
        <strong>⑥ 本日のご相談・次回予定：</strong><br>
        実証実験への助言、11月中旬のアンケート調査結果持参・次回報告のお願い、将来的な広報連携に向けた事前相談。
      </div>
    </div>
  </div>

  <div class="cover-meta" style="padding: 11px 16px; font-size: 8.5pt; line-height: 1.6;">
    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
      <span style="white-space:nowrap;"><strong>相談日時：</strong> 2026年10月20日（火）10:00〜10:30</span>
      <span style="white-space:nowrap;"><strong>提出先：</strong> 三鷹市役所 子ども政策部 子ども育成課 御中（ご担当：波照間 様）</span>
    </div>
    <div style="border-top:1px dashed #cbd5e1; padding-top:6px;">
      <strong>提出団体：</strong> 一般社団法人KidsRide（キッズライド）<br>
      <strong>代表者：</strong> 代表理事 七夕 光明（三鷹市在住・三鷹のぞみ幼稚園在園児の父）<br>
      <strong>所在地：</strong> 〒181-0013 東京都三鷹市下連雀3-36-1-1701  /  <strong>Webサイト：</strong> https://www.kidsride.jp/<br>
      <strong>連絡先：</strong> 070-2251-1896  /  info@kids-ride.jp
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- 本文ページ 1 -->
<div class="header-rule">
  <span>三鷹市役所 子ども育成課（波照間様）事前相談資料：一般社団法人KidsRide</span>
  <span>1. 事業趣旨・サービス概要・法令適合性</span>
</div>

<h2>1. 事業の趣旨と背景（なぜ三鷹市で取り組むのか）</h2>
<p>
  三鷹市をはじめとする都市部において共働き世帯やワンオペ育児家庭が増加する中、毎日の保育園・幼稚園・学童への送迎は保護者にとって最大の生活課題の一つとなっています。特に翌年4月の一斉入所選考（保活）を控える現在、多くの保護者が「希望する園があるが、毎日の送迎が困難であるため選択肢から外さざるを得ない」という現実に直面しています。
</p>
<ul>
  <li><strong>日常の突発的ピンチ：</strong>急な残業、突発的な会議、きょうだいの急な発熱・通院、悪天候（豪雨・猛暑）時、既存の公的支援では当日の急な依頼に対応しきれません。</li>
  <li><strong>送迎不安による園選択の断念：</strong>「自宅から遠い」「送迎時間の両立が不安」という理由で、保護者が本来希望する教育方針の幼稚園や保育園を諦めざるを得ないケースが散見されます。</li>
  <li><strong>保育・教育現場の負担：</strong>保護者のお迎え遅れは、保育士等の延長保育対応や超過勤務、代理引き渡し時のセキュリティ懸念など園現場にも多大な負荷を与えています。</li>
</ul>
<p>
  KidsRideは、<strong>「同じ園に通う身元の確かな保護者同士が、日々の送迎をついでに助け合う地域互助プラットフォーム」</strong>です。見知らぬ他人に預ける不安を排除し、顔の見える関係性の中で安心な送迎インフラを構築します。
</p>

<h2>2. サービスモデルと安心・非営利の設計</h2>
<p>
  当事業は、道路運送法および児童安全基準に厳格に適合した完全なクローズド・非営利設計としています。
</p>
<ul>
  <li><strong>同一園・同一施設の保護者限定：</strong>送迎の依頼者も受託者（サポーター）も、同じ園に子どもを通わせる保護者に厳格限定。身元確認（免許証等）に加え、在園確認（在園証明書・連絡帳・保護者証）を必須としています。</li>
  <li><strong>ハイブリッド送迎手段：</strong>徒歩送迎（手つなぎ引率）、自転車送迎（幼児同乗器・ヘルメット着用）、自家用車送迎（R129適合チャイルドシート常設、点検・アルコール検知0.00mg/L義務化）に対応。</li>
  <li><strong>非営利・実費精算の徹底：</strong>車送迎はガソリン代実費のみ（走行距離×11円/km、端数切捨て）。自転車・徒歩送迎は換金できないポイント（200pt）のみ。送迎対価で利益を得る構造を完全に排除しています。</li>
</ul>

<h2>3. 法令適合性とコンプライアンス（東京運輸支局の書面確認済）</h2>
<div class="highlight-box">
  <strong>【国土交通省 関東運輸局 東京運輸支局からの正式書面回答を受領済み】</strong><br>
  当法人は事前に東京運輸支局輸送統括担当と協議を行い、現行モデルが道路運送法第78条（自家用有償運送の禁止）の適用除外であり、<strong>「許可・登録は一切不要（合法）」</strong>である旨の書面回答を得ております。
</div>

<table>
  <thead>
    <tr>
      <th style="width:30%;">確認事項</th>
      <th style="width:20%;">支局の回答</th>
      <th style="width:50%;">判断理由・適合根拠</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>① 自家用車での実費受領</strong></td>
      <td><span class="badge badge-success">登録不要</span></td>
      <td>ガソリン代実費のみの授受は運送の対価にあたらず、法上の無償運送の範囲内であるため。</td>
    </tr>
    <tr>
      <td><strong>② 自転車・徒歩送迎のポイント</strong></td>
      <td><span class="badge badge-success">登録不要</span></td>
      <td>換金不可のポイントは対価性がなく、かつ人力による移動のため法対象外であるため。</td>
    </tr>
    <tr>
      <td><strong>③ プラットフォーム利用料別建て</strong></td>
      <td><span class="badge badge-success">登録不要</span></td>
      <td>月額会費はシステム役務の対価であり、送迎運送の対価ではないため。</td>
    </tr>
    <tr>
      <td><strong>④ 決済代行業者を通じた自動精算</strong></td>
      <td><span class="badge badge-success">登録不要</span></td>
      <td>代行精算を行うのみであり、KidsRide自身が運送事業を経営するものではないため。</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- 本文ページ 2 -->
<div class="header-rule">
  <span>三鷹市役所 子ども育成課（波照間様）事前相談資料：一般社団法人KidsRide</span>
  <span>2. ファミサポ共存・安全管理体制・包括損害保険</span>
</div>

<h2>4. 三鷹市ファミリー・サポート・センター事業との共存・相互補完</h2>
<p>
  公的なセーフティネットである三鷹市ファミサポ事業と競合するものではなく、<strong>ファミサポの手が届きにくい隙間を埋める「相互補完関係」</strong>として位置づけています。
</p>

<table>
  <thead>
    <tr>
      <th style="width:22%;">比較項目</th>
      <th style="width:39%;">三鷹市ファミリー・サポート・センター</th>
      <th style="width:39%;">KidsRide（当事業）</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>支援の性質</strong></td>
      <td>計画的・定期的な支援（事前予約型）</td>
      <td><strong>突発的・日常的なラストワンマイルの互助</strong></td>
    </tr>
    <tr>
      <td><strong>支援者と利用者の関係</strong></td>
      <td>地域の協力会員（一般市民ボランティア）</td>
      <td><strong>同じ園に通う顔見知りの保護者同士</strong></td>
    </tr>
    <tr>
      <td><strong>マッチング方式</strong></td>
      <td>アドバイザーを介した事前調整・顔合わせ</td>
      <td><strong>スマホアプリによる即時・柔軟なマッチング</strong></td>
    </tr>
    <tr>
      <td><strong>主な対応シーン</strong></td>
      <td>毎週決まった習い事、事前の予定支援</td>
      <td><strong>当日の急な残業、下の子の発熱、悪天候等</strong></td>
    </tr>
    <tr>
      <td><strong>対価体系</strong></td>
      <td>1時間あたり約800〜1,000円の謝礼金</td>
      <td><strong>ガソリン実費（車）またはポイント（徒歩・自転車）</strong></td>
    </tr>
  </tbody>
</table>

<h2>5. 安全管理体制と包括損害保険（あいおいニッセイ同和損保）</h2>
<p>
  子どもの安全確保を最優先とし、リアルタイムGPS位置追跡、顔写真付き引き渡し認証、出庫前点検・アルコール検知（0.00mg/L）を義務化。さらに、団体として以下の包括保険を締結・適用します。
</p>

<table>
  <thead>
    <tr>
      <th style="width:22%;">送迎手段</th>
      <th style="width:34%;">適用保険商品（あいおい損保）</th>
      <th style="width:44%;">補償限度額・内容</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>自家用車送迎</strong></td>
      <td>移動支援サービス専用自動車包括特約</td>
      <td><strong>対人無制限 / 対物無制限 / 人身傷害3,000万円</strong><br>※サポーターの個人任意保険を優先させず団体保険を適用</td>
    </tr>
    <tr>
      <td><strong>自転車・徒歩送迎</strong></td>
      <td>NPO活動総合保険（賠償特約＋傷害特約）</td>
      <td><strong>第三者賠償責任：最高 2億円</strong>（免責金額 0円）<br>見舞金50万 / 預かり品損壊50万 / 対応費用500万<br><strong>サポーター傷害補償：入院2,000円/日、通院1,000円/日</strong></td>
    </tr>
  </tbody>
</table>
<p style="font-size:8.3pt; color:#475569;">
  ※事故時は警察（110番）への届出を義務化し、損保会社への事故報告・有責判断の窓口はKidsRide本部が一本化して担います。
</p>

<div class="page-break"></div>

<!-- 本文ページ 3 -->
<div class="header-rule">
  <span>三鷹市役所 子ども育成課（波照間様）事前相談資料：一般社団法人KidsRide</span>
  <span>3. 実証実験計画・アンケート調査・代表理事略歴</span>
</div>

<h2>6. 実証実験計画：アンケート調査連動 ＆ 段階的拡大（ロールアウト）</h2>
<div class="accent-box" style="margin-bottom:8px; padding:7px 12px; font-size:8.3pt;">
  <strong>【アンケート調査（データ分析）に基づく対象園の客観的選定】</strong><br>
  実証実験の対象園は恣意的に決定せず、事前アンケート調査で<strong>「送迎困難度（遠方通園・第一希望断念経験）」および「モニター希望率」が最も高かった園からデータに基づいて客観的に選定</strong>し、公平性と実効性を担保します。
</div>

<table style="margin-top:6px; margin-bottom:8px; font-size:8.1pt;">
  <thead>
    <tr>
      <th style="width:20%;">フェーズ</th>
      <th style="width:27%;">対象施設・規模</th>
      <th style="width:53%;">検証テーマ・ステップアップの狙い</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>第1期（1ヶ月目）</strong></td>
      <td><strong>先行 3園</strong><br>（約30世帯 / サポーター約15名）</td>
      <td>アンケートで送迎ニーズ最上位の3園で開始。出庫前点検・GPS・引き渡し認証など安全運用プロセスの徹底検証。</td>
    </tr>
    <tr>
      <td><strong>第2期（2ヶ月目）</strong></td>
      <td><strong>6園へ拡大</strong><br>（約60世帯 / サポーター約30名）</td>
      <td>隣接園・近隣ルートへ拡大。園を跨ぐ保護者間の送迎連携、需要ピーク時のマッチング効率性を検証。</td>
    </tr>
    <tr>
      <td><strong>第3期（3ヶ月目）</strong></td>
      <td><strong>10園へ拡大</strong><br>（約100世帯 / サポーター約50名）</td>
      <td>三鷹駅周辺〜東八道路沿いまでエリア展開。2027年4月本格運用に向けた自律的互助モデルの確立。</td>
    </tr>
  </tbody>
</table>

<div style="font-size:7.9pt; line-height:1.48; color:#334155; margin-bottom:5px;">
  <strong>【直近のご相談（アンケート調査・次回のご報告予定 ＆ 将来的な広報連携）】</strong><br>
  ・<strong>園の負担ゼロ：</strong>スマホWeb回答（所要2〜3分）のため、先生方の集計作業は一切発生しません（お便り同封または掲示のみ）。<br>
  ・<strong>三鷹市・園への無償還元：</strong>集計結果レポートを三鷹市および協力園へ無償提供し、子育て施策・地域交通の基礎エビデンスとしてご活用いただけます。<br>
  ・<strong>次回のご報告・コンタクト予定（11月中旬）：</strong>アンケート集計完了後、集計レポートをまとめ子ども育成課様へ真っ先にご持参・共有し、先行3園選定と実証開始に向けた意見交換の場を頂戴したく存じます。<br>
  ・<strong>将来的な広報連携の検討：</strong>実証実験での安全確認を経て、2027年4月本格運用時には「三鷹市後援名義」の取得や「広報みたか」等での市民周知連携に向けた事前相談を希望いたします。
</div>

<div style="margin-top:14px; padding:12px 14px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; font-size:8.4pt; line-height:1.65;">
  <strong style="color:#1e3a8a; font-size:9.5pt;">【代表理事 略歴・実績：七夕 光明（たなばた みつあき）】</strong><br>
  アップル（Apple）およびアマゾン（Amazon）において24年以上にわたり、業務オペレーション構築、組織マネジメント、品質・コンプライアンス管理のシニアリーダーを歴任。<br>
  <strong>● アマゾンジャパン合同会社（Amazon Ads ビジネスオペレーションズマネージャー / 2022年〜2026年）</strong><br>
  広告審査部門にてマネージャー4名・最大40名規模の組織を統括（Manager of Managers）。品質管理・SLA・根本原因分析サイクルを標準化し、広告審査のエラー・差し戻し率を半減（平時16%→8%、大型セール時30%超→10%未満）へ大幅改善。<br>
  <strong>● アップルジャパン合同会社（ストアマネージャー / APACオペレーションリーダー / 2003年〜2022年・通算19年）</strong><br>
  日本初の旗艦店「Apple 銀座」創業メンバー。初代iPod mini、初代iPhone、iPadの販売・安全運行オペレーションをゼロから構築。60〜80名のスタッフ中、顧客の潜在ニーズを引き出す提案で常時トップ3の営業実績を記録。その後、APAC（日本・シンガポール・台湾・韓国）の製品ローンチ統括リーダーとして初代Apple Watch等の展開を指揮し、納期遵守率実質100%を達成。<br>
  <strong>● 本事業にかける想い：</strong>
  三鷹市在住で<strong>三鷹のぞみ幼稚園に子どもを通わせる現役の父親</strong>として日々の送迎調整の難しさや雨の日の移動負担を当事者として痛感。「顔の見える保護者同士がルールと安心感を持って助け合える仕組みを作りたい」との志から本法人を設立。外資系で培った「徹底した規律遵守・安全運行管理（ミスを構造的に防ぐ仕組みづくり）」を三鷹市の地域社会へ還元してまいります。
</div>

</body>
</html>
"""

html_path = os.path.join(OUTPUT_DIR, "三鷹市事前相談_KidsRide事業概要説明書.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

pdf_path = os.path.join(OUTPUT_DIR, "三鷹市事前相談_KidsRide事業概要説明書.pdf")

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
