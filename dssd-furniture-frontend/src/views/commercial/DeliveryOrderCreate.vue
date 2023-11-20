<template>
  <div class="text-center">
    <h1>Delivery Order Create</h1>
    <div v-if="lotQuantity">
      <h2>Ordenes de entrega sin asignar: {{ lotQuantity }}</h2>
      <div class="mx-auto" style="max-width: 500px;"> <!-- Adjust max-width as needed -->
        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <label class="input-group-text" for="distributorDropdown">Distribuidor</label>
          </div>
          <select v-model="selectedLocation" class="custom-select" id="distributorDropdown">
            <option v-for="distributor in distributors" :key="distributor.id" :value="distributor.id">{{ distributor.nombre }}</option>
          </select>
        </div>
        <div class="input-group mb-3">
          <label class="input-group-text" for="quantityInput">Cantidad</label>
          <input
            type="number"
            id="quantityInput"
            class="form-control"
            v-model="quantity"
            :min="1"
            :max="lotQuantity"
            @input="handleInput"
          >
        </div>
        <div class="d-flex justify-content-end"> <!-- Align buttons to the right -->
          <button class="btn btn-primary mt-2 mr-2" @click="assignOrders">Asignar</button>
          <button class="btn btn-danger mt-2" @click="cancel">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getBonitaVariable, fetchWrapper } from '@/helpers';
import { useCollectionsStore } from '@/stores'
import { storeToRefs } from 'pinia'
import { router } from '@/helpers'

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)

const distributors = ref([])
const baseUrl = `${import.meta.env.VITE_API_URL}`
const collectionId = router.currentRoute.value.params.collection
const lotQuantity = ref(0)
const quantity = ref(1) // Initialize quantity with a default value
const selectedLocation = ref(null); // Selected location from the dropdown
const locations = ref([]); // Assuming you have an array of locations

const handleInput = () => {
  // Ensure the entered value is within the specified range
  if (quantity.value < 1) {
    quantity.value = 1;
  } else if (quantity.value > lotQuantity.value) {
    quantity.value = lotQuantity.value;
  }
};

const assignOrders = () => {
  // Your logic to handle the assignment of orders based on the entered quantity and selected location
  // This could involve making API calls or updating some state in your application
  console.log('Assigning orders:', quantity.value, 'to location:', selectedLocation.value);
};

const cancel = () => {
  // Redirect to the previous page
  router.go(-1);
};

onMounted(async () => {
  let caseId
  try {
    caseId = JSON.parse(localStorage.getItem('collections')).collections.find((collection) => collection.id == collectionId).caseId
  } catch (error) {
    await collectionStore.getAll()
    caseId = collections.value.find((collection) => collection.id == collectionId).caseId
  }
  lotQuantity.value = Number(JSON.parse(await getBonitaVariable(caseId, 'plan_de_fabricacion')).lotQuantity)

  const response = await fetchWrapper.get(`${baseUrl}/entregas/vendedores-finales/`)
  distributors.value = response

});
</script>

