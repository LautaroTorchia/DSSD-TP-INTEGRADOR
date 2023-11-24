<template>
    <div>
      <h1>Renegociar {{ collection.name }} </h1>
      <form @submit.prevent="renegotiate">
        <div class="mb-3">
          <label for="newReleaseDate" class="form-label">Nueva Fecha de Lanzamiento:</label>
          <input type="date" id="newReleaseDate" v-model="newReleaseDate" class="form-control" required />
        </div>
      <div class="d-flex justify-content-between mt-4">
        <button @click="renegotiate()" type="submit" class="btn btn-primary">Renegociar</button>
        <button @click="cancelCollection()" type="submit" class="btn btn-danger">Cancelar coleccion</button>
      </div>
      </form>
    </div>
  </template>
  
<script setup>

  import { ref, onMounted,computed } from 'vue'
  import { router, setBonitaVariable,fetchWrapper, advanceNamedBonitaTask } from '@/helpers';
  import { storeToRefs } from 'pinia'
  import { useCollectionsStore } from '@/stores'
  
  const newReleaseDate = ref('');
  const collectionId = router.currentRoute.value.params.collection;
  const caseId = ref('');
  const collectionStore = useCollectionsStore()
  const collection = ref({}); // Move inside setup
  const { collections } = storeToRefs(collectionStore)
  const deliveryOrders = ref([]);
  const baseUrl = `${import.meta.env.VITE_API_URL}`
  
  const renegotiate = async () => {
    try {
      // set bonita variables
      await setBonitaVariable(caseId.value, 'se_renegocio', "true");
      await advanceNamedBonitaTask(caseId.value, 'Renegociar');
      
      //set new collection release date
      await fetchWrapper.patch(`${baseUrl}/coleccion/${collectionId}/`, {
        fecha_lanzamiento_estimada: newReleaseDate.value,
      });

      //delete old delivery orders
      deliveryOrders.value = await fetchWrapper.get(`${baseUrl}/entregas/ordenes/`)
      deliveryOrders.value.map( async (order) => await fetchWrapper.delete(`${baseUrl}/entregas/ordenes/${order.id}/`))

      router.push('/');
    } catch (error) {
      console.error(error);
    }
  };

  const cancelCollection = async () => {
    try {

      //delete old delivery orders
      deliveryOrders.value = await fetchWrapper.get(`${baseUrl}/entregas/ordenes/`)
      deliveryOrders.value.map( async (order) => await fetchWrapper.delete(`${baseUrl}/entregas/ordenes/${order.id}/`))
      
      //delete collection
      await fetchWrapper.delete(`${baseUrl}/coleccion/${collectionId}/`)

      // set bonita variables
      await setBonitaVariable(caseId.value, 'se_renegocio', "false");
      await advanceNamedBonitaTask(caseId.value, 'Renegociar');

      router.push('/');
    } catch (error) {
      console.error(error);
    }
  };
  
  onMounted(async () => {
    await collectionStore.getAll()
    const collectionIdAsInt = parseInt(collectionId, 10)
    collection.value=collections.value.find((collection) => collection.id === collectionIdAsInt)
    caseId.value = collections.value.find((collection) => collection.id === collectionIdAsInt).caseId
    })
</script>
  