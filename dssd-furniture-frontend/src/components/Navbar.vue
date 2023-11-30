<template>
  <nav v-show="authStore.user" class="navbar navbar-expand navbar-dark bg-dark">
    <div class="navbar-nav">
      <router-link to="/" class="nav-item nav-link">Home</router-link>
      <router-link v-if="role.some(r => ['admin','designer'].includes(r))" :to="{ name: 'collections' }" class="nav-item nav-link">Ver Colecciones</router-link>
      <router-link v-if="role.some(r => ['admin','operations_analist'].includes(r))" :to="{ name: 'designed-collections' }" class="nav-item nav-link">Analizar materiales</router-link>
      <router-link v-if="role.some(r => ['admin','commercial_analist'].includes(r))" :to="{ name: 'delivery-order-collection-list' }" class="nav-item nav-link">Ordenes de entrega</router-link>
      <router-link v-if="role.some(r => ['admin','factory_liason'].includes(r))" :to="{ name: 'fabrication-control-list' }" class="nav-item nav-link">Controlar fabricación</router-link>
      <router-link v-if="role.some(r => ['admin','operations_analist'].includes(r))" :to="{ name: 'distribution-list' }" class="nav-item nav-link">Distribución interna</router-link>
      <router-link v-if="role.some(r => ['admin','commercial_analist'].includes(r))" :to="{ name: 'associate-lots-list' }" class="nav-item nav-link">Asociar lotes</router-link>
      <a @click="authStore.logout()" class="nav-item nav-link">Logout</a>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from "@/stores";
import { ref } from "vue";
const authStore = useAuthStore();

const role = ref(authStore.user?.role);
</script>
