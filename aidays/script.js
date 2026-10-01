// мобильное меню
const burger = document.getElementById("burger");
const menu = document.getElementById("menu");
burger.addEventListener("click", () => {
  burger.classList.toggle("is-open");
  menu.classList.toggle("is-open");
});
menu.querySelectorAll("a").forEach((a) =>
  a.addEventListener("click", () => {
    burger.classList.remove("is-open");
    menu.classList.remove("is-open");
  }),
);

// таймер до начала конференции
const start = new Date("2026-11-20T10:00:00+03:00").getTime();
const cells = Object.fromEntries(
  [...document.querySelectorAll("#timer [data-t]")].map((el) => [el.dataset.t, el]),
);
const pad = (n) => String(n).padStart(2, "0");
function tick() {
  const left = Math.max(0, start - Date.now());
  const s = Math.floor(left / 1000);
  cells.d.textContent = pad(Math.floor(s / 86400));
  cells.h.textContent = pad(Math.floor((s % 86400) / 3600));
  cells.m.textContent = pad(Math.floor((s % 3600) / 60));
  cells.s.textContent = pad(s % 60);
}
tick();
setInterval(tick, 1000);

// вкладки программы
document.querySelectorAll(".tab").forEach((tab) =>
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("is-active", t === tab));
    document.querySelectorAll(".program").forEach((p) =>
      p.classList.toggle("is-active", p.dataset.day === tab.dataset.day),
    );
  }),
);
