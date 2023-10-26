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
          <button type="submit">Crear</button>
        </div>
      </form>
      <router-link :to="{ name: 'collections' }">Volver</router-link>
    </div>
  </template>
  
  <script>
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
  