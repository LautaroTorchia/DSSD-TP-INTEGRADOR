<script setup>
import { storeToRefs } from 'pinia'
import { useCollectionsStore } from '@/stores'
import { getBonitaVariable, fetchWrapper } from '@/helpers';
import { onMounted, onBeforeMount, ref } from 'vue';
const collectionStore = useCollectionsStore()
const baseUrl = `${import.meta.env.VITE_API_URL}`

const { collections } = storeToRefs(collectionStore)
const loading = ref(true)



async function getCantidadMateriales(caseId) {
    return await getBonitaVariable(caseId, "cantidad_materiales")
}

async function getPlanDeFabricacion(caseId) {
    return await getBonitaVariable(caseId, "plan_de_fabricacion")
}

onBeforeMount(async () => {
    await collectionStore.getAll()
    collections.value.forEach(async (collection) => {
        try {
            collection.cantidadMateriales = JSON.parse(await getCantidadMateriales(collection.caseId))
        } catch (error) {}
        try {
            collection.planDeFabricacion = JSON.parse(await getPlanDeFabricacion(collection.caseId))
        } catch (error) {}
        collection.orders_placed = !!(await fetchWrapper.get(`${baseUrl}/reservas/reservas-lugares-fabricacion/`)).find((order) => order.coleccion == collection.id)
        loading.value = false
    })
})


</script>

<template>
    <div>
        <template v-for="collection in collections" :key="collection.id">
        <ul v-if="!loading && collection.orders_placed">
                <span v-if="collection.designed">
                    <li>Nombre: {{ collection.name }} </li>
                    <li>Descripción: {{ collection.description }}</li>
                    <div v-if="collection.planDeFabricacion">
                        <div v-if="collection.orders_placed">
                            Ordenes de materiales y lugar de fabricación reservados
                        </div>
                        <div v-else>
                            <router-link
                                :to="{ name: 'fabrication-plan-confirm', params: { collection: collection.id } }">Confirmar
                                plan de fabricación</router-link>
                        </div>
                    </div>
                    <div v-if="!collection.planDeFabricacion && collection.cantidadMateriales"><router-link
                            :to="{ name: 'fabrication-plan', params: { collection: collection.id } }">Armar plan de
                            fabricación</router-link></div>
                    <div v-if="!collection.planDeFabricacion && !collection.cantidadMateriales"><router-link
                            :to="{ name: 'material-analysis', params: { collection: collection.id } }">Analizar
                            materiales</router-link></div>
                </span>
            </ul>
            <div v-else-if="collections.loading || loading" class="spinner-border spinner-border-sm"></div>
            <div v-else-if="collections.error" class="text-danger">Error loading collections: {{ collections.error }}</div>
            <div v-else>No hay nada</div>
        </template>
    </div>
</template>