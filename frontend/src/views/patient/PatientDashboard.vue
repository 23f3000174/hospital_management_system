<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <h2 class="mb-4">Patient Dashboard</h2>
      
      <div class="row g-4 mb-5">
        <div class="col-md-4">
          <div class="card bg-primary text-white p-4 h-100">
            <h3>Find a Doctor</h3>
            <p>Search by specialization and book your slot.</p>
            <router-link to="/patient/search" class="btn btn-light fw-bold text-primary">Book Now</router-link>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card bg-success text-white p-4 h-100">
            <h3>My Appointments</h3>
            <p>View upcoming visits and past history.</p>
            <router-link to="/patient/appointments" class="btn btn-light fw-bold text-success">View History</router-link>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card bg-info text-white p-4 h-100">
            <h3>Export Records</h3>
            <p>Download your complete treatment history as a CSV.</p>
            <button @click="exportCSV" :disabled="exporting" class="btn btn-light fw-bold text-info">
              <span v-if="exporting" class="spinner-border spinner-border-sm me-2"></span>
              {{ exporting ? 'Exporting...' : 'Export CSV' }}
            </button>
            <div v-if="exportMsg" class="mt-2 small text-dark fw-bold bg-light p-1 rounded">{{ exportMsg }}</div>
          </div>
        </div>
      </div>

      <div class="card shadow-sm">
        <div class="card-header bg-dark text-white">My Profile</div>
        <div class="card-body">
          <form @submit.prevent="updateProfile">
            <div class="row g-3">
              <div class="col-md-6">
                <label>Name</label>
                <input v-model="profile.full_name" class="form-control" type="text" required>
              </div>
              <div class="col-md-6">
                <label>Email</label>
                <input v-model="profile.email" class="form-control" type="email" disabled>
              </div>
              <div class="col-md-4">
                <label>Mobile</label>
                <input v-model="profile.mobile_no" class="form-control" type="text">
              </div>
              <div class="col-md-4">
                <label>Age</label>
                <input v-model="profile.age" class="form-control" type="number">
              </div>
              <div class="col-md-4">
                <label>Gender</label>
                <input v-model="profile.gender" class="form-control" type="text" disabled>
              </div>
            </div>
            <button class="btn btn-primary mt-3">Update Profile</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../../components/Navbar.vue';
import api from '../../services/api';
import { ref, onMounted } from 'vue';

const profile = ref({});
const exporting = ref(false);
const exportMsg = ref('');

onMounted(async () => {
  const res = await api.get('/patient/profile');
  profile.value = res.data;
});

const updateProfile = async () => {
  try {
    await api.put('/patient/profile', profile.value);
    alert("Profile Updated!");
  } catch(e) { alert("Error updating profile"); }
};

const exportCSV = async () => {
  exporting.value = true;
  exportMsg.value = '';
  try {
    const res = await api.get('/patient/export');
    exportMsg.value = res.data.message;
  } catch (error) {
    exportMsg.value = "Failed to start export.";
  } finally {
    exporting.value = false;
  }
};
</script>