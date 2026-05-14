# Face Recognition

an api endpoint for adding and indentifying face using Robyn and AuraFace

# Setup

## Development

### Create virtual env

```cmd
python -m venv .venv
```

### Setup Docker

```cmd
docker compose up --build
```

# Deployment

you can directly use the dockerfile to host this anywhere no env setup needed

## Scaling

you can edit the dockerfile to adjust the number of workers and processes, more info on [robyn deployment](https://robyn.tech/documentation/en/example_app/deployment)

## DB Migration

Generate the Initial Migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

To update your database schema to the latest version, run the upgrade command.

```bash
alembic upgrade head
```

Common Commands Reference

| Action                 | Command                     |
| ---------------------- | --------------------------- |
| Check Current Version  | `alembic current`           |
| View Migration History | `alembic history --verbose` |
| Revert One Migration   | `alembic downgrade -1`      |
| Upgrade to Latest      | `alembic upgrade head`      |
