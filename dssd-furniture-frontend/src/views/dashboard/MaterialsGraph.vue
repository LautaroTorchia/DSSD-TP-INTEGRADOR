<template>
    <div class="medium">
        <div v-if="loading" class="spinner"></div>
        <canvas id="myChart" ref="chart"></canvas>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import Chart from 'chart.js/auto'
import { useFurnitureStore } from '@/stores'
import { fetchWrapper } from '@/helpers'

const chart = ref(null)
const loading = ref(true)
const furnitureStore = useFurnitureStore()
const { furniture } = storeToRefs(furnitureStore)

const proveedoresUrl = `${import.meta.env.VITE_API_PROVEEDORES_URL}`

onMounted(async () => {
    await furnitureStore.getAll()
    await fetchWrapper.get
    const materialsData = {}

    furniture.value.forEach((furniturePiece) => {

        furniturePiece.materiales.forEach((material) => {
            if (materialsData[material]) {
                materialsData[material] += 1
            } else {
                materialsData[material] = 1
            }
        })
    })
    const materialsNameList = await fetchWrapper.get(proveedoresUrl+'/proveedores/materiales/')

    const materialLabels = Object.keys(materialsData).map((materialKey) => {
        const material = materialsNameList.find((m) => m.id == materialKey)
        return material.nombre 
    })
    const materialValues = Object.values(materialsData)

    const ctx = document.getElementById('myChart');

    const chartElem = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: materialLabels,
            datasets: [{
                label: 'Cantidad de muebles que usaron el material',
                data: materialValues,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Proporcion de materiales totales usados en los muebles'
                },
            }
        }
    });
    chart.value = chartElem
    loading.value = false
})
</script>

<style>
.medium {
    width: 50%;
    margin: auto;
}

.spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #7983ff;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
</style>
