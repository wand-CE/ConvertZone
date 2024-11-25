const form_files = document.querySelector(".form_files").dataset;
const accept_files = form_files.accept_files.split(",");

const current_url = form_files.url_function;
const limit = parseInt(form_files.multiple);
const service_type = form_files.service_type;

const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const filesDisplay = document.getElementById("filesDisplay");
const sendButton = document.querySelector(".send");

fileInput.multiple = !!limit;

let allFiles = [];

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.remove("bg-white");
    dropZone.classList.add("bg-light");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("bg-light");
    dropZone.classList.add("bg-white");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("bg-light");
    dropZone.classList.add("bg-white");
    const files = e.dataTransfer.files;
    addFiles(files);
});

dropZone.addEventListener("click", (event) => {
    if (!event.target.classList.contains("removeFile")) {
        fileInput.click();
    } else {
        const element = event.target.parentElement;

        for (let i = 0; i < allFiles.length; i++) {
            if (allFiles[i].name === element.innerText) {
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

function changeSendButton() {
    sendButton.disabled = !dropZone.getElementsByTagName("li").length;
}

function addFiles(files) {
    if (limit === 0) {
        if (files.length && (accept_files.includes(files[0].type) || files[0].type.startsWith("image/"))) {
            allFiles = [files[0]];
        }
    } else {
        for (let i = 0; i < files.length; i++) {
            if (accept_files.includes(files[i].type) && !allFiles.some((f) => f.name === files[i].name)) {
                allFiles.push(files[i]);
            }
        }
    }
    displayFiles();
}

function displayFiles() {
    filesDisplay.innerHTML = "";
    allFiles.forEach((file) => {

        const currentFile = document.createElement("li");
        currentFile.className = "current-file row";

        const divFile = document.createElement('div');

        divFile.style.width = "90%";
        divFile.style.overflowWrap = "break-word";
        divFile.textContent = file.name;
        currentFile.appendChild(divFile);

        const new_button = document.createElement("div");
        new_button.className = "bi bi-x float-right removeFile h-25";
        new_button.style.color = "red";
        currentFile.appendChild(new_button);

        filesDisplay.appendChild(currentFile);
        changeSendButton();
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
                }
                throw new Error("Erro Interno");

            })
            .then((data) => {
                if (data['error']) {
                    throw new Error(data['error']);
                }

                let path = data["path_file"];
                let fileName = data["file_name"];
                let extension = {
                    docx: "/static/img/word.png",
                    pdf: "/static/img/pdf.png",
                    zip: "/static/img/zip.png",
                    mp3: "/static/img/mp3.png",
                    png: `/api/download/${path}`,
                };

                document.querySelector("#show_file").children[0].src = extension[fileName.split(".")[1]];

                document.querySelector("#file_name").innerText = fileName;
                document.querySelector("#download_button").href = `/api/download/${path}`;

                load_element_visible.style.display = "none";

                document.querySelector("#finalZoneChildren").style.display = "flex";
            })
            .catch((error) => {
                load_element_visible.style.display = "none";
                alert(error.message);
            });
    } else {
        alert("Adicione arquivo");
        load_element_visible.style.display = "none";
    }
});

// dropZone.addEventListener("change", () => {
//     changeSendButton();
// });
