/** Diálogos nativos (<dialog data-dialog>): abrem como modal, fecham no botão, no fundo ou com Esc. */
export function initDialogs(root = document) {
  root.querySelectorAll("dialog[data-dialog]").forEach((dialog) => {
    if (typeof dialog.showModal !== "function") return;

    // O servidor entrega o diálogo já aberto (sem JS); aqui ele passa a modal, com fundo e foco preso.
    if (dialog.open) dialog.close();
    dialog.showModal();

    dialog.querySelectorAll("[data-dialog-close]").forEach((button) => {
      button.addEventListener("click", () => dialog.close());
    });

    // Clique no fundo escurecido (fora do painel) fecha.
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
  });
}
