<template>
     <div class="chart-container" style="position: relative; height:40vh; width:30vw">
        <div v-if="loading" class="spinner"></div>
        <h4 class="text-center">Tiempo promedio de diseño: {{ averageDesignTime }} dias</h4>
        <canvas id="AverageDesignTimeChart" ref="chart"></canvas>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCollectionsStore } from '@/stores'
import { storeToRefs } from 'pinia'
import Chart from 'chart.js/auto'

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)

const averageDesignTime = ref(0)
const chart = ref(null)
const loading = ref(true)

onMounted(async () => {
    await collectionStore.getAll()
    let designTimeList = bonitaTasks.filter(task => task.name === "Diseñar coleccion").map(task => {
        const collection = collections.value.find(collection => collection.caseId == task.caseId)
        return {
            caseId: task.caseId,
            name: collection.name,
            created_at: collection.created_at,
            reached_state_date: task.archivedDate
        }
    })

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
})

const bonitaTasks = [{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 20:44:01.281","rootContainerId":"73","assigned_date":"2023-11-20 20:44:01.245","displayName":"Analizar materiales","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"244","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"73","name":"Analizar materiales","reached_state_date":"2023-11-20 20:44:01.272","rootCaseId":"73","id":"315","state":"completed","parentCaseId":"73","last_update_date":"2023-11-20 20:44:01.272","assigned_id":"3"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 21:04:54.633","rootContainerId":"76","assigned_date":"2023-11-20 21:04:54.609","displayName":"Analizar materiales","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"260","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"76","name":"Analizar materiales","reached_state_date":"2023-11-20 21:04:54.620","rootCaseId":"76","id":"344","state":"completed","parentCaseId":"76","last_update_date":"2023-11-20 21:04:54.620","assigned_id":"3"},{"displayDescription":"","executedBy":"1","archivedDate":"2023-11-20 21:33:52.057","rootContainerId":"75","assigned_date":"2023-11-20 21:33:52.027","displayName":"Analizar materiales","executedBySubstitute":"1","dueDate":"","description":"","sourceObjectId":"273","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"75","name":"Analizar materiales","reached_state_date":"2023-11-20 21:33:52.047","rootCaseId":"75","id":"371","state":"completed","parentCaseId":"75","last_update_date":"2023-11-20 21:33:52.047","assigned_id":"1"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 20:45:45.595","rootContainerId":"73","assigned_date":"2023-11-20 20:45:45.577","displayName":"Armar plan de fabricacion","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"246","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"73","name":"Armar plan de fabricacion","reached_state_date":"2023-11-20 20:45:45.590","rootCaseId":"73","id":"320","state":"completed","parentCaseId":"73","last_update_date":"2023-11-20 20:45:45.590","assigned_id":"3"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 21:06:12.020","rootContainerId":"76","assigned_date":"2023-11-20 21:06:12.006","displayName":"Armar plan de fabricacion","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"262","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"76","name":"Armar plan de fabricacion","reached_state_date":"2023-11-20 21:06:12.015","rootCaseId":"76","id":"349","state":"completed","parentCaseId":"76","last_update_date":"2023-11-20 21:06:12.015","assigned_id":"3"},{"displayDescription":"","executedBy":"1","archivedDate":"2023-11-20 22:02:07.314","rootContainerId":"75","assigned_date":"2023-11-20 22:02:07.268","displayName":"Armar plan de fabricacion","executedBySubstitute":"1","dueDate":"","description":"","sourceObjectId":"275","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"75","name":"Armar plan de fabricacion","reached_state_date":"2023-11-20 22:02:07.296","rootCaseId":"75","id":"376","state":"completed","parentCaseId":"75","last_update_date":"2023-11-20 22:02:07.296","assigned_id":"1"},{"displayDescription":"","executedBy":"0","archivedDate":"2023-11-20 20:44:02.200","rootContainerId":"73","displayName":"Consultar API de proveedores","executedBySubstitute":"0","description":"","sourceObjectId":"245","type":"AUTOMATIC_TASK","processId":"9073786231475008302","caseId":"73","name":"Consultar API de proveedores","reached_state_date":"2023-11-20 20:44:02.189","rootCaseId":"73","id":"317","state":"completed","parentCaseId":"73","last_update_date":"2023-11-20 20:44:02.189"},{"displayDescription":"","executedBy":"0","archivedDate":"2023-11-20 21:04:55.195","rootContainerId":"76","displayName":"Consultar API de proveedores","executedBySubstitute":"0","description":"","sourceObjectId":"261","type":"AUTOMATIC_TASK","processId":"9073786231475008302","caseId":"76","name":"Consultar API de proveedores","reached_state_date":"2023-11-20 21:04:55.189","rootCaseId":"76","id":"346","state":"completed","parentCaseId":"76","last_update_date":"2023-11-20 21:04:55.189"},{"displayDescription":"","executedBy":"0","archivedDate":"2023-11-20 21:33:52.621","rootContainerId":"75","displayName":"Consultar API de proveedores","executedBySubstitute":"0","description":"","sourceObjectId":"274","type":"AUTOMATIC_TASK","processId":"9073786231475008302","caseId":"75","name":"Consultar API de proveedores","reached_state_date":"2023-11-20 21:33:52.613","rootCaseId":"75","id":"373","state":"completed","parentCaseId":"75","last_update_date":"2023-11-20 21:33:52.613"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 20:55:44.048","rootContainerId":"73","assigned_date":"2023-11-20 20:55:44.021","displayName":"Controlar entrega de materiales","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"253","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"73","name":"Controlar entrega de materiales","reached_state_date":"2023-11-20 20:55:44.039","rootCaseId":"73","id":"335","state":"completed","parentCaseId":"73","last_update_date":"2023-11-20 20:55:44.039","assigned_id":"3"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 21:06:57.365","rootContainerId":"76","assigned_date":"2023-11-20 21:06:57.351","displayName":"Controlar entrega de materiales","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"269","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"76","name":"Controlar entrega de materiales","reached_state_date":"2023-11-20 21:06:57.360","rootCaseId":"76","id":"363","state":"completed","parentCaseId":"76","last_update_date":"2023-11-20 21:06:57.360","assigned_id":"3"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 23:07:58.595","rootContainerId":"75","assigned_date":"2023-11-20 23:07:58.570","displayName":"Controlar entrega de materiales","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"282","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"75","name":"Controlar entrega de materiales","reached_state_date":"2023-11-20 23:07:58.587","rootCaseId":"75","id":"395","state":"completed","parentCaseId":"75","last_update_date":"2023-11-20 23:07:58.587","assigned_id":"3"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 23:04:09.911","rootContainerId":"76","assigned_date":"2023-11-20 23:04:09.878","displayName":"Controlar fabricación","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"272","type":"USER_TASK","priority":"normal","actorId":"67","processId":"9073786231475008302","caseId":"76","name":"Controlar fabricación","reached_state_date":"2023-11-20 23:04:09.900","rootCaseId":"76","id":"390","state":"completed","parentCaseId":"76","last_update_date":"2023-11-20 23:04:09.900","assigned_id":"3"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 23:14:26.568","rootContainerId":"75","assigned_date":"2023-11-20 23:14:26.549","displayName":"Controlar fabricación","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"287","type":"USER_TASK","priority":"normal","actorId":"67","processId":"9073786231475008302","caseId":"75","name":"Controlar fabricación","reached_state_date":"2023-11-20 23:14:26.562","rootCaseId":"75","id":"401","state":"completed","parentCaseId":"75","last_update_date":"2023-11-20 23:14:26.562","assigned_id":"3"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 20:43:42.087","rootContainerId":"73","assigned_date":"2023-11-20 20:43:42.056","displayName":"Diseñar coleccion","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"241","type":"USER_TASK","priority":"normal","actorId":"66","processId":"9073786231475008302","caseId":"73","name":"Diseñar coleccion","reached_state_date":"2023-11-20 20:43:42.078","rootCaseId":"73","id":"312","state":"completed","parentCaseId":"73","last_update_date":"2023-11-20 20:43:42.078","assigned_id":"3"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-12-20 21:04:32.999","rootContainerId":"76","assigned_date":"2023-11-20 21:04:32.954","displayName":"Diseñar coleccion","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"259","type":"USER_TASK","priority":"normal","actorId":"66","processId":"9073786231475008302","caseId":"76","name":"Diseñar coleccion","reached_state_date":"2023-11-20 21:04:32.986","rootCaseId":"76","id":"341","state":"completed","parentCaseId":"76","last_update_date":"2023-11-20 21:04:32.986","assigned_id":"3"},{"displayDescription":"","executedBy":"1","archivedDate":"2023-11-20 21:33:26.850","rootContainerId":"75","assigned_date":"2023-11-20 21:33:26.812","displayName":"Diseñar coleccion","executedBySubstitute":"1","dueDate":"","description":"","sourceObjectId":"255","type":"USER_TASK","priority":"normal","actorId":"66","processId":"9073786231475008302","caseId":"75","name":"Diseñar coleccion","reached_state_date":"2023-11-20 21:33:26.837","rootCaseId":"75","id":"368","state":"completed","parentCaseId":"75","last_update_date":"2023-11-20 21:33:26.837","assigned_id":"1"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 20:45:46.480","rootContainerId":"73","assigned_date":"2023-11-20 20:45:46.463","displayName":"Reservar espacio de fabricación","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"249","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"73","name":"Reservar espacio de fabricación","reached_state_date":"2023-11-20 20:45:46.474","rootCaseId":"73","id":"327","state":"completed","parentCaseId":"73","last_update_date":"2023-11-20 20:45:46.474","assigned_id":"3"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 21:06:12.880","rootContainerId":"76","assigned_date":"2023-11-20 21:06:12.861","displayName":"Reservar espacio de fabricación","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"265","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"76","name":"Reservar espacio de fabricación","reached_state_date":"2023-11-20 21:06:12.872","rootCaseId":"76","id":"356","state":"completed","parentCaseId":"76","last_update_date":"2023-11-20 21:06:12.872","assigned_id":"3"},{"displayDescription":"","executedBy":"1","archivedDate":"2023-11-20 22:02:09.472","rootContainerId":"75","assigned_date":"2023-11-20 22:02:09.433","displayName":"Reservar espacio de fabricación","executedBySubstitute":"1","dueDate":"","description":"","sourceObjectId":"278","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"75","name":"Reservar espacio de fabricación","reached_state_date":"2023-11-20 22:02:09.463","rootCaseId":"75","id":"383","state":"completed","parentCaseId":"75","last_update_date":"2023-11-20 22:02:09.463","assigned_id":"1"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 20:45:47.838","rootContainerId":"73","assigned_date":"2023-11-20 20:45:47.815","displayName":"Reservar materiales necesarios","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"248","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"73","name":"Reservar materiales necesarios","reached_state_date":"2023-11-20 20:45:47.833","rootCaseId":"73","id":"329","state":"completed","parentCaseId":"73","last_update_date":"2023-11-20 20:45:47.833","assigned_id":"3"},{"displayDescription":"","executedBy":"3","archivedDate":"2023-11-20 21:06:13.967","rootContainerId":"76","assigned_date":"2023-11-20 21:06:13.944","displayName":"Reservar materiales necesarios","executedBySubstitute":"3","dueDate":"","description":"","sourceObjectId":"264","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"76","name":"Reservar materiales necesarios","reached_state_date":"2023-11-20 21:06:13.956","rootCaseId":"76","id":"358","state":"completed","parentCaseId":"76","last_update_date":"2023-11-20 21:06:13.956","assigned_id":"3"},{"displayDescription":"","executedBy":"1","archivedDate":"2023-11-20 22:02:11.306","rootContainerId":"75","assigned_date":"2023-11-20 22:02:11.249","displayName":"Reservar materiales necesarios","executedBySubstitute":"1","dueDate":"","description":"","sourceObjectId":"277","type":"USER_TASK","priority":"normal","actorId":"69","processId":"9073786231475008302","caseId":"75","name":"Reservar materiales necesarios","reached_state_date":"2023-11-20 22:02:11.282","rootCaseId":"75","id":"385","state":"completed","parentCaseId":"75","last_update_date":"2023-11-20 22:02:11.282","assigned_id":"1"}]
</script>
