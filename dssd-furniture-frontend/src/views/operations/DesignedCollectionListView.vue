<script setup>
import { storeToRefs } from 'pinia'
import { useCollectionsStore } from '@/stores'
import { getBonitaVariable, fetchWrapper } from '@/helpers';
import { onBeforeMount, ref } from 'vue';
const collectionStore = useCollectionsStore()
const baseUrl = `${import.meta.env.VITE_API_URL}`

const { collections } = storeToRefs(collectionStore)
const loading = ref(true)
const designedCollections = ref([])



async function getCantidadMateriales(caseId) {
    return await getBonitaVariable(caseId, "cantidad_materiales")
}

async function getPlanDeFabricacion(caseId) {
    return await getBonitaVariable(caseId, "plan_de_fabricacion")
}

onBeforeMount(async () => {
    await collectionStore.getAll()
    designedCollections.value = collections.value.filter((collection) => collection.designed)
    const ordersPlaced = await fetchWrapper.get(`${baseUrl}/reservas/reservas-lugares-fabricacion/`)
    designedCollections.value.forEach(async (collection) => {
        collection.loading = true
        try {
            const materialAmount = await getCantidadMateriales(collection.caseId)
            collection.cantidadMateriales = !!materialAmount
            if (collection.cantidadMateriales) {
                const fabricationPlan = await getPlanDeFabricacion(collection.caseId)
                collection.planDeFabricacion = !!fabricationPlan
            }
            if (collection.planDeFabricacion) {
                collection.orders_placed = !!(ordersPlaced.find((order) => order.coleccion == collection.id))
            }
        } catch (error) { }
        collection.loading = false
    })
    loading.value = false
})


</script>

<template>
    <div>
        <ul v-if="!loading">
            <div v-for="collection in designedCollections" :key="collection.id">
                <span v-if="collection.designed">
                    <li>Nombre: {{ collection.name }} </li>
                    <li>Descripción: {{ collection.description }}</li>

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

                </span>
            </div>
        </ul>
        <div v-else-if="collections.loading || loading" class="spinner-border spinner-border-sm"></div>
        <div v-else-if="collections.error" class="text-danger">Error loading collections: {{ collections.error }}</div>
        <div v-else>No hay nada</div>
    </div>
</template>