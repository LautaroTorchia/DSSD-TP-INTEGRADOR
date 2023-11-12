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
import { useMaterialListStore } from '@/stores'
import { onMounted, ref } from 'vue'
import { fetchWrapper } from '@/helpers'
import { router } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}`

function validateMaterialPresence(materialsFromProviders, collectionMaterialList) {
    return collectionMaterialList.materials.map((material) => material.id).every((id) => materialsFromProviders.value.map((material) => material.material).includes(id))
}

function validateMaterialAmount(materialsFromProviders, collectionMaterialList) {
    const materialsFromProvidersWithAmount = materialsFromProviders.value.map(({ material, cantidad_disponible }) => ({ id: material, amount_available: cantidad_disponible }))
    const collectionMaterialListWithAmount = collectionMaterialList.materials.map(({ id, amount }) => ({ id, amount }))
    return collectionMaterialListWithAmount.every((material) => {
        const availableMaterial = materialsFromProvidersWithAmount.filter((m) => m.id === material.id)
        const totalAmountAvailable = availableMaterial.reduce((total, m) => total + m.amount_available, 0)
        console.log(totalAmountAvailable, availableMaterial, material.amount)
        return totalAmountAvailable >= material.amount
    })
}

const materialListStore = useMaterialListStore()
const collectionId = router.currentRoute.value.params.collection
const materialsList = materialListStore.getMaterials
const collectionMaterialList = materialsList.find((list) => list.id == collectionId)
const materialsFromProviders = ref([])

const fetchMaterialsFromProviders = async () => {
    try {
        materialsFromProviders.value = await fetchWrapper.get(`${baseUrl}/proveedores/proveedores-materiales/`)
    } catch (error) {
        console.error(error)
    }
}

onMounted(async () => {
    await fetchMaterialsFromProviders()
    const allMaterialsProvided = validateMaterialPresence(materialsFromProviders, collectionMaterialList)
    const canFulfillAllMaterials = validateMaterialAmount(materialsFromProviders, collectionMaterialList)

    if (!allMaterialsProvided && !canFulfillAllMaterials) {
        router.push({ name: 'designed-collections' })
    }
})

</script>