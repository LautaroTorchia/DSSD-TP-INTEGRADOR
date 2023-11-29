<template>
  <div class="container d-flex justify-content-center align-items-center">
    <div class="card">
      <div class="card-body">
        <h1 class="card-title">
          Análisis de materiales de la coleccion {{ collectionName }}
        </h1>
        <div v-if="loading" class="spinner-border spinner-border-sm"></div>
        <div v-else>
          <form @submit.prevent="submitForm">
            <div v-for="(piece, index) in furniture" :key="index">
              <h2>Mueble: {{ piece.nombre }}</h2>
              <div v-for="(material, index) in piece.materiales" :key="index">
                <label>{{ material.nombre }}:</label>
                <input
                  type="number"
                  v-model="material.amount"
                  min="1"
                  class="form-control"
                />
                kg
              </div>
            </div>
            <button type="submit" class="btn btn-primary">Aceptar</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from "pinia";
import { useFurnitureStore, useMaterialsStore } from "@/stores";
import {
  router,
  advanceNamedBonitaTask,
  fetchWrapper,
  getBonitaVariable,
} from "@/helpers";
import { onMounted, ref } from "vue";

const baseUrl = `${import.meta.env.VITE_API_URL}`;

const furnitureStore = useFurnitureStore();
const materialsStore = useMaterialsStore();
const { furniture } = storeToRefs(furnitureStore);
const collectionId = router.currentRoute.value.params.collection;
const materialsAmount = ref([]);
const collectionName = ref("");
const caseId = JSON.parse(localStorage.getItem("collections")).collections.find(
  (collection) => collection.id == collectionId,
).caseId;
const loading = ref(true);

furnitureStore.getCollectionFurniture(collectionId);

try {
  collectionName.value = JSON.parse(
    localStorage.getItem("collections"),
  ).collections.find((collection) => collection.id == collectionId).name;
} catch (error) {
  console.error(error);
}

const submitForm = async () => {
  materialsAmount.value = [];

  furniture.value.forEach((piece) => {
    piece.materiales.forEach((material) => {
      const existingMaterial = materialsAmount.value.find(
        (m) => m.id === material.id,
      );
      if (existingMaterial) {
        existingMaterial.amount += material.amount;
      } else {
        materialsAmount.value.push({
          id: material.id,
          name: material.nombre,
          amount: material.amount,
        });
      }
    });
  });

  materialsAmount.value = materialsAmount.value.filter((material) => material); // delete empty slots

  const message = {};
  materialsAmount.value.forEach((material) => {
    message[material.name] = material.amount;
  });

  const confirmed = confirm(
    "Confirma estos materiales: \n" +
      Object.entries(message)
        .map(([material, amount]) => `${material}: ${amount}`)
        .join("\n"),
  );

  if (confirmed) {
    try {
      await fetchWrapper.put(
        `${baseUrl}/bonita/update-case-variable/${caseId}/cantidad_materiales/`,
        {
          type: "java.lang.String",
          value: JSON.stringify(materialsAmount.value),
        },
      );
      await advanceNamedBonitaTask(caseId, "Analizar materiales");
      router.push({ name: "fabrication-plan" });
    } catch (error) {
      console.error(error);
    }
  }
};

onMounted(async () => {
  const materials = await materialsStore.getAll();
  await furnitureStore.getCollectionFurniture(collectionId);
  furniture.value.forEach((piece) => {
    piece.materiales = piece.materiales.map((material) => Number(material));
    piece.materiales.forEach((materialId, index) => {
      const material = materials.find((m) => m.id == materialId);
      if (material) {
        piece.materiales[index] = { ...material, amount: 0 };
      }
    });
  });
  loading.value = false;
});
</script>
