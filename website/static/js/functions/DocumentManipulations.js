const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const filesDisplay = document.getElementById("filesDisplay");
const sendButton = document.querySelector(".send");

let allFiles = [];

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
  addFiles(files);
});

dropZone.addEventListener("click", (event) => {
  if (!event.target.classList.contains("removeFile")) {
    fileInput.click();
  } else {
    const element = event.target.parentElement;

    for (let i = 0; i < allFiles.length; i++) {
      if (allFiles[i].name == element.innerText) {
        allFiles.splice(i, 1);
        element.remove();
        break;
      }
    }
  }
});

fileInput.addEventListener("change", (e) => {
  const files = e.target.files;
  addFiles(files);
});

function addFiles(files) {
  for (let i = 0; i < files.length; i++) {
    if (
      /* mudar logica depois */
      files[i].type === "application/pdf" &&
      !allFiles.some((f) => f.name === files[i].name)
    ) {
      allFiles.push(files[i]);
    }
  }
  displayFiles();
}

function displayFiles() {
  filesDisplay.innerHTML = "";
  allFiles.forEach((file) => {
    const currentFile = document.createElement("li");
    currentFile.className = "current-file row";
    currentFile.innerHTML = `<div style="width:90%; overflow-wrap: break-word;">${file.name}</div>`;

    const new_button = document.createElement("div");
    new_button.className = "bi bi-x-square float-right removeFile h-25";
    currentFile.appendChild(new_button);

    filesDisplay.appendChild(currentFile);
  });
}

$(() => {
  let oldIndex;
  $(filesDisplay).sortable({
    start: function (_, ui) {
      oldIndex = ui.item.index();
    },
    stop: function (_, ui) {
      const movedFile = allFiles.splice(oldIndex, 1)[0];

      allFiles.splice(ui.item.index(), 0, movedFile);
    },
  });
});

$(filesDisplay).disableSelection();

sendButton.addEventListener("click", () => {
  if (allFiles.length) {
    const formData = new FormData();

    allFiles.forEach((file) => {
      formData.append("filesList", file);
    });

    /* editar para função correta, dependendo da pagina que estou */
    fetch("/api/merge_pdf", {
      method: "POST",
      headers: {
        "X-CSRFToken": token,
      },
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("File upload failed");
        }
      })
      .then((data) => {
        console.log("Server response:", data);
        alert(data);
      })
      .catch((_) => {
        alert("Não foi possível concluir a operação");
      });
  } else {
    alert("Adicione arquivo");
  }
});

dropZone.addEventListener("change", () => {
  sendButton.disabled = dropZone.getElementsByTagName("li").length
    ? false
    : true;
});
