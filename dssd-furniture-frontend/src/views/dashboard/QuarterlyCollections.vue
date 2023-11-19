<script setup>
import { ref, onMounted, watch } from 'vue';
import { storeToRefs } from 'pinia';
import { useCollectionsStore } from '@/stores';
const collectionStore = useCollectionsStore();
const { collections } = storeToRefs(collectionStore);
const quarterCollections = ref([]);

const selectedQuarter = ref('');

const currentYear = new Date().getFullYear();

const generateQuarters = (startYear, endYear) => {
  const quarters = [];
  for (let i = startYear; i <= endYear; i++) {
    for (let j = 1; j <= 4; j++) {
      quarters.push(`Q${j} ${i}`);
    }
  }
  return quarters;
};

const quarters = generateQuarters(currentYear - 2, currentYear + 2);

onMounted(async () => {
  await collectionStore.getAll()
  collections.value.forEach(async (collection) => {
    const launchDate = new Date(collection.estimated_launch_date)
    collection.quarter = `Q${Math.floor((launchDate.getMonth() + 1) / 3) + 1} ${launchDate.getFullYear()}`;
  })
})

watch(selectedQuarter, (newQuarter) => {
  quarterCollections.value = collections.value.filter((collection) => collection.quarter == newQuarter);
});
</script>

<template>
  <div class="container text-center">
    <h1 class="text-center" style="font-size: 20px;">Seleccionar cuatrimestre</h1>
    <div class="d-flex justify-content-center">
      <select v-model="selectedQuarter" class="my-4 form-select" style="font-size: 16px;">
        <option v-for="quarter in quarters" :key="quarter" :value="quarter">{{ quarter }}</option>
      </select>
    </div>
    <h2 style="font-size: 18px;">Cantidad de colecciones para el cuatrimestre {{ selectedQuarter }}: {{
      quarterCollections.length }}</h2>
    <div style="height: 100px; overflow-y: auto;">
      <ul class="list-group">
        <li v-for="collection in quarterCollections" :key="collection.id" class="list-group-item"
          style="font-size: 14px;">{{ collection.name }}</li>
      </ul>
    </div>
  </div>
</template>

