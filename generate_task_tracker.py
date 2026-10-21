import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import subprocess

OUTPUT_DIR = os.path.expanduser("~/Desktop/KidsRide/実証実験タスクトラッカー")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========================================================
# タスクデータ定義（実証実験までの全時系列アクション）
# ========================================================
tasks = [
    # フェーズ0: 直近準備・保険保留連絡
    ("P0-01", "0. 事前準備", "保険代理店・平様への状況共有メール送信（参加者確定待ちの旨）", "メール送信文", "七夕", "2026/10/16", "2026/10/16", "未着手", 0, "高", "参加人数確定後に正式試算するため一旦待機を依頼"),
    ("P0-02", "0. 事前準備", "Googleフォームの開設（PARENT_SURVEY_FORM.mdの登録）", "Googleフォーム公開URL", "七夕", "2026/10/16", "2026/10/18", "未着手", 0, "高", "第一希望断念の質問を含む全11問。ログイン不要設定"),
    ("P0-03", "0. 事前準備", "Googleスプレッドシート自動連携の設定", "集計用スプレッドシート", "七夕", "2026/10/18", "2026/10/18", "未着手", 0, "高", "フォーム回答のリアルタイム追記を確認"),
    ("P0-04", "0. 事前準備", "回答用QRコードの発行 ＆ A4案内チラシへの貼り付け", "印刷用チラシPDF", "七夕", "2026/10/18", "2026/10/19", "未着手", 0, "高", "スマホカメラでの読取テスト実施"),
    ("P0-05", "0. 事前準備", "三鷹市役所 事前相談資料（PDF/PPTX）の印刷・準備", "提出用資料（カラー印刷）", "七夕", "2026/10/19", "2026/10/20", "未着手", 0, "高", "A4縦PDF（3〜4部）印刷、クリアファイル製本"),

    # フェーズ1: 三鷹市役所への事前相談
    ("P1-01", "1. 三鷹市事前相談", "三鷹市役所（子ども政策部・子ども育成課）へ電話アポ打診", "訪問日時確定（10/20 10:00〜10:30 子ども育成課 波照間様）", "七夕", "2026/10/16", "2026/10/16", "完了", 100, "高", "4月入所選考繁忙期につき15分程度で要約説明・庁内回覧の合意取得"),
    ("P1-02", "1. 三鷹市事前相談", "三鷹市役所 訪問・事業概要説明の実施（子ども育成課 波照間様）", "事前相談完了・所感ヒアリング", "七夕", "2026/10/20", "2026/10/20", "未着手", 0, "高", "15分要約説明、エグゼクティブサマリー提示、庁内情報共有依頼"),
    ("P1-03", "1. 三鷹市事前相談", "三鷹市から送迎ニーズの高い候補園（1〜3園）のアドバイス受領", "候補園リスト", "七夕", "2026/10/22", "2026/10/24", "未着手", 0, "中", "駅から遠い園や送迎相談の多い園を特定"),
    ("P1-04", "1. 三鷹市事前相談", "三鷹商工会 創業補助金（上限30万円）の申請書提出", "補助金申請書類一式", "七夕", "2026/10/23", "2026/10/27", "未着手", 0, "中", "チラシ印刷費・広告費等への充当"),

    # フェーズ2: 園・保護者アンケート＆モニター募集
    ("P2-01", "2. アンケート＆募集", "対象園（1〜3施設）の園長先生へ訪問アポイント連絡", "訪問日時確定", "七夕", "2026/10/26", "2026/10/28", "未着手", 0, "高", "「市役所にも相談済みの実態調査」として打診"),
    ("P2-02", "2. アンケート＆募集", "園長先生への訪問・依頼状持参・趣旨説明", "KINDERGARTEN_REQUEST_LETTER.md", "七夕", "2026/10/28", "2026/10/30", "未着手", 0, "高", "集計負担ゼロ、集計レポート無償還元を確約"),
    ("P2-03", "2. アンケート＆募集", "チラシ印刷（各園100〜200部）の納品・お便り袋同封手配", "印刷現物チラシ", "七夕", "2026/10/30", "2026/11/02", "未着手", 0, "高", "玄関掲示板ポスター掲示も併せて依頼"),
    ("P2-04", "2. アンケート＆募集", "アンケート回答受付・リアルタイム進捗モニタリング", "Googleスプレッドシート回答データ", "七夕", "2026/11/02", "2026/11/13", "未着手", 0, "高", "目標回答数：50〜100世帯。中間集計を確認"),
    ("P2-05", "2. アンケート＆募集", "アンケート受付締切 ＆ 回答データの集計・分析", "集計データ（CSV）", "七夕", "2026/11/13", "2026/11/15", "未着手", 0, "高", "第一希望断念割合、送迎ニーズ、モニター希望者特定"),
    ("P2-06", "2. アンケート＆募集", "「三鷹市 子どもの送迎実態調査レポート」の作成（グラフ化）", "調査報告レポート（PDF）", "七夕", "2026/11/15", "2026/11/16", "未着手", 0, "高", "Googleフォーム自動グラフ＋考察"),
    ("P2-07", "2. アンケート＆募集", "園長先生および三鷹市へレポート共有・お礼訪問", "持参レポート・協力確定", "七夕", "2026/11/16", "2026/11/18", "未着手", 0, "高", "実証実験への正式協力・園内周知の合意取り付け"),

    # フェーズ3: 保険契約締結・実証運行準備
    ("P3-01", "3. 保険・運行準備", "アンケート分析に基づく先行3園および実証モニターの客観選定", "先行3園確定・参加者名簿", "七夕", "2026/11/15", "2026/11/18", "未着手", 0, "高", "ニーズ最上位3園から利用側約30世帯・サポーター約15名を客観選定"),
    ("P3-02", "3. 保険・運行準備", "保険代理店・平様へ確定条件の提示（日数、平均人数、活動時間）", "見積もり条件確定メール", "七夕", "2026/11/18", "2026/11/19", "未着手", 0, "高", "アンケートで確定した実態数値を正確に提示"),
    ("P3-03", "3. 保険・運行準備", "自家用車送迎：自動車包括特約の申込書捺印・車検証9台分提出", "自動車特約申込書類", "七夕", "2026/11/19", "2026/11/21", "未着手", 0, "高", "対人対物無制限、90円/h精算特約"),
    ("P3-04", "3. 保険・運行準備", "自転車・徒歩送迎：NPO活動総合保険の契約締結（暫定・確定精算）", "NPO保険申込書類", "七夕", "2026/11/19", "2026/11/21", "未着手", 0, "高", "賠償2億円＋サポーター傷害。備付名簿確定"),
    ("P3-05", "3. 保険・運行準備", "保険始期日の決定 ＆ 両保険の有効化完了", "保険証券・付保証明", "七夕", "2026/11/21", "2026/11/23", "未着手", 0, "高", "運行開始日前に保険が100%効いている状態にする"),
    ("P3-06", "3. 保険・運行準備", "参加保護者・サポーターへのアプリ案内・アカウント登録", "アプリ登録・審査完了", "七夕", "2026/11/20", "2026/11/24", "未着手", 0, "高", "在園確認、本人確認、備付名簿への自動登載"),
    ("P3-07", "3. 保険・運行準備", "送迎サポーター向け安全運行ブリーフィング（オンライン/対面）", "安全ルール確認・合意", "七夕", "2026/11/23", "2026/11/25", "未着手", 0, "高", "110番義務、アルコール検査、チャイルドシート等"),

    # フェーズ4: 実証実験運行（1ヶ月毎の段階的ロールアウト）・検証・総括
    ("P4-01", "4. 実証運行・検証", "KidsRide 実証実験キックオフ【第1期：先行3園】運行開始", "第1期運行日報・GPSログ", "七夕", "2026/11/26", "2026/11/26", "未着手", 0, "高", "システム無料、先行3園・約30世帯で安全運行の検証開始"),
    ("P4-02", "4. 実証運行・検証", "第1期（3園）運行管理・出庫前点検・アルコール検知・引き渡し監査", "管理ポータル監査ログ", "七夕", "2026/11/26", "2026/12/25", "未着手", 0, "高", "事故ゼロ徹底。11月稼働実績CSVをあいおい損保へ提出"),
    ("P4-03", "4. 実証運行・検証", "【第2期：6園へ拡大】対象園追加・参加者説明会・運行開始", "第2期運行計画・登録名簿", "七夕", "2027/01/05", "2027/01/31", "未着手", 0, "高", "隣接園へ拡大（約60世帯）。園間連携・マッチング効率の検証"),
    ("P4-04", "4. 実証運行・検証", "【第3期：10園へ拡大】三鷹駅周辺〜東八道路沿い展開・運行開始", "第3期運行計画・登録名簿", "七夕", "2027/02/01", "2027/02/28", "未着手", 0, "高", "市内広域展開（約100世帯）。自律的互助モデルの確立"),
    ("P4-05", "4. 実証運行・検証", "実証参加者（全10園・保護者・サポーター）事後アンケート＆総括", "実証総括レポート（PDF）", "七夕", "2027/02/20", "2027/03/05", "未着手", 0, "高", "累計300回運行、事故ゼロ、満足度80%以上の検証"),
    ("P4-06", "4. 実証運行・検証", "三鷹市役所・地域公共交通会議へ総括レポート提出・本格運用協議", "公的報告書・本格合意書", "七夕", "2027/03/05", "2027/03/20", "未着手", 0, "高", "2027年4月本格運用（市内全域展開）に向けた行政連携合意")
]

