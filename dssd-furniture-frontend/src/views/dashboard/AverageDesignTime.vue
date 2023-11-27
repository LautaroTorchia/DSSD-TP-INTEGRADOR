<template>
    <div v-if="loading" class="spinner"></div>
    <div :style="{visibility : hiddenVisibility}">
        <div class="chart-container" style="position: relative; height:40vh; width:30vw">
            <h4 class="text-center">Tiempo promedio de diseño: {{ averageDesignTime }} dias</h4>
            <canvas id="AverageDesignTimeChart" ref="chart"></canvas>
        </div>
    </div>
    
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCollectionsStore } from '@/stores'
import { storeToRefs } from 'pinia'
import { fetchWrapper } from '@/helpers'
import Chart from 'chart.js/auto'

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)
const base_url = `${import.meta.env.VITE_API_URL}`

const averageDesignTime = ref(0)
const chart = ref(null)
const loading = ref(true)
const hiddenVisibility = ref("hidden")

const getTasks = async () => {
    let bonitaTasks = []
    if (!localStorage.getItem("bonitaTasks")){
        bonitaTasks = await fetchWrapper.get(`${base_url}/bonita/archived-tasks/`)
        localStorage.setItem("bonitaTasks", JSON.stringify(bonitaTasks))
    }else{
        bonitaTasks = JSON.parse(localStorage.getItem("bonitaTasks"))
    }
    return bonitaTasks
}

const filterTasks = async (taskName) => {
    const bonitaTasks = await getTasks()
    return bonitaTasks.filter(task => task.name === taskName )
}

const getArchivedTasks = async (collectionList, taskName) => {
    const bonitaTasks = await filterTasks(taskName)
    return bonitaTasks.map(task => {
        const collection = collectionList.find(collection => collection.caseId == task.caseId)
        if (!collection) {
            return undefined
        }
        return {
            caseId: task.caseId,
            name: collection.name,
            created_at: collection.created_at,
            reached_state_date: task.archivedDate
        }
    }).filter(task => task !== undefined)
}
onMounted(async () => {
    await collectionStore.getAll()
    const filteredCollections =  collections.value.filter((collection) => {
        return collection.designed 
    })
    
    let designTimeList = await getArchivedTasks(filteredCollections, "Diseñar coleccion")
    

    designTimeList = designTimeList.map(designTime => {
        const created_at = new Date(designTime.created_at)
        const reached_state_date = new Date(designTime.reached_state_date)
        const diffTime = Math.abs(reached_state_date - created_at)
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
        return {
            caseId: designTime.caseId,
            name: designTime.name,
            designTime: diffDays
        }
    })
    if (planTimeList.length === 0) {
        loading.value = false
        hiddenVisibility.value = ""
        return
    }
    averageDesignTime.value = designTimeList.reduce((sum, designTime) => sum + designTime.designTime, 0) / designTimeList.length

    chart.value = new Chart(document.getElementById('AverageDesignTimeChart'), {
        type: 'bar',
        data: {
            labels: designTimeList.map(designTime => designTime.name),
            datasets: [{
                label: 'Tiempo de diseño (días)',
                data: designTimeList.map(designTime => designTime.designTime),
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
                    text: 'Tiempo de diseño por colección'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: designTimeList.reduce((max, designTime) => {
                        const designTimeMonths = Math.ceil(designTime.designTime)
                        return designTimeMonths > max ? designTimeMonths : max;
                    }, 0),
                    ticks: {
                        stepSize: 1
                    }
                },
            }
        }
    })

    loading.value = false
    hiddenVisibility.value = ""
})


</script>
