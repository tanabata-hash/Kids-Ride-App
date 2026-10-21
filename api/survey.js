// Vercel Serverless Function: 三鷹市保護者送迎アンケート回答 受信・メール通知API
// エンドポイント: POST /api/survey

const FORMSUBMIT_TOKEN = '8110355a424c7cae2d1068e2dfc68556'; // tanabata@kidsride.jp 認証済トークン

export default async function handler(req, res) {
  // CORSヘッダー設定
  res.setHeader('Access-Control-Allow-Credentials', true);
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

  if (req.method === 'GET') {
    return res.status(200).json({
      status: 'ok',
      service: 'KidsRide Survey Receiver API',
      timestamp: new Date().toISOString()
    });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const data = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;

    if (!data || !data.id) {
      return res.status(400).json({ error: 'Invalid survey data' });
    }

    // 1. Vercelの実行ログに構造化JSONとして永続記録（VercelダッシュボードのLogsで全件閲覧・抽出可能）
    console.log('[KIDSRIDE_SURVEY_SUBMISSION]', JSON.stringify({
      id: data.id,
      submittedAt: data.submittedAt || new Date().toISOString(),
      childAges: data.childAges,
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

    // 2. 代表メール（tanabata@kidsride.jp）へFormSubmit経由で即時メール自動通知
    const emailPayload = {
      _subject: `【KidsRideアンケート回答】${(data.childAges || []).join('・')}の保護者様より新しい回答が届きました (${data.id})`,
      _template: 'table',
      '回答ID': data.id,
      '回答日時': data.submittedAt || new Date().toLocaleString('ja-JP'),
      'Q1_お子様の年齢': Array.isArray(data.childAges) ? data.childAges.join('、') : (data.childAges || ''),
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
      await fetch(`https://formsubmit.co/ajax/${FORMSUBMIT_TOKEN}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Origin': 'https://www.kidsride.jp',
          'Referer': 'https://www.kidsride.jp/'
        },
        body: JSON.stringify(emailPayload)
      });
    } catch (mailErr) {
      console.error('[MAIL_NOTIFICATION_ERROR]', mailErr.message);
    }

    // 3. 外部Webhook（Google Apps Script / スプレッドシート連携用URL等）が設定されている場合は転送
    const externalWebhookUrl = process.env.SURVEY_WEBHOOK_URL;
    if (externalWebhookUrl) {
      try {
        await fetch(externalWebhookUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
      } catch (forwardErr) {
        console.error('[FORWARD_ERROR]', forwardErr.message);
      }
    }

    return res.status(200).json({
      success: true,
      id: data.id,
      message: 'アンケート回答を受信・記録し、メール通知を送信しました。'
    });
  } catch (err) {
    console.error('[API_ERROR]', err);
    return res.status(500).json({ error: 'Internal Server Error', details: err.message });
  }
}
