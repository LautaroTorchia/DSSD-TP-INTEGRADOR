<template>
  <div class="app-container bg-light">
    <Navbar />
    <div class="container pt-4 pb-4">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import Navbar from "@/components/NavBar.vue";
</script>

<style>
@import "@/assets/base.css";
</style>
