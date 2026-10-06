import os
import random
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError

# Check if AWS credentials exist in the environment
AWS_ENABLED = bool(
    os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY")
)


def get_daily_costs(days: int = 30):
  """Fetches real AWS Cost Explorer data if credentials exist,

  otherwise falls back to realistic multi-cloud simulation data.
  """
  if AWS_ENABLED:
    try:
      
      ce_client = boto3.client(# Standard production boto3 client for AWS Cost Explorer
          "ce",
          region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
          aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
          aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
      )

      end_date = datetime.utcnow().date()
      start_date = end_date - timedelta(days=days)

      response = ce_client.get_cost_and_usage(
          TimePeriod={
              "Start": start_date.strftime("%Y-%m-%d"),
              "End": end_date.strftime("%Y-%m-%d"),
          },
          Granularity="DAILY",
          Metrics=["UnblendedCost"],
      )

      
      formatted_data = []# Parse real AWS response structure into your dashboard format
      for result in response.get("ResultsByTime", []):
        date_str = result["TimePeriod"]["Start"]
        cost = float(
            result["Total"]["UnblendedCost"].get("Amount", 0.0)
        )
        formatted_data.append({
            "date": date_str,
            "provider": "AWS",
            "service": "EC2/S3 (Live)",
            "cost": round(cost, 2),
        })
      return formatted_data

    except (NoCredentialsError, BotoCoreError) as e:
      print(f"AWS credentials invalid or missing. Falling back to simulation: {e}")

  # ***********************FALLBACK SIMULATION (Runs locally without IAM keys) ********************
  providers = ["AWS", "Azure", "GCP"]
  services = {
      "AWS": ["EC2", "S3", "RDS"],
      "Azure": ["Virtual Machines", "Blob Storage", "CosmosDB"],
      "GCP": ["Compute Engine", "Cloud Storage", "BigQuery"],
  }

  data = []
  base_date = datetime.utcnow().date() - timedelta(days=days)

  for i in range(days):
    current_date = base_date + timedelta(days=i)
    date_str = current_date.strftime("%Y-%m-%d")

    for provider in providers:
      service = random.choice(services[provider])
      # Generate realistic random daily spend
      cost = round(random.uniform(5.0, 45.0), 2)
      data.append(
          {"date": date_str, "provider": provider, "service": service, "cost": cost}
      )

  return data