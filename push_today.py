#!/usr/bin/env python3
"""生成今日减脂安排文本，并可一键推送到飞书。

用法：
  python3 push_today.py              # 打印今天的内容
  python3 push_today.py --send       # 打印并推送到飞书
  python3 push_today.py --date 2026-09-15 --send   # 指定日期（测试用）
"""

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent

# ---- 周期推算（按 28 天周期，上次经期 8/18 开始、8/23 结束，下次经期预计 9/15）----
PREV_START = dt.date(2026, 8, 18)
NEXT_START = dt.date(2026, 9, 15)
CYCLE_DAYS = 28

WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

STRENGTH = {
    "周一": (
        "下肢力量 A",
        "高脚杯深蹲 3×12-15（哑铃6-8kg）｜罗马尼亚硬拉 3×12（各4-6kg）｜负重臀桥 3×12-15（6-10kg）｜箭步蹲 2×10/侧（各3-5kg）｜弹力带侧向走 3×15｜平板支撑 3×30s",
    ),
    "周四": (
        "上肢力量 B",
        "哑铃卧推 3×10-12（各3-5kg）｜单臂划船 3×12/侧（6-8kg）｜肩推 3×10-12（各2-4kg）｜弹力带面拉 3×15-20｜二头弯举 2×12-15（各2-3kg）｜跪姿俯卧撑 2×8-12",
    ),
}

SPIN_STEADY = "🚴 Keep C3 动感单车 35-40 分钟稳态燃脂：热身 8-10 挡(5min) ➔ 巡航 13-16 挡(踏频75-85,微出汗) ➔ 排酸冷身 6-8 挡(5min)"
SPIN_INTERVAL = "🚴 Keep C3 动感单车 30 分钟 HIIT：热身 8-10 挡(5min) ➔ 6-8 轮【冲刺 20-24 挡(1min,踏频95-110) + 恢复 8-10 挡(2min,踏频70-80)】➔ 冷身 6-8 挡(5min)"
REST_DAY = "休息日：散步 20-30 分钟 + 全身拉伸放松"
MENSTRUAL_LIGHT = "经期轻活动：散步 / 拉伸 / 动感单车 20-25 分钟低强度即可，不安排力量训练"

TIPS = [
    "今天喝够 2L 水，餐前喝一杯，帮助控制进食速度。",
    "吃饭慢一点，每餐至少 15-20 分钟，先吃菜和肉再吃主食。",
    "起床排空后称体重，记晨重，只看一周平均，别被单日波动吓到。",
    "动感单车强度调到“能说话但不轻松”，这个强度燃脂效率最高。",
    "力量训练记住渐进原则：能做完上限次数就下次加一点重量（0.5-1kg）。",
    "睡前 1 小时放下手机，保证 7-8 小时睡眠，睡不够会放大饥饿感。",
    "黄体期体重涨 1-2kg 大多是水分，别焦虑，正常执行计划。",
]


def load_meals():
    return json.loads((BASE / "meals.json").read_text(encoding="utf-8"))


def cycle_info(date: dt.date):
    if date >= NEXT_START:
        day = (date - NEXT_START).days % CYCLE_DAYS + 1
    else:
        day = (date - PREV_START).days % CYCLE_DAYS + 1
    if day <= 6:
        phase = f"经期第 {day} 天"
    elif day <= 15:
        phase = f"卵泡期（D{day}）"
    elif day <= 18:
        phase = f"排卵期（D{day}）"
    else:
        phase = f"黄体期（D{day}）"
    return day, phase


def build_message(date: dt.date, meals: dict) -> str:
    day, phase = cycle_info(date)
    weekday = WEEKDAY_CN[date.weekday()]
    offset = (date - dt.date(2026, 9, 2)).days % 3
    meal_day = ["Day A", "Day B", "Day C"][offset]
    meal = meals[meal_day]

    # 热量与碳水按周期弹性调整（蛋白质 105g / 脂肪 52g 不变）
    if day <= 6:  # 经期
        kcal, carbs, note = 1600, "165g", "经期不节食，重点补铁"
    elif day >= 24:  # 黄体后期
        kcal, carbs, note = 1530, "160g", "易饿是正常的，主食稍多一点，控盐"
    else:
        kcal, carbs, note = 1470, "145g", "正常执行碳水渐降"

    # 训练安排：周一/周四力量，周三周中休息日，周五间歇，周二/周六/周日稳定有氧
    if day <= 6:
        training = MENSTRUAL_LIGHT
    elif weekday == "周一":
        title, detail = STRENGTH["周一"]
        training = f"{title}：{detail}"
    elif weekday == "周四":
        title, detail = STRENGTH["周四"]
        training = f"{title}：{detail}"
    elif weekday == "周三":
        training = REST_DAY
    elif weekday == "周五":
        training = SPIN_INTERVAL
    else:
        training = SPIN_STEADY

    tip = TIPS[(date - dt.date(2026, 9, 2)).days % len(TIPS)]

    lines = [
        f"📅 {date.month}月{date.day}日（{weekday}）· 减脂第 {(date - dt.date(2026, 9, 2)).days + 1} 天",
        f"🌸 周期：{phase}",
        f"🔥 今日摄入：约 {kcal} kcal｜蛋白质 105g｜碳水 {carbs}｜脂肪 52g",
        f"🏋️ 训练：{training}",
        f"🍱 今日三餐（{meal_day}，{meal['kcal']}｜{meal['protein']}）：",
    ]
    lines += [f"• {m}" for m in meal["meals"]]
    if day <= 6:
        lines.append("• 经期加餐：再多 1 份主食（+50g 米饭或 +1 根玉米），优先选红肉/菠菜补铁")
    elif day >= 24:
        lines.append("• 黄体期加餐：+20g 主食（半根香蕉或一小块红薯），帮助稳住食欲")
    lines.append(f"💡 提醒：{note}。{tip}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="指定日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--send", action="store_true", help="推送到飞书")
    args = parser.parse_args()

    date = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    text = build_message(date, load_meals())
    print(text)

    if args.send:
        result = subprocess.run(
            [sys.executable, str(BASE / "send_feishu.py"), "--text", text],
            capture_output=True,
            text=True,
        )
        print(result.stdout.strip())
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
