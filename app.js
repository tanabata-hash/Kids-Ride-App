// システム設定 (System Configuration & Production Switch)
const CONFIG = {
  IS_DEMO: true, // true: デモ・審査・実証実験モード (現在表示中), false: 本番実稼働モード (一瞬で切り替え可能)
  STRIPE_PUBLIC_KEY: 'pk_live_kidsride_production_key_sample',
  FIREBASE_ENABLED: true,
  APP_VERSION: '1.0.0-prod-ready',
  
  // ガソリン実費単価 自動見直し設定 (国交省・運輸支局事前相談コンプライアンス準拠)
  GAS_PRICE_PER_LITER: 170, // 参照レギュラーガソリン平均価格 (円/L)
  FUEL_EFFICIENCY: 15,     // 実用平均燃費 (15km/L固定・コンパクトカー/軽自動車想定)
  GAS_RATE_PER_KM: 11,     // 実費単価: Math.floor(170 / 15) = 11 円/km (切り捨て絶対固定)
  GAS_RATE_MIN: 5,         // 安全バリデーション最小値 (円/km)
  GAS_RATE_MAX: 30         // 安全バリデーション最大値 (円/km)
};

// Firebase 接続用設定 (本番環境接続キーといつでも差し替え可能)
const firebaseConfig = {
  apiKey: "DUMMY_API_KEY_FOR_LOCAL_MOCK_TESTING",
  authDomain: "kids-ride-app.firebaseapp.com",
  projectId: "kids-ride-app",
  storageBucket: "kids-ride-app.appspot.com",
  messagingSenderId: "1234567890",
  appId: "1:1234567890:web:abcdef123456"
};

// Firebaseのモック/本番切り替えロジック
const useRealFirebase = false; // 本番環境接続時は true に変更
if (useRealFirebase) {
  // firebase.initializeApp(firebaseConfig);
  // const db = firebase.firestore();
} else {
  console.log("[Firebase/Production Engine] System initialized. IS_DEMO:", CONFIG.IS_DEMO);
}

// 状態管理 (State management)
const state = {
  currentRoute: 'login',
  isAuthenticated: false, // 未ログイン状態に初期化
  // ガソリン単価改訂の監査ログ（東京運輸支局提示用）
  gasRateAuditLogs: [
    {
      timestamp: '2026-08-25 09:00:00',
      gasPrice: 170,
      fuelEfficiency: 15,
      calculatedRate: 11,
      previousRate: 11,
      source: '資源エネルギー庁 石油製品価格調査（週次発表値）',
      status: '適正承認（Math.floor切り捨て適合）',
      operator: '自動更新（週次 Cron）'
    }
  ],
  // ドライバー受取用 銀行口座情報 (収納代行実費送金用)
  driverBankAccount: {
    bankName: 'みずほ銀行',
    branchName: '三鷹支店',
    branchCode: '210',
    accountType: '普通',
    accountNumber: '1234567',
    accountHolder: 'サトウ カズヤ',
    isRegistered: true
  },
  requestForm: {
    kindergarten: '',
    location: '',
    timeType: 'Morning',
    specificTime: '07:00',
    selectedDriver: 'おまかせ（自動マッチング）',
    frequency: 'once', // 'once' (都度), 'weekly' (週単位), 'monthly' (月単位)
    weeklyDays: [], // 選択された曜日 [1, 2, 3, 4, 5, 6, 7] (1:月〜7:日)
    monthlyType: 'dates', // 'dates' (日付指定), 'flat' (月定額)
    monthlyDays: [], // 選択された日付
    onceDate: null, // 選択された単発の日付
    estimatedPrice: 100, // 初期化
    estimatedPoints: 0,  // ポイント見積もり
    estimatedTrips: 1,
    distanceKm: 2.5,     // 距離 (km)
    oneTripPrice: 100,   // 1回あたりの料金
    isBooked: false
  },
  // GPSリアルタイム追跡の状態管理
  activeRide: {
    status: 'idle', // 'idle' (待機), 'riding' (送迎中), 'completed' (完了)
    transportMethod: 'Car', // 'Car' (車・バイク) または 'Bicycle' (徒歩・自転車)
    currentLocation: null, // { lat, lng }
    routePoints: [],       // 走行予定ルートの座標リスト
    currentIndex: 0,       // 現在位置のインデックス
    intervalId: null       // GPS送信シミュレーターのタイマーID
  },
  driverSchedule: {
    availableDays: [3, 4, 5, 10, 11, 12, 17, 18, 19, 24, 25, 26],
    assignedDays: [11]
  }
};

// 三鷹市内の座標マップデータ (Leaflet地図用)
const coordinatesMap = {
  "三鷹市立あゆみ保育園": { lat: 35.6765, lng: 139.5620 },
  "三鷹市立上連雀保育園": { lat: 35.6896, lng: 139.5492 },
  "三鷹市立大沢保育園": { lat: 35.6791, lng: 139.5312 },
  "三鷹市立牟礼保育園": { lat: 35.6881, lng: 139.5855 },
  "三鷹台保育園": { lat: 35.6945, lng: 139.5982 },
  "明泉幼稚園": { lat: 35.6820, lng: 139.5750 },
  "下連雀3丁目": { lat: 35.6934, lng: 139.5620 }, // 大沢から約3.2kmの位置
  "自宅（デフォルト）": { lat: 35.6920, lng: 139.5930 } // 三鷹台マンション付近
};

// 地球上の2点間の距離を計算する関数 (ハバース公式)
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // 地球の半径 (km)
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

// ルート経由点 (routePoints) の生成 (直線補間)
function generateRoutePoints(start, end, steps = 12) {
  const points = [];
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    points.push({
      lat: start.lat + (end.lat - start.lat) * t,
      lng: start.lng + (end.lng - start.lng) * t
    });
  }
  return points;
}

// GPS 送信シミュレーターのロジック
window.startGpsSimulation = function() {
  const ride = state.activeRide;
  if (ride.intervalId) {
    clearInterval(ride.intervalId);
  }
  
  const startCoord = coordinatesMap[state.requestForm.kindergarten] || coordinatesMap["三鷹市立大沢保育園"];
  const destCoord = coordinatesMap[state.requestForm.location] || coordinatesMap["自宅（デフォルト）"];
  
  // 送迎手段の判定
  const selectedDriverName = state.requestForm.selectedDriver === 'おまかせ（自動マッチング）' ? '佐藤 カズヤ' : state.requestForm.selectedDriver;
  const currentDriver = driversList.find(d => d.name === selectedDriverName) || driversList[1];
  const isCar = (currentDriver.methodType === 'Car' || currentDriver.methodType === 'Motorcycle' || currentDriver.methodType === 'Unknown');
  
  ride.status = 'riding';
  ride.transportMethod = isCar ? 'Car' : 'Bicycle';
  ride.routePoints = generateRoutePoints(startCoord, destCoord, 12); // 12ステップで移動
  ride.currentIndex = 0;
  ride.currentLocation = ride.routePoints[0];
  
  const intervalSec = isCar ? 10 : 15; // 車なら10秒、自転車・徒歩なら15秒
  
  ride.intervalId = setInterval(() => {
    window.simulateGpsStep();
  }, intervalSec * 1000);
  
  render();
};

window.simulateGpsStep = function() {
  const ride = state.activeRide;
  if (ride.status !== 'riding' || !ride.routePoints || ride.routePoints.length === 0) return;
  
  const oldLoc = ride.currentLocation;
  ride.currentIndex++;
  
  if (ride.currentIndex >= ride.routePoints.length) {
    // 目的地に到着 (完了)
    window.stopGpsSimulation(false);
    ride.status = 'completed';
    ride.currentLocation = ride.routePoints[ride.routePoints.length - 1];
    
    // 実績サマリーを更新
    if (state.requestForm.isBooked) {
      alert("目的地に到着しました。送迎完了です！");
    }
    render();
  } else {
    ride.currentLocation = ride.routePoints[ride.currentIndex];
    
    // 画面全体を再描画するとLeafletがリセットされるため、DOMとマーカーの位置を直接更新する
    window.updateGpsPositionOnUi(oldLoc, ride.currentLocation);
  }
};

window.stopGpsSimulation = function(isPause = false) {
  const ride = state.activeRide;
  if (ride.intervalId) {
    clearInterval(ride.intervalId);
    ride.intervalId = null;
  }
  if (isPause) {
    alert("GPS信号の送信を一時停止しました。");
    render();
  }
};

window.resetGpsSimulation = function() {
  const ride = state.activeRide;
  window.stopGpsSimulation(false);
  ride.status = 'idle';
  ride.currentIndex = 0;
  ride.currentLocation = null;
  ride.routePoints = [];
  render();
};

// UIと地図を直接更新する関数 (チラつき防止)
window.updateGpsPositionOnUi = function(oldLoc, newLoc) {
  const ride = state.activeRide;
  if (!oldLoc || !newLoc) return;
  
  // 1. マーカーの滑らかなアニメーション移動
  if (window.driverMarker) {
    window.transitionMarker(window.driverMarker, oldLoc, newLoc, 2000);
  }
  
  // 2. 残り距離のテキスト更新
  const distEl = document.getElementById('tracking-distance-left');
  if (distEl) {
    const destCoord = coordinatesMap[state.requestForm.location] || coordinatesMap["自宅（デフォルト）"];
    const dist = calculateDistance(newLoc.lat, newLoc.lng, destCoord.lat, destCoord.lng);
    distEl.innerText = `${Math.round(dist * 10) / 10} km`;
  }
  
  // 3. 送迎者画面の進捗プログレスバーの更新
  const progressPercent = (ride.currentIndex / (ride.routePoints.length - 1)) * 100;
  const progressBar = document.getElementById('driver-progress-bar-fill');
  if (progressBar) {
    progressBar.style.width = `${progressPercent}%`;
  }
  
  // 送迎者画面の残り時間テキストの更新
  const intervalSec = ride.transportMethod === 'Car' ? 10 : 15;
  const timeEl = document.getElementById('driver-time-left');
  if (timeEl) {
    const remainingSteps = ride.routePoints.length - 1 - ride.currentIndex;
    const minutesLeft = Math.round(remainingSteps * (intervalSec / 6)) / 10;
    timeEl.innerText = `残り約 ${minutesLeft} 分`;
  }
};

// マーカーのアニメーションスライド補間
window.transitionMarker = function(marker, startLatLng, endLatLng, duration = 2000) {
  const startTime = performance.now();
  function animate(time) {
    const elapsed = time - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // イージング (ease-in-out)
    const t = progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;
    
    const lat = startLatLng.lat + (endLatLng.lat - startLatLng.lat) * t;
    const lng = startLatLng.lng + (endLatLng.lng - startLatLng.lng) * t;
    
    marker.setLatLng([lat, lng]);
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }
  requestAnimationFrame(animate);
};

// Router
const ADMIN_ROUTES = ['admin', 'facility-admin', 'driver-dashboard'];

function navigate(route) {
  if (ADMIN_ROUTES.includes(route) && !state.isAuthenticated) {
    window.showCustomAlert('ログインが必要です', 'このページはログイン後にご利用いただけます。');
    return;
  }
  state.currentRoute = route;
  render();
}

// Ensure navigate is globally available for inline event handlers if needed
window.navigate = navigate;

