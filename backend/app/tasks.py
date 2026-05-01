from celery import Celery
from .config import settings
from .db import SessionLocal
from .models import ContentTask
from .agents.pipeline import trend_agent, content_agent, rewrite_agent, evaluator_agent

celery_app = Celery("content_worker", broker=settings.redis_url, backend=settings.redis_url)

@celery_app.task(name="run_content_pipeline")
def run_content_pipeline(task_id: int, use_evaluator: bool = True):
    db = SessionLocal()
    try:
        task = db.query(ContentTask).filter(ContentTask.id == task_id).first()
        if not task:
            return
        task.status = "running"
        db.commit()

        trend = trend_agent(task.topic, task.platform)
        generated = content_agent(task.topic, task.platform, trend, task.count)
        rewritten = rewrite_agent(task.platform, generated)
        evaluated = evaluator_agent(rewritten) if use_evaluator else ""

        task.trend_output = trend
        task.generated_output = generated
        task.rewritten_output = rewritten
        task.evaluated_output = evaluated
        task.status = "done"
        db.commit()
    except Exception as e:
        task.status = "failed"
        task.error_message = str(e)
        db.commit()
    finally:
        db.close()
