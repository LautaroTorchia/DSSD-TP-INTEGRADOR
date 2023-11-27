<template>
    <div v-if="loading" class="spinner"></div>
    <div :style="{visibility : hiddenVisibility}">
        <div class="chart-container" style="position: relative; height:40vh; width:30vw">
            <h4 class="text-center">Tiempo promedio de fabricacion y distribucion: {{ averagePlanTime }} dias</h4>
            <canvas id="AverageFabricationAndDistributionTime" ref="chart"></canvas>
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

const averagePlanTime = ref(0)
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
    
    const designTimeList = await getArchivedTasks(filteredCollections, "Reservar espacio de fabricación")
    const fabricationOrderList = await getArchivedTasks(filteredCollections, "Asociar lotes a orden de entraga")

    const matchingItems = designTimeList.filter(designItem => {
        return fabricationOrderList.some(fabricationItem => fabricationItem.caseId === designItem.caseId)
    }).concat(fabricationOrderList.filter(fabricationItem => {
        return designTimeList.some(designItem => designItem.caseId === fabricationItem.caseId)
    }))

    
    const dupPlanTimeList = matchingItems.map(item => {
        const designTime = designTimeList.find(designItem => designItem.caseId === item.caseId)
        const fabricationTime = fabricationOrderList.find(fabricationItem => fabricationItem.caseId === item.caseId)
        return {
            name: item.name,
            caseId: item.caseId,
            planTime: Math.ceil((new Date(fabricationTime.reached_state_date) - new Date(designTime.reached_state_date)) / (1000 * 60 * 60 * 24))
        }
    })

    const planTimeList = Array.from(new Set(dupPlanTimeList.map(planTime => planTime.caseId)))
    .map(caseId => {
        return dupPlanTimeList.find(planTime => planTime.caseId === caseId)
    })

    if (planTimeList.length === 0) {
        loading.value = false
        return
    }
    averagePlanTime.value = planTimeList.reduce((sum, planTime) => sum + planTime.planTime, 0) / planTimeList.length

    chart.value = new Chart(document.getElementById('AverageFabricationAndDistributionTime'), {
        type: 'bar',
        data: {
            labels: planTimeList.map(planTime => planTime.name),
            datasets: [{
                label: 'Tiempo de planeamiento (días)',
                data: planTimeList.map(planTime => planTime.planTime),
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
                    text: 'Tiempo de planeamiento por colección'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: planTimeList.reduce((max, planTime) => {
                        const planTimeMonths = Math.ceil(planTime.planTime)
                        return planTimeMonths > max ? planTimeMonths : max;
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
