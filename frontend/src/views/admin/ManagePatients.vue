<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <h3>Manage Patients</h3>

      <div class="mb-3 mt-3">
        <input v-model="searchQuery" @input="fetchPatients" class="form-control" placeholder="Search by name, ID, or mobile...">
      </div>

      <div class="card shadow-sm">
        <table class="table table-hover mb-0">
          <thead class="table-success">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Mobile</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in patients" :key="p.id">
              <td>{{ p.id }}</td>
              <td>{{ p.full_name }}</td>
              <td>{{ p.email }}</td>
              <td>{{ p.mobile_no }}</td>
              <td>
                 <span :class="p.flag === 'active' ? 'badge bg-success' : 'badge bg-danger'">
                   {{ p.flag }}
                 </span>
              </td>
              <td>
                <router-link :to="`/admin/patient/${p.id}/history`" class="btn btn-info btn-sm me-2">History</router-link>
                <button 
                  v-if="p.flag === 'active'" 
                  @click="toggleFlag(p.id, 'blacklisted')" 
                  class="btn btn-warning btn-sm me-2">
                  Block
                </button>
                <button 
                  v-else 
                  @click="toggleFlag(p.id, 'active')" 
                  class="btn btn-success btn-sm me-2">
                  Unblock
                </button>
                
                <button @click="deletePatient(p.id)" class="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../../components/Navbar.vue';
import api from '../../services/api';
import { ref, onMounted } from 'vue';

const patients = ref([]);
const searchQuery = ref('');

const fetchPatients = async () => {
  try {
    const res = await api.get(`/admin/patient?q=${searchQuery.value}`); 
    patients.value = res.data;
  } catch (error) {
    console.error("Error fetching patients:", error);
  }
};

const toggleFlag = async (id, status) => {
  if (!confirm(`Confirm status change to: ${status}?`)) return;

  try {
    await api.put(`/admin/patient/${id}`, { flag: status });
    fetchPatients();
  } catch(e) { 
    alert("Error updating status"); 
  }
};

const deletePatient = async (id) => {
  if(!confirm("Delete patient?")) return;
  try {
    await api.delete(`/admin/patient/${id}`);
    fetchPatients();
  } catch(e) { alert("Error deleting"); }
};

onMounted(fetchPatients);
</script>