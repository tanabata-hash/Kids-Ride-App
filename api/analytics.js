// Vercel Serverless Function: KidsRide アクセス解析・トラフィック記録API
// エンドポイント: POST /api/analytics, GET /api/analytics

// サーバーレスインスタンス内での直近アクセスログ保持（最大300件）
let recentLogs = [];

export default async function handler(req, res) {
  // CORSヘッダー設定
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,POST');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'Content-Type, X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length'
  );

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // ==========================================
  // GET: 直近のアクセス解析データを取得
  // ==========================================
  if (req.method === 'GET') {
    const cityMap = {
      'Tokyo': '東京都',
      'Mitaka': '東京都三鷹市',
      'Musashino': '東京都武蔵野市',
      'Chofu': '東京都調布市',
      'Fuchu': '東京都府中市',
      'Koganei': '東京都小金井市',
      'Suginami': '東京都杉並区',
      'Setagaya': '東京都世田谷区',
      'Kichijoji': '東京都武蔵野市(吉祥寺)'
    };

    const totalPV = recentLogs.length;
    const uids = new Set(recentLogs.map(l => l.visitorId || l.ip));
    const totalUU = uids.size;

    const pageCounts = {};
    const deviceCounts = { 'iPhone (iOS)': 0, 'Android': 0, 'PC (Mac/Win)': 0, 'その他': 0 };
    const referrerCounts = { 'LINEアプリ経由': 0, 'QRコード/直接アクセス': 0, 'Web検索/その他': 0 };
    const regionCounts = {};

    recentLogs.forEach(l => {
      // 1. ページ別PV
      const p = l.path || '/';
      pageCounts[p] = (pageCounts[p] || 0) + 1;

      // 2. デバイス種別
      const ua = l.userAgent || '';
      if (/iPhone|iPad|iPod/i.test(ua)) deviceCounts['iPhone (iOS)']++;
      else if (/Android/i.test(ua)) deviceCounts['Android']++;
      else if (/Macintosh|Windows|Linux/i.test(ua)) deviceCounts['PC (Mac/Win)']++;
      else deviceCounts['その他']++;

      // 3. 流入経路
      const ref = l.referrer || '';
      if (l.source === 'line' || /Line/i.test(ua) || ref.includes('line.me') || ref.includes('naver')) {
        referrerCounts['LINEアプリ経由']++;
      } else if (l.source === 'qr' || !ref || ref === 'direct' || ref.includes('kidsride.jp')) {
        referrerCounts['QRコード/直接アクセス']++;
      } else {
        referrerCounts['Web検索/その他']++;
      }

      // 4. 地域（Vercelヘッダーの都市名または東京都）
      const city = l.city || '東京都';
      const displayCity = cityMap[city] || city;
      regionCounts[displayCity] = (regionCounts[displayCity] || 0) + 1;
    });

    return res.status(200).json({
      status: 'ok',
      totalPV,
      totalUU,
      pageCounts,
      deviceCounts,
      referrerCounts,
      regionCounts,
      recentLogs: recentLogs.slice(0, 50)
    });
  }

  // ==========================================
  // POST: 新規アクセスログの記録
  // ==========================================
  if (req.method === 'POST') {
    try {
      const body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});

      // Vercel標準のエッジジオロケーションヘッダーから都市・地域・国を取得
      const rawCity = req.headers['x-vercel-ip-city'];
      const city = rawCity ? decodeURIComponent(rawCity) : (body.city || '東京都');
      const region = req.headers['x-vercel-ip-country-region'] || '13';
      const country = req.headers['x-vercel-ip-country'] || 'JP';
      const ip = req.headers['x-forwarded-for']
        ? req.headers['x-forwarded-for'].split(',')[0].trim()
        : (req.socket?.remoteAddress || '127.0.0.1');
      const ua = req.headers['user-agent'] || body.userAgent || '';

      const logEntry = {
        id: 'ACC-' + Date.now().toString(36) + '-' + Math.floor(Math.random() * 1000),
        timestamp: new Date().toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' }),
        path: body.path || '/',
        referrer: body.referrer || 'direct',
        source: body.source || (body.referrer && body.referrer.includes('line') ? 'line' : 'direct'),
        city: city,
        region: region,
        country: country,
        userAgent: ua,
        visitorId: body.visitorId || ip,
        ip: ip.replace(/\.\d+$/, '.***') // プライバシー配慮の末尾マスク化
      };

      recentLogs.unshift(logEntry);
      if (recentLogs.length > 300) {
        recentLogs = recentLogs.slice(0, 300);
      }

      console.log('[KIDSRIDE_PAGE_VIEW]', JSON.stringify(logEntry));

      return res.status(200).json({ status: 'ok', entry: logEntry });
    } catch (err) {
      console.error('[ANALYTICS_ERROR]', err);
      return res.status(500).json({ error: err.message });
    }
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
}
