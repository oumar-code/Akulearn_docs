"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabaseClient";
import styles from "./user-management.module.css";

  type User = { id: string; email: string; role?: string };
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch users from Supabase (requires service role key in a secure API route in production)
  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      setError("");
      try {
        // This is a placeholder. In production, use a secure API route to fetch users with the service role key.
        const { data, error } = await supabase.rpc('list_users');
        if (error) throw error;
        setUsers(data || []);
      } catch {
        setError("Unable to fetch users. This feature requires a secure API route with service role key.");
      }
      setLoading(false);
    };
    fetchUsers();
  }, []);

  return (
    <div className={styles.userPanel}>
      <h3>User Management</h3>
      {loading && <div>Loading users...</div>}
      {error && <div className={styles.userError}>{error}</div>}
      {!loading && !error && (
        <table className={styles.userTable}>
          <thead>
            <tr>
              <th>Email</th>
              <th>Role</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id}>
                <td>{user.email}</td>
                <td>{user.role || '-'}</td>
                <td className={styles.userActions}>
                  {/* Add actions: Remove, Assign Role, Reset Password */}
                  <button disabled>Remove</button>
                  <button disabled>Assign Role</button>
                  <button disabled>Reset Password</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <div className={styles.userAdd}>
        <button disabled>Add User (Coming Soon)</button>
      </div>
      <p className={styles.userNote}>
        Note: For security, user management actions should be implemented via a secure API route using the Supabase service role key.
      </p>
    </div>
  );
}

export default UserManagementPanel;
