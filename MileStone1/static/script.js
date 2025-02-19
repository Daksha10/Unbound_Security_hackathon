document.getElementById("fetchModels").addEventListener("click", function () {
    fetch("/models")
        .then(response => response.json())
        .then(data => {
            let modelList = document.getElementById("modelList");
            modelList.innerHTML = "";  // Clear previous data
            data.forEach(model => {
                let li = document.createElement("li");
                li.textContent = model;
                modelList.appendChild(li);
            });
        })
        .catch(error => console.error("Error fetching models:", error));
});
