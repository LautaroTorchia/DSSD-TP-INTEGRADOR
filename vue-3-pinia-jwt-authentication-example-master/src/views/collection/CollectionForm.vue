<template>
    <div>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="formData.name" />
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" v-model="formData.description"></textarea>
        </div>
        <div class="form-group">
          <button type="submit">Confirmar</button>
        </div>
      </form>
        <BackButton />
    </div>
  </template>
  
  <script>
  import BackButton from '@/components/backButton.vue';
  export default {
    data() {
      return {
        formData: {
          name: '',
          description: '',
        },
      };
    },
    methods: {
      submitForm() {
        this.$emit('form-submitted', this.formData);
      },
    },
  };
  </script>
  