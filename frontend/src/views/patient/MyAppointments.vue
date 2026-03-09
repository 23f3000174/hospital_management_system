<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <h3 class="mb-4">My Appointments</h3>
      
      <div class="card shadow-sm">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Date / Time</th>
              <th>Doctor</th>
              <th>Status</th>
              <th>Details</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="apt in appointments" :key="apt.id">
              <td>
                <div>{{ apt.date }}</div>
                <small class="text-muted">{{ apt.start_time }}</small>
              </td>
              <td>
                <div class="fw-bold">{{ apt.doctor_name }}</div>
                <small>{{ apt.department }}</small>
              </td>
              <td>
                <span :class="getStatusClass(apt.status)">{{ apt.status }}</span>
              </td>
              <td>
                <div v-if="apt.status === 'Completed'">
                  <strong>Dx:</strong> {{ apt.diagnosis?.text }} <br>
                  <small><strong>Rx:</strong> {{ apt.prescription?.list?.join(', ') }}</small>
                </div>
                <span v-else class="text-muted">-</span>
              </td>
              <td>
                <button 
                  v-if="apt.status === 'Booked'" 
                  @click="cancelAppt(apt.id)" 
                  class="btn btn-sm btn-outline-danger">
                  Cancel
                </button>
              </td>
            </tr>
            <tr v-if="appointments.length === 0"><td colspan="5" class="text-center p-4">No history found.</td></tr>
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

const appointments = ref([]);

const fetchAppts = async () => {
  const res = await api.get('/patient/my-appointments');
  appointments.value = res.data;
};

const cancelAppt = async (id) => {
  if(!confirm("Cancel this appointment?")) return;
  await api.put(`/patient/appointment/${id}/cancel`);
  fetchAppts();
};

const getStatusClass = (status) => {
  if(status === 'Booked') return 'badge bg-primary';
  if(status === 'Completed') return 'badge bg-success';
  return 'badge bg-secondary';
};

onMounted(fetchAppts);
</script>