# README for `src` Folder

This repository contains the core components of our project, each organized into specific subfolders within the `src` directory. Below is an overview of each folder and its purpose.

## Folder Structure

### 1. `local_pipeline`
- **Description**: This folder contains the primary scripts for data cleaning, enrichment, synthesis, and merging processes. It was the main workspace where the team performed detailed data operations before moving to the cloud.
- **Key Features**:
  - Individual scripts for each step, providing detailed processing and modularity.
  - Comprehensive data manipulation and preparation for later stages of cloud integration.
- **Contents**: Scripts for various data processing stages, such as `clean_data.py`, `enrich_data.py`, `synthesize_data.py`, and `merge_data.py`.

### 2. `terraform`
- **Description**: This folder holds the infrastructure as code (IaC) files for deploying and automating our data processing workflows on Azure. The scripts in this folder are designed to combine and streamline the processes found in the `local_pipeline` into larger, cloud-executable functions.
- **Key Features**:
  - Automates deployment of the data processing pipeline to Azure services.
  - Ensures scalability and consistency across cloud environments.
- **Contents**: Files for defining Azure resources and infrastructure, such as `main.tf`, `variables.tf`, and deployment scripts.

### 3. `webapp`
- **Description**: This folder contains the codebase for the user interface (UI) of the project. It includes all the components required for the web application, enabling interaction and visualization for end users.
- **Key Features**:
  - Front-end development using Next.js and Node.js.
  - UI components to facilitate user interactions, such as login, dashboard, and claim processing features.
- **Contents**: `pages`, `components`, and configuration files for building and running the web application.

### 4. `func_app`
- **Description**: This folder includes the necessary files for running specific functions related to the project. It contains scripts and configuration files that assist with task execution.
- **Contents**:
  - `.funcignore`: Specifies files to ignore during deployments.
  - `.gitignore`: Lists files and directories ignored by Git.
  - `function_app`: A Python file with core functions for task execution.
  - `host`: JSON configuration file for function hosting.
  - `requirements`: Text document specifying Python package dependencies.

## Summary
Each folder within the `src` directory plays a unique and integral role in the overall project workflow, from data preparation in `local_pipeline`, to cloud deployment with `terraform`, to building user interfaces in `webapp`, and running specific tasks with `func_app`.

---
