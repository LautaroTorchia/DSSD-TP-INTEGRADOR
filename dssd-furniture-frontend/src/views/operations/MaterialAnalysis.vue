<template>
    <div>
        <h1>Material Analysis for Collection {{ collectionId }}</h1>
        <form @submit.prevent="submitForm">
            <div v-for="(piece, index) in furniture" :key="index">
                <h2>{{ piece.nombre }}</h2>
                <div v-for="(material, index) in piece.materiales" :key="index">
                    <label>{{ material.nombre }}:</label>
                    <input type="number" v-model="material.amount" min="1">
                    kg
                </div>
            </div>
            <button type="submit">Aceptar</button>
        </form>
    </div>
</template>

<script>
import { storeToRefs } from 'pinia'
import { useFurnitureStore, useMaterialsStore } from '@/stores'
import { router, advanceBonitaTask, fetchWrapper, getBonitaVariable } from '@/helpers'
import { onMounted } from 'vue'

const baseUrl = `${import.meta.env.VITE_API_URL}`

export default {
    setup() {

        const furnitureStore = useFurnitureStore()
        const materialsStore = useMaterialsStore()
        const { furniture } = storeToRefs(furnitureStore)
        const collectionId = router.currentRoute.value.params.collection

        furnitureStore.getCollectionFurniture(collectionId)

        const submitForm = async () => {
            var materialsAmount = []

            furniture.value.forEach((piece) => {
                piece.materiales.forEach((material) => {
                    if (materialsAmount[material.id]) {
                        materialsAmount[material.id].amount += material.amount
                    } else {
                        materialsAmount[material.id] = { id: material.id, name: material.nombre, amount: material.amount }
                    }
                })
            })
            materialsAmount = materialsAmount.filter((material) => material)//delete empty slots
            let message = {}
            materialsAmount.forEach((material) => {
                message[material.name] = material.amount
            })

            const confirmed = confirm("Confirma estos materiales: \n" +
                Object.entries(message)
                    .map(([material, amount]) => `${material}: ${amount}`)
                    .join('\n')
            )
            if (confirmed) {
                try {
                    const caseId = JSON.parse(localStorage.getItem('collections')).collections.find((collection) => collection.id == collectionId).caseId
                    await fetchWrapper.put(`${baseUrl}/bonita/update-case-variable/${caseId}/cantidad_materiales/`, { type: "java.lang.String", value: JSON.stringify(materialsAmount) })
                    await advanceBonitaTask(caseId)
                    router.push({ name: 'fabrication-plan' })
                } catch (error) {
                    console.error(error)
                }
            }
        }

        onMounted(async () => {
            const caseId = JSON.parse(localStorage.getItem('collections')).collections.find((collection) => collection.id == collectionId).caseId
            if (await getBonitaVariable(caseId, "consulta_materiales")) {
                router.push({ name: 'fabrication-plan' })
            }

            const materials = await materialsStore.getAll()
            furniture.value.forEach((piece) => {
                piece.materiales = piece.materiales.split(',').map((material) => Number(material))
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
