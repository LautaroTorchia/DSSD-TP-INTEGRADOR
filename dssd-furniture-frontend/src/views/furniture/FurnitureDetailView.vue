<script setup>
import { ref, onMounted } from 'vue'
import { useFurnitureStore, useCollectionsStore, useMaterialsStore } from '@/stores'
import { router } from '@/helpers'
import BackButton from '@/components/BackButton.vue'

const furniturePiece = ref({})
const collection = ref('')
const furnitureStore = useFurnitureStore()
const collectionsStore = useCollectionsStore()
const materialsStore = useMaterialsStore()

onMounted(async () => {
    const id = router.currentRoute.value.params.id
    const collectionId = router.currentRoute.value.params.collection
    furniturePiece.value = await furnitureStore.getFurnitureDetail(id)
    const materials = await materialsStore.getAll()
    console.log(furniturePiece.value.materiales)
    furniturePiece.value.materiales = furniturePiece.value.materiales.map(material => {
        const materialData = materials.find(m => m.id == material|| console.log(material, m.id))
        
        return materialData.nombre
    })
    collection.value = collectionsStore.getById(collectionId).name
})
</script>

<template>
    <div>
        <h2>Mueble {{ furniturePiece.nombre }}</h2>
        <li>Colección: {{ collection }} </li>
        <li>Plazo de fabricación: {{ furniturePiece.plazo_fabricacion }}</li>
        <li>Descripción: {{ furniturePiece.descripcion }}</li>
        <li>Imagen:</li>
        <img :src="furniturePiece.imagen" alt="Imagen del mueble">
        <li>Plan de fabricación: {{ furniturePiece.plan_fabricacion }}</li>
        <li>Materiales: 
            <span v-for="(material, index) in furniturePiece.materiales" :key="index">
                {{ material }}{{ index !== furniturePiece.materiales.length - 1 ? ', ' : '' }}
            </span>
        </li>
        <li>Colección: {{ furniturePiece.coleccion }}</li>
        <BackButton />
    </div>
</template>


