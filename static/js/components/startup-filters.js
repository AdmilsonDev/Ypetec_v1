// Envia o filtro de categoria assim que o usuário escolhe uma opção.
export function initStartupFilters() {
  document.querySelectorAll("[data-startup-filters]").forEach((form) => {
    const select = form.querySelector("select");
    if (!select) return;
    select.addEventListener("change", () => form.requestSubmit());
  });
}
