<script>
import { ref, onMounted } from 'vue'
import { useFurnitureStore, useCollectionsStore } from '@/stores'
import { router } from '@/helpers'
import BackButton from '@/components/BackButton.vue'

export default {
    components: {
        BackButton
    },
    setup() {
        const furniturePiece = ref({})
        const collection = ref('')
        const furnitureStore = useFurnitureStore()
        const collectionsStore = useCollectionsStore()

        onMounted(async () => {
            const id = router.currentRoute.value.params.id
            const collectionId = router.currentRoute.value.params.collection
            furniturePiece.value = await furnitureStore.getFurnitureDetail(id)
            collection.value = collectionsStore.getById(collectionId).name
            console.log(furniturePiece.value)
        })

        return {
            furniturePiece,
            collection
        }
    }
}
</script>

<template>
    <div>
        <h2>Mueble {{ furniturePiece.nombre }}</h2>
        <li>Colección: {{ collection }} </li>
        <li>Plazo de fabricación: {{ furniturePiece.plazo_fabricacion }}</li>
        <li>Fecha de lanzamiento estimada: {{ furniturePiece.fecha_lanzamiento_estimada }}</li>
        <li>Descripción: {{ furniturePiece.descripcion }}</li>
        <li>Imagen:</li>
        <img :src="furniturePiece.imagen" alt="Imagen del mueble">
        <li>Plan de fabricación: {{ furniturePiece.plan_fabricacion }}</li>
        <li>Materiales: {{ furniturePiece.materiales }}</li>
        <li>Colección: {{ furniturePiece.coleccion }}</li>
        <BackButton />
    </div>
</template>


