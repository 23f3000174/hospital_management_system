<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <h2 class="mb-4">Doctor Dashboard</h2>
      
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card bg-primary text-white p-3">
            <h4>Upcoming Appointments</h4>
            <h1 class="fw-bold">{{ appointments.length }}</h1>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card bg-success text-white p-3">
            <h4>Assigned Patients</h4>
            <h1 class="fw-bold">{{ stats.total_patients }}</h1>
          </div>
        </div>
        <div class="col-md-4 d-flex align-items-center justify-content-end">
          <router-link to="/doctor/availability" class="btn btn-outline-primary btn-lg w-100 h-100 d-flex align-items-center justify-content-center">
            📅 Manage Availability
          </router-link>
        </div>
      </div>

      <!-- Appointments Table -->
      <div class="card shadow-sm">
        <div class="card-header bg-dark text-white">Today's Schedule</div>
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Patient</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="apt in appointments" :key="apt.id">
                <td>{{ apt.date }}</td>
                <td>{{ apt.start_time }}</td>
                <td>
                  {{ apt.patient_name }} 
                  <button @click="viewHistory(apt.patient_id)" class="btn btn-link btn-sm p-0 ms-2">(History)</button>
                </td>
                <td>
                  <span :class="getStatusClass(apt.status)">{{ apt.status }}</span>
                </td>
                <td>
                  <div v-if="apt.status === 'Booked'">
                    <button @click="openTreatment(apt)" class="btn btn-success btn-sm me-2">Treat</button>
                    <button @click="cancelApt(apt.id)" class="btn btn-danger btn-sm">Cancel</button>
                  </div>
                  <span v-else class="text-muted">No actions</span>
                </td>
              </tr>
              <tr v-if="appointments.length === 0"><td colspan="5" class="text-center p-3">No appointments found.</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Treatment Modal (Simple Custom Modal) -->
    <div v-if="showModal" class="modal d-block" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">Treating: {{ selectedApt.patient_name }}</h5>
            <button @click="showModal = false" class="btn-close btn-close-white"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitTreatment">
              <div class="mb-3">
                <label class="fw-bold">Diagnosis</label>
                <input v-model="form.diagnosis" class="form-control" required placeholder="e.g. Viral Fever">
              </div>
              <div class="mb-3">
                <label class="fw-bold">Prescription</label>
                <textarea v-model="form.prescription" class="form-control" rows="3" required placeholder="e.g. Paracetamol 500mg (Morning/Night)"></textarea>
              </div>
              <div class="mb-3">
                <label class="fw-bold">Doctor Notes</label>
                <textarea v-model="form.notes" class="form-control" rows="2" placeholder="Internal notes..."></textarea>
              </div>
              <button class="btn btn-success w-100">Complete Appointment</button>
            </form>
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
import { useRouter } from 'vue-router';

const router = useRouter();
const appointments = ref([]);
const stats = ref({ total_patients: 0 });
const showModal = ref(false);
const selectedApt = ref(null);
const form = ref({ diagnosis: '', prescription: '', notes: '' });

const fetchDashboard = async () => {
  try {
    const res = await api.get('/doctor/dashboard');
    appointments.value = res.data.appointments;
    stats.value.total_patients = res.data.total_patients;
  } catch (e) { console.error(e); }
};

const getStatusClass = (status) => {
  if (status === 'Booked') return 'badge bg-primary';
  if (status === 'Completed') return 'badge bg-success';
  return 'badge bg-danger';
};

const cancelApt = async (id) => {
  if(!confirm("Cancel this appointment?")) return;
  await api.put(`/doctor/appointment/${id}`, { status: 'Cancelled' });
  fetchDashboard();
};

const openTreatment = (apt) => {
  selectedApt.value = apt;
  form.value = { diagnosis: '', prescription: '', notes: '' };
  showModal.value = true;
};

const submitTreatment = async () => {
  try {
    // Send diagnosis/prescription as Strings or JSON based on your Model requirement.
    // Assuming Model stores JSON but we input strings for simplicity:
    const payload = {
      diagnosis: { text: form.value.diagnosis },
      prescription: { list: form.value.prescription.split('\n') },
      notes: form.value.notes
    };
    
    await api.post(`/doctor/treatment/${selectedApt.value.id}`, payload);
    showModal.value = false;
    alert("Treatment Recorded!");
    fetchDashboard();
  } catch (e) {
    alert("Error saving treatment");
  }
};

const viewHistory = (patientId) => {
  router.push(`/doctor/patient/${patientId}/history`);
};

onMounted(fetchDashboard);
</script>
