<template>
  <Navbar />
  <div class="container pt-4 pb-4">
    <div>
      <h1>Asociar ordenes de colecciones:</h1>
      <div v-if="!loading">
        <ul v-for="collection in showCollections" :key="collection.id" class="list-group">
          <li class="list-group-item">
            <div class="d-flex justify-content-between align-items-center">
              <span>{{ collection.name }}</span>
              <router-link :to="{
                name: 'associate-lots',
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
  const ordersPromise = fetchWrapper.get(`${baseUrl}/entregas/ordenes/`);
  const lotOrderPromise = fetchWrapper.get(
    `${baseUrl}/entregas/orden-de-lote/`,
  );
  await collectionStore.getAll();
  showCollections.value = collections.value.filter(
    (collection) => collection.fabricated,
  );
  const orders = await ordersPromise;
  const lotOrders = await lotOrderPromise;
  showCollections.value = showCollections.value.filter((collection) => {
    const order = orders.find((order) => order.id_coleccion == collection.id);
    if (!order) return false;
    const lotOrder = lotOrders.find(
      (lotOrder) => lotOrder.orden_entrega == order.id,
    );
    if (lotOrder) return false;
    return true;
  });
  loading.value = false;
});
</script>
