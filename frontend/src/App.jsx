import { useEffect, useState } from "react";
import "./App.css";
import AlertConfig from "./components/AlertConfig";
import AnomalyCard from "./components/AnomalyCard";
import BudgetGauge from "./components/BudgetGauge";
import CostChart from "./components/CostChart";
const API_URL = "http://localhost:8000";

function App() {
  const [records, setRecords] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [budgetInfo, setBudgetInfo] = useState(null);
  const [lastSynced, setLastSynced] = useState("Loading...");
  const [error, setError] = useState("");

  async function loadData() {
    try {
      const historyRes = await fetch(`${API_URL}/history?days=30`);
      const historyJson = await historyRes.json();
      
      const anomalyRes = await fetch(`${API_URL}/anomalies`);
      const anomalyJson = await anomalyRes.json();
      
      const budgetRes = await fetch(`${API_URL}/budget`);
      const budgetJson = await budgetRes.json();

      const syncRes = await fetch(`${API_URL}/api/last-sync`);
      const syncJson = await syncRes.json();

      setRecords(historyJson.data);
      setAnomalies(anomalyJson.anomalies);
      setBudgetInfo(budgetJson);
      setLastSynced(syncJson.last_synced);
      setError("");
    } catch (err) {
      setError("Could not reach the backend. Is uvicorn running?");
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="page animate-fade-in">
      <div className="header-flex">
        <div className="brand-header">
          <img src="/logo.png" alt="NimbusWatch Logo" className="logo" />
          <h1>NimbusWatch Cost Monitor</h1>
        </div>
        <div className="live-indicator">
          <span className="pulse-dot"></span> Live Sync Active
        </div>
      </div>
      
      {/* System Status Card with Last Automatic Sync */}
      <div className="card hover-card">
        <h2>System Status</h2>
        <p>Last Automatic Sync: <strong>{lastSynced}</strong></p>
      </div>

      {error && <p className="error-text">{error}</p>}
      
      <div className="card-wrapper">
        {budgetInfo && <BudgetGauge info={budgetInfo} />}
      </div>

      {budgetInfo && (
        <div className="card hover-card">
          <AlertConfig
            budget={budgetInfo.monthly_budget}
            apiUrl={API_URL}
            onSaved={loadData}
          />
        </div>
      )}
      
      <div className="hover-card">
        <AnomalyCard anomalies={anomalies} />
      </div>
      
      <div className="card hover-card">
        <CostChart records={records} />
      </div>
    </div>
  );
}

export default App;