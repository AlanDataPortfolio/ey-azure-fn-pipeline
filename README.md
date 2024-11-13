![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Running the Function App Locally](#running-the-function-app-locally)
  - [Deployment](#deployment)
- [License](#license)
- [Contact](#contact)

## Overview
The `ey-azure-fn-pipeline` project is designed to automate the deployment and management of Azure Functions and related infrastructure. This project leverages GitHub Actions for CI/CD, ensuring that code changes are automatically tested, built, and deployed to Azure. The project is structured to maintain clean and organized code, data, and documentation.

## Project Structure
The project is organized into the following directories:

- `.github/workflows/`: Contains GitHub Actions workflows for CI/CD.

- `assets/`: Contains data and documentation assets.
  - `data/`: Various data files used in the project.
  - `docs/`: Project documentation.
    - `folder_structure.tree`: Tree view of the project structure.
    - `guides/`: Guides and tutorials.
  - `img/`: Image assets.

- `src/`: Source code for the project.
  - `func_app/`: Azure Functions application.
  - `local_pipeline/`: Local data processing pipelines.
  - `terraform/`: Terraform scripts for infrastructure as code.
  - `webapp/`: Web application code.

## Getting Started
### Prerequisites
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- [Python](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/)

### Setup
1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/ey-azure-fn-pipeline.git
   cd ey-azure-fn-pipeline
   ```
2. ***Install Python dependencies:***
    ```sh
    cd src/func_app
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    pip install -r requirements.txt
    ```
3. ***Configure Azure CLI:***
    ```sh
    az login
    az account set --subscription <your-subscription-id>
    ```
4. ***Deploy infrastructure using Terraform:***
    ```sh
    cd src/terraform
    terraform init
    terraform apply
    ```
### Running the Function App Locally
1. ***Navigate to the function app directory:***
    ```sh
    cd src/func_app
    ```
2. ***Start the function app:***
    ```sh
    func start
    ```
## Deployment
The deployment is automated using GitHub Actions. Any changes pushed to the `main` branch will trigger the deployment workflow defined in `.github/workflows/infrastructure_deploy.yaml`.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact
For support or questions, please contact alan.ng.work@gmail.com

