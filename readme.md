# CI/CD Pipeline with Docker, Trivy, and Pytest

This repository sets up a Continuous Integration/Continuous Deployment (CI/CD) pipeline for a Python application. The pipeline includes:

- **Testing with Pytest**
- **Building and Pushing Docker Images**
- **Security Scanning with Trivy**
- **Caching Docker and Trivy artifacts for faster builds**

## Requirements

- **GitHub Actions** for CI/CD
- **Docker** for containerization
- **Trivy** for security scanning
- **Pytest** for unit testing
- **Python** 3.10+ for application runtime

## Workflow Overview

The pipeline is defined in `.github/workflows/ci-cd.yml` and runs the following jobs:

### 1. **Test Job**

This job is triggered on every push or pull request to the `main` branch and does the following:

- Sets up the Python environment
- Installs dependencies from `requirements.txt`
- Caches Python packages for faster builds
- Runs tests using **Pytest** to ensure that your code is correct and works as expected

### 2. **Build and Push Docker Image**

Once the tests pass, this job:

- Builds a Docker image of the application
- Pushes the Docker image to DockerHub
- Caches the Docker image layers to speed up subsequent builds

### 3. **Security Scanning with Trivy**

This job scans the Docker image for vulnerabilities using **Trivy**. It does the following:

- Installs **Trivy** for security scanning
- Downloads the Trivy vulnerability database (cache is used to speed up subsequent runs)
- Scans the Docker image for security vulnerabilities with **Trivy**, checking for critical and high-severity issues

## Setup

To set up this project on your local machine:

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
2. Make sure you have a DockerHub account and store your username and token as GitHub secrets:

DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
3. Ensure your requirements.txt file lists the required dependencies for your project.

Secrets Configuration
You need to configure the following GitHub Secrets in the repository:

DOCKERHUB_USERNAME: Your DockerHub username.
DOCKERHUB_TOKEN: A personal access token from DockerHub with permissions to push images.

Conclusion
This setup ensures a robust CI/CD pipeline with automated testing, secure image builds, and vulnerability scanning, streamlining your development workflow.
