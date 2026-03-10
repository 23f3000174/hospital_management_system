<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h3>Manage Doctors</h3>
        <router-link to="/admin/add-doctor" class="btn btn-primary"> + Register Doctor</router-link>
      </div>

      <div class="mb-3">
        <input v-model="searchQuery" @input="fetchDocs" class="form-control" placeholder="Search by name or department...">
      </div>

      <div class="card shadow-sm">
        <table class="table table-hover mb-0">
          <thead class="table-primary">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Department</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in docs" :key="doc.id">
              <td>{{ doc.full_name }}</td>
              <td>{{ doc.email }}</td>
              <td>{{ doc.department }}</td>
              <td>
                <span :class="doc.status === 'active' ? 'badge bg-success' : 'badge bg-danger'">
                  {{ doc.status }}
                </span>
              </td>
              <td>

                <button 
                  v-if="doc.status === 'active'" 
                  @click="toggleStatus(doc.id, 'blacklisted')" 
                  class="btn btn-warning btn-sm me-2">
                  Block
                </button>
                <button 
                  v-else 
                  @click="toggleStatus(doc.id, 'active')" 
                  class="btn btn-success btn-sm me-2">
                  Activate
                </button>

                <button @click="deleteDoc(doc.id)" class="btn btn-danger btn-sm">Delete</button>
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

const docs = ref([]);
const searchQuery = ref('');

const fetchDocs = async () => {
  try {
    const res = await api.get(`/admin/doctor?q=${searchQuery.value}`);
    docs.value = res.data;
  } catch (error) {
    console.error("Error fetching doctors:", error);
  }
};

const toggleStatus = async (id, newStatus) => {
  if (!confirm(`Are you sure you want to change status to ${newStatus}?`)) return;
  
  try {
    await api.put(`/admin/doctor/${id}`, { flag: newStatus });
    fetchDocs(); 
  } catch (error) {
    alert(error.response?.data?.message || "Error updating status");
  }
};

const deleteDoc = async (id) => {
  if (!confirm("Are you sure? This action is permanent.")) return;
  try {
    await api.delete(`/admin/doctor/${id}`);
    fetchDocs();
  } catch (e) { 
    alert("Error deleting doctor"); 
  }
};

onMounted(fetchDocs);
</script>