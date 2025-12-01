<template>
  <div>
    <Navbar />
    <div class="container mt-4" style="max-width: 600px;">
      <h3 class="mb-4">Add New Department</h3>
      <div class="card shadow-sm">
        <div class="card-body">
          <form @submit.prevent="addDept">
            <div class="mb-3">
              <label class="fw-bold">Department Name</label>
              <input v-model="name" type="text" class="form-control" required placeholder="Cardiology">
            </div>
            <div class="mb-3">
              <label class="fw-bold">Description</label>
              <textarea v-model="desc" class="form-control" rows="3" required></textarea>
            </div>
            <div class="mb-3">
              <label class="fw-bold">Issues Covered (Comma separated)</label>
              <input v-model="issues" type="text" class="form-control" placeholder="Flu, Fever, Pain">
            </div>
            
            <div v-if="msg" :class="`alert alert-${type}`">{{ msg }}</div>
            <button class="btn btn-primary w-100" :disabled="loading">Create Department</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import Navbar from '../../components/Navbar.vue';
import api from '../../services/api';
import { ref } from 'vue';

const name = ref('');
const desc = ref('');
const issues = ref('');
const msg = ref('');
const type = ref('success');
const loading = ref(false);

const addDept = async () => {
  loading.value = true;
  msg.value = '';
  const issuesList = issues.value.split(',').map(i => i.trim()).filter(i => i);

  try {
    await api.post('/admin/department', {
      department_name: name.value,
      description: { description: desc.value, issues_covered: issuesList }
    });
    msg.value = "Success!"; type.value = "success";
    name.value = ''; desc.value = ''; issues.value = '';
  } catch (e) {
    msg.value = e.response?.data?.message || "Error"; type.value = "danger";
  } finally { loading.value = false; }
};
</script>