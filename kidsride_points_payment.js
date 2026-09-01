/**
 * KidsRide ポイント購入・実費精算・換金上限バリデーション リファレンス実装
 * ============================================================================
 *
 * 対応ドキュメント：「KidsRide 料金体系 実装計画書 Ver.6」 3.1節・3.2節・6章
 *
 * 位置づけ
 * --------
 * 本ファイルは既存サイト（app.js等）のソースコードを前提としない、独立した
 * リファレンス実装です。実装計画書の設計方針・データモデル・バリデーション
 * ロジックを、そのまま呼び出し可能な関数として提供します。
 * 開発チームは、この中の関数（またはロジック）を既存の
 * 「ポイント購入（チャージ）」機能・実費精算フローに組み込んでください。
 *
 * 実装している法的ガードレール
 * -----------------------------
 * 1. 徒歩・自転車（walk/cycle）：送迎者が受け取るのは常にポイントのみ。
 *    ポイント→現金の換金・出金は、依頼者の購入有無に関わらず一切不可
 *    （points.cash_convertible = false 固定）。
 * 2. 車・バイク（car/bike）：依頼者は現金またはポイントで実費を精算できる。
 *    送迎者が受け取ったポイントを換金する場合、換金額は当該送迎
 *    （または換金対象とする複数送迎の合計）の実費相当額
 *    （ride.actual_cost_amount の合計）を超えてはならない。
 * 3. KidsRideは、いずれの取引でも資金を保有・仲介しない
 *    （payment.payer_id → payment.payee_id は常に保護者→送迎者の直接関係）。
 * 4. 送迎ごとに紐づく形でKidsRideが収益を得るロジックは実装しない
 *    （system_fee は ride に直接ひもづけない）。
 *
 * 実行方法（自己テスト）： node kidsride_points_payment.js
 * ============================================================================
 */

"use strict";

// ----------------------------------------------------------------------------
// エラー型
// ----------------------------------------------------------------------------

class ComplianceError extends Error {
  constructor(message, code) {
    super(message);
    this.name = "ComplianceError";
    this.code = code;
  }
}

// ----------------------------------------------------------------------------
// 定数（実装計画書 6章 データモデルに対応）
// ----------------------------------------------------------------------------

const TransportType = Object.freeze({
  CAR: "car",
  BIKE: "bike",
  WALK: "walk",
  CYCLE: "cycle",
});

// 実費精算の対象になる移動手段（換金上限バリデーションが適用される側）
const ACTUAL_COST_TRANSPORT_TYPES = new Set([TransportType.CAR, TransportType.BIKE]);
// ポイントのみ・非換金の移動手段
const POINTS_ONLY_TRANSPORT_TYPES = new Set([TransportType.WALK, TransportType.CYCLE]);

const PaymentType = Object.freeze({
  ACTUAL_COST: "actual_cost",
  SYSTEM_FEE: "system_fee",
  COURTESY_FEE: "courtesy_fee",
});

const SettlementMethod = Object.freeze({
  DIRECT_CASH: "direct_cash",
  DIRECT_POINTS: "direct_points",
  PSP_SPLIT: "psp_split",
});

const PointsTransactionType = Object.freeze({
  EARN_NONMONETARY: "earn_nonmonetary", // 非金銭的行動による付与（紹介・コミュニティ活動等）
  PURCHASE: "purchase",                 // 依頼者による金銭でのポイント購入（Ver.5で追加）
  CONSUME: "consume",                   // 送迎依頼によるポイント消費
});

// ----------------------------------------------------------------------------
// 3.2節：徒歩・自転車 — ポイント購入・消費
// ----------------------------------------------------------------------------

/**
 * 依頼者によるポイント購入（徒歩・自転車／車・バイク共通で利用可）。
 * 購入されたポイントは非金銭的行動で得たポイントと同様に扱い、
 * 消費（送迎依頼）にのみ使用できる。払い戻し・換金APIはここでは提供しない。
 *
 * @param {{userId: string, amountJPY: number}} params
 * @returns {{transaction_type: string, amount_points: number, source: string}}
 */
