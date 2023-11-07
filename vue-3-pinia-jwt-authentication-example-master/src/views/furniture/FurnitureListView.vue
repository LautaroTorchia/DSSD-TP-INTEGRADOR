<script setup>
import { storeToRefs } from 'pinia'
import { useFurnitureStore } from '@/stores'
import { router } from '@/helpers'
import BackButton from '@/components/BackButton.vue'

const furnitureStore = useFurnitureStore()
const { furniture } = storeToRefs(furnitureStore)
const collectionId = router.currentRoute.value.params.collection


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
                <li>Fecha de lanzamiento estimada: {{ furniture.fecha_lanzamiento_estimada }}</li>
                <router-link :to="{ name: 'furniture-detail', params: { collection: collectionId, id: furniture.id } }">Ver</router-link>
                <button @click="deleteFurniture(furniture.id)">Borrar</button>
                <button @click="updateFurniture(furniture.id)">Editar</button>
            </template>
        </ul>
        <div v-else-if="furniture.loading" class="spinner-border spinner-border-sm"></div>
        <div v-else-if="furniture.error" class="text-danger">Error loading furniture: {{ furniture.error }}</div>
        <div v-else>No hay muebles en la coleccion</div>
        <BackButton/>
    </div>
</template>
