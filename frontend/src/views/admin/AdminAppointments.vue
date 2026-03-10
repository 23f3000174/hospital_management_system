<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <h3 class="mb-4">All Appointments</h3>

      <div class="btn-group mb-4">
        <button v-for="f in filters" :key="f.value"
          @click="activeFilter = f.value; fetchAppointments()"
          :class="activeFilter === f.value ? 'btn btn-primary' : 'btn btn-outline-primary'">
          {{ f.label }}
        </button>
      </div>

      <div class="card shadow-sm">
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead class="table-dark">
              <tr>
                <th>Date / Time</th>
                <th>Doctor</th>
                <th>Patient</th>
                <th>Status</th>
                <th>Treatment</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="apt in appointments" :key="apt.id">
                <td>
                  <div>{{ apt.date }}</div>
                  <small class="text-muted">{{ apt.start_time }}</small>
                </td>
                <td>{{ apt.doctor_name }}</td>
                <td>
                  {{ apt.patient_name }}
                  <button @click="viewHistory(apt.patient_id)" class="btn btn-link btn-sm p-0 ms-1">(History)</button>
                </td>
                <td>
                  <span :class="getStatusClass(apt.status)">{{ apt.status }}</span>
                </td>
                <td>
                  <div v-if="apt.diagnosis">
                    <strong>Dx:</strong> {{ apt.diagnosis?.text || apt.diagnosis }}
                    <br><small><strong>Rx:</strong> {{ formatPrescription(apt.prescription) }}</small>
                  </div>
                  <span v-else class="text-muted">-</span>
                </td>
                <td>
                  <router-link :to="`/admin/patient/${apt.patient_id}/history`" class="btn btn-outline-info btn-sm">
                    View Records
                  </router-link>
                </td>
              </tr>
              <tr v-if="appointments.length === 0">
                <td colspan="6" class="text-center p-4 text-muted">No appointments found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../../components/Navbar.vue';
import api from '../../services/api';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const appointments = ref([]);
const activeFilter = ref('');

const filters = [
  { label: 'All', value: '' },
  { label: 'Upcoming', value: 'upcoming' },
  { label: 'Completed', value: 'completed' },
  { label: 'Cancelled', value: 'cancelled' },
  { label: 'Past', value: 'past' }
];

const fetchAppointments = async () => {
  try {
    const res = await api.get(`/admin/appointments?status=${activeFilter.value}`);
    appointments.value = res.data;
  } catch (e) { console.error(e); }
};

const getStatusClass = (status) => {
  if (status === 'Booked') return 'badge bg-primary';
  if (status === 'Completed') return 'badge bg-success';
  return 'badge bg-danger';
};

const formatPrescription = (p) => {
  if (!p) return '';
  if (p.list) return p.list.join(', ');
  return String(p);
};

const viewHistory = (patientId) => {
  router.push(`/admin/patient/${patientId}/history`);
};

onMounted(fetchAppointments);
</script>
