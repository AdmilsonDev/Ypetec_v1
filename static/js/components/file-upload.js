/** Mostra o nome do arquivo escolhido nos campos de anexo do formulário de incubação. */
export function initFileUploads() {
  document.querySelectorAll("[data-upload]").forEach((upload) => {
    const input = upload.querySelector('input[type="file"]');
    const name = upload.querySelector("[data-upload-name]");
    if (!input || !name) return;

    input.addEventListener("change", () => {
      const file = input.files && input.files[0];
      name.textContent = file ? file.name : "";
      name.hidden = !file;
      upload.classList.toggle("is-filled", Boolean(file));
    });
  });
}
