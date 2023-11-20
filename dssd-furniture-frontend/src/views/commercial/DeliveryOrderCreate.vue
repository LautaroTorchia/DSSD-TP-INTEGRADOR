
<template>
    <div>
        <h1>Delivery Order Create</h1>
        <div v-if="lotQuantity">
            <h2>Ordenes de entrega: </h2>
            <p>{{ lotQuantity }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getBonitaVariable, fetchWrapper } from '@/helpers';
import { useCollectionsStore } from '@/stores'
import { storeToRefs } from 'pinia'
import { router } from '@/helpers'

const collectionStore = useCollectionsStore()
const caseId = ref('')
const { collections } = storeToRefs(collectionStore)

const baseUrl = `${import.meta.env.VITE_API_URL}`
const collectionId = router.currentRoute.value.params.collection
const lotQuantity = ref(0)


const planDeFabricacion = ref('');

onMounted(async () => {
    try {
        caseId.value = JSON.parse(localStorage.getItem('collections')).collections.find((collection) => collection.id == collectionId).caseId
    } catch (error) {
        await collectionStore.getAll()
        caseId.value = JSON.parse(localStorage.getItem('collections')).collections.find((collection) => collection.id == collectionId).caseId
    }
    lotQuantity.value = Number(JSON.parse(await getBonitaVariable(caseId.value, 'plan_de_fabricacion')).lotQuantity)
});
</script>
