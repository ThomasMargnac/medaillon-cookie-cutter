# {{ cookiecutter.project_slug }}
Author: {{ cookiecutter.author }}

## Table of contents

1. [📁 Project structure](#-project-structure)
2. [🚀 Usage](#-usage)
3. [🙏 Credits](#-credits)

## 📁 Project structure

```
├─ .gitignore                <- Specifies files and directories ignored by Git.
├─ .pre-commit-config.yaml   <- Configuration for pre-commit hooks to enforce code style.
├─ .venv/                    <- Local Python virtual environment (not versioned).
├─ config/                   <- Contains configuration files used by the project.
│   └─ minio-mc/                        <- Configuration directory for the MinIO client (mc) used to manage MinIO buckets.
│       └─ init.sh                                 <- Shell script executed to initialize MinIO buckets at container startup.
├─ docs/                     <- Documentation related to the project.
├─ src/                      <- Main source code directory containing the data pipeline logic.
│   ├─ bronze/                          <- Bronze layer: raw data ingestion.
│   ├─ silver/                          <- Silver layer: standardized and cleaned data transformations.
│   ├─ gold/                            <- Gold layer: curated and enriched data ready for analytics or exposure.
│   └─ utils/                           <- Utility modules and helper functions reused across layers.
├─ tests/                    <- All test suites for the project.
│   ├─ integration/                     <- Integration tests verifying that components work together.
│   └─ unit/                            <- Unit tests for individual functions or classes.
├─ docker-compose.yaml       <- Docker Compose file for orchestrating local services.
├─ poetry.lock               <- Lock file ensuring dependency version consistency.
├─ pyproject.toml            <- Project metadata and dependencies configuration.
├─ README.md                 <- Main documentation file describing setup, usage, and project context.
└─ template.env              <- Example environment file (.env) to define environment variables and secrets.
```

## 🚀 Usage
### Virtual environment

Activate the environment to develop:
```bash
source .venv/bin/activate   # On Linux/Mac
# or
.venv\Scripts\activate      # On Windows
```

### Environment variables

Before running the project, configure your environment variables. An example file is provided as `template.env`.
1. Copy the template file:
```bash
cp template.env .env
```
2. Edit `.env` with your own configuration values.

### Run the project

You can run the project with Docker Compose:
```bash
docker compose --env-file <path_to_env_file> up
```

## 🙏 Credits

This project was generated using the [Medaillon Cookie Cutter](https://github.com/ThomasMargnac/medaillon-cookie-cutter).