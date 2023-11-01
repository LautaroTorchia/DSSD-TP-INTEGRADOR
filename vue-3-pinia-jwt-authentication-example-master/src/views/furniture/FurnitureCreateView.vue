<script>
import { defineComponent } from 'vue';
import { router } from '@/helpers';
import FurnitureForm from './FurnitureForm.vue';
import { useCollectionsStore } from '@/stores';

export default defineComponent({
    components: {
        FurnitureForm,
    },
    setup() {
        const formData = {
            name: '',
            deadline: '',
            estimated_release: '',
            description: '',
            image: '',
            manufacturing_plan: '',
            materials: '',
        };

        const collectionStore = useCollectionsStore();

        const handleFormSubmission = () => {
            collectionStore.create(formData);
            router.push({ name: 'collections' });
        };

        return {
            formData,
            handleFormSubmission,
        };
    },
});
</script>
<template>
    <div>
        <h2>Crear Mueble de la collección {{ coll }}</h2>
        <FurnitureForm @form-submitted="handleFormSubmission" />
    </div>
</template>
