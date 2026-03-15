"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../../lib/supabaseClient";
import styles from "./system-analytics.module.css";
import dynamic from "next/dynamic";

const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

export default function SystemAnalyticsDashboard() {
  type UserStat = { id: string; date?: string; active_users?: number; new_signups?: number };
  const [userStats, setUserStats] = useState<UserStat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true);
      setError("");
      try {
        // Replace with your actual analytics query/table
        const { data, error } = await supabase.from('user_activity').select('*');
        if (error) throw error;
        setUserStats(data || []);
      } catch {
        setError("Unable to fetch analytics data. Please check your Supabase table and permissions.");
      }
      setLoading(false);
    };
    fetchStats();
  }, []);

  // Example chart data (replace with real data mapping)
  const chartOptions = {
    chart: { id: 'user-activity' },
    xaxis: { categories: userStats.map(u => u.date || u.id) },
  };
  const chartSeries = [
    {
      name: 'Active Users',
      data: userStats.map(u => u.active_users || 0),
    },
    {
      name: 'New Signups',
      data: userStats.map(u => u.new_signups || 0),
    },
  ];

  return (
    <div className={styles.analyticsPanel}>
      <h3>System Analytics Dashboard</h3>
      {loading && <div>Loading analytics...</div>}
      {error && <div className={styles.analyticsError}>{error}</div>}
      {!loading && !error && userStats.length > 0 && (
        <Chart options={chartOptions} series={chartSeries} type="line" height={320} />
      )}
      {!loading && !error && userStats.length === 0 && <div>No analytics data available.</div>}
    </div>
  );
}
