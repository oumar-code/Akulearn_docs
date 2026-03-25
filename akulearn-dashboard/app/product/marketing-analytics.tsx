"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabaseClient";
import styles from "./marketing-analytics.module.css";
import dynamic from "next/dynamic";

const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

export default function MarketingAnalytics() {
  type Campaign = { id: string; name?: string; engagement?: number; reach?: number };
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCampaigns = async () => {
      setLoading(true);
      setError("");
      try {
        // Replace 'marketing_campaigns' with your actual table name
        const { data, error } = await supabase.from('marketing_campaigns').select('*');
        if (error) throw error;
        setCampaigns(data || []);
      } catch (err) {
        setError("Unable to fetch marketing analytics. Please check your Supabase table and permissions.");
      }
      setLoading(false);
    };
    fetchCampaigns();
  }, []);

  // Example chart data (replace with real data mapping)
  const chartOptions = {
    chart: { id: 'marketing-analytics' },
    xaxis: { categories: campaigns.map(c => c.name || c.id) },
  };
  const chartSeries = [
    {
      name: 'Engagement',
      data: campaigns.map(c => c.engagement || 0),
    },
    {
      name: 'Reach',
      data: campaigns.map(c => c.reach || 0),
    },
  ];

  return (
    <div className={styles.marketingPanel}>
      <h3>Marketing Analytics</h3>
      {loading && <div>Loading analytics...</div>}
      {error && <div className={styles.marketingError}>{error}</div>}
      {!loading && !error && campaigns.length > 0 && (
        <Chart options={chartOptions} series={chartSeries} type="bar" height={320} />
      )}
      {!loading && !error && campaigns.length === 0 && <div>No campaign data available.</div>}
    </div>
  );
}
