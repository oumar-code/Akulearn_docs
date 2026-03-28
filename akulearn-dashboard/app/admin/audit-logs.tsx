"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabaseClient";
import styles from "./audit-logs.module.css";

type Log = { id: string; user: string; action: string; details?: string; created_at: string };

export default function AuditLogsViewer() {
  const [logs, setLogs] = useState<Log[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState<{ user: string; action: string; date: string }>({ user: '', action: '', date: '' });

  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      setError("");
      try {
        let query = supabase.from('audit_logs').select('*').order('created_at', { ascending: false });
        if (filter.user) query = query.eq('user', filter.user);
        if (filter.action) query = query.eq('action', filter.action);
        if (filter.date) query = query.gte('created_at', filter.date);
        const { data, error } = await query;
        if (error) throw error;
        setLogs(data || []);
      } catch {
        setError("Unable to fetch audit logs. Please check your Supabase table and permissions.");
      }
      setLoading(false);
    };
    fetchLogs();
  }, [filter]);

  return (
    <div className={styles.auditPanel}>
      <h3>Audit Logs Viewer</h3>
      <div className={styles.auditFilter}>
        <label htmlFor="audit-user" className={styles.auditLabel}>User:</label>
        <input
          id="audit-user"
          className={styles.auditInput}
          placeholder="User"
          title="Filter by user"
          value={filter.user}
          onChange={e => setFilter(f => ({ ...f, user: e.target.value }))}
        />
        <label htmlFor="audit-action" className={styles.auditLabel}>Action:</label>
        <input
          id="audit-action"
          className={styles.auditInput}
          placeholder="Action"
          title="Filter by action"
          value={filter.action}
          onChange={e => setFilter(f => ({ ...f, action: e.target.value }))}
        />
        <label htmlFor="audit-date" className={styles.auditLabel}>Date:</label>
        <input
          id="audit-date"
          type="date"
          className={styles.auditInput}
          title="Filter by date"
          value={filter.date}
          onChange={e => setFilter(f => ({ ...f, date: e.target.value }))}
        />
        <button className={styles.auditClear} onClick={() => setFilter({ user: '', action: '', date: '' })}>Clear</button>
      </div>
      {loading && <div>Loading logs...</div>}
      {error && <div className={styles.auditError}>{error}</div>}
      {!loading && !error && logs.length > 0 && (
        <table className={styles.auditTable}>
          <thead>
            <tr>
              <th>User</th>
              <th>Action</th>
              <th>Details</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {logs.map(log => (
              <tr key={log.id}>
                <td>{log.user}</td>
                <td>{log.action}</td>
                <td>{log.details}</td>
                <td>{log.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {!loading && !error && logs.length === 0 && <div>No logs found.</div>}
    </div>
  );
}
