import json
import random
import re
from pathlib import Path

import ziranbianzhengfa_v3_all_choices as bank


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "docs"
SHORT_ANSWERS_PATH = ROOT / "short_answers.json"


PERSON_HINTS = (
    "孔德", "泰勒斯", "波普尔", "培根", "托勒密", "阿那克西曼德", "布什", "拉什", "恩格斯",
    "康德", "卡普", "斯诺", "海德格尔", "默顿", "卡逊", "米都斯", "弗里曼", "亨普尔",
    "毕达哥拉斯", "德谟克利特", "阿里斯塔克", "亚里士多德", "赖尔", "马尔库塞", "普利高津",
    "丹皮尔", "托夫勒", "马克思", "维特根斯坦", "彭加勒", "拉卡托斯", "库恩", "贝尔",
    "莱恩", "阿那克萨戈拉", "赫拉克利特", "雅克", "埃吕尔", "利奥波德", "法兰西", "熊彼特",
    "哈肯", "托姆", "牛顿", "苏格拉底", "爱因斯坦", "贝尔纳", "罗伯特", "门捷列夫",
    "米杜斯", "波珀", "德谟克里特", "普里戈金", "伽利略", "阿奎那", "芒福德", "石里克",
    "维勒", "麦克斯韦", "哥白尼", "开普勒",
)

INSTITUTION_HINTS = ("科学院", "皇家学会", "俱乐部", "国家", "美国", "英国", "法国", "德国", "瑞典")
TIME_HINTS = ("世纪", "时期", "革命", "年代", "年", "16", "17", "18", "19", "20")
METHOD_HINTS = ("从一般到个别", "从个别到一般", "否定后件式", "P-TT-EE-P", "DN模型")
WORK_HINTS = ("《", "》")
NATURE_VIEW_HINTS = ("自然观", "地心说", "原子论", "水本原", "火本原", "种子说", "地动说")
SCIENCE_THEORY_HINTS = (
    "相对论", "进化论", "细胞学说", "能量守恒", "元素周期律", "三大发现",
    "星云假说", "人工合成尿素", "电磁场理论",
)

TOPIC_OPTION_OVERRIDES = (
    ("《第三次浪潮》的作者", ["托夫勒", "丹尼尔贝尔", "万·布什", "库恩"]),
    ("耗散", ["普利高津（普里戈金）", "哈肯", "托姆", "贝尔纳"]),
    ("《科学史及其与哲学和宗教的关系》", ["丹皮尔", "贝尔纳", "罗伯特·K·默顿", "库恩"]),
    ("“第三次浪潮”指", ["信息革命", "工业革命", "科学革命", "农业革命"]),
    ("演绎方法的基本方向", ["从一般到个别", "从个别到一般", "从特殊到特殊", "从经验到假说"]),
    ("科学研究纲领", ["拉卡托斯", "库恩", "波普尔", "维特根斯坦"]),
    ("范式概念", ["库恩", "波普尔", "拉卡托斯", "罗伯特·K·默顿"]),
    ("不属于顿悟", ["计划性", "突发性", "直觉性", "灵感性"]),
    ("《大地的伦理》作者", ["利奥波德", "卡逊", "康德", "海德格尔"]),
    ("创新理论", ["熊彼特", "弗里曼", "罗伯特·K·默顿", "丹尼尔贝尔"]),
    ("水是万物本原", ["泰勒斯", "赫拉克利特", "阿那克西曼德", "德谟克利特"]),
    ("科学社会学之父", ["罗伯特·K·默顿", "库恩", "波普尔", "贝尔纳"]),
    ("《增长的极限》由哪个机构", ["罗马俱乐部", "法国科学院", "英国皇家学会", "美国科学院"]),
    ("地心说由谁", ["托勒密", "哥白尼", "开普勒", "伽利略"]),
    ("第二次工业革命时间", ["19世纪末到20世纪初", "18世纪60年代", "20世纪中叶", "17世纪"]),
    ("技术自主论", ["雅克·埃吕尔", "海德格尔", "芒福德", "马尔库塞"]),
    ("机械唯物主义自然观大致诞生", ["16—18世纪", "古希腊时期", "19世纪末到20世纪初", "20世纪中叶"]),
)


