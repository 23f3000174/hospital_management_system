<template>
  <div>
    <Navbar />
    <div class="container mt-5" style="max-width: 500px;">
      <div class="card shadow p-4 border-0">
        <h3 class="text-center mb-4 text-primary fw-bold">Patient Registration</h3>
        
        <form @submit.prevent="handleRegister">
          
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input v-model="form.full_name" type="text" class="form-control" required placeholder="John Doe">
          </div>

          <div class="mb-3">
            <label class="form-label">Email Address</label>
            <input v-model="form.email" type="email" class="form-control" required placeholder="john@example.com">
          </div>

          <div class="row g-2 mb-3">
            <div class="col-6">
              <label class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-control" required>
            </div>
            <div class="col-6">
              <label class="form-label">Mobile No</label>
              <input v-model="form.mobile_no" type="text" class="form-control" required placeholder="9876543210">
            </div>
          </div>

          <div class="row g-2 mb-3">
            <div class="col-6">
              <label class="form-label">Age</label>
              <input v-model="form.age" type="number" class="form-control" required placeholder="25">
            </div>
            <div class="col-6">
              <label class="form-label">Gender</label>
              <select v-model="form.gender" class="form-select" required>
                <option disabled value="">Select</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div v-if="message" :class="`alert alert-${msgType} text-center`">
            {{ message }}
          </div>

          <button type="submit" class="btn btn-primary w-100 fw-bold" :disabled="loading">
            {{ loading ? 'Registering...' : 'Register' }}
          </button>
        </form>

        <div class="text-center mt-3">
          <small>Already have an account? <router-link to="/login">Login here</router-link></small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue';
import api from '../services/api';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const form = ref({
  full_name: '',
  email: '',
  password: '',
  mobile_no: '',
  age: '',
  gender: ''
});

const message = ref('');
const msgType = ref('success'); 
const loading = ref(false);

const handleRegister = async () => {
  loading.value = true;
  message.value = '';

  try {
    const response = await api.post('/auth/register', form.value);
    
    message.value = "Registration Successful! Redirecting...";
    msgType.value = "success";
    
    setTimeout(() => {
      router.push('/login');
    }, 1500);

  } catch (error) {
    if (error.response && error.response.data) {
      message.value = error.response.data.message; 
    } else {
      message.value = "Server error. Please try again.";
    }
    msgType.value = "danger";
  } finally {
    loading.value = false;
  }
};
</script>