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
  const pool = state.questions.map((item) => item.correctText).filter((item) => item !== question.correctText);
  const picked = shuffle([...new Set(pool)]).slice(0, 3);
  const values = shuffle([...picked, question.correctText]);
  return Object.fromEntries(values.map((text, index) => [String.fromCharCode(65 + index), text]));
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

function renderScore() {
  score.textContent = `已答 ${state.total} 题，正确 ${state.right} 题`;
}

function showQuizQuestion() {
  const base = state.questions[Math.floor(Math.random() * state.questions.length)];
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
  const res = await fetch("./questions.json");
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
  bankCount.textContent = "题库加载失败，请确认通过网页服务或 GitHub Pages 打开。";
});
