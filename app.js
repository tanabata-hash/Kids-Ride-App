// State management
const state = {
  currentRoute: 'login',
  isAuthenticated: localStorage.getItem('kidsride_demo_auth') === 'true',
  requestForm: {
    kindergarten: '',
    location: '',
    timeType: 'Morning',
    specificTime: '07:00',
    selectedDriver: 'おまかせ（自動マッチング）'
  }
};

// Router
function navigate(route) {
  state.currentRoute = route;
  render();
}

// Ensure navigate is globally available for inline event handlers if needed
window.navigate = navigate;

// Components
function renderHeader(title) {
  return `
    <header>
      <div class="brand">
        <i class="ph-fill ph-car-profile"></i>
        KidsRide
      </div>
    </header>
    <div style="background-color: #fee2e2; color: #991b1b; text-align: center; padding: 6px 12px; font-size: 0.75rem; font-weight: 700; border-bottom: 1px solid #fca5a5; display: flex; align-items: center; justify-content: center; gap: 6px;">
      <i class="ph-fill ph-warning" style="font-size: 1rem;"></i>
      <span>本サイトは開発中のデモプロトタイプです。実際の送迎や決済は行われません。</span>
    </div>
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
  
  alert('データベースに登録が完了しました！');
  navigate('profile');
};

window.exportCSV = function() {
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
    <main class="fade-in" style="display:flex; flex-direction:column; justify-content:center; padding-top:40px;">
      <div style="text-align:center; margin-bottom:24px;">
        <h2 style="color:var(--primary); font-size:1.5rem;">${greeting}</h2>
        <p style="font-size:0.9rem;">メールアドレスとパスワードを入力してください。</p>
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
    <main class="fade-in" style="display:flex; flex-direction:column; justify-content:center; padding-top:40px;">
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
        <div style="display:flex; justify-content:space-between; align-items:center; cursor:pointer;" onclick="navigate('driver-verify')">
          <span style="font-weight:600;"><i class="ph ph-identification-card" style="margin-right:8px;"></i>審査書類（免許・保険等）のアップロード</span>
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

  return `
    ${renderHeader('ホーム')}
    <main class="fade-in">
      <div class="card" style="background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: white;">
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
window.submitRequest = function(event) {
  event.preventDefault();
  const select = document.getElementById('kindergarten-select');
  const otherInput = document.getElementById('request-other-kg');
  const location = document.getElementById('location-input');
  
  if (select.value === 'その他（自由記入）' && otherInput && otherInput.value) {
    state.requestForm.kindergarten = otherInput.value + '（その他）';
  } else {
    state.requestForm.kindergarten = select.value;
  }
  state.requestForm.location = location.value;
  
  let matchedDriverInfo;
  let driverStr;
  
  if (state.requestForm.selectedDriver === 'おまかせ（自動マッチング）') {
    const match = driversList.find(d => d.kindergarten === state.requestForm.kindergarten);
    if (match) {
      matchedDriverInfo = match;
      driverStr = `${match.name}（自動割当）`;
    } else {
      matchedDriverInfo = driversList[1]; // fallback
      driverStr = `${matchedDriverInfo.name}（自動割当）`;
    }
  } else {
    matchedDriverInfo = driversList.find(d => d.name === state.requestForm.selectedDriver) || driversList[0];
    driverStr = matchedDriverInfo.name;
  }
  
  navigate('payment');
};

function RequestFormView() {
  const options = kindergartens.map(k => `<option value="${k}">${k}</option>`).join('');
  const currentDriverInfo = driversList.find(d => d.name === state.requestForm.selectedDriver) || driversList[0];
  
  return `
    ${renderHeader('送迎を依頼する')}
    <main class="fade-in">
      <form onsubmit="submitRequest(event)">
        <div class="form-group">
          <label>1. 三鷹市内の幼稚園・保育園を選択</label>
          <select id="kindergarten-select" class="form-control" onchange="window.toggleOtherInput(this, 'request-other-kg')">
            <option value="">選択してください</option>
            ${options}
          </select>
          <input type="text" id="request-other-kg" class="form-control" placeholder="施設名をご記入ください" style="display:none; margin-top:8px;">
        </div>

        <div class="form-group">
          <label>2. 待ち合わせ場所</label>
          <input type="text" id="location-input" class="form-control" placeholder="例: 自宅マンションエントランス" value="${state.requestForm.location}">
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
          <label>5. 送迎時間の指定</label>
          <div style="display:flex; gap:12px; margin-bottom:12px;">
            <button type="button" class="btn ${state.requestForm.timeType === 'Morning' ? 'btn-primary' : 'btn-outline'}" onclick="selectTimeType('Morning')">朝 (送り)</button>
            <button type="button" class="btn ${state.requestForm.timeType === 'Evening' ? 'btn-primary' : 'btn-outline'}" onclick="selectTimeType('Evening')">夕 (迎え)</button>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-weight:500; font-size:0.9rem; color:var(--text-main);">指定時間:</span>
            <input type="time" class="form-control" style="width: auto; flex:1;" value="${state.requestForm.specificTime}" onchange="updateSpecificTime(this.value)">
          </div>
        </div>

        <button type="submit" class="btn btn-primary" style="margin-top:16px;">この内容で依頼する</button>
      </form>
    </main>
    ${renderBottomNav()}
  `;
}

window.submitPayment = function(event, method = 'クレジットカード') {
  if(event) event.preventDefault();
  alert(`【${method}】にて250円の決済が完了しました！送迎者とのマッチングを開始します。`);
  navigate('active');
};

function PaymentView() {
  const method = state.requestForm.selectedDriver === 'おまかせ（自動マッチング）' ? 'おまかせ（自動割当）' : state.requestForm.selectedDriver;
  
  return `
    ${renderHeader('手数料決済と確認')}
    <main class="fade-in" style="padding-bottom: 20px;">
      <div class="card" style="margin-bottom: 24px; border: 2px solid var(--primary);">
        <h3 style="color:var(--primary); margin-top:0; text-align:center;">送迎料金のご確認</h3>
        <div style="font-size:2rem; font-weight:700; text-align:center; margin: 16px 0;">
          ¥250 <span style="font-size:1rem; font-weight:400; color:var(--text-muted);">/ 1回</span>
        </div>
        
        <div style="background:var(--background); padding:16px; border-radius:8px; margin-bottom:16px;">
          <p style="font-weight:700; margin-top:0; margin-bottom:8px;">【料金の内訳】</p>
          <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
            <span>実費相当額（ガソリン代等の実費）</span>
            <span style="font-weight:600;">¥200</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem; color:var(--text-muted);">
            <span>コミュニティ維持・安全管理料</span>
            <span>¥50</span>
          </div>
          <hr style="border:none; border-top:1px dashed #ccc; margin:12px 0;">
          <div style="font-size:0.8rem; color:var(--text-muted); line-height:1.5;">
            <p style="margin-top:0; font-weight:700; color:var(--primary); margin-bottom:4px;">【コミュニティ維持・安全管理料】</p>
            本サービスは、地域の助け合いを安全に行うためのプラットフォームです。利用料は、会員間の身元確認、24時間監視システム、専用保険の維持に充てられます。送迎協力者へは、過分な利益の発生しないガソリン代等の実費相当額のみが支払われます。
          </div>
        </div>

        <div style="font-size:0.9rem;">
          <strong>予定:</strong> ${state.requestForm.timeType === 'Morning' ? '朝' : '夕'} ${state.requestForm.specificTime}指定<br>
          <strong>対象施設:</strong> ${state.requestForm.kindergarten || '未選択'}<br>
          <strong>ご指名の送迎者:</strong> ${method}
        </div>
      </div>

      <div class="card" style="margin-bottom: 24px;">
        <h3 style="margin-top:0; font-size:1.1rem; border-bottom:1px solid var(--background); padding-bottom:8px;">オンライン・QR決済</h3>
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
        <h3 style="margin-top:0; font-size:1.1rem; border-bottom:1px solid var(--background); padding-bottom:8px;">銀行振込・その他</h3>
        <button type="button" class="btn btn-outline" style="border-color:#555; color:#555; margin-top:12px;" onclick="submitPayment(event, '銀行振込')">
          <i class="ph ph-bank"></i> 銀行振込で支払う（後払い）
        </button>
      </div>

      <form onsubmit="submitPayment(event, 'クレジットカード')" class="card">
        <h3 style="margin-top:0; font-size:1.1rem; border-bottom:1px solid var(--background); padding-bottom:8px;">クレジットカード決済</h3>
        
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

        <button type="submit" class="btn btn-primary" style="margin-top:16px; display:flex; align-items:center; justify-content:center; gap:8px;">
          <i class="ph ph-credit-card"></i> 250円を支払って依頼を確定する
        </button>
        <button type="button" class="btn btn-outline" style="margin-top:8px;" onclick="navigate('request')">依頼内容を修正する</button>
      </form>
    </main>
    ${renderBottomNav()}
  `;
}

function ActiveRideView() {
  return `
    ${renderHeader('送迎ステータス')}
    <main class="fade-in" style="padding-bottom: 20px;">
      <!-- Map Mock with Freemium Upsell -->
      <div class="map-mock" style="position:relative;">
        <div class="tracking-marker" style="filter: blur(2px);"></div>
        <div class="map-overlay">
          <div style="font-weight:700; font-size:1.1rem;">送迎中</div>
          <div style="font-size:0.9rem; opacity:0.9;">目的地まで約5分</div>
        </div>
        
        <!-- Freemium Overlay -->
        <div style="position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(255,255,255,0.75); display:flex; flex-direction:column; align-items:center; justify-content:center; padding:16px;">
          <i class="ph-fill ph-lock-key" style="font-size:2rem; color:var(--text-muted); margin-bottom:8px;"></i>
          <p style="font-size:0.85rem; font-weight:700; text-align:center; color:var(--text-main); margin-top:0; margin-bottom:4px;">無料版では出発・到着の通知のみご利用いただけます</p>
          <p style="font-size:0.7rem; text-align:center; color:var(--text-muted); margin-bottom:12px; line-height:1.4;">※「リアルタイムGPS追跡」と「ドラレコ映像のリアルタイム表示」を利用するには、有料見守りプランが必要です。</p>
          <button class="btn" style="background:var(--primary); color:white; width:auto; padding:8px 16px; font-size:0.8rem; box-shadow:0 4px 12px rgba(230,126,34,0.3);" onclick="alert('有料プランの登録画面へ推移します（プロトタイプ）')">
            月額500円「安心見守りパック」を試す
          </button>
        </div>
      </div>

      <!-- Driver Info -->
      <div class="card" style="display:flex; align-items:center; gap:16px;">
        <img src="${driver.avatar}" alt="Driver" class="avatar" style="width:50px; height:50px;">
        <div style="flex:1;">
          <h3 style="margin:0;">${driver.name}</h3>
          <div class="rating" style="font-size:0.9rem;">
            <i class="ph-fill ph-star"></i> ${driver.rating}
          </div>
          <div style="font-size:0.8rem; color:var(--text-muted);">${driver.vehicle}</div>
        </div>
        <button class="btn btn-outline" style="width:auto; padding:8px; border-radius:50%;"><i class="ph ph-phone"></i></button>
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
          <button><i class="ph ph-paper-plane-right"></i></button>
        </div>
      </div>
      
    </main>
    ${renderBottomNav()}
  `;
}

function AdminView() {
  return `
    ${renderHeader('管理者ダッシュボード')}
    <main class="fade-in" style="padding-top:40px;">
      <div class="card" style="text-align:center; margin-bottom:24px;">
        <h3 style="color:var(--primary); margin-top:8px;">登録者データの管理</h3>
        <p style="font-size:0.9rem; margin-bottom:24px;">システムに登録されている全ユーザー（保護者・送迎者）の情報をエクスポートできます。</p>
        <button class="btn btn-primary" onclick="exportCSV()">
          <i class="ph ph-download-simple"></i> CSVファイルをダウンロード
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
        <h3 style="color:var(--primary); margin-top:0; font-size:1.1rem;">自動車保険証券の提出（任意）</h3>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px; line-height:1.5;">自家用車での送迎を希望される場合は、対人・対物無制限の任意保険証券の画像をアップロードしてください。</p>
        
        <div style="border: 2px dashed #cbd5e1; border-radius: 8px; padding: 32px 16px; text-align: center; background: #f8fafc; cursor:pointer;" onclick="alert('デバイスのカメラまたは写真フォルダが起動します（プロトタイプ）')">
          <i class="ph ph-file-text" style="font-size: 2.5rem; color: #94a3b8; margin-bottom: 8px;"></i>
          <br>
          <span style="font-size: 0.9rem; font-weight: 600; color: var(--text-main);">保険証券を撮影または選択</span>
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

      <button class="btn btn-primary" onclick="alert('書類が提出されました。運営の審査が完了するまでしばらくお待ち下さい。'); navigate('driver-dashboard')">審査を申し込む処理へ（モック）</button>
      <div style="text-align:center; margin-top:16px;">
        <a href="#" onclick="navigate('profile')" style="color:var(--text-muted); font-size:0.9rem;">戻る</a>
      </div>
    </main>
    ${renderBottomNav()}
  `;
}

function DriverDashboardView() {
  return `
    ${renderHeader('【送迎者用】稼働・精算ダッシュボード')}
    <main class="fade-in" style="padding-bottom:80px; padding-top:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; padding: 0 8px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=driver_user" alt="Me" class="avatar" style="width:48px; height:48px; display:block;">
          <div>
            <div style="font-weight:700; font-size:1.1rem;">田中 マリ</div>
            <div style="font-size:0.75rem; color:var(--text-muted); margin-top:2px;"><i class="ph-fill ph-check-circle" style="color:#22c55e;"></i> 審査通過済 (自転車)</div>
          </div>
        </div>
        <div>
          <span style="background:#dcfce7; color:#166534; padding:6px 12px; border-radius:16px; font-size:0.8rem; font-weight:700;">受付中</span>
        </div>
      </div>

      <div class="card" style="margin-bottom:24px; text-align:center; border: 2px solid var(--primary); background: #fffaf0;">
        <p style="margin-top:0; font-size:0.95rem; font-weight:700; color:var(--primary);">今月の稼働サマリー（実費精算実績）</p>
        <div style="display:flex; justify-content:space-around; margin-top:16px; align-items:center;">
          <div>
            <div style="font-size:2rem; font-weight:700; color:var(--text-main);">12<span style="font-size:1rem;"> 回</span></div>
            <div style="font-size:0.8rem; color:var(--text-muted); font-weight:600;">送迎完了</div>
          </div>
          <div style="width:1px; background:#e2e8f0; height:40px;"></div>
          <div>
            <div style="font-size:2.2rem; font-weight:700; color:var(--primary);"><span style="font-size:1.2rem; font-weight:600;">¥</span>2,400</div>
            <div style="font-size:0.8rem; color:var(--text-muted); font-weight:600;">実費精算見込額</div>
          </div>
        </div>
        <div style="font-size:0.7rem; color:var(--text-muted); margin-top:16px; line-height:1.5; text-align:left; background:#f8fafc; padding:8px 12px; border-radius:6px; border:1px solid #e2e8f0;">
          ※ KidsRideはボランタリーな地域互助システムです。表示されている金額は「運送の対価（報酬）」ではなく、事前の合意に基づき計算されたガソリン代等の「実費精算分」となります。
        </div>
      </div>

      <h3 style="font-size:1.1rem; margin-bottom:12px; padding-left:8px; display:flex; align-items:center; gap:8px;"><i class="ph-fill ph-car-profile" style="color:var(--primary)"></i> 未完了の送迎依頼</h3>
      <div class="card" style="margin-bottom:24px; border-left:4px solid var(--primary);">
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">
          <span style="font-weight:700; color:var(--text-main);">本日 16:30 予定</span>
          <span style="font-size:0.85rem; color:var(--text-muted);"><i class="ph-fill ph-bicycle"></i> 自転車利用</span>
        </div>
        <div style="font-size:0.95rem; margin-bottom:6px; font-weight:600;"><i class="ph ph-map-pin" style="color:var(--primary)"></i> 迎：三鷹市立大沢保育園</div>
        <div style="font-size:0.95rem; margin-bottom:16px;"><i class="ph ph-house" style="color:var(--text-muted)"></i> 送：三鷹台マンション前</div>
        <button class="btn btn-primary" onclick="navigate('active')">送迎ステータスを開始する（モック）</button>
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
  
  // パスコード認証チェック
  if (!state.isAuthenticated) {
    appContainer.innerHTML = PasswordView();
    return;
  }

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
      break;
    default:
      appContainer.innerHTML = AuthLoginView();
  }
}

// Init
document.addEventListener('DOMContentLoaded', () => {
  render();
});
