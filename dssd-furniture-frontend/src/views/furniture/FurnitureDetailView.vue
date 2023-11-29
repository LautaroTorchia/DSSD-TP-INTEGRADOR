<template>
    <div v-if="!loading" class="card" >
        <div class="card-body">
            <h2 class="card-title">Mueble {{ furniturePiece.nombre }}</h2>
            <ul class="list-group">
                <li class="list-group-item">Colección: {{ collection }}</li>
                <li class="list-group-item">Plazo de fabricación: {{ furniturePiece.plazo_fabricacion }}</li>
                <li class="list-group-item">Descripción: {{ furniturePiece.descripcion }}</li>
                <li class="list-group-item">Imagen:</li>
                <img :src="`data:image/png;base64,${furniturePiece.imagen_content}`" class="card-img-top"
                    alt="Furniture Image" />
                <li class="list-group-item">Plan de fabricación:
                    <a :href="`data:application/pdf;base64,${furniturePiece.plan_fabricacion_content}`"
                        download="plan_fabricacion.pdf">Descargar</a>
                </li>
                <li class="list-group-item">Materiales:
                    <span v-for="(material, index) in furniturePiece.materiales" :key="index">
                        {{ material }}{{ index !== furniturePiece.materiales.length - 1 ? ', ' : '' }}
                    </span>
                </li>
                <li class="list-group-item">Colección: {{ furniturePiece.coleccion }}</li>
            </ul>
        </div>
    </div>
    <div v-else class="spinner-border spinner-border-sm"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useFurnitureStore, useCollectionsStore, useMaterialsStore } from '@/stores'
import { router } from '@/helpers'

const furniturePiece = ref({})
const collection = ref('')
const furnitureStore = useFurnitureStore()
const collectionsStore = useCollectionsStore()
const materialsStore = useMaterialsStore()
const loading = ref(true)

onMounted(async () => {
    const id = router.currentRoute.value.params.id
    const collectionId = router.currentRoute.value.params.collection
    const materialsPromise = materialsStore.getAll()
    furniturePiece.value = await furnitureStore.getFurnitureDetail(id)
    const materials = await materialsPromise
    furniturePiece.value.materiales = furniturePiece.value.materiales.map(material => {
        const materialData = materials.find(m => m.id == material)
        return materialData.nombre
    })
    collection.value = collectionsStore.getById(collectionId).name
    loading.value = false
})
</script>

<style scoped>
.card {
    width: 400px;
    margin: 0 auto;
    margin-top: 20px;
    padding: 20px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    border-radius: 5px;
}

.card-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
}

.list-group-item {
    border: none;
    padding: 5px;
}

.card-img-top {
    width: 100%;
    height: auto;
    margin-top: 10px;
}
</style>