// 洗練されたカスタムモーダル表示関数 (Rich Aesthetics & フリーズ回避)
window.showCustomAlert = function(title, message, callback) {
  // すでにモーダルがあれば削除
  const existingModal = document.getElementById('custom-alert-modal');
  if (existingModal) {
    existingModal.remove();
  }

  let hasCallbackRun = false; // コールバックの重複実行を防止するフラグ

  const modalHtml = `
    <div id="custom-alert-modal" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 9999; opacity: 0; transition: opacity 0.25s ease;">
      <div style="background: white; width: 90%; max-width: 380px; padding: 24px; border-radius: 16px; box-shadow: var(--shadow-xl); text-align: center; transform: scale(0.9); transition: transform 0.25s ease;">
        <div style="font-size: 3rem; color: var(--primary); margin-bottom: 12px;">
          <i class="ph-fill ph-info" style="color: var(--primary);"></i>
        </div>
        <h3 style="margin-top: 0; margin-bottom: 8px; color: var(--text-main); font-size: 1.15rem; font-weight: 700;">${title}</h3>
        <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 20px;">${message}</p>
        <button id="custom-alert-ok-btn" class="btn btn-primary" style="width: 100%; padding: 10px 16px; border-radius: 8px; font-weight: 600; font-size: 0.9rem;">確認</button>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);

  const modal = document.getElementById('custom-alert-modal');
  const content = modal.querySelector('div');
  
  // アニメーション表示
  setTimeout(() => {
    modal.style.opacity = '1';
    content.style.transform = 'scale(1)';
  }, 10);

  const closeFn = () => {
    modal.style.opacity = '0';
    content.style.transform = 'scale(0.9)';
    setTimeout(() => {
      modal.remove();
      if (callback && !hasCallbackRun) {
        hasCallbackRun = true;
        callback();
      }
    }, 250);
  };

  document.getElementById('custom-alert-ok-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    closeFn();
  });
  
  // 背景クリックでも閉じる
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeFn();
    }
  });
};

// HTMLダイアログ表示ユーティリティ
window.showCustomModalHtml = function(title, htmlContent) {
  const existingModal = document.getElementById('custom-alert-modal');
  if (existingModal) existingModal.remove();

  const modalOverlay = document.createElement('div');
  modalOverlay.id = 'custom-alert-modal';
  modalOverlay.style.cssText = `
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background-color: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px);
    display: flex; align-items: center; justify-content: center;
    z-index: 99999; padding: 16px; box-sizing: border-box;
  `;

  modalOverlay.innerHTML = `
    <div style="background: #ffffff; border-radius: 16px; max-width: 440px; width: 100%; padding: 24px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); border: 1px solid #e2e8f0; max-height: 90vh; overflow-y: auto; text-align: left;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">
        <h3 style="margin:0; font-size: 1.1rem; color: #1e293b; font-weight: 700;">${title}</h3>
        <button onclick="document.getElementById('custom-alert-modal').remove()" style="background:none; border:none; font-size:1.2rem; cursor:pointer; color:#64748b;">✕</button>
      </div>
      ${htmlContent}
    </div>
  `;

  document.body.appendChild(modalOverlay);
};

// 送迎パートナー（ドライバー）向け 実費受取銀行口座 登録・変更ダイアログ
window.showBankAccountModal = function() {
  const acc = state.driverBankAccount || {};
  const content = `
    <div style="font-size:0.85rem; line-height:1.6; color:var(--text-main);">
      <div style="background:#f1f5f9; padding:10px 12px; border-radius:8px; margin-bottom:14px; font-size:0.78rem; color:var(--text-muted);">
        <i class="ph-fill ph-shield-check" style="color:var(--primary)"></i> 
        保護者から代理受領（収納代行）したガソリン代実費（20円/km）を全自動で受け取るための指定銀行口座を設定します（Stripe Connect決済送金システム統合済み）。
      </div>
      <div style="margin-bottom:10px;">
        <label style="font-weight:700; display:block; margin-bottom:4px; font-size:0.8rem;">金融機関名</label>
        <input type="text" id="bank-name" class="form-control" value="${acc.bankName || ''}" placeholder="例: みずほ銀行">
      </div>
      <div style="margin-bottom:10px; display:flex; gap:8px;">
        <div style="flex:2;">
          <label style="font-weight:700; display:block; margin-bottom:4px; font-size:0.8rem;">支店名</label>
          <input type="text" id="bank-branch" class="form-control" value="${acc.branchName || ''}" placeholder="例: 三鷹支店">
        </div>
        <div style="flex:1;">
          <label style="font-weight:700; display:block; margin-bottom:4px; font-size:0.8rem;">支店コード</label>
          <input type="text" id="bank-branch-code" class="form-control" value="${acc.branchCode || ''}" placeholder="210">
        </div>
      </div>
      <div style="margin-bottom:10px; display:flex; gap:8px;">
        <div style="flex:1;">
          <label style="font-weight:700; display:block; margin-bottom:4px; font-size:0.8rem;">口座種別</label>
          <select id="bank-type" class="form-control">
            <option value="普通" ${acc.accountType === '普通' ? 'selected' : ''}>普通</option>
            <option value="当座" ${acc.accountType === '当座' ? 'selected' : ''}>当座</option>
          </select>
        </div>
        <div style="flex:2;">
          <label style="font-weight:700; display:block; margin-bottom:4px; font-size:0.8rem;">口座番号 (7桁)</label>
          <input type="text" id="bank-number" class="form-control" value="${acc.accountNumber || ''}" placeholder="1234567">
        </div>
      </div>
      <div style="margin-bottom:16px;">
        <label style="font-weight:700; display:block; margin-bottom:4px; font-size:0.8rem;">口座名義 (全角カナ)</label>
        <input type="text" id="bank-holder" class="form-control" value="${acc.accountHolder || ''}" placeholder="例: サトウ カズヤ">
      </div>
      <button class="btn btn-primary" style="width:100%; padding:10px;" onclick="saveBankAccount()">受取口座情報を保存・有効化する</button>
    </div>
  `;
  window.showCustomModalHtml('実費振込先 銀行口座の登録・変更', content);
};

window.saveBankAccount = function() {
  const bankName = document.getElementById('bank-name').value;
  const branchName = document.getElementById('bank-branch').value;
  const branchCode = document.getElementById('bank-branch-code').value;
  const accountType = document.getElementById('bank-type').value;
  const accountNumber = document.getElementById('bank-number').value;
  const accountHolder = document.getElementById('bank-holder').value;

  if (!bankName || !branchName || !accountNumber || !accountHolder) {
    window.showCustomAlert('入力エラー', 'すべての口座情報を正しく入力してください。');
    return;
  }

  state.driverBankAccount = {
    bankName, branchName, branchCode, accountType, accountNumber, accountHolder, isRegistered: true
  };
  
  const modal = document.getElementById('custom-alert-modal');
  if (modal) modal.remove();

  window.showCustomAlert(
    '受取口座の登録完了',
    `収納代行実費の振込先口座を登録・暗号化保存しました。\n\n【登録口座情報】\n${bankName} ${branchName} (${accountType}) ${accountNumber}\n名義: ${accountHolder}\n\n実費精算時にこちらの口座へStripe Connect経由で送金されます。`
  );
  render();
};

// Components
function renderHeader(title) {
  return `
    <header>
      <div class="brand" style="cursor: pointer;" onclick="navigate('dashboard')">
        <img src="./logo-symbol.png" alt="KidsRide Logo" class="brand-logo-img" style="width: 34px; height: 34px; vertical-align: middle;" />
        <span style="color:#1E293B; font-weight:700;">Kids<span style="color:var(--primary);">Ride</span></span>
      </div>
    </header>
    ${CONFIG.IS_DEMO ? `
      <div style="background-color: #fee2e2; color: #991b1b; text-align: center; padding: 6px 12px; font-size: 0.75rem; font-weight: 700; border-bottom: 1px solid #fca5a5; display: flex; align-items: center; justify-content: center; gap: 6px;">
        <i class="ph-fill ph-warning" style="font-size: 1rem;"></i>
        <span>本サイトは開発中のデモプロトタイプです。実際の送迎や決済は行われません。</span>
      </div>
    ` : ''}
  `;
}

function renderBottomNav() {
  const routes = [
    { id: 'dashboard', icon: 'ph-house', label: 'ホーム' },
    { id: 'request', icon: 'ph-calendar-plus', label: '依頼する' },
    { id: 'active', icon: 'ph-map-pin-line', label: '現在地' },
    { id: 'profile', icon: 'ph-user', label: 'マイページ' }
  ];

  const navItems = routes.map(route => `
    <a class="nav-item ${state.currentRoute === route.id || (route.id === 'profile' && state.currentRoute === 'login') ? 'active' : ''}" 
       onclick="navigate('${route.id}')">
      <i class="${route.id === state.currentRoute ? 'ph-fill' : 'ph'} ${route.icon}"></i>
      <span>${route.label}</span>
    </a>
  `).join('');

  return `<nav class="bottom-nav">${navItems}</nav>`;
}

// Views
window.submitRegistration = function(event) {
  event.preventDefault();
  
  // Save form data to LocalStorage database mock
  const form = event.target;
  const formData = new FormData(form);
  const user = Object.fromEntries(formData.entries());
  user.createdAt = new Date().toLocaleString();
  
  const DB_KEY = 'kidsride_users_db';
  let db = JSON.parse(localStorage.getItem(DB_KEY) || '[]');
  db.push(user);
  localStorage.setItem(DB_KEY, JSON.stringify(db));
  
  showCustomAlert('登録完了', 'データベースに登録が完了しました！', () => navigate('profile'));
};

window.exportCSV = function() {
  if (!state.isAuthenticated) {
    showCustomAlert('アクセス拒否', 'この操作を実行するにはログインが必要です。');
    return;
  }
  const DB_KEY = 'kidsride_users_db';
  let db = JSON.parse(localStorage.getItem(DB_KEY) || '[]');
  if (db.length === 0) {
    alert('登録データがありません。先に新規登録を行ってください。');
    return;
  }
  
  const headers = ['名前', 'メール', '電話', '住所', '保育園', '子ども1', '子ども1年齢', '子ども2', '子ども2年齢', '子ども3', '子ども3年齢', '目的', '登録日時'];
  const rows = db.map(u => [
    u.name || '', u.email || '', u.phone || '', u.address || '', u.kindergarten || '',
    u.child1_name || '', u.child1_age || '',
    u.child2_name || '', u.child2_age || '',
    u.child3_name || '', u.child3_age || '',
    u.purpose || '', u.createdAt || ''
  ]);
  
  let csvContent = headers.join(',') + '\n';
  rows.forEach(rowArray => {
    const row = rowArray.map(item => `"${String(item).replace(/"/g, '""')}"`);
    csvContent += row.join(',') + '\n';
  });
  
  // Excelで文字化けしないようにBOM付きUTF-8にする
  const blob = new Blob([new Uint8Array([0xEF, 0xBB, 0xBF]), csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement("a");
  const url = URL.createObjectURL(blob);
  link.setAttribute("href", url);
  link.setAttribute("download", "registrants.csv");
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

window.submitLogin = function(event) {
  event.preventDefault();
  state.isAuthenticated = true; // ログイン成功フラグ
  navigate('dashboard');
};

function AuthLoginView() {
  const hour = new Date().getHours();
  let greeting = 'こんばんは！';
  if (hour >= 5 && hour < 11) {
    greeting = 'おはようございます！';
  } else if (hour >= 11 && hour < 18) {
    greeting = 'こんにちは！';
  }

  return `
    ${renderHeader('ログイン')}
    <main class="fade-in" style="display:flex; flex-direction:column; justify-content:center; padding-top:20px;">
      <!-- 美しく余白調整されたブランドロゴ -->
      <div class="welcome-logo-container" style="width: 130px; height: 143px; margin: 24px auto 32px auto;">
        <img src="./logo.png" alt="KidsRide Logo" class="welcome-logo" style="width: 100%; height: 100%; object-fit: contain;">
      </div>
      <div style="text-align:center; margin-bottom:24px;">
        <h2 style="color:var(--primary); font-size:1.5rem;">${greeting}</h2>
        <p style="font-size:0.9rem;">メールアドレスとパスワードを入力してください。</p>
      </div>

      <!-- サービス概要案内（銀行口座審査・関係者向け） -->
      <div class="card" style="margin-bottom: 24px; border-left: 4px solid var(--primary); background-color: #f7fafc; padding: 16px; text-align: left;">
        <h3 style="margin-top: 0; font-size: 0.95rem; color: var(--primary); font-weight: 700; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
          <span style="font-size: 1.2rem;">💡</span> KidsRide サービス概要とフェーズ（STEP 1）
        </h3>
        <p style="font-size: 0.8rem; line-height: 1.5; color: var(--text-main); margin-bottom: 10px;">
          KidsRideは、同一の保育園・学童・幼稚園等の施設に子どもを通わせる保護者同士と、施設をつなぐ<strong>「子ども送迎・見守り互助プラットフォーム」</strong>です。送迎者は、依頼者と同一施設に子どもを通わせる保護者に限定しており、施設外の第三者は登録できません。現在は【STEP 1：ボランティア実証実験期】として、送迎運送・資金決済上の法的課題を整理し、非該当となるよう設計・運営しています（国土交通省 東京運輸支局への確認を進めています）。
        </p>
        <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.45; border-top: 1px dashed #e2e8f0; padding-top: 8px;">
          <strong>STEP 1 実証実験期の仕様:</strong>
          <ul style="margin: 4px 0 0 16px; padding: 0;">
            <li><strong>送迎手数料</strong>: 送迎1回ごとの当法人システム手数料は¥0（無徴収）</li>
            <li><strong>車・バイク送迎</strong>: ドライバー利益ゼロ・純粋なガソリン代実費（20円/km）のみ</li>
            <li><strong>徒歩・自転車送迎</strong>: 現金非発生・相互扶助ポイント（200pt）消費のみ</li>
          </ul>
        </div>
      </div>

      <form onsubmit="submitLogin(event)" class="card">
        <div class="form-group">
          <label>メールアドレス</label>
          <input type="email" class="form-control" placeholder="example@email.com">
        </div>

        <div class="form-group">
          <label>パスワード</label>
          <input type="password" class="form-control" placeholder="パスワード">
        </div>

        <button type="submit" class="btn btn-primary" style="margin-top:16px;">ログイン</button>
      </form>

      <div style="text-align:center; margin-top:32px;">
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:8px;">はじめての方はこちら</p>
        <a href="#" onclick="navigate('register')" style="color:var(--primary); font-size:1rem; font-weight:700;">利用者登録ページへ進む</a>
        <div style="margin-top:24px;">
          <a href="#" onclick="navigate('admin')" style="color:var(--text-muted); font-size:0.85rem; text-decoration:underline; display:block; margin-bottom:8px;">★ 登録データ管理者（事業母体）用ページへ</a>
          <a href="#" onclick="navigate('facility-admin')" style="color:var(--text-muted); font-size:0.85rem; text-decoration:underline;">★【法人案内用】学童・提携施設ダッシュボードデモへ</a>
        </div>
      </div>
      </div>
    </main>
  `;
}

window.previewImage = function(event) {
  const reader = new FileReader();
  reader.onload = function(){
    const output = document.getElementById('profile-preview');
    output.src = reader.result;
    output.style.display = 'block';
  };
  if(event.target.files[0]) {
    reader.readAsDataURL(event.target.files[0]);
  }
};

function RegisterView() {
  const options = kindergartens.map(k => `<option value="${k}">${k}</option>`).join('');

  return `
    ${renderHeader('新規登録')}
    <main class="fade-in" style="display:flex; flex-direction:column; justify-content:center; padding-top:20px;">
      <!-- 美しく余白調整されたブランドロゴ -->
      <div class="welcome-logo-container" style="width: 120px; height: 132px; margin: 24px auto 32px auto;">
        <img src="./logo.png" alt="KidsRide Logo" class="welcome-logo" style="width: 100%; height: 100%; object-fit: contain;">
      </div>
      <div style="text-align:center; margin-bottom:24px;">
        <h2 style="color:var(--primary); font-size:1.5rem;">KidsRideへようこそ</h2>
        <p style="font-size:0.9rem;">保護者または送迎者としてご登録ください。</p>
      </div>

      <form onsubmit="submitRegistration(event)" class="card">
        <div class="form-group" style="text-align: center;">
          <label>プロフィール画像（任意）</label>
          <div style="margin: 8px auto; width: 100px; height: 100px; border-radius: 50%; background-color: #f1f5f9; display: flex; align-items: center; justify-content: center; overflow: hidden; border: 2px dashed #cbd5e1; position: relative; cursor: pointer;" onclick="document.getElementById('profile-upload').click()">
            <img id="profile-preview" src="" style="width: 100%; height: 100%; object-fit: cover; display: none; position: absolute; z-index: 2;" />
            <i class="ph ph-camera" style="font-size: 2rem; color: #94a3b8; position: absolute; z-index: 1;" id="camera-icon"></i>
          </div>
          <input type="file" name="profile_image" id="profile-upload" accept="image/*" style="display: none;" onchange="window.previewImage(event); document.getElementById('camera-icon').style.display='none';">
          <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">タップして画像を選択</div>
        </div>

        <div class="form-group">
          <label>お名前（フルネーム）</label>
          <input type="text" name="name" class="form-control" placeholder="例: 山田 花子">
        </div>
        
        <div class="form-group">
          <label>メールアドレス</label>
          <input type="email" name="email" class="form-control" placeholder="example@email.com">
        </div>

        <div class="form-group">
          <label>電話番号</label>
          <input type="tel" name="phone" class="form-control" placeholder="例: 090-1234-5678">
        </div>

        <div class="form-group">
          <label>住所</label>
          <input type="text" name="address" class="form-control" placeholder="例: 東京都三鷹市大沢1-2-3">
        </div>

        <div class="form-group">
          <label>通っている保育園または幼稚園</label>
          <select name="kindergarten" class="form-control" onchange="window.toggleOtherInput(this, 'register-other-kg')">
            <option value="">選択してください（任意）</option>
            ${options}
          </select>
          <input type="text" id="register-other-kg" class="form-control" placeholder="施設名をご記入ください" style="display:none; margin-top:8px;">
        </div>

        <div class="form-group">
          <label>お子さんの名前と年齢（最大3名まで）</label>
          <div style="display:flex; flex-direction:column; gap:8px;">
            <div style="display:flex; gap:8px;">
              <input type="text" name="child1_name" class="form-control" style="flex:2;" placeholder="1人目のお名前（任意）">
              <select name="child1_age" class="form-control" style="flex:1; padding:0 4px;">
                <option value="">年齢</option>
                <option value="0">0歳</option>
                <option value="1">1歳</option>
                <option value="2">2歳</option>
                <option value="3">3歳（年少）</option>
                <option value="4">4歳（年中）</option>
                <option value="5">5歳（年長）</option>
                <option value="6">6歳</option>
              </select>
            </div>
            <div style="display:flex; gap:8px;">
              <input type="text" name="child2_name" class="form-control" style="flex:2;" placeholder="2人目のお名前（任意）">
              <select name="child2_age" class="form-control" style="flex:1; padding:0 4px;">
                <option value="">年齢</option>
                <option value="0">0歳</option>
                <option value="1">1歳</option>
                <option value="2">2歳</option>
                <option value="3">3歳（年少）</option>
                <option value="4">4歳（年中）</option>
                <option value="5">5歳（年長）</option>
                <option value="6">6歳</option>
              </select>
            </div>
            <div style="display:flex; gap:8px;">
              <input type="text" name="child3_name" class="form-control" style="flex:2;" placeholder="3人目のお名前（任意）">
              <select name="child3_age" class="form-control" style="flex:1; padding:0 4px;">
                <option value="">年齢</option>
                <option value="0">0歳</option>
                <option value="1">1歳</option>
                <option value="2">2歳</option>
                <option value="3">3歳（年少）</option>
                <option value="4">4歳（年中）</option>
                <option value="5">5歳（年長）</option>
                <option value="6">6歳</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>パスワード</label>
          <input type="password" name="password" class="form-control" placeholder="8文字以上">
        </div>

        <div class="form-group">
          <label>ご利用の目的</label>
          <select name="purpose" class="form-control">
            <option value="parent">保護者（送迎を依頼する）</option>
            <option value="driver">送迎者（送迎代行を行う）</option>
            <option value="both">両方（保護者・送迎者）</option>
          </select>
        </div>
        <div style="margin-top:16px; margin-bottom:16px; font-size:0.75rem; text-align:center; color:var(--text-muted); line-height:1.5;">
          ご登録により、当サービスの<a href="#" onclick="alert('別途準備した「利用規約」ファイルの内容が表示されます')" style="color:var(--primary); text-decoration:underline;">利用規約</a>、
          <a href="#" onclick="alert('別途準備した「プライバシーポリシー」ファイルの内容が表示されます')" style="color:var(--primary); text-decoration:underline;">プライバシーポリシー</a>、<br>
          <a href="#" onclick="alert('別途準備した「特定商取引法に基づく表記」ファイルの内容が表示されます')" style="color:var(--primary); text-decoration:underline;">特定商取引法に基づく表記</a> に同意したものとみなされます。
        </div>

        <button type="submit" class="btn btn-primary">上記に同意して登録する</button>
      </form>

      <div style="text-align:center; margin-top:20px;">
        <a href="#" onclick="navigate('login')" style="color:var(--primary); font-size:0.9rem; font-weight:600;">すでにアカウントをお持ちの方（ログイン）</a>
      </div>
    </main>
  `;
}

function ProfileView() {
  return `
    ${renderHeader('ユーザープロフィール')}
    <main class="fade-in">
      <div class="card">
        <div class="profile-header">
          <img src="${currentUser.avatar}" alt="Avatar" class="avatar">
          <div>
            <h2>${currentUser.name} 様</h2>
            <div class="rating">
              <i class="ph-fill ph-star"></i>
              ${currentUser.rating}
              <span class="reviews">(${currentUser.reviews}件のレビュー)</span>
            </div>
          </div>
        </div>
        <button class="btn btn-primary" onclick="navigate('dashboard')" style="margin-bottom: 12px;">ホーム画面へ戻る</button>
      </div>

      <h3 style="margin-top:24px; font-size:1.1rem; color:var(--text-main);">相互扶助ポイント（徒歩・自転車送迎用）</h3>
      <div class="card" style="margin-bottom:16px; padding:16px; background:#fafdfb; border:1px solid #c6f6d5;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div>
            <span style="font-size:0.8rem; color:var(--text-muted); display:block;">保有相互扶助ポイント</span>
            <strong style="font-size:1.5rem; color:var(--secondary);">1,000 pt</strong>
          </div>
        </div>
        <p style="font-size:0.75rem; color:var(--text-muted); margin:8px 0 0 0; line-height:1.45;">
          ※登録時初期付与ポイントです。地域の助け合い送迎（自分が送迎をお手伝いすること）でポイントが貯まります。
        </p>
      </div>

      <h3 style="margin-top:24px; font-size:1.1rem; color:var(--text-main);">保護者（依頼）向けメニュー</h3>
      <div class="card" style="margin-bottom:16px; padding: 12px 16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:12px; margin-bottom:12px; cursor:pointer;" onclick="alert('支払い方法の登録・変更画面を表示します')">
          <span style="font-weight:600;"><i class="ph ph-credit-card" style="margin-right:8px;"></i>支払い方法の管理</span>
          <i class="ph ph-caret-right" style="color:var(--text-muted)"></i>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; cursor:pointer;" onclick="alert('これまでの依頼履歴を表示します')">
          <span style="font-weight:600;"><i class="ph ph-clock-counter-clockwise" style="margin-right:8px;"></i>依頼履歴</span>
          <i class="ph ph-caret-right" style="color:var(--text-muted)"></i>
        </div>
      </div>

      <h3 style="margin-top:24px; font-size:1.1rem; color:var(--primary);">送迎協力者（ドライバー）向けメニュー</h3>
      <div class="card" style="margin-bottom:16px; padding: 12px 16px; border: 2px solid #e2e8f0;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:12px; margin-bottom:12px; cursor:pointer;" onclick="navigate('driver-dashboard')">
          <span style="font-weight:700; color:var(--primary);"><i class="ph-fill ph-steering-wheel" style="margin-right:8px;"></i>稼働・実費精算ダッシュボード</span>
          <i class="ph ph-caret-right" style="color:var(--primary)"></i>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:12px; margin-bottom:12px; cursor:pointer;" onclick="showBankAccountModal()">
          <span style="font-weight:600;"><i class="ph ph-bank" style="margin-right:8px; color:var(--primary);"></i>実費振込先 銀行口座の登録・設定</span>
          <span style="font-size:0.75rem; color:var(--primary); font-weight:700;">${state.driverBankAccount.bankName || '未登録'} <i class="ph ph-caret-right"></i></span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; cursor:pointer;" onclick="navigate('driver-verify')">
          <span style="font-weight:600;"><i class="ph ph-identification-card" style="margin-right:8px;"></i>審査書類（運転免許証・同一施設在園確認書類等）のアップロード</span>
          <i class="ph ph-caret-right" style="color:var(--text-muted)"></i>
        </div>
      </div>
    </main>
    ${renderBottomNav()}
  `;
}

function DashboardView() {
  const historyList = rideHistory.map(ride => `
    <div class="card" style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-weight:600; color:var(--primary);">${ride.date} (${ride.type === 'Morning' ? '朝' : '夕'})</div>
        <div style="font-size:0.9rem; margin-top:4px;">${ride.location}</div>
        <div style="font-size:0.8rem; color:var(--text-muted); display:flex; align-items:center; gap:4px;">
          担当: ${ride.driver}
          <span style="color:var(--warning); display:flex; align-items:center; font-weight:600;">
            <i class="ph-fill ph-star"></i>${ride.rating}
          </span>
        </div>
      </div>
      <div>
        <span style="background:#def7ec; color:var(--secondary); padding:4px 8px; border-radius:12px; font-size:0.8rem; font-weight:600;">${ride.status}</span>
      </div>
    </div>
  `).join('');

  let activePlanHtml = '';
  if (state.requestForm.isBooked) {
    let detailText = '';
    let titleText = '';
    if (state.requestForm.frequency === 'once') {
      titleText = '確定済みの送迎依頼（単発）';
      detailText = `単発・都度送迎 (8月${state.requestForm.onceDate}日) ${state.requestForm.specificTime}指定 お迎え・お送り`;
    } else if (state.requestForm.frequency === 'weekly') {
      titleText = '契約中の定期プラン（週単位）';
      const dayNames = ['月', '火', '水', '木', '金', '土', '日'];
      const selectedDays = state.requestForm.weeklyDays.map(d => dayNames[d - 1]).join('・');
      detailText = `毎週 [${selectedDays}] ${state.requestForm.specificTime}指定 お送り・お迎え`;
    } else if (state.requestForm.frequency === 'monthly') {
      titleText = '契約中の定期プラン（月単位）';
      if (state.requestForm.monthlyType === 'dates') {
        detailText = `月単位日付指定 (計 ${state.requestForm.estimatedTrips}回) ${state.requestForm.specificTime}指定`;
      } else {
        detailText = `安心月定額プラン (平日毎日) ${state.requestForm.specificTime}指定`;
      }
    }
    
    // 2026年8月のカレンダーを生成 (1日は土曜日、前月分余白6日、当月31日、翌月分余白5日、計42マス)
    let calendarDaysHtml = '';
    for (let i = 0; i < 6; i++) {
      calendarDaysHtml += '<div class="calendar-day muted"></div>';
    }
    for (let d = 1; d <= 31; d++) {
      // 曜日を計算 (0:日、1:月、...、6:土)
      const w = (d + 5) % 7; 
      const dayOfWeekVal = w === 0 ? 7 : w; // 1:月〜7:日
      
      let isSelected = false;
      if (state.requestForm.frequency === 'once') {
        isSelected = (state.requestForm.onceDate === d);
      } else if (state.requestForm.frequency === 'weekly') {
        isSelected = state.requestForm.weeklyDays.includes(dayOfWeekVal);
      } else if (state.requestForm.frequency === 'monthly') {
        if (state.requestForm.monthlyType === 'dates') {
          isSelected = state.requestForm.monthlyDays.includes(d);
        } else {
          // 平日のみ
          isSelected = (dayOfWeekVal >= 1 && dayOfWeekVal <= 5);
        }
      }
      
      const selectedClass = isSelected ? 'day-parent-selected' : '';
      calendarDaysHtml += `<div class="calendar-day ${selectedClass}" style="cursor: default; pointer-events: none;">${d}</div>`;
    }
    for (let i = 0; i < 5; i++) {
      calendarDaysHtml += '<div class="calendar-day muted"></div>';
    }
    
    activePlanHtml = `
      <div class="card" style="border: 2px solid var(--secondary); background: #f0fdf4; margin-bottom: 20px; box-shadow: none; cursor: default;">
        <h3 style="color: var(--secondary); margin-top: 0; display: flex; align-items: center; gap: 6px; font-size: 1.05rem;">
          <i class="ph-fill ph-check-circle" style="font-size: 1.2rem;"></i> ${titleText}
        </h3>
        <p style="font-size: 0.9rem; font-weight: 700; margin-bottom: 6px; color: var(--text-main); margin-top: 8px;">
          対象施設: ${state.requestForm.kindergarten || '三鷹市立大沢保育園'}
        </p>
        <p style="font-size: 0.8rem; margin-bottom: 12px; color: var(--text-muted); line-height: 1.4;">
          <strong>プラン内容:</strong> ${detailText}<br>
          <strong>待ち合わせ:</strong> ${state.requestForm.location || '指定場所'}<br>
          <strong>担当予定:</strong> ${state.requestForm.selectedDriver === 'おまかせ（自動マッチング）' ? 'おまかせ（自動割当）' : state.requestForm.selectedDriver}
        </p>
        
        <!-- 日程カレンダー表示 -->
        <div style="border-top: 1px dashed #c2f5d3; padding-top: 12px; margin-top: 12px;">
          <div style="font-size:0.8rem; font-weight:700; color:var(--text-main); margin-bottom:8px; display:flex; align-items:center; gap:4px;">
            <i class="ph ph-calendar-check" style="color:var(--secondary);"></i> 8月の送迎予定カレンダー
          </div>
          <div class="calendar-container" style="padding: 8px; box-shadow: none; border-color: #c2f5d3; background: #fafdfb; margin-top: 4px;">
            <div class="calendar-grid">
              ${['日', '月', '火', '水', '木', '金', '土'].map(w => `<div class="calendar-weekday" style="font-size:0.7rem; padding-bottom:4px;">${w}</div>`).join('')}
              ${calendarDaysHtml}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  return `
    ${renderHeader('ホーム')}
    <main class="fade-in">
      <div class="card" style="background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: white; margin-bottom: 20px;">
        <h2 style="color: white; font-size:1.5rem;">こんにちは、${currentUser.name.split(' ')[0]}さん！</h2>
        
        <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; margin-top: 12px; margin-bottom: 12px;">
          <h3 style="margin:0 0 8px 0; font-size:1rem; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 4px; color:white;">本日の送迎予定（未完了）</h3>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div style="font-weight:700;">17:00 (お迎え)</div>
              <div style="font-size:0.9rem;">三鷹市立大沢保育園</div>
              <div style="font-size:0.8rem; margin-top:4px;">担当: 高橋 ケンタ</div>
            </div>
            <button class="btn" style="background:white; color:var(--primary); width:auto; padding:8px 16px; font-size:0.85rem;" onclick="navigate('active')">詳細を見る</button>
          </div>
        </div>

        <button class="btn" style="background:transparent; border:1px solid white; color:white; margin-top:4px;" onclick="navigate('request')">新しく依頼する</button>
      </div>

      ${activePlanHtml}

      <h3>過去の送迎履歴</h3>
      ${historyList}
    </main>
    ${renderBottomNav()}
  `;
}

// Global functions for handling request form
window.toggleOtherInput = function(selectElem, targetId) {
  const target = document.getElementById(targetId);
  if (target) {
    if (selectElem.value === 'その他（自由記入）') {
      target.style.display = 'block';
      target.focus();
    } else {
      target.style.display = 'none';
      target.value = '';
    }
  }
};

window.updateDriver = function(val) {
  state.requestForm.selectedDriver = val;
  window.calculateEstimation();
  render();
};
window.selectTimeType = function(timeType) {
  state.requestForm.timeType = timeType;
  if(timeType === 'Morning') {
    state.requestForm.specificTime = '07:00';
  } else {
    state.requestForm.specificTime = '11:00';
  }
  render();
};
window.updateSpecificTime = function(val) {
  state.requestForm.specificTime = val;
};

function isFormValid() {
  const form = state.requestForm;
  if (!form.kindergarten) return false;
  if (form.frequency === 'once' && !form.onceDate) return false;
  if (form.frequency === 'weekly' && form.weeklyDays.length === 0) return false;
  if (form.frequency === 'monthly' && form.monthlyType === 'dates' && form.monthlyDays.length === 0) return false;
  return true;
}

window.submitRequestForm = function(event) {
  event.preventDefault();
  const select = document.getElementById('kg-select');
  const location = document.getElementById('location-input');
  const otherInput = document.getElementById('kg-other-input');
  
  if (select) {
    if (select.value === 'その他（自由記入）' && otherInput && otherInput.value) {
      state.requestForm.kindergarten = otherInput.value + '（その他）';
    } else {
      state.requestForm.kindergarten = select.value;
    }
  }
  if (location) {
    state.requestForm.location = location.value;
  }
  
  if (!isFormValid()) {
    window.showCustomAlert('必要項目を選択してください', '1. 三鷹市内の幼稚園・保育園、および 6. 送迎日 を選択してください。');
    return;
  }

  // 自動マッチング時のドライバー決定ロジック
  if (state.requestForm.selectedDriver === 'おまかせ（自動マッチング）') {
    const match = driversList.find(d => d.kindergarten === state.requestForm.kindergarten);
    if (match) {
      state.requestForm.selectedDriver = match.name;
    } else {
      state.requestForm.selectedDriver = driversList[1].name; // 佐藤カズヤをフォールバックに
    }
  }
  
  // 強制的に最終再計算を走らせる
  window.calculateEstimation();
  
  navigate('payment');
};

// 幼稚園・保育園の選択変更時のイベントハンドラ
window.changeKindergarten = function(val) {
  const otherInput = document.getElementById('request-other-kg');
  if (val === 'その他（自由記入）') {
    if (otherInput) {
      otherInput.style.display = 'block';
      otherInput.focus();
    }
    state.requestForm.kindergarten = otherInput ? otherInput.value : '';
  } else {
    if (otherInput) {
      otherInput.style.display = 'none';
      otherInput.value = '';
    }
    state.requestForm.kindergarten = val;
  }
  window.calculateEstimation();
  render();
};

// その他幼稚園の自由記述入力時のイベントハンドラ
window.changeOtherKindergarten = function(val) {
  state.requestForm.kindergarten = val;
  window.calculateEstimation();
};

// 待ち合わせ場所（目的地）の選択変更時のイベントハンドラ
window.changeLocation = function(val) {
  state.requestForm.location = val;
  window.calculateEstimation();
  render();
};

// ガソリン実費単価（円/km）算定関数（切り上げ・四捨五入絶対禁止・Math.floor固定）
window.calculateGasRatePerKm = function(pricePerLiter, fuelEfficiency = CONFIG.FUEL_EFFICIENCY) {
  if (typeof pricePerLiter !== 'number' || isNaN(pricePerLiter) || pricePerLiter <= 0) {
    return 11; // デフォルト値
  }
  return Math.floor(pricePerLiter / fuelEfficiency);
};

// ガソリン価格更新＆実費単価自動改訂関数（監査ログ記録・安全チェック付）
window.updateGasPriceAndRate = function(newPrice, sourceReason = '管理画面からの手動設定・手動更新') {
  const priceNum = Number(newPrice);
  if (isNaN(priceNum) || priceNum <= 0) {
    window.showCustomAlert('入力エラー', '正しいガソリン価格（円/L）を半角数字で入力してください。');
    return false;
  }

  const newRate = window.calculateGasRatePerKm(priceNum, CONFIG.FUEL_EFFICIENCY);

  // 安全レンジ検証 (5〜30円/km)
  if (newRate < CONFIG.GAS_RATE_MIN || newRate > CONFIG.GAS_RATE_MAX) {
    window.showCustomAlert(
      '⚠️ 異常値警告（自動反映を中止しました）',
      `算定単価（${newRate}円/km）が安全想定範囲（${CONFIG.GAS_RATE_MIN}〜${CONFIG.GAS_RATE_MAX}円/km）を外れているため、自動反映をストップしました。`
    );
    return false;
  }

  const oldRate = CONFIG.GAS_RATE_PER_KM;
  CONFIG.GAS_PRICE_PER_LITER = priceNum;
  CONFIG.GAS_RATE_PER_KM = newRate;

  // 監査ログ（運輸支局提示用）への記録
  const nowStr = new Date().toLocaleString('ja-JP');
  if (!state.gasRateAuditLogs) state.gasRateAuditLogs = [];
  state.gasRateAuditLogs.unshift({
    timestamp: nowStr,
    gasPrice: priceNum,
    fuelEfficiency: CONFIG.FUEL_EFFICIENCY,
    calculatedRate: newRate,
    previousRate: oldRate,
    source: sourceReason,
    status: '適正承認（Math.floor切り捨て適合）',
    operator: '管理者実行'
  });

  if (window.calculateEstimation) {
    window.calculateEstimation();
  }

  window.showCustomAlert(
    '実費単価を適正改訂しました',
    `【改訂結果】\n・参照ガソリン価格: ¥${priceNum} / L\n・実用平均燃費: ${CONFIG.FUEL_EFFICIENCY} km/L 固定\n・新実費単価: ¥${newRate} / km (計算式: Math.floor(${priceNum}/15))\n\n※運輸支局提示用の監査ログへ保存されました。`
  );

  render();
  return true;
};

// 繰り返し設定と料金見積もり計算用の関数
window.calculateEstimation = function() {
  const form = state.requestForm;
  
  // 1. 出発地と目的地の距離 (distanceKm) を動的計算
  const startCoord = coordinatesMap[form.kindergarten];
  const destCoord = coordinatesMap[form.location] || coordinatesMap["自宅（デフォルト）"];
  
  if (startCoord && destCoord) {
    form.distanceKm = calculateDistance(startCoord.lat, startCoord.lng, destCoord.lat, destCoord.lng);
  } else {
    form.distanceKm = 2.5; // 座標未特定時のデフォルト値
  }
  // 小数点第1位に四捨五入
  form.distanceKm = Math.round(form.distanceKm * 10) / 10;
  
  // 2. 選択された送迎パートナーの移動手段を特定 (車・バイクか、徒歩・自転車か)
  const currentDriver = driversList.find(d => d.name === form.selectedDriver) || driversList[0];
  const isCar = (currentDriver.methodType === 'Car' || currentDriver.methodType === 'Motorcycle' || currentDriver.methodType === 'Unknown');
  
  // 3. 送迎回数のカウント
  if (form.frequency === 'once') {
    form.estimatedTrips = 1;
  } else if (form.frequency === 'weekly') {
    const tripsPerWeek = form.weeklyDays.length;
    form.estimatedTrips = tripsPerWeek * 4;
  } else if (form.frequency === 'monthly') {
    if (form.monthlyType === 'dates') {
      form.estimatedTrips = form.monthlyDays.length;
    } else {
      form.estimatedTrips = 20; // 平日毎日 (安心月定額プラン)
    }
  }
  
  // 4. STEP 1 (ボランティア実証実験期) の精算額・消費ポイント計算
  if (isCar) {
    // 【車・バイクの場合】：過分な利益ゼロ・ガソリン代実費のみ（CONFIG.GAS_RATE_PER_KM 円/km・切り捨て計算）、個別手数料¥0
    if (form.frequency === 'monthly' && form.monthlyType === 'flat') {
      // 月額コミュニティ会員費プラン（個別送迎と切り離された月額固定費）
      form.estimatedPrice = 1000;
      form.estimatedPoints = 0;
      form.oneTripPrice = Math.round(form.distanceKm * CONFIG.GAS_RATE_PER_KM);
    } else {
      const gasFee = Math.round(form.distanceKm * CONFIG.GAS_RATE_PER_KM);
      form.oneTripPrice = gasFee;
      form.estimatedPrice = gasFee * form.estimatedTrips;
      form.estimatedPoints = 0;
    }
  } else {
    // 【徒歩・自転車の場合】：現金非発生・相互扶助ポイントのみ（200pt/回）、個別手数料¥0
    if (form.frequency === 'monthly' && form.monthlyType === 'flat') {
      // 月額コミュニティ会員費プラン
      form.estimatedPrice = 1000;
      form.estimatedPoints = 4000;
      form.oneTripPrice = 50;
    } else {
      form.oneTripPrice = 0;
      form.estimatedPrice = 0;
      form.estimatedPoints = 200 * form.estimatedTrips;
    }
  }
};

window.changeFrequency = function(freq) {
  state.requestForm.frequency = freq;
  window.calculateEstimation();
  render();
};

window.toggleWeeklyDay = function(day) {
  const idx = state.requestForm.weeklyDays.indexOf(day);
  if (idx > -1) {
    state.requestForm.weeklyDays.splice(idx, 1);
  } else {
    state.requestForm.weeklyDays.push(day);
    state.requestForm.weeklyDays.sort();
  }
  window.calculateEstimation();
  render();
};

window.changeMonthlyType = function(type) {
  state.requestForm.monthlyType = type;
  window.calculateEstimation();
  render();
};

window.toggleMonthlyDay = function(day) {
  const idx = state.requestForm.monthlyDays.indexOf(day);
  if (idx > -1) {
    state.requestForm.monthlyDays.splice(idx, 1);
  } else {
    state.requestForm.monthlyDays.push(day);
    state.requestForm.monthlyDays.sort((a, b) => a - b);
  }
  window.calculateEstimation();
  render();
};

window.selectOnceDay = function(day) {
  state.requestForm.onceDate = day;
  render();
};

window.submitRequest = function(event) {
  event.preventDefault();

  // バリデーション
  if (state.requestForm.frequency === 'once' && !state.requestForm.onceDate) {
    showCustomAlert('入力エラー', '送迎を希望する日付を選択してください。');
    return;
  }
  if (state.requestForm.frequency === 'weekly' && state.requestForm.weeklyDays.length === 0) {
    showCustomAlert('入力エラー', '送迎を希望する曜日を1つ以上選択してください。');
    return;
  }
  if (state.requestForm.frequency === 'monthly' && state.requestForm.monthlyType === 'dates' && state.requestForm.monthlyDays.length === 0) {
    showCustomAlert('入力エラー', '送迎を希望する日付を1つ以上選択してください。');
    return;
  }

  const select = document.getElementById('kindergarten-select');
  const otherInput = document.getElementById('request-other-kg');
  const location = document.getElementById('location-input');
  
  if (select.value === 'その他（自由記入）' && otherInput && otherInput.value) {
    state.requestForm.kindergarten = otherInput.value + '（その他）';
  } else {
    state.requestForm.kindergarten = select.value;
  }
  state.requestForm.location = location.value;
  
  // 自動マッチング時のドライバー決定ロジック
  if (state.requestForm.selectedDriver === 'おまかせ（自動マッチング）') {
    const match = driversList.find(d => d.kindergarten === state.requestForm.kindergarten);
    if (match) {
      state.requestForm.selectedDriver = match.name;
    } else {
      state.requestForm.selectedDriver = driversList[1].name; // 佐藤カズヤをフォールバックに
    }
  }
  
  // 強制的に最終再計算を走らせる
  window.calculateEstimation();
  
  navigate('payment');
};

function RequestFormView() {
  const currentDriverInfo = driversList.find(d => d.name === state.requestForm.selectedDriver) || driversList[0];
  const isOtherKg = kindergartens.indexOf(state.requestForm.kindergarten) === -1 && state.requestForm.kindergarten !== '';
  
  // 移動手段の判定 (車・バイクか、徒歩・自転車か)
  const isCar = (currentDriverInfo.methodType === 'Car' || currentDriverInfo.methodType === 'Motorcycle' || currentDriverInfo.methodType === 'Unknown');

  return `
    ${renderHeader('送迎を依頼する')}
    <main class="fade-in">
      <form onsubmit="submitRequest(event)">
        <div class="form-group">
          <label>1. 三鷹市内の幼稚園・保育園を選択</label>
          <select id="kindergarten-select" class="form-control" onchange="window.changeKindergarten(this.value)">
            <option value="">選択してください</option>
            ${kindergartens.map(k => `
              <option value="${k}" ${state.requestForm.kindergarten === k ? 'selected' : (k === 'その他（自由記入）' && isOtherKg ? 'selected' : '')}>${k}</option>
            `).join('')}
          </select>
          <input type="text" id="request-other-kg" class="form-control" placeholder="施設名をご記入ください" style="display:${isOtherKg ? 'block' : 'none'}; margin-top:8px;" value="${isOtherKg ? state.requestForm.kindergarten : ''}" onchange="window.changeOtherKindergarten(this.value)">
        </div>

        <div class="form-group">
          <label>2. 待ち合わせ場所</label>
          <input type="text" id="location-input" class="form-control" placeholder="例: 自宅マンションエントランス" value="${state.requestForm.location}" onchange="window.changeLocation(this.value)">
        </div>

        <div class="form-group">
          <label>3. 送迎者の選択</label>
          <select id="driver-select" class="form-control" onchange="updateDriver(this.value)">
            ${driversList.map(d => `<option value="${d.name}" ${state.requestForm.selectedDriver === d.name ? 'selected' : ''}>${d.name}</option>`).join('')}
          </select>
        </div>

        <div class="form-group">
          <label>4. 送迎手段（担当送迎者に紐づきます）</label>
          <div class="transport-card selected" style="cursor: default; width: 100%; pointer-events: none;">
            <i class="ph ${currentDriverInfo.icon}"></i>
            <span class="method-name" style="font-size: 1.1rem; margin-top: 4px;">${currentDriverInfo.method}</span>
          </div>
        </div>

        <div class="form-group">
          <label>5. 送迎頻度の指定</label>
          <div class="frequency-toggle">
            <button type="button" class="${state.requestForm.frequency === 'once' ? 'active' : ''}" onclick="changeFrequency('once')">都度 (単発)</button>
            <button type="button" class="${state.requestForm.frequency === 'weekly' ? 'active' : ''}" onclick="changeFrequency('weekly')">週単位 (曜日)</button>
            <button type="button" class="${state.requestForm.frequency === 'monthly' ? 'active' : ''}" onclick="changeFrequency('monthly')">月単位 (まとめ)</button>
          </div>
        </div>

        ${state.requestForm.frequency === 'once' ? `
          <div class="form-group fade-in">
            <label>6. 送迎日の指定（カレンダーから1日選択）</label>
            <div class="calendar-container" style="margin-bottom:16px;">
              <div class="calendar-header">
                <span>2026年 8月</span>
                <span style="font-size:0.75rem; font-weight:normal; color:var(--text-muted);">単発の日付をタップして選択してください</span>
              </div>
              <div class="calendar-grid">
                ${['日', '月', '火', '水', '木', '金', '土'].map(w => `<div class="calendar-weekday">${w}</div>`).join('')}
                ${Array(6).fill(0).map(() => `<div class="calendar-day muted"></div>`).join('')}
                ${Array(31).fill(0).map((_, i) => {
                  const dayVal = i + 1;
                  const isActive = state.requestForm.onceDate === dayVal;
                  return `<div class="calendar-day ${isActive ? 'active' : ''}" onclick="selectOnceDay(${dayVal})">${dayVal}</div>`;
                }).join('')}
                ${Array(5).fill(0).map(() => `<div class="calendar-day muted"></div>`).join('')}
              </div>
            </div>
            
            <label>7. 送迎時間の指定（都度）</label>
            <div style="display:flex; gap:12px; margin-bottom:12px;">
              <button type="button" class="btn ${state.requestForm.timeType === 'Morning' ? 'btn-primary' : 'btn-outline'}" onclick="selectTimeType('Morning')">朝 (送り)</button>
              <button type="button" class="btn ${state.requestForm.timeType === 'Evening' ? 'btn-primary' : 'btn-outline'}" onclick="selectTimeType('Evening')">夕 (迎え)</button>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-weight:500; font-size:0.9rem; color:var(--text-main);">指定時間:</span>
              <input type="time" class="form-control" style="width: auto; flex:1;" value="${state.requestForm.specificTime}" onchange="updateSpecificTime(this.value)">
            </div>
          </div>
        ` : ''}

        ${state.requestForm.frequency === 'weekly' ? `
          <div class="form-group fade-in">
            <label>6. 送迎曜日の選択（週単位繰り返し）</label>
            <p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:8px;">
              毎週指定された曜日に定期的に送迎を行います（4週間換算で見積もり）。
            </p>
            <div class="day-selector" style="margin-bottom:16px;">
              ${['月', '火', 'w', '木', '金', '土', '日'].map((day, i) => {
                const dayVal = i + 1; // 1:月 〜 7:日
                const isActive = state.requestForm.weeklyDays.includes(dayVal);
                const dispDay = day === 'w' ? '水' : day;
                return `<button type="button" class="day-btn ${isActive ? 'active' : ''}" onclick="toggleWeeklyDay(${dayVal})">${dispDay}</button>`;
              }).join('')}
            </div>

            <!-- 自動ハイライト用カレンダー (クリック可能) -->
            <div class="calendar-container" style="margin-bottom:16px;">
              <div class="calendar-header">
                <span>2026年 8月 送迎日程（プレビュー）</span>
                <span style="font-size:0.75rem; font-weight:normal; color:var(--text-muted);">カレンダーの日付タップでも曜日を選択できます</span>
              </div>
              <div class="calendar-grid">
                ${['日', '月', '火', '水', '木', '金', '土'].map(w => `<div class="calendar-weekday">${w}</div>`).join('')}
                ${Array(6).fill(0).map(() => `<div class="calendar-day muted"></div>`).join('')}
                ${Array(31).fill(0).map((_, i) => {
                  const dayVal = i + 1;
                  const w = (dayVal + 5) % 7;
                  const dayOfWeekVal = w === 0 ? 7 : w; // 1:月〜7:日
                  const isActive = state.requestForm.weeklyDays.includes(dayOfWeekVal);
                  const selectedClass = isActive ? 'day-parent-selected' : '';
                  return `<div class="calendar-day ${selectedClass}" onclick="toggleWeeklyDay(${dayOfWeekVal})">${dayVal}</div>`;
                }).join('')}
                ${Array(5).fill(0).map(() => `<div class="calendar-day muted"></div>`).join('')}
              </div>
            </div>

            <div style="display:flex; gap:12px; margin-top:16px; margin-bottom:12px;">
              <button type="button" class="btn ${state.requestForm.timeType === 'Morning' ? 'btn-primary' : 'btn-outline'}" onclick="selectTimeType('Morning')">朝 (送り)</button>
              <button type="button" class="btn ${state.requestForm.timeType === 'Evening' ? 'btn-primary' : 'btn-outline'}" onclick="selectTimeType('Evening')">夕 (迎え)</button>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-weight:500; font-size:0.9rem; color:var(--text-main);">指定時間:</span>
              <input type="time" class="form-control" style="width: auto; flex:1;" value="${state.requestForm.specificTime}" onchange="updateSpecificTime(this.value)">
            </div>
          </div>
        ` : ''}

        ${state.requestForm.frequency === 'monthly' ? `
          <div class="form-group fade-in">
            <label>6. 月単位プランの選択</label>
            <div class="frequency-toggle" style="margin-bottom: 12px;">
              <button type="button" class="${state.requestForm.monthlyType === 'dates' ? 'active' : ''}" onclick="changeMonthlyType('dates')">日付指定 (まとめ)</button>
              <button type="button" class="${state.requestForm.monthlyType === 'flat' ? 'active' : ''}" onclick="changeMonthlyType('flat')">安心月定額 (平日毎日)</button>
            </div>

            ${state.requestForm.monthlyType === 'dates' ? `
              <div class="fade-in">
                <p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:8px;">
                  カレンダーから希望する日付を選択してください。まとめ割（1回230円）が適用されます。
                </p>
                <div class="calendar-container">
                  <div class="calendar-header">
                    <span>2026年 8月</span>
                    <span style="font-size:0.75rem; font-weight:normal; color:var(--text-muted);">翌月分の一括登録</span>
                  </div>
                  <div class="calendar-grid">
                    ${['日', '月', '火', '水', '木', '金', '土'].map(w => `<div class="calendar-weekday">${w}</div>`).join('')}
                    <!-- 2026年8月1日は土曜日 -->
                    <!-- 前月分余白(6日間) -->
                    ${Array(6).fill(0).map(() => `<div class="calendar-day muted"></div>`).join('')}
                    <!-- 8月の日付(31日間) -->
                    ${Array(31).fill(0).map((_, i) => {
                      const dayVal = i + 1;
                      const isActive = state.requestForm.monthlyDays.includes(dayVal);
                      return `<div class="calendar-day ${isActive ? 'active' : ''}" onclick="toggleMonthlyDay(${dayVal})">${dayVal}</div>`;
                    }).join('')}
                    <!-- 翌月分余白(5日間) -->
                    ${Array(5).fill(0).map(() => `<div class="calendar-day muted"></div>`).join('')}
                  </div>
                </div>
              </div>
            ` : `
              <div class="card fade-in" style="background:#eef2ff; border-color:#c7d2fe; margin-top:12px; margin-bottom:12px; padding:12px 16px; box-shadow:none; cursor:default;">
                <p style="font-weight:700; color:#312e81; font-size:0.9rem; margin-top:0; margin-bottom:4px;"><i class="ph-fill ph-sparkle" style="color:var(--primary)"></i> 月額使い放題プラン (¥3,980)</p>
                <p style="font-size:0.8rem; color:#4338ca; margin-bottom:0; line-height:1.4;">
                  1ヶ月間の平日すべて（月20回程度）でお迎えまたはお送りを代行します。都度のご決済も不要になる大変便利でお得なプランです。
                </p>
              </div>

              <!-- 月定額用の平日毎日自動ハイライトカレンダー (表示専用) -->
              <div class="calendar-container fade-in" style="margin-bottom:16px; background-color:#fafafb; border-color:#e2e8f0;">
                <div class="calendar-header">
                  <span>2026年 8月 送迎日程（プレビュー）</span>
                  <span style="font-size:0.75rem; font-weight:normal; color:var(--text-muted);">平日（月〜金）がすべて対象日となります</span>
                </div>
                <div class="calendar-grid">
                  ${['日', '月', '火', '水', '木', '金', '土'].map(w => `<div class="calendar-weekday">${w}</div>`).join('')}
                  ${Array(6).fill(0).map(() => `<div class="calendar-day muted"></div>`).join('')}
                  ${Array(31).fill(0).map((_, i) => {
                    const dayVal = i + 1;
                    const w = (dayVal + 5) % 7;
                    const dayOfWeekVal = w === 0 ? 7 : w; // 1:月〜7:日
                    const isWeekday = dayOfWeekVal >= 1 && dayOfWeekVal <= 5;
                    const selectedClass = isWeekday ? 'day-parent-selected' : '';
                    return `<div class="calendar-day ${selectedClass}" style="cursor: default; pointer-events: none;">${dayVal}</div>`;
                  }).join('')}
                  ${Array(5).fill(0).map(() => `<div class="calendar-day muted"></div>`).join('')}
                </div>
              </div>
            `}

            <div style="display:flex; gap:12px; margin-top:16px; margin-bottom:12px;">
              <button type="button" class="btn ${state.requestForm.timeType === 'Morning' ? 'btn-primary' : 'btn-outline'}" onclick="selectTimeType('Morning')">朝 (送り)</button>
              <button type="button" class="btn ${state.requestForm.timeType === 'Evening' ? 'btn-primary' : 'btn-outline'}" onclick="selectTimeType('Evening')">夕 (迎え)</button>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-weight:500; font-size:0.9rem; color:var(--text-main);">指定時間:</span>
              <input type="time" class="form-control" style="width: auto; flex:1;" value="${state.requestForm.specificTime}" onchange="updateSpecificTime(this.value)">
            </div>
          </div>
        ` : ''}

        <!-- 料金見積もりカード -->
        ${!isFormValid() ? `
          <div class="estimation-card fade-in" style="display:flex; flex-direction:column; gap:8px; padding:16px; background:#f8fafc; border:1px dashed #cbd5e0; border-radius:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
              <div>
                <div class="estimation-title" style="color:var(--text-muted);">お見積もり合計額</div>
                <div style="font-size:0.75rem; color:var(--text-muted); margin-top:2px;">条件を選択すると計算されます</div>
              </div>
              <div class="estimation-value" style="text-align:right;">
                <div class="estimation-price" style="color:#94a3b8; font-size:1.6rem; font-weight:700;">¥ ---</div>
                <div style="font-size:0.7rem; color:#94a3b8; margin-top:2px;">(必要項目未選択)</div>
              </div>
            </div>
            
            <div style="border-top:1px dashed #e2e8f0; padding-top:8px; width:100%; font-size:0.75rem; color:var(--text-muted); text-align:center;">
              💡 1. 幼稚園・保育園、および 6. 送迎日 を選択すると、お見積もりが自動表示されます。
            </div>
          </div>
        ` : `
          <div class="estimation-card fade-in" style="display:flex; flex-direction:column; gap:8px; padding:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
              <div>
                <div class="estimation-title">お見積もり合計額</div>
                <div class="estimation-trips">
                  ${state.requestForm.frequency === 'once' ? '単発・都度送迎 (計1回)' : ''}
                  ${state.requestForm.frequency === 'weekly' ? `毎週 ${state.requestForm.weeklyDays.length}回指定 (4週分: 計${state.requestForm.estimatedTrips}回)` : ''}
                  ${state.requestForm.frequency === 'monthly' && state.requestForm.monthlyType === 'dates' ? `日付指定 (計${state.requestForm.estimatedTrips}回・まとめ割)` : ''}
                  ${state.requestForm.frequency === 'monthly' && state.requestForm.monthlyType === 'flat' ? `安心月定額 (平日使い放題プラン)` : ''}
                </div>
              </div>
              <div class="estimation-value" style="text-align:right;">
                <div class="estimation-price">¥${state.requestForm.estimatedPrice.toLocaleString()}</div>
                ${state.requestForm.estimatedPoints > 0 ? `
                  <div style="font-size:0.85rem; font-weight:700; color:var(--secondary); margin-top:2px;">+ ${state.requestForm.estimatedPoints.toLocaleString()} pt</div>
                ` : ''}
                <div style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">(実費＋維持管理料込)</div>
              </div>
            </div>
            
            <!-- 料金詳細内訳の表示 -->
            <div style="border-top:1px dashed #e2e8f0; padding-top:8px; width:100%; font-size:0.75rem; color:var(--text-muted); display:flex; flex-direction:column; gap:4px;">
              <div style="display:flex; justify-content:space-between;">
                <span>送迎手段:</span>
                <strong style="color:var(--text-main);">${currentDriverInfo.method}</strong>
              </div>
              ${isCar ? `
                <div style="display:flex; justify-content:space-between;">
                  <span>片道距離 (直線換算):</span>
                  <strong>約 ${state.requestForm.distanceKm || 2.5} km</strong>
                </div>
                <div style="display:flex; justify-content:space-between;">
                  <span>ガソリン代実費 (1回あたり):</span>
                  <strong>約 ¥${Math.round((state.requestForm.distanceKm || 2.5) * CONFIG.GAS_RATE_PER_KM)} <span style="font-size:0.7rem; font-weight:normal; color:var(--text-muted);">(${CONFIG.GAS_RATE_PER_KM}円/km)</span></strong>
                </div>
                <div style="display:flex; justify-content:space-between;">
                  <span>当法人手数料 (STEP1非徴収):</span>
                  <strong style="color:var(--primary);">¥0</strong>
                </div>
              ` : `
                <div style="display:flex; justify-content:space-between;">
                  <span>必要ポイント (1回あたり):</span>
                  <strong style="color:var(--secondary);">200 pt</strong>
                </div>
                <div style="display:flex; justify-content:space-between;">
                  <span>現金代金 (STEP1非発生):</span>
                  <strong style="color:var(--primary);">¥0</strong>
                </div>
              `}
            </div>
          </div>
        `}

        <button type="submit" class="btn btn-primary" style="margin-top:16px;">この内容で依頼する</button>
      </form>
    </main>
    ${renderBottomNav()}
  `;
}

window.submitPayment = function(event, method = 'クレジットカード') {
  if(event) event.preventDefault();
  const price = state.requestForm.estimatedPrice;
  showCustomAlert('決済完了', `【${method}】にて${price.toLocaleString()}円の決済が完了しました！送迎者とのマッチングを開始します。`, () => {
    state.requestForm.isBooked = true; // 予約完了フラグ
    navigate('active');
  });
};

function PaymentView() {
  const currentDriverInfo = driversList.find(d => d.name === state.requestForm.selectedDriver) || driversList[0];
  const method = state.requestForm.selectedDriver === 'おまかせ（自動マッチング）' ? 'おまかせ（自動割当）' : state.requestForm.selectedDriver;
  const price = state.requestForm.estimatedPrice;
  const points = state.requestForm.estimatedPoints;
  const trips = state.requestForm.estimatedTrips;
  const distance = state.requestForm.distanceKm || 2.5;
  
  // 移動手段の判定 (車・バイクか、徒歩・自転車か)
  const isCar = (currentDriverInfo.methodType === 'Car' || currentDriverInfo.methodType === 'Motorcycle' || currentDriverInfo.methodType === 'Unknown');
  
  let costItemBreakdown = '';
  let planLabel = '';
  
  // 2026年8月のカレンダーを生成 (1日は土曜日、前月分余白6日、当月31日、翌月分余白5日、計42マス)
  let calendarDaysHtml = '';
  for (let i = 0; i < 6; i++) {
    calendarDaysHtml += '<div class="calendar-day muted"></div>';
  }
  for (let d = 1; d <= 31; d++) {
    // 曜日を計算 (0:日、1:月、...、6:土)
    const w = (d + 5) % 7; 
    const dayOfWeekVal = w === 0 ? 7 : w; // 1:月〜7:日
    
    let isSelected = false;
    if (state.requestForm.frequency === 'once') {
      isSelected = (state.requestForm.onceDate === d);
    } else if (state.requestForm.frequency === 'weekly') {
      isSelected = state.requestForm.weeklyDays.includes(dayOfWeekVal);
    } else if (state.requestForm.frequency === 'monthly') {
      if (state.requestForm.monthlyType === 'dates') {
        isSelected = state.requestForm.monthlyDays.includes(d);
      } else {
        // 平日のみ
        isSelected = (dayOfWeekVal >= 1 && dayOfWeekVal <= 5);
      }
    }
    
    const selectedClass = isSelected ? 'day-parent-selected' : '';
    calendarDaysHtml += `<div class="calendar-day ${selectedClass}" style="cursor: default; pointer-events: none;">${d}</div>`;
  }
  for (let i = 0; i < 5; i++) {
    calendarDaysHtml += '<div class="calendar-day muted"></div>';
  }
  
  if (state.requestForm.frequency === 'once') {
    planLabel = state.requestForm.onceDate ? `単発・都度送迎（8月${state.requestForm.onceDate}日・計1回分）` : '単発・都度送迎（計1回分）';
    if (isCar) {
      const gasFee = Math.round(distance * 20);
      costItemBreakdown = `
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
          <span>送迎パートナー受領実費 (ガソリン代/1km20円)</span>
          <span style="font-weight:600;">¥${gasFee}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem; color:var(--text-muted);">
          <span>KidsRide 個別送迎手数料 (STEP1非徴収)</span>
          <span style="font-weight:600; color:var(--primary);">¥0</span>
        </div>
      `;
    } else {
      costItemBreakdown = `
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
          <span>必要ポイント (相互扶助)</span>
          <span style="font-weight:600; color:var(--secondary);">200 pt</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem; color:var(--text-muted);">
          <span>現金金銭のお支払い (STEP1非発生)</span>
          <span style="font-weight:600; color:var(--primary);">¥0</span>
        </div>
      `;
    }
  } else if (state.requestForm.frequency === 'weekly') {
    const dayNames = ['月', '火', '水', '木', '金', '土', '日'];
    const selectedDays = state.requestForm.weeklyDays.map(d => dayNames[d - 1]).join('・');
    planLabel = `週単位繰り返し [毎週 ${selectedDays}]（4週分・計${trips}回）`;
    
    if (isCar) {
      const gasFee = Math.round(distance * 20) * trips;
      costItemBreakdown = `
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
          <span>送迎パートナー受領実費 (¥${Math.round(distance * 20)} × ${trips}回)</span>
          <span style="font-weight:600;">¥${gasFee.toLocaleString()}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem; color:var(--text-muted);">
          <span>KidsRide 個別送迎手数料 (STEP1非徴収)</span>
          <span style="font-weight:600; color:var(--primary);">¥0</span>
        </div>
      `;
    } else {
      costItemBreakdown = `
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
          <span>必要ポイント (200pt × ${trips}回)</span>
          <span style="font-weight:600; color:var(--secondary);">${(200 * trips).toLocaleString()} pt</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem; color:var(--text-muted);">
          <span>現金金銭のお支払い (STEP1非発生)</span>
          <span style="font-weight:600; color:var(--primary);">¥0</span>
        </div>
      `;
    }
  } else if (state.requestForm.frequency === 'monthly') {
    if (state.requestForm.monthlyType === 'dates') {
      planLabel = `月単位日付指定（8月分・計${trips}回・まとめ割）`;
      if (isCar) {
        const gasFee = Math.round(distance * 20) * trips;
        costItemBreakdown = `
          <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
            <span>送迎パートナー受領実費 (¥${Math.round(distance * 20)} × ${trips}回)</span>
            <span style="font-weight:600;">¥${gasFee.toLocaleString()}</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem; color:var(--text-muted);">
            <span>KidsRide 個別送迎手数料 (STEP1非徴収)</span>
            <span style="font-weight:600; color:var(--primary);">¥0</span>
          </div>
        `;
      } else {
        costItemBreakdown = `
          <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
            <span>必要ポイント (200pt × ${trips}回)</span>
            <span style="font-weight:600; color:var(--secondary);">${(200 * trips).toLocaleString()} pt</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem; color:var(--text-muted);">
            <span>現金金銭のお支払い (STEP1非発生)</span>
            <span style="font-weight:600; color:var(--primary);">¥0</span>
          </div>
        `;
      }
    } else {
      planLabel = 'コミュニティ安心月額会員プラン';
      costItemBreakdown = `
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
          <span>月額コミュニティ安心会員費 (固定基本管理費)</span>
          <span style="font-weight:600;">¥1,000</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem; color:var(--text-muted);">
          <span>個別送迎ごとの当法人手数料</span>
          <span style="font-weight:600; color:var(--primary);">¥0 (完全無料)</span>
        </div>
      `;
    }
  }
  
  return `
    ${renderHeader('手数料決済と確認')}
    <main class="fade-in" style="padding-bottom: 20px;">
      <div class="card" style="margin-bottom: 24px; border: 2px solid var(--primary);">
        <h3 style="color:var(--primary); margin-top:0; text-align:center;">送迎料金のご確認</h3>
        <div style="font-size:2rem; font-weight:700; text-align:center; margin: 16px 0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:4px;">
          <div>¥${price.toLocaleString()}</div>
          ${points > 0 ? `
            <div style="font-size:1.1rem; color:var(--secondary); font-weight:700;">+ ${points.toLocaleString()} pt</div>
          ` : ''}
          <div style="font-size:0.8rem; font-weight:400; color:var(--text-muted); margin-top:4px;">
            ${state.requestForm.frequency === 'once' ? '/ 1回分' : '/ 期間合計'}
          </div>
        </div>
        
        <div style="background:#f8fafc; padding:16px; border-radius:8px; margin-bottom:16px; border: 1px solid var(--border);">
          <p style="font-weight:700; margin-top:0; margin-bottom:8px; font-size:0.95rem;">【料金の内訳】</p>
          ${costItemBreakdown}
          <hr style="border:none; border-top:1px dashed #ccc; margin:12px 0;">
          <div style="font-size:0.78rem; color:var(--text-muted); line-height:1.55; background:#edf2f7; padding:10px 12px; border-radius:6px; margin-top:8px;">
            <p style="margin-top:0; font-weight:700; color:var(--primary); margin-bottom:4px;">【STEP 1 実証実験期 法令遵守（コンプライアンス）のご案内】</p>
            <ul style="margin:0; padding-left:14px;">
              <li><strong>道路運送法</strong>: 個別送迎に紐づく当法人の手数料徴収はゼロ（¥0）です。車・バイクは純粋なガソリン代実費（20円/km）のみの精算であり、ドライバー利益は一切発生しません。</li>
              <li><strong>資金決済法</strong>: 個別送迎からの手数料天引きを行わない独立構造とし、関係省庁・行政機関への事前確認・検討を進めています。</li>
            </ul>
          </div>
        </div>

        <div style="font-size:0.9rem; line-height:1.6; background:#fffbf5; padding:12px; border-radius:8px; border:1px solid #fee7c8;">
          <strong>プラン:</strong> ${planLabel}<br>
          <strong>予定:</strong> ${state.requestForm.timeType === 'Morning' ? '朝' : '夕'} ${state.requestForm.specificTime}指定<br>
          <strong>対象施設:</strong> ${state.requestForm.kindergarten || '未選択'}<br>
          <strong>ご指名の送迎者:</strong> ${method}
        </div>

        <!-- 決済前の日程確認カレンダー -->
        <div style="border-top: 1px dashed var(--border); padding-top: 12px; margin-top: 16px;">
          <div style="font-size:0.8rem; font-weight:700; color:var(--text-main); margin-bottom:8px; display:flex; align-items:center; gap:4px;">
            <i class="ph ph-calendar-check" style="color:var(--primary);"></i> 8月の送迎予定カレンダー（最終確認）
          </div>
          <div class="calendar-container" style="padding: 8px; box-shadow: none; border-color: var(--border); background: #fafdfb; margin-top: 4px;">
            <div class="calendar-grid">
              ${['日', '月', '火', '水', '木', '金', '土'].map(w => `<div class="calendar-weekday" style="font-size:0.7rem; padding-bottom:4px;">${w}</div>`).join('')}
              ${calendarDaysHtml}
            </div>
          </div>
        </div>
      </div>

      <div class="card" style="margin-bottom: 24px;">
        <h3 style="margin-top:0; font-size:1.1rem; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">オンライン・QR決済</h3>
        <div style="display:flex; flex-direction:column; gap:12px; margin-top:16px;">
          <button type="button" class="btn" style="background:#000; color:#fff;" onclick="submitPayment(event, 'Apple Pay')">
            <i class="ph-fill ph-apple-logo"></i> Apple Pay で支払う
          </button>
          <button type="button" class="btn" style="background:#fff; color:#3c4043; border: 1px solid #dadce0;" onclick="submitPayment(event, 'Google Pay')">
            <i class="ph-fill ph-google-logo" style="color:#4285F4;"></i> Google Pay で支払う
          </button>
          <button type="button" class="btn" style="background:#E3003F; color:#fff; font-weight:900;" onclick="submitPayment(event, 'PayPay')">
            <span style="font-style:italic; margin-right:4px; font-size:1.2rem;">P</span> PayPay で支払う
          </button>
          <button type="button" class="btn" style="background:#06C755; color:#fff;" onclick="submitPayment(event, 'LINE Pay')">
            <i class="ph-fill ph-chat-circle"></i> LINE Pay で支払う
          </button>
        </div>
      </div>

      <div class="card" style="margin-bottom: 24px;">
        <h3 style="margin-top:0; font-size:1.1rem; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">銀行振込・その他</h3>
        <button type="button" class="btn btn-outline" style="border-color:#555; color:#555; margin-top:12px;" onclick="submitPayment(event, '銀行振込')">
          <i class="ph ph-bank"></i> 銀行振込で支払う（後払い）
        </button>
      </div>

      <form onsubmit="submitPayment(event, 'クレジットカード')" class="card">
        <h3 style="margin-top:0; font-size:1.1rem; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">クレジットカード決済</h3>
        
        <div class="form-group">
          <label>カード番号</label>
          <input type="text" class="form-control" placeholder="0000 0000 0000 0000">
        </div>
        
        <div style="display:flex; gap:16px;">
          <div class="form-group" style="flex:1;">
            <label>有効期限</label>
            <input type="text" class="form-control" placeholder="MM/YY">
          </div>
          <div class="form-group" style="flex:1;">
            <label>CVC</label>
            <input type="text" class="form-control" placeholder="123">
          </div>
        </div>

        <button type="submit" class="btn btn-primary" style="margin-top:16px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:4px; padding: 12px 16px;">
          <span style="display:flex; align-items:center; gap:8px; font-weight:700;">
            <i class="ph ph-credit-card"></i> ¥${price.toLocaleString()} を支払って依頼を確定する
          </span>
          ${points > 0 ? `
            <span style="font-size:0.75rem; font-weight:600; color:rgba(255,255,255,0.9);">
              (および ${points.toLocaleString()} pt の消費)
            </span>
          ` : ''}
        </button>
        <button type="button" class="btn btn-outline" style="margin-top:8px;" onclick="navigate('request')">依頼内容を修正する</button>
      </form>
    </main>
    ${renderBottomNav()}
  `;
}

// 保護者画面の Leaflet マップ初期化関数
function initActiveRideMap() {
  setTimeout(() => {
    const mapEl = document.getElementById('map');
    if (!mapEl) return;
    
    const startCoord = coordinatesMap[state.requestForm.kindergarten] || coordinatesMap["三鷹市立大沢保育園"];
    const destCoord = coordinatesMap[state.requestForm.location] || coordinatesMap["自宅（デフォルト）"];
    
    if (window.leafletMap) {
      window.leafletMap.remove();
      window.leafletMap = null;
    }
    
    // マップインスタンスの生成
    const map = L.map('map').setView([startCoord.lat, startCoord.lng], 14);
    window.leafletMap = map;
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    
    // 出発地 (保育園) ピン
    L.marker([startCoord.lat, startCoord.lng], {
      icon: L.divIcon({
        className: 'map-pin-start',
        html: `<div style="background:var(--primary); color:white; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; border:2px solid white; box-shadow:var(--shadow-md);"><i class="ph ph-map-pin" style="font-size:1.2rem;"></i></div>`,
        iconSize: [30, 30],
        iconAnchor: [15, 15]
      })
    }).addTo(map).bindPopup('出発地: ' + (state.requestForm.kindergarten || '保育園'));
    
    // 目的地 (自宅) ピン
    L.marker([destCoord.lat, destCoord.lng], {
      icon: L.divIcon({
        className: 'map-pin-end',
        html: `<div style="background:#0284c7; color:white; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; border:2px solid white; box-shadow:var(--shadow-md);"><i class="ph ph-house" style="font-size:1.2rem;"></i></div>`,
        iconSize: [30, 30],
        iconAnchor: [15, 15]
      })
    }).addTo(map).bindPopup('目的地: ' + (state.requestForm.location || 'ご自宅'));
    
    // 送迎ルートと送迎者マーカー
    if (state.activeRide.status === 'riding' || state.activeRide.status === 'completed') {
      if (state.activeRide.routePoints && state.activeRide.routePoints.length > 0) {
        const latlngs = state.activeRide.routePoints.map(p => [p.lat, p.lng]);
        L.polyline(latlngs, { color: 'var(--primary)', weight: 4, opacity: 0.7, dashArray: '8, 8' }).addTo(map);
      }
      
      const curLoc = state.activeRide.currentLocation || startCoord;
      const selectedDriverName = state.requestForm.selectedDriver === 'おまかせ（自動マッチング）' ? '佐藤 カズヤ' : state.requestForm.selectedDriver;
      const driverInfo = driversList.find(d => d.name === selectedDriverName) || driversList[1];
      const isCar = (driverInfo.methodType === 'Car' || driverInfo.methodType === 'Motorcycle' || driverInfo.methodType === 'Unknown');
      
      const driverIcon = L.divIcon({
        className: 'map-pin-driver',
        html: `<div style="background:var(--secondary); color:white; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; border:3px solid white; box-shadow:var(--shadow-lg); animation: pulse 2s infinite;"><i class="ph-fill ${isCar ? 'ph-steering-wheel' : 'ph-bicycle'}" style="font-size:1.4rem;"></i></div>`,
        iconSize: [36, 36],
        iconAnchor: [18, 18]
      });
      
      window.driverMarker = L.marker([curLoc.lat, curLoc.lng], { icon: driverIcon }).addTo(map);
      window.driverMarker.bindPopup('送迎パートナー現在地').openPopup();
      
      map.fitBounds([[startCoord.lat, startCoord.lng], [destCoord.lat, destCoord.lng]], { padding: [50, 50] });
    } else {
      map.setView([startCoord.lat, startCoord.lng], 14);
    }
  }, 100);
}

function ActiveRideView() {
  const ride = state.activeRide;
  let statusBadge = '';
  let statusText = '';
  
  if (ride.status === 'idle') {
    statusBadge = '<span style="background:#f1f5f9; color:#475569; padding:4px 8px; border-radius:12px; font-size:0.8rem; font-weight:700;">待機中</span>';
    statusText = '送迎パートナーからの「送迎開始」を待っています。';
  } else if (ride.status === 'riding') {
    statusBadge = '<span style="background:#def7ec; color:var(--secondary); padding:4px 8px; border-radius:12px; font-size:0.8rem; font-weight:700; animation: pulse 2s infinite;">送迎中</span>';
    statusText = `目的地（ご自宅）へ移動中です。`;
  } else if (ride.status === 'completed') {
    statusBadge = '<span style="background:#e0f2fe; color:#0369a1; padding:4px 8px; border-radius:12px; font-size:0.8rem; font-weight:700;">送迎完了</span>';
    statusText = '無事に目的地に到着しました。送迎完了です。';
  }

  const selectedDriverName = state.requestForm.selectedDriver === 'おまかせ（自動マッチング）' ? '佐藤 カズヤ' : state.requestForm.selectedDriver;
  const driverInfo = driversList.find(d => d.name === selectedDriverName) || driversList[1];
  const distanceLeft = state.requestForm.distanceKm || 2.5;

  return `
    ${renderHeader('送迎ステータス')}
    <main class="fade-in" style="padding-bottom: 20px;">
      <!-- Realtime Leaflet Map -->
      <div style="position:relative; margin-bottom:16px;">
        <div id="map" style="width: 100%; height: 320px; border-radius: 12px; box-shadow: var(--shadow-sm); border:1px solid var(--border); z-index:1;"></div>
        
        <div class="map-overlay" style="z-index: 2; position: absolute; bottom: 12px; left: 12px; right: 12px; background: rgba(255,255,255,0.95); padding: 12px; border-radius: 8px; box-shadow: var(--shadow-md); display:flex; align-items:center; justify-content:space-between; gap:12px;">
          <div>
            <div style="display:flex; align-items:center; gap:8px;">
              <strong>ステータス:</strong> ${statusBadge}
            </div>
            <div style="font-size:0.8rem; color:var(--text-muted); margin-top:4px;" id="tracking-info-text">
              ${statusText}
            </div>
          </div>
          ${ride.status === 'riding' ? `
            <div style="text-align:right;">
              <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600; display:block;">残り距離</span>
              <strong style="color:var(--primary); font-size:1.1rem;" id="tracking-distance-left">${distanceLeft} km</strong>
            </div>
          ` : ''}
        </div>
      </div>

      <!-- Driver Info -->
      <div class="card" style="display:flex; align-items:center; gap:16px; margin-bottom:16px;">
        <img src="${driver.avatar}" alt="Driver" class="avatar" style="width:50px; height:50px;">
        <div style="flex:1;">
          <h3 style="margin:0;">${driverInfo.name}</h3>
          <div class="rating" style="font-size:0.9rem;">
            <i class="ph-fill ph-star"></i> ${driver.rating}
          </div>
          <div style="font-size:0.8rem; color:var(--text-muted);">移動手段: ${driverInfo.method}</div>
        </div>
        <button class="btn btn-outline" style="width:auto; padding:8px; border-radius:50%;" onclick="showCustomAlert('通話機能', '送迎パートナーへ発信します（デモ用）')"><i class="ph ph-phone"></i></button>
      </div>



      <!-- Chat UI -->
      <div class="chat-container">
        <div class="chat-messages">
          <div class="message received">
            もうすぐマンションの前に到着します。準備の方よろしくお願いします。
          </div>
          <div class="message sent">
            ありがとうございます！今エントランスに向かっています。
          </div>
        </div>
        <div class="chat-input-area">
          <input type="text" placeholder="メッセージを入力...">
          <button onclick="showCustomAlert('メッセージ送信', 'メッセージを送信しました（デモ用）')"><i class="ph ph-paper-plane-right"></i></button>
        </div>
      </div>
      
    </main>
    ${renderBottomNav()}
  `;
}

window.exportGasAuditCSV = function() {
  const logs = state.gasRateAuditLogs || [];
  let csv = '日時,参照ガソリン価格(円/L),実用燃費(km/L),算定単価(円/km),変更前単価(円/km),算出ロジック,ステータス,実行者\n';
  logs.forEach(l => {
    csv += `"${l.timestamp}",${l.gasPrice},${l.fuelEfficiency},${l.calculatedRate},${l.previousRate},"Math.floor(価格/15)","${l.status}","${l.operator}"\n`;
  });
  const blob = new Blob([new Uint8Array([0xEF, 0xBB, 0xBF]), csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `KidsRide_ガソリン実費単価_監査ログ_${new Date().toISOString().slice(0,10)}.csv`;
  link.click();
};

function AdminView() {
  return `
    ${renderHeader('管理者ダッシュボード')}
    <main class="fade-in" style="padding-top:20px;">
      <!-- ガソリン価格連動 実費単価設定 ＆ 監査ログ管理（東京運輸支局コンプライアンス適合） -->
      <div class="card" style="margin-bottom:24px; text-align:left; border-left:4px solid var(--primary);">
        <h3 style="color:var(--primary); margin-top:0; font-size:1.05rem; display:flex; align-items:center; gap:6px;">
          <i class="ph-fill ph-gas-pump"></i> ガソリン実費単価（円/km）改訂・管理
        </h3>
        <p style="font-size:0.8rem; color:var(--text-muted); line-height:1.45; margin-bottom:12px;">
          国交省・東京運輸支局の指示に基づき、参照ガソリン価格の変動に応じて実費単価を自動・手動で適正改訂します。過分な対価（白タクリスク）を発生させないため、計算式は一律 <strong>Math.floor（切り捨て）</strong> で固定されています。
        </p>

        <div style="background:#f8fafc; padding:12px; border-radius:8px; border:1px solid #e2e8f0; margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.85rem; font-weight:700; color:var(--text-main);">現在の参照ガソリン価格:</span>
            <span style="font-size:1.1rem; font-weight:700; color:var(--primary);">¥${CONFIG.GAS_PRICE_PER_LITER} / L</span>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.85rem; font-weight:700; color:var(--text-main);">適用中の実費単価 (算式: floor/15):</span>
            <span style="font-size:1.2rem; font-weight:800; color:var(--secondary);">¥${CONFIG.GAS_RATE_PER_KM} / km</span>
          </div>
          <div style="display:flex; gap:8px; margin-top:12px;">
            <input type="number" id="admin-gas-price-input" class="form-control" style="flex:2;" placeholder="例: 175 (円/L)" value="${CONFIG.GAS_PRICE_PER_LITER}">
            <button class="btn btn-primary" style="flex:1; padding:8px 12px; font-size:0.85rem;" onclick="updateGasPriceAndRate(document.getElementById('admin-gas-price-input').value)">単価を改訂</button>
          </div>
        </div>

        <h4 style="font-size:0.9rem; margin-bottom:8px; color:var(--text-main);">【東京運輸支局提示用 監査ログ（改訂履歴）】</h4>
        <div style="max-height:180px; overflow-y:auto; border:1px solid #cbd5e1; border-radius:6px; margin-bottom:12px;">
          <table style="width:100%; border-collapse:collapse; font-size:0.75rem; text-align:left;">
            <tr style="background:#f1f5f9; position:sticky; top:0;">
              <th style="padding:6px; border-bottom:1px solid #ccc;">日時</th>
              <th style="padding:6px; border-bottom:1px solid #ccc;">ガソリン価格</th>
              <th style="padding:6px; border-bottom:1px solid #ccc;">単価(floor)</th>
              <th style="padding:6px; border-bottom:1px solid #ccc;">ステータス</th>
            </tr>
            ${(state.gasRateAuditLogs || []).map(l => `
              <tr style="border-bottom:1px solid #eee;">
                <td style="padding:6px;">${l.timestamp}</td>
                <td style="padding:6px;">¥${l.gasPrice}/L</td>
                <td style="padding:6px; font-weight:700; color:var(--secondary);">¥${l.calculatedRate}/km</td>
                <td style="padding:6px; color:#166534;">${l.status}</td>
              </tr>
            `).join('')}
          </table>
        </div>
        <button class="btn btn-outline" style="width:100%; padding:8px; font-size:0.85rem;" onclick="exportGasAuditCSV()">
          <i class="ph ph-file-text"></i> 運輸支局提示用 監査ログ(CSV)をダウンロード
        </button>
      </div>

      <div class="card" style="text-align:center; margin-bottom:24px;">
        <h3 style="color:var(--primary); margin-top:8px;">登録者データの管理</h3>
        <p style="font-size:0.9rem; margin-bottom:24px;">システムに登録されている全ユーザー（保護者・送迎者）の情報をエクスポートできます。</p>
        <button class="btn btn-primary" onclick="exportCSV()">
          <i class="ph ph-download-simple"></i> ユーザー情報CSVをダウンロード
        </button>
      </div>

      <div style="text-align:center;">
        <button class="btn btn-outline" onclick="navigate('login')" style="width: auto; padding: 8px 24px;">ログイン画面へ戻る</button>
      </div>
    </main>
  `;
}

function FacilityAdminView() {
  return `
    ${renderHeader('【提携施設用】ダッシュボード')}
    <main class="fade-in" style="padding-top:20px; padding-bottom: 20px;">
      <div class="card" style="background: linear-gradient(135deg, #1d4ed8, #3b82f6); color: white; margin-bottom:24px;">
        <h2 style="color: white; font-size:1.1rem; margin-top:0;">三鷹市立大沢保育園 様</h2>
        <p style="color: rgba(255,255,255,0.9); margin-top:4px; font-size:0.9rem;">本日の送迎予定（システム管理）</p>
      </div>

      <div class="card" style="padding:0; overflow:hidden; border: 1px solid #e2e8f0;">
        <table style="width:100%; border-collapse:collapse; font-size:0.8rem; text-align:left;">
          <tr style="background:#f8fafc; border-bottom:1px solid #cbd5e1;">
            <th style="padding:12px 8px; font-weight:700; color:var(--text-main);">児童名</th>
            <th style="padding:12px 8px; font-weight:700; color:var(--text-main);">送迎者</th>
            <th style="padding:12px 8px; font-weight:700; color:var(--text-main);">予定</th>
            <th style="padding:12px 8px; font-weight:700; color:var(--text-main);">状況</th>
          </tr>
          <tr style="border-bottom:1px solid #e2e8f0;">
            <td style="padding:12px 8px; font-weight:600;">山田 太郎 (4歳)</td>
            <td style="padding:12px 8px;">高橋 ケンタ</td>
            <td style="padding:12px 8px;">17:00</td>
            <td style="padding:12px 8px;"><span style="background:#fef08a; color:#854d0e; padding:4px 6px; border-radius:12px; font-weight:700; display:inline-block; font-size:0.7rem;">迎車中</span></td>
          </tr>
          <tr style="border-bottom:1px solid #e2e8f0;">
            <td style="padding:12px 8px; font-weight:600;">鈴木 アリサ (3歳)</td>
            <td style="padding:12px 8px;">佐藤 カズヤ</td>
            <td style="padding:12px 8px;">17:30</td>
            <td style="padding:12px 8px;"><span style="background:#f1f5f9; color:#475569; padding:4px 6px; border-radius:12px; font-weight:700; display:inline-block; font-size:0.7rem;">待機中</span></td>
          </tr>
          <tr>
            <td style="padding:12px 8px; font-weight:600;">佐藤 健太 (6歳)</td>
            <td style="padding:12px 8px;">渡辺 ユウキ</td>
            <td style="padding:12px 8px;">16:00</td>
            <td style="padding:12px 8px;"><span style="background:#dcfce7; color:#166534; padding:4px 6px; border-radius:12px; font-weight:700; display:inline-block; font-size:0.7rem;">送迎完了</span></td>
          </tr>
        </table>
      </div>

      <div style="margin-top:24px; text-align:center;">
        <p style="font-size:0.75rem; color:var(--text-muted); margin-bottom:16px; line-height:1.5;">施設管理者様は、本日到着予定・出発予定の児童の状況や、担当送迎者が誰かという情報を一元管理することで、引き渡しのリスクを大幅に軽減できます。</p>
        <button class="btn btn-outline" onclick="navigate('login')" style="width:auto; padding: 8px 24px;">通常のログイン画面へ戻る</button>
      </div>
    </main>
  `;
}

function DriverVerificationView() {
  return `
    ${renderHeader('送迎者 審査・登録')}
    <main class="fade-in" style="padding-bottom:80px; padding-top:20px;">
      <div class="card" style="margin-bottom:24px;">
        <h3 style="color:var(--primary); margin-top:0; font-size:1.1rem;">本人確認書類の提出</h3>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px; line-height:1.5;">安心・安全なコミュニティ維持のため、ご本人の身分証（運転免許証やマイナンバーカード等）のアップロードをお願いいたします。</p>
        
        <div style="border: 2px dashed #cbd5e1; border-radius: 8px; padding: 32px 16px; text-align: center; background: #f8fafc; cursor:pointer;" onclick="alert('デバイスのカメラまたは写真フォルダが起動します（プロトタイプ）')">
          <i class="ph ph-camera" style="font-size: 2.5rem; color: #94a3b8; margin-bottom: 8px;"></i>
          <br>
          <span style="font-size: 0.9rem; font-weight: 600; color: var(--text-main);">書類を撮影または選択</span>
        </div>
      </div>

      <div class="card" style="margin-bottom:24px;">
        <h3 style="color:var(--primary); margin-top:0; font-size:1.1rem;">同一施設の在園確認書類の提出</h3>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px; line-height:1.5;">送迎者は依頼者と同一施設（保育園・幼稚園・学童等）に子どもを通わせる保護者に限定されます。在園証明書・連絡帳・保護者証などの画像をアップロードしてください。</p>
        
        <div style="border: 2px dashed #cbd5e1; border-radius: 8px; padding: 32px 16px; text-align: center; background: #f8fafc; cursor:pointer;" onclick="alert('デバイスのカメラまたは写真フォルダが起動します（プロトタイプ）')">
          <i class="ph ph-file-text" style="font-size: 2.5rem; color: #94a3b8; margin-bottom: 8px;"></i>
          <br>
          <span style="font-size: 0.9rem; font-weight: 600; color: var(--text-main);">在園確認書類を撮影または選択</span>
        </div>
      </div>

      <div class="card" style="margin-bottom:24px;">
        <h3 style="color:var(--primary); margin-top:0; font-size:1.1rem;">自撮り写真（プロフィール用）</h3>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px; line-height:1.5;">保護者の方に安心いただくため、お顔がはっきりわかる写真をご登録ください。</p>
        
        <div style="border: 2px dashed #cbd5e1; border-radius: 8px; padding: 32px 16px; text-align: center; background: #f8fafc; cursor:pointer;" onclick="alert('デバイスのカメラが起動します（プロトタイプ）')">
          <i class="ph ph-user-portrait" style="font-size: 2.5rem; color: #94a3b8; margin-bottom: 8px;"></i>
          <br>
          <span style="font-size: 0.9rem; font-weight: 600; color: var(--text-main);">顔写真を撮影</span>
        </div>
      </div>

      <button class="btn btn-primary" onclick="showCustomAlert('申請完了', '書類が提出されました。運営の審査が完了するまでしばらくお待ち下さい。', () => navigate('driver-dashboard'))">審査を申し込む処理へ（モック）</button>
      <div style="text-align:center; margin-top:16px;">
        <a href="#" onclick="navigate('profile')" style="color:var(--text-muted); font-size:0.9rem;">戻る</a>
      </div>
    </main>
    ${renderBottomNav()}
  `;
}

function DriverDashboardView() {
  const ride = state.activeRide;
  const isBooked = state.requestForm.isBooked;
  
  const selectedDriverName = state.requestForm.selectedDriver === 'おまかせ（自動マッチング）' ? '佐藤 カズヤ' : state.requestForm.selectedDriver;
  const isMe = (selectedDriverName === '佐藤 カズヤ'); // デモ用：自分が担当か判定
  
  let activeRideCardHtml = '';
  let estimationSummaryHtml = `
    <div style="font-size:2rem; font-weight:700; color:var(--text-main);">12<span style="font-size:1rem;"> 回</span></div>
    <div style="font-size:0.8rem; color:var(--text-muted); font-weight:600;">送迎完了</div>
  `;
  let earningsSummaryHtml = `
    <div style="font-size:2.2rem; font-weight:700; color:var(--primary);"><span style="font-size:1.2rem; font-weight:600;">¥</span>2,400</div>
    <div style="font-size:0.8rem; color:var(--text-muted); font-weight:600;">実費精算見込額</div>
  `;

  if (isBooked && isMe) {
    const isCar = (state.activeRide.transportMethod === 'Car' || state.requestForm.transportMethod === 'Motorcycle' || state.requestForm.transportMethod === 'Unknown');
    
    // 実費表示の更新
    if (ride.status === 'completed') {
      const addedGas = isCar ? Math.round((state.requestForm.distanceKm || 2.5) * 20) : 0;
      const totalGas = 2400 + addedGas;
      earningsSummaryHtml = `
        <div style="font-size:2.2rem; font-weight:700; color:var(--primary);"><span style="font-size:1.2rem; font-weight:600;">¥</span>${totalGas.toLocaleString()}</div>
        <div style="font-size:0.8rem; color:var(--text-muted); font-weight:600;">実費精算見込額 <span style="color:var(--secondary);">（+¥${addedGas} 反映済）</span></div>
      `;
      estimationSummaryHtml = `
        <div style="font-size:2rem; font-weight:700; color:var(--text-main);">13<span style="font-size:1rem;"> 回</span></div>
        <div style="font-size:0.8rem; color:var(--text-muted); font-weight:600;">送迎完了 <span style="color:var(--secondary);">（本日分 +1）</span></div>
      `;
    }

    let controlPanelHtml = '';
    if (ride.status === 'idle') {
      controlPanelHtml = `
        <p style="font-size:0.8rem; color:var(--text-muted); line-height:1.4; margin-top:8px;">
          ※「送迎開始」を押すと、保護者のアプリ画面にリアルタイムの位置追跡マップが公開され、GPS信号の送信が始まります。
        </p>
        <button class="btn btn-primary" onclick="window.startGpsSimulation()" style="margin-top:8px; display:flex; align-items:center; justify-content:center; gap:8px;">
          <i class="ph-fill ph-play-circle" style="font-size:1.2rem;"></i> 送迎を開始する（GPS配信開始）
        </button>
      `;
    } else if (ride.status === 'riding') {
      const progressPercent = ride.routePoints && ride.routePoints.length > 0 ? (ride.currentIndex / (ride.routePoints.length - 1)) * 100 : 0;
      const intervalSec = isCar ? 10 : 15;
      const remainingSteps = ride.routePoints ? ride.routePoints.length - 1 - ride.currentIndex : 0;
      const minutesLeft = Math.round(remainingSteps * (intervalSec / 6)) / 10;
      
      controlPanelHtml = `
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:12px; margin-top:8px; margin-bottom:12px; text-align:left;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.8rem; font-weight:700; color:#15803d; display:flex; align-items:center; gap:4px;">
              <span style="width:8px; height:8px; background:#22c55e; border-radius:50%; display:inline-block; animation:pulse 1s infinite;"></span>
              現在GPS信号を配信中
            </span>
            <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">
              電波強度: <span style="color:#22c55e;">●●● 良好</span>
            </span>
          </div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:6px;">
            送信間隔: <strong id="driver-interval-desc">${intervalSec}秒おき</strong> (${isCar ? '車ルート' : '徒歩・自転車ルート'})
          </div>
          
          <!-- 進捗プログレスバー -->
          <div style="width:100%; background:#e2e8f0; height:6px; border-radius:3px; overflow:hidden; margin-bottom:6px;">
            <div id="driver-progress-bar-fill" style="width:${progressPercent}%; background:var(--secondary); height:100%; transition: width 0.5s ease;"></div>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:var(--text-muted);">
            <span>出発地</span>
            <span id="driver-time-left">残り約 ${minutesLeft} 分</span>
            <span>目的地</span>
          </div>
        </div>
        
        <div style="display:flex; gap:8px;">
          <button class="btn btn-outline" style="flex:1; border-color:var(--danger); color:var(--danger);" onclick="window.stopGpsSimulation(true)">
            一時停止
          </button>
          <button class="btn btn-secondary" style="flex:2;" onclick="window.simulateGpsStep()">
            手動で進める (デモ用)
          </button>
        </div>
      `;
    } else if (ride.status === 'completed') {
      controlPanelHtml = `
        <div style="background:#e0f2fe; border:1px solid #bae6fd; border-radius:8px; padding:12px; margin-top:8px; text-align:center; color:#0369a1;">
          <i class="ph-fill ph-check-circle" style="font-size:1.8rem; margin-bottom:4px; display:block;"></i>
          <span style="font-size:0.85rem; font-weight:700;">本日の送迎は正常に完了しました</span>
          <p style="font-size:0.75rem; margin:4px 0 0 0; color:#075985;">ご協力ありがとうございました。実費精算残高が更新されました。</p>
        </div>
        <button class="btn btn-outline" onclick="window.resetGpsSimulation()" style="margin-top:12px;">
          ステータスをリセットする
        </button>
      `;
    }

    activeRideCardHtml = `
      <div class="card" style="margin-bottom:24px; border-left:4px solid var(--primary); box-shadow: var(--shadow-md);">
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">
          <span style="font-weight:700; color:var(--text-main);">本日 ${state.requestForm.specificTime} 予定</span>
          <span style="font-size:0.85rem; color:var(--text-muted); font-weight:700;">
            <i class="ph ${isCar ? 'ph-car' : 'ph-bicycle'}"></i> ${isCar ? '車送迎（ガソリン実費精算）' : '自転車・徒歩（ポイント互助）'}
          </span>
        </div>
        <div style="font-size:0.9rem; margin-bottom:6px; font-weight:600;"><i class="ph ph-map-pin" style="color:var(--primary)"></i> 発：${state.requestForm.kindergarten}</div>
        <div style="font-size:0.9rem; margin-bottom:12px;"><i class="ph ph-house" style="color:var(--text-muted)"></i> 着：${state.requestForm.location || 'ご自宅'}</div>
        
        <!-- GPS送信操作パネル -->
        <div style="border-top:1px dashed #e2e8f0; padding-top:12px; margin-top:8px;">
          ${controlPanelHtml}
        </div>
      </div>
    `;
  } else {
    activeRideCardHtml = `
      <div class="card" style="margin-bottom:24px; text-align:center; color:var(--text-muted); padding: 32px 16px;">
        <i class="ph ph-calendar-x" style="font-size:2rem; margin-bottom:8px; color:#94a3b8;"></i>
        <p style="font-size:0.85rem; margin:0;">現在アサインされている未完了の送迎依頼はありません。</p>
      </div>
    `;
  }

  return `
    ${renderHeader('【送迎者用】稼働・精算ダッシュボード')}
    <main class="fade-in" style="padding-bottom:80px; padding-top:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; padding: 0 8px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=driver_user" alt="Me" class="avatar" style="width:48px; height:48px; display:block;">
          <div>
            <div style="font-weight:700; font-size:1.1rem;">佐藤 カズヤ</div>
            <div style="font-size:0.75rem; color:var(--text-muted); margin-top:2px;"><i class="ph-fill ph-check-circle" style="color:#22c55e;"></i> 審査通過済 (三鷹地区)</div>
          </div>
        </div>
        <div>
          <span style="background:#dcfce7; color:#166534; padding:6px 12px; border-radius:16px; font-size:0.8rem; font-weight:700;">受託可能</span>
        </div>
      </div>

      <div class="card" style="margin-bottom:24px; text-align:center; border: 2px solid var(--primary); background: #fffaf0;">
        <p style="margin-top:0; font-size:0.95rem; font-weight:700; color:var(--primary);">今月の稼働サマリー（実費精算実績）</p>
        <div style="display:flex; justify-content:space-around; margin-top:16px; align-items:center;">
          <div>
            ${estimationSummaryHtml}
          </div>
          <div style="width:1px; background:#e2e8f0; height:40px;"></div>
          <div>
            ${earningsSummaryHtml}
          </div>
        </div>
        <div style="font-size:0.7rem; color:var(--text-muted); margin-top:16px; line-height:1.5; text-align:left; background:#f8fafc; padding:8px 12px; border-radius:6px; border:1px solid #e2e8f0;">
          ※ KidsRideはボランタリーな地域互助システムです。表示されている金額は「運送の対価（報酬）」ではなく、事前の合意に基づき計算されたガソリン代等の「実費精算分」となります。
        </div>
      </div>

      <!-- 振込受取銀行口座（収納代行用） -->
      <div class="card" style="margin-bottom:24px; padding:16px; background:#f8fafc; border:1px solid #cbd5e1;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div>
            <span style="font-size:0.75rem; color:var(--text-muted); display:block; font-weight:600;">実費受取 銀行口座 (Stripe Connect全自動送金)</span>
            <strong style="font-size:0.9rem; color:var(--text-main);">${state.driverBankAccount.bankName || '未登録'} ${state.driverBankAccount.branchName || ''} (${state.driverBankAccount.accountType || ''} ${state.driverBankAccount.accountNumber || ''})</strong>
          </div>
          <button class="btn btn-outline" style="width:auto; padding:6px 12px; font-size:0.8rem; border-color:var(--primary); color:var(--primary);" onclick="showBankAccountModal()">口座変更</button>
        </div>
        <div style="font-size:0.72rem; color:var(--text-muted); margin-top:6px;">
          名義: ${state.driverBankAccount.accountHolder || '未登録'} ※毎月末に受領実費が自動送金されます。
        </div>
      </div>

      <h3 style="font-size:1.1rem; margin-bottom:12px; padding-left:8px; display:flex; align-items:center; gap:8px;"><i class="ph-fill ph-car-profile" style="color:var(--primary)"></i> 未完了の送迎依頼</h3>
      ${activeRideCardHtml}

      <!-- 送迎者 稼働スケジュール設定用カレンダー -->
      <div class="card" style="margin-bottom:24px;">
        <h3 style="margin-top:0; font-size:1rem; border-bottom:1px solid #e2e8f0; padding-bottom:8px; display:flex; align-items:center; gap:8px;">
          <i class="ph ph-calendar-plus" style="color:var(--primary);"></i> 稼働スケジュールの設定（8月）
        </h3>
        <p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:12px; line-height:1.4;">
          送迎が可能な日（稼働可能日）をカレンダー上でタップして設定してください。
        </p>
        <div style="display:flex; gap:16px; margin-bottom:12px; font-size:0.75rem; justify-content:center;">
          <div style="display:flex; align-items:center; gap:4px;">
            <div style="width:14px; height:14px; background:rgba(16,185,129,0.1); border:1px solid var(--secondary); border-radius:4px;"></div>
            <span>稼働可能</span>
          </div>
          <div style="display:flex; align-items:center; gap:4px;">
            <div style="width:14px; height:14px; background:var(--primary); border-radius:4px; position:relative;">
              <span style="font-size:0.4rem; color:white; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);">★</span>
            </div>
            <span>送迎担当確定</span>
          </div>
          <div style="display:flex; align-items:center; gap:4px;">
            <div style="width:14px; height:14px; background:white; border:1px solid var(--border); border-radius:4px;"></div>
            <span>稼働不可・未設定</span>
          </div>
        </div>
        
        <div class="calendar-container" style="padding: 8px; box-shadow: none; margin-top: 4px;">
          <div class="calendar-grid">
            ${['日', '月', '火', '水', '木', '金', '土'].map(w => `<div class="calendar-weekday" style="font-size:0.7rem; padding-bottom:4px;">${w}</div>`).join('')}
            ${Array(6).fill(0).map(() => `<div class="calendar-day muted"></div>`).join('')}
            ${Array(31).fill(0).map((_, i) => {
              const dayVal = i + 1;
              const isAssigned = state.driverSchedule.assignedDays.includes(dayVal);
              const isAvailable = state.driverSchedule.availableDays.includes(dayVal);
              
              let dayClass = '';
              if (isAssigned) {
                dayClass = 'day-assigned';
              } else if (isAvailable) {
                dayClass = 'day-available';
              }
              
              return `<div class="calendar-day ${dayClass}" onclick="toggleDriverAvailability(${dayVal})">${dayVal}</div>`;
            }).join('')}
            ${Array(5).fill(0).map(() => `<div class="calendar-day muted"></div>`).join('')}
          </div>
        </div>
      </div>

      <div class="card" style="margin-bottom:24px;">
        <h3 style="margin-top:0; font-size:1rem; border-bottom:1px solid #e2e8f0; padding-bottom:8px;">実費振込先口座の設定</h3>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:16px;">
          <div style="font-size:0.9rem;">
            <div style="font-weight:600;">三菱UFJ銀行</div>
            <div style="color:var(--text-muted);">普通 123****</div>
          </div>
          <button class="btn btn-outline" style="width:auto; padding:6px 16px; font-size:0.8rem;" onclick="alert('口座情報の編集画面が立ち上がります')">変更</button>
        </div>
      </div>
    </main>
    ${renderBottomNav()}
  `;
}

function PasswordView() {
  return `
    <div style="min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; background-color: var(--bg-color);">
      <div class="card" style="width: 100%; max-width: 360px; text-align: center; box-shadow: var(--shadow-lg);">
        <div style="font-size: 3rem; color: var(--primary); margin-bottom: 16px;">
          <i class="ph-fill ph-lock-key"></i>
        </div>
        <h2 style="font-size: 1.3rem; margin-bottom: 8px; color: var(--text-main);">関係者専用アクセス</h2>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 24px; line-height: 1.5;">このサイトは開発中のデモ用プロトタイプです。閲覧するにはデモ用のパスコードを入力してください。</p>
        
        <form onsubmit="window.submitPassword(event)">
          <div class="form-group" style="text-align: left;">
            <label>パスコードを入力（デモ用: kidsride）</label>
            <input type="password" id="demo-passcode" class="form-control" placeholder="パスコードを入力" autofocus style="text-align: center;">
          </div>
          <button type="submit" class="btn btn-primary" style="margin-top: 8px;">閲覧を開始する</button>
        </form>
        <div id="passcode-error" style="color: var(--danger); font-size: 0.8rem; margin-top: 12px; display: none; font-weight: 600;">
          パスコードが正しくありません。
        </div>
      </div>
    </div>
  `;
}

window.submitPassword = function(event) {
  event.preventDefault();
  const input = document.getElementById('demo-passcode');
  const error = document.getElementById('passcode-error');
  if (input.value.trim().toLowerCase() === 'kidsride') {
    state.isAuthenticated = true;
    localStorage.setItem('kidsride_demo_auth', 'true');
    render();
  } else {
    error.style.display = 'block';
    input.value = '';
    input.focus();
  }
};

// App Entry Point
function render() {
  const appContainer = document.getElementById('app');
  


  switch(state.currentRoute) {
    case 'facility-admin':
      appContainer.innerHTML = FacilityAdminView();
      break;
    case 'payment':
      appContainer.innerHTML = PaymentView();
      break;
    case 'admin':
      appContainer.innerHTML = AdminView();
      break;
    case 'login':
      appContainer.innerHTML = AuthLoginView();
      break;
    case 'register':
      appContainer.innerHTML = RegisterView();
      break;
    case 'profile':
      appContainer.innerHTML = ProfileView();
      break;
    case 'dashboard':
      appContainer.innerHTML = DashboardView();
      break;
    case 'driver-verify':
      appContainer.innerHTML = DriverVerificationView();
      break;
    case 'driver-dashboard':
      appContainer.innerHTML = DriverDashboardView();
      break;
    case 'request':
      appContainer.innerHTML = RequestFormView();
      break;
    case 'active':
      appContainer.innerHTML = ActiveRideView();
      initActiveRideMap();
      break;
    default:
      appContainer.innerHTML = AuthLoginView();
  }
}

window.showPointChargeModal = function() {
  showCustomAlert(
    '相互扶助ポイント チャージ（購入）',
    '【1,000 pt パック（¥1,000）】\n・有効期限: 購入日より5ヶ月29日（6ヶ月未満・資金決済法非該当）\n・用途: 徒歩・自転車送迎の依頼時消費\n\n※デモ環境のため実際の発注決済は行われません。デモポイントが追加されました。'
  );
};

// Init
document.addEventListener('DOMContentLoaded', () => {
  render();
});
