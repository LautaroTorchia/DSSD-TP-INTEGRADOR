<template>
  <Navbar />
  <div class="container pt-4 pb-4">
    <div>
      <h1>Confirmar plan de fabricación</h1>
      <div v-if="loading">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div v-else>
        <div class="row">
          <div class="col-md-6">
            <div class="card mb-4 shadow">
              <div v-if="fabricationPlan.factory_slot" class="card-body">
                <h2 class="card-title">Factory Slot</h2>
                <p class="card-text">
                  Factory: {{ fabricationPlan.factory_slot.factory }}
                </p>
                <p class="card-text">
                  Start Date: {{ fabricationPlan.factory_slot.slot_start_date }}
                </p>
                <p class="card-text">
                  End Date: {{ fabricationPlan.factory_slot.slot_end_date }}
                </p>
                <p class="card-text">
                  Cantidad de lotes: {{ fabricationPlan.lotQuantity }}
                </p>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card mb-4 shadow">
              <div class="card-body">
                <h2 class="card-title">Materials</h2>
                <div class="overflow-auto" style="max-height: 400px">
                  <div v-for="(material, index) in fabricationPlan.materials" :key="index" class="card mb-2 shadow">
                    <div class="card-body">
                      <p class="card-text">Actor: {{ material.actor }}</p>
                      <p class="card-text">Material: {{ material.material }}</p>
                      <p class="card-text">Amount: {{ material.amount }}</p>
                      <p class="card-text">
                        Delivery Date: {{ material.deliveryDate }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <button class="btn btn-primary" @click="submitForm">Confirmar</button>
          <button class="btn btn-primary" @click="cancelPlan">Cancelar</button>
        </div>
      </div>
    </div>
    <p class="text-center">
      <router-link :to="{ name: 'designed-collections' }" class="btn btn-secondary">
        Volver
      </router-link>
    </p>
  </div>
</template>

<script setup>
import {
  getBonitaVariable,
  router,
  advanceNamedBonitaTask,
  fetchWrapper,
  setBonitaVariable,
} from "@/helpers";
import Navbar from "@/components/Navbar.vue";
import { onBeforeMount, ref } from "vue";

const baseUrl = `${import.meta.env.VITE_API_URL}`;
const collectionId = router.currentRoute.value.params.collection;
const caseId = JSON.parse(localStorage.getItem("collections")).collections.find(
  (collection) => collection.id == collectionId,
).caseId;
const fabricationPlan = ref({});
const loading = ref(true);

async function submitForm() {
  loading.value = true;
  try {
    await advanceNamedBonitaTask(caseId, "Armar plan de fabricacion");
    await placeOrders(fabricationPlan.value);
    router.push({ name: "designed-collections" });
  } catch (error) {
    console.error(error);
  }
}

async function placeMateriallOrders(materials) {
  for (const material of materials) {
    const payload = {
      id_venta_proveedor: material.actor,
      cantidad_pactada: material.amount,
      sede_entrega: fabricationPlan.value.factory_slot.factory,
      id_coleccion: collectionId,
      fecha_entrega_pactada: material.deliveryDate,
    };
    fetchWrapper.post(`${baseUrl}/reservas/reservar-material/`, payload);
  }
}

async function placeFactorySlotOrder(factorySlot) {
  const payload = {
    lugar_de_fabricacion: factorySlot.factory,
    fecha_inicio_reserva: factorySlot.slot_start_date,
    fecha_fin_reserva: factorySlot.slot_end_date,
    coleccion: collectionId,
  };
  fetchWrapper.post(
    `${baseUrl}/reservas/reservas-lugares-fabricacion/`,
    payload,
  );
}

async function placeOrders(fabricationPlan) {
  try {
    placeMateriallOrders(fabricationPlan.materials);
    await advanceNamedBonitaTask(caseId, "Reservar materiales necesarios");
  } catch (error) {
    throw error;
  }
  try {
    placeFactorySlotOrder(fabricationPlan.factory_slot);
    await advanceNamedBonitaTask(caseId, "Reservar espacio de fabricación");
  } catch (error) {
    throw error;
  }
}

function cancelPlan() {
  confirm("¿Está seguro que desea cancelar el plan de fabricación?");
  if (confirm) {
    setBonitaVariable(caseId, "plan_de_fabricacion", "");
    router.push({ name: "fabrication-plan" });
  }
}

onBeforeMount(async () => {
  fabricationPlan.value = await getBonitaVariable(
    caseId,
    "plan_de_fabricacion",
  );
  fabricationPlan.value = JSON.parse(fabricationPlan.value);
  loading.value = false;
});
</script>

<style>
.btn-primary {
  background-color: blue;
  color: white;
}
</style>
