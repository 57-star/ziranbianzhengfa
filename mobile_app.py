import argparse
import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse

import ziranbianzhengfa_v3_all_choices as bank


ANSWER_POOL = bank.build_answer_pool()


def choice_question_payload(index, question):
    correct_text = bank.get_correct_text(question)
    options = question.get("options")
    if options:
        normalized_options = dict(sorted(options.items()))
    else:
        normalized_options = bank.generate_options(correct_text, ANSWER_POOL)

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
        "source": question.get("source", ""),
        "note": question.get("note", ""),
    }


def matching_question_payload(index, question, answer):
    distractors = [item for item in ANSWER_POOL if item != answer]
    choices = random.sample(distractors, min(3, len(distractors))) + [answer]
    random.shuffle(choices)
    options = {chr(65 + i): item for i, item in enumerate(choices)}
    correct_letter = next(letter for letter, text in options.items() if text == answer)
    return {
        "id": "matching-{}".format(index),
        "type": "匹配题",
        "question": question,
        "options": options,
        "answer": correct_letter,
        "correctText": answer,
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


def json_response(handler, payload, status=200):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


INDEX_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>自然辩证法刷题</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5f7fb;
      --panel: #ffffff;
      --text: #172033;
      --muted: #647084;
      --line: #dce3ef;
      --primary: #0f766e;
      --primary-soft: #dff5f1;
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
    .tabs {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }
    button, input {
      font: inherit;
    }
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
    .result.good { border-color: var(--good); background: var(--good-soft); color: var(--good); }
    .result.bad { border-color: var(--bad); background: var(--bad-soft); color: var(--bad); }
    .actions {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 12px;
    }
    .secondary {
      background: #fff;
    }
    .hidden {
      display: none;
    }
    @media (min-width: 720px) {
      h1 { font-size: 24px; }
      .options.two-col { grid-template-columns: 1fr 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1>自然辩证法刷题</h1>
    <nav class="tabs" aria-label="功能">
      <button class="tab active" id="bankTab" type="button">所有题库</button>
      <button class="tab" id="quizTab" type="button">随机出题</button>
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
  </main>
  <script>
    const state = { questions: [], current: null, answered: false, total: 0, right: 0 };
    const bankTab = document.getElementById("bankTab");
    const quizTab = document.getElementById("quizTab");
    const bankView = document.getElementById("bankView");
    const quizView = document.getElementById("quizView");
    const bankList = document.getElementById("bankList");
    const bankCount = document.getElementById("bankCount");
    const search = document.getElementById("search");
    const score = document.getElementById("score");
    const quizCard = document.getElementById("quizCard");

    function escapeHtml(value) {
      return String(value || "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
      }[char]));
    }

    function optionHtml(options, correctAnswer = "") {
      return Object.entries(options).map(([letter, text]) => {
        const cls = letter === correctAnswer ? "option correct" : "option";
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
          <div class="options two-col">${optionHtml(item.options, item.answer)}</div>
          <div class="result">正确答案：${escapeHtml(item.answer)}. ${escapeHtml(item.correctText)}</div>
          ${item.note ? `<div class="result">${escapeHtml(item.note)}</div>` : ""}
        </article>
      `).join("");
    }

    function renderScore() {
      score.textContent = `已答 ${state.total} 题，正确 ${state.right} 题`;
    }

    function showQuizQuestion() {
      state.current = state.questions[Math.floor(Math.random() * state.questions.length)];
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
          <div class="actions">
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
      bankTab.classList.toggle("active", isBank);
      quizTab.classList.toggle("active", !isBank);
      bankView.classList.toggle("hidden", !isBank);
      quizView.classList.toggle("hidden", isBank);
      if (!isBank && !state.current) showQuizQuestion();
    }

    async function loadQuestions() {
      const res = await fetch("/api/questions");
      state.questions = await res.json();
      renderBank();
      renderScore();
    }

    bankTab.addEventListener("click", () => setView("bank"));
    quizTab.addEventListener("click", () => setView("quiz"));
    search.addEventListener("input", renderBank);
    document.getElementById("clearSearch").addEventListener("click", () => {
      search.value = "";
      renderBank();
      search.focus();
    });

    loadQuestions().catch(() => {
      bankCount.textContent = "题库加载失败，请检查电脑上的服务是否仍在运行。";
    });
  </script>
</body>
</html>
"""


class MobileQuizHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("{} - {}".format(self.address_string(), fmt % args))

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            body = INDEX_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/api/questions":
            json_response(self, all_questions())
        elif path == "/api/random":
            json_response(self, random.choice(all_questions()))
        else:
            json_response(self, {"error": "Not found"}, 404)


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


def main():
    parser = argparse.ArgumentParser(description="自然辩证法手机刷题网页")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), MobileQuizHandler)
    print("自然辩证法刷题网页已启动：http://{}:{}/".format(args.host, args.port))
    print("手机和电脑连接同一个 Wi-Fi 后，用电脑局域网 IP 访问。按 Ctrl+C 停止。")
    server.serve_forever()


if __name__ == "__main__":
    main()
