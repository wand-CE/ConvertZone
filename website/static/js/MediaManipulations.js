const dropZone = document.getElementById("dropZone");
const pdfInput = document.getElementById("pdfInput");
const pdfDisplay = document.getElementById("pdfDisplay");

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("bg-light");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("bg-light");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("bg-light");
  const files = e.dataTransfer.files;
  displayFiles(files);
  pdfInput.files = files;
});

dropZone.addEventListener("click", () => {
  pdfInput.click();
});

pdfInput.addEventListener("change", (e) => {
  const files = e.target.files;
  displayFiles(files);
});

function displayFiles(files) {
  pdfDisplay.innerHTML = "";
  for (let i = 0; i < files.length; i++) {
    if (files[i].type === "application/pdf") {
      const pdfFile = document.createElement("div");
      pdfFile.className = "pdf-file";
      pdfFile.innerHTML = '<div class="pdf-icon">PDF</div>' + files[i].name;
      pdfDisplay.appendChild(pdfFile);
    }
  }
}

// Para permitir a reordenação dos arquivos, podemos usar uma biblioteca como o Sortable.js.
// Isso é apenas um exemplo básico, e você precisaria incorporar a biblioteca para torná-lo totalmente funcional.
// ... (restante do código anterior)

let allFiles = []; // armazena todos os arquivos

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("bg-light");
  const files = e.dataTransfer.files;
  addFiles(files);
});

pdfInput.addEventListener("change", (e) => {
  const files = e.target.files;
  addFiles(files);
});

function addFiles(files) {
  for (let i = 0; i < files.length; i++) {
    if (files[i].type === "application/pdf" && !allFiles.includes(files[i])) {
      // verifica se o arquivo já foi adicionado
      allFiles.push(files[i]);
    }
  }
  displayFiles();
}

function displayFiles() {
  pdfDisplay.innerHTML = ""; // limpa a visualização anterior
  for (let i = 0; i < allFiles.length; i++) {
    const pdfFile = document.createElement("div");
    pdfFile.className = "pdf-file";
    pdfFile.innerHTML = '<div class="pdf-icon">PDF</div>' + allFiles[i].name;
    pdfDisplay.appendChild(pdfFile);
  }
}

// ... (restante do código anterior)

// torna a lista de arquivos ordenável
const sortable = new Sortable(pdfDisplay, {
  animation: 150,
  onStart(evt) {
    // Quando o arrastar começa, destacamos o item que está sendo movido
    evt.item.classList.add("bg-light");
  },
  onEnd(evt) {
    // Quando o arrastar termina, removemos o destaque e atualizamos a ordem dos arquivos em allFiles
    evt.item.classList.remove("bg-light");
    const [movedFile] = allFiles.splice(evt.oldIndex, 1);
    allFiles.splice(evt.newIndex, 0, movedFile);
  },
});

// ...

// ...
