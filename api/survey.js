// Vercel Serverless Function: 三鷹市保護者送迎アンケート回答 受信API
// エンドポイント: POST /api/survey

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

    // 2. 外部Webhook（Google Apps Script / スプレッドシート連携用URL等）が設定されている場合は転送
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
      message: 'アンケート回答を受信・記録しました。'
    });
  } catch (err) {
    console.error('[API_ERROR]', err);
    return res.status(500).json({ error: 'Internal Server Error', details: err.message });
  }
}
