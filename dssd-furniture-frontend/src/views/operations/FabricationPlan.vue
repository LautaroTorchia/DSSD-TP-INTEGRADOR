<template>
    <div>
        <div>
            {{ collectionMaterialList }}
            <h3>Material List</h3>
            <ul>
                <li v-for="material in collectionMaterialList.materials" :key="material.id">{{ material.name }}</li>
            </ul>
        </div>
        <div>
            {{ materialsFromProviders }}
            <h3>Materials from Providers</h3>
            <ul>
                <li v-for="material in materialsFromProviders" :key="material.id">{{ material.material_nombre }}</li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchWrapper } from '@/helpers'
import { router } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}`

function validateMaterialPresence(materialsFromProviders, collectionMaterialList) {
    return collectionMaterialList.map((material) => material.id).every((id) => materialsFromProviders.value.map((material) => material.material).includes(id))
}

function validateMaterialAmount(materialsFromProviders, collectionMaterialList) {
    const materialsFromProvidersWithAmount = materialsFromProviders.value.map(({ material, cantidad_disponible }) => ({ id: material, amount_available: cantidad_disponible }))
    const collectionMaterialListWithAmount = collectionMaterialList.map(({ id, amount }) => ({ id, amount }))
    return collectionMaterialListWithAmount.every((material) => {
        const availableMaterial = materialsFromProvidersWithAmount.filter((m) => m.id === material.id)
        const totalAmountAvailable = availableMaterial.reduce((total, m) => total + m.amount_available, 0)
        return totalAmountAvailable >= material.amount
    })
}

const collectionId = router.currentRoute.value.params.collection
const caseId = JSON.parse(localStorage.getItem('collections')).collections.find((collection) => collection.id == collectionId).caseId
const materialsFromProviders = ref([])
const collectionMaterialList = ref([])

const fetchMaterialsFromProviders = async () => {
    try {
        materialsFromProviders.value = await fetchWrapper.get(`${baseUrl}/proveedores/proveedores-materiales/`)
    } catch (error) {
        console.error(error)
    }
}

onMounted(async () => {
    await fetchMaterialsFromProviders()
    collectionMaterialList.value = await fetchWrapper.get(`${baseUrl}/bonita/case-variable/${caseId}/cantidad_materiales/`)
    collectionMaterialList.value = JSON.parse(collectionMaterialList.value.value)
    const allMaterialsProvided = validateMaterialPresence(materialsFromProviders, collectionMaterialList.value)
    const canFulfillAllMaterials = validateMaterialAmount(materialsFromProviders, collectionMaterialList.value)

    if (!allMaterialsProvided && !canFulfillAllMaterials) {
        router.push({ name: 'designed-collections' })
    }
})

</script>