const form_files = document.querySelector(".form_files").dataset;

const current_url = form_files.url_function;

const sendButton = document.querySelector(".send");
const textZone = document.getElementById("textZone");

textZone.addEventListener("input", (e) => {
  sendButton.disabled = e.target.value.length ? false : true;
});

sendButton.addEventListener("click", () => {
  const load_element_visible = document.querySelector(".loader-wrapper");

  load_element_visible.style.display = "flex";

  const formData = new FormData();

  formData.append("text", textZone.value);

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
        docx: "/static/img/word.png",
        pdf: "/static/img/pdf.png",
        zip: "/static/img/zip.png",
        mp3: "/static/img/mp3.png",
        png: `/api/download/${path}`,
      };

      document.querySelector("#show_file").children[0].src =
        extension[fileName.split(".")[1]];

      document.querySelector("#file_name").innerText = fileName;
      document.querySelector("#download_button").href = `/api/download/${path}`;

      load_element_visible.style.display = "none";

      document.querySelector("#finalZoneChildren").style.display = "flex";
    })
    .catch((_) => {
      load_element_visible.style.display = "none";
      alert("Não foi possível concluir a operação");
    });
});
