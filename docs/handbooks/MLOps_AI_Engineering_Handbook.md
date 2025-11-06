## MLOps & AI Engineering Handbook (Aku Platform)

This handbook outlines the recommended MLOps and AI engineering practices for the Aku Platform. It covers model lifecycle, data pipelines, training, deployment tiers (Edge / Super / IG-Hub), monitoring, security, and operational responsibilities.

1. Objectives
- Deliver repeatable, auditable ML model development and deployment.
- Maintain safe, monitored models in production with automated retraining where needed.

2. Roles
- ML Engineers: model development, training, experiment tracking.
- MLOps Engineers: pipelines, deployments, infra for training/serving.
- Data Engineers: ingestion, cleaning, labeling, feature stores.
- SRE / NOC: monitoring, incident response for model endpoints.

3. Data collection & curation
- Collect and tag curriculum content, OERs, localized text for Aku Learn.
- Collect anonymized network and sensor logs for Aku Data Insights.
- Enforce privacy by design: anonymize PII, keep provenance metadata, retain audit logs.

4. Pipeline primitives
- Use DAG systems (Airflow or Prefect) for deterministic ETL and preprocessing.
- Store intermediate artifacts (tokenized datasets, embeddings) in object storage with checksums.

5. Experimentation & tracking
- Use MLflow (or Vertex Experiments) for tracking hyper-parameters, metrics, and model artifacts.
- Maintain a model registry with versioned artifacts and deployment metadata.

6. Model selection & fine-tuning
- Start from HF pre-trained models (BERT-family, XLM-R, Distil models for low-latency.)
- Fine-tune on curated Aku datasets for task-specific models (summarization, QG, intent detection).

7. Training & compute
- Use Super Hubs (GPUs/TPUs) for heavy training. Use IG-Hub cloud endpoints for global models.
- Keep reproducible training scripts with seed control, deterministic configs, and containerized environments.

8. Model packaging & edge optimization
- Export to efficient formats: ONNX, TFLite, or quantized PyTorch where applicable.
- Provide a small inference runtime (tflite-runtime, onnxruntime, or trimmed PyTorch) for Edge Hubs.

9. Deployment tiers
- Edge Hub: quantized, low-latency models in a small inference container or native runtime.
- Super Hub: containerized endpoints (FastAPI/gunicorn + TorchServe/TF-Serving) in k8s.
- IG-Hub: large managed endpoints (Vertex AI / managed LLMs) for global services.

10. Monitoring & drift
- Instrument inference endpoints: latency, error rate, input distributions.
- Setup data-drift detectors (feature distribution checks) and trigger retrain flows when thresholds exceeded.

11. Security
- Protect model artifacts and keys with Vault. Secure model registries and artifact stores.
- Practice Zero Trust for eSIM and model management integrations.

12. Playbooks
- Incident: degrade to a safe fallback model, throttle traffic, trace recent model versions and data.
- Retrain: run the scheduled/triggered retrain DAG, validate new model against a test-suite, and promote via CI/CD.

Appendix: Quick references and templates are in the `mlops/` folder of the repository.
