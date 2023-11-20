<template>
    <div class="medium">
        <div v-if="loading" class="spinner"></div>
        <canvas id="myChart" ref="chart"></canvas>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBonitaVariable } from '@/helpers'

const chart = ref(null)
const loading = ref(true)


onMounted(async () => {

})
</script>
