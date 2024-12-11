# Klaro! GTM Consent Manager

[![Google Cloud Status](https://storage.googleapis.com/artlab-public.appspot.com/badges/badges-status.svg)](https://status.cloud.google.com/)
[![Deploy to Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run/?git_repo=https://github.com/shyamAdw/gKlaro.git)

## Overview

The Klaro! GTM Consent Manager is a web application designed to simplify the implementation of a user-friendly and compliant consent management solution using the [Klaro!](https://kiprotect.com/docs/klaro/) consent management library and [Google Tag Manager (GTM)](https://tagmanager.google.com/). This tool provides a graphical user interface (GUI) to configure Klaro! settings and automatically generates GTM templates (tags, triggers, and variables) to manage consent within your website or application.

## Features

*   **Visual Klaro! Configuration:** Easily set up Klaro! options through a user-friendly web interface, including appearance, language, consent options, and more.
*   **GTM Template Generation:** Automatically generates GTM templates (tags, triggers, and variables) based on your Klaro! configuration, ready to be imported into your GTM container.
*   **Consent Simulation and Debugging:** Simulate user consent choices and debug your GTM setup to ensure proper functionality.
*   **Privacy Policy Guidance:** Provides templates and resources to help you create a clear and comprehensive privacy policy.
*   **Consent Analytics:** Offers insights into user consent behavior, including consent rates, popular choices, and trends over time (basic implementation provided, can be expanded).
*   **Built with Flask:** Developed using the Flask web framework for Python, making it lightweight, flexible, and easy to extend.
*   **Deployable on Google App Engine:** Designed for easy deployment on Google App Engine, providing scalability and reliability.

## Prerequisites

*   A Google Cloud Platform (GCP) account.
*   A Google Tag Manager (GTM) account and container.
*   Python 3.11 or higher installed locally (for development and testing).
*   Familiarity with GTM concepts (tags, triggers, variables, data layer).

## Installation and Deployment

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/shyamAdw/gKlaro.git
    cd gklaro
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Google App Engine:**
    *   Update the `app.yaml` file:
        *   Replace `your_default_secret_key` with a strong, random secret key for your application.

5.  **Deploy to Google App Engine:**

    ```bash
    gcloud app deploy
    ```

    Follow the prompts to select your GCP project and region. Once the deployment is complete, the application will be accessible via a URL provided by App Engine.

## Usage

1.  **Access the Application:** Open the URL of your deployed App Engine application in your web browser.

2.  **Configure Klaro!:**
    *   Use the GUI to set up your desired Klaro! configuration:
        *   **Language:** Select the language for the consent interface.
        *   **Storage Method:** Choose between using cookies or localStorage.
        *   **Consent Options:** Define the different consent options you want to offer (e.g., "Analytics," "Marketing"). Provide a name, title, description, purposes, default state (true/false), and whether it's required or optional.
        *   **Appearance:** Customize the look and feel of the consent modal (if applicable).
    *   Click the "Generate GTM Template" button.

3.  **Import into GTM:**
    *   The application will generate GTM templates and triggers. Copy the provided code.
    *   In your GTM container, create a new custom template.
    *   Paste the copied code into the template editor.
    *   Save the template.
    *   Import triggers.

4.  **Configure Tags:**
    *   Create or modify your existing tags (e.g., Google Analytics, Facebook Pixel) in GTM.
    *   Set the firing triggers for these tags to be based on the consent choices obtained from Klaro!
        *   Use the generated `klaroScriptLoaded` trigger to ensure tags only fire after Klaro! has been initialized.

5.  **Debug and Simulate:**
    *   Use the "GTM Debugging" section of the application to simulate user consent choices.
    *   Observe the behavior of your tags in the GTM preview mode to ensure they are firing correctly based on consent.

6.  **Privacy Policy:**
    *   Use the "Privacy Policy" section to upload a custom privacy policy or download a sample template to help you get started.

7.  **Consent Analytics:**
    *   View basic consent analytics in the "Consent Analytics" section. (Note: This is a basic implementation, and you may want to enhance it by integrating with a database to store consent events.)

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b bugfix/your-bug-fix`.
3.  Make your changes and commit them with clear messages: `git commit -m "Add: Your feature description"` or `git commit -m "Fix: Your bug fix description"`.
4.  Push your branch to your forked repository: `git push origin your-branch-name`.
5.  Open a pull request from your forked repository to the main repository.

## Security

*   **Secret Key:** Ensure that you replace the placeholder secret key in `app.yaml` with a strong, randomly generated key in your production environment.
*   **Input Validation:** The application includes basic input validation, but you should thoroughly review and enhance it to prevent security vulnerabilities.
*   **Data Protection:** If you are storing user data, make sure to follow secure coding practices and comply with relevant data privacy regulations (e.g., GDPR).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (You'll need to create a LICENSE file with the MIT License text).

## Acknowledgements

*   [Klaro!](https://kiprotect.com/docs/klaro/) - The open-source consent management library.
*   [Google Tag Manager](https://tagmanager.google.com/) - The tag management system.
*   [Flask](https://flask.palletsprojects.com/) - The Python web framework.

---

**Disclaimer:** This tool is provided as a helpful resource and starting point. It is your responsibility to ensure that your consent implementation complies with all applicable laws and regulations. Consult with legal counsel if you have any questions about legal compliance.
