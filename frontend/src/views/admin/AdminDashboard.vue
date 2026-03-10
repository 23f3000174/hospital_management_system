<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <h2 class="mb-4 fw-bold text-primary">Admin Dashboard</h2>
      
      <div v-if="loading" class="spinner-border text-primary"></div>
      <div v-else class="row g-4 mb-5">
        <div class="col-md-4">
          <div class="card bg-primary text-white h-100 shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">Total Doctors</h5>
              <h1 class="display-4 fw-bold">{{ stats.total_doctors }}</h1>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card bg-success text-white h-100 shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">Total Patients</h5>
              <h1 class="display-4 fw-bold">{{ stats.total_patients }}</h1>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card bg-info text-white h-100 shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">Appointments</h5>
              <h1 class="display-4 fw-bold">{{ stats.total_appointments }}</h1>
            </div>
          </div>
        </div>
      </div>

      <h4 class="mb-3 border-bottom pb-2">Quick Actions</h4>
      <div class="row g-3">
        <div class="col-md-3">
          <router-link to="/admin/doctors" class="btn btn-outline-primary w-100 p-4 fw-bold">
            Manage Doctors
          </router-link>
        </div>
        
        <div class="col-md-3">
          <router-link to="/admin/departments" class="btn btn-outline-dark w-100 p-4 fw-bold">
            Manage Departments
          </router-link>
        </div>

        <div class="col-md-3">
          <router-link to="/admin/patients" class="btn btn-outline-success w-100 p-4 fw-bold">
            Manage Patients
          </router-link>
        </div>

        <div class="col-md-3">
          <router-link to="/admin/appointments" class="btn btn-outline-info w-100 p-4 fw-bold">
            View Appointments
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../../components/Navbar.vue';
import api from '../../services/api';
import { ref, onMounted } from 'vue';

const stats = ref({ total_doctors: 0, total_patients: 0, total_appointments: 0 });
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await api.get('/admin/dashboard');
    stats.value = res.data;
  } catch (error) {
    console.error(error);
    if (error.response && (error.response.status === 401 || error.response.status === 422)) {
      alert("Session expired. Please login again.");
      localStorage.clear();
      window.location.href = '/login';
    }
  } finally {
    loading.value = false;
  }
});
</script>