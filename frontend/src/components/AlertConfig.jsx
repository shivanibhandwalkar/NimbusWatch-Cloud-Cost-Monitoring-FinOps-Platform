import { useState } from "react";

function AlertConfig({ budget, apiUrl, onSaved }) {
  const [value, setValue] = useState(budget);
  const [message, setMessage] = useState("");

  async function save() {
    const amount = Number(value);
    if (!amount || amount <= 0) {
      setMessage("Enter a number greater than 0");
      return;
    }

    try {
      const response = await fetch(`${apiUrl}/budget`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ monthly_budget: amount }),
      });
      if (!response.ok) {
        throw new Error("Save failed");
      }
      setMessage("Saved");
      onSaved(); // tell the parent page to reload its data
    } catch (err) {
      setMessage("Could not save the budget");
    }
  }

  return (
    <div className="card">
      <h2>Alert settings</h2>
      <label>
        Monthly budget ($){" "}
        <input
          type="number"
          value={value}
          onChange={(event) => setValue(event.target.value)}
        />
      </label>{" "}
      <button onClick={save}>Save</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default AlertConfig;