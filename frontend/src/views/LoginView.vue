<template>
  <div>
    <Navbar />
    <div class="container d-flex justify-content-center align-items-center" style="min-height: 80vh;">
      <div class="card shadow p-4 border-0" style="max-width: 400px; width: 100%;">
        <h3 class="text-center mb-4 text-primary fw-bold">Login</h3>
        
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label">Email address</label>
            <input type="email" class="form-control" v-model="email" required placeholder="example@gmail.com">
          </div>
          
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" class="form-control" v-model="password" required placeholder="123@abc">
          </div>

          <div v-if="errorMessage" class="alert alert-danger p-2 text-center small">
            {{ errorMessage }}
          </div>

          <button type="submit" class="btn btn-primary w-100 fw-bold" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>

        <div class="text-center mt-3">
          <small>Don't have an account? <router-link to="/register">Register here</router-link></small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const loading = ref(false);
const router = useRouter();

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const response = await api.post('/auth/login', {
      email: email.value,
      password: password.value
    });

    console.log("Login Response:", response.data);

    const token = response.data.access_token;
    
    if (!token) {
      throw new Error("No token received from server!");
    }

    localStorage.setItem('access_token', token);
    localStorage.setItem('user_role', response.data.role);
    localStorage.setItem('user_id', response.data.user_id);
    localStorage.setItem('user_name', response.data.full_name);
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    alert("Login Successful!");

    if (response.data.role === 'Admin') {
      router.push('/admin/dashboard');
    } else if (response.data.role === 'Doctor') {
      router.push('/doctor/dashboard'); 
    } else {
      router.push('/patient/dashboard');
    }

  } catch (error) {
    console.error("Login Error:", error);
    if (error.response && error.response.data) {
      errorMessage.value = error.response.data.message;
    } else {
      errorMessage.value = error.message || 'Server error. Is the backend running?';
    }
  } finally {
    loading.value = false;
  }
};
</script>
