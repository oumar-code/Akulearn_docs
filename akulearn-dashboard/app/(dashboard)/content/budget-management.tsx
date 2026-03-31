"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../../lib/supabaseClient";

export default function BudgetManagementPanel() {
  type BudgetItem = { id: string; description: string; amount?: number; category?: string };
  const [items, setItems] = useState<BudgetItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchBudget = async () => {
      setLoading(true);
      setError("");
      try {
        const { data, error } = await supabase.from("budget_items").select("*");
        if (error) throw error;
        setItems(data || []);
      } catch {
        setError("Unable to fetch budget data.");
      }
      setLoading(false);
    };
    fetchBudget();
  }, []);

  return (
    <div style={{ padding: "1rem", border: "1px solid #e0e0e0", borderRadius: 8, margin: "1rem 0" }}>
      <h3>Budget Management</h3>
      {loading && <div>Loading budget...</div>}
      {error && <div style={{ color: "#d32f2f" }}>{error}</div>}
      {!loading && !error && (
        <ul>
          {items.map(item => (
            <li key={item.id}>{item.description} — ₦{item.amount?.toLocaleString() ?? 0} ({item.category || "N/A"})</li>
          ))}
          {items.length === 0 && <li>No budget items found.</li>}
        </ul>
      )}
    </div>
  );
}
