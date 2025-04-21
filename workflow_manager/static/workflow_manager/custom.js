console.log("✅ custom.js loaded and running!");

function renderTemplateFields() {
    console.log("prefillVars:", prefillVars);
    const selector = document.getElementById("template-selector");
    const selected = selector.value;
    const container = document.getElementById("template-fields");
    container.innerHTML = "";

    if (!selected || !templateVars[selected]) return;

    templateVars[selected].forEach(field => {
        const label = document.createElement("label");
        label.textContent = field.charAt(0).toUpperCase() + field.slice(1) + ":";
        const input = document.createElement("input");
        input.name = field;
        input.required = true;

        // Prefill if available
        if (prefillVars && prefillVars[field]) {
            input.value = prefillVars[field];
        } else if (field === "start_date") {
            input.value = new Date().toISOString().split("T")[0];
        }

        if (field === "retry_delay") {
            input.placeholder = "e.g. timedelta(minutes=5)";
        }

        container.appendChild(label);
        container.appendChild(document.createElement("br"));
        container.appendChild(input);
        container.appendChild(document.createElement("br"));
        container.appendChild(document.createElement("br"));
    });
}


document.addEventListener("DOMContentLoaded", () => {
    console.log("JS loaded. Attaching onchange listener...");
    const selector = document.getElementById("template-selector");
    if (selector) {
        selector.addEventListener("change", () => {
            console.log("Template changed → triggering renderTemplateFields()");
            renderTemplateFields();
        });

        //FIX: call once on load if pre-selected (from URL or DB)
        if (selector.value && templateVars[selector.value]) {
            console.log("Template pre-selected → auto rendering fields");
            renderTemplateFields();
        } else {
            console.warn("No template selected on load.");
        }
    } else {
        console.error("Could not find #template-selector");
    }
});

