<template>
  <div>
    <h1>Plan de Fabricacion</h1>
    <p>{{ planDeFabricacion }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getBonitaVariable } from '@/helpers';

const planDeFabricacion = ref('');

onMounted(async () => {
  const caseId = 123; // Replace with the actual case ID
  planDeFabricacion.value = await getBonitaVariable(caseId, 'plan_de_fabricacion');
});
</script>
