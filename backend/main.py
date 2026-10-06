from datetime import datetime  # database and business logic modules
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from alerter import budget_status, check_and_alert
from anomaly_detector import find_anomalies
from cost_fetcher import get_daily_costs
from database import get_budget, init_db, load_costs, save_costs, set_budget

app = FastAPI(title="Cloud Cost Monitor")


app.add_middleware(# Enabling CORS so your frontend can communicate with the backend smoothly
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()    # Initialize database tables on startup

last_synced_time = "Not synced yet"# Global state for last synced timestamp


def run_automated_sync_job():
  """Background job that syncs costs, checks anomalies, and updates the timestamp."""
  global last_synced_time
  print(f"[{datetime.now()}] Running background cost sync & anomaly check...")

  try:
    
    data = get_daily_costs(30)# Automatically fetch and save mock/real cloud costs
    save_costs(data)
  except Exception as e:
    print(f"Error during automated sync: {e}")

  last_synced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


scheduler = BackgroundScheduler()
# Initialize and start the APScheduler
scheduler.add_job(
    run_automated_sync_job, "interval", hours=3
)  # Runs every 3 hours
scheduler.start()


@app.on_event("startup")
def startup_event():
  """Run the sync job immediately when the server boots up."""
  run_automated_sync_job()


@app.on_event("shutdown")
def shutdown_scheduler():
  """Gracefully shut down the scheduler when FastAPI stops."""
  scheduler.shutdown()


class BudgetUpdate(BaseModel):
  monthly_budget: float = Field(gt=0)


@app.get("/")
def home():
  return {"message": "Cloud Cost Monitor is running"}


@app.get("/api/last-sync")
def get_last_sync():
  return {"last_synced": last_synced_time}


@app.get("/costs")
def costs(days: int = 7):
  data = get_daily_costs(days)
  return {"days": days, "count": len(data), "data": data}


@app.post("/sync")
def sync(days: int = 30):
  data = get_daily_costs(days)
  saved = save_costs(data)
  return {"saved": saved}


@app.get("/history")
def history(days: int = 30):
  data = load_costs(days)
  return {"days": days, "count": len(data), "data": data}


@app.get("/anomalies")
def anomalies():
  records = load_costs(14)
  found = find_anomalies(records)
  return {"count": len(found), "anomalies": found}


@app.get("/budget")
def read_budget():
  budget = get_budget()
  total, percent = budget_status(load_costs(30), budget)
  return {"monthly_budget": budget, "total_spent": total, "percent_used": percent}


@app.post("/budget")
def update_budget(body: BudgetUpdate):
  set_budget(body.monthly_budget)
  return {"monthly_budget": body.monthly_budget}


@app.get("/check-alerts")
def check_alerts():
  records = load_costs(30)
  found = find_anomalies(records)
  return check_and_alert(records, found, get_budget())