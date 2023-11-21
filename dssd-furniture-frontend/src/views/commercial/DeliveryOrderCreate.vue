<template>
  <h1>Delivery Order Create</h1>
  <div v-if="!loading">
    <h2>Ordenes de entrega sin asignar: {{ lotQuantity }}</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group" name="assignElement">
        <label for="distributorDropdown">Distribuidor:</label>
        <select v-model="selectedLocation" class="custom-select" id="distributorDropdown" required>
          <option v-for="distributor in distributors" :key="distributor.id" :value="distributor">{{ distributor.nombre
          }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="quantityInput">Cantidad:</label>
        <input type="number" id="quantityInput" class="form-control" v-model="quantity" :min="1" :max="lotQuantity"
          @input="handleInput" required>
      </div>
      <p class="text-danger" >{{ amountError }}</p>
      <div class="form-group">
        <label for="delivery-date">Fecha de entrega:</label>
        <input type="date" id="delivery-date" class="form-control" v-model="deliveryDate" :min="end_date" required/>
        <div class="text-danger" ref="deliveryDateError"></div>
      </div>
      <div class="d-flex justify-content-end">
        <button type="submit" class="btn btn-primary mt-2 mr-2" @click="assignOrders"
          v-if="totalQuantity < lotQuantity">
          Asignar
        </button>
        <p v-else>Cantidad de lotes máxima alcanzada</p>
        <router-link :to="{ name: 'delivery-order-collection-list' }" class="btn btn-danger mt-2">Cancelar</router-link>
      </div>
    </form>
    <button type="submit" class="btn btn-primary mt-2 mr-2" @click="finishAssignment">Confirmar</button>
    <div>
      <h3>Asignaciones:</h3>
      <div class="d-flex flex-column justify-content-between" style="width: 7cm;" >
        <div v-for="assignment in assignmentList" :key="assignment.location" class="badge badge-primary font-weight-bold">
          <p>{{ 'Punto de venta: ' + assignment.assignmentTag.location }}</p>
          <p>{{ 'Cantidad de lotes: ' + assignment.lotsAmount }}</p>
          <p>{{ 'Fecha de entrega: ' + assignment.assignmentTag.formattedDate }}</p>
          <button class="btn btn-danger btn-sm" @click="removeAssignment(assignment)">X</button>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="loading" class="spinner-border spinner-border-sm"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBonitaVariable, fetchWrapper, router } from '@/helpers'
import { useCollectionsStore } from '@/stores'
import { storeToRefs } from 'pinia'

const collectionId = router.currentRoute.value.params.collection
const baseUrl = `${import.meta.env.VITE_API_URL}`
const loading = ref(true)

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const distributors = ref([])
const lotQuantity = ref(0)

const quantity = ref(1)
const totalQuantity = ref(0)
const selectedLocation = ref(null)
const assignmentList = ref([])
const amountError = ref('')
const end_date = ref('')
const deliveryDate = ref('')

onMounted(async () => {
  const plan = await getPlan()
  lotQuantity.value = Number(plan.lotQuantity)
  end_date.value = plan.factory_slot.slot_end_date
  distributors.value = await fetchWrapper.get(`${baseUrl}/entregas/vendedores-finales/`)
  loading.value = false
})

const finishAssignment = () => {
  if (lotQuantity.value !== totalQuantity.value) {
    alert('Debe asignar todos los lotes disponibles')
    return
  }
  assignmentList.value.forEach(async (assignment) => {
    const body = {
      descripcion: 'Entrega de orden de entrega creada el' + new Date().toISOString().split('T')[0] + ' para la colección ',
      fecha_entrega: assignment.deliveryDate,
      se_entrego: false,
      id_coleccion: collectionId,
      vendedor_final: assignment.location,
    }
    console.log(body)
    await fetchWrapper.post(`${baseUrl}/entregas/ordenes/`, body)
  })
  router.push({ name: 'delivery-order-collection-list' })
}

const handleInput = () => {
  if (quantity.value < 0) {
    quantity.value = 0
  } else if (quantity.value > lotQuantity.value) {
    quantity.value = lotQuantity.value
  }
  if (totalQuantity.value + quantity.value > lotQuantity.value) {
    quantity.value = lotQuantity.value - totalQuantity.value
  } else {
    amountError.value = ''
  }
}

const assignOrders = () => {
  if (quantity.value === 0) {
    alert('Debe ingresar una cantidad válida')
    return
  }
  if (!selectedLocation.value) {
    alert('Debe seleccionar un distribuidor')
    return
  }
  if (totalQuantity.value + quantity.value > lotQuantity.value) {
    amountError.value = "La cantidad de lotes asignados no puede superar la cantidad de lotes disponibles"
    return
  }
  const assignment = {
    location: selectedLocation.value.id,
    lotsAmount: quantity.value,
    deliveryDate: deliveryDate.value,
    assignmentTag: {
      location: selectedLocation.value.nombre,
      formattedDate: new Date(deliveryDate.value).toLocaleString('en-US', { timeZone: 'America/Argentina/Buenos_Aires' }).split(',')[0]
    }
  }
  assignmentList.value.push(assignment)
  totalQuantity.value += quantity.value
}

const removeAssignment = (assignment) => {
  const index = assignmentList.value.indexOf(assignment)
  assignmentList.value.splice(index, 1)
  totalQuantity.value -= assignment.lotsAmount
}

const getPlan = async () => {
  let caseId
  try {
    caseId = JSON.parse(localStorage.getItem('collections')).collections.find((collection) => collection.id == collectionId).caseId
  } catch (error) {
    await collectionStore.getAll()
    caseId = collections.value.find((collection) => collection.id == collectionId).caseId
  }
  let plan = await getBonitaVariable(caseId, 'plan_de_fabricacion')
  plan = JSON.parse(plan)
  return plan
}
</script>
