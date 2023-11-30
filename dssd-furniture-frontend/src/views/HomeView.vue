<script setup>
import { storeToRefs } from "pinia";
import Navbar from "@/components/Navbar.vue";
import { useAuthStore } from "@/stores";
import { Dashboard } from "@/views";

const authStore = useAuthStore();
const { user: authUser } = storeToRefs(authStore);
</script>

<template>
  <Navbar />
  <div class="container pt-4 pb-4">
    <div>
      <h1 class="text-center">GlobalFurniture-LJJ Muebles</h1>
      <h2 class="text-center">Hola {{ authUser?.username }}!</h2>
      <Dashboard />
    </div>
  </div>
</template>
