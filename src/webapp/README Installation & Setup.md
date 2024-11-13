# README for Building and Running the Web App

## Prerequisites
- **Visual Studio Code (VSC)**: Ensure Visual Studio Code is installed. [Download VSC](https://code.visualstudio.com/).
- **Node.js**: Required to run the Next.js application. [Download Node.js](https://nodejs.org/).
- **Next.js Library**: Installed within your Visual Studio Code environment.

## Clone the Repository
Clone the repository to your local machine using the following command:
```bash
git clone https://github.com/AlanDataPortfolio/ey-azure-fn-pipeline.git
```

Navigate to the `webapp` folder in Visual Studio Code.

## Install Required Dependencies
Before running the web app, ensure all necessary libraries and imports are installed:

### Libraries and Imports Used
- **React Hooks**:
  ```javascript
  import { useState, useEffect } from 'react';
  ```
- **Routing**:
  ```javascript
  import { useRouter } from 'next/router';
  ```
- **Markdown Rendering**:
  ```javascript
  import ReactMarkdown from 'react-markdown';
  import remarkBreaks from 'remark-breaks';
  ```
- **HTTP Requests**:
  ```javascript
  const axios = require('axios'); // or
  import axios from 'axios';
  ```

### Installation Command
Open the terminal in Visual Studio Code and navigate to the `webapp` directory, then run:
```bash
npm install
```
This command installs all dependencies as listed in the `package.json` file, ensuring that the imported libraries are correctly set up.

## Run the Development Server
Start the development server by running:
```bash
npm run dev
```
This will start the application, typically at `http://localhost:3000`.

## Accessing the App
Open your browser and go to:
```
http://localhost:3000/login
```
This link takes you directly to the login page of the web app.

## Troubleshooting Tips
- **Ensure Node.js version compatibility**: Confirm that your Node.js version is compatible with the libraries being used.
- **Check for import errors**: If the app fails to compile, make sure all libraries (such as `axios`, `react-markdown`, and `remark-breaks`) are correctly imported and installed.

## Project Acknowledgment

This project was conducted for EY by Team 14 of the Macquarie University PACE Program in Session 2, 2024. All rights belong to Team 14, EY, and Macquarie University.

### Team 14 Members:
- Noorullah Khan | 47197404 | Project Manager, Lead Data & Software Engineer
- Ninuri Mahagoda | 46592156 | Business Analyst & Documentation
- Tashiya Vilathgamuwa | 46992162 | Business Analyst & Documentation
- Quoc Hung Nguyen | 47578130 | Cloud Solutions Architect & Infrastructure Lead
- Aasnayem Chowdhury | 46325824 | Data Engineer & Data Modeller

---

© 2024 Team 14 for Macquarie University S2 2024. All rights reserved.
