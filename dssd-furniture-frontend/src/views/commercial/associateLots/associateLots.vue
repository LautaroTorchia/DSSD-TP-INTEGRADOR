<template>
    <Navbar />
  <div class="container pt-4 pb-4">
  <div v-if="!loading" class="container">
    <div class="card shadow p-3 mb-5 bg-white rounded">
      <h2 class="card-title">Órdenes</h2>
      <div class="card-body">
        <form @submit.prevent="submit">
          <div class="row">
            <div
              v-for="(order, index) in orders"
              :key="order.id"
              class="col-md-3"
            >
              <div class="card mb-3" :style="{ flex: cardFlex }">
                <div class="card-body" style="text-align: center">
                  <h6 class="card-title">Orden: {{ order.id }}</h6>
                  <p>Vendedor final: {{ order.vendedor_final }}</p>
                  <div v-if="order.lot">
                    <p>Lote seleccionado: {{ order.lot.id }}</p>
                    <p>Lugar de distribución: {{ order.lot.distPlace }}</p>
                  </div>

                  <select
                    v-else
                    v-model="order.lot"
                    @change="updateLots(order)"
                    class="form-select"
                  >
                    <option
                      v-for="lot in availableLots"
                      :key="lot.id"
                      :value="lot"
                    >
                      Lote {{ lot.id }} Centro de distribucion
                      {{ lot.distPlace }}
                    </option>
                  </select>
                  <button @click="clearLot(order)" class="btn btn-danger">
                    Clear
                  </button>
                </div>
              </div>
            </div>
          </div>
          <button type="submit" class="btn btn-primary">Enviar</button>
        </form>
      </div>
    </div>
  </div>
  <div v-else class="spinner-border"></div>
</div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import Navbar from "@/components/Navbar.vue";
import {
  fetchWrapper,
  router,
  advanceNamedBonitaTaskWithCollection,
} from "@/helpers";

const baseUrl = `${import.meta.env.VITE_API_URL}`;
const collectionId = router.currentRoute.value.params.collection;
const orders = ref([]);
const lots = ref([]);
const loading = ref(true);
const availableLots = ref([]);
const cardFlex = ref("1"); // Added cardFlex

onMounted(async () => {
  const ordersPromise = fetchWrapper.get(`${baseUrl}/entregas/ordenes/`);
  const lotsPromise = fetchWrapper.get(`${baseUrl}/entregas/lotes-fabricados/`);
  const distPromise = fetchWrapper.get(
    `${baseUrl}/entregas/distribucion-de-lote/`,
  );
  const distPlacesPromise = fetchWrapper.get(
    `${baseUrl}/entregas/lugares-de-distribucion/`,
  );
  const finalSellersPromise = fetchWrapper.get(
    `${baseUrl}/entregas/vendedores-finales/`,
  );

  const allOrders = await ordersPromise;
  const allLots = await lotsPromise;
  orders.value = allOrders
    .filter((order) => order.id_coleccion == collectionId)
    .map((order) => ({ ...order, lot: null }));
  lots.value = allLots.filter((lot) => lot.coleccion == collectionId);
  availableLots.value = lots.value;

  const finalSellers = await finalSellersPromise;
  orders.value.map((order) => {
    order.vendedor_final = finalSellers.find(
      (seller) => seller.id == order.vendedor_final,
    ).nombre;
  });
  const distPlaces = await distPlacesPromise;
  const dist = await distPromise;
  lots.value.forEach((lot) => {
    lot.distPlace = distPlaces.find(
      (place) => place.id == dist.find((d) => d.lote == lot.id).distribucion,
    ).nombre;
  });
  loading.value = false;
});

const updateLots = (order) => {
  availableLots.value = availableLots.value.filter(
    (lot) => lot.id != order.lot.id,
  );
};

const clearLot = (order) => {
  const lot = lots.value.find((lot) => lot.id == order.lot.id);
  availableLots.value.push(lot);
  availableLots.value.sort((a, b) => a.id - b.id);
  order.lot = null;
};

const submit = async () => {
  loading.value = true;
  const promiseList = [];
  orders.value.forEach((order) => {
    const data = {
      orden_entrega: order.id,
      lote: order.lot.id,
    };
    promiseList.push(
      fetchWrapper.post(`${baseUrl}/entregas/orden-de-lote/`, data),
    );
  });
  await Promise.all(promiseList);
  loading.value = false;
  await advanceNamedBonitaTaskWithCollection(
    collectionId,
    "Asociar lotes a orden de entrega",
  );
  alert("Lotes asociados correctamente");
  router.push({ name: "home" });
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  border-radius: 10px;
  margin: 0;
}

.card-title {
  text-align: center;
}

.card-body {
  margin: 0;
  padding: 0;
  text-align: center;
}

.form-select {
  width: 100%;
}

.btn {
  margin-top: 10px;
}

.row {
  display: flex;
  /* Added */
}

.card.mb-3 {
  flex: 1;
  /* Added */
}
</style>
