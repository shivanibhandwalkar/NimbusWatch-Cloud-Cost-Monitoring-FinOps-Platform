import os

import boto3


USE_MOCK_ALERTS = True# Switch to False after SNS is set up

BUDGET_WARN_PERCENT = 80   # warn once spending reaches 80% of the budget


SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "")# Readin from environment variables so secrets never live in the code
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")


def budget_status(records, budget):
    """Total up all costs and compare them with the budget."""
    total = sum(record["cost"] for record in records)
    percent_used = total / budget * 100 if budget > 0 else 0
    return round(total, 2), round(percent_used, 1)


def build_alert(records, anomalies, budget):
    """Create the alert text. Returns None if everything looks fine."""
    total, percent_used = budget_status(records, budget)
    lines = []

    if percent_used >= BUDGET_WARN_PERCENT:
        lines.append(
            f"Budget warning: you have spent ${total} of ${budget:.0f} "
            f"({percent_used}%)."
        )

    for item in anomalies:
        lines.append(f"Anomaly: {item['message']}")

    if not lines:
        return None
    return "\n".join(lines)


def send_alert(subject, message):
    """Send the alert through SNS, or just print it in mock mode."""
    if USE_MOCK_ALERTS:
        print(f"\n[MOCK ALERT] {subject}\n{message}\n")
        return "mock"

    sns = boto3.client("sns", region_name=AWS_REGION)
    response = sns.publish(TopicArn=SNS_TOPIC_ARN, Subject=subject, Message=message)
    return response["MessageId"]


def check_and_alert(records, anomalies, budget):
    """Main function: build the alert and send it only if there is something to say."""
    message = build_alert(records, anomalies, budget)
    if message is None:
        return {"alert_sent": False, "reason": "All costs look normal"}

    send_alert("NimbusWatch cost alert", message)
    return {"alert_sent": True, "message": message}