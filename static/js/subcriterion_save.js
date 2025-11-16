async function saveSubcriterion(company, criterion, subcriterion) {
    const strengths = document.getElementById("strengths").value.split("\n");
    const opportunities = document.getElementById("opportunities").value.split("\n");

    const radar = {
        approach: parseInt(document.getElementById("radar_approach").value) || 0,
        deployment: parseInt(document.getElementById("radar_deployment").value) || 0,
        assessment_refinement: parseInt(document.getElementById("radar_ar").value) || 0,
        results: parseInt(document.getElementById("radar_results").value) || 0
    };

    const payload = {
        company,
        criterion,
        subcriterion,
        strengths,
        opportunities,
        radar
    };

    const response = await fetch("/api/save-subcriterion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const result = await response.json();

    alert(result.message);
}
