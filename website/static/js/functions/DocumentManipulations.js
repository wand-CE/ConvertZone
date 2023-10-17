const form_files = document.querySelector(".form_files").dataset;
const accept_files = form_files.accept_files.split(",");

const current_url = form_files.url_function;
const limit = parseInt(form_files.multiple);

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
        sendButton.disabled = dropZone.getElementsByTagName("li").length
          ? false
          : true;
        break;
      }
    }
  }
});

fileInput.addEventListener("change", (e) => {
  const files = e.target.files;
  if (limit === 0) {
    if (files.length) {
      allFiles = [files[0]];
      displayFiles();
    }
  } else {
    addFiles(files);
  }
});

function addFiles(files) {
  for (let i = 0; i < files.length; i++) {
    if (
      accept_files.includes(files[i].type) &&
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
    new_button.style.color = "red";
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
  const load_element_visible = document.querySelector(".loader-wrapper");

  if (allFiles.length) {
    load_element_visible.style.display = "flex";
    const formData = new FormData();

    allFiles.forEach((file) => {
      formData.append("files", file);
    });

    fetch(`/api/${current_url}`, {
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
        let path = data["path_file"];
        let fileName = data["file_name"];
        let extension = {
          docx: "word.png",
          pdf: "pdf.png",
          zip: "zip.png",
        };

        document.querySelector("#show_file").children[0].src = `/static/img/${
          extension[fileName.split(".")[1]]
        }`;
        document.querySelector("#file_name").innerText = fileName;
        document.querySelector(
          "#download_button"
        ).href = `/api/download/${path}`;

        load_element_visible.style.display = "none";

        document.querySelector("#finalZoneChildren").style.display = "flex";
      })
      .catch((_) => {
        load_element_visible.style.display = "none";
        alert("Não foi possível concluir a operação");
      });
  } else {
    alert("Adicione arquivo");
    load_element_visible.style.display = "none";
  }
});

dropZone.addEventListener("change", () => {
  sendButton.disabled = dropZone.getElementsByTagName("li").length
    ? false
    : true;
});
