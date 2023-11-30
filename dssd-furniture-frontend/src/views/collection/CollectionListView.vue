<script setup>
import { ref, onMounted } from "vue";
import { storeToRefs } from "pinia";
import { useCollectionsStore, useFurnitureStore } from "@/stores";
import Navbar from "@/components/Navbar.vue";

const collectionStore = useCollectionsStore();
const furnitureStore = useFurnitureStore();
const loading = ref(true);

const { collections } = storeToRefs(collectionStore);

const orderedCollections = ref([]);

onMounted(async () => {
  await collectionStore.getAll();
  collections.value.forEach(async (collection) => {
    const furniture = await furnitureStore.getCollectionFurniture(
      collection.id,
    );
    collection.hasFurniture = !!furniture.length;
  });
  orderedCollections.value = orderCollections(collections.value);
  loading.value = false;
});

function orderCollections(collections) {
  return collections.slice().sort((a, b) => {
    if (a.designed !== b.designed) {
      return a.designed ? 1 : -1;
    } else {
      return new Date(b.fecha_creacion) - new Date(a.fecha_creacion);
    }
  });
}

const deleteCollection = async (id) => {
  const confirmed = confirm("¿Desea borrar la colección?");
  if (confirmed) {
    try {
      await collectionStore.delete(id);
    } catch (error) {
      alert("Error al borrar la colección");
      console.error(error);
    }
  }
};

const finishCollection = async (collection) => {
  const confirmed = confirm("¿Desea terminar la colección?");
  if (confirmed) {
    try {
      if (!collection.hasFurniture) {
        alert("No se puede terminar una colección sin muebles");
        return;
      }
      await collectionStore.finish(collection);
    } catch (error) {
      alert("Error al terminar la colección");
      console.error(error);
    }
  }
};
</script>

<template>
  <Navbar />
  <div class="container pt-4 pb-4">
    <div v-if="collections.loading" class="spinner-border spinner-border-sm"></div>
    <div v-else class="container mt-4">
      <div class="mb-3 d-flex justify-content-end">
        <router-link :to="{ name: 'collection-create' }" class="btn btn-primary">Crear colección</router-link>
      </div>
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Descripción</th>
            <th scope="col">Fecha de lanzamiento estimada</th>
            <th scope="col">Terminada</th>
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="orderedCollections.length">
            <template v-for="(collection, index) in orderedCollections" :key="collection.id">
              <tr :style="{
                'background-color': index % 2 === 0 ? '#fff' : '#000',
                color: index % 2 === 0 ? '#000' : '#fff',
              }">
                <td>
                  <strong>{{ collection.name }}</strong>
                </td>
                <td>{{ collection.description }}</td>
                <td>{{ collection.estimated_launch_date }}</td>
                <td>{{ collection.designed ? "Sí" : "No" }}</td>
                <td>
                  <router-link :to="`/${collection.id}/furniture`" class="btn btn-dark btn-sm">Ver Muebles</router-link>
                  <button v-if="!collection.designed" @click="deleteCollection(collection.id)"
                    class="btn btn-danger btn-sm ml-1">
                    Borrar
                  </button>
                  <button v-if="!collection.designed" @click="finishCollection(collection)"
                    class="btn btn-success btn-sm ml-1">
                    Terminar
                  </button>
                </td>
              </tr>
            </template>
          </template>
          <tr v-else>
            <td colspan="5" class="text-center">
              <div v-if="collections.loading" class="spinner-border spinner-border-sm"></div>
              <div v-else-if="collections.error" class="text-danger mt-3">
                Error loading collections: {{ collections.error }}
              </div>
              <div v-else>No hay nada</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
