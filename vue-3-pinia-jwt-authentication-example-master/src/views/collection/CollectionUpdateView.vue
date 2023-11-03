<template>
    <div>
        <h2>Editar Colección {{ collection.id }}</h2>
        <CollectionForm :formData="formData" @form-submitted="handleFormSubmission" />
    </div>
</template>

<script>
import { defineComponent } from 'vue'
import { router } from '@/helpers/router'
import CollectionForm from './CollectionForm.vue'
import { useCollectionsStore } from '@/stores'

export default defineComponent({
    components: {
        CollectionForm,
    },
    setup() {
        const collectionStore = useCollectionsStore()
        const collectionId = router.currentRoute.value.params.collection
        const collection = collectionStore.getById(collectionId)
        const formData = {
            name: collection.name,
            description: collection.description,
        }

        const handleFormSubmission = (formData) => {
            const updatedCollection = { ...collection, ...formData }
            collectionStore.update(updatedCollection)
            router.push({ name: 'collections' })
        }

        return {
            collection,
            formData,
            handleFormSubmission,
        }
    },
})
</script>
