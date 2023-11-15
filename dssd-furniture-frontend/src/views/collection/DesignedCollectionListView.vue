<script setup>
import { storeToRefs } from 'pinia'
import { useCollectionsStore } from '@/stores'
import { getBonitaVariable } from '@/helpers';
import { onMounted, ref } from 'vue'; // Import the onMounted hook
const baseUrl = `${import.meta.env.VITE_API_URL}`

const collectionStore = useCollectionsStore()

const { collections } = storeToRefs(collectionStore)
let loading = ref(true)



async function getCantidadMateriales(caseId) {
    return await getBonitaVariable(caseId, "cantidad_materiales")
}

async function getPlanDeFabricacion(caseId) {
    return await getBonitaVariable(caseId, "plan_de_fabricaion")
}

onMounted(async () => {
    await collectionStore.getAll()
    collections.value.forEach(async (collection) => {
        collection.cantidadMateriales = await getCantidadMateriales(collection.caseId)
        collection.planDeFabricacion = await getPlanDeFabricacion(collection.caseId)
    })
    loading.value = false
})

</script>

<template>
    <div>
        <ul v-if="collections.length > 0 && !loading">
            <template v-for="collection in collections" :key="collection.id">
                <span v-if="collection.designed">
                    <li>Nombre: {{ collection.name }} </li>
                    <li>Descripción: {{ collection.description }}</li>

                    <div v-if="collection.cantidadMateriales"><router-link
                            :to="{ name: 'fabrication-plan', params: { collection: collection.id } }">Armar plan de
                            fabricación</router-link></div>
                    <div v-else-if="collection.planDeFabricacion"><router-link
                            :to="{ name: 'fabrication-plan-confirm', params: { collection: collection.id } }">Confirmar plan de fabricación</router-link></div>
                    <div v-else><router-link
                            :to="{ name: 'material-analysis', params: { collection: collection.id } }">Analizar
                            materiales</router-link></div>
                </span>
            </template>
        </ul>
        <div v-else-if="collections.loading || loading" class="spinner-border spinner-border-sm"></div>
        <div v-else-if="collections.error" class="text-danger">Error loading collections: {{ collections.error }}</div>
        <div v-else>No hay nada</div>
</div></template>