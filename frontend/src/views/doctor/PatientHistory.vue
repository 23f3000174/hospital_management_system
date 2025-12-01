<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <h3>Patient Medical History</h3>
      <div v-if="history.length === 0" class="alert alert-info mt-3">No history found for this patient.</div>
      
      <div v-else class="timeline mt-4">
        <div v-for="(record, index) in history" :key="index" class="card mb-3 shadow-sm">
          <div class="card-header d-flex justify-content-between">
            <strong>{{ record.date }}</strong>
            <span class="text-muted">Dr. {{ record.doctor }}</span>
          </div>
          <div class="card-body">
            <p><strong>Diagnosis:</strong> {{ record.diagnosis.text }}</p>
            <p><strong>Prescription:</strong></p>
            <ul>
              <li v-for="med in record.prescription.list" :key="med">{{ med }}</li>
            </ul>
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
const history = ref([]);

onMounted(async () => {
  try {
    const res = await api.get(`/doctor/patient-history/${route.params.id}`);
    history.value = res.data;
  } catch (e) { console.error(e); }
});
</script>
```

#### 6. Update `frontend/src/router/index.js`
Add the new routes.

```javascript
// ... existing imports ...
import DoctorDashboard from '../views/doctor/DoctorDashboard.vue'
import ManageAvailability from '../views/doctor/ManageAvailability.vue'
import PatientHistory from '../views/doctor/PatientHistory.vue'

// ... inside routes array ...
    // --- Doctor Routes ---
    { path: '/doctor/dashboard', component: DoctorDashboard, meta: { requiresAuth: true, role: 'Doctor' } },
    { path: '/doctor/availability', component: ManageAvailability, meta: { requiresAuth: true, role: 'Doctor' } },
    { path: '/doctor/patient/:id/history', component: PatientHistory, meta: { requiresAuth: true, role: 'Doctor' } },
