export function initCarousels(root = document) {
  root.querySelectorAll("[data-carousel]").forEach(setupCarousel);
}

function setupCarousel(carousel) {
  const track = carousel.querySelector("[data-carousel-track]");
  const prev = carousel.querySelector("[data-carousel-prev]");
  const next = carousel.querySelector("[data-carousel-next]");
  if (!track || !prev || !next) return;

  const step = () => {
    const item = track.firstElementChild;
    const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    return item ? item.getBoundingClientRect().width + gap : track.clientWidth;
  };

  const go = (direction) => {
    const max = track.scrollWidth - track.clientWidth;
    if (max <= 1) return;
    if (direction > 0 && track.scrollLeft >= max - 1) {
      track.scrollTo({ left: 0 });
    } else if (direction < 0 && track.scrollLeft <= 1) {
      track.scrollTo({ left: max });
    } else {
      track.scrollBy({ left: direction * step() });
    }
  };

  prev.addEventListener("click", () => go(-1));
  next.addEventListener("click", () => go(1));
}
