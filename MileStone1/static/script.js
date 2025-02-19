document.getElementById("fetchModels").addEventListener("click", function () {
    fetch("/models")
        .then(response => response.json())
        .then(data => {
            let providerSelect = document.getElementById("provider");
            let modelSelect = document.getElementById("model");
            let rerouteMessage = document.querySelector(".reroute-message");

            providerSelect.innerHTML = `<option value="" disabled selected>Select a provider</option>`;
            modelSelect.innerHTML = `<option value="" disabled selected>Select a model</option>`;
            modelSelect.disabled = true; // Disable model dropdown initially

            let providers = [...new Set(data.map(m => m.provider))];

            // Populate provider dropdown
            providers.forEach(provider => {
                let option = document.createElement("option");
                option.value = provider;
                option.textContent = provider.charAt(0).toUpperCase() + provider.slice(1);
                providerSelect.appendChild(option);
            });

            // When a provider is selected, populate models dynamically
            providerSelect.addEventListener("change", function () {
                let selectedProvider = providerSelect.value;
                modelSelect.innerHTML = `<option value="" disabled selected>Select a model</option>`;
                modelSelect.disabled = false; // Enable model selection

                data
                    .filter(m => m.provider === selectedProvider)
                    .forEach(model => {
                        let option = document.createElement("option");
                        option.value = model.name;
                        option.textContent = model.name;
                        modelSelect.appendChild(option);
                    });
            });

            // Handle rerouting logic
            document.getElementById("submit").addEventListener("click", function () {
                let selectedModel = modelSelect.value;
                let prompt = document.getElementById("prompt").value;

                if (!selectedModel || !prompt.trim()) {
                    alert("Please select a model and enter a prompt.");
                    return;
                }

                fetch("/check_routing", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ model: selectedModel, prompt: prompt }),
                })
                    .then(response => response.json())
                    .then(result => {
                        if (result.redirected_model) {
                            rerouteMessage.textContent = `Your request was rerouted to: ${result.redirected_model}`;
                            modelSelect.value = result.redirected_model;
                        } else {
                            rerouteMessage.textContent = "No rerouting applied.";
                        }
                        sendPrompt(modelSelect.value, prompt);
                    })
                    .catch(error => console.error("Error checking rerouting:", error));
            });

            function sendPrompt(model, prompt) {
                fetch("/v1/chat/completions", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ model: model, prompt: prompt }),
                })
                    .then(response => response.json())
                    .then(data => {
                        document.querySelector(".response-container").innerText = data.response || "No response received.";
                    })
                    .catch(error => console.error("Error sending prompt:", error));
            }
        })
        .catch(error => console.error("Error fetching models:", error));
});
