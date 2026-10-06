function AnomalyCard({ anomalies }) {
  return (
    <div className="card">
      <h2>Cost anomalies</h2>
      {anomalies.length === 0 ? (
        <p className="ok-text">No unusual spending this week.</p>
      ) : (
        anomalies.map((item) => (
          <div className="alert-item" key={item.service}>
            {item.message}
          </div>
        ))
      )}
    </div>
  );
}

export default AnomalyCard;