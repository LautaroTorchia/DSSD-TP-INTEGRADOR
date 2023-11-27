<template>
  <h2>Colecciones diseñadas:</h2>
  <div v-if="!loading">
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">Nombre</th>
          <th scope="col">Descripción</th>
          <th scope="col">Fecha de lanzamiento estimada</th>
          <th scope="col">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <template v-if="!loading">
          <template v-for="(collection, index) in orderedCollections" :key="collection.id">
            <tr :style="{ 'background-color': index % 2 === 0 ? '#fff' : '#f8f9fa' }">
              <td><strong>{{ collection.name }}</strong></td>
              <td>{{ collection.description }}</td>
              <td>{{ collection.estimated_launch_date }}</td>
              <td>
                <div v-if="collection.cantidadMateriales">
                  <div v-if="collection.planDeFabricacion">
                    <div v-if="collection.orders_placed">
                      <router-link
                        :to="{ name: 'material-control-list', params: { collection: collection.id } }">Controlar
                        entrega de materiales</router-link>
                    </div>
                    <div v-else-if="!collection.loading">
                      <router-link
                        :to="{ name: 'fabrication-plan-confirm', params: { collection: collection.id } }">Confirmar
                        plan de fabricación</router-link>
                    </div>
                  </div>
                  <div v-else-if="!collection.loading"><router-link
                      :to="{ name: 'fabrication-plan', params: { collection: collection.id } }">Armar plan de
                      fabricación</router-link></div>
                </div>
                <div v-else-if="!collection.loading"><router-link
                    :to="{ name: 'material-analysis', params: { collection: collection.id } }">Analizar
                    materiales</router-link></div>
              </td>
            </tr>
          </template>
        </template>
        <tr v-else>
          <td colspan="4" class="text-center">
            <div v-if="collections.loading" class="spinner-border spinner-border-sm"></div>
            <div v-else-if="collections.error" class="text-danger mt-3">Error loading collections: {{ collections.error }}
            </div>
            <div v-else>No hay nada</div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else class="spinner-border spinner-border-sm"></div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useCollectionsStore } from '@/stores'
import { getBonitaVariable, fetchWrapper } from '@/helpers';
import { onBeforeMount, ref } from 'vue';
const baseUrl = `${import.meta.env.VITE_API_URL}`

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const loading = ref(true)
const designedCollections = ref([])
const orderedCollections = ref([])

onBeforeMount(async () => {
  await collectionStore.getAll()
  const ordersPlaced = await fetchWrapper.get(`${baseUrl}/reservas/reservas-lugares-fabricacion/`)
  designedCollections.value = collections.value.filter((collection) => collection.designed && !collection.fabricated)
  for (const collection of designedCollections.value) {
    collection.loading = true;
    try {
      const materialAmount = await getBonitaVariable(collection.caseId, 'cantidad_materiales')
      collection.cantidadMateriales = !!materialAmount;
      if (collection.cantidadMateriales) {
        const fabricationPlan = await getBonitaVariable(collection.caseId, "plan_de_fabricacion")
        console.log(fabricationPlan)
        if (fabricationPlan === "") {
          collection.planDeFabricacion = false;
        }
        collection.planDeFabricacion = !!fabricationPlan;
      }
      console.log(collection.planDeFabricacion)
      if (collection.planDeFabricacion) {
        collection.orders_placed = !!(ordersPlaced.find((order) => order.coleccion == collection.id))
      }
    } catch (error) {
      console.error(error)
    }
    collection.loading = false;
  }
  orderedCollections.value = designedCollections.value.slice().sort((a, b) => {
    const dateA = new Date(a.fecha_creacion)
    const dateB = new Date(b.fecha_creacion)
    return dateA - dateB;
  })

  loading.value = false
})


</script>
