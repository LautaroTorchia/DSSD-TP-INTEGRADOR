<template>
    <div>
      <h2>Crear Colección</h2>
      <CollectionForm @form-submitted="handleFormSubmission" />
    </div>
  </template>
  
  <script>
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
        collectionStore.create(formData)
      },
    },
  };
  </script>
  