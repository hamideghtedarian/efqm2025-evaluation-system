async function saveAssessmentToServer() {
    const company = document.getElementById("companyName").value;
    const criterion = document.getElementById("criteriaDropdown").value;

    if (!company || company.trim() === "") {
        alert("لطفاً نام شرکت را وارد کنید.");
        return;
    }

    // نمونه ساده: بعداً گسترش می‌دهیم
    const payload = {
        company: company,
        assessment: {
            criterion: criterion,
            timestamp: new Date().toISOString(),
            notes: "این بخش بعداً با نقاط قوت و فرصت بهبود پر می‌شود."
        }
    };

    const response = await fetch("/api/save-assessment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (result.message === "Saved") {
        alert("✔️ ارزیابی با موفقیت ذخیره شد");
    } else {
        alert("❌ خطا در ذخیره‌سازی: " + result.error);
    }
}
