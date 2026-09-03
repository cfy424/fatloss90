# add_keep_c3_gears.py
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add CSS for Keep C3 HUD
old_css_anchor = """.hiit-phase-tag {
  display: inline-block;"""

new_css_hud = """.hiit-c3-hud {
  display: flex;
  gap: 10px;
  margin: 10px 0 14px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 14px;
  padding: 10px 14px;
  backdrop-filter: blur(6px);
}
.c3-hud-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}
.c3-hud-item:first-child {
  border-right: 1px solid rgba(255, 255, 255, 0.12);
}
.c3-hud-lbl {
  font-size: 11px;
  color: #94A3B8;
  font-weight: 700;
}
.c3-hud-val {
  font-size: 15px;
  font-weight: 850;
  color: #F8FAFC;
  letter-spacing: 0.3px;
  transition: all 0.2s;
}

.hiit-phase-tag {"""

assert old_css_anchor in content, "old_css_anchor not found"
content = content.replace(old_css_anchor, new_css_hud, 1)

# 2. Add Keep C3 HUD to cardHiitTimer in Tab 2 HTML
old_hiit_html = """    <!-- 动感单车 HIIT 计时器 -->
    <section class="hiit-banner" id="cardHiitTimer">
      <div class="card-title-row" style="margin-bottom:6px;">
        <span style="font-size:15px; font-weight:800;">🚴 动感单车间歇 (HIIT) 专用助手</span>
        <span style="font-size:12px; color:#94A3B8;" id="hiitTotalRemain">总时长 30:00</span>
      </div>
      <span class="hiit-phase-tag warm" id="hiitPhaseTag">热身阶段 (5 min)</span>"""

new_hiit_html = """    <!-- 动感单车 HIIT 计时器 -->
    <section class="hiit-banner" id="cardHiitTimer">
      <div class="card-title-row" style="margin-bottom:6px;">
        <span style="font-size:15px; font-weight:800;">🚴 动感单车间歇 (HIIT) 专用助手</span>
        <span style="font-size:12px; color:#94A3B8;" id="hiitTotalRemain">总时长 30:00</span>
      </div>

      <!-- Keep C3 阻力与踏频实时仪表盘 -->
      <div class="hiit-c3-hud" id="hiitC3Hud">
        <div class="c3-hud-item">
          <span class="c3-hud-lbl">⚙️ Keep C3 阻力 (共36挡)</span>
          <span class="c3-hud-val" id="hiitGearVal"><span style="color:#38BDF8;">8 - 10 挡</span></span>
        </div>
        <div class="c3-hud-item">
          <span class="c3-hud-lbl">⚡ 建议踏频 RPM</span>
          <span class="c3-hud-val" id="hiitRpmVal">80 - 90 RPM</span>
        </div>
      </div>

      <span class="hiit-phase-tag warm" id="hiitPhaseTag">热身阶段 (5 min)</span>"""

assert old_hiit_html in content, "old_hiit_html not found"
content = content.replace(old_hiit_html, new_hiit_html, 1)

# 3. Update WORKOUT_PLANS in index.html for Tuesday, Friday, Saturday, Sunday
old_workout_plans = """  "周二": {
    title: "动感单车 · 稳态燃脂",
    desc: "🚴 动感单车 40-45 分钟：保持心率在燃脂区间（约125-145bpm），微喘但能说话，稳态高效消耗脂肪",
    type: "c"
  },
  "周三": {
    title: "周中休息日 · 散步与拉伸",
    variants: [
      { id: "R1", name: "全身深度柔韧拉伸跟练", list: ["股四头肌侧卧拉伸", "腘绳肌柔韧拉伸", "坐姿臀肌深度拉伸", "死虫式"] }
    ],
    type: "r"
  },
  "周四": {
    title: "上肢力量塑型",
    variants: [
      { id: "B1", name: "B1: 紧致胸背肩 (改善体态)", list: ["哑铃卧推", "单臂哑铃划船", "坐姿哑铃推举", "哑铃侧平举", "哑铃二头弯举", "跪姿俯卧撑"] },
      { id: "B2", name: "B2: 天鹅臂直角肩 (消除副乳)", list: ["跪姿俯卧撑", "单臂哑铃划船", "哑铃侧平举", "哑铃俯身后臂屈伸", "哑铃二头弯举", "死虫式"] }
    ],
    type: "s"
  },
  "周五": {
    title: "动感单车 · 极速间歇",
    desc: "🚴 动感单车 HIIT 约 30 分钟：热身 5min + 6-8 轮（高阻冲刺 1min + 轻松恢复 2min）+ 放松 5min",
    type: "c"
  },
  "周六": {
    title: "动感单车 · 稳定燃脂",
    desc: "🚴 动感单车 35-40 分钟：匀速踩踏，高效消耗糖原并促进脂肪氧化",
    type: "c"
  },
  "周日": {
    title: "动感单车 · 音乐轻踩恢复",
    desc: "🚴 动感单车 30 分钟：听轻快音乐慢速踩踏，促进乳酸代谢，活力满满迎接下周！",
    type: "c"
  }"""

new_workout_plans = """  "周二": {
    title: "动感单车 · 稳态燃脂",
    desc: `<div style="font-weight:750; margin-bottom:6px; font-size:14px; color:#0369A1;">🚴 Keep C3 动感单车 · 45分钟黄金稳态燃脂</div>
<div style="font-size:12.5px; line-height:1.7; color:#0C4A6E;">
  Keep C3 智能磁控共 36 挡，今日控制在 <strong>FatMax（最佳脂肪氧化心率区间）</strong>：<br>
  • <strong>0-5 min (热身启动)</strong>：<strong>8 - 10 挡</strong> ｜ 踏频 80-90 RPM ｜ 唤醒髋膝与心肺<br>
  • <strong>5-40 min (黄金巡航)</strong>：<strong>13 - 16 挡</strong> ｜ 踏频 75-85 RPM ｜ 适中有力阻力，微微出汗，能连续说话但微喘<br>
  • <strong>40-45 min (排酸冷身)</strong>：<strong>6 - 8 挡</strong> ｜ 踏频 65-75 RPM ｜ 慢速平踩，心率回落至100以下
</div>`,
    type: "c"
  },
  "周三": {
    title: "周中休息日 · 散步与拉伸",
    variants: [
      { id: "R1", name: "全身深度柔韧拉伸跟练", list: ["股四头肌侧卧拉伸", "腘绳肌柔韧拉伸", "坐姿臀肌深度拉伸", "死虫式"] }
    ],
    type: "r"
  },
  "周四": {
    title: "上肢力量塑型",
    variants: [
      { id: "B1", name: "B1: 紧致胸背肩 (改善体态)", list: ["哑铃卧推", "单臂哑铃划船", "坐姿哑铃推举", "哑铃侧平举", "哑铃二头弯举", "跪姿俯卧撑"] },
      { id: "B2", name: "B2: 天鹅臂直角肩 (消除副乳)", list: ["跪姿俯卧撑", "单臂哑铃划船", "哑铃侧平举", "哑铃俯身后臂屈伸", "哑铃二头弯举", "死虫式"] }
    ],
    type: "s"
  },
  "周五": {
    title: "动感单车 · 极速间歇",
    desc: `<div style="font-weight:750; margin-bottom:6px; font-size:14px; color:#B45309;">🚴 Keep C3 动感单车 · 30分钟极速间歇 (HIIT)</div>
<div style="font-size:12.5px; line-height:1.7; color:#78350F;">
  Keep C3 阻力旋钮随时切换，点下方按钮进入专用全自动计时助手：<br>
  • <strong>热身 (5 min)</strong>：<strong>8 - 10 挡</strong> ｜ 踏频 80-90 RPM<br>
  • <strong>6-8 轮冲刺循环</strong>：<br>
  &nbsp;&nbsp;🔥 <strong>爆发冲刺 1min</strong>：<strong>20 - 24 挡</strong>（站姿冲刺建议 <strong>24-26 挡</strong>）｜ 踏频 95-110 RPM，心率飙升至85%+<br>
  &nbsp;&nbsp;🧘 <strong>间歇恢复 2min</strong>：<strong>8 - 10 挡</strong> ｜ 踏频 70-80 RPM，深呼吸慢骑还清氧债，勿完全停脚！<br>
  • <strong>冷身 (5 min)</strong>：<strong>6 - 8 挡</strong> ｜ 极轻阻力慢骑平复心率
</div>`,
    type: "c"
  },
  "周六": {
    title: "动感单车 · 坡度耐力燃脂",
    desc: `<div style="font-weight:750; margin-bottom:6px; font-size:14px; color:#0369A1;">🚴 Keep C3 动感单车 · 40分钟模拟爬坡耐力</div>
<div style="font-size:12.5px; line-height:1.7; color:#0C4A6E;">
  利用 Keep C3 大阻力模拟户外盘山爬坡，深度激活臀腿大肌群：<br>
  • <strong>0-5 min (平路热身)</strong>：<strong>8 - 10 挡</strong> ｜ 踏频 85 RPM<br>
  • <strong>5-25 min (缓坡坐姿攀爬)</strong>：<strong>15 - 18 挡</strong> ｜ 踏频 70-75 RPM ｜ 坐姿臀部稍往后坐，脚跟带动发力<br>
  • <strong>25-35 min (陡坡站姿重踏)</strong>：<strong>22 - 26 挡</strong> ｜ 踏频 55-65 RPM ｜ 站姿收紧核心，身体不剧烈晃动，专注臀大肌下压<br>
  • <strong>35-40 min (平路冷身)</strong>：<strong>6 - 8 挡</strong> ｜ 慢踏排酸
</div>`,
    type: "c"
  },
  "周日": {
    title: "动感单车 · 音乐排酸轻骑",
    desc: `<div style="font-weight:750; margin-bottom:6px; font-size:14px; color:#0369A1;">🚴 Keep C3 动感单车 · 30分钟音乐排酸</div>
<div style="font-size:12.5px; line-height:1.7; color:#0C4A6E;">
  • <strong>全程低阻顺畅</strong>：<strong>8 - 11 挡</strong> ｜ 踏频 75-85 RPM<br>
  • 戴上耳机听喜欢的轻快音乐或播客，极度轻松慢踩，加速下肢血液循环和乳酸代谢，消肿放松迎接新一周！
</div>`,
    type: "c"
  }"""

