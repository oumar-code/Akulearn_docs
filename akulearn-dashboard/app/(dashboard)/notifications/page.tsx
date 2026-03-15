"use client";
import { useEffect, useState } from "react";
import styles from "./notifications.module.css";


import { supabase } from "../../../lib/supabaseClient";


type Notification = { id: string; message: string; read?: boolean };

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  // Fetch notifications from Supabase
  useEffect(() => {
    let channel: ReturnType<typeof supabase.channel> | null = null;
    const fetchNotifications = async () => {
      const { data, error } = await supabase.from('notifications').select('*').order('created_at', { ascending: false });
      if (!error) setNotifications(data || []);
    };
    fetchNotifications();

    // Subscribe to real-time changes
    channel = supabase.channel('public:notifications')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'notifications' }, (payload) => {
        fetchNotifications();
      })
      .subscribe();

    return () => {
      if (channel) supabase.removeChannel(channel);
    };
  }, []);

  return (
    <div className={styles.notificationsPanel}>
      <h2>Notifications</h2>
      {notifications.length === 0 && <div>No notifications.</div>}
      <ul className={styles.notificationsList}>
        {notifications.map(n => (
          <li
            key={n.id}
            className={
              styles.notificationItem + ' ' + (n.read ? styles.notificationRead : styles.notificationUnread)
            }
          >
            {n.message}
          </li>
        ))}
      </ul>
    </div>
  );
}
