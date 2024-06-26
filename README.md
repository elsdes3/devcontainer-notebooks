# Multi-Container Notebook Workflow with Dev Containers

![CI](https://github.com/elsdes3/devcontainer-notebooks/workflows/CI/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/mit)
![OpenSource](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![prs-welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)

## About

Run a multi-step Jupyter notebook-based workflow on [Ubuntu Desktop](https://ubuntu.com/desktop), in which each step runs inside its own [Dev Container](https://containers.dev/).

The following workflow steps are included

1. retrieve raw data
   - runs ETL pipeline to retrieve data and store in private cloud storage (AWS S3 bucket)
   - see `notebooks/01-get-data`
2. explore raw data
   - performs exploratory data analysis using data stored in private cloud storage (AWS S3 bucket)
   - see `notebooks/02-eda`

## Pre-Requisites

1. Install the Ubuntu desktop operating system
2. Ensure Docker (including `docker-compose`) is installed locally. For detailed instructions on installing Docker on Ubuntu, see the following helpful resources
   - [Docker installation instructions on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
   - [Digital Ocean installation walkthrough on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
2. [Download](https://code.visualstudio.com/download) and [install VS Code](https://code.visualstudio.com/docs/setup/setup-overview#_cross-platform). Install the VS Code [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
3. Create an AWS account and provision the following AWS resources

   - create a private S3 bucket
     - [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
     - [Simplified.guide](https://www.simplified.guide/aws/s3/create-private-bucket) walkthrough
   - [create an (Administrator) IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console) with [the `AdministratorAccess` policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AdministratorAccess.html) or with another policy that permits the user to access the private S3 bucket created above
   - [create access keys for the IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)
   - [copy the *Access key ID* and *Secret Access Key* into `~/.aws/credentials`](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#shared-credentials-file)

## Usage

Clone this repo into the working folder (eg. clone into `~/Downloads`) and launch VS Code.

### Build and Run a Container

Use the following approach to execute a single step of the workflow (`01-get-data` or `02-eda`) inside a container. If the container has not been built, it will first be built before running it.

1. Select File > Open Folder... and select the `notebooks` sub-folder (eg. select `~/Downloads/devcontainer-notebooks/notebooks`)
   - two sub-folders (`01-get-data` and `02-eda`) should be visible
   - each sub-folder corresponds to a single step in the above workflow
2. During the first build and run of a container, a pop-up appears at the bottom right of the screen indicating the parent directory is detected to be a `git` repository. It asks if this repository should be opened in the text editor (VS Code)

   > A git repository was found in the parent folders of the workspace or the open file(s). Would you like to open the repository?

   The parent directory is not required for any analysis *inside the container*, so this message can be ignored. Click **Never**.
3. Press <kbd>F1</kbd> or <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> and select *Dev Containers: Open Folder in Container...*.
4. Select a sub-folder (`01-get-data` or `02-eda`) to run one step of the workflow
   - a container will now be built to run this step
5. (optional) A pop-up appears at the bottom right of the screen indicating *Starting Dev Contiainer (show log)*. Click *Starting Dev Contiainer (show log)* to view the container build logs.
6. (optional) The TERMINAL shows the logs of the container build process. To view these logs, select *TERMINAL > Maximize Panel Size*.
7. (optional) After the container has been built

   - the logs in the TERMINAL will stop updating
   - the lower left remote indicator will display one of
     - *Dev Container: Get Data* (for the `get-data` step of the workflow)
     - *Dev Container: Eda* (for the `eda` step)
   - the following contents of the workspace will be visible in the File Explorer
     - `.devcontainer`
     - `notebooks`
     - `src`
8. (optional) In the terminal, click *Restore Panel Size*.
9. Open the `notebooks` folder and launch a notebook
10. Select a Jupyter kernel
    - from the top-right corner, click *Select Kernel*
      - select *Python Environments*
      - select one of
        - *`get-data` (Python 3.xx.xx)*
        - *`eda` (Python 3.xx.xx)*
    - all the Python libraries listed in the above `.devcontainer/environment.yml` file for development of this step of the workflow have been installed in this Python environment. After the kernel is selected, all these libraries can be imported into this notebook and all cells in the notebook can be executed without any errors about missing dependencies.

### Shut Down a Container

1. Shut down the container inside which the notebook for the workflow step is running
   - close any open notebooks
   - close the connection to the container
     - click the lower left remote development indicator
     - select *Close Remote Connection*

### Run a Local Container

To run a container that was previously built locally, follow steps 1 to 9 from above.

### Remove a Container

1. Remove any container resources for the workflow step
   - launch a terminal at the root directory of the project (eg. in `~/Downloads`)
   - clean up containers and images for a single workflow step (`get-data` or `eda`)
     ```bash
      ~/Downloads/devcontainer-notebooks$ make reset-<step-name>
     ```
   - (optional) [Remove unused docker resources](https://docs.docker.com/reference/cli/docker/system/prune/)
     ```bash
     ~/Downloads/devcontainer-notebooks$ make docker-system-prune
     ```

## Notes

1. Code formatting settings specified in `.devcontainer/devcontainers.json` are being ignored. As a result, Python modules in `src` are not correctly formatted.
2. This container will support running a Jupyter notebook in VS Code. It will not start the [Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/) interface in a web browser.
3. It was not possible to mount the local `~/.aws` folder to the same path inside the container [using the `docker-compose.yml` file](https://code.visualstudio.com/remote/advancedcontainers/add-local-file-mount). Instead, [this mounting was done using the `devcontainer.json file`](https://renatogolia.com/2020/10/12/working-with-aws-in-devcontainers/).
4. This is an opinionated setup to work with containers inside multiple containers. A separate `docker-compose.yml` file is used per step of the workflow. An alternate setup to work with multiple Dev Containers (not involving notebooks) is demonstrated [here](https://www.youtube.com/watch?v=bVmczgfeR5Y). It has the benefit of using a single `docker-compose.yml` file that could be adapted to capture all steps of a multi-step notebook-based workflow.

## Links Used

1. [AWS documentation to create an IAM user](https://docs.aws.amazon.com/sdkref/latest/guide/access-iam-users.html)
2. VS Code
   - [Configuring multiple Dev Containers](https://code.visualstudio.com/remote/advancedcontainers/configure-separate-containers)
   - [Dev Containers Playlist](https://www.youtube.com/playlist?list=PLj6YeMhvp2S6GjVyDHTPp8tLOR0xLGLYb)
     - [change a user](https://www.youtube.com/watch?v=PSBeVOw7cKQ&list=PLj6YeMhvp2S6GjVyDHTPp8tLOR0xLGLYb)
     - [work with monorepos](https://www.youtube.com/watch?v=o5coAL7oE0o&list=PLj6YeMhvp2S6GjVyDHTPp8tLOR0xLGLYb)
     - [add (mount) a local folder](https://www.youtube.com/watch?v=L1-dx-ZD0Ao&list=PLj6YeMhvp2S6GjVyDHTPp8tLOR0xLGLYb)
