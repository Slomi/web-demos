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

// переключатель месяц / год
const fmt = (n) => Number(n).toLocaleString("ru-RU");
document.querySelectorAll(".switch__btn").forEach((btn) =>
  btn.addEventListener("click", () => {
    document.querySelectorAll(".switch__btn").forEach((b) => b.classList.remove("is-active"));
    btn.classList.add("is-active");
    const period = btn.dataset.period;
    document.querySelectorAll(".plan__price span").forEach((el) => {
      el.textContent = fmt(el.dataset[period]);
    });
  }),
);

// появление блоков при прокрутке
const io = new IntersectionObserver(
  (entries) =>
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("is-visible");
        io.unobserve(e.target);
      }
    }),
  { threshold: 0.12 },
);
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