function purchasePoints({ userId, amountJPY }) {
  if (!userId) throw new ComplianceError("userId is required", "MISSING_USER");
  if (!Number.isFinite(amountJPY) || amountJPY <= 0) {
    throw new ComplianceError("amountJPY must be a positive number", "INVALID_AMOUNT");
  }
  // 1ポイント = 1円 換算を仮定（実際のレートはサイト側の既存仕様に合わせる）
  return {
    transaction_type: PointsTransactionType.PURCHASE,
    amount_points: amountJPY,
    source: "money_purchase",
  };
}

/**
 * 徒歩・自転車送迎の完了に伴うポイント消費。
 * 送迎者は常にポイントのみを受け取り、現金化APIは提供しない
 * （points.cash_convertible = false を固定的に強制する）。
 *
 * @param {{transportType: string, requesterId: string, transporterId: string, pointsAmount: number}} params
 */
function settleWalkCycleRideWithPoints({ transportType, requesterId, transporterId, pointsAmount }) {
  assertPointsOnlyTransportType(transportType);
  if (!Number.isFinite(pointsAmount) || pointsAmount <= 0) {
    throw new ComplianceError("pointsAmount must be a positive number", "INVALID_AMOUNT");
  }
  return {
    payment: {
      payer_id: requesterId,
      payee_id: transporterId, // KidsRideはpayeeに含めない
      type: PaymentType.COURTESY_FEE,
      settlement_method: SettlementMethod.DIRECT_POINTS,
    },
    points: {
      transaction_type: PointsTransactionType.CONSUME,
      amount_points: pointsAmount,
      cash_convertible: false, // 常にfalse固定。呼び出し側で上書き不可
    },
  };
}

/**
 * 徒歩・自転車のポイント換金・出金は一切提供しない。
 * 呼び出された場合は必ず例外を投げる（実装上のガードレール）。
 */
function redeemWalkCyclePointsForCash() {
  throw new ComplianceError(
    "徒歩・自転車のポイントは換金できません（points.cash_convertible = false固定）。" +
      "現金報酬の導入はSTEP2以降、運輸支局への別途照会後に検討します。",
    "WALK_CYCLE_REDEMPTION_NOT_ALLOWED"
  );
}

// ----------------------------------------------------------------------------
// 3.1節：車・バイク — 実費精算（現金／ポイント）・換金上限バリデーション
// ----------------------------------------------------------------------------

/**
 * 車・バイク送迎の実費精算。現金またはポイントのいずれかで行える。
 * KidsRideは資金を保有・仲介しない（payer→payeeの直接関係を維持）。
 *
 * @param {{transportType: string, requesterId: string, driverId: string,
 *          actualCostAmount: number, method: "direct_cash"|"direct_points"|"psp_split"}} params
 */
function settleCarBikeActualCost({ transportType, requesterId, driverId, actualCostAmount, method }) {
  assertActualCostTransportType(transportType);
  if (!Number.isFinite(actualCostAmount) || actualCostAmount <= 0) {
    throw new ComplianceError("actualCostAmount must be a positive number", "INVALID_AMOUNT");
  }
  if (!Object.values(SettlementMethod).includes(method)) {
    throw new ComplianceError(`invalid settlement method: ${method}`, "INVALID_METHOD");
  }

  return {
    ride: { transport_type: transportType, actual_cost_amount: actualCostAmount },
    payment: {
      payer_id: requesterId,
      payee_id: driverId, // KidsRideはpayeeに含めない
      type: PaymentType.ACTUAL_COST, // system_fee等を合算しない
      settlement_method: method,
    },
  };
}

/**
 * 【重要】車・バイクの送迎者が受領したポイントを換金する場合の上限バリデーション。
 *
 * 実装計画書 Ver.6 6章 payment.point_redemption_cap の仕様：
 *   - 上限は「換金対象とする送迎（1回、または複数回まとめて換金する場合は
 *     その合計）の実費相当額（ride.actual_cost_amount の合計）」。
 *   - ガソリン代等の特定費目に限定されず、距離連動の実費全般を指す。
 *   - 実費相当額を「1円でも」超える換金は許可しない
 *     （超過は有償旅客運送に該当する可能性があるため）。
 *   - 徒歩・自転車（walk/cycle）にはこの関数は適用しない
 *     （そもそも換金自体を実装しないため。上のredeemWalkCyclePointsForCashを参照）。
 *
 * @param {{transporterId: string, redemptionAmountJPY: number, rides: Array<{rideId: string, transportType: string, actualCostAmount: number}>}} params
 * @returns {{approved: true, redemptionAmountJPY: number, capJPY: number}}
 * @throws {ComplianceError} 換金額が実費相当額の合計を超える場合、または対象rideに徒歩・自転車が含まれる場合
 */