# ========================================================
# 1. Excel（.xlsx）の生成
# ========================================================
def generate_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "実証実験タスクトラッカー"
    ws.views.sheetView[0].showGridLines = True

    # スタイル定義
    font_title = Font(name="Yu Gothic", size=16, bold=True, color="1E3A8A")
    font_subtitle = Font(name="Yu Gothic", size=10, color="64748B")
    font_header = Font(name="Yu Gothic", size=10, bold=True, color="FFFFFF")
    font_data = Font(name="Yu Gothic", size=9.5)
    font_bold = Font(name="Yu Gothic", size=9.5, bold=True)
    font_kpi_label = Font(name="Yu Gothic", size=9, bold=True, color="475569")
    font_kpi_val = Font(name="Yu Gothic", size=14, bold=True, color="1E3A8A")

    fill_header = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    fill_phase0 = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    fill_phase1 = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")
    fill_phase2 = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    fill_phase3 = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    fill_phase4 = PatternFill(start_color="FCE7F3", end_color="FCE7F3", fill_type="solid")
    fill_kpi = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    # タイトル
    ws["B2"] = "KidsRide 実証実験 アクションアイテム ＆ タスクトラッカー"
    ws["B2"].font = font_title
    ws["B3"] = "一般社団法人KidsRide | 2026年10月中旬〜12月末 実証実験に向けた日次タスク管理台帳"
    ws["B3"].font = font_subtitle

    # KPIサマリーカード
    ws["B5"] = "全タスク数"
    ws["B5"].font = font_kpi_label
    ws["B6"] = len(tasks)
    ws["B6"].font = font_kpi_val

    ws["C5"] = "完了タスク"
    ws["C5"].font = font_kpi_label
    ws["C6"] = '=COUNTIF(I9:I50, "完了")'
    ws["C6"].font = font_kpi_val

    ws["D5"] = "進行中タスク"
    ws["D5"].font = font_kpi_label
    ws["D6"] = '=COUNTIF(I9:I50, "進行中")'
    ws["D6"].font = font_kpi_val

    ws["E5"] = "未着手タスク"
    ws["E5"].font = font_kpi_label
    ws["E6"] = '=COUNTIF(I9:I50, "未着手")'
    ws["E6"].font = font_kpi_val

    ws["F5"] = "全体進捗率"
    ws["F5"].font = font_kpi_label
    ws["F6"] = '=IF(B6>0, C6/B6, 0)'
    ws["F6"].font = font_kpi_val
    ws["F6"].number_format = '0.0%'

    for col in ["B", "C", "D", "E", "F"]:
        ws[f"{col}5"].fill = fill_kpi
        ws[f"{col}5"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"{col}5"].border = thin_border
        ws[f"{col}6"].fill = fill_kpi
        ws[f"{col}6"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"{col}6"].border = thin_border

    # ヘッダー
    headers = [
        "タスクID", "フェーズ", "タスク内容（アクション項目）", "主要成果物 / 確認項目",
        "担当", "開始日", "期日(締切)", "ステータス", "進捗率", "優先度", "備考・確認メモ"
    ]
    start_row = 8
    for col_idx, h_text in enumerate(headers, start=2): # B列から
        cell = ws.cell(row=start_row, column=col_idx, value=h_text)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
    ws.row_dimensions[start_row].height = 26

    # データ行
    for row_idx, t in enumerate(tasks, start=9):
        task_id, phase, task_name, deliverable, owner, start_d, end_d, status, prog, priority, memo = t
        
        row_vals = [task_id, phase, task_name, deliverable, owner, start_d, end_d, status, prog, priority, memo]
        for col_idx, val in enumerate(row_vals, start=2):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_data
            cell.border = thin_border
            
            # 配置・書式
            if col_idx in [2, 6, 7, 8, 9, 11]: # ID, 担当, 日付, ステータス, 優先度
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 10: # 進捗率
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.number_format = '0%'
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

            # フェーズ列のカラーリング
            if col_idx == 3:
                cell.font = font_bold
                if "0. 事前" in phase: cell.fill = fill_phase0
                elif "1. 三鷹" in phase: cell.fill = fill_phase1
                elif "2. アン" in phase: cell.fill = fill_phase2
                elif "3. 保険" in phase: cell.fill = fill_phase3
                elif "4. 実証" in phase: cell.fill = fill_phase4

            # ステータスの文字色
            if col_idx == 9: # ステータス
                cell.font = font_bold
                if status == "完了":
                    cell.font = Font(name="Yu Gothic", size=9.5, bold=True, color="15803D")
                elif status == "進行中":
                    cell.font = Font(name="Yu Gothic", size=9.5, bold=True, color="0284C7")
                elif status == "未着手":
                    cell.font = Font(name="Yu Gothic", size=9.5, bold=True, color="64748B")

            # 優先度
            if col_idx == 11:
                if priority == "高":
                    cell.font = Font(name="Yu Gothic", size=9.5, bold=True, color="DC2626")
        
        ws.row_dimensions[row_idx].height = 22

    # 列幅の自動調整
    col_widths = {
        "A": 3, "B": 10, "C": 18, "D": 45, "E": 28, "F": 8, "G": 12, "H": 12, "I": 12, "J": 10, "K": 8, "L": 38
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    xlsx_path = os.path.join(OUTPUT_DIR, "KidsRide_実証実験タスクトラッカー.xlsx")
    wb.save(xlsx_path)
    print(f"Excel saved to: {xlsx_path}")

# ========================================================
# 2. PDF（印刷用・クリップボード用 A4横）の生成
# ========================================================
def generate_pdf():
    rows_html = ""
    for t in tasks:
        task_id, phase, task_name, deliverable, owner, start_d, end_d, status, prog, priority, memo = t
        
        phase_color = "#f1f5f9"
        if "1. 三鷹" in phase: phase_color = "#e0f2fe"
        elif "2. アン" in phase: phase_color = "#fef3c7"
        elif "3. 保険" in phase: phase_color = "#dcfce7"
        elif "4. 実証" in phase: phase_color = "#fce7f3"

        rows_html += f"""
        <tr>
          <td style="text-align:center; font-weight:700; font-size:8pt;">{task_id}</td>
          <td style="background:{phase_color}; font-weight:700; font-size:8pt; white-space:nowrap;">{phase}</td>
          <td style="font-weight:600; font-size:8.5pt;">{task_name}</td>
          <td style="font-size:7.8pt; color:#475569;">{deliverable}</td>
          <td style="text-align:center; font-size:8pt;">{owner}</td>
          <td style="text-align:center; font-size:7.5pt; white-space:nowrap;">{end_d}</td>
          <td style="text-align:center; font-weight:700; font-size:8pt; color:#64748b;">{status}</td>
          <td style="text-align:center; font-weight:700; font-size:8pt; color:{'#dc2626' if priority=='高' else '#475569'};">{priority}</td>
          <td style="font-size:7.5pt; color:#64748b;">{memo}</td>
          <td style="width:30px; border:1px solid #cbd5e1; text-align:center;">□</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>KidsRide 実証実験タスクトラッカー</title>
<style>
  @page {{
    size: A4 landscape;
    margin: 10mm 10mm 10mm 10mm;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    color: #0f172a;
    margin: 0;
    padding: 0;
    font-size: 8.5pt;
    line-height: 1.4;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid #1e3a8a;
    padding-bottom: 6px;
    margin-bottom: 8px;
  }}
  .title {{
    font-size: 15pt;
    font-weight: 800;
    color: #1e3a8a;
    margin: 0;
  }}
  .subtitle {{
    font-size: 8pt;
    color: #64748b;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 4px;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 4px 6px;
    vertical-align: middle;
  }}
  th {{
    background: #1e3a8a;
    color: white;
    font-weight: 700;
    font-size: 8pt;
    text-align: center;
  }}
  tr:nth-child(even) td {{
    background: #fafafa;
  }}
  .page-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1 class="title">KidsRide 実証実験 アクションアイテム ＆ タスクトラッカー</h1>
    <div class="subtitle">一般社団法人KidsRide | 2026年10月中旬〜12月末 実証実験に向けた日次進捗管理シート</div>
  </div>
  <div style="font-size:8pt; color:#475569; text-align:right;">
    作成日: 2026年10月15日 / 代表理事 七夕 光明<br>
    ※実証実験開始（11月下旬）までの全タスク一覧
  </div>
</div>

<table>
  <thead>
    <tr>
      <th style="width:45px;">ID</th>
      <th style="width:90px;">フェーズ</th>
      <th>タスク内容（アクション項目）</th>
      <th style="width:170px;">成果物 / 確認項目</th>
      <th style="width:35px;">担当</th>
      <th style="width:65px;">期日</th>
      <th style="width:50px;">状態</th>
      <th style="width:40px;">優先度</th>
      <th style="width:230px;">備考・メモ</th>
      <th style="width:30px;">Check</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>

</body>
</html>
"""

    html_path = os.path.join(OUTPUT_DIR, "KidsRide_実証実験タスクトラッカー.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    pdf_path = os.path.join(OUTPUT_DIR, "KidsRide_実証実験タスクトラッカー.pdf")
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

generate_excel()
generate_pdf()
