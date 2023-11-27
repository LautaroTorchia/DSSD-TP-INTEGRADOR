<template>
    <div v-if="!loading">
        <h2>Distribuir lotes: {{ collection.name  }}</h2>
        <div v-for="lot in lots" :key="lot.id">
            <div class="card">
                <div class="card-header">Lote {{ lot.id }}</div>
                <div class="card-body">
                    <label for="distributor">Lugar de distribución:</label>
                    <select v-model="lot.distributor" id="distributor">
                        <option v-for="distributor in distributors" :key="distributor.id" :value="distributor.id">
                            {{ distributor.nombre }}
                        </option>
                    </select>
                </div>
            </div>
        </div>
    </div>
    <div v-else class="spinner-border text-primary" role="status"></div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { router, fetchWrapper } from '@/helpers'
import { storeToRefs } from 'pinia'
import { useCollectionsStore } from '@/stores'

const collectionId = router.currentRoute.value.params.collection
const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const baseUrl = `${import.meta.env.VITE_API_URL}`

const lots = ref([])
const distributors = ref([])
const collection = ref(null)
const loading = ref(true)

onMounted(async () => {
    const lotsPromise = fetchWrapper.get(`${baseUrl}/entregas/lotes-fabricados/`)
    const distributorsPromise = fetchWrapper.get(`${baseUrl}/entregas/lugares-de-distribucion/`)
    await collectionStore.getAll()
    collection.value = collections.value.find(collection => collection.id == collectionId)
    lots.value = (await lotsPromise).filter(lot => lot.coleccion == collectionId)
    distributors.value = await distributorsPromise
    console.log(collection.value)
    console.log(lots.value)
    console.log(distributors.value)
    loading.value = false
})
</script>

