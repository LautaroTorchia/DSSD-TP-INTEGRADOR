<script setup>
import { storeToRefs } from 'pinia';
import { useCollectionsStore } from '@/stores'

const collectionStore = useCollectionsStore();
const { collections } = storeToRefs(collectionStore);
collectionStore.getAll();

const deleteCollection = async (id) => {
    const confirmed = confirm('Are you sure you want to delete this collection?');
    if (confirmed) {
        try {
            collectionStore.delete(id);
            collectionStore.getAll();
        } catch (error) {
            console.error(error);
        }
    }
};

</script>

<template>
    <div>
        <div>
            <router-link :to="{ name: 'collection-create' }">Crear colección</router-link>
        </div>
        <ul v-if="collections.length">
            <template v-for="collection in collections" :key="collection.id">
                <li>Nombre: {{ collection.name }} </li>
                <li>Descripción: {{ collection.description }}</li>
                <button @click="deleteCollection(collection.id)">Delete</button>
            </template>
        </ul>
        <div v-else-if="collections.loading" class="spinner-border spinner-border-sm"></div>
        <div v-else-if="collections.error" class="text-danger">Error loading collections: {{ collections.error }}</div>
        <div v-else>No hay nada</div>
    </div>
</template>
