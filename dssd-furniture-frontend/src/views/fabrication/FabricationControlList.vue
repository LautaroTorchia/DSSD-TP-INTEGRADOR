<template></template>
TODO Fabrication control list
<script setup>
import { onMounted, ref } from 'vue'
import { getBonitaVariable } from '@/helpers'
import { storeToRefs } from 'pinia'
import { useCollectionsStore } from '@/stores'

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const showCollections = ref([])

onMounted(async () => {
    await collectionStore.getAll()
    
    
    showCollections.value = collections.value.filter((collection) => {
        return collection.designed
    })
    
    
    showCollections.value = showCollections.value.filter(async (collection) => {
        const behindSchedule = await getBonitaVariable(collection.caseId, "retraso_materiales")
        
        return behindSchedule == "true"
    })
    
})
</script>