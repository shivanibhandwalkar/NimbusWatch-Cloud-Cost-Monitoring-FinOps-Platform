from collections import defaultdict
from datetime import date, timedelta

# Rules for what counts as an anomaly
PERCENT_THRESHOLD = 30   # flag if the cost rose by 30% or more
MIN_EXTRA_COST = 0.50    # ...and rose by at least $0.50 (ignores tiny changes)


def split_into_weeks(records):
    """Add up costs per service for this week and last week."""
    cutoff = (date.today() - timedelta(days=7)).isoformat()

    this_week = defaultdict(float)
    last_week = defaultdict(float)

    for record in records:
        if record["date"] >= cutoff:
            this_week[record["service"]] += record["cost"]
        else:
            last_week[record["service"]] += record["cost"]

    return this_week, last_week


def find_anomalies(records):
    """Compare the two weeks and return a list of unusual cost increases."""
    this_week, last_week = split_into_weeks(records)
    anomalies = []

    for service, current in this_week.items():
        previous = last_week.get(service, 0)
        if previous == 0:
            continue  # nothing to compare against

        extra = current - previous
        percent = extra / previous * 100

        if percent >= PERCENT_THRESHOLD and extra >= MIN_EXTRA_COST:
            anomalies.append(
                {
                    "service": service,
                    "last_week": round(previous, 2),
                    "this_week": round(current, 2),
                    "extra_cost": round(extra, 2),
                    "percent_increase": round(percent, 1),
                    "message": (
                        f"{service} cost rose {percent:.0f}% "
                        f"(${previous:.2f} to ${current:.2f}, ${extra:.2f} extra) "
                        f"compared to last week."
                    ),
                }
            )

    # Biggest money jump first
    anomalies.sort(key=lambda item: item["extra_cost"], reverse=True)
    return anomalies


if __name__ == "__main__":
    # Quick self-test with hand-made data: EC2 doubles this week, S3 stays flat
    fake = []
    for i in range(14, 0, -1):
        day = (date.today() - timedelta(days=i)).isoformat()
        ec2_cost = 3.0 if i > 7 else 6.0
        fake.append({"date": day, "service": "Amazon EC2", "cost": ec2_cost})
        fake.append({"date": day, "service": "Amazon S3", "cost": 0.5})

    for item in find_anomalies(fake):
        print(item["message"])