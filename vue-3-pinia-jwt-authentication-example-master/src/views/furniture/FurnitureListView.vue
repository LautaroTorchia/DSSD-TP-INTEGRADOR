<script setup>
import { storeToRefs } from 'pinia';
import { useFurnituresStore } from '@/stores'

const furnitureStore = useFurnituresStore();
const { furnitures } = storeToRefs(furnitureStore);
furnitureStore.getAll();

const deleteFurniture = async (id) => {
    const confirmed = confirm('¿Desea borrar el mueble?')
    if (confirmed) {
        try {
            furnitureStore.delete(id);
            furnitureStore.getAll();
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
        <ul v-if="furnitures.length">
            <template v-for="furniture in furnitures" :key="furniture.id">
                <li>Nombre: {{ furniture.name }} </li>
                <li>Descripción: {{ furniture.description }}</li>
                <button @click="deleteFurniture(furniture.id)">Borrar</button>
            </template>
        </ul>
        <div v-else-if="furnitures.loading" class="spinner-border spinner-border-sm"></div>
        <div v-else-if="furnitures.error" class="text-danger">Error loading furnitures: {{ furnitures.error }}</div>
        <div v-else>No hay muebles en la coleccion</div>
    </div>
</template>

