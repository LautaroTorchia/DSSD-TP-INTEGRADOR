<script setup>
import { router } from "@/helpers";
import FurnitureForm from "./FurnitureForm.vue";
import { useFurnitureStore } from "@/stores";
import { ref } from "vue";
import Navbar from "@/components/Navbar.vue";

const loading = ref(false);

async function handleFormSubmission(formData) {
  let formObj = new FormData();
  formObj.append("nombre", formData.name);
  formObj.append("plazo_fabricacion", formData.estimated_days);
  formObj.append("fecha_lanzamiento_estimada", formData.estimated_release);
  formObj.append("descripcion", formData.description);
  formObj.append("materiales", formData.materials);
  formObj.append("plan_fabricacion", formData.manufacturing_plan);
  formObj.append("imagen", formData.image);
  let collectionId = router.currentRoute.value.params.collection;
  formObj.append("coleccion", collectionId);

  const furnitureStore = useFurnitureStore();
  loading.value = true;
  await furnitureStore.create(formObj);
  router.push({ name: "furniture", params: { collection: collectionId } });
}
</script>
<template>
  <Navbar />
  <div class="container pt-4 pb-4">
    <div>
      <div v-if="loading">
        <div class="spinner-border spinner-border-sm"></div>
        <h2 class="text-center">Creando mueble</h2>
      </div>
      <div v-else>
        <h2 class="text-center">Crear Mueble de la colección</h2>
        <FurnitureForm @form-submitted="handleFormSubmission" />
      </div>
    </div>
    <p class="text-center">
      <router-link :to="{ name: 'furniture' }" class="btn btn-secondary">
        Volver
      </router-link>
    </p>
  </div>
</template>
