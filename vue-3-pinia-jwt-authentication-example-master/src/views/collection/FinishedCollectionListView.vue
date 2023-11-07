<script setup>
import { storeToRefs } from 'pinia'
import { useCollectionsStore, useMaterialsStore } from '@/stores'

const collectionStore = useCollectionsStore()
const materiasStore = useMaterialsStore()
const material = {
    nombre: "Madera",
    // add more properties as needed
};



materiasStore.create(material)
console.log("materiasStore.getAll()")
console.log(materiasStore.getAll())
const { collections } = storeToRefs(collectionStore)
collectionStore.getAll()



</script>

<template>
    <div>
        <ul v-if="collections.length > 0">
            <template v-for="collection in collections" :key="collection.id">
                <span v-if="collection.finished">
                    <li>Nombre: {{ collection.name }} </li>
                    <li>Descripción: {{ collection.description }}</li>
                    <router-link :to="{ name: 'material-analysis', params: { collection: collection.id } }">Analizar materiales</router-link>
                </span>
            </template>
        </ul>
        <div v-else-if="collections.loading" class="spinner-border spinner-border-sm"></div>
        <div v-else-if="collections.error" class="text-danger">Error loading collections: {{ collections.error }}</div>
        <div v-else>No hay nada</div>
    </div>
</template>
