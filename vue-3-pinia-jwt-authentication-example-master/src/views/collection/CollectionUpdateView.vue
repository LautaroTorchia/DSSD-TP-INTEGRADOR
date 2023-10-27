<template>
    <div>
        <h2>Editar Colección</h2>
        <CollectionForm @form-submitted="handleFormSubmission" />
    </div>
</template>
  
<script>
import { router } from '../../helpers/router';
import CollectionForm from './CollectionForm.vue';
import { useCollectionsStore } from '@/stores'

export default {
    components: {
        CollectionForm,
    },
    data() {
        return {
            formData: {
                name: '',
                description: '',
            },
        };
    },
    methods: {
        handleFormSubmission(formData) {
            const collectionStore = useCollectionsStore()
            collectionStore.update(formData)
            router.push({ name: 'collections' })
        },
    },
};
</script>
  