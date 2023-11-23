<script setup>
import { storeToRefs } from 'pinia'
import { useFurnitureStore, useCollectionsStore } from '@/stores'
import { router } from '@/helpers'
import BackButton from '@/components/BackButton.vue'
import { onBeforeMount, ref } from 'vue'

const furnitureStore = useFurnitureStore()
const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const { furniture } = storeToRefs(furnitureStore)
const collectionId = router.currentRoute.value.params.collection
const loading = ref(true)
const collection = ref({})

onBeforeMount(async () => {
    await furnitureStore.getCollectionFurniture(collectionId)
    collection.value = collections.value.find((collection) => collection.id == collectionId)
    loading.value = false
})



const deleteFurniture = async (id) => {
    const confirmed = confirm('¿Desea borrar el mueble?')
    if (confirmed) {
        try {
            furnitureStore.delete(id)
        } catch (error) {
            alert('Error al borrar el mueble')
            console.error(error)
        }
    }
}



</script>

<template>
    <div>
        <div>
            <router-link :to="{ name: 'furniture-create' }">Crear mueble</router-link>
        </div>
        <ul v-if="furniture.length">
            <template v-for="furniture in furniture" :key="furniture.id">
                <li>Nombre: {{ furniture.nombre }} </li>
                <router-link :to="{ name: 'furniture-detail', params: { collection: collectionId, id: furniture.id } }">Ver</router-link>
                
                <button v-if="!collection.designed" @click="deleteFurniture(furniture.id)">Borrar</button>
            </template>
        </ul>
        <div v-else-if="furniture.loading" class="spinner-border spinner-border-sm"></div>
        <div v-else-if="furniture.error" class="text-danger">Error loading furniture: {{ furniture.error }}</div>
        <div v-else>No hay muebles en la coleccion</div>
        <BackButton/>
    </div>
</template>
