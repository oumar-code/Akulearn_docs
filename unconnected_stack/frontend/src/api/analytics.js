// API module for Analytics microservice
export async function reportProgress(studentId, lessonId, score, timeSpent) {
  const response = await fetch('/analytics_service/report_progress', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ student_id: studentId, lesson_id: lessonId, score, time_spent: timeSpent })
  });
  if (!response.ok) throw new Error('Failed to report progress');
  return await response.json();
}

export async function getReports() {
  const response = await fetch('/analytics_service/get_reports');
  if (!response.ok) throw new Error('Failed to get reports');
  return await response.json();
}
