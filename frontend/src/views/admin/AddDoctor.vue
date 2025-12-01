<template>
  <div>
    <Navbar />
    <div class="container mt-4" style="max-width: 600px;">
      <h3 class="mb-4">Register New Doctor</h3>
      <div class="card shadow-sm">
        <div class="card-body">
          <form @submit.prevent="registerDoctor">
            <div class="row g-3">
              <div class="col-6"><label>Full Name</label><input v-model="form.full_name" type="text" class="form-control" required></div>
              <div class="col-6"><label>Email</label><input v-model="form.email" type="email" class="form-control" required></div>
              <div class="col-6"><label>Password</label><input v-model="form.password" type="password" class="form-control" required></div>
              <div class="col-6"><label>Mobile</label><input v-model="form.mobile_no" type="text" class="form-control" required></div>
              <div class="col-6"><label>Medical ID</label><input v-model="form.medical_id" type="text" class="form-control" required></div>
              <div class="col-6">
                <label>Department</label>
                <select v-model="form.department_name" class="form-select" required>
                  <option disabled value="">Select One</option>
                  <option v-for="d in depts" :key="d.id" :value="d.name">{{ d.name }}</option>
                </select>
              </div>
            </div>
            <div v-if="msg" :class="`alert alert-${type} mt-3`">{{ msg }}</div>
            <button class="btn btn-primary w-100 mt-3" :disabled="loading">Register Doctor</button>
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

const form = ref({ full_name: '', email: '', password: '', mobile_no: '', medical_id: '', department_name: '' });
const depts = ref([]);
const msg = ref(''); const type = ref(''); const loading = ref(false);

onMounted(async () => {
  const res = await api.get('/public/departments'); 
  depts.value = res.data;
});

const registerDoctor = async () => {
  loading.value = true;
  msg.value = '';
  try {
    await api.post('/admin/doctor', form.value);
    msg.value = "Doctor Added!"; type.value = "success";
    form.value = { full_name: '', email: '', password: '', mobile_no: '', medical_id: '', department_name: '' };
  } catch (e) {
    msg.value = e.response?.data?.message || "Error adding doctor"; type.value = "danger";
  } finally { loading.value = false; }
};
</script>