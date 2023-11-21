<template>
    <div class="fabrication-control container mt-4">
      <h1 class="mb-4">Fabrication Control for Collection {{ collectionId }}</h1>
      <div v-if="isFabricated" class="alert alert-success">
        <p>The collection has been fabricated successfully.</p>
      </div>
      <div v-else>
        <p>The collection is not yet fabricated.</p>
        <div v-if="fabricationReservations.length > 0" class="mt-4">
          <h2>Fabrication Reservations:</h2>
          <div class="row">
            <div v-for="reservation in filteredFabrications" :key="reservation.id" class="col-md-6 mb-3">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">Reservation ID: {{ reservation.id }}</h5>
                  <p class="card-text">
                    Fabrication Location: {{ reservation.lugar_de_fabricacion }}
                  </p>
                  <p class="card-text">
                    Start Date: {{ reservation.fecha_inicio_reserva }}
                  </p>
                  <p class="card-text">
                    End Date: {{ reservation.fecha_fin_reserva }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-for="reservation in filteredFabrications" :key="reservation.id" class="col-md-6 mb-3">
            <div class="mt-4">
            <button
                class="btn btn-success me-2"
                @click="markAsFabricated(reservation)"
                :disabled="isFabricated"
            >
                Mark as Fabricated
            </button>
            <button
                class="btn btn-primary"
                @click="renegotiate"
                :disabled="isFabricated"
            >
                Renegotiate
            </button>
            </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { router,fetchWrapper,setBonitaVariable,advanceNamedBonitaTask,getBonitaVariable } from '@/helpers';
  import { storeToRefs } from 'pinia'
  import { useCollectionsStore } from '@/stores'
  
  const collectionId = router.currentRoute.value.params.collection;
  const fabricationReservations = ref([]);
  const filteredFabrications = ref([]);
  const collectionStore = useCollectionsStore()
  const { collections } = storeToRefs(collectionStore)
  const caseId=ref("")
  const lotQuantity = ref(1);
  const baseUrl = `${import.meta.env.VITE_API_URL}`
  
  const fetchFabricationReservations = async () => {
    try {
      const response = await fetchWrapper.get(`${import.meta.env.VITE_API_URL}/reservas/reservas-lugares-fabricacion/`);
      fabricationReservations.value = response;
      filterFabricationReservations();
    } catch (error) {
      console.error(error);
    }
  };
  
  const filterFabricationReservations = () => {
    const collectionIdAsInt = parseInt(collectionId, 10); 
    filteredFabrications.value = fabricationReservations.value.filter(reservation => reservation.coleccion === collectionIdAsInt);
  };
  
  const markAsFabricated = async (reservation) => {
    try {
        const confirmed = window.confirm('Are you sure you want to mark this material as delivered?');
        if (confirmed) {
            const plan_fabricacion=await getBonitaVariable(caseId.value, 'plan_de_fabricacion')
            const deliveryDate = new Date().toISOString(); // Current date
            console.log(reservation)
            const data = {
                fecha_fabricado: deliveryDate,
                lugar: reservation.lugar_de_fabricacion,
                coleccion: collectionId,
            };
            lotQuantity.value = Number(JSON.parse(plan_fabricacion).lotQuantity)
            console.log(lotQuantity.value)
            for (let i = 0; i < lotQuantity.value; i++) {
                const response = await fetchWrapper.post(`${baseUrl}/entregas/lotes-fabricados/`, data);
                console.log(response)
            }
           
            await setBonitaVariable(caseId.value,"retraso_fabricacion","false")
            await advanceNamedBonitaTask(caseId.value,"Controlar fabricación")
            router.push("/")
            reservation.markAsFabricated = true;
        }
    } catch (error) {
      console.error(error);
    }
  };
  
  const renegotiate = () => {
    // Implement the logic to navigate to the renegotiate view
    // You can use router.push or router.replace to navigate to the desired route
    console.log('Navigating to renegotiate view...');
  };
  
  const isFabricated = ref(false); // Set this based on your backend logic
  
  onMounted(async () => {
    await collectionStore.getAll()
    const collectionIdAsInt = parseInt(collectionId, 10);
    caseId.value = collections.value.find((collection) => collection.id === collectionIdAsInt).caseId
    fetchFabricationReservations();
  });
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
  </style>
  