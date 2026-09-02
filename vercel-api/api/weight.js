// 体重同步接口：POST 存体重到 GitHub 仓库 weight.json，GET 读取最新体重。
export default async function handler(req, res) {
  const TOKEN = process.env.GITHUB_TOKEN;
  const REPO = "cfy424/fatloss90";
  const FILE = "weight.json";
  const API = `https://api.github.com/repos/${REPO}/contents/${FILE}`;

  const headers = TOKEN
    ? {
        Authorization: `Bearer ${TOKEN}`,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
      }
    : { Accept: "application/vnd.github+json" };

  async function readFile() {
    const r = await fetch(API, { headers });
    if (r.status === 404) return null;
    if (!r.ok) throw new Error("read failed: " + r.status);
    const j = await r.json();
    let parsed = null;
    try {
      parsed = JSON.parse(Buffer.from(j.content, "base64").toString("utf-8"));
    } catch (e) {
      parsed = null;
    }
    return { sha: j.sha, data: parsed };
  }

  async function writeFile(weight) {
    // 写入后 GitHub 可能有短暂缓存延迟，重试几次
    for (let attempt = 1; attempt <= 4; attempt++) {
      try {
        const cur = await readFile();
        const content = Buffer.from(
          JSON.stringify({ weight, updatedAt: new Date().toISOString() }, null, 2)
        ).toString("base64");
        const body = { message: `chore: 更新体重 ${weight}kg`, content };
        if (cur && cur.sha) body.sha = cur.sha;
        const r = await fetch(API, {
          method: "PUT",
          headers: { ...headers, "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
        const j = await r.json();
        if (r.ok) return true;
        if (r.status === 422 && /sha/i.test(j.message || "")) {
          await new Promise((s) => setTimeout(s, 1500));
          continue;
        }
        throw new Error(j.message || "write failed");
      } catch (e) {
        if (attempt === 4) throw e;
        await new Promise((s) => setTimeout(s, 1500));
      }
    }
    return false;
  }

  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method === "POST") {
    const weight = Number(req.body && req.body.weight);
    if (!Number.isFinite(weight) || weight <= 0 || weight > 200) {
      return res.status(400).json({ error: "invalid weight" });
    }
    try {
      await writeFile(weight);
      return res.json({ ok: true, weight });
    } catch (e) {
      return res.status(500).json({ error: String(e) });
    }
  }

  // GET：公开仓库无需令牌即可读取
  try {
    const f = await readFile();
    const w = f && f.data ? Number(f.data.weight) : NaN;
    return res.json({ weight: Number.isFinite(w) && w > 0 ? w : 58 });
  } catch (e) {
    return res.status(500).json({ error: String(e) });
  }
}
