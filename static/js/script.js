document.addEventListener('DOMContentLoaded', function() {
    const klaroForm = document.getElementById('klaro-form');
    const debugForm = document.getElementById('debug-form');
    const policyForm = document.getElementById('policy-form');
    const addConsentOptionButton = document.getElementById('add-consent-option');
    const consentOptionsContainer = document.getElementById('consent-options-container');
    const consentAnalyticsSection = document.getElementById('consent-analytics-section');

    // Function to add a new consent option input group
    function addConsentOption() {
        const consentOptionDiv = document.createElement('div');
        consentOptionDiv.className = 'consent-option';
        consentOptionDiv.innerHTML = `
            <label for="consent-name">Name:</label>
            <input type="text" name="consentName[]" required>
            <label for="consent-title">Title:</label>
            <input type="text" name="consentTitle[]" required>
            <label for="consent-description">Description:</label>
            <textarea name="consentDescription[]" required></textarea>
            <label for="consent-purposes">Purposes (comma-separated):</label>
            <input type="text" name="consentPurposes[]" required>
            <label for="consent-default">Default:</label>
            <select name="consentDefault[]">
                <option value="true">true</option>
                <option value="false" selected>false</option>
            </select>
            <label for="consent-required">Required:</label>
            <select name="consentRequired[]">
                <option value="true">true</option>
                <option value="false" selected>false</option>
            </select>
            <button type="button" class="remove-consent-option">Remove</button>
        `;
        consentOptionsContainer.appendChild(consentOptionDiv);

        // Attach event listener to the new remove button
        consentOptionDiv.querySelector('.remove-consent-option').addEventListener('click', function() {
            consentOptionsContainer.removeChild(consentOptionDiv);
        });
    }

    // Add initial consent option and event listener for adding more
    addConsentOption();
    addConsentOptionButton.addEventListener('click', addConsentOption);

    // Event listener for generating GTM template
    klaroForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(klaroForm);
        const klaroConfig = {
            language: formData.get('lang'),
            storageMethod: formData.get('storageMethod'),
            consentTitle: formData.get('consentTitle'),
            consentDescription: formData.get('consentDescription'),
            services: [] // To store individual consent options
        };

        // Get all consent options
        const consentOptions = klaroForm.querySelectorAll('.consent-option');
        consentOptions.forEach((option) => {
            const nameInputs = option.querySelectorAll('input[name="consentName[]"]');
            const titleInputs = option.querySelectorAll('input[name="consentTitle[]"]');
            const descriptionInputs = option.querySelectorAll('textarea[name="consentDescription[]"]');
            const purposesInputs = option.querySelectorAll('input[name="consentPurposes[]"]');
            const defaultSelects = option.querySelectorAll('select[name="consentDefault[]"]');
            const requiredSelects = option.querySelectorAll('select[name="consentRequired[]"]');

            for (let i = 0; i < nameInputs.length; i++) {
                klaroConfig.services.push({
                    name: nameInputs[i].value,
                    title: titleInputs[i].value,
                    description: descriptionInputs[i].value,
                    purposes: purposesInputs[i].value.split(',').map(purpose => purpose.trim()),
                    default: defaultSelects[i].value === 'true',
                    required: requiredSelects[i].value === 'true'
                });
            }
        });

        // Send the configuration to the server to generate GTM template
        fetch('/generate-gtm-template', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(klaroConfig)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('error-message').textContent = data.error;
                document.getElementById('gtm-template-output').style.display = 'none';
            } else {
                document.getElementById('gtm-template-code').textContent = data.template;
                document.getElementById('gtm-trigger-code').textContent = data.trigger;
                document.getElementById('gtm-variable-code').textContent = data.variable;
                document.getElementById('gtm-template-output').style.display = 'block';
                document.getElementById('error-message').textContent = '';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('error-message').textContent = 'An error occurred while generating the template.';
            document.getElementById('gtm-template-output').style.display = 'none';
        });
    });

    // Event listener for simulating consent choices
    debugForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const consentChoices = {
            analytics: document.getElementById('debug-analytics').checked,
            marketing: document.getElementById('debug-marketing').checked
            // Add more choices as needed
        };

        // Send consent choices to the server for simulation
        fetch('/simulate-consent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(consentChoices)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Log the simulation message
            // You can update the UI or show a message based on the simulation result
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Event listener for privacy policy form 
    policyForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(policyForm);

        // Send the form data to the server for processing
        fetch('/upload-policy', {
            method: 'POST',
            body: formData // No need to set Content-Type, it's handled automatically for FormData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // Handle error (e.g., display error message)
                console.error('Error uploading policy:', data.error);
                document.getElementById('error-message').textContent = data.error;
            } else {
                // Handle success (e.g., display success message, update UI)
                console.log(data.message); 
                document.getElementById('error-message').textContent = ''; // Clear any previous errors
                alert(data.message); // Or display a more user-friendly success message
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('error-message').textContent = 'An error occurred while uploading the file.';
        });
    });

    // Fetch and display consent analytics
    function fetchConsentAnalytics() {
        fetch('/consent-analytics')
            .then(response => response.json())
            .then(data => {
                const analyticsDataContainer = document.getElementById('consent-analytics-data');
                analyticsDataContainer.innerHTML = ''; // Clear previous data

                // Display consent rates
                const consentRateElement = document.createElement('p');
                consentRateElement.innerHTML = `<strong>Consent Rate:</strong> ${data.consent_rate * 100}%`;
                analyticsDataContainer.appendChild(consentRateElement);

                const rejectionRateElement = document.createElement('p');
                rejectionRateElement.innerHTML = `<strong>Rejection Rate:</strong> ${data.rejection_rate * 100}%`;
                analyticsDataContainer.appendChild(rejectionRateElement);

                // Display popular choices
                const popularChoicesElement = document.createElement('p');
                popularChoicesElement.innerHTML = `<strong>Popular Choices:</strong>`;
                analyticsDataContainer.appendChild(popularChoicesElement);

                const choicesList = document.createElement('ul');
                for (const service in data.popular_choices) {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `${service}: ${data.popular_choices[service] * 100}%`;
                    choicesList.appendChild(listItem);
                }
                analyticsDataContainer.appendChild(choicesList);

                // Display consent over time (basic example)
                const consentOverTimeElement = document.createElement('p');
                consentOverTimeElement.innerHTML = `<strong>Consent Over Time:</strong>`;
                analyticsDataContainer.appendChild(consentOverTimeElement);

                const timeList = document.createElement('ul');
                for (const item of data.consent_over_time) {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `${item.date}: ${item.consent_rate * 100}%`;
                    timeList.appendChild(listItem);
                }
                analyticsDataContainer.appendChild(timeList);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('consent-analytics-data').innerHTML = '<p>Error loading analytics data.</p>';
            });
    }

    // Fetch analytics on page load and potentially set up periodic refresh
    if (consentAnalyticsSection) {
        fetchConsentAnalytics();
        // Optional: Refresh analytics data periodically (e.g., every 5 minutes)
        // setInterval(fetchConsentAnalytics, 300000); // 300000 ms = 5 minutes
    }
});