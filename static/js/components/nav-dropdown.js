/* Submenu do item "Startups": abre ao clicar no botão; fecha com Esc, clique fora ou perda de foco. */
export function initNavDropdowns(root = document) {
  const dropdowns = [...root.querySelectorAll("[data-nav-dropdown]")];
  if (!dropdowns.length) return;

  const parts = (dropdown) => ({
    toggle: dropdown.querySelector(".main-nav__toggle"),
    menu: dropdown.querySelector(".main-nav__submenu"),
  });

  const setOpen = (dropdown, open) => {
    const { toggle, menu } = parts(dropdown);
    toggle.setAttribute("aria-expanded", String(open));
    dropdown.classList.toggle("is-open", open);
    menu.hidden = !open;
  };

  const closeAll = (except) => {
    dropdowns.forEach((dropdown) => {
      if (dropdown !== except) setOpen(dropdown, false);
    });
  };

  dropdowns.forEach((dropdown) => {
    const { toggle } = parts(dropdown);

    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      closeAll(dropdown);
      setOpen(dropdown, open);
    });

    toggle.addEventListener("keydown", (event) => {
      if (event.key === "ArrowDown") {
        event.preventDefault();
        setOpen(dropdown, true);
        dropdown.querySelector(".main-nav__sublink")?.focus();
      }
    });

    dropdown.addEventListener("focusout", (event) => {
      if (!dropdown.contains(event.relatedTarget)) setOpen(dropdown, false);
    });
  });

  document.addEventListener("click", (event) => {
    dropdowns.forEach((dropdown) => {
      if (!dropdown.contains(event.target)) setOpen(dropdown, false);
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    dropdowns.forEach((dropdown) => {
      if (dropdown.classList.contains("is-open")) {
        setOpen(dropdown, false);
        if (dropdown.contains(document.activeElement)) parts(dropdown).toggle.focus();
      }
    });
  });
}