assert old_workout_plans in content, "old_workout_plans not found"
content = content.replace(old_workout_plans, new_workout_plans, 1)

# 4. Update renderHiitUI in JS to update hiitGearVal and hiitRpmVal
old_hiit_render = """    if (hiitState.phase === "warmup") {
      tagEl.className = "hiit-phase-tag warm";
      tagEl.textContent = "热身阶段 (5 min)";
      statusEl.textContent = "踏频 80-90，低阻力唤醒心肺与膝盖关节";
    } else if (hiitState.phase === "sprint") {
      tagEl.className = "hiit-phase-tag sprint";
      tagEl.textContent = `第 ${hiitState.currentRound}/${HIIT_CONFIG.rounds} 轮 · 冲刺 🔥 (1 min)`;
      statusEl.textContent = "加阻力！站姿或坐姿全力踩踏！冲刺！";
    } else if (hiitState.phase === "recover") {
      tagEl.className = "hiit-phase-tag recover";
      tagEl.textContent = `第 ${hiitState.currentRound}/${HIIT_CONFIG.rounds} 轮 · 恢复 🧘 (2 min)`;
      statusEl.textContent = "调低阻力，深呼吸，平稳轻踩恢复心率";
    } else if (hiitState.phase === "cooldown") {
      tagEl.className = "hiit-phase-tag cool";
      tagEl.textContent = "放松冷身 (5 min)";
      statusEl.textContent = "极轻阻力慢踩，逐渐降低心率，准备拉伸";
    } else {
      tagEl.className = "hiit-phase-tag recover";
      tagEl.textContent = "训练完成 🎉";
      statusEl.textContent = "太棒了！今日间歇单车已圆满达成！";
    }"""

new_hiit_render = """    const gearValEl = document.getElementById("hiitGearVal");
    const rpmValEl = document.getElementById("hiitRpmVal");

    if (hiitState.phase === "warmup") {
      tagEl.className = "hiit-phase-tag warm";
      tagEl.textContent = "热身阶段 (5 min)";
      statusEl.textContent = "热身启动：轻阻力平稳踩踏，唤醒膝关节与心肺";
      if (gearValEl) gearValEl.innerHTML = '<span style="color:#38BDF8;">8 - 10 挡 (轻盈启动)</span>';
      if (rpmValEl) rpmValEl.textContent = "80 - 90 RPM (平稳快踩)";
    } else if (hiitState.phase === "sprint") {
      tagEl.className = "hiit-phase-tag sprint";
      tagEl.textContent = `第 ${hiitState.currentRound}/${HIIT_CONFIG.rounds} 轮 · 冲刺 🔥 (1 min)`;
      statusEl.textContent = "迅速加阻力！站姿或坐姿全力踩踏！冲刺爆发！";
      if (gearValEl) gearValEl.innerHTML = '<span style="color:#EF4444; font-weight:900;">20 - 24 挡 🔥</span> <span style="font-size:11px; color:#FCA5A5;">(站姿24-26)</span>';
      if (rpmValEl) rpmValEl.textContent = "95 - 110 RPM (全力冲刺)";
    } else if (hiitState.phase === "recover") {
      tagEl.className = "hiit-phase-tag recover";
      tagEl.textContent = `第 ${hiitState.currentRound}/${HIIT_CONFIG.rounds} 轮 · 恢复 🧘 (2 min)`;
      statusEl.textContent = "迅速降回低阻力，大口深呼吸平复心率，保持轻踩勿骤停！";
      if (gearValEl) gearValEl.innerHTML = '<span style="color:#10B981;">8 - 10 挡 🧘 (大幅减阻)</span>';
      if (rpmValEl) rpmValEl.textContent = "70 - 80 RPM (平缓轻踩)";
    } else if (hiitState.phase === "cooldown") {
      tagEl.className = "hiit-phase-tag cool";
      tagEl.textContent = "放松冷身 (5 min)";
      statusEl.textContent = "极轻阻力慢踩，促使心率平稳回落，准备下车拉伸";
      if (gearValEl) gearValEl.innerHTML = '<span style="color:#818CF8;">6 - 8 挡 ❄️ (极轻排酸)</span>';
      if (rpmValEl) rpmValEl.textContent = "60 - 70 RPM (慢速放松)";
    } else {
      tagEl.className = "hiit-phase-tag recover";
      tagEl.textContent = "训练完成 🎉";
      statusEl.textContent = "太棒了！今日 Keep C3 间歇单车已圆满达成！";
      if (gearValEl) gearValEl.textContent = "达成 30min 🎉";
      if (rpmValEl) rpmValEl.textContent = "训练结束";
    }"""

assert old_hiit_render in content, "old_hiit_render not found"
content = content.replace(old_hiit_render, new_hiit_render, 1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Keep C3 gears added to index.html successfully!")