def stable_rng(*parts):
    seed = "|".join(str(part) for part in parts)
    return random.Random(seed)


def unique(values):
    result = []
    seen = set()
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def comparable_text(text):
    text = re.sub(r"[（(].*?[）)]", "", str(text))
    text = re.sub(r"[·.\s/、，,：:《》“”\"'—-]", "", text)
    return text


def too_similar(left, right):
    a = comparable_text(left)
    b = comparable_text(right)
    return bool(a and b and (a in b or b in a))


def classify_text(text):
    text = str(text)
    if any(item in text for item in WORK_HINTS):
        return "著作"
    if "学派" in text:
        return "概念"
    if any(item in text for item in INSTITUTION_HINTS) and not any(item in text for item in ("法国科学院", "法兰西皇家科学院")):
        return "机构"
    if any(item in text for item in ("法国科学院", "法兰西皇家科学院", "罗马俱乐部")):
        return "机构"
    if any(item in text for item in TIME_HINTS):
        return "年代"
    if any(item in text for item in METHOD_HINTS):
        return "方法"
    if any(item in text for item in SCIENCE_THEORY_HINTS):
        return "科学理论"
    if any(item in text for item in NATURE_VIEW_HINTS):
        return "自然观/理论"
    if any(item in text for item in PERSON_HINTS):
        return "人物"
    return "概念"


def expected_category(question, correct_text):
    question = str(question)
    if "机构" in question or "报告" in question:
        return "机构"
    if any(item in question for item in ("哪本书", "哪部书", "哪本著作", "哪部著作")):
        return "著作"
    if any(item in question for item in ("作者", "谁", "哪位", "哪个人", "人物", "代表人物", "提出者", "出自谁")):
        return "人物"
    if any(item in question for item in ("学者是", "哲学家是", "思想家是", "学者提出", "哲学家提出", "思想家提出")):
        return "人物"
    if any(item in question for item in ("时间", "时期", "哪一年", "阶段")) or ("世纪" in question and "《" not in question):
        return "年代"
    if "科学基础" in question or "科学技术基础" in question:
        return "科学理论"
    if any(item in question for item in ("表现形式", "基本特征", "流派")):
        return "概念"
    if any(item in question for item in ("方法", "方向", "模式")):
        return "方法"
    if any(item in question for item in ("著作", "作品", "哪本书")):
        return "著作"
    if "自然观" in question or "理论" in question:
        return "自然观/理论"
    return classify_text(correct_text)


