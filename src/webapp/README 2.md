# README: Using the Insurance Claims Processing Web App

## Overview
This guide provides a step-by-step walkthrough for navigating and using the insurance claims processing web app developed for NRMA. The application is designed to enhance claim agent workflows by integrating real-time AI-powered fraud detection, user-friendly navigation, and comprehensive claims processing functionalities.

## Step-by-Step Instructions

### 1. Logging In
- **Navigate to the Login Page**: Open your browser and go to `localhost:3000/login` to access the login page.
- **Enter Credentials**: Enter your assigned username and password and click the **Login** button.
- **Security Note**: The login feature ensures that only authorized claim agents can access sensitive claim data, maintaining data security and compliance.

### 2. Navigating the Dashboard
- **Dashboard Overview**: After logging in, the main dashboard will be displayed, showing an overview of claims that are pending processing.
- **Navigation Bar**: The top navigation bar includes:
  - **Home (NRMA Logo)**: Click to return to the main dashboard.
  - **Search Bar**: Use this to search for specific claims or related information.
  - **Profile Icon**: Click to log out or access user settings.

### 3. Processing a Claim
- **Selecting a Claim**:
  - Choose the type of claim to process (e.g., car insurance).
  - Click **Fetch Claim** to load a pending claim for review.
- **Claim Details and Description**: Review the details of the fetched claim displayed on the left side of the page, including key information such as claimant name, incident type, and total claim amount.
- **Fraud Detection**:
  - Click the **Check Fraud** button to initiate AI analysis.
  - View the **Fraud Risk Score** displayed as a percentage, with color-coded feedback:
    - **Green** (<40%): Low fraud risk.
    - **Orange** (40-70%): Moderate fraud risk.
    - **Red** (>70%): High fraud risk.
  - Read the **Fraud Analysis Summary** for concise reasoning behind the AI's fraud assessment.
- **Explain More Feature**: Click **Explain More** to get additional details and reasoning from the AI about the claim's risk assessment.
- **Ask AI Custom Question**:
  - Use the **Ask AI** feature to input any custom question related to the claim for tailored responses.
  - This feature helps claim agents gain more context or clarify specific aspects of a claim.

### 4. Completing the Claim Process
- **Selecting an Outcome**:
  - Choose between **Approve**, **Deny**, or **Escalate** as the outcome for the claim.
  - Add any relevant notes or observations before finalizing.
- **Submitting the Outcome**: Click the **Close Case** button to submit the selected outcome, recording the outcome date automatically.
- **Escalating a Claim**: If the claim requires further review, use the **Escalate to Manager** button to alert senior staff.

### 5. Insights and History Page
- **Accessing the Page**: Navigate to the **Insights/History Page** via the navigation bar.
- **Reviewing Processed Claims**:
  - View a comprehensive list of closed and escalated claims.
  - Check details such as outcomes, notes, and fraud risk scores for past claims.
- **Purpose**: This feature helps claim agents and management review decision patterns, maintain consistency, and learn from historical data.

## Additional Features
- **AI-Driven Interactions**: The integration of AI allows for real-time fraud detection and enhanced claim insights.
- **Ask AI**: Use the **Ask AI** function to pose custom questions for deeper understanding or clarification related to a claim.
- **Consistent UI/UX**: The application’s uniform design across all pages, including the login, dashboard, and history pages, ensures ease of use and a professional experience.

## Final Notes
This app is designed to support claim agents in processing claims efficiently while leveraging AI to minimize fraud risks and optimize decision-making. The features included promote transparency, aid in detailed claim assessments, and maintain a structured workflow.
