const FONT_KEY = "ypetec:font-scale";
const CONTRAST_KEY = "ypetec:contrast";
const SCALES = [87.5, 100, 112.5, 125];
const DEFAULT_SCALE = 100;

export function initAccessibility(root = document) {
  const html = document.documentElement;
  let scale = Number(localStorage.getItem(FONT_KEY)) || DEFAULT_SCALE;
  const contrastBtn = root.querySelector('[data-a11y="contrast"]');

  const applyScale = () => {
    html.style.fontSize = scale === DEFAULT_SCALE ? "" : `${scale}%`;
    localStorage.setItem(FONT_KEY, String(scale));
  };

  const applyContrast = (on) => {
    html.classList.toggle("high-contrast", on);
    contrastBtn?.setAttribute("aria-pressed", String(on));
    localStorage.setItem(CONTRAST_KEY, on ? "1" : "0");
  };

  const shift = (delta) => {
    const index = SCALES.indexOf(scale);
    const nextIndex = Math.min(SCALES.length - 1, Math.max(0, (index === -1 ? 1 : index) + delta));
    scale = SCALES[nextIndex];
    applyScale();
  };

  root.addEventListener("click", (event) => {
    const button = event.target.closest("[data-a11y]");
    if (!button) return;
    const action = button.dataset.a11y;
    if (action === "font-up") shift(1);
    else if (action === "font-down") shift(-1);
    else if (action === "font-reset") {
      scale = DEFAULT_SCALE;
      applyScale();
    } else if (action === "contrast") {
      applyContrast(!html.classList.contains("high-contrast"));
    }
  });

  applyScale();
  applyContrast(localStorage.getItem(CONTRAST_KEY) === "1");
}
