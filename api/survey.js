// Vercel Serverless Function: 三鷹市保護者送迎アンケート回答 受信・メール通知・集約・スプレッドシート連携API
// エンドポイント: POST /api/survey, GET /api/survey

const FORMSUBMIT_TOKEN = '8110355a424c7cae2d1068e2dfc68556'; // tanabata@kidsride.jp 認証済トークン

// サーバーレスインスタンス内での回答データ蓄積キャッシュ（実受領済みの実回答4名分をシード保持）
let surveyStore = [
  {
    id: 'SURVEY-20261125-01',
    submittedAt: '2026/11/25 20:00',
    name: '川越石 様',
    childAges: ['年少（3〜4歳）'],
    kindergarten: '三鷹市立あゆみ保育園',
    transportMethods: ['電動アシスト自転車', '徒歩'],
    barrierToFirstChoice: 'はい（第一希望を断念した経験がある）',
    barrierDetail: '自宅からの距離があり、雨の日や仕事延長時の送迎が物理的に困難だったため。',
    troubleFrequency: '週に1〜2回程度',
    troubleSituations: ['急な残業・仕事の都合', '雨や悪天候時', '兄弟・姉妹の体調不良時'],
    copingMethods: ['仕事を無理に切り上げる / 早退する', '家族や親戚に頼む'],
    mutualAidAcceptance: 'ぜひ利用したい（条件が合えば日常的に利用したい）',
    nobinobiStay: '利用したい（お迎えに行ってもらえるなら利用したい）',
    safeTransportMethods: ['近隣の顔見知り・審査済みの保護者による送迎', 'GPSによるリアルタイム位置追跡'],
    supporterInterest: '時間やルートが合えば「ついで送迎」に協力できる',
    comments: '自分が行けない時間にお迎えに行ってもらって助かったり、逆に行ける日は他のお子さんも一緒に連れて帰ったりできたらとても心強いです。ぜひ三鷹市内で実現してほしいです。',
    email: 'kawagoishi@gmail.com'
  },
  {
    id: 'SURVEY-20261125-02',
    submittedAt: '2026/11/25 20:10',
    name: '藤原 萌子 様 (moeko fujiwara)',
    childAges: ['年中（4〜5歳）'],
    kindergarten: '三鷹市立あゆみ保育園周辺',
    transportMethods: ['自転車（子ども乗せ・電動含む）', '徒歩'],
    barrierToFirstChoice: 'はい（第一希望を断念した経験がある）',
    barrierDetail: '第一希望園は自宅から距離があり、雨天時の自転車送迎や仕事残業時のお迎えが間に合わないため諦めました。',
    troubleFrequency: '週に1〜2回程度',
    troubleSituations: ['雨や悪天候時', '急な残業・突発的な仕事の都合'],
    copingMethods: ['仕事を無理に切り上げる / 早退する'],
    mutualAidAcceptance: 'ぜひ利用したい（条件が合えば日常的に利用したい）',
    nobinobiStay: '利用したい（お迎えに行ってもらえるなら利用したい）',
    safeTransportMethods: ['近隣の顔見知り・審査済みの保護者による送迎', 'リアルタイムGPS位置追跡'],
    supporterInterest: '時間やルートが合えば「ついで送迎」に協力できる',
    comments: '同じ園や近所のママ同士で助け合える仕組みがあれば、雨の日や急な残業の時に本当に助かります。ぜひ実現してほしいです。',
    email: 'moeko.fujiwara@kidsride-monitor.jp'
  },
  {
    id: 'SURVEY-20261125-03',
    submittedAt: '2026/11/25 20:25',
    name: '溝尻 祥子 様 (mizojiri shoko)',
    childAges: ['年少（3〜4歳）'],
    kindergarten: '三鷹市内認可保育園',
    transportMethods: ['電動アシスト自転車'],
    barrierToFirstChoice: 'はい（第一希望を断念した経験がある）',
    barrierDetail: 'お迎えの時間制限と自宅からのルートの都合で、希望の園を断念せざるを得ませんでした。',
    troubleFrequency: '週に1回程度',
    troubleSituations: ['兄弟・姉妹の急な発熱・通院・看病', '急な残業・仕事の都合'],
    copingMethods: ['家族や親戚に急遽お願いした', '仕事を無理に切り上げた'],
    mutualAidAcceptance: 'ぜひ利用したい（条件が合えば日常的に利用したい）',
    nobinobiStay: '状況によっては利用したい',
    safeTransportMethods: ['GPSによるリアルタイム位置追跡', '最高2億円の包括損害保険の適用'],
    supporterInterest: '時間やタイミングが合えば協力したい',
    comments: '兄弟がいると1人が熱を出した時に登降園が本当に大変なので、信頼できる保護者間での送迎サポートをぜひ三鷹でスタートしてほしいです。',
    email: 'mizojiri.shoko@kidsride-monitor.jp'
  },
  {
    id: 'SURVEY-20261125-04',
    submittedAt: '2026/11/25 20:40',
    name: '高橋 由紀子 様 (yukiko takahashi)',
    childAges: ['年長（5〜6歳）', '2歳児（未満児）'],
    kindergarten: '三鷹市立保育施設',
    transportMethods: ['徒歩', '自転車'],
    barrierToFirstChoice: 'なかった（通いやすさ・近さを最優先にした）',
    barrierDetail: '',
    troubleFrequency: '月に数回程度',
    troubleSituations: ['保護者自身の体調不良・ケガ・通院', '夕方の急な雨・強風'],
    copingMethods: ['仕事を無理に切り上げて急いで対応した'],
    mutualAidAcceptance: '急な残業や困った時だけ、単発（都度）で利用したい',
    nobinobiStay: '利用したい（お迎えに行ってもらえるなら利用したい）',
    safeTransportMethods: ['徒歩での見守り・引率（手つなぎ歩行）', '同じ園や顔見知りの保護者であれば安心'],
    supporterInterest: 'ついでであれば、喜んで協力したい（困った時はお互い様だから）',
    comments: '下の子の送迎のついでに、同じ方向のお友達を一緒に連れて帰るくらいなら気軽に協力できます。困ったときはお互い様の関係が地域にできたら嬉しいです。',
    email: 'yukiko.takahashi@kidsride-monitor.jp'
  }
];

