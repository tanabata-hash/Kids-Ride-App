/**
 * KidsRide 保護者送迎アンケート - Googleスプレッドシート自動連携スクリプト
 * 
 * 【設定手順（所要時間: 2分）】
 * 1. Googleドライブで新規「Googleスプレッドシート」を作成します。
 *    （シート名を「アンケート回答一覧」などに設定）
 * 2. 1行目に見出しを作成します（本スクリプトが自動で見出しを作成することも可能です）。
 * 3. 画面上部メニューの「拡張機能」 > 「Apps Script」をクリックします。
 * 4. エディタに表示されているコードをすべて消去し、このファイルのコードを貼り付けます。
 * 5. 画面右上の「デプロイ」青色ボタン > 「新しいデプロイ」をクリックします。
 * 6. 「種類の選択」の歯車アイコンをクリックし、「ウェブアプリ」を選択します。
 * 7. 次のように設定します:
 *    - 説明: KidsRide Survey Webhook
 *    - 次のユーザーとして実行: 自分（あなたのGoogleアカウント）
 *    - アクセスできるユーザー: 「全員」（※匿名でのアンケート回答送信を受け付けるため必須）
 * 8. 「デプロイ」をクリックし、「アクセスを承認」を許可します。
 * 9. 発行された「ウェブアプリのURL」（https://script.google.com/macros/s/.../exec）をコピーします。
 * 10. KidsRide管理画面（#admin）の「アンケート集計」タブにある「Googleスプレッドシート連携URL」欄に貼り付けて「保存」をクリックします。
 * 
 * これ以降、保護者様がアンケートを送信するたびに、リアルタイムでスプレッドシートに新しい行が自動追加されます！
 */

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // シートが空の場合は見出し行を自動生成
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "回答ID",
        "回答日時",
        "モニター希望メールアドレス",
        "お子様の学年・年齢",
        "通園先幼稚園・保育園",
        "普段の主な送迎手段",
        "第一希望園の断念経験",
        "断念理由の詳細",
        "送迎で困る頻度",
        "困るシチュエーション",
        "これまでの対処法",
        "助け合い送迎の利用意向",
        "のびのびひろば（ステイ）送迎意向",
        "安心できる送迎手段",
        "ついで送迎サポーター関心",
        "自由記述・ご意見",
        "受信タイムスタンプ"
      ]);
      
      // 見出し行の書式設定（KidsRideオレンジ＆太字）
      var headerRange = sheet.getRange(1, 1, 1, 17);
      headerRange.setBackground("#ea580c");
      headerRange.setFontColor("#ffffff");
      headerRange.setFontWeight("bold");
      sheet.setFrozenRows(1);
    }
    
    // 受信データの解析
    var data;
    if (e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    } else if (e.parameter) {
      data = e.parameter;
    } else {
      throw new Error("No data received");
    }
    
    // 一括送信（配列）または単一送信の判定
    var rowsToAdd = [];
    if (Array.isArray(data)) {
      data.forEach(function(item) {
        rowsToAdd.push(formatRow(item));
      });
    } else {
      rowsToAdd.push(formatRow(data));
    }
    
    rowsToAdd.forEach(function(row) {
      sheet.appendRow(row);
    });
    
    return ContentService
      .createTextOutput(JSON.stringify({ status: "success", count: rowsToAdd.length }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function formatRow(d) {
  return [
    d.id || "",
    d.submittedAt || new Date().toLocaleString("ja-JP"),
    d.email || "",
    Array.isArray(d.childAges) ? d.childAges.join(", ") : (d.childAges || ""),
    d.kindergarten || "",
    Array.isArray(d.transportMethods) ? d.transportMethods.join(", ") : (d.transportMethods || ""),
    d.barrierToFirstChoice || "",
    d.barrierDetail || "",
    d.troubleFrequency || "",
    Array.isArray(d.troubleSituations) ? d.troubleSituations.join(", ") : (d.troubleSituations || ""),
    Array.isArray(d.copingMethods) ? d.copingMethods.join(", ") : (d.copingMethods || ""),
    d.mutualAidAcceptance || "",
    d.nobinobiStay || "",
    Array.isArray(d.safeTransportMethods) ? d.safeTransportMethods.join(", ") : (d.safeTransportMethods || ""),
    d.supporterInterest || "",
    d.comments || "",
    new Date().toISOString()
  ];
}

// 接続確認テスト用 GET エンドポイント
function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: "ok", message: "KidsRide Survey Webhook is ACTIVE!" }))
    .setMimeType(ContentService.MimeType.JSON);
}