def build_category_pools():
    values = []
    values.extend(bank.MATCHING_DATA.values())
    for question in bank.CHOICE_QUESTIONS:
        values.append(bank.get_correct_text(question))
        values.extend(question.get("options", {}).values())

    pools = {}
    for value in unique(str(item) for item in values):
        pools.setdefault(classify_text(value), []).append(value)

    pools.setdefault("人物", []).extend([
        "孔德", "泰勒斯", "波普尔", "弗朗西斯·培根", "托勒密", "阿那克西曼德", "恩格斯", "康德",
        "恩斯特·卡普", "C.P.斯诺", "海德格尔", "罗伯特·K·默顿", "蕾切尔·卡逊", "托夫勒",
        "马克思", "维特根斯坦", "彭加勒", "拉卡托斯", "库恩", "丹尼尔·贝尔", "熊彼特", "利奥波德",
        "普利高津", "哈肯", "托姆", "雅克·埃吕尔", "丹皮尔", "毕达哥拉斯", "德谟克利特",
        "阿里斯塔克", "亚里士多德", "马尔库塞", "贝尔纳", "爱因斯坦",
    ])
    pools.setdefault("机构", []).extend([
        "法国科学院", "英国皇家学会", "瑞典科学院", "美国科学院", "罗马俱乐部", "法兰西皇家科学院",
    ])
    pools.setdefault("著作", []).extend([
        "《自然辩证法》", "《科学：无尽的前沿》", "《寂静的春天》", "《两种文化》",
        "《十七世纪英格兰的科学、技术与社会》", "《增长的极限》", "《单向度的人》",
        "《科学史及其与哲学和宗教的关系》", "《第三次浪潮》", "《后工业社会》",
        "《知识社会》", "《大地的伦理》", "《1844年经济学哲学手稿》",
    ])
    pools.setdefault("年代", []).extend([
        "16—18世纪", "16-18世纪", "17世纪", "18世纪", "19世纪末到20世纪初", "工业革命",
        "信息革命", "古希腊时期", "近代科学革命时期",
    ])
    pools.setdefault("方法", []).extend([
        "从一般到个别", "从个别到一般", "否定后件式", "演绎-律则模型", "P-TT-EE-P",
    ])
    pools.setdefault("自然观/理论", []).extend([
        "朴素唯物主义自然观", "机械唯物主义自然观", "系统自然观", "生态自然观", "古代原子论",
        "地心说", "地动说", "耗散结构理论", "技术自主论",
    ])
    pools.setdefault("科学理论", []).extend([
        "能量守恒与转化定律", "细胞学说", "生物进化论", "元素周期律", "爱因斯坦的相对论",
        "牛顿力学", "热力学第二定律",
    ])
    pools.setdefault("概念", []).extend([
        "信息革命", "计划性", "问题", "权威主义", "技术理性", "国家创新体系", "科学共同体",
    ])
    return {category: unique(items) for category, items in pools.items()}


def generate_options(question, correct_text, preferred_category=None, existing_options=None):
    category = preferred_category or expected_category(question, correct_text)
    for marker, values in TOPIC_OPTION_OVERRIDES:
        if marker in str(question) and correct_text in values:
            options = values[:]
            rng = stable_rng(question, correct_text, "override")
            rng.shuffle(options)
            letters = list(existing_options.keys()) if existing_options else ["A", "B", "C", "D"]
            return {letter: value for letter, value in zip(letters, options)}

    pool = [
        item for item in CATEGORY_POOLS.get(category, [])
        if item != correct_text and not too_similar(item, correct_text)
    ]
    if len(pool) < 3:
        pool.extend(
            item for item in ANSWER_POOL
            if item != correct_text and item not in pool and not too_similar(item, correct_text)
        )

    rng = stable_rng(question, correct_text, category)
    candidates = pool[:]
    rng.shuffle(candidates)
    distractors = []
    for item in candidates:
        if all(not too_similar(item, selected) for selected in distractors):
            distractors.append(item)
        if len(distractors) == 3:
            break
    values = distractors + [correct_text]
    rng.shuffle(values)

    if existing_options:
        letters = list(existing_options.keys())
    else:
        letters = ["A", "B", "C", "D"]
    return {letter: value for letter, value in zip(letters, values)}


def should_rebuild_options(question, correct_text, options):
    if not options or len(options) < 4:
        return True

    category = expected_category(question, correct_text)
    if category not in ("人物", "机构", "年代", "著作", "科学理论"):
        return False

    same_category_count = sum(1 for value in options.values() if classify_text(value) == category)
    return same_category_count < 3


def choice_question_payload(index, question):
    correct_text = bank.get_correct_text(question)
    options = question.get("options")
    category = expected_category(question["question"], correct_text)
    if should_rebuild_options(question["question"], correct_text, options):
        normalized_options = generate_options(
            question["question"],
            correct_text,
            category,
            existing_options=options,
        )
    else:
        normalized_options = dict(sorted(options.items()))

    correct_letter = next(
        (letter for letter, text in normalized_options.items() if text == correct_text),
        question.get("answer", ""),
    )
    return {
        "id": "choice-{}".format(index),
        "type": "选择题",
        "question": question["question"],
        "options": normalized_options,
        "answer": correct_letter,
        "correctText": correct_text,
        "category": category,
        "source": question.get("source", ""),
        "note": question.get("note", ""),
    }


