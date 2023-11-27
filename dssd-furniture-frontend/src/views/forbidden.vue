<template>
    <div class="container mt-5">
      <div class="card">
        <div class="card-header bg-secondary text-white">
          <h2>Acceso Prohibido (403)</h2>
        </div>
        <div class="card-body">
          <p class="card-text">
            ¡Ops! No tienes permisos para acceder a esta página.
          </p>
          <p class="card-text">
            Por favor, contacta a tu administrador si crees que esto es un error.
          </p>
        </div>
        <div class="card-footer">
          <router-link to="/" class="btn btn-primary">Ir a la Página Principal</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ForbiddenPage'
  };
  </script>
  
  <style scoped>
  .card {
    border: 1px solid #ccc;
    border-radius: 8px;
    margin: 0 auto;
    max-width: 400px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .card-header {
    padding: 15px;
  }
  
  .card-body {
    padding: 15px;
  }
  
  .card-footer {
    background-color: #f8f9fa;
    border-top: 1px solid #ccc;
    padding: 15px;
    text-align: center;
  }
  </style>
  