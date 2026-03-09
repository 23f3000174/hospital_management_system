<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <h3>Book Appointment</h3>
      
      <!-- Search Filters -->
      <div class="row mb-4 g-2">
        <div class="col-md-5">
          <input v-model="query" class="form-control" placeholder="Search Doctor Name...">
        </div>
        <div class="col-md-5">
          <select v-model="deptFilter" class="form-select">
            <option value="">All Departments</option>
            <option v-for="d in departments" :key="d.id" :value="d.name">{{ d.name }}</option>
          </select>
        </div>
        <div class="col-md-2">
          <button @click="searchDocs" class="btn btn-primary w-100">Search</button>
        </div>
      </div>

      <!-- Doctor List -->
      <div class="row g-4">
        <div class="col-md-4" v-for="doc in doctors" :key="doc.id">
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <h5 class="fw-bold">{{ doc.name }}</h5>
              <span class="badge bg-info text-dark mb-2">{{ doc.department }}</span>
              <button @click="viewSlots(doc)" class="btn btn-outline-primary w-100 mt-3">View Availability</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Booking Modal -->
    <div v-if="showModal" class="modal d-block" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Book with {{ selectedDoc.name }}</h5>
            <button @click="showModal = false" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <div v-if="slots.length === 0" class="text-center p-3 text-muted">No slots available.</div>
            <div v-else class="list-group">
              <button 
                v-for="(slot, i) in slots" :key="i"
                @click="bookSlot(slot)"
                class="list-group-item list-group-item-action d-flex justify-content-between">
                <span>{{ slot.date }}</span>
                <span class="fw-bold">{{ slot.start_time }} - {{ slot.end_time }}</span>
              </button>
            </div>
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

const query = ref('');
const deptFilter = ref('');
const doctors = ref([]);
const departments = ref([]);
const router = useRouter();

// Modal State
const showModal = ref(false);
const selectedDoc = ref(null);
const slots = ref([]);

onMounted(async () => {
  const dRes = await api.get('/public/departments');
  departments.value = dRes.data;
  searchDocs();
});

const searchDocs = async () => {
  const res = await api.get(`/patient/search?q=${query.value}&dept=${deptFilter.value}`);
  doctors.value = res.data;
};

const viewSlots = async (doc) => {
  selectedDoc.value = doc;
  const res = await api.get(`/patient/availability/${doc.id}`);
  slots.value = res.data;
  showModal.value = true;
};

const bookSlot = async (slot) => {
  if(!confirm(`Confirm booking on ${slot.date} at ${slot.start_time}?`)) return;
  try {
    await api.post('/patient/book', {
      doctor_id: selectedDoc.value.id,
      date: slot.date,
      start_time: slot.start_time
    });
    alert("Booking Confirmed!");
    showModal.value = false;
    router.push('/patient/appointments');
  } catch(e) { alert(e.response?.data?.message || "Error"); }
};
</script>