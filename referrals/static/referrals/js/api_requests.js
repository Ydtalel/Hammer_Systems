document.addEventListener("DOMContentLoaded", function () {
  const accordionItems = document.querySelectorAll(".accordion-item");

  accordionItems.forEach(function (item) {
    const reqBody = item.children[1].querySelector('.accordion-body');
    const button = reqBody.querySelector('.btn.btn-outline-primary.btn-send');
    const urlInput = reqBody.querySelectorAll('.form-control')[0];
    const requestTextarea = reqBody.querySelectorAll('.form-control')[1];
    const responseElement = reqBody.querySelector('.response');

    const requestMethod = item.children[0].querySelector('.accordion-button').innerText.split("/")[0].trim().toUpperCase();

    button.addEventListener("click", function () {
      const requestBody = requestTextarea.value;
      const url = urlInput.value;

      try {
        let jsonData = {};
        if (requestMethod !== "GET") {
          jsonData = JSON.parse(requestBody);
        }
        sendRequest(jsonData, url, requestMethod, responseElement);
      } catch (error) {
        console.error("Invalid JSON format");
      }
    });
  });

  function sendRequest(data, url, method, responseElement) {
    const requestOptions = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      }
    };

    if (method !== "GET") {
      requestOptions.body = JSON.stringify(data);
    }

    fetch(url, requestOptions)
      .then((response) => response.json())
      .then((responseData) => {
        const responseText = `
        <div class="mb-3">
            <div class="card-body">
            <p class="card-text">Message: ${JSON.stringify(responseData, null, 2)}</p>
            </div>
         </div>
        `
        responseElement.innerHTML = responseText;
      })
      .catch((error) => {
        console.error("Request failed", error);
      });
  }
});
