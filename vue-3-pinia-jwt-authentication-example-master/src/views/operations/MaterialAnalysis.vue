<template>
    <div>
        <h1>Material Analysis for Collection {{ collectionId }}</h1>
        <form @submit.prevent="submitForm">
            <div v-for="(piece, index) in furniture" :key="index">
                <h2>{{ piece.nombre }}</h2>
                <div v-for="(material, index) in piece.materiales" :key="index">
                    <label>{{ material.nombre }}:</label>
                    <input type="number" v-model="material.amount">
                </div>
            </div>
            <button type="submit">Submit</button>
        </form>
    </div>
</template>

<script>
import { storeToRefs } from 'pinia'
import { useFurnitureStore, useMaterialsStore } from '@/stores'
import { router } from '@/helpers'
import { onMounted } from 'vue'

export default {
    setup() {
        const furnitureStore = useFurnitureStore()
        const materialsStore = useMaterialsStore()
        const { furniture } = storeToRefs(furnitureStore)
        const collectionId = router.currentRoute.value.params.collection

        furnitureStore.getCollectionFurniture(collectionId)

        const submitForm = () => {
            const materialsAmount = {}
            furniture.value.forEach((piece) => {
                piece.materiales.forEach((material) => {
                    if (materialsAmount[material.nombre]) {
                        materialsAmount[material.nombre] += material.amount
                    } else {
                        materialsAmount[material.nombre] = material.amount
                    }
                })
            })
            let message = ''
            for (const material in materialsAmount) {
                message += `${material}: ${materialsAmount[material]}\n`
            }
            alert(message)
        }

        onMounted(async () => {
            const materials = await materialsStore.getAll()
            furniture.value.forEach((piece) => {
                piece.materiales.forEach((materialId, index) => {
                    const material = materials.find((m) => m.id == materialId)
                    if (material) {
                        piece.materiales[index] = { ...material, amount: 0 }
                    }
                })
            })
        })

        return {
            furniture,
            collectionId,
            submitForm
        }
    }
}
</script>
