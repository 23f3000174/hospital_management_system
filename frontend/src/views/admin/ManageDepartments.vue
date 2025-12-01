<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>Manage Departments</h3>
        <router-link to="/admin/add-department" class="btn btn-success"> + Add New</router-link>
      </div>

      <div class="card shadow-sm">
        <table class="table table-hover mb-0">
          <thead class="table-dark">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Issues</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in depts" :key="d.id">
              <td class="fw-bold">{{ d.name }}</td>
              <td>{{ d.description?.description || 'No description' }}</td>
              <td>
                <span v-for="i in d.description?.issues_covered" :key="i" class="badge bg-light text-dark border me-1">
                  {{ i }}
                </span>
              </td>
              <td>
                <button @click="deleteDept(d.id)" class="btn btn-danger btn-sm">Delete</button>
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

const depts = ref([]);

const fetchDepts = async () => {
  try {
    const res = await api.get('/admin/department');
    depts.value = res.data;
  } catch (e) { console.error(e); }
};

const deleteDept = async (id) => {
  if(!confirm("Delete this department?")) return;
  try {
    await api.delete(`/admin/department/${id}`);
    fetchDepts();
  } catch (e) {
    alert(e.response?.data?.message || "Cannot delete department");
  }
};

onMounted(fetchDepts);
</script>