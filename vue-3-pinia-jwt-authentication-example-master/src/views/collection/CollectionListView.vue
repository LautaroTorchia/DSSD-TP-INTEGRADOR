<script setup>
import { storeToRefs } from 'pinia';
import { useCollectionsStore } from '@/stores'
import { router } from '@/helpers/router'

const collectionStore = useCollectionsStore();
const { collections } = storeToRefs(collectionStore);
collectionStore.getAll();

const deleteCollection = async (id) => {
    const confirmed = confirm('¿Desea borrar la colección?')
    if (confirmed) {
        try {
            await collectionStore.delete(id);
        } catch (error) {
            alert('Error al borrar la colección')
            console.error(error);
        }
    }
}

const updateCollection = (collection) => {
    localStorage.setItem(collection.id, JSON.stringify(collection));
    router.push({ name: 'collection-update', params: { collection: collection.id } });
}

const finishCollection = async (collection) => {
    const confirmed = confirm('¿Desea terminar la colección?');
    if (confirmed) {
        try {
            collection.finished = true
            await collectionStore.finish(collection);
        } catch (error) {
            alert('Error al terminar la colección')
            console.error(error);
        }
    }
}

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
                <router-link :to="`/${collection.id}/furniture`">Ver muebles</router-link>

                <li v-if="collection.finished">
                    Terminada: Sí
                </li>
                <li v-else>
                    Terminada: No
                    <button @click="deleteCollection(collection.id)">Borrar</button>
                    <button @click="updateCollection(collection)">Editar</button>
                    <button @click="finishCollection(collection)">Terminar</button>
                </li>
            </template>
        </ul>
        <div v-else-if="collections.loading" class="spinner-border spinner-border-sm"></div>
        <div v-else-if="collections.error" class="text-danger">Error loading collections: {{ collections.error }}</div>
        <div v-else>No hay nada</div>
    </div>
</template>