function validateAndRedeemCarBikePoints({ transporterId, redemptionAmountJPY, rides }) {
  if (!transporterId) throw new ComplianceError("transporterId is required", "MISSING_USER");
  if (!Array.isArray(rides) || rides.length === 0) {
    throw new ComplianceError("rides must be a non-empty array", "MISSING_RIDES");
  }
  if (!Number.isFinite(redemptionAmountJPY) || redemptionAmountJPY <= 0) {
    throw new ComplianceError("redemptionAmountJPY must be a positive number", "INVALID_AMOUNT");
  }

  for (const ride of rides) {
    assertActualCostTransportType(ride.transportType); // walk/cycleが混入していたら例外
    if (!Number.isFinite(ride.actualCostAmount) || ride.actualCostAmount < 0) {
      throw new ComplianceError(`invalid actualCostAmount for ride ${ride.rideId}`, "INVALID_AMOUNT");
    }
  }

  const capJPY = rides.reduce((sum, ride) => sum + ride.actualCostAmount, 0);

  if (redemptionAmountJPY > capJPY) {
    throw new ComplianceError(
      `換金額（¥${redemptionAmountJPY}）が対象送迎の実費相当額合計（¥${capJPY}）を超えています。` +
        `実費相当額を超える換金は有償旅客運送に該当する可能性があるため許可できません。`,
      "REDEMPTION_EXCEEDS_ACTUAL_COST"
    );
  }

  return {
    approved: true,
    redemptionAmountJPY,
    capJPY,
    payment: {
      point_redemption_cap: capJPY,
    },
  };
}

// ----------------------------------------------------------------------------
// フィーチャーフラグ（3.4節）
// ----------------------------------------------------------------------------

const CURRENT_PHASE = "STEP1";

/**
 * STEP2以降のロジック（システム利用料の別建て請求、金銭謝礼など）は、
 * フラグがSTEP1の間は絶対に有効化しない。
 */
function assertStep1Only(featureName) {
  if (CURRENT_PHASE !== "STEP1") return;
  throw new ComplianceError(
    `${featureName} はSTEP2以降の機能です。current_phase="STEP1"の間は有効化できません。`,
    "STEP2_FEATURE_IN_STEP1"
  );
}

// ----------------------------------------------------------------------------
// 内部ヘルパー
// ----------------------------------------------------------------------------

function assertPointsOnlyTransportType(transportType) {
  if (!POINTS_ONLY_TRANSPORT_TYPES.has(transportType)) {
    throw new ComplianceError(
      `transportType "${transportType}" は徒歩・自転車向けの関数では扱えません`,
      "INVALID_TRANSPORT_TYPE"
    );
  }
}

function assertActualCostTransportType(transportType) {
  if (!ACTUAL_COST_TRANSPORT_TYPES.has(transportType)) {
    throw new ComplianceError(
      `transportType "${transportType}" は車・バイク向けの関数では扱えません` +
        `（徒歩・自転車は換金を実装しないため対象外です）`,
      "INVALID_TRANSPORT_TYPE"
    );
  }
}

module.exports = {
  ComplianceError,
  TransportType,
  PaymentType,
  SettlementMethod,
  PointsTransactionType,
  purchasePoints,
  settleWalkCycleRideWithPoints,
  redeemWalkCyclePointsForCash,
  settleCarBikeActualCost,
  validateAndRedeemCarBikePoints,
  assertStep1Only,
};

// ============================================================================
// 自己テスト（node kidsride_points_payment.js で実行）
// ============================================================================

