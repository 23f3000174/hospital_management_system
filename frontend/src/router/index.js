import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import ManageDoctors from '../views/admin/ManageDoctors.vue'
import AddDoctor from '../views/admin/AddDoctor.vue'
import ManageDepartments from '../views/admin/ManageDepartments.vue'
import AddDepartment from '../views/admin/AddDepartment.vue'
import ManagePatients from '../views/admin/ManagePatients.vue'
import AdminAppointments from '../views/admin/AdminAppointments.vue'
import AdminPatientHistory from '../views/admin/AdminPatientHistory.vue'
import DoctorDashboard from '../views/doctor/DoctorDashboard.vue'
import ManageAvailability from '../views/doctor/ManageAvailability.vue'
import PatientHistory from '../views/doctor/PatientHistory.vue'
import PatientDashboard from '../views/patient/PatientDashboard.vue'
import SearchDoctors from '../views/patient/SearchDoctors.vue'
import MyAppointments from '../views/patient/MyAppointments.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/admin/dashboard', name: 'admin-dashboard', component: AdminDashboard, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/admin/doctors', name: 'manage-doctors', component: ManageDoctors, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/admin/add-doctor', name: 'add-doctor', component: AddDoctor, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/admin/departments', name: 'manage-departments', component: ManageDepartments, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/admin/add-department', name: 'add-department', component: AddDepartment, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/admin/patients', name: 'manage-patients', component: ManagePatients, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/admin/appointments', name: 'admin-appointments', component: AdminAppointments, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/admin/patient/:id/history', name: 'admin-patient-history', component: AdminPatientHistory, meta: { requiresAuth: true, role: 'Admin' } },
    { path: '/doctor/dashboard', name: 'doctor-dashboard', component: DoctorDashboard, meta: { requiresAuth: true, role: 'Doctor' } },
    { path: '/doctor/availability', name: 'manage-availability', component: ManageAvailability, meta: { requiresAuth: true, role: 'Doctor' } },
    { path: '/doctor/patient/:id/history', name: 'patient-history', component: PatientHistory, meta: { requiresAuth: true, role: 'Doctor' } },
    { path: '/patient/dashboard', component: PatientDashboard, meta: { requiresAuth: true, role: 'Patient' } },
    { path: '/patient/search', component: SearchDoctors, meta: { requiresAuth: true, role: 'Patient' } },
    { path: '/patient/appointments', component: MyAppointments, meta: { requiresAuth: true, role: 'Patient' } }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  const userRole = localStorage.getItem('user_role');
  if (to.meta.requiresAuth) {
    if (!token) next('/login');
    else if (to.meta.role && to.meta.role !== userRole) { alert('Unauthorized access!'); next('/'); }
    else next();
  } else next();
});

export default router