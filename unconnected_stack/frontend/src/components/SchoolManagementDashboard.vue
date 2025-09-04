<template>
  <div class="school-management-dashboard">
    <h2>School Management Dashboard</h2>
    <section>
      <h3>Students</h3>
      <button @click="fetchStudents">Refresh</button>
      <ul>
        <li v-for="student in students" :key="student.id">{{ student.name }} ({{ student.grade }})</li>
      </ul>
    </section>
    <section>
      <h3>Staff</h3>
      <button @click="fetchStaff">Refresh</button>
      <ul>
        <li v-for="staff in staffList" :key="staff.id">{{ staff.name }} - {{ staff.role }}</li>
      </ul>
    </section>
    <section>
      <h3>Timetable</h3>
      <button @click="fetchTimetable">Refresh</button>
      <ul>
        <li v-for="entry in timetable" :key="entry.id">{{ entry.class_name }} - {{ entry.teacher }} ({{ entry.time }})</li>
      </ul>
    </section>
  </div>
</template>

<script>
import { listStudents, listStaff, listTimetable } from '../api/school_management.js';

export default {
  name: 'SchoolManagementDashboard',
  data() {
    return {
      students: [],
      staffList: [],
      timetable: []
    };
  },
  methods: {
    async fetchStudents() {
      this.students = await listStudents();
    },
    async fetchStaff() {
      this.staffList = await listStaff();
    },
    async fetchTimetable() {
      this.timetable = await listTimetable();
    }
  },
  mounted() {
    this.fetchStudents();
    this.fetchStaff();
    this.fetchTimetable();
  }
};
</script>

<style scoped>
.school-management-dashboard {
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 8px;
}
section {
  margin-bottom: 2rem;
}
</style>
