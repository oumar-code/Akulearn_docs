// API module for School Management microservice
export async function addStudent(student) {
  const response = await fetch('/school_management_service/students/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(student)
  });
  if (!response.ok) throw new Error('Failed to add student');
  return await response.json();
}

export async function listStudents() {
  const response = await fetch('/school_management_service/students/list');
  if (!response.ok) throw new Error('Failed to list students');
  return await response.json();
}

export async function addStaff(staff) {
  const response = await fetch('/school_management_service/staff/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(staff)
  });
  if (!response.ok) throw new Error('Failed to add staff');
  return await response.json();
}

export async function listStaff() {
  const response = await fetch('/school_management_service/staff/list');
  if (!response.ok) throw new Error('Failed to list staff');
  return await response.json();
}

export async function addTimetable(entry) {
  const response = await fetch('/school_management_service/timetable/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(entry)
  });
  if (!response.ok) throw new Error('Failed to add timetable entry');
  return await response.json();
}

export async function listTimetable() {
  const response = await fetch('/school_management_service/timetable/list');
  if (!response.ok) throw new Error('Failed to list timetable');
  return await response.json();
}
