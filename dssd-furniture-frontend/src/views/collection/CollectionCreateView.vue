<template>
  <Navbar />
  <div class="container pt-4 pb-4">
    <div>
      <h2 class="text-center">Crear Colección</h2>
      <CollectionForm @form-submitted="handleFormSubmission" />
      <p class="text-center">
        <router-link :to="{ name: 'collections' }" class="btn btn-secondary">
          Volver
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { router } from "../../helpers/router";
import CollectionForm from "./CollectionForm.vue";
import Navbar from "@/components/Navbar.vue"
import { useCollectionsStore } from "@/stores";

const formData = {
  name: "",
  description: "",
};

function handleFormSubmission(formData) {
  const collectionStore = useCollectionsStore();
  collectionStore.create(formData);
  router.push({ name: "collections" });
}
</script>
