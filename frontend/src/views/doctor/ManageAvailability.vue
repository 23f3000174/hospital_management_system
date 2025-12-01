<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <h3 class="mb-4">Manage Availability</h3>
      <div class="row">
        <div class="col-md-5">
          <div class="card shadow-sm">
            <div class="card-header bg-primary text-white">Add Weekly Schedule</div>
            <div class="card-body">
              <form @submit.prevent="addBulkSlots">
                <div class="mb-3">
                  <label class="fw-bold d-block mb-2">Repeat On:</label>
                  <div class="d-flex flex-wrap gap-2">
                    <div v-for="day in allDays" :key="day" class="form-check form-check-inline">
                      <input class="form-check-input" type="checkbox" :value="day" v-model="selectedDays" :id="'check-'+day">
                      <label class="form-check-label" :for="'check-'+day">{{ day.substring(0,3) }}</label>
                    </div>
                  </div>
                </div>
                <div class="row g-2">
                  <div class="col-6"><label class="fw-bold">Start</label><input v-model="form.start_time" type="time" class="form-control" required></div>
                  <div class="col-6"><label class="fw-bold">End</label><input v-model="form.end_time" type="time" class="form-control" required></div>
                </div>
                <div v-if="msg" :class="`alert alert-${type} mt-3`">{{ msg }}</div>
                <button class="btn btn-primary w-100 mt-2" :disabled="loading || selectedDays.length === 0">{{ loading ? 'Generating...' : 'Add Schedule' }}</button>
              </form>
            </div>
          </div>
        </div>
        <div class="col-md-7">
          <div class="card shadow-sm">
            <div class="card-body p-0" style="max-height: 550px; overflow-y: auto;">
              <table class="table table-hover mb-0">
                <thead class="table-light sticky-top"><tr><th>Date</th><th>Day</th><th>Time</th><th>Action</th></tr></thead>
                <tbody>
                  <tr v-for="slot in slots" :key="slot.id">
                    <td>{{ formatDate(slot.date) }}</td>
                    <td>{{ slot.day }}</td>
                    <td>{{ formatTime(slot.start_time) }} - {{ formatTime(slot.end_time) }}</td>
                    <td><button @click="deleteSlot(slot.id)" class="btn btn-danger btn-sm py-0 px-2">&times;</button></td>
                  </tr>
                </tbody>
              </table>
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

const slots = ref([]);
const allDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const selectedDays = ref([]); 
const form = ref({ start_time: '09:00', end_time: '17:00' });
const msg = ref(''); const type = ref(''); const loading = ref(false);

const fetchSlots = async () => { try { const res = await api.get('/doctor/availability'); slots.value = res.data; } catch (e) {} };

const addBulkSlots = async () => {
  loading.value = true;
  try {
    const res = await api.post('/doctor/availability', { days: selectedDays.value, start_time: form.value.start_time, end_time: form.value.end_time });
    msg.value = res.data.message; type.value = 'success'; fetchSlots();
  } catch (e) { msg.value = "Error adding slots"; type.value = 'danger'; } 
  finally { loading.value = false; }
};

const deleteSlot = async (id) => { if(!confirm("Remove?")) return; await api.delete(`/doctor/availability/${id}`); fetchSlots(); };
const formatDate = (d) => new Date(d).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
const formatTime = (t) => { const [h, m] = t.split(':'); const d = new Date(); d.setHours(h, m); return d.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }); };

onMounted(fetchSlots);
</script>