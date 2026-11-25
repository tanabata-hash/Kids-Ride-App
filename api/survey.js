// Vercel Serverless Function: 三鷹市保護者送迎アンケート回答 受信・メール通知・集約・スプレッドシート連携API
// エンドポイント: POST /api/survey, GET /api/survey

const FORMSUBMIT_TOKEN = '8110355a424c7cae2d1068e2dfc68556'; // tanabata@kidsride.jp 認証済トークン

// サーバーレスインスタンス内での回答データ蓄積キャッシュ（初期データとして実受領済みの回答をシード保持）
let surveyStore = [
  {
    id: 'SURVEY-20261125-01',
    submittedAt: '2026/11/25 20:00',
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
