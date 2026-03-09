<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm mb-4">
    <div class="container">
      <router-link class="navbar-brand fw-bold" to="/"> Hospital Management System </router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>

          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" :to="dashboardLink">Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const token = localStorage.getItem('access_token');
const role = localStorage.getItem('user_role');
const name = localStorage.getItem('user_name');

const isLoggedIn = computed(() => !!token);
const userName = computed(() => name || 'User');

const dashboardLink = computed(() => {
  if (role === 'Admin') return '/admin/dashboard';
  if (role === 'Doctor') return '/doctor/dashboard';
  return '/patient/dashboard';
});

const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_role');
  localStorage.removeItem('user_id');
  window.location.href = '/login'; 
};
</script>