def matching_question_payload(index, question, answer):
    category = classify_text(answer)
    options = generate_options(question, answer, category)
    correct_letter = next(letter for letter, text in options.items() if text == answer)
    return {
        "id": "matching-{}".format(index),
        "type": "匹配题",
        "question": question,
        "options": options,
        "answer": correct_letter,
        "correctText": answer,
        "category": category,
        "source": "观点-人物/答案匹配题",
        "note": "",
    }


def all_questions():
    questions = [
        choice_question_payload(i, question)
        for i, question in enumerate(bank.CHOICE_QUESTIONS, 1)
    ]
    questions.extend(
        matching_question_payload(i, question, answer)
        for i, (question, answer) in enumerate(bank.MATCHING_DATA.items(), 1)
    )
    return questions


def short_answers():
    return json.loads(SHORT_ANSWERS_PATH.read_text(encoding="utf-8"))


INDEX_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>自然辩证法刷题</title>
  <link rel="stylesheet" href="./styles.css">
</head>
<body>
  <header>
    <h1>自然辩证法刷题</h1>
    <nav class="tabs" aria-label="功能">
      <button class="tab active" id="bankTab" type="button">所有题库</button>
      <button class="tab" id="quizTab" type="button">随机出题</button>
      <button class="tab" id="shortTab" type="button">简答题</button>
    </nav>
  </header>
  <main>
    <section id="bankView">
      <div class="toolbar">
        <input id="search" placeholder="搜索题干、选项、答案、来源" autocomplete="off">
        <button class="secondary" id="clearSearch" type="button">清空</button>
      </div>
      <p class="count" id="bankCount">正在加载题库...</p>
      <div id="bankList"></div>
    </section>
    <section id="quizView" class="hidden">
      <p class="count" id="score">已答 0 题，正确 0 题</p>
      <div id="quizCard"></div>
    </section>
    <section id="shortView" class="hidden">
      <div class="toolbar">
        <input id="shortSearch" placeholder="搜索简答题题目、答案" autocomplete="off">
        <button class="secondary" id="clearShortSearch" type="button">清空</button>
      </div>
      <p class="count" id="shortCount">正在加载简答题...</p>
      <div id="shortPractice"></div>
      <div id="shortList"></div>
    </section>
  </main>
  <script src="./app.js"></script>
