async function loadCriteria() {
    try {
        const response = await fetch("/data/criteria/efqm2025_full_model.json");
        const data = await response.json();
        return data.criteria;
    } catch (error) {
        console.error("Error loading EFQM Model:", error);
        return [];
    }
}

// نمایش لیست معیارها در فرم ارزیابی
async function populateCriteriaDropdown() {
    const criteria = await loadCriteria();
    const dropdown = document.getElementById("criteriaDropdown");

    dropdown.innerHTML = ""; 

    criteria.forEach(c => {
        const option = document.createElement("option");
        option.value = c.code;
        option.textContent = `${c.code} — ${c.title_fa}`;
        dropdown.appendChild(option);
    });
}

// نمایش زیرمعیارها بر اساس انتخاب معیار
async function populateSubcriteria() {
    const selectedCode = document.getElementById("criteriaDropdown").value;
    const criteria = await loadCriteria();

    const selectedCriterion = criteria.find(c => c.code === selectedCode);
    const listContainer = document.getElementById("subcriteriaList");

    listContainer.innerHTML = "";

    selectedCriterion.subcriteria.forEach(sc => {
        const item = document.createElement("div");
        item.classList.add("subcriteria-item");
        item.innerHTML = `
            <strong>${sc.code}</strong> — ${sc.title_fa}
            <p class="sub-desc">${sc.description_fa}</p>
        `;
        listContainer.appendChild(item);
    });
}

// بارگذاری اولیه
window.onload = async function () {
    await populateCriteriaDropdown();
    await populateSubcriteria();
};