if (require.main === module) {
  const assert = require("assert");
  let passed = 0;

  function test(name, fn) {
    try {
      fn();
      passed += 1;
      console.log(`OK   ${name}`);
    } catch (e) {
      console.error(`FAIL ${name}`);
      console.error(`     ${e.message}`);
      process.exitCode = 1;
    }
  }

  test("依頼者はポイントを金銭で購入できる（purchase種別が付与される）", () => {
    const result = purchasePoints({ userId: "parent_1", amountJPY: 1000 });
    assert.strictEqual(result.transaction_type, PointsTransactionType.PURCHASE);
    assert.strictEqual(result.amount_points, 1000);
  });

  test("徒歩送迎はポイント消費のみで完結し、cash_convertibleは常にfalse", () => {
    const result = settleWalkCycleRideWithPoints({
      transportType: TransportType.WALK,
      requesterId: "parent_1",
      transporterId: "volunteer_1",
      pointsAmount: 100,
    });
    assert.strictEqual(result.points.cash_convertible, false);
    assert.strictEqual(result.payment.payer_id, "parent_1");
    assert.strictEqual(result.payment.payee_id, "volunteer_1");
  });

  test("自転車送迎も同様に扱われる", () => {
    const result = settleWalkCycleRideWithPoints({
      transportType: TransportType.CYCLE,
      requesterId: "parent_1",
      transporterId: "volunteer_2",
      pointsAmount: 50,
    });
    assert.strictEqual(result.points.cash_convertible, false);
  });

  test("徒歩・自転車のポイント換金は常に拒否される", () => {
    assert.throws(() => redeemWalkCyclePointsForCash(), /換金できません/);
  });

  test("車の実費精算は現金・ポイントいずれでも可能", () => {
    const cash = settleCarBikeActualCost({
      transportType: TransportType.CAR,
      requesterId: "parent_1",
      driverId: "driver_1",
      actualCostAmount: 800,
      method: SettlementMethod.DIRECT_CASH,
    });
    assert.strictEqual(cash.payment.type, PaymentType.ACTUAL_COST);

    const points = settleCarBikeActualCost({
      transportType: TransportType.CAR,
      requesterId: "parent_1",
      driverId: "driver_1",
      actualCostAmount: 800,
      method: SettlementMethod.DIRECT_POINTS,
    });
    assert.strictEqual(points.payment.settlement_method, SettlementMethod.DIRECT_POINTS);
  });

  test("車・バイクのポイント換金は実費相当額の範囲内なら承認される", () => {
    const result = validateAndRedeemCarBikePoints({
      transporterId: "driver_1",
      redemptionAmountJPY: 800,
      rides: [{ rideId: "ride_1", transportType: TransportType.CAR, actualCostAmount: 800 }],
    });
    assert.strictEqual(result.approved, true);
    assert.strictEqual(result.capJPY, 800);
  });

  test("複数送迎をまとめて換金する場合は実費相当額の合計が上限になる", () => {
    const result = validateAndRedeemCarBikePoints({
      transporterId: "driver_1",
      redemptionAmountJPY: 1500,
      rides: [
        { rideId: "ride_1", transportType: TransportType.CAR, actualCostAmount: 800 },
        { rideId: "ride_2", transportType: TransportType.BIKE, actualCostAmount: 700 },
      ],
    });
    assert.strictEqual(result.capJPY, 1500);
  });

  test("実費相当額を1円でも超える換金は拒否される", () => {
    assert.throws(
      () =>
        validateAndRedeemCarBikePoints({
          transporterId: "driver_1",
          redemptionAmountJPY: 801,
          rides: [{ rideId: "ride_1", transportType: TransportType.CAR, actualCostAmount: 800 }],
        }),
      /実費相当額.*超えています/
    );
  });

  test("換金対象に徒歩・自転車のrideが混入していたら拒否される", () => {
    assert.throws(
      () =>
        validateAndRedeemCarBikePoints({
          transporterId: "driver_1",
          redemptionAmountJPY: 500,
          rides: [{ rideId: "ride_3", transportType: TransportType.WALK, actualCostAmount: 500 }],
        }),
      /徒歩・自転車は換金を実装しないため対象外/
    );
  });

  test("STEP1中はSTEP2機能（システム利用料別建て請求等）を有効化できない", () => {
    assert.throws(() => assertStep1Only("システム利用料の別建て請求"), /STEP2以降の機能/);
  });

  console.log(`\n${passed} tests passed.`);
}
