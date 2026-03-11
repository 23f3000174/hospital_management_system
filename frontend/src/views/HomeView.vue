<template>
  <div>
    <Navbar />
    <div class="container text-center mt-5">
      <div class="p-5 mb-4 bg-light rounded-3 shadow-sm">
        <h1 class="display-4 fw-bold text-primary">Welcome to HMS V2</h1>
        <p class="lead">Your Health, Our Priority. Book appointments seamlessly.</p>
        <button v-if="!isLoggedIn" @click="handleBookClick" class="btn btn-primary btn-lg px-4 gap-3">Book Appointment</button>
        <router-link v-else :to="dashboardLink" class="btn btn-primary btn-lg px-4 gap-3">Go to Dashboard</router-link>
      </div>
      <h3 class="mb-4 text-start border-bottom pb-2">Our Departments</h3>
      <div v-if="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
      <div v-else-if="errorMessage" class="alert alert-danger"><strong>Error:</strong> {{ errorMessage }}</div>
      <div v-else class="row g-4">
        <div class="col-md-4" v-for="dept in departments" :key="dept.id">
          <div class="card h-100 shadow-sm hover-card">
            <div class="card-body text-start">
              <h5 class="card-title fw-bold mb-0">{{ dept.name }}</h5>
              <p class="card-text text-muted small">{{ getDesc(dept.description) }}</p>
              <div class="mt-2"><span v-for="issue in getIssues(dept.description)" :key="issue" class="badge bg-light text-dark border me-1">{{ issue }}</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import Navbar from '../components/Navbar.vue';
import api from '../services/api';
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const departments = ref([]);
const loading = ref(true);
const errorMessage = ref('');

const token = localStorage.getItem('access_token');
const role = localStorage.getItem('user_role');
const isLoggedIn = ref(!!token);

const dashboardLink = computed(() => {
  if (role === 'Admin') return '/admin/dashboard';
  if (role === 'Doctor') return '/doctor/dashboard';
  return '/patient/dashboard';
});

const getDesc = (descData) => (!descData ? 'No description.' : (typeof descData === 'string' ? descData : descData.description || 'No description.'));
const getIssues = (descData) => (!descData ? [] : (Array.isArray(descData.issues_covered) ? descData.issues_covered : []));

const handleBookClick = () => {
  router.push('/login'); 
};
onMounted(async () => {
  try {
    const response = await api.get('/public/departments');
    departments.value = response.data;
  } catch (error) { errorMessage.value = "Could not connect to Backend."; } 
  finally { loading.value = false; }
});
</script>