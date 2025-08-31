// Simple Vue global state for user role
import { reactive } from 'vue';
export const store = reactive({
  role: localStorage.getItem('role') || 'student',
  setRole(newRole) {
    this.role = newRole;
    localStorage.setItem('role', newRole);
  }
});
