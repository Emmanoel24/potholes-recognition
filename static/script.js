const form = document.getElementById("uploadForm");
const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const browseLink = document.getElementById("browseLink");
const preview = document.getElementById("preview");
const detectBtn = document.getElementById("detectBtn");
const clearBtn = document.getElementById("clearBtn");
const loader = document.getElementById("loader");

function showPreview(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    preview.src = e.target.result;
    preview.style.display = "block";
    detectBtn.disabled = false;
  };
  reader.readAsDataURL(file);
}

browseLink.addEventListener("click", (e) => {
  e.preventDefault();
  fileInput.click();
});

fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;
  if (!file.type.startsWith("image/")) {
    alert("Please select an image.");
    return;
  }
  showPreview(file);
});

["dragenter", "dragover"].forEach((evt) => {
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropzone.style.borderColor = "#3c8eff";
  });
});
["dragleave", "drop"].forEach((evt) => {
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropzone.style.borderColor = "#2b3546";
  });
});
dropzone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (!file) return;
  if (!file.type.startsWith("image/")) {
    alert("Please drop an image file.");
    return;
  }
  fileInput.files = e.dataTransfer.files;
  showPreview(file);
});

clearBtn.addEventListener("click", () => {
  fileInput.value = "";
  preview.src = "";
  preview.style.display = "none";
  detectBtn.disabled = true;
});

form.addEventListener("submit", () => {
  // Show loading overlay when submitting
  loader.classList.remove("hidden");
});
