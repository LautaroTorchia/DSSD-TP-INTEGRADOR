<template>
    <button @click="() => {this.$router.back()}">Volver</button>
</template>
<script>
  export default {
    name: 'BackButton',
  }
  </script>