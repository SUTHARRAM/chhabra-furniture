import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";

export default function BillsList() {
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const res = await api.get("/bills?limit=50&page=1");
        // fallback in case res.data.data is null/undefined
        setRows(res?.data?.data || []);
      } catch (err: any) {
        console.error("Failed to fetch bills", err);
        setError("Could not load bills. Please try again later.");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return <p>Loading bills...</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  return (
    <div>
      <div className="actions">
        <Link to="/bills/new">+ New Bill</Link>
      </div>

      {rows.length === 0 ? (
        <p>No bills found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Bill No</th>
              <th>Customer</th>
              <th>Total</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id}>
                <td>{r.bill_date ? new Date(r.bill_date).toLocaleString() : "-"}</td>
                <td>{r.bill_no || "-"}</td>
                <td>{r.to?.name || "-"}</td>
                <td>₹{typeof r.total === "number" ? r.total.toFixed(2) : "0.00"}</td>
                <td>
                  <Link to={`/bills/${r.id}`}>Open</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
