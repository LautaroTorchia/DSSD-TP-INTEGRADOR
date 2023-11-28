<template>
  <div v-if="!loading">
    <div>
      <h1>Renegociar {{ collection.name }} </h1>
      <form @submit.prevent="renegotiate">
        <div class="mb-3">
          <label for="newReleaseDate" class="form-label">Nueva Fecha de Lanzamiento:</label>
          <input type="date" id="newReleaseDate" v-model="newReleaseDate" class="form-control" required 
          :min="collection.estimated_launch_date"/>
        </div>
      <div class="d-flex justify-content-between mt-4">
        <button @click="renegotiate" class="btn btn-primary">Renegociar</button>
        <button @click="cancelCollection" class="btn btn-danger">Cancelar colección</button>
      </div>
      </form>
    </div>
  </div>
  <div v-else class="spinner-border spinner-border-sm"></div>
  </template>
  
<script setup>

  import { ref, onMounted,computed } from 'vue'
  import { router, setBonitaVariable,fetchWrapper, advanceNamedBonitaTask,getBonitaVariable } from '@/helpers';
  import { storeToRefs } from 'pinia'
  import { useCollectionsStore } from '@/stores'
  
  const newReleaseDate = ref('')
  const collectionId = router.currentRoute.value.params.collection;
  const caseId = ref('')
  const collectionStore = useCollectionsStore()
  const collection = ref({}) // Move inside setup
  const { collections } = storeToRefs(collectionStore)
  const deliveryOrders = ref([])
  const baseUrl = `${import.meta.env.VITE_API_URL}`
  const loading = ref(true)
  
  const renegotiate = async () => {
    loading.value = true
    try {
      const collectionIdAsInt = parseInt(collectionId, 10)
      // set bonita variables
      await setBonitaVariable(caseId.value, 'se_renegocio', "true")
      await advanceNamedBonitaTask(caseId.value, 'Renegociar')
      
      //set new collection release date
      await fetchWrapper.patch(`${baseUrl}/coleccion/${collectionId}/`, {
        fecha_lanzamiento_estimada: newReleaseDate.value,
      })

      //delete old delivery orders
      deliveryOrders.value = await fetchWrapper.get(`${baseUrl}/entregas/ordenes/`)
      deliveryOrders.value.map( async (order) => await fetchWrapper.delete(`${baseUrl}/entregas/ordenes/${order.id}/`))

      // get delivered material reservations
      const deliveredMaterialReservations = await fetchWrapper.get(`${baseUrl}/reservas/material-entregado/`)

      // get all material reservations for the collection
      const totalMaterialReservations = await fetchWrapper.get(`${baseUrl}/reservas/reservas-materiales/`)
      console.log(totalMaterialReservations)
      const allMaterialReservations = totalMaterialReservations.filter(reservation =>
        reservation.coleccion === collectionIdAsInt
      )

      
      // filter out material reservations that were not delivered
      const materialReservationsToDelete = allMaterialReservations.filter(reservation =>
        !deliveredMaterialReservations.some(deliveredReservation => deliveredReservation.id_reserva === reservation.id)
      )

      // delete material reservations that were not delivered
      await Promise.all(materialReservationsToDelete.map(reservation =>
        fetchWrapper.delete(`${baseUrl}/reservas/reservas-materiales/${reservation.id}/`)
      ))
    
      // delete old lugar fabricacion reservations
      const lugarFabricacionReservations = await fetchWrapper.get(`${baseUrl}/reservas/reservas-lugares-fabricacion/`)
      console.log(lugarFabricacionReservations)

      const lugarFabricacionReservationsToDelete = lugarFabricacionReservations.filter(reservation =>
        reservation.coleccion === collectionIdAsInt
      )


      await Promise.all(lugarFabricacionReservationsToDelete.map(reservation =>
        fetchWrapper.delete(`${baseUrl}/reservas/reservas-lugares-fabricacion/${reservation.id}/`)
      ))

      //now modify cantidad_materiales variable
      const materialReservationsToUpdate = allMaterialReservations.filter(reservation =>
        deliveredMaterialReservations.some(deliveredReservation => deliveredReservation.id_reserva === reservation.id)
      )


      console.log("materiales_entregados: ",materialReservationsToUpdate)

      const cantidadMateriales = await getBonitaVariable(caseId.value, 'cantidad_materiales')
      console.log(cantidadMateriales)
      const materialsArray = JSON.parse(cantidadMateriales)

      for (let i = 0; i < materialsArray.length; i++) {
        const material = materialsArray[i];
        const deliveredReservations = materialReservationsToUpdate.filter(
          (reservation) => reservation.nombre_material === material.name
        );
        deliveredReservations.forEach((deliveredReservation) => {
          material.amount -= deliveredReservation.cantidad_pactada;
          // If the amount reaches 0, remove the element from the array
          if (material.amount <= 0) {
            materialsArray.splice(i, 1); // Use the current index (i) to remove the element
          }
        });
      }
      await setBonitaVariable(caseId.value, "plan_de_fabricacion", "")
      await setBonitaVariable(caseId.value, 'cantidad_materiales',materialsArray)
      router.push('/')
    } catch (error) {
      console.error(error)
    }
  };

  const cancelCollection = async () => {
    try {

      //delete collection
      await fetchWrapper.delete(`${baseUrl}/coleccion/${collectionId}/`)

      // set bonita variables
      await setBonitaVariable(caseId.value, 'se_renegocio', "false")
      await advanceNamedBonitaTask(caseId.value, 'Renegociar')

      router.push('/')
    } catch (error) {
      console.error(error)
    }
  };
  
  onMounted(async () => {
    await collectionStore.getAll()
    const collectionIdAsInt = parseInt(collectionId, 10)
    collection.value=collections.value.find((collection) => collection.id === collectionIdAsInt)
    caseId.value = collections.value.find((collection) => collection.id === collectionIdAsInt).caseId
    })
    loading.value = false
</script>
  