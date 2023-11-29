<template>
  <nav v-show="authStore.user" class="navbar navbar-expand navbar-dark bg-dark">
    <div class="navbar-nav">
      <router-link to="/" class="nav-item nav-link">Home</router-link>
      <a @click="authStore.logout()" class="nav-item nav-link">Logout</a>
    </div>
  </nav>
</template>
<script setup>
import { useAuthStore } from "@/stores";
const authStore = useAuthStore();
</script>
