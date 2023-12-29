const loading = document.querySelector(".loading");
const loadingBg = document.querySelector(".loading-background");

function generateSummary() {
  var inputText = document.getElementById("textInput").value;

  // Make a fetch request to the Flask API endpoint
  console.log(inputText);
  showLoading();
  fetch("https://text-summarize-7dlettdd4a-et.a.run.app/api/fromtext", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      full_text: inputText,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Display the result in the resultTextarea
      hideLoading();
      document.getElementById("resultTextarea").value = data.summarize;
      document.getElementById("tess").value = data.summarize;
    })
    .catch((error) => {
      hideLoading();
      console.error("Error:", error);
    });
}

function generateSummaryLink() {
  var inputLink = document.getElementById("linkInput").value;

  // Make a fetch request to the Flask API endpoint
  console.log(inputLink);
  showLoading();
  fetch("https://text-summarize-7dlettdd4a-et.a.run.app/api/fromnews", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      full_link: inputLink,
    }),
  })
    .then((response) => {
      if (response.status === 400) {
        Toastify({
          text: "Expected a BBC News 😰",
          duration: 3000,
          style: {
            background:
              "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",
            transform: "translate(0px, 0px); top: 15px",
          },
          close: true,
        }).showToast();
      } else if (response.status === 404) {
        Toastify({
          text: "News not found 😱",
          duration: 3000,
          style: {
            background:
              "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",
            transform: "translate(0px, 0px); top: 15px",
          },
          close: true,
        }).showToast();
      } else {
        return response.json();
      }
    })
    .then((data) => {
      // Display the result in the resultTextarea
      hideLoading();
      document.getElementById("resultFromLink").value = data.summarize;
      document.getElementById("tess").value = data.summarize;
    })
    .catch((error) => {
      hideLoading();
      console.log(error.message);
    });
}

//function used to show the loading
function showLoading() {
  loading.classList.add("loading-active");
  loadingBg.classList.add("loading-active");
}
//function used to hide the loading
function hideLoading() {
  loading.classList.remove("loading-active");
  setTimeout(function () {
    loadingBg.classList.remove("loading-active");
  }, 20);
}
