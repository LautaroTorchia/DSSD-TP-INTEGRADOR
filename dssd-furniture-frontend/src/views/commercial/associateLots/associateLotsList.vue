<template>
    <div>
        {{showCollections}}

    </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useCollectionsStore } from '@/stores'
import { fetchWrapper } from '@/helpers'
import { ref, onMounted } from 'vue'

const baseUrl = `${import.meta.env.VITE_API_URL}`

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const showCollections = ref([])
const loading = ref(true)

onMounted(async () => {
    let distributions = await fetchWrapper.get(`${baseUrl}/entregas/distribucion-de-lote/`)
    let lots = await fetchWrapper.get(`${baseUrl}/entregas/lotes-fabricados/`)
    await collectionStore.getAll()
    showCollections.value = collections.value.filter(collection => collection.fabricated)
    lots = await lots
})
</script>