</body>
</html>
"""


CSS = """:root {
  color-scheme: light;
  --bg: #f5f7fb;
  --panel: #ffffff;
  --text: #172033;
  --muted: #647084;
  --line: #dce3ef;
  --primary: #0f766e;
  --bad: #b42318;
  --bad-soft: #fee4e2;
  --good: #087443;
  --good-soft: #dcfae6;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
  line-height: 1.5;
}
header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(245, 247, 251, .94);
  border-bottom: 1px solid var(--line);
  backdrop-filter: blur(10px);
  padding: max(12px, env(safe-area-inset-top)) 14px 10px;
}
h1 {
  margin: 0 0 10px;
  font-size: 20px;
  letter-spacing: 0;
}
.tabs, .actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
button, input { font: inherit; }
.tab, .option, .primary, .secondary {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--panel);
  color: var(--text);
  min-height: 44px;
  padding: 10px 12px;
  text-align: center;
}
.tab.active, .primary {
  border-color: var(--primary);
  background: var(--primary);
  color: #fff;
}
main {
  max-width: 860px;
  margin: 0 auto;
  padding: 14px 14px 28px;
}
.toolbar {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px;
  margin-bottom: 12px;
}
input {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 8px;
  min-height: 44px;
  padding: 10px 12px;
  background: #fff;
}
.count {
  color: var(--muted);
  font-size: 13px;
  margin: 0 0 10px;
}
.card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 14px;
  margin-bottom: 10px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, .04);
}
.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
  color: var(--muted);
  font-size: 12px;
}
.pill {
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 2px 8px;
  background: #fff;
}
.question {
  margin: 0 0 12px;
  font-weight: 650;
  word-break: break-word;
}
.options {
  display: grid;
  gap: 8px;
}
.option {
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 8px;
  text-align: left;
  align-items: start;
}
.option .letter {
  color: var(--primary);
  font-weight: 700;
}
.option.correct {
  border-color: var(--good);
  background: var(--good-soft);
}
.option.wrong {
  border-color: var(--bad);
  background: var(--bad-soft);
}
.result {
  margin-top: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--line);
  background: #fff;
}
.result.good {
  border-color: var(--good);
  background: var(--good-soft);
  color: var(--good);
}
.result.bad {
  border-color: var(--bad);
  background: var(--bad-soft);
  color: var(--bad);
}
.actions { margin-top: 12px; }
.actions.two { grid-template-columns: 1fr 1fr; }
.secondary { background: #fff; }
.hidden { display: none; }
.answer {
  white-space: pre-wrap;
}
@media (min-width: 720px) {
  h1 { font-size: 24px; }
  .options.two-col { grid-template-columns: 1fr 1fr; }
}
"""


JS = """const state = {
  questions: [],
  shortAnswers: [],
  quizQueue: [],
  shortQueue: [],
  current: null,
  currentShort: null,
  answered: false,
  total: 0,
  right: 0,
  round: 1,
  shortRound: 1
};
const bankTab = document.getElementById("bankTab");
const quizTab = document.getElementById("quizTab");
const shortTab = document.getElementById("shortTab");
const bankView = document.getElementById("bankView");
const quizView = document.getElementById("quizView");
const shortView = document.getElementById("shortView");
const bankList = document.getElementById("bankList");
const bankCount = document.getElementById("bankCount");
const search = document.getElementById("search");
const score = document.getElementById("score");
const quizCard = document.getElementById("quizCard");
const shortSearch = document.getElementById("shortSearch");
const shortCount = document.getElementById("shortCount");
const shortPractice = document.getElementById("shortPractice");
const shortList = document.getElementById("shortList");

function escapeHtml(value) {
  return String(value || "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[char]));
}

function shuffle(values) {
  const result = [...values];
  for (let i = result.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

function buildQuizOptions(question) {
  if (Object.keys(question.options).length > 1) return question.options;
  let pool = state.questions
    .filter((item) => item.category === question.category)
    .map((item) => item.correctText)
    .filter((item) => item !== question.correctText);
  if (pool.length < 3) {
    pool = state.questions.map((item) => item.correctText).filter((item) => item !== question.correctText);
  }
  const picked = shuffle([...new Set(pool)]).slice(0, 3);
  const values = shuffle([...picked, question.correctText]);
  return Object.fromEntries(values.map((text, index) => [String.fromCharCode(65 + index), text]));
}

function resetQuizQueue() {
  let nextQueue = shuffle(state.questions);
  if (state.current && nextQueue.length > 1 && nextQueue[0].id === state.current.id) {
    nextQueue.push(nextQueue.shift());
  }
  state.quizQueue = nextQueue;
}

function nextBaseQuestion() {
  if (state.quizQueue.length === 0) {
    if (state.current) state.round += 1;
    resetQuizQueue();
  }
  return state.quizQueue.shift();
}

function resetShortQueue() {
  let nextQueue = shuffle(state.shortAnswers);
  if (state.currentShort && nextQueue.length > 1 && nextQueue[0].id === state.currentShort.id) {
    nextQueue.push(nextQueue.shift());
  }
  state.shortQueue = nextQueue;
}

function nextShortQuestion() {
  if (state.shortQueue.length === 0) {
    if (state.currentShort) state.shortRound += 1;
    resetShortQueue();
  }
  return state.shortQueue.shift();
}

function optionHtml(options, correctText = "") {
  return Object.entries(options).map(([letter, text]) => {
    const cls = text === correctText ? "option correct" : "option";
    return `<div class="${cls}"><span class="letter">${letter}</span><span>${escapeHtml(text)}</span></div>`;
  }).join("");
}

function renderBank() {
  const keyword = search.value.trim().toLowerCase();
  const filtered = state.questions.filter((item) => {
    const haystack = [
      item.type, item.question, item.correctText, item.source,
      ...Object.values(item.options || {})
    ].join(" ").toLowerCase();
    return haystack.includes(keyword);
  });
  bankCount.textContent = `共 ${state.questions.length} 题，当前显示 ${filtered.length} 题`;
  bankList.innerHTML = filtered.map((item, idx) => `
    <article class="card">
      <div class="meta">
        <span class="pill">${idx + 1}</span>
        <span class="pill">${escapeHtml(item.type)}</span>
        ${item.source ? `<span class="pill">${escapeHtml(item.source)}</span>` : ""}
      </div>
      <p class="question">${escapeHtml(item.question)}</p>
      <div class="options two-col">${optionHtml(item.options, item.correctText)}</div>
      <div class="result">正确答案：${escapeHtml(item.correctText)}</div>
      ${item.note ? `<div class="result">${escapeHtml(item.note)}</div>` : ""}
    </article>
  `).join("");
}

function renderShortList() {
  const keyword = shortSearch.value.trim().toLowerCase();
  const filtered = state.shortAnswers.filter((item) => {
    const haystack = [item.number, item.title, item.answer].join(" ").toLowerCase();
    return haystack.includes(keyword);
  });
  shortCount.textContent = `共 ${state.shortAnswers.length} 道简答题，当前显示 ${filtered.length} 道，本轮剩余 ${state.shortQueue.length} 道`;
  shortList.innerHTML = filtered.map((item) => `
    <article class="card">
      <div class="meta">
        <span class="pill">${item.number}</span>
        <span class="pill">简答题</span>
      </div>
      <p class="question">${escapeHtml(item.title)}</p>
      <div class="result answer">${escapeHtml(item.answer)}</div>
    </article>
  `).join("");
}

function renderScore() {
  const remaining = state.quizQueue.length;
  score.textContent = `第 ${state.round} 轮，已答 ${state.total} 题，正确 ${state.right} 题，本轮剩余 ${remaining} 题`;
}

function showQuizQuestion() {
  const base = nextBaseQuestion();
  const options = buildQuizOptions(base);
  const answer = Object.entries(options).find(([, text]) => text === base.correctText)[0];
  state.current = { ...base, options, answer };
  state.answered = false;
  const q = state.current;
  quizCard.innerHTML = `
    <article class="card">
      <div class="meta">
        <span class="pill">${escapeHtml(q.type)}</span>
        ${q.source ? `<span class="pill">${escapeHtml(q.source)}</span>` : ""}
      </div>
      <p class="question">${escapeHtml(q.question)}</p>
      <div class="options" id="quizOptions">
        ${Object.entries(q.options).map(([letter, text]) => `
          <button class="option" data-letter="${letter}" type="button">
            <span class="letter">${letter}</span><span>${escapeHtml(text)}</span>
          </button>
        `).join("")}
      </div>
      <div id="quizResult"></div>
      <div class="actions two">
        <button class="primary" id="nextQuestion" type="button">下一题</button>
        <button class="secondary" id="showAnswer" type="button">看答案</button>
      </div>
    </article>
  `;
  document.querySelectorAll("#quizOptions .option").forEach((button) => {
    button.addEventListener("click", () => answerQuestion(button.dataset.letter));
  });
  document.getElementById("nextQuestion").addEventListener("click", showQuizQuestion);
  document.getElementById("showAnswer").addEventListener("click", () => answerQuestion(""));
}

function showShortQuestion() {
  const item = nextShortQuestion();
  state.currentShort = item;
  shortPractice.innerHTML = `
    <article class="card">
      <div class="meta">
        <span class="pill">随机抽背</span>
        <span class="pill">第 ${state.shortRound} 轮</span>
        <span class="pill">剩余 ${state.shortQueue.length}</span>
      </div>
      <p class="question">${item.number}. ${escapeHtml(item.title)}</p>
      <div id="shortAnswerBox" class="result answer hidden">${escapeHtml(item.answer)}</div>
      <div class="actions two">
        <button class="primary" id="toggleShortAnswer" type="button">显示答案</button>
        <button class="secondary" id="nextShort" type="button">下一题</button>
      </div>
    </article>
  `;
  const answerBox = document.getElementById("shortAnswerBox");
  const toggle = document.getElementById("toggleShortAnswer");
  toggle.addEventListener("click", () => {
    const hidden = answerBox.classList.toggle("hidden");
    toggle.textContent = hidden ? "显示答案" : "隐藏答案";
  });
  document.getElementById("nextShort").addEventListener("click", () => {
    showShortQuestion();
    renderShortList();
  });
}

function answerQuestion(letter) {
  if (state.answered) return;
  state.answered = true;
  const q = state.current;
  const isRight = letter === q.answer;
  if (letter) {
    state.total += 1;
    if (isRight) state.right += 1;
  }
  renderScore();
  document.querySelectorAll("#quizOptions .option").forEach((button) => {
    if (button.dataset.letter === q.answer) button.classList.add("correct");
    if (letter && button.dataset.letter === letter && !isRight) button.classList.add("wrong");
  });
  const result = document.getElementById("quizResult");
  const cls = !letter ? "" : isRight ? "good" : "bad";
  const prefix = !letter ? "正确答案" : isRight ? "回答正确" : "回答错误";
  result.innerHTML = `
    <div class="result ${cls}">${prefix}：${escapeHtml(q.answer)}. ${escapeHtml(q.correctText)}</div>
    ${q.note ? `<div class="result">${escapeHtml(q.note)}</div>` : ""}
  `;
}

function setView(view) {
  const isBank = view === "bank";
  const isQuiz = view === "quiz";
  const isShort = view === "short";
  bankTab.classList.toggle("active", isBank);
  quizTab.classList.toggle("active", isQuiz);
  shortTab.classList.toggle("active", isShort);
  bankView.classList.toggle("hidden", !isBank);
  quizView.classList.toggle("hidden", !isQuiz);
  shortView.classList.toggle("hidden", !isShort);
  if (isQuiz && !state.current) showQuizQuestion();
  if (isShort && !state.currentShort) showShortQuestion();
}

async function loadQuestions() {
  const [questionsRes, shortRes] = await Promise.all([
    fetch("./questions.json"),
    fetch("./short_answers.json")
  ]);
  state.questions = await questionsRes.json();
  state.shortAnswers = await shortRes.json();
  resetQuizQueue();
  resetShortQueue();
  renderBank();
  renderShortList();
  renderScore();
}

bankTab.addEventListener("click", () => setView("bank"));
quizTab.addEventListener("click", () => setView("quiz"));
shortTab.addEventListener("click", () => setView("short"));
search.addEventListener("input", renderBank);
shortSearch.addEventListener("input", renderShortList);
document.getElementById("clearSearch").addEventListener("click", () => {
  search.value = "";
  renderBank();
  search.focus();
});
document.getElementById("clearShortSearch").addEventListener("click", () => {
  shortSearch.value = "";
  renderShortList();
  shortSearch.focus();
});

loadQuestions().catch(() => {
  bankCount.textContent = "题库加载失败，请确认通过网页服务或 GitHub Pages 打开。";
});
"""


ANSWER_POOL = bank.build_answer_pool()
CATEGORY_POOLS = build_category_pools()


def main():
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    (OUT_DIR / "styles.css").write_text(CSS, encoding="utf-8")
    (OUT_DIR / "app.js").write_text(JS, encoding="utf-8")
    (OUT_DIR / "questions.json").write_text(
        json.dumps(all_questions(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "short_answers.json").write_text(
        json.dumps(short_answers(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print("Built {} questions into {}".format(len(all_questions()), OUT_DIR))


if __name__ == "__main__":
    main()
