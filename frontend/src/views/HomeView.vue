<template>
  <div>
    <Navbar />
    
    <div class="container text-center mt-5">

      <h1 class="display-4 fw-bold text-primary">Welcome to Hospital Management System</h1>
      <p class="lead text-secondary"><b>Your Health, Our Priority. Book appointments seamlessly.</b></p>
      
      <div v-if="loading" class="spinner-border text-primary mt-5" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      
      <div v-else class="row mt-5">
        <div class="col-md-4 mb-4" v-for="dept in departments" :key="dept.id">
          <div class="card shadow-sm h-100 border-0">
            <div class="card-body p-4">
              <h5 class="card-title fw-bold text-dark">{{ dept.name }}</h5>
              <p class="card-text text-muted small">{{ dept.description?.description }}</p>
              
              <div class="mt-3">
                 <span v-for="issue in dept.description?.issues_covered" :key="issue" class="badge bg-light text-dark border me-1">
                    {{ issue }}
                  </span>
              </div>
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
import { ref, onMounted } from 'vue';

const departments = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const response = await api.get('/public/departments');
    departments.value = response.data;
  } catch (error) {
    console.error("Failed to load departments:", error);
  } finally {
    loading.value = false;
  }
});
</script>
