document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const text = document.getElementById('emailText').value;
    const fileInput = document.getElementById('screenshotFile');
    const spf = document.getElementById('spfStatus').value;
    const dkim = document.getElementById('dkimStatus').value;

    const formData = new FormData();
    formData.append('text', text);
    formData.append('spf', spf);
    formData.append('dkim', dkim);

    if (fileInput.files[0]) {
        formData.append('file', fileInput.files[0]);
    }

    // UI Updates
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('resultsContent').classList.add('hidden');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Update UI with results
        document.getElementById('finalScore').textContent = data.fusion.final_threat_score;
        document.getElementById('threatLevel').textContent = data.fusion.threat_level;

        // Color coding
        const level = data.fusion.threat_level;
        const levelEl = document.getElementById('threatLevel');
        if (level === 'CRITICAL') levelEl.style.color = 'var(--danger)';
        else if (level === 'HIGH') levelEl.style.color = '#f97316'; // Orange
        else if (level === 'MODERATE') levelEl.style.color = '#eab308'; // Yellow
        else levelEl.style.color = 'var(--success)';

        document.getElementById('visionScore').textContent = data.vision.vision_score + '%';
        document.getElementById('nlpScore').textContent = data.nlp.nlp_score + '%';
        document.getElementById('forensicScore').textContent = data.forensics.forensic_score + '%';

        // Enrichment Updates
        const enrichmentScore = data.fusion.components.enrichment || 0;
        document.getElementById('enrichmentScore').textContent = Math.round(enrichmentScore) + '%';

        document.getElementById('domainAge').textContent = data.enrichment.domain_age_days + ' days';
        document.getElementById('domainRegistrar').textContent = data.enrichment.registrar;
        document.getElementById('domainReputation').textContent = data.enrichment.reputation_score + '/100';

        const tactics = data.enrichment.mitre_tactics;
        document.getElementById('mitreTactics').textContent = tactics.length > 0 ? tactics.join(', ') : 'None';

        document.getElementById('recommendation').textContent = data.fusion.recommendation;

    } catch (error) {
        console.error('Error:', error);
        alert('Analysis failed. Check console.');
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('resultsContent').classList.remove('hidden');
    }
});
