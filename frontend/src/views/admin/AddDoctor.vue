<template>
  <div>
    <Navbar />
    <div class="container mt-4" style="max-width: 600px;">
      <h3 class="mb-4">Register New Doctor</h3>
      <div class="card shadow-sm">
        <div class="card-body">
          <form @submit.prevent="registerDoctor">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Full Name</label>
                <input v-model="form.full_name" type="text" class="form-control" required placeholder="Dr. Abc">
              </div>
              <div class="col-md-6">
                <label class="form-label">Email</label>
                <input v-model="form.email" type="email" class="form-control" required placeholder="abc@hospital.com">
              </div>
              <div class="col-md-6">
                <label class="form-label">Password</label>
                <input v-model="form.password" type="password" class="form-control" required placeholder="******">
              </div>
              <div class="col-md-6">
                <label class="form-label">Mobile No</label>
                <input v-model="form.mobile_no" type="text" class="form-control" required placeholder="9876543210">
              </div>
              <div class="col-md-6">
                <label class="form-label">Medical ID</label>
                <input v-model="form.medical_id" type="text" class="form-control" required placeholder="MED-123">
              </div>
              
              <div class="col-md-6">
                <label class="form-label">Department</label>
                <select v-model="form.department_name" class="form-select" required>
                  <option disabled value="">Select Department</option>
                  <option v-for="d in depts" :key="d.id" :value="d.name">
                    {{ d.name }}
                  </option>
                </select>
                <div v-if="depts.length === 0" class="form-text text-danger">
                  No departments found. Add one first!
                </div>
              </div>
            </div>

            <div v-if="msg" :class="`alert alert-${type} mt-3`">{{ msg }}</div>
            
            <button type="submit" class="btn btn-primary w-100 mt-3" :disabled="loading">
              {{ loading ? 'Registering...' : 'Register Doctor' }}
            </button>
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

const form = ref({ 
  full_name: '', 
  email: '', 
  password: '', 
  mobile_no: '', 
  medical_id: '', 
  department_name: '' 
});

const depts = ref([]);
const msg = ref(''); 
const type = ref('success'); 
const loading = ref(false);

onMounted(async () => {
  try {
    const res = await api.get('/public/departments'); 
    depts.value = res.data;
  } catch (error) {
    console.error("Error loading departments:", error);
  }
});

const registerDoctor = async () => {
  loading.value = true;
  msg.value = '';
  
  try {
    await api.post('/admin/doctor', form.value);
    
    msg.value = "Doctor Registered Successfully!"; 
    type.value = "success";
    

    form.value = { 
      full_name: '', email: '', password: '', 
      mobile_no: '', medical_id: '', department_name: '' 
    };
    
  } catch (e) {
    msg.value = e.response?.data?.message || "Error adding doctor"; 
    type.value = "danger";
  } finally { 
    loading.value = false; 
  }
};
</script>