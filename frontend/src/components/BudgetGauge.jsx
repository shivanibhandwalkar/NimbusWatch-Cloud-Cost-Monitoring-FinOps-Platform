function BudgetGauge({ info }) {
  const percent = info.percent_used;
  const barWidth = Math.min(percent, 100); // the bar never goes past 100%

  // Green is fine, orange is a warning, red is over budget
  let color = "#2b8a3e";
  if (percent >= 100) {
    color = "#e03131";
  } else if (percent >= 80) {
    color = "#f08c00";
  }

  return (
    <div className="card">
      <h2>Budget vs actual</h2>
      <div className="gauge-track">
        <div
          className="gauge-fill"
          style={{ width: `${barWidth}%`, background: color }}
        />
      </div>
      <p>
        ${info.total_spent.toFixed(2)} spent of ${info.monthly_budget.toFixed(2)}{" "}
        <strong style={{ color }}>({percent}%)</strong>
      </p>
    </div>
  );
}

export default BudgetGauge;
