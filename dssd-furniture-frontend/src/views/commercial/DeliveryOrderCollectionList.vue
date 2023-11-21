<template>
    <div>
        <h1>Crear ordenes de entrega</h1>
        <div v-if="!loading">
            <ul v-for="collection in showCollections" :key="collection.id" class="list-group">
                <li class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                        <span>{{ collection.name }}</span>
                        <router-link :to="{ name: 'delivery-order-create', params: { collection: collection.id } }"
                            class="btn btn-primary">
                            <slot>Crear ordenes de entrega</slot>
                        </router-link>
                    </div>
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
import { ref, onMounted, computed } from 'vue'
import { fetchWrapper } from '@/helpers'

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const showCollections = ref([])
const baseUrl = `${import.meta.env.VITE_API_URL}`
const loading = ref(true)

onMounted(async () => {
    await collectionStore.getAll()
    const factoryOrder = await fetchWrapper.get(`${baseUrl}/reservas/reservas-lugares-fabricacion/`)
    const orders = await fetchWrapper.get(`${baseUrl}/entregas/ordenes/`)
    showCollections.value = collections.value.filter(collection => {
        const factoryOrderExists = factoryOrder.some(order => order.coleccion == collection.id)
        const orderExists = orders.some(order => order.id_coleccion == collection.id)
        return factoryOrderExists && !orderExists
    })
    loading.value = false
})

</script>

