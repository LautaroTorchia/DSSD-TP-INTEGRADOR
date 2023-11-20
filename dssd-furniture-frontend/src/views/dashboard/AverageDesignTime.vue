<template>
    <div class="medium">
        {{ chartData  }}
        <div v-if="loading" class="spinner"></div>
        <canvas id="AverageDesignTimeChart" ref="chart"></canvas>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBonitaVariable, fetchWrapper } from '@/helpers'
import { useCollectionsStore } from '@/stores'
import { storeToRefs } from 'pinia'
import Chart from 'chart.js/auto'

const collectionStore = useCollectionsStore()
const { collections } = storeToRefs(collectionStore)

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
            }
        }
    })

    loading.value = false
})

const bonitaTasks = [
  {
    "displayDescription": "",
    "executedBy": "1",
    "archivedDate": "2023-11-20 22:02:11.306",
    "rootContainerId": {
      "displayDescription": "",
      "deploymentDate": "2023-11-20 20:42:04.688",
      "displayName": "Muebles",
      "name": "Muebles",
      "description": "",
      "deployedBy": "3",
      "id": "9073786231475008302",
      "activationState": "ENABLED",
      "version": "2.0",
      "configurationState": "RESOLVED",
      "last_update_date": "2023-11-20 20:42:08.706",
      "actorinitiatorid": "68"
    },
    "assigned_date": "2023-11-20 22:02:11.249",
    "displayName": "Reservar materiales necesarios",
    "executedBySubstitute": "1",
    "dueDate": "",
    "description": "",
    "sourceObjectId": "277",
    "type": "USER_TASK",
    "priority": "normal",
    "actorId": "69",
    "processId": "9073786231475008302",
    "caseId": "75",
    "name": "Reservar materiales necesarios",
    "reached_state_date": "2023-11-20 22:02:11.282",
    "rootCaseId": "75",
    "id": "385",
    "state": "completed",
    "parentCaseId": "75",
    "last_update_date": "2023-11-20 22:02:11.282",
    "assigned_id": {
      "firstname": "Juan",
      "icon": "icons/default/icon_user.png",
      "creation_date": "2023-10-16 22:31:26.619",
      "userName": "juan.vicens@gmail.com",
      "title": "",
      "created_by_user_id": "-1",
      "enabled": "true",
      "lastname": "Vicens",
      "last_connection": "2023-11-20 22:28:34.388",
      "password": "",
      "manager_id": "0",
      "id": "1",
      "job_title": "",
      "last_update_date": "2023-10-16 22:31:26.619"
    }
  },
  {
    "displayDescription": "",
    "executedBy": "1",
    "archivedDate": "2023-11-20 22:02:09.472",
    "rootContainerId": {
      "displayDescription": "",
      "deploymentDate": "2023-11-20 20:42:04.688",
      "displayName": "Muebles",
      "name": "Muebles",
      "description": "",
      "deployedBy": "3",
      "id": "9073786231475008302",
      "activationState": "ENABLED",
      "version": "2.0",
      "configurationState": "RESOLVED",
      "last_update_date": "2023-11-20 20:42:08.706",
      "actorinitiatorid": "68"
    },
    "assigned_date": "2023-11-20 22:02:09.433",
    "displayName": "Reservar espacio de fabricación",
    "executedBySubstitute": "1",
    "dueDate": "",
    "description": "",
    "sourceObjectId": "278",
    "type": "USER_TASK",
    "priority": "normal",
    "actorId": "69",
    "processId": "9073786231475008302",
    "caseId": "75",
    "name": "Reservar espacio de fabricación",
    "reached_state_date": "2023-11-20 22:02:09.463",
    "rootCaseId": "75",
    "id": "383",
    "state": "completed",
    "parentCaseId": "75",
    "last_update_date": "2023-11-20 22:02:09.463",
    "assigned_id": {
      "firstname": "Juan",
      "icon": "icons/default/icon_user.png",
      "creation_date": "2023-10-16 22:31:26.619",
      "userName": "juan.vicens@gmail.com",
      "title": "",
      "created_by_user_id": "-1",
      "enabled": "true",
      "lastname": "Vicens",
      "last_connection": "2023-11-20 22:28:34.388",
      "password": "",
      "manager_id": "0",
      "id": "1",
      "job_title": "",
      "last_update_date": "2023-10-16 22:31:26.619"
    }
  },
  {
    "displayDescription": "",
    "executedBy": "1",
    "archivedDate": "2023-11-20 22:02:07.314",
    "rootContainerId": {
      "displayDescription": "",
      "deploymentDate": "2023-11-20 20:42:04.688",
      "displayName": "Muebles",
      "name": "Muebles",
      "description": "",
      "deployedBy": "3",
      "id": "9073786231475008302",
      "activationState": "ENABLED",
      "version": "2.0",
      "configurationState": "RESOLVED",
      "last_update_date": "2023-11-20 20:42:08.706",
      "actorinitiatorid": "68"
    },
    "assigned_date": "2023-11-20 22:02:07.268",
    "displayName": "Armar plan de fabricacion",
    "executedBySubstitute": "1",
    "dueDate": "",
    "description": "",
    "sourceObjectId": "275",
    "type": "USER_TASK",
    "priority": "normal",
    "actorId": "69",
    "processId": "9073786231475008302",
    "caseId": "75",
    "name": "Armar plan de fabricacion",
    "reached_state_date": "2023-11-20 22:02:07.296",
    "rootCaseId": "75",
    "id": "376",
    "state": "completed",
    "parentCaseId": "75",
    "last_update_date": "2023-11-20 22:02:07.296",
    "assigned_id": {
      "firstname": "Juan",
      "icon": "icons/default/icon_user.png",
      "creation_date": "2023-10-16 22:31:26.619",
      "userName": "juan.vicens@gmail.com",
      "title": "",
      "created_by_user_id": "-1",
      "enabled": "true",
      "lastname": "Vicens",
      "last_connection": "2023-11-20 22:28:34.388",
      "password": "",
      "manager_id": "0",
      "id": "1",
      "job_title": "",
      "last_update_date": "2023-10-16 22:31:26.619"
    }
  },
  {
    "displayDescription": "",
    "executedBy": "0",
    "archivedDate": "2023-11-20 21:33:52.621",
    "rootContainerId": {
      "displayDescription": "",
      "deploymentDate": "2023-11-20 20:42:04.688",
      "displayName": "Muebles",
      "name": "Muebles",
      "description": "",
      "deployedBy": "3",
      "id": "9073786231475008302",
      "activationState": "ENABLED",
      "version": "2.0",
      "configurationState": "RESOLVED",
      "last_update_date": "2023-11-20 20:42:08.706",
      "actorinitiatorid": "68"
    },
    "displayName": "Consultar API de proveedores",
    "executedBySubstitute": "0",
    "description": "",
    "sourceObjectId": "274",
    "type": "AUTOMATIC_TASK",
    "processId": "9073786231475008302",
    "caseId": "75",
    "name": "Consultar API de proveedores",
    "reached_state_date": "2023-11-20 21:33:52.613",
    "rootCaseId": "75",
    "id": "373",
    "state": "completed",
    "parentCaseId": "75",
    "last_update_date": "2023-11-20 21:33:52.613"
  },
  {
    "displayDescription": "",
    "executedBy": "1",
    "archivedDate": "2023-11-20 21:33:52.057",
    "rootContainerId": {
      "displayDescription": "",
      "deploymentDate": "2023-11-20 20:42:04.688",
      "displayName": "Muebles",
      "name": "Muebles",
      "description": "",
      "deployedBy": "3",
      "id": "9073786231475008302",
      "activationState": "ENABLED",
      "version": "2.0",
      "configurationState": "RESOLVED",
      "last_update_date": "2023-11-20 20:42:08.706",
      "actorinitiatorid": "68"
    },
    "assigned_date": "2023-11-20 21:33:52.027",
    "displayName": "Analizar materiales",
    "executedBySubstitute": "1",
    "dueDate": "",
    "description": "",
    "sourceObjectId": "273",
    "type": "USER_TASK",
    "priority": "normal",
    "actorId": "69",
    "processId": "9073786231475008302",
    "caseId": "75",
    "name": "Analizar materiales",
    "reached_state_date": "2023-11-20 21:33:52.047",
    "rootCaseId": "75",
    "id": "371",
    "state": "completed",
    "parentCaseId": "75",
    "last_update_date": "2023-11-20 21:33:52.047",
    "assigned_id": {
      "firstname": "Juan",
      "icon": "icons/default/icon_user.png",
      "creation_date": "2023-10-16 22:31:26.619",
      "userName": "juan.vicens@gmail.com",
      "title": "",
      "created_by_user_id": "-1",
      "enabled": "true",
      "lastname": "Vicens",
      "last_connection": "2023-11-20 22:28:34.388",
      "password": "",
      "manager_id": "0",
      "id": "1",
      "job_title": "",
      "last_update_date": "2023-10-16 22:31:26.619"
    }
  },
  {
    "displayDescription": "",
    "executedBy": "1",
    "archivedDate": "2023-11-20 21:33:26.850",
    "rootContainerId": {
      "displayDescription": "",
      "deploymentDate": "2023-11-20 20:42:04.688",
      "displayName": "Muebles",
      "name": "Muebles",
      "description": "",
      "deployedBy": "3",
      "id": "9073786231475008302",
      "activationState": "ENABLED",
      "version": "2.0",
      "configurationState": "RESOLVED",
      "last_update_date": "2023-11-20 20:42:08.706",
      "actorinitiatorid": "68"
    },
    "assigned_date": "2023-11-20 21:33:26.812",
    "displayName": "Diseñar coleccion",
    "executedBySubstitute": "1",
    "dueDate": "",
    "description": "",
    "sourceObjectId": "255",
    "type": "USER_TASK",
    "priority": "normal",
    "actorId": "66",
    "processId": "9073786231475008302",
    "caseId": "75",
    "name": "Diseñar coleccion",
    "reached_state_date": "2023-11-20 21:33:26.837",
    "rootCaseId": "75",
    "id": "368",
    "state": "completed",
    "parentCaseId": "75",
    "last_update_date": "2023-11-20 21:33:26.837",
    "assigned_id": {
      "firstname": "Juan",
      "icon": "icons/default/icon_user.png",
      "creation_date": "2023-10-16 22:31:26.619",
      "userName": "juan.vicens@gmail.com",
      "title": "",
      "created_by_user_id": "-1",
      "enabled": "true",
      "lastname": "Vicens",
      "last_connection": "2023-11-20 22:28:34.388",
      "password": "",
      "manager_id": "0",
      "id": "1",
      "job_title": "",
      "last_update_date": "2023-10-16 22:31:26.619"
    }
  },
  {
    "displayDescription": "",
    "executedBy": "3",
    "archivedDate": "2023-11-20 21:06:57.365",
    "rootContainerId": {
      "displayDescription": "",
      "deploymentDate": "2023-11-20 20:42:04.688",
      "displayName": "Muebles",
      "name": "Muebles",
      "description": "",
      "deployedBy": "3",
      "id": "9073786231475008302",
      "activationState": "ENABLED",
      "version": "2.0",
      "configurationState": "RESOLVED",
      "last_update_date": "2023-11-20 20:42:08.706",
      "actorinitiatorid": "68"
    },
    "assigned_date": "2023-11-20 21:06:57.351",
    "displayName": "Controlar entrega de materiales",
    "executedBySubstitute": "3",
    "dueDate": "",
    "description": "",
    "sourceObjectId": "269",
    "type": "USER_TASK",
    "priority": "normal",
    "actorId": "69",
    "processId": "9073786231475008302",
    "caseId": "76",
    "name": "Controlar entrega de materiales",
    "reached_state_date": "2023-11-20 21:06:57.360",
    "rootCaseId": "76",
    "id": "363",
    "state": "completed",
    "parentCaseId": "76",
    "last_update_date": "2023-11-20 21:06:57.360",
    "assigned_id": {
      "firstname": "Lautaro",
      "icon": "icons/default/icon_user.png",
      "creation_date": "2023-10-16 22:31:26.674",
      "userName": "lautaro.torchia@gmail.com",
      "title": "",
      "created_by_user_id": "-1",
      "enabled": "true",
      "lastname": "Torchia",
      "last_connection": "2023-11-20 21:48:52.125",
      "password": "",
      "manager_id": "0",
      "id": "3",
      "job_title": "",
      "last_update_date": "2023-10-16 22:31:26.674"
    }
  },
  {
    "displayDescription": "",
    "executedBy": "3",
    "archivedDate": "2023-11-20 21:06:13.967",
    "rootContainerId": {
      "displayDescription": "",
      "deploymentDate": "2023-11-20 20:42:04.688",
      "displayName": "Muebles",
      "name": "Muebles",
      "description": "",
      "deployedBy": "3",
      "id": "9073786231475008302",
      "activationState": "ENABLED",
      "version": "2.0",
      "configurationState": "RESOLVED",
      "last_update_date": "2023-11-20 20:42:08.706",
      "actorinitiatorid": "68"
    },
    "assigned_date": "2023-11-20 21:06:13.944",
    "displayName": "Reservar materiales necesarios",
    "executedBySubstitute": "3",
    "dueDate": "",
    "description": "",
    "sourceObjectId": "264",
    "type": "USER_TASK",
    "priority": "normal",
    "actorId": "69",
    "processId": "9073786231475008302",
    "caseId": "76",
    "name": "Reservar materiales necesarios",
    "reached_state_date": "2023-11-20 21:06:13.956",
    "rootCaseId": "76",
    "id": "358",
    "state": "completed",
    "parentCaseId": "76",
    "last_update_date": "2023-11-20 21:06:13.956",
    "assigned_id": {
      "firstname": "Lautaro",
      "icon": "icons/default/icon_user.png",
      "creation_date": "2023-10-16 22:31:26.674",
      "userName": "lautaro.torchia@gmail.com",
      "title": "",
      "created_by_user_id": "-1",
      "enabled": "true",
      "lastname": "Torchia",
      "last_connection": "2023-11-20 21:48:52.125",
      "password": "",
      "manager_id": "0",
      "id": "3",
      "job_title": "",
      "last_update_date": "2023-10-16 22:31:26.674"
    }
  },
  {
    "displayDescription": "",
    "executedBy": "3",
    "archivedDate": "2023-11-20 21:06:12.880",
    "rootContainerId": {
      "displayDescription": "",
      "deploymentDate": "2023-11-20 20:42:04.688",
      "displayName": "Muebles",
      "name": "Muebles",
      "description": "",
      "deployedBy": "3",
      "id": "9073786231475008302",
      "activationState": "ENABLED",
      "version": "2.0",
      "configurationState": "RESOLVED",
      "last_update_date": "2023-11-20 20:42:08.706",
      "actorinitiatorid": "68"
    },
    "assigned_date": "2023-11-20 21:06:12.861",
    "displayName": "Reservar espacio de fabricación",
    "executedBySubstitute": "3",
    "dueDate": "",
    "description": "",
    "sourceObjectId": "265",
    "type": "USER_TASK",
    "priority": "normal",
    "actorId": "69",
    "processId": "9073786231475008302",
    "caseId": "76",
    "name": "Reservar espacio de fabricación",
    "reached_state_date": "2023-11-20 21:06:12.872",
    "rootCaseId": "76",
    "id": "356",
    "state": "completed",
    "parentCaseId": "76",
    "last_update_date": "2023-11-20 21:06:12.872",
    "assigned_id": {
      "firstname": "Lautaro",
      "icon": "icons/default/icon_user.png",
      "creation_date": "2023-10-16 22:31:26.674",
      "userName": "lautaro.torchia@gmail.com",
      "title": "",
      "created_by_user_id": "-1",
      "enabled": "true",
      "lastname": "Torchia",
      "last_connection": "2023-11-20 21:48:52.125",
      "password": "",
      "manager_id": "0",
      "id": "3",
      "job_title": "",
      "last_update_date": "2023-10-16 22:31:26.674"
    }
  },
  {
    "displayDescription": "",
    "executedBy": "3",
    "archivedDate": "2023-11-20 21:06:12.020",
    "rootContainerId": {
      "displayDescription": "",
      "deploymentDate": "2023-11-20 20:42:04.688",
      "displayName": "Muebles",
      "name": "Muebles",
      "description": "",
      "deployedBy": "3",
      "id": "9073786231475008302",
      "activationState": "ENABLED",
      "version": "2.0",
      "configurationState": "RESOLVED",
      "last_update_date": "2023-11-20 20:42:08.706",
      "actorinitiatorid": "68"
    },
    "assigned_date": "2023-11-20 21:06:12.006",
    "displayName": "Armar plan de fabricacion",
    "executedBySubstitute": "3",
    "dueDate": "",
    "description": "",
    "sourceObjectId": "262",
    "type": "USER_TASK",
    "priority": "normal",
    "actorId": "69",
    "processId": "9073786231475008302",
    "caseId": "76",
    "name": "Armar plan de fabricacion",
    "reached_state_date": "2023-11-20 21:06:12.015",
    "rootCaseId": "76",
    "id": "349",
    "state": "completed",
    "parentCaseId": "76",
    "last_update_date": "2023-11-20 21:06:12.015",
    "assigned_id": {
      "firstname": "Lautaro",
      "icon": "icons/default/icon_user.png",
      "creation_date": "2023-10-16 22:31:26.674",
      "userName": "lautaro.torchia@gmail.com",
      "title": "",
      "created_by_user_id": "-1",
      "enabled": "true",
      "lastname": "Torchia",
      "last_connection": "2023-11-20 21:48:52.125",
      "password": "",
      "manager_id": "0",
      "id": "3",
      "job_title": "",
      "last_update_date": "2023-10-16 22:31:26.674"
    }
  }
]

</script>
