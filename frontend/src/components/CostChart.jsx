import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

// Add up costs grouped by a field ("service" or "date")
function totalsBy(records, field) {
  const totals = {};
  for (const record of records) {
    totals[record[field]] = (totals[record[field]] || 0) + record.cost;
  }
  return Object.entries(totals).map(([name, cost]) => ({
    name,
    cost: Number(cost.toFixed(2)),
  }));
}

function CostChart({ records }) {
  const perService = totalsBy(records, "service");
  const perDay = totalsBy(records, "date").sort((a, b) =>
    a.name.localeCompare(b.name)
  );

  return (
    <>
      <div className="card">
        <h2>Cost per service (last 30 days)</h2>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={perService}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="cost" fill="#4c6ef5" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h2>Daily spend trend</h2>
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={perDay}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="cost" stroke="#e8590c" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </>
  );
}

export default CostChart;