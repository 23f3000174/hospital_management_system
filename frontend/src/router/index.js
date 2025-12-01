import { createRouter, createWebHistory } from 'vue-router'

// 1. Core Views
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

// 2. Admin Views (Make sure ALL 5 are imported here)
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import ManageDoctors from '../views/admin/ManageDoctors.vue'
import AddDoctor from '../views/admin/AddDoctor.vue'             // <-- This was likely missing
import ManageDepartments from '../views/admin/ManageDepartments.vue'
import AddDepartment from '../views/admin/AddDepartment.vue'     // <-- Check this one too
import ManagePatients from '../views/admin/ManagePatients.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // --- Public Routes ---
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },

    // --- Admin Routes ---
    { 
      path: '/admin/dashboard', 
      name: 'admin-dashboard', 
      component: AdminDashboard,
      meta: { requiresAuth: true, role: 'Admin' }
    },
    // Doctors
    { 
      path: '/admin/doctors', 
      name: 'manage-doctors', 
      component: ManageDoctors,
      meta: { requiresAuth: true, role: 'Admin' }
    },
    { 
      path: '/admin/add-doctor', 
      name: 'add-doctor', 
      component: AddDoctor, // Now this will work because it is imported above
      meta: { requiresAuth: true, role: 'Admin' }
    },
    // Departments
    { 
      path: '/admin/departments', 
      name: 'manage-departments', 
      component: ManageDepartments,
      meta: { requiresAuth: true, role: 'Admin' }
    },
    { 
      path: '/admin/add-department', 
      name: 'add-department', 
      component: AddDepartment,
      meta: { requiresAuth: true, role: 'Admin' }
    },
    // Patients
    { 
      path: '/admin/patients', 
      name: 'manage-patients', 
      component: ManagePatients,
      meta: { requiresAuth: true, role: 'Admin' }
    }
  ]
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  const userRole = localStorage.getItem('user_role');

  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login');
    } else if (to.meta.role && to.meta.role !== userRole) {
      alert('Unauthorized access!');
      next('/'); 
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router