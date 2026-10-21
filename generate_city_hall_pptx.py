import os
import subprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.expanduser("~/Desktop/KidsRide/市役所説明資料")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================
# 1. PPTX（プレゼン・印刷用スライド）の生成
# ==========================================
def create_pptx():
    prs = Presentation()
    # 16:9 ワイドスライド
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    BLANK_LAYOUT = prs.slide_layouts[6]

    # カラーパレット
    PRIMARY = RGBColor(30, 58, 138)     # 濃紺 #1e3a8a
    SECONDARY = RGBColor(2, 132, 199)   # 水色 #0284c7
    DARK_TEXT = RGBColor(15, 23, 42)    # 文字色 #0f172a
    MUTED_TEXT = RGBColor(100, 116, 139) # 補足文字 #64748b
    ACCENT = RGBColor(234, 88, 12)      # オレンジ #ea580c
    BG_LIGHT = RGBColor(248, 250, 252)  # 背景薄グレー #f8fafc
    WHITE = RGBColor(255, 255, 255)

    def add_base_slide(title_text, category_text="三鷹市 事前相談・事業概要説明資料"):
        slide = prs.slides.add_slide(BLANK_LAYOUT)
        
        # 背景
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()

        # ヘッダー帯
        header_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.1))
        header_bar.fill.solid()
        header_bar.fill.fore_color.rgb = WHITE
        header_bar.line.color.rgb = RGBColor(226, 232, 240)

        tf = header_bar.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.15)

        p1 = tf.paragraphs[0]
        p1.text = category_text.upper()
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = SECONDARY

        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = PRIMARY

        # フッター
        footer = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.4))
        ftf = footer.text_frame
        fp = ftf.paragraphs[0]
        fp.text = "一般社団法人KidsRide | 子ども送迎相互支援プラットフォーム実証実験"
        fp.font.size = Pt(10)
        fp.font.color.rgb = MUTED_TEXT

        return slide

    # ----------------------------------------------------
    # Slide 1: 表紙
    # ----------------------------------------------------
    slide1 = prs.slides.add_slide(BLANK_LAYOUT)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = PRIMARY
    bg1.line.fill.background()

    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.2), Inches(10.933), Inches(5.1))
    card1.fill.solid()
    card1.fill.fore_color.rgb = WHITE
    card1.line.fill.background()

    tf1 = card1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.8)
    tf1.margin_top = Inches(0.8)

    p = tf1.paragraphs[0]
    p.text = "三鷹市 子ども政策部・地域交通担当窓口 御中"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    p = tf1.add_paragraph()
    p.text = "三鷹市における保育園・幼稚園・学童\n子ども送迎相互支援プラットフォーム実証事業"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_before = Pt(14)

    p = tf1.add_paragraph()
    p.text = "〜 顔の見える保護者同士の互助 × 東京運輸支局確認済の適法設計 × 手厚い包括保険 〜"
    p.font.size = Pt(16)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(10)

    p = tf1.add_paragraph()
    p.text = "提出先：三鷹市役所 子ども政策部 子ども育成課 御中（ご担当：波照間 様）  |  相談日時：2026年10月20日（火）\n提出団体：一般社団法人KidsRide  |  代表理事 七夕 光明（三鷹市在住・三鷹のぞみ幼稚園在園児の父）\n〒181-0013 東京都三鷹市下連雀3-36-1-1701  |  info@kids-ride.jp  |  https://www.kidsride.jp/"
    p.font.size = Pt(11)
    p.font.color.rgb = MUTED_TEXT
    p.space_before = Pt(24)

    # ----------------------------------------------------
    # Slide 2: 事業の背景と課題
    # ----------------------------------------------------
    s2 = add_base_slide("1. 地域が直面する「通園・送迎の壁」と保育現場の課題")
    
    # 2カラムカード
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.7), Inches(4.7))
    c1.fill.solid()
    c1.fill.fore_color.rgb = WHITE
    c1.line.color.rgb = RGBColor(226, 232, 240)
    tf = c1.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.4)
    
    p = tf.paragraphs[0]
    p.text = "【子育て世帯のリアルな困りごと】"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT

    bullets1 = [
        "突発的なピンチへの対応限界:\n急な残業、下の子の発熱・通院、悪天候（豪雨・猛暑）時にお迎えが間に合わない。",
        "送迎不安による園選択の断念:\n「毎日の送迎が難しい・遠い」という理由で、第一希望の幼稚園や保育園を諦めざるを得ないケースが頻発。",
        "既存手段の制約:\nタクシーやシッターは高額。ファミサポは事前調整型のため当日の突発的な依頼に対応しづらい。"
    ]
    for b in bullets1:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.7))
    c2.fill.solid()
    c2.fill.fore_color.rgb = WHITE
    c2.line.color.rgb = RGBColor(226, 232, 240)
    tf = c2.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.4)
    
    p = tf.paragraphs[0]
    p.text = "【園現場およびKidsRideの解決策】"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    bullets2 = [
        "保育現場（園）の負担軽減:\n保護者のお迎え遅れによる保育士の超過勤務や、代理引き渡し時のセキュリティ懸念を解消。",
        "顔の見える同一園の保護者互助:\n見知らぬ他人ではなく、「同じ園に通わせる身元確認済みの保護者」が自分の送迎のついでに支え合う。",
        "地域の安心インフラ構築:\nデジタル技術（GPS・顔認証）と手厚い損害保険を組み合わせ、無理のない地域共助を実現。"
    ]
    for b in bullets2:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    # ----------------------------------------------------
    # Slide 3: サービス概要と非営利・互助設計
    # ----------------------------------------------------
    s3 = add_base_slide("2. KidsRideの仕組み：安心のクローズド設計と実費精算")
    
    # 3つの特徴ボックス
    box_w = Inches(3.64)
    h = Inches(4.7)
    
    # 特徴1
    b1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), box_w, h)
    b1.fill.solid()
    b1.fill.fore_color.rgb = WHITE
    b1.line.color.rgb = SECONDARY
    tf = b1.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "① 同一園の保護者に限定"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    items1 = [
        "・頼む側も受託側も「同じ園に通う保護者」に厳格限定",
        "・本人確認書類 ＋ 在園確認（在園証明書・連絡帳・保護者証）の審査必須",
        "・見知らぬ第三者が介在しない安心のコミュニティ"
    ]
    for it in items1:
        p = tf.add_paragraph()
        p.text = it
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(10)

    # 特徴2
    b2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.84), Inches(1.9), box_w, h)
    b2.fill.solid()
    b2.fill.fore_color.rgb = WHITE
    b2.line.color.rgb = PRIMARY
    tf = b2.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "② 多様な送迎手段に対応"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    items2 = [
        "・徒歩送迎: 手つなぎ引率、見守り歩行",
        "・自転車送迎: 幼児同乗器・ヘルメット着用、日常点検",
        "・車送迎: R129適合チャイルドシート常設、出庫前点検・アルコール検知(0.00mg/L)",
        "・地域の道路事情に応じた柔軟な運用"
    ]
    for it in items2:
        p = tf.add_paragraph()
        p.text = it
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(10)

    # 特徴3
    b3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.88), Inches(1.9), box_w, h)
    b3.fill.solid()
    b3.fill.fore_color.rgb = WHITE
    b3.line.color.rgb = ACCENT
    tf = b3.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "③ 実費とポイントのみ（非営利）"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    items3 = [
        "・車送迎: ガソリン実費のみ（11円/km、端数切捨て）",
        "・自転車/徒歩: 換金不可の相互扶助ポイント（200pt）",
        "・送迎対価による利益を一切排除",
        "・運営費: 月額会費（500円）※実証実験中は完全無料"
    ]
    for it in items3:
        p = tf.add_paragraph()
        p.text = it
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(10)

    # ----------------------------------------------------
    # Slide 4: 法令適合性（東京運輸支局との書面確認）
    # ----------------------------------------------------
    s4 = add_base_slide("3. 法令コンプライアンス：東京運輸支局より「登録不要」の書面回答受領済")
    
    banner = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.733), Inches(1.1))
    banner.fill.solid()
    banner.fill.fore_color.rgb = RGBColor(240, 253, 244)
    banner.line.color.rgb = RGBColor(134, 239, 172)
    tf = banner.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "【道路運送法第78条（自家用有償運送）に関する公式見解】"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(21, 128, 61)
    p = tf.add_paragraph()
    p.text = "国土交通省 関東運輸局 東京運輸支局 輸送統括担当へ事前相談を行い、現行モデルは道路運送法上の許可・登録は一切不要（適法・適用除外）との正式書面回答を受領済みです。"
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT

    # 4つの確認事項表カード
    grid_c = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.2), Inches(11.733), Inches(3.4))
    grid_c.fill.solid()
    grid_c.fill.fore_color.rgb = WHITE
    grid_c.line.color.rgb = RGBColor(226, 232, 240)
    tf = grid_c.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.3)

    legal_items = [
        ("① 自家用車送迎での実費受領", "登録不要（適法）", "ガソリン代実費（11円/km）のみの授受であり、運送の対価にあたらない無償運送の範囲内であるため。"),
        ("② 自転車・徒歩送迎でのポイント授受", "登録不要（適法）", "換金できない相互扶助ポイントであり対価性がなく、かつ人力による移動のため法対象外。"),
        ("③ プラットフォーム利用料の別建て", "登録不要（適法）", "システム利用料はマッチング等の役務対価であり、送迎運送の対価ではないため。"),
        ("④ 決済代行業者を通じた自動決済", "登録不要（適法）", "代行精算を行うのみであり、KidsRide自身が運送事業を経営するものではないため。")
    ]
    
    p = tf.paragraphs[0]
    p.text = "【東京運輸支局との書面確認 4大ポイント】"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    for title, status, reason in legal_items:
        p = tf.add_paragraph()
        p.text = f"● {title} ──【{status}】\n    理由: {reason}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(8)

    # ----------------------------------------------------
    # Slide 5: 三鷹市ファミサポとの共存関係
    # ----------------------------------------------------
    s5 = add_base_slide("4. 三鷹市ファミリー・サポート・センター事業との共存・相互補完")

    table_shape = s5.shapes.add_table(6, 3, Inches(0.8), Inches(1.9), Inches(11.733), Inches(4.7))
    table = table_shape.table
    table.columns[0].width = Inches(2.3)
    table.columns[1].width = Inches(4.7)
    table.columns[2].width = Inches(4.733)

    headers = ["比較項目", "三鷹市ファミリー・サポート・センター", "KidsRide（当事業）"]
    for i, h_text in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h_text
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER

    rows_data = [
        ("支援の性質", "計画的・定期的な支援（事前予約型）", "突発的・日常的なラストワンマイルの互助"),
        ("支援者と利用者の関係", "地域の協力会員（一般市民ボランティア）", "同じ園に通う顔見知りの保護者同士"),
        ("マッチング方式", "アドバイザーを介した事前調整・顔合わせ", "スマホアプリによる即時・柔軟なマッチング"),
        ("主な対応シーン", "毎週決まった習い事、事前の予定支援", "当日の急な残業、下の子の発熱、悪天候等"),
        ("対価・位置づけ", "謝礼金（約800〜1,000円/h）\n公的なセーフティネット支援", "実費のみ（ガソリン代/ポイント）\n園コミュニティ内のピンポイントな助け合い")
    ]

    for row_idx, r_data in enumerate(rows_data, start=1):
        for col_idx, text in enumerate(r_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.color.rgb = DARK_TEXT
                if col_idx == 0:
                    p.font.bold = True

    # ----------------------------------------------------
    # Slide 6: 安全管理と包括保険体制
    # ----------------------------------------------------
    s6 = add_base_slide("5. 安全管理体制と包括損害保険（あいおいニッセイ同和損保）")

    # 左：安全管理システム
    l_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.7), Inches(4.7))
    l_card.fill.solid()
    l_card.fill.fore_color.rgb = WHITE
    l_card.line.color.rgb = RGBColor(226, 232, 240)
    tf = l_card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "【安全運行管理システム】"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    sec_items = [
        "・リアルタイムGPS追跡:\n送迎中は保護者アプリに現在地・速度が常時配信",
        "・顔写真付き引き渡し認証:\n児童取り違え・誤認引き渡しをシステム照合で防止",
        "・出庫前点検・アルコール検知:\n車両送迎時は0.00mg/L検査記録を義務化",
        "・警察110番義務 ＆ 本部窓口一本化:\n事故時はKidsRide本部が損保会社と連携対応"
    ]
    for it in sec_items:
        p = tf.add_paragraph()
        p.text = it
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(8)

    # 右：包括保険
    r_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.7))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = WHITE
    r_card.line.color.rgb = RGBColor(226, 232, 240)
    tf = r_card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "【あいおいニッセイ同和損保 包括保険】"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(21, 128, 61)
    ins_items = [
        "● 自家用車送迎（包括自動車特約）:\n・対人賠償：無制限 / 対物賠償：無制限\n・人身傷害：3,000万円（ドライバー個人保険優先なし）",
        "● 自転車・徒歩送迎（NPO活動総合保険）:\n・第三者賠償責任：最高2億円（免責0円）\n・見舞金費用50万 / 預かり品損壊50万 / 対応費用500万\n・サポーター傷害補償：入院2,000円/日、通院1,000円/日\n・準記名式（登録サポーター全員自動適用）",
        "※サポーター個人の費用負担ゼロ（KidsRide全額負担）"
    ]
    for it in ins_items:
        p = tf.add_paragraph()
        p.text = it
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(8)

    # ----------------------------------------------------
    # Slide 7: 実証実験計画とアンケート調査
    # ----------------------------------------------------
    s7 = add_base_slide("6. 実証実験計画：アンケート調査連動 ＆ 段階的拡大（ロールアウト）")

    # 左カード：アンケート調査と客観的選定
    s7_l = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.7), Inches(4.7))
    s7_l.fill.solid()
    s7_l.fill.fore_color.rgb = WHITE
    s7_l.line.color.rgb = RGBColor(226, 232, 240)
    tf = s7_l.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "【アンケート調査に基づく客観的選定】"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    s7_l_items = [
        "● データに基づく公平な園選定:\n・対象園は恣意的に選ばず、アンケートで「送迎困難度」「モニター希望率」が最も高かった園から客観的に選定。",
        "● 調査の目的と園負担ゼロ:\n・第一希望園の選択断念の実態把握 ＆ モニター世帯募集。\n・スマホWeb回答（所要2〜3分）で先生方の集計作業ゼロ。",
        "● 三鷹市への無償還元 ＆ 次回報告（11月中旬）:\n・集計分析レポートを子ども育成課様へ真っ先にご持参・共有し、先行3園選定と実証開始に向けた意見交換を実施予定。",
        "● 将来的な広報連携の相談:\n・実証での安全確認を経て、本格運用時に向けた「後援名義」や「広報みたか」等での市民周知の要件を相談。"
    ]
    for it in s7_l_items:
        p = tf.add_paragraph()
        p.text = it
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(5)

    # 右カード：1ヶ月毎の段階的ロールアウト
    s7_r = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.7))
    s7_r.fill.solid()
    s7_r.fill.fore_color.rgb = WHITE
    s7_r.line.color.rgb = RGBColor(226, 232, 240)
    tf = s7_r.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "【1ヶ月毎の段階的拡大ロードマップ】"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(21, 128, 61)

    s7_r_items = [
        "● 第1期（1ヶ月目）：先行 3園（約30世帯）\n・アンケートで送迎困難度最上位の3園でスタート。\n・出庫前点検、アルコール検知、リアルタイムGPS追跡、顔写真照合による引き渡し確認など安全運行を徹底検証。",
        "● 第2期（2ヶ月目）：6園へ拡大（約60世帯）\n・隣接園・近隣通園ルートへ拡大展開。\n・園を跨ぐ保護者間の送迎連携やピーク時マッチングを検証。",
        "● 第3期（3ヶ月目）：10園へ拡大（約100世帯）\n・三鷹駅周辺〜東八道路沿いまで対象エリアを拡大。\n・2027年4月本格運用（市内全域）に向けた自律モデル確立。",
        "● 行政・地域交通への貢献:\n・事故ゼロ（0件）の確認とエビデンス蓄積。"
    ]
    for it in s7_r_items:
        p = tf.add_paragraph()
        p.text = it
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(7)

    # ----------------------------------------------------
    # Slide 8: スケジュールと代表略歴
    # ----------------------------------------------------
    s8 = add_base_slide("7. 今後のスケジュール と 法人・代表者略歴")

    sl_l = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.7), Inches(4.7))
    sl_l.fill.solid()
    sl_l.fill.fore_color.rgb = WHITE
    sl_l.line.color.rgb = RGBColor(226, 232, 240)
    tf = sl_l.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "【今後のステップ・時系列計画】"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    sch_items = [
        "・2026年10月20日: 三鷹市役所子ども育成課へ事前相談（波照間様）",
        "・2026年10月下旬〜11月上旬: 市内園での保護者アンケート実施 ＆ ニーズ上位園の選定",
        "・2026年11月中旬: 実証モニター確定 ＆ あいおい包括保険契約締結",
        "・2026年11月下旬〜12月下旬: 【第1期実証】先行3園（約30世帯・月100回）運行",
        "・2027年1月: 【第2期実証】6園へ拡大（約60世帯）",
        "・2027年2月: 【第3期実証】10園へ拡大（約100世帯）",
        "・2027年3月: 実証総括レポート提出・地域公共交通会議報告",
        "・2027年4月〜: 三鷹市内本格運用スタート（月額500円会員制）"
    ]
    for sc in sch_items:
        p = tf.add_paragraph()
        p.text = sc
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(6)

    sl_r = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.7))
    sl_r.fill.solid()
    sl_r.fill.fore_color.rgb = WHITE
    sl_r.line.color.rgb = RGBColor(226, 232, 240)
    tf = sl_r.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "【代表理事 略歴・実績：七夕 光明】"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    bio_items = [
        "● Apple Japan / APAC（2003〜2022年・通算19年）:\n・日本初旗艦店「Apple銀座」創業メンバー。iPod mini、iPhone、iPadの販売・安全運行をゼロから構築。60〜80名中トップ3の個人売上を維持。\n・APAC（日本・シンガポール・台湾・韓国）の製品ローンチ統括としてApple Watch等を展開。全ローンチ納期遵守率実質100%を達成。\n・量販店・キャリア向けサポート窓口を新設、厳格なSLA（応答≤6分、解決≤15分）を定着。",
        "● Amazon Ads Japan（2022〜2026年）:\n・広告審査組織（マネージャー4名・最大40名）を統括（Manager of Managers）。\n・KPI・品質改善サイクルを標準化し、広告差し戻し率を半減（平時16%→8%、セール時30%超→10%未満）へ改善。",
        "● 三鷹市民・現役保護者としての想い:\n・自身も「三鷹のぞみ幼稚園」に子どもを通わせる現役の父親。日々の送迎負担を当事者として痛感。外資系で培った「徹底した規律遵守・安全運行管理（ミスを構造的に防ぐ仕組み）」を結集し、三鷹市の子育て安心インフラを創出します。"
    ]
    for bi in bio_items:
        p = tf.add_paragraph()
        p.text = bi
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(6)

    pptx_path = os.path.join(OUTPUT_DIR, "三鷹市事前相談_KidsRide事業概要説明書.pptx")
    prs.save(pptx_path)
    print(f"PPTX saved to: {pptx_path}")

create_pptx()
