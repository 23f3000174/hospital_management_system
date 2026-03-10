<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>Treatment History: {{ patientName }}</h3>
        <button @click="$router.back()" class="btn btn-outline-secondary">Back</button>
      </div>

      <div v-if="records.length === 0" class="alert alert-info">No treatment records found for this patient.</div>

      <div v-else>
        <div v-for="(record, index) in records" :key="index" class="card mb-3 shadow-sm">
          <div class="card-header d-flex justify-content-between">
            <strong>{{ record.date }}</strong>
            <span class="text-muted">Dr. {{ record.doctor }}</span>
          </div>
          <div class="card-body">
            <p><strong>Diagnosis:</strong> {{ record.diagnosis?.text || record.diagnosis }}</p>
            <p><strong>Prescription:</strong></p>
            <ul v-if="record.prescription?.list">
              <li v-for="med in record.prescription.list" :key="med">{{ med }}</li>
            </ul>
            <p v-else>{{ record.prescription }}</p>
            <p class="text-muted small">Notes: {{ record.notes }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../../components/Navbar.vue';
import api from '../../services/api';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const patientName = ref('');
const records = ref([]);

onMounted(async () => {
  try {
    const res = await api.get(`/admin/patient-history/${route.params.id}`);
    patientName.value = res.data.patient_name;
    records.value = res.data.records;
  } catch (e) { console.error(e); }
});
</script>
