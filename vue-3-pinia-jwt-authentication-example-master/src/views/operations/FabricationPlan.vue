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
            {{materialsFromProviders}}
            <h3>Materials from Providers</h3>
            <ul>
                <li v-for="material in materialsFromProviders" :key="material.id">{{ material.material_nombre }}</li>
            </ul>
        </div>
    </div>
</template>

<script>
import { useFurnitureStore, useMaterialsStore, useMaterialListStore } from '@/stores'
import { onMounted, ref } from 'vue'
import { fetchWrapper } from '@/helpers'
import { router } from '@/helpers'
const baseUrl = `${import.meta.env.VITE_API_URL}`

export default {
    setup() {
        const materialListStore = useMaterialListStore()        
        const collectionId = router.currentRoute.value.params.collection
        const materialsList = materialListStore.getMaterials
        const collectionMaterialList = materialsList.find((list) => list.id == collectionId)
        console.log(collectionMaterialList.materials)
        const materialsFromProviders = ref([])
        
        const fetchMaterialsFromProviders = async () => {
            try {
                materialsFromProviders.value = await fetchWrapper.get(`${baseUrl}/proveedores/proveedores-materiales/`)
            } catch (error) {
                console.error(error)
            }
        }
        
        onMounted(() => {
            fetchMaterialsFromProviders()
        })
        
        return {
            collectionMaterialList,
            materialsFromProviders
        }
    },
}
</script>