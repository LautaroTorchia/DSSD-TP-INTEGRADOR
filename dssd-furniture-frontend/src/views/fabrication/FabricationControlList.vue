<template>
    <div  >
        <h1>Controlar Fabricacion</h1>
        <ul class="list-group">
            <li v-for="collection in showCollections" :key="collection.id" class="list-group-item">
                <router-link :to="{ name: 'fabrication-control', params: { collection: collection.id } }" class="text-decoration-none">
                    {{ collection.name }}
                </router-link>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getBonitaVariable } from '@/helpers'
import { storeToRefs } from 'pinia'
import { useCollectionsStore } from '@/stores'

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const showCollections = ref([])
const loading = ref(true)

onMounted(async () => {
    await collectionStore.getAll()
    const designedCollections = collections.value.filter((collection) => {
        return collection.designed
    })

    showCollections.value = await Promise.all(designedCollections.map(async (collection) => {
        const behindSchedule = await getBonitaVariable(collection.caseId, "retraso_materiales")
        if (behindSchedule === "false") {
            return collection
        }
    })).then(res => res.filter(collection => collection !== undefined))
    loading.value = false
})

</script>