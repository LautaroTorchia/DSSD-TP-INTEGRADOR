<template>
  <Navbar />
  <div class="container pt-4 pb-4">
    <div>
      <h1>Asociar distribucion interna</h1>
      <div v-if="!loading">
        <ul v-for="collection in showCollections" :key="collection.id" class="list-group">
          <li class="list-group-item">
            <div class="d-flex justify-content-between align-items-center">
              <span>{{ collection.name }}</span>
              <router-link :to="{
                name: 'distribution-create',
                params: { collection: collection.id },
              }" class="btn btn-primary">
                <slot>Asociar lotes</slot>
              </router-link>
            </div>
          </li>
        </ul>
      </div>
      <div v-else-if="loading" class="spinner-border spinner-border-sm"></div>
      <div v-else-if="collections.error" class="text-danger">
        Error loading collections: {{ collections.error }}
      </div>
      <div v-else>No hay nada</div>
    </div>
    <p class="text-center">
      <router-link :to="{ name: 'home' }" class="btn btn-secondary">
        Volver
      </router-link>
    </p>
  </div>
</template>

<script setup>
import { storeToRefs } from "pinia";
import { useCollectionsStore } from "@/stores";
import { fetchWrapper } from "@/helpers";
import { ref, onMounted } from "vue";
import Navbar from "@/components/Navbar.vue";

const baseUrl = `${import.meta.env.VITE_API_URL}`;

const collectionStore = useCollectionsStore();
const { collections } = storeToRefs(collectionStore);
const showCollections = ref([]);
const loading = ref(true);

onMounted(async () => {
  let distributions = fetchWrapper.get(
    `${baseUrl}/entregas/distribucion-de-lote/`,
  );
  let lots = fetchWrapper.get(`${baseUrl}/entregas/lotes-fabricados/`);
  await collectionStore.getAll();
  showCollections.value = collections.value.filter((collection) => {
    return collection.fabricated;
  });
  distributions = await distributions;
  lots = await lots;
  showCollections.value = showCollections.value.filter((collection) => {
    let lotsDistributed = lots.filter((lot) => {
      return distributions.some((distribution) => {
        return distribution.lote == lot.id;
      });
    });
    let distributed = lotsDistributed.some(
      (lot) => lot.coleccion == collection.id,
    );
    return !distributed;
  });
  loading.value = false;
});
</script>
