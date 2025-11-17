async function loadSavedSubcriterion(company, criterion, subcriterion) {
    try {
        const response = await fetch(`/data/companies/${company}/assessment.json`);
        if (!response.ok) return;

        const data = await response.json();

        if (
            data.criteria &&
            data.criteria[criterion] &&
            data.criteria[criterion][subcriterion]
        ) {
            const sub = data.criteria[criterion][subcriterion];

            document.getElementById("strengths").value = sub.strengths.join("\n");
            document.getElementById("opportunities").value = sub.opportunities.join("\n");

            document.getElementById("radar_approach").value = sub.radar.approach;
            document.getElementById("radar_deployment").value = sub.radar.deployment;
            document.getElementById("radar_ar").value = sub.radar.assessment_refinement;
            document.getElementById("radar_results").value = sub.radar.results;
        }
    } catch (e) {
        console.log("No saved data yet.");
    }
}
