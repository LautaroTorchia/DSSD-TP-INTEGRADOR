<template>
    <div v-if="loading">
      <div class="spinner-border text-primary" role="status">
      </div>
  </div>
  <div v-else class="fabrication-control container mt-4">
    <h1 class="mb-4">Control de Fabricación para la Colección {{ collectionId }}</h1>

    <div v-if="isFabricated" class="alert alert-success">
      <p>La colección se ha fabricado con éxito.</p>
    </div>

    <div v-else>
      <div class="d-flex flex-wrap justify-content-between mb-4">
        <div class="card collection-card">
          <div class="card-body">
            <h5 class="card-title">Detalles de la Colección</h5>
            <p class="card-text"><strong>Nombre de la Colección:</strong> {{ collection.name }}</p>
            <p class="card-text"><strong>Descripción:</strong> {{ collection.description }}</p>
            <p class="card-text"><strong>Diseñada:</strong> {{ collection.designed ? 'Sí' : 'No' }}</p>
            <p class="card-text"><strong>Fabricada:</strong> {{ collection.fabricated ? 'Sí' : 'No' }}</p>
            <p class="card-text"><strong>Fecha Estimada de Lanzamiento:</strong> {{ collection.estimated_launch_date }}</p>
          </div>
        </div>
      </div>

      <p class="not-fabricated-text"><strong>La colección aún no ha sido fabricada.</strong></p>

      <div class="card reservation-card" v-if="fabricationReservations.length > 0">
          <div class="card-body">
            <h5 class="card-title">Reservas de Fabricación</h5>
        <div class="row">
          <div v-for="reservation in filteredFabrications" :key="reservation.id" class="col-md-6 mb-3">
              <div class="card-body">
                <h5 class="card-title">ID de Reserva: {{ reservation.id }}</h5>
                <p class="card-text"><strong>Ubicación de Fabricación:</strong> {{ reservation.lugar_de_fabricacion_nombre }}</p>
                <p class="card-text"><strong>Fecha de Inicio:</strong> {{ reservation.fecha_inicio_reserva }}</p>
                <p class="card-text"><strong>Fecha de Fin:</strong> {{ reservation.fecha_fin_reserva }}</p>

            </div>
          </div>
        </div>
      </div>
    </div>
      <!-- Error Message -->
      <div v-if="errorMessage" class="alert alert-danger mt-3">
            {{ errorMessage }}
      </div>
      <div class="mt-4">
        <button
          class="btn btn-success me-2"
          @click="markAsFabricated(filteredFabrications[0])"
        >
          Marcar como Fabricada
        </button>
          <button class="btn btn-primary me-2"
          @click="renegociate()"
          >
          Renegociar
        </button>
      </div>
    </div>
  </div>
</template>

  
<script setup>
  import { ref, onMounted,computed } from 'vue'
  import { router,fetchWrapper,setBonitaVariable,advanceNamedBonitaTask,getBonitaVariable,getBonitaTask } from '@/helpers'
  import { storeToRefs } from 'pinia'
  import { useCollectionsStore } from '@/stores'
  
  const collectionId = router.currentRoute.value.params.collection
  const collectionStore = useCollectionsStore()
  const { collections } = storeToRefs(collectionStore)
  const fabricationReservations = ref([])
  const filteredFabrications = ref([])
  const collection = ref({})
  const caseId=ref("")
  const lotQuantity = ref(1)
  const loading = ref(true)
  const baseUrl = `${import.meta.env.VITE_API_URL}`
  const proveedoresUrl = `${import.meta.env.VITE_API_PROVEEDORES_URL}`
  const errorMessage = ref('')

  const fetchFabricationReservations = async () => {
    try {
      const response = await fetchWrapper.get(`${import.meta.env.VITE_API_URL}/reservas/reservas-lugares-fabricacion/`)
      fabricationReservations.value = response
      await filterFabricationReservations(fabricationReservations.value)
    } catch (error) {
      console.error(error)
    }
  }
  
  const filterFabricationReservations = async (fabrications) => {
  const collectionIdAsInt = parseInt(collectionId, 10)
  filteredFabrications.value = fabrications.filter((reservation) => {
    return reservation.coleccion === collectionIdAsInt
  })
  filteredFabrications.value = filteredFabrications.value.filter( async (reservation) => {
    return await fetchFabricationLocation(reservation,reservation.lugar_de_fabricacion)
  })
}

const fetchFabricationLocation = async (reservation,fabricationLocationId) => {
  try {
    const response = await fetchWrapper.get(`${proveedoresUrl}/proveedores/lugar-fabricacion/${fabricationLocationId}/`)
    const fabricationLocation = response
    reservation.lugar_de_fabricacion_nombre = fabricationLocation.nombre 
    return true
  } catch (error) {
    console.error(error)
    return false
  }
}
  const renegociate = async ( ) => {
    const bonitaTasks = await getBonitaTask(caseId.value);
    const controlarMaterialesTaskExists = bonitaTasks.some(task => task.displayName === 'Controlar fabricación');

    if (!controlarMaterialesTaskExists) {
      errorMessage.value = 'Error: Todavía no ha pasado el tiempo estipulado para finalizar el control';
      return;
    }
    router.push({ name: 'yourRouteName' });
  }

  const markAsFabricated = async (reservation) => {
    try {
        const bonitaTasks = await getBonitaTask(caseId.value)
        const controlarMaterialesTaskExists = bonitaTasks.some(task => task.displayName === 'Controlar fabricación')
        
        if (!controlarMaterialesTaskExists) {
          errorMessage.value = 'Error: Todavia no ha pasado el tiempo estipulado para finalizar el control'
          return
        }
        const confirmed = window.confirm('Estas seguro que quieres confirmar a la coleccion como fabricada?')
        if (confirmed) {
            const plan_fabricacion=await getBonitaVariable(caseId.value, 'plan_de_fabricacion')
            const deliveryDate = new Date().toISOString().split('T')[0]
            
            const data = {
                fecha_fabricado: deliveryDate,
                lugar: reservation.lugar_de_fabricacion,
                coleccion: collectionId,
            }
            lotQuantity.value = Number(JSON.parse(plan_fabricacion).lotQuantity)
            
            for (let i = 0; i < lotQuantity.value; i++) {
                const response = await fetchWrapper.post(`${baseUrl}/entregas/lotes-fabricados/`, data)
                
            }
            await setBonitaVariable(caseId.value,"retraso_fabricacion","false")
            await advanceNamedBonitaTask(caseId.value,"Controlar fabricación")
            await fetchWrapper.patch(`${baseUrl}/coleccion/${collectionId}/`, { fabricada: true })

            router.push("/")
            reservation.markAsFabricated = true
        }
    } catch (error) {
      console.error(error)
    }
  }
  
  
  const isFabricated = ref(false)
  
  onMounted(async () => {
    await collectionStore.getAll()
    const collectionIdAsInt = parseInt(collectionId, 10)
    collection.value=collections.value.find((collection) => collection.id === collectionIdAsInt)
    caseId.value = collections.value.find((collection) => collection.id === collectionIdAsInt).caseId
    await fetchFabricationReservations()
    loading.value = false
  })
  
</script>
  
  <style scoped>
  .fabrication-control {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .alert-success {
    background-color: #d4edda;
    border-color: #c3e6cb;
    color: #155724;
  }
  
  .card {
    width: 100%;
  }
  .not-fabricated-text {
    font-weight: bold;
    color: #721c24; /* Dark red text color */
  }
  </style>
  