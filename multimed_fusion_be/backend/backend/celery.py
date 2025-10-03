from celery import Celery

# Create Celery instance
app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',   # Redis as broker
    backend='redis://localhost:6379/0'   # Redis as backend
)
