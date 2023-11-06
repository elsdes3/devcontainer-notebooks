# Multi-Container Notebook Workflow with Dev Containers

![CI](https://github.com/elsdes3/devcontainer-notebooks/workflows/CI/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/mit)
![OpenSource](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![prs-welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)

## About

Run a multi-step Jupyter notebook-based workflow, in which each step runs inside its own Dev Container. This was adapted from the [VS Code documentation for configuring multiple Dev Containers](https://code.visualstudio.com/remote/advancedcontainers/configure-separate-containers).

The following workflow steps are shown here within the `notebooks` folder

1. `get-data`
   - runs ETL pipeline to retrieve data and store in private cloud storage (AWS S3 bucket)
2. `eda`
   - performs exploratory data analysis using data stored in private cloud storage (AWS S3 bucket)

## Pre-Requisites

1. Install Docker, including `docker-compose` ([1](https://docs.docker.com/engine/install/ubuntu/), [2](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04) [3](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)).
2. [Download](https://code.visualstudio.com/download) and [install VS Code](https://code.visualstudio.com/docs/setup/setup-overview#_cross-platform), with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
3. Create an AWS account and create the following AWS resources

   - [create an (Administrator) IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console) with [the `AdministratorAccess` policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AdministratorAccess.html) or with another policy that permits the user to access the private S3 bucket
     - create access keys for this IAM user ([1](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey), [2](https://docs.aws.amazon.com/sdkref/latest/guide/access-iam-users.html))
     - copy the *Access key ID* and *Secret Access Key* into `~/.aws/credentials` per [these instructions](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#shared-credentials-file)
   - create a private S3 bucket ([1](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html), [2](https://www.simplified.guide/aws/s3/create-private-bucket))

## Usage

1. Clone this repo into the working folder (eg. clone into `~/Downloads`).
2. In VS Code, select File > Open Folder... and select the `notebooks` folder inside project root inside the working directory (eg. open `~/Downloads/devcontainer-notebooks/notebooks`). Two sub-folders (`get-data` and `eda`) should be visible. One sub-folder corresponds to a single step in the workflow.
3. A pop-up appears at the bottom right of the screen. Ignore this for now.
4. Change the contents of `.devcontainer/environment.yml` inside the appropriate sub-folder as required.
5. Click the *Reopen in Container* button (as shown in the image [here](https://code.visualstudio.com/docs/devcontainers/create-dev-container#_add-configuration-files-to-a-repository)) in order to re-open one of the sub-folders inside a Dev Container. If the button has disappeared, press <kbd>F1</kbd> or <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> and select *Dev Containers: Open in Container...*
6. Select the required sub-folder (`get-data` or `eda`).

### VS Code Actions

Perform the following in VS Code

1. Click *Starting Dev Contiainer (show log)* to view the container building logs.
2. In the TERMINAL, click *Maximize Panel Size*.
3. The TERMINAL shows the progress of the container build process.
4. After the container has been built

   - the TERMINAL will stop updating
   - The lower left remote indicator will display *Dev Container: Containerized Jupyter Notebook*
   - the contents of the workspace will be visible in the File Explorer
5. In the terminal, click *Restore Panel Size*.
6. Open the `notebooks` folder and launch a notebook.

### Cleanup

First shut down the container

1. Close any open notebooks.
2. Click the lower left remote indicator and select *Close Remote Connection*.

Next, from the root directory of the project, remove any containers and images using

1. cleanup container resources for the `get-data` step of the workflow
   ```bash
   make reset-get-data docker-system-prune
   ```
2. cleanup container resources for the `eda` step of the workflow
   ```bash
   make reset-eda docker-system-prune
   ```

## Notes

1. Code formatting settings specified in `.devcontainer/devcontainers.json` are being ignored. Python modules in `src` are not correctly formatted based on these settings.
2. This container will support running a Jupyter notebook, and will not start the [Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/) interface.
3. It was not possible to mount the local `~/.aws` folder to the same path inside the container [using the `docker-compose.yml` file](https://code.visualstudio.com/remote/advancedcontainers/add-local-file-mount), so [this mounting was done using the `devcontainer.json file`](https://renatogolia.com/2020/10/12/working-with-aws-in-devcontainers/).
