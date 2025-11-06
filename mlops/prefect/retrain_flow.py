from prefect import flow, task
import mlflow

@task
def download_data():
    print('Downloading prepared dataset...')
    return '/tmp/aku_dataset'

@task
def train_model(data_path: str):
    print(f'Training model on {data_path} (placeholder)')
    # insert training code here (HF Trainer, PyTorch Lightning, etc.)
    metrics = {'val_loss': 0.1, 'accuracy': 0.95}
    return metrics

@task
def register_model(metrics):
    print('Registering model - placeholder')
    # Use MLflow to log and register model
    mlflow.log_metrics(metrics)
    return 'models:/aku_transformer/1'

@flow
def retrain_flow():
    data = download_data()
    metrics = train_model(data)
    model_ref = register_model(metrics)
    return model_ref

if __name__ == '__main__':
    retrain_flow()
