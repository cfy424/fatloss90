#!/usr/bin/env node
/* 每天凌晨 1 点（北京时间）生成当天的训练与三餐数据，写入 today.json。
   由 GitHub Actions 定时执行：cron '0 17 * * *'（UTC）== 北京时间次日 01:00。 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DAY_MS = 86400000;
const CARB_LADDER = [2.5, 2.4, 2.2, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.5];

const CFG = {
  height: 164,
  age: 29,
  nextPeriod: "2026-09-15",
  cycleLen: 28,
  startDate: "2026-09-02",
};

const EXERCISES = {
  "下肢力量 A": [
    { name: "高脚杯深蹲", emoji: "🏋️", detail: "3 × 12-15", weight: "哑铃 6-8kg", tips: "脚跟踩稳，膝盖对准脚尖，核心收紧" },
    { name: "罗马尼亚硬拉", emoji: "🏋️", detail: "3 × 12", weight: "各 4-6kg", tips: "髋部后移、背部平直，腘绳肌有拉伸感" },
    { name: "负重臀桥", emoji: "🍑", detail: "3 × 12-15", weight: "6-10kg 放髋上", tips: "顶峰停顿 1-2 秒，臀部发力、别顶腰" },
    { name: "箭步蹲", emoji: "🦵", detail: "2 × 10/侧", weight: "各 3-5kg", tips: "前膝不过脚尖，重心垂直下放" },
    { name: "弹力带侧向走", emoji: "🩹", detail: "3 × 15", weight: "轻-中阻力", tips: "半蹲横向移动，感受臀中肌发力" },
    { name: "平板支撑", emoji: "🧱", detail: "3 × 30s", weight: "自重", tips: "身体一条直线，不要塌腰" },
  ],
  "上肢力量 B": [
    { name: "哑铃卧推", emoji: "🏋️", detail: "3 × 10-12", weight: "各 3-5kg", tips: "肩胛下沉，下放约 2 秒" },
    { name: "单臂哑铃划船", emoji: "💪", detail: "3 × 12/侧", weight: "6-8kg", tips: "背平直，肘贴近身体向后拉" },
    { name: "哑铃肩推", emoji: "🏋️", detail: "3 × 10-12", weight: "各 2-4kg", tips: "核心收紧，不塌腰" },
    { name: "弹力带面拉", emoji: "🩹", detail: "3 × 15-20", weight: "轻-中阻力", tips: "拉向面部，肩胛向后收" },
    { name: "二头弯举", emoji: "💪", detail: "2 × 12-15", weight: "各 2-3kg", tips: "肘部固定，身体不晃动" },
    { name: "跪姿俯卧撑", emoji: "🧱", detail: "2 × 8-12", weight: "自重", tips: "身体一条直线，胸口接近地面" },
  ],
  "动感单车 · 稳定": [
    { name: "动感单车", emoji: "🚴", detail: "30-40 分钟", weight: "中低阻力", tips: "强度调到“能说话但微喘”" },
  ],
  "动感单车 · 间歇": [
    { name: "动感单车间歇", emoji: "🚴", detail: "约 30 分钟", weight: "热身5min + 6-8轮（冲刺1min/恢复2min）+ 放松5min", tips: "冲刺用八成力，恢复期轻松踩" },
  ],
};

const MEALS = {
  "Day A": {
    kcal: "约 1455 kcal", protein: "蛋白质约 101g",
    items: [
      { name: "早餐", emoji: "🥣", detail: "燕麦 45g（约4平勺）+ 鸡蛋 2 个 + 无糖豆浆 250ml" },
      { name: "午餐", emoji: "🍚", detail: "米饭 140g（约一小拳）+ 鸡胸肉 150g（约一掌）+ 西兰花 250g（约两拳）+ 油 5g" },
      { name: "加餐", emoji: "🍎", detail: "苹果 1 个（约一拳）+ 无糖酸奶 60g（约半杯）" },
      { name: "晚餐", emoji: "🥗", detail: "米饭 120g + 鱼/虾仁 150g + 豆腐 120g（约半盒）+ 绿叶菜 250g + 油 5g" },
    ],
  },
  "Day B": {
    kcal: "约 1445 kcal", protein: "蛋白质约 96g",
    items: [
      { name: "早餐", emoji: "🍞", detail: "全麦吐司 2 片（约手掌大小）+ 鸡蛋 2 个 + 低脂牛奶 200ml" },
      { name: "午餐", emoji: "🥩", detail: "杂粮饭 140g（约一小拳）+ 瘦牛肉 120g（约扑克牌大小）+ 彩椒/黄瓜 250g + 油 5g" },
      { name: "加餐", emoji: "🍌", detail: "香蕉 1 根（约一拳）+ 原味坚果 8g（约一小把）" },
      { name: "晚餐", emoji: "🍠", detail: "红薯 170g（约一拳）+ 去皮鸡腿肉 130g（约一掌）+ 大叶菜 250g + 油 4g" },
    ],
  },
  "Day C": {
    kcal: "约 1370 kcal", protein: "蛋白质约 95g",
    items: [
      { name: "早餐", emoji: "🥣", detail: "燕麦 40g（约4平勺）+ 全蛋 1 个 + 蛋白 2 个 + 无糖酸奶 100g" },
      { name: "午餐", emoji: "🐟", detail: "米饭 130g（约小拳少一点）+ 三文鱼/鲈鱼 150g（约一掌）+ 芦笋/西葫芦 250g + 油 4g" },
      { name: "加餐", emoji: "🫐", detail: "蓝莓/草莓 150g（约一拳）+ 原味坚果 8g（约一小把）" },
      { name: "晚餐", emoji: "🌽", detail: "玉米 180g（约一根）+ 瘦猪肉/鸡胸 120g（约一掌）+ 菠菜 300g 蒜炒 + 豆腐 100g + 油 4g" },
    ],
  },
};

const WEEK = [
  { day: "周一", type: "s", title: "下肢力量 A" },
  { day: "周二", type: "c", title: "动感单车 · 稳定" },
  { day: "周三", type: "s", title: "上肢力量 B" },
  { day: "周四", type: "c", title: "动感单车 · 间歇" },
  { day: "周五", type: "c", title: "动感单车 · 稳定" },
  { day: "周六", type: "c", title: "动感单车 · 稳定" },
  { day: "周日", type: "r", title: "休息日：散步 20-30 分钟 + 拉伸" },
];

const TIPS = [
  "今天喝够 2L 水，餐前喝一杯。",
  "每餐至少吃 15-20 分钟，先吃菜和肉再吃主食。",
  "起床排空后称体重，只看 10 天平均趋势。",
  "单车强度“能说话但不轻松”最合适。",
  "力量训练能做满上限次数就加 0.5-1kg。",
  "睡前 1 小时放下手机，睡够 7-8 小时。",
  "黄体期体重涨 1-2kg 大多是水分，别焦虑。",
];

function cnToday() {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Shanghai", year: "numeric", month: "2-digit", day: "2-digit",
  }).format(new Date());
  return parts;
}

function parseDate(s) { const a = s.split("-").map(Number); return new Date(a[0], a[1] - 1, a[2]); }
function addDays(d, n) { const x = new Date(d); x.setDate(x.getDate() + n); return x; }
function dayDiff(a, b) { return Math.round((parseDate(a) - parseDate(b)) / DAY_MS); }

function cycleInfo(dateStr) {
  const d = parseDate(dateStr);
  const np = parseDate(CFG.nextPeriod);
  let start = new Date(np);
  while (d < start) start = addDays(start, -CFG.cycleLen);
  const day = (Math.round((d - start) / DAY_MS) % CFG.cycleLen) + 1;
  let phase;
  if (day <= 6) phase = "经期";
  else if (day <= 15) phase = "卵泡期";
  else if (day <= 18) phase = "排卵期";
  else phase = "黄体期";
  return { day, phase };
}

function buildTraining(cyc, wd) {
  if (cyc.phase === "经期") {
    return { title: "经期轻活动", note: "经期模式：只做轻活动 —— 散步 / 拉伸 / 动感单车 20-25 分钟低强度，不安排力量训练。", items: [] };
  }
  if (wd.type === "r") {
    return { title: wd.title, note: wd.title, items: [] };
  }
  return { title: wd.title, note: null, items: EXERCISES[wd.title] || [] };
}

function readLatestWeight() {
  try {
    const raw = fs.readFileSync(path.join(__dirname, "weight.json"), "utf-8");
    const w = Number(JSON.parse(raw).weight);
    return Number.isFinite(w) && w > 0 ? w : 58;
  } catch (e) {
    return 58;
  }
}

function computeTargets(weight, idx, cyc) {
  const p = Math.round(weight * 1.8);
  const f = Math.round(weight * 0.9);
  let c = Math.max(100, Math.round(weight * CARB_LADDER[idx]));
  let kcal = p * 4 + f * 9 + c * 4;
  let note = "";
  if (cyc.phase === "经期") {
    c = Math.round(c * 1.14);
    kcal = Math.round(kcal * 1.09);
    note = "经期放宽";
  } else if (cyc.day >= 24) {
    c = Math.round(c * 1.1);
    kcal = Math.round(kcal * 1.04);
    note = "黄体期稍加";
  }
  return { kcal, protein: p, carbs: c, fat: f, note };
}

function main() {
  const date = cnToday();
  let dayIndex = dayDiff(date, CFG.startDate);
  if (dayIndex < 0) dayIndex = 0;
  if (dayIndex > 89) dayIndex = 89;
  const cyc = cycleInfo(date);
  const d = parseDate(date);
  const wd = WEEK[(d.getDay() + 6) % 7];
  const mealDay = ["Day A", "Day B", "Day C"][dayIndex % 3];
  const weight = readLatestWeight();
  const idx = Math.floor(dayIndex / 10);

  const payload = {
    date,
    generatedAt: new Date().toISOString(),
    dayIndex,
    cycleDay: cyc.day,
    phase: cyc.phase,
    weight,
    targets: computeTargets(weight, idx, cyc),
    training: buildTraining(cyc, wd),
    meal: { day: mealDay, ...MEALS[mealDay] },
    tip: TIPS[dayIndex % TIPS.length],
  };

  fs.writeFileSync(path.join(__dirname, "today.json"), JSON.stringify(payload, null, 2) + "\n", "utf-8");
  console.log("generated today.json for", date, "- weight", weight, "-", mealDay, "-", wd.title);
}

main();
