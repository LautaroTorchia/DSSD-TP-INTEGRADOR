<template>
  <div>
    <h2>Collections Happening This Quarter: {{ quarter }}</h2>
        {{ collectionsThisQuarter }} - 
  </div>
</template>

<script setup>
import { useCollectionsStore } from '@/stores'
import { storeToRefs } from 'pinia';
import { onMounted, ref } from 'vue';
const collectionsStore = useCollectionsStore()
const { collections } = storeToRefs(collectionsStore)
const collectionsThisQuarter = ref([])
const quarter = Math.floor((new Date().getMonth() / 3) + 1)

onMounted(async () => {
    await collectionsStore.getAll()
    
})

</script>
