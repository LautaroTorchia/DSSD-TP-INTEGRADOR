<template>
  <div>
    <div class="d-flex justify-content-end mb-3">
      <router-link :to="{ name: 'furniture-create' }" class="btn btn-primary">Crear mueble</router-link>
    </div>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">Nombre</th>
          <th scope="col">Descripción</th>
          <th scope="col">Días estimados</th>
          <th scope="col">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <template v-if="furniture.length">
          <template v-for="furnitureItem in furniture" :key="furnitureItem.id">
            <tr>
              <td>{{ furnitureItem.nombre }}</td>
              <td>{{ furnitureItem.descripcion }}</td>
              <td>{{ furnitureItem.plazo_fabricacion }} días</td>
              <td>
                <router-link
                  :to="{ name: 'furniture-detail', params: { collection: collectionId, id: furnitureItem.id } }"
                  class="btn btn-dark btn-sm">
                  Ver
                </router-link>
                <button v-if="!collection.designed" @click="deleteFurniture(furnitureItem.id)" class="btn btn-danger btn-sm">
                  Eliminar
                </button>
              </td>
            </tr>
          </template>
        </template>
        <tr v-else>
          <td colspan="4" class="text-center">
            <div v-if="furniture.loading" class="spinner-border spinner-border-sm"></div>
            <div v-else-if="furniture.error" class="text-danger mt-3">Error loading furniture: {{ furniture.error }}</div>
            <div v-else>No hay muebles en la colección</div>
          </td>
        </tr>
      </tbody>
    </table>
    <BackButton />
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useFurnitureStore, useCollectionsStore } from '@/stores';
import { router } from '@/helpers';
import BackButton from '@/components/BackButton.vue';
import { onBeforeMount, ref } from 'vue';

const furnitureStore = useFurnitureStore();
const collectionStore = useCollectionsStore();
const { collections } = storeToRefs(collectionStore);
const { furniture } = storeToRefs(furnitureStore);
const collectionId = router.currentRoute.value.params.collection;
const loading = ref(true);
const collection = ref({});

onBeforeMount(async () => {
  await furnitureStore.getCollectionFurniture(collectionId);
  collection.value = collections.value.find((collection) => collection.id == collectionId);
  loading.value = false;
});

const deleteFurniture = async (id) => {
  const confirmed = confirm('¿Desea borrar el mueble?');
  if (confirmed) {
    try {
      furnitureStore.delete(id);
    } catch (error) {
      alert('Error al borrar el mueble');
      console.error(error);
    }
  }
};
</script>
