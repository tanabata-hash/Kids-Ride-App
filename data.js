const kindergartens = [
  "三鷹市立あゆみ保育園",
  "三鷹市立井の頭保育園",
  "三鷹市立大沢保育園",
  "三鷹市立上連雀保育園",
  "三鷹市立こじか保育園",
  "三鷹市立下連雀保育園",
  "三鷹市立新川保育園",
  "三鷹市立中原保育園",
  "三鷹市立野崎保育園",
  "三鷹市立深大寺保育園",
  "三鷹市立牟礼保育園",
  "三鷹台保育園",
  "三鷹みどり幼稚園",
  "三鷹若葉幼稚園",
  "三鷹双葉幼稚園",
  "明泉幼稚園",
  "春清学苑幼稚園",
  "牟礼幼稚園",
  "明星学園幼稚園",
  "のぞみ幼稚園",
  "グローバルキッズ武蔵境園",
  "椎の実子供の家",
  "みたか小鳥の森保育園",
  "どんぐり山保育園",
  "その他（自由記入）"
];

const driversList = [
  { name: "おまかせ（自動マッチング）", method: "未定（マッチング後に決定）", icon: "ph-question", methodType: "Unknown", kindergarten: "any" },
  { name: "佐藤 カズヤ", method: "車", icon: "ph-car", methodType: "Car", kindergarten: "三鷹市立牟礼保育園" },
  { name: "鈴木 アヤ", method: "自転車", icon: "ph-bicycle", methodType: "Bicycle", kindergarten: "明泉幼稚園" },
  { name: "高橋 ケンタ", method: "バイク", icon: "ph-motorcycle", methodType: "Motorcycle", kindergarten: "三鷹市立大沢保育園" },
  { name: "渡辺 ユウキ", method: "徒歩", icon: "ph-sneaker", methodType: "Walking", kindergarten: "三鷹市立上連雀保育園" }
];

const driver = {
  id: "d1",
  name: "佐藤 カズヤ",
  rating: 4.8,
  reviews: 124,
  vehicle: "TOYOTA Noah (Silver)",
  avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=driver1"
};

const currentUser = {
  id: "u1",
  name: "田中 マリ",
  rating: 4.9,
  reviews: 32,
  avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=user1"
};

const rideHistory = [
  { id: 1, date: "2026-04-10", type: "Morning", status: "Completed", location: "三鷹市立中原保育園", driver: "佐藤 カズヤ", rating: 4.8 },
  { id: 2, date: "2026-04-12", type: "Evening", status: "Completed", location: "三鷹市立上連雀保育園", driver: "鈴木 アヤ", rating: 4.6 },
];
