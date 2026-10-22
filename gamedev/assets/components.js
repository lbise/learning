/* Reusable lesson components. Include with:
     <script src="../assets/components.js" defer></script>

   QUIZ: multiple choice, instant feedback, options shuffled on load.
     <div class="quiz">
       <p class="q">Question?</p>
       <button data-why="Why this is wrong">Option A</button>
       <button data-correct data-why="Why this is right">Option B</button>
       <p class="feedback"></p>
     </div>
     First click counts toward the score. Wrong picks can be retried.
     Optional page score: <p class="score" id="score"></p>

   RECALL: try to answer from memory, then reveal.
     <div class="recall">
       <p class="q">Question?</p>
       <details><summary>Show answer</summary>Answer…</details>
     </div>

   CHECKLIST: real-world steps, ticks persist in localStorage.
     <ol class="checklist" id="unique-id">
       <li>Step one</li>
       <li>Step two</li>
     </ol>
     <p class="progress" data-for="unique-id"></p>
*/
(function () {
  "use strict";

  const shuffle = (arr) => {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  };

  /* ---------- Quiz ---------- */
  const quizzes = [...document.querySelectorAll(".quiz")];
  const scoreEl = document.getElementById("score");
  let firstTryRight = 0;
  let answered = 0;

  const renderScore = () => {
    if (!scoreEl) return;
    scoreEl.textContent = answered === quizzes.length
      ? `Score: ${firstTryRight} / ${quizzes.length} on the first try`
      : `${answered} of ${quizzes.length} answered`;
  };

  quizzes.forEach((quiz) => {
    const buttons = [...quiz.querySelectorAll("button")];
    const feedback = quiz.querySelector(".feedback");
    const anchor = feedback || null;
    shuffle(buttons).forEach((b) => quiz.insertBefore(b, anchor));
    let attempted = false;

    buttons.forEach((btn) => {
      btn.type = "button";
      btn.addEventListener("click", () => {
        const correct = btn.hasAttribute("data-correct");
        if (!attempted) {
          attempted = true;
          answered++;
          if (correct) firstTryRight++;
          renderScore();
        }
        if (feedback) {
          feedback.className = "feedback " + (correct ? "right" : "wrong");
          feedback.textContent = (correct ? "Right. " : "Not quite. ") + (btn.dataset.why || "");
        }
        if (correct) {
          btn.classList.add("right");
          buttons.forEach((b) => (b.disabled = true));
        } else {
          btn.classList.add("wrong");
          btn.disabled = true;
        }
      });
    });
  });
  renderScore();

  /* ---------- Checklist ---------- */
  document.querySelectorAll(".checklist").forEach((list) => {
    const key = `gamedev:${location.pathname}:${list.id}`;
    const saved = JSON.parse(localStorage.getItem(key) || "[]");
    const items = [...list.children];
    const progress = document.querySelector(`.progress[data-for="${list.id}"]`);

    const update = () => {
      const state = items.map((li) => li.querySelector("input").checked);
      items.forEach((li, i) => li.classList.toggle("done", state[i]));
      localStorage.setItem(key, JSON.stringify(state));
      if (progress) {
        const n = state.filter(Boolean).length;
        progress.textContent = n === items.length
          ? `All ${n} steps done.`
          : `${n} of ${items.length} steps done`;
      }
    };

    items.forEach((li, i) => {
      const label = document.createElement("label");
      const box = document.createElement("input");
      box.type = "checkbox";
      box.checked = !!saved[i];
      box.addEventListener("change", update);
      const span = document.createElement("span");
      while (li.firstChild) span.appendChild(li.firstChild);
      label.append(box, span);
      li.appendChild(label);
    });
    update();
  });
})();
