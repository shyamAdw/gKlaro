import json
from jsmin import jsmin

def validate_klaro_config(config):
    """
    Validates the provided Klaro configuration.

    Args:
        config (dict): The Klaro configuration dictionary.

    Returns:
        bool: True if the configuration is valid, False otherwise.
    """
    # Implement your validation logic here
    # Example:
    if not config.get('language'):
        return False
    if not config.get('services'):
        return False
    # Add more checks as needed...
    return True


def generate_gtm_template_code(klaro_config):
    """
    Generates the GTM template code based on the Klaro configuration.

    Args:
        klaro_config (dict): The Klaro configuration dictionary.

    Returns:
        str: The GTM template code (as a JSON string - for dataLayer).
    """
    # Minify the Klaro config to reduce the size
    minified_config = jsmin(json.dumps(klaro_config))

    # Construct the GTM template using the minified Klaro config
    gtm_template = {
        "template": {
            "type": "tag",
            "name": "Klaro Consent Manager",
            "metadata": {
                "displayName": "Klaro Consent Manager",
                "category": "Consents"
            },
            "fields": [
                {
                    "name": "klaroConfig",
                    "displayName": "Klaro Configuration",
                    "type": "textarea",
                    "defaultValue": minified_config,
                    "help": "Paste your minified Klaro configuration here."
                }
            ],
            "code": """
                // Load minified Klaro config from the GTM template field
                var klaroConfig = JSON.parse({{klaroConfig}});

                // Initialize Klaro with the config
                var klaro = window.klaro = window.klaro || {};
                klaro.config = klaroConfig;

                // Function to update consent status in dataLayer
                function updateConsentStatus(serviceName, consentGiven) {
                    var consentStatus = {};
                    consentStatus['klaro_' + serviceName] = consentGiven;
                    dataLayer.push({'event': 'klaroConsentUpdate', 'consentStatus': consentStatus});
                }

                // Check for existing consent or initialize
                for (var i = 0; i < klaroConfig.services.length; i++) {
                    var service = klaroConfig.services[i];
                    if (typeof klaro.getConsent(service.name) === 'undefined') {
                        // Initialize consent (default or as per your logic)
                        klaro.setup(klaroConfig);
                    }
                    // Push initial consent status to dataLayer
                    updateConsentStatus(service.name, klaro.getConsent(service.name));
                }

                // Attach listener for consent changes
                klaro.callback = function(consent, service) {
                    updateConsentStatus(service.name, consent);
                };

                // Load and run Klaro
                var script = document.createElement('script');
                script.type = 'text/javascript';
                script.src = 'https://cdn.kiprotect.com/klaro/latest/klaro.js';
                script.async = true;
                script.onload = function() {
                    // Ensure Klaro is fully initialized before using it
                    if (window.klaro && typeof window.klaro.show === 'function') {
                        window.klaro.show();
                    }
                };
                document.head.appendChild(script);
                
                // Data layer push for successful script execution
                dataLayer.push({'event': 'klaroScriptLoaded'});
            """
        }
    }

    return json.dumps(gtm_template, indent=2)

def generate_gtm_trigger_code(klaro_config):
    """
    Generates the GTM trigger code based on the Klaro configuration.

    Args:
        klaro_config (dict): The Klaro configuration dictionary.

    Returns:
        str: The GTM trigger code (as a JSON string).
    """
    gtm_trigger = {
        "trigger": {
            "type": "customEvent",
            "name": "Klaro Consent Update",
            "metadata": {
                "displayName": "Klaro Consent Update Trigger"
            },
            "filter": [
                {
                    "type": "equals",
                    "parameter": [
                        {
                            "type": "runtimeVariable",
                            "key": "event"
                        },
                        {
                            "type": "template",
                            "value": "klaroConsentUpdate"
                        }
                    ]
                }
            ],
            "uniqueTriggerId": "klaro_consent_update",
            "triggerId": "1"
        }
    }

    return json.dumps(gtm_trigger, indent=2)

def generate_gtm_variable_code(klaro_config):
    """
    Generates the GTM variable code to access consent status.

    Args:
        klaro_config (dict): The Klaro configuration dictionary.

    Returns:
        str: The GTM variable code (as a JSON string).
    """
    gtm_variable = {
        "variable": {
            "type": "jsm",
            "name": "Klaro Consent Status",
            "metadata": {
                "displayName": "Klaro Consent Status Variable"
            },
            "code": """
                function() {
                    var consentStatus = {{k.consentStatus}};
                    return consentStatus;
                }
            """,
            "variableId": "klaro_consent_status"
        }
    }

    return json.dumps(gtm_variable, indent=2)