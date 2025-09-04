// API module for Classroom Management microservice
export async function markAttendance(studentId, present) {
  const response = await fetch('/classroom_mgmt_service/mark_attendance', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ student_id: studentId, present })
  });
  if (!response.ok) throw new Error('Failed to mark attendance');
  return await response.json();
}

export async function getAttendance() {
  const response = await fetch('/classroom_mgmt_service/get_attendance');
  if (!response.ok) throw new Error('Failed to get attendance');
  return await response.json();
}
