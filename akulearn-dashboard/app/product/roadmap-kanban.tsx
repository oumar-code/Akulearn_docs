export default ProductRoadmapKanban;
"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabaseClient";
import styles from "./roadmap-kanban.module.css";

// Minimal Kanban board for product roadmap
const columns = ["Backlog", "In Progress", "Review", "Done"];

  type Task = { id: string; title: string; description?: string; status: string };
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      setError("");
      try {
        // Replace 'product_roadmap' with your actual table name
        const { data, error } = await supabase.from('product_roadmap').select('*');
        if (error) throw error;
        setTasks(data || []);
      } catch (err) {
        setError("Unable to fetch roadmap tasks. Please check your Supabase table and permissions.");
      }
      setLoading(false);
    };
    fetchTasks();
  }, []);

  return (
    <div className={styles.kanbanPanel}>
      <h3>Product Roadmap (Kanban)</h3>
      {loading && <div>Loading roadmap...</div>}
      {error && <div className={styles.kanbanError}>{error}</div>}
      <div className={styles.kanbanColumns}>
        {columns.map(col => (
          <div key={col} className={styles.kanbanColumn}>
            <h4>{col}</h4>
            {tasks.filter(t => t.status === col).map(t => (
              <div key={t.id} className={styles.kanbanTask}>
                <b>{t.title}</b>
                <div className={styles.kanbanTaskDesc}>{t.description}</div>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
