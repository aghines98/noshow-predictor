# No-Show Predictor

A small backend service that predicts the probability a patient will miss a
scheduled appointment, using a scikit-learn model trained on historical
appointment data.

## Status

🚧 Under active development. Current pieces:
- `modeltrainer/` — data prep and model training scripts (Python, scikit-learn)

Coming next: an Express API that serves predictions from the trained model,
containerized with Docker and deployed to a live demo.

## Why this exists

Built to practice full-stack backend development (Node/Express) alongside a
practical machine learning component (Python/scikit-learn) — two skills I'm
developing in parallel while job hunting for entry-level software engineering
roles.
