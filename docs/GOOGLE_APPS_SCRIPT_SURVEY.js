/**
 * KidsRide 三鷹市保護者送迎アンケート回答 Googleスプレッドシート自動収集スクリプト
 * 
 * 【設定手順（所要時間：約1分）】
 * 1. お使いのGoogleアカウントで新規Googleスプレッドシート（名前例: 「三鷹市_送迎アンケート集計」）を作成
 * 2. メニューバーの「拡張機能」>「Apps Script」をクリック
 * 3. もともと書かれているコードをすべて消去し、このファイルのコードをすべて貼り付けて保存（Ctrl+S または Cmd+S）
 * 4. 画面右上の青い「デプロイ」ボタン >「新しいデプロイ」をクリック
 * 5. 種類の選択（歯車アイコン）をクリックし、「ウェブアプリ」を選択
 * 6. 次の2箇所を設定：
 *    - 次のユーザーとして実行: 「自分」
 *    - アクセスできるユーザー: 「全員」（※保護者がログイン不要で回答を保存できるようにするため）
 * 7. 「デプロイ」をクリックし、表示された「ウェブアプリのURL」をコピー
 * 8. KidsRide管理者画面（#admin）の「スプレッドシート連携設定」ボタンに貼り付けるだけで完全連動！
 */

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // ヘッダー行が存在しない（新規作成時）は自動作成・スタイリング
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "回答ID",
        "回答日時",
        "お子様の年齢(学年)",
        "普段の送迎手段",
        "第一希望園の断念有無(Q3)",
        "断念・迷った理由詳細(Q3付問)",
        "送迎の困りごと頻度(Q4)",
        "困るシチュエーション(Q5)",
        "過去の対処方法(Q6)",
        "助け合いサービス利用意向(Q7)",
        "のびのび広場(トワイライトステイ)送迎利用意向(Q8)",
        "安心できる送迎手段(Q9)",
        "ついで送迎サポーター関心(Q10)",
        "自由記述・ご要望(Q11)",
        "実証モニター希望メールアドレス(Q12)"
      ]);
      // ヘッダー行をKidsRideブルーで装飾
      var headerRange = sheet.getRange(1, 1, 1, 15);
      headerRange.setBackground("#0284c7");
      headerRange.setFontColor("#ffffff");
      headerRange.setFontWeight("bold");
      sheet.setFrozenRows(1);
    }
    
    var data = JSON.parse(e.postData.contents);
    
    // 1行追加（配列項目はカンマ区切りで展開）
    sheet.appendRow([
      data.id || ("SURVEY-" + Utilities.formatDate(new Date(), "JST", "yyyyMMdd-HHmmss")),
      data.submittedAt || Utilities.formatDate(new Date(), "JST", "yyyy/MM/dd HH:mm"),
      Array.isArray(data.childAges) ? data.childAges.join("、") : (data.childAges || ""),
      Array.isArray(data.transportMethods) ? data.transportMethods.join("、") : (data.transportMethods || ""),
      data.barrierToFirstChoice || "",
      data.barrierDetail || "",
      data.troubleFrequency || "",
      Array.isArray(data.troubleSituations) ? data.troubleSituations.join("、") : (data.troubleSituations || ""),
      Array.isArray(data.copingMethods) ? data.copingMethods.join("、") : (data.copingMethods || ""),
      data.mutualAidAcceptance || "",
      data.nobinobiStay || "",
      Array.isArray(data.safeTransportMethods) ? data.safeTransportMethods.join("、") : (data.safeTransportMethods || ""),
      data.supporterInterest || "",
      data.comments || "",
      data.email || ""
    ]);
    
    return ContentService.createTextOutput(JSON.stringify({ status: "success", id: data.id }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({ status: "ok", service: "KidsRide Survey GAS Webhook" }))
    .setMimeType(ContentService.MimeType.JSON);
}
