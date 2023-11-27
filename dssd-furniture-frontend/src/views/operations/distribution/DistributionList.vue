<template>
    <div>
        <h1>Asociar distribucion interna</h1>
        <div v-if="!loading">
            <ul v-for="collection in showCollections" :key="collection.id" class="list-group">
                <li class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                        <span>{{ collection.name }}</span>
                        <router-link :to="{ name: 'distribution-create', params: { collection: collection.id } }"
                            class="btn btn-primary">
                            <slot>Asociar lotes</slot>
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
import { ref, onMounted } from 'vue'

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const showCollections = ref([])
const loading = ref(true)

onMounted(async () => {
    await collectionStore.getAll()
    showCollections.value = collections.value.filter(collection => {return collection.fabricated})
    loading.value = false
})

</script>
