document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('gymForm');
    const generateBtn = document.getElementById('generateBtn');
    const resultsPlaceholder = document.getElementById('resultsPlaceholder');
    const resultsContent = document.getElementById('resultsContent');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const planOutput = document.getElementById('planOutput');
    const copyBtn = document.getElementById('copyBtn');
    const printBtn = document.getElementById('printBtn');

    let goalValue = '';
    let fitnessLevel = '';
    let rawMarkdown = '';

    // Goal buttons
    document.querySelectorAll('.goal-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.goal-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            goalValue = btn.dataset.value;
            document.getElementById('goal').value = goalValue;
            document.getElementById('customGoal').value = '';
        });
    });

    // Custom goal input
    document.getElementById('customGoal').addEventListener('input', (e) => {
        if (e.target.value.trim()) {
            document.querySelectorAll('.goal-btn').forEach(b => b.classList.remove('active'));
            goalValue = e.target.value.trim();
            document.getElementById('goal').value = goalValue;
        } else if (goalValue) {
            document.getElementById('goal').value = goalValue;
        }
    });

    // Level buttons
    document.querySelectorAll('.level-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            fitnessLevel = btn.dataset.value;
            document.getElementById('fitness_level').value = fitnessLevel;
        });
    });

    // Days slider
    const daysSlider = document.getElementById('days_per_week');
    const daysDisplay = document.getElementById('daysDisplay');
    daysSlider.addEventListener('input', () => {
        daysDisplay.textContent = daysSlider.value;
    });

    // Duration buttons
    document.querySelectorAll('.duration-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.duration-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('duration').value = btn.dataset.value;
        });
    });

    // Equipment chips
    document.querySelectorAll('.equipment-chip input').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
        });
    });

    function getEquipment() {
        const checked = [];
        document.querySelectorAll('.equipment-chip input:checked').forEach(cb => {
            checked.push(cb.value);
        });
        return checked.join(', ');
    }

    function showLoading() {
        resultsPlaceholder.style.display = 'none';
        resultsContent.style.display = 'none';
        loadingOverlay.style.display = 'flex';
    }

    function showResults() {
        loadingOverlay.style.display = 'none';
        resultsPlaceholder.style.display = 'none';
        resultsContent.style.display = 'block';
    }

    function renderMarkdown(text, streaming = false) {
        let html = marked.parse(text);
        planOutput.innerHTML = html;
        if (streaming) {
            planOutput.classList.add('streaming-cursor');
        } else {
            planOutput.classList.remove('streaming-cursor');
        }
    }

    // Form submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const goal = document.getElementById('goal').value.trim();
        const fitness = document.getElementById('fitness_level').value;

        if (!goal) {
            showValidationError('Please select or enter your fitness goal.');
            return;
        }
        if (!fitness) {
            showValidationError('Please select your fitness level.');
            return;
        }

        const payload = {
            goal: goal,
            fitness_level: fitness,
            days_per_week: document.getElementById('days_per_week').value,
            duration: document.getElementById('duration').value,
            equipment: getEquipment(),
            age: document.getElementById('age').value,
            injuries: document.getElementById('injuries').value,
            additional: document.getElementById('additional').value
        };

        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        showLoading();

        rawMarkdown = '';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.error || 'Failed to generate plan.');
            }

            showResults();
            planOutput.innerHTML = '';

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop();

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            if (data.error) {
                                planOutput.innerHTML = `<div class="error-message"><i class="fas fa-circle-exclamation"></i> ${data.error}</div>`;
                                planOutput.classList.remove('streaming-cursor');
                                break;
                            }
                            if (data.done) {
                                renderMarkdown(rawMarkdown, false);
                                break;
                            }
                            if (data.content) {
                                rawMarkdown += data.content;
                                renderMarkdown(rawMarkdown, true);
                            }
                        } catch (e) {
                        }
                    }
                }
            }

            renderMarkdown(rawMarkdown, false);

        } catch (err) {
            showResults();
            planOutput.innerHTML = `<div class="error-message"><i class="fas fa-circle-exclamation"></i> ${err.message}</div>`;
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> Generate My Gym Plan';
        }
    });

    function showValidationError(msg) {
        const existing = document.querySelector('.validation-error');
        if (existing) existing.remove();
        const div = document.createElement('div');
        div.className = 'error-message validation-error';
        div.innerHTML = `<i class="fas fa-circle-exclamation"></i> ${msg}`;
        form.appendChild(div);
        setTimeout(() => div.remove(), 4000);
    }

    // Copy button
    copyBtn.addEventListener('click', async () => {
        if (!rawMarkdown) return;
        try {
            await navigator.clipboard.writeText(rawMarkdown);
            copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
                copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
            }, 2000);
        } catch (e) {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
        }
    });

    // Print button
    printBtn.addEventListener('click', () => {
        if (!rawMarkdown) return;
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <title>My Gym Plan</title>
                <style>
                    body { font-family: Georgia, serif; max-width: 800px; margin: 40px auto; color: #222; line-height: 1.6; }
                    h1, h2 { color: #4f46e5; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; }
                    h3 { color: #f59e0b; }
                    table { width: 100%; border-collapse: collapse; margin: 16px 0; }
                    th { background: #e0e7ff; padding: 10px; text-align: left; }
                    td { padding: 8px 10px; border: 1px solid #e5e7eb; }
                    tr:nth-child(even) td { background: #f9fafb; }
                    .header { text-align: center; margin-bottom: 32px; }
                </style>
            </head>
            <body>
                <div class="header"><h1>My Gym Plan</h1><p>Generated by GymAI</p></div>
                ${planOutput.innerHTML}
            </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    });
});
