<template>
    <div>
        <h1>Crear ordenes de entrega</h1>
        <div v-if="!loading">
            <ul v-for="collection in collections" :key="collection.id" class="list-group">
                <li v-if="collection.orders_placed" class="list-group-item">
                    {{ collection.name }}
                </li>
            </ul>
        </div>
        <div v-else-if="loading" class="spinner-border spinner-border-sm"></div>
        <div v-else-if="collections.error" class="text-danger">Error loading collections: {{ collections.error }}</div>
        <div v-else>No hay nada</div>
    </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useCollectionsStore } from '@/stores'
import { ref, onMounted } from 'vue'
import { fetchWrapper } from '@/helpers'

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const baseUrl = `${import.meta.env.VITE_API_URL}`
const loading = ref(true)

onMounted(async () => {
    await collectionStore.getAll()
    collections.value.forEach(async (collection) => {
        collection.orders_placed = !!(await fetchWrapper.get(`${baseUrl}/reservas/reservas-lugares-fabricacion/`)).find((order) => order.coleccion == collection.id)
    })
    loading.value = false
})

</script>

