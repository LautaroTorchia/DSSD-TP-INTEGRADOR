<script>
import { router } from '@/helpers';
import FurnitureForm from './FurnitureForm.vue';
import { useFurnitureStore} from '@/stores';

export default {
    components: {
        FurnitureForm,
    },
    data() {
      return {
        formData: {
          name: '',
          estimated_days: '',
          estimated_release: '',
          description: '',
          image: '',
          manufacturing_plan: '',
          materials: '',
        },
      };
    },
    methods: {
        handleFormSubmission(formData) {
            console.log("create form: ", formData)
            const furnitureStore = useFurnitureStore()
            furnitureStore.create(formData)
            router.push({ name: 'furniture' })
        },
    },
};
</script>
<template>
    <div>
        <h2>Crear Mueble de la collección</h2>
        <FurnitureForm @form-submitted="handleFormSubmission" />
    </div>
</template>
