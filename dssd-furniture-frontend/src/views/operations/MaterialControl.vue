<template>
  <div v-if="loading">
      <div class="spinner-border text-primary" role="status">
      </div>
  </div>
  <div v-else>
    <h1>Control de materiales reservados de la colección {{ collectionId }}</h1>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Proveedor</th>
          <th>Material</th>
          <th>Cantidad Pactada</th>
          <th>Fecha Entrega Pactada</th>
          <th>Sede a Entregar</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reservation in filteredReservations" :key="reservation.id">
          <td>{{ reservation.id }}</td>
          <td>{{ reservation.nombre_proveedor }}</td>
          <td>{{ reservation.nombre_material }}</td>
          <td>{{ reservation.cantidad_pactada }}</td>
          <td>{{ reservation.fecha_entrega_pactada }}</td>
          <td>{{ reservation.sede_a_entregar }}</td>
          <td>
            <span v-if="reservation.markedAsDelivered">Entregado</span>
            <span v-else>
              <button @click="confirmMarkAsDelivered(reservation)" :disabled="reservation.markedAsDelivered">
                Marcar como Entregado
              </button>
            </span>
          </td>
        </tr>
      </tbody>
    </table>
    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-danger mt-3">
      {{ errorMessage }}
    </div>
    <div class="d-flex justify-content-between mt-4">
      <button class="btn btn-primary" @click="renegociate">
        Renegociar entregas
      </button>
      <button class="btn btn-success" @click="advanceToNextStep" :disabled="!allReservationsDelivered">
        Confirmar Entrega
      </button>
    </div>
  </div>
</template>
  
<script setup>
import { ref, onMounted,computed } from 'vue'
import { getBonitaTask,router,fetchWrapper,setBonitaVariable,advanceNamedBonitaTask } from '@/helpers'
import { storeToRefs } from 'pinia'
import { useCollectionsStore } from '@/stores'

const collectionId = router.currentRoute.value.params.collection
const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)

const reservations = ref([])
const caseId=ref("")
const filteredReservations = ref([])
const baseUrl = `${import.meta.env.VITE_API_URL}`
const loading = ref(true)
const errorMessage = ref('')


const allReservationsDelivered = computed(() => {
  return filteredReservations.value.every((reservation) => reservation.markedAsDelivered)
})

const fetchReservations = async () => {
  try {
    // Fetch reservations
    const responseReservations = await fetchWrapper.get(`${baseUrl}/reservas/reservas-materiales/`)
    reservations.value = responseReservations

    // Fetch already delivered materials
    const responseDelivered = await fetchWrapper.get(`${baseUrl}/reservas/material-entregado/`)

    // Update markedAsDelivered property based on delivered materials
    reservations.value.forEach((reservation) => {
      reservation.markedAsDelivered = responseDelivered.some(
        (delivered) => delivered.id_reserva === reservation.id
      )
    })

    filterReservations()
  } catch (error) {
    console.error(error)
  }
}

const filterReservations = () => {
    const collectionIdAsInt = parseInt(collectionId, 10) 
    filteredReservations.value=reservations.value.filter(reservation => reservation.coleccion === collectionIdAsInt)
}

const confirmMarkAsDelivered = async (reservation) => {
  try {
    const confirmed = window.confirm('Are you sure you want to mark this material as delivered?')

    if (confirmed) {
      const deliveryDate = new Date().toISOString().split('T')[0] // Current date
      const data = {
        dia_entregad: deliveryDate,
        id_reserva: reservation.id,
      }
      const response = await fetchWrapper.post(`${baseUrl}/reservas/material-entregado/`, data)
      reservation.markedAsDelivered = true
    }
  } catch (error) {
    console.error(error)
  }
}

const renegociate = async () => {
  try {
    const bonitaTasks = await getBonitaTask(caseId.value)
    const controlarMaterialesTaskExists = bonitaTasks.some(task => task.displayName === 'Controlar entrega de materiales')
    
    if (!controlarMaterialesTaskExists) {
      errorMessage.value = 'Error: Todavia no ha pasado el tiempo estipulado para finalizar el control'
      return
    }
    
    await setBonitaVariable(caseId.value, 'retraso_materiales', 'true')
    await advanceNamedBonitaTask(caseId.value, 'Controlar entrega de materiales')
    router.push('/')
  } catch (error) {
    console.error(error)
  }
}

const advanceToNextStep = async () => {
  try {
    const bonitaTasks = await getBonitaTask(caseId.value)
    const controlarMaterialesTaskExists = bonitaTasks.some(task => task.displayName === 'Controlar entrega de materiales')
    
    if (!controlarMaterialesTaskExists) {
      errorMessage.value = 'Error: Todavia no ha pasado el tiempo estipulado para finalizar el control'
      return
    }
    
    await setBonitaVariable(caseId.value, 'retraso_materiales', 'false')
    await advanceNamedBonitaTask(caseId.value, 'Controlar entrega de materiales')
    router.push('/')
  } catch (error) {
    console.error(error)
  }
}

onMounted(async () => {
    await collectionStore.getAll()
    const collectionIdAsInt = parseInt(collectionId, 10)
    caseId.value = collections.value.find((collection) => collection.id === collectionIdAsInt).caseId
    fetchReservations()
    loading.value = false
})
</script>
  