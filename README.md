# Iris MLOps Project (CI/CD + Monitoring)

A small web app that predicts the Iris flower species. It shows the full DevOps / MLOps flow:
**Code -> Git -> GitHub -> Jenkins (build, test) -> Docker -> Prometheus + Grafana (monitoring)**

## Project files
| File | Purpose |
|------|---------|
| `train.py` | Trains the model on the Iris dataset and saves `model.joblib` |
| `app.py` | Flask web app (`/`, `/predict`, `/health`, `/metrics`) |
| `templates/index.html` | Web page with the prediction form |
| `tests/test_app.py` | Automatic tests (run by pytest in the pipeline) |
| `Dockerfile` | Builds the app image |
| `docker-compose.yml` | Starts App + Prometheus + Grafana together |
| `Jenkinsfile` | Jenkins pipeline (Windows) |
| `.github/workflows/ci.yml` | GitHub Actions pipeline (extra CI on GitHub) |
| `monitoring/` | Prometheus config and Grafana dashboard |

## Run locally (Windows, Command Prompt)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python train.py
python -m pytest -v
python app.py
```
Open http://localhost:5000

## Run with Docker (App + Prometheus + Grafana)
```
docker compose up -d --build
```
| Service | URL |
|---------|-----|
| Web app | http://localhost:5000 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 (user: admin, password: admin) |

Stop everything: `docker compose down`

## Jenkins
1. New Item -> Pipeline.
2. Pipeline -> "Pipeline script from SCM" -> Git -> paste your GitHub repository URL, branch `*/main`.
3. Script Path: `Jenkinsfile` -> Save -> Build Now.

(Jenkins must be installed directly on Windows, with Python, Git and Docker Desktop available.)