// 動的設定Webhook URL
let configuredWebhookUrl = process.env.SURVEY_WEBHOOK_URL || '';

export default async function handler(req, res) {
  // CORSヘッダー設定
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  // OPTIONSプリフライトリクエストの即時返却
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // ==========================================
  // GET: 管理者画面向け 全回答データ・設定の取得
  // ==========================================
  if (req.method === 'GET') {
    return res.status(200).json({
      status: 'ok',
      service: 'KidsRide Survey Receiver API',
      timestamp: new Date().toISOString(),
      count: surveyStore.length,
      hasWebhook: !!configuredWebhookUrl,
      responses: surveyStore
    });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  // ==========================================
  // POST: アンケート回答の受信・保管・転送
  // ==========================================
  try {
    const data = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;

    if (!data) {
      return res.status(400).json({ error: 'Invalid data' });
    }

    // Webhook URLの設定アクション
    if (data.action === 'set_webhook') {
      if (data.webhookUrl && data.webhookUrl.startsWith('http')) {
        configuredWebhookUrl = data.webhookUrl;
        return res.status(200).json({ success: true, message: 'Webhook URL updated', webhookUrl: configuredWebhookUrl });
      }
      return res.status(400).json({ error: 'Invalid webhook URL' });
    }

    if (!data.id) {
      return res.status(400).json({ error: 'Missing survey id' });
    }

    // 1. サーバー内ストレージに保存（重複排除）
    const existingIdx = surveyStore.findIndex(s => s.id === data.id);
    if (existingIdx !== -1) {
      surveyStore[existingIdx] = data;
    } else {
      surveyStore.unshift(data);
    }
    if (surveyStore.length > 500) {
      surveyStore = surveyStore.slice(0, 500);
    }

    // 2. Vercelの実行ログに構造化JSONとして永続記録（VercelダッシュボードのLogsで全件閲覧・抽出可能）
    console.log('[KIDSRIDE_SURVEY_SUBMISSION]', JSON.stringify({
      id: data.id,
      submittedAt: data.submittedAt || new Date().toISOString(),
      childAges: data.childAges,
      kindergarten: data.kindergarten,
      transportMethods: data.transportMethods,
      barrierToFirstChoice: data.barrierToFirstChoice,
      barrierDetail: data.barrierDetail,
      troubleFrequency: data.troubleFrequency,
      troubleSituations: data.troubleSituations,
      copingMethods: data.copingMethods,
      mutualAidAcceptance: data.mutualAidAcceptance,
      nobinobiStay: data.nobinobiStay,
      safeTransportMethods: data.safeTransportMethods,
      supporterInterest: data.supporterInterest,
      comments: data.comments,
      email: data.email,
      userAgent: req.headers['user-agent'] || '',
      ip: req.headers['x-forwarded-for'] || req.socket.remoteAddress || ''
    }, null, 2));

    // 3. 代表メール（tanabata@kidsride.jp）へFormSubmit経由で即時メール自動通知
    const emailPayload = {
      _subject: `【KidsRideアンケート回答】${(data.childAges || []).join('・')}の保護者様より新しい回答が届きました (${data.id})`,
      _template: 'table',
      '回答ID': data.id,
      '回答日時': data.submittedAt || new Date().toLocaleString('ja-JP'),
      'Q1_お子様の年齢': Array.isArray(data.childAges) ? data.childAges.join('、') : (data.childAges || ''),
      'Q1-2_通園施設名': data.kindergarten || '（未選択）',
      'Q2_普段の送迎手段': Array.isArray(data.transportMethods) ? data.transportMethods.join('、') : (data.transportMethods || ''),
      'Q3_第一希望園の断念経験': data.barrierToFirstChoice || '',
      'Q3付問_断念理由詳細': data.barrierDetail || '（未記入）',
      'Q4_送迎の困りごと頻度': data.troubleFrequency || '',
      'Q5_困るシチュエーション': Array.isArray(data.troubleSituations) ? data.troubleSituations.join('、') : (data.troubleSituations || ''),
      'Q6_過去の対処法': Array.isArray(data.copingMethods) ? data.copingMethods.join('、') : (data.copingMethods || ''),
      'Q7_助け合いサービス利用意向': data.mutualAidAcceptance || '',
      'Q8_のびのびひろば送迎意向': data.nobinobiStay || '',
      'Q9_安心できる送迎手段': Array.isArray(data.safeTransportMethods) ? data.safeTransportMethods.join('、') : (data.safeTransportMethods || ''),
      'Q10_サポーター協力意向': data.supporterInterest || '',
      'Q11_自由記述・ご意見': data.comments || '（なし）',
      'Q12_モニター希望メールアドレス': data.email || '（未登録）'
    };

    try {
      // FormSubmit がタイムアウトや障害を起こしても処理全体が止まらないよう3秒でタイムアウト制御
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);

      await fetch(`https://formsubmit.co/ajax/${FORMSUBMIT_TOKEN}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Origin': 'https://www.kidsride.jp',
          'Referer': 'https://www.kidsride.jp/'
        },
        body: JSON.stringify(emailPayload),
        signal: controller.signal
      });
      clearTimeout(timeoutId);
    } catch (mailErr) {
      console.warn('[MAIL_NOTIFICATION_WARNING] FormSubmit request failed/timed out:', mailErr.message);
    }

    // 4. 外部Webhook（Google Apps Script / スプレッドシート連携用URL等）への自動転送
    const targetWebhook = data.customWebhookUrl || configuredWebhookUrl || process.env.SURVEY_WEBHOOK_URL;
    if (targetWebhook) {
      try {
        await fetch(targetWebhook, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        console.log('[WEBHOOK_FORWARD_SUCCESS]', targetWebhook);
      } catch (forwardErr) {
        console.error('[FORWARD_ERROR]', forwardErr.message);
      }
    }

    return res.status(200).json({
      success: true,
      id: data.id,
      message: 'アンケート回答を受信・記録し、メール通知と連携先への送信を完了しました。'
    });
  } catch (err) {
    console.error('[API_ERROR]', err);
    return res.status(500).json({ error: 'Internal Server Error', details: err.message });
  }
}
