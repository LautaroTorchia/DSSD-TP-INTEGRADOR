<script setup>
import { storeToRefs } from 'pinia'
import { useFurnitureStore } from '@/stores'
import { router } from '@/helpers'

const furnitureStore = useFurnitureStore();
const { furniture } = storeToRefs(furnitureStore);
const collection_id = router.currentRoute.value.params.collection
furnitureStore.getCollectionFurniture(collection_id)


const deleteFurniture = async (id) => {
    const confirmed = confirm('¿Desea borrar el mueble?')
    if (confirmed) {
        try {
            furnitureStore.delete(id);
        } catch (error) {
            alert('Error al borrar el mueble')
            console.error(error);
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
                <li>Nombre: {{ furniture.name }} </li>
                <li>Descripción: {{ furniture.description }}</li>
                <button @click="deleteFurniture(furniture.id)">Borrar</button>
                <button @click="updateFurniture(furniture.id)">Editar</button>
            </template>
        </ul>
        <div v-else-if="furniture.loading" class="spinner-border spinner-border-sm"></div>
        <div v-else-if="furniture.error" class="text-danger">Error loading furniture: {{ furniture.error }}</div>
        <div v-else>No hay muebles en la coleccion</div>
    </div>
</template>