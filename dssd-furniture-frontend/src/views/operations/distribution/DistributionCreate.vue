<template>
  <form @submit.prevent="submitForm">
    <div v-if="!loading">
      <h2>Distribuir lotes: {{ collection.name }}</h2>
      <div v-for="lot in lots" :key="lot.id">
        <div class="card">
          <div class="card-header">Lote {{ lot.id }}</div>
          <div class="card-body">
            <label for="distributor">Lugar de distribución:</label>
            <select v-model="lot.distributor" id="distributor">
              <option
                v-for="distributor in distributors"
                :key="distributor.id"
                :value="distributor.id"
              >
                {{ distributor.nombre }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <p class="text-danger text-center">{{ submitError }}</p>
      <div class="submit-container">
        <button type="submit" class="btn btn-primary">Submit</button>
        <button type="button" class="btn btn-secondary" @click="clearForm">
          Clear
        </button>
      </div>
    </div>
    <div v-else class="spinner-border text-primary" role="status"></div>
  </form>
</template>

<style>
.submit-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.btn-secondary {
  margin-left: 10px;
}
</style>

<script setup>
import { ref, onMounted } from "vue";
import {
  router,
  fetchWrapper,
  advanceNamedBonitaTaskWithCollection,
} from "@/helpers";
import { storeToRefs } from "pinia";
import { useCollectionsStore } from "@/stores";

const collectionId = router.currentRoute.value.params.collection;
const collectionStore = useCollectionsStore();
const { collections } = storeToRefs(collectionStore);
const baseUrl = `${import.meta.env.VITE_API_URL}`;

const lots = ref([]);
const distributors = ref([]);
const collection = ref(null);
const loading = ref(true);
const submitError = ref("");

onMounted(async () => {
  const lotsPromise = fetchWrapper.get(`${baseUrl}/entregas/lotes-fabricados/`);
  const distributorsPromise = fetchWrapper.get(
    `${baseUrl}/entregas/lugares-de-distribucion/`,
  );
  await collectionStore.getAll();
  collection.value = collections.value.find(
    (collection) => collection.id == collectionId,
  );
  lots.value = (await lotsPromise).filter(
    (lot) => lot.coleccion == collectionId,
  );
  distributors.value = await distributorsPromise;
  loading.value = false;
});

const checkAllFieldsFull = () => {
  return lots.value.every((lot) => lot.distributor);
};

const setErrors = (errorString) => {
  submitError.value = errorString;
};

const postDistributions = async (lots) => {
  let distpost = new Promise(() => {});
  lots.forEach((lot) => {
    const distribution = {
      lote: lot.id,
      distribucion: lot.distributor,
    };
    distpost = fetchWrapper.post(
      `${baseUrl}/entregas/distribucion-de-lote/`,
      distribution,
    );
  });
  await distpost;
};

const submitForm = async () => {
  if (!checkAllFieldsFull()) {
    setErrors("Por favor, rellene todos los campos");
    return;
  } else {
    setErrors("");
  }
  await postDistributions(lots.value);
  await advanceNamedBonitaTaskWithCollection(
    collectionId,
    "Distribuir colección",
  );
  router.push({ name: "distribution-list" });
};

const clearForm = () => {
  lots.value.forEach((lot) => (lot.distributor = null));
};
</script>
