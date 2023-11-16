<script setup>
import { storeToRefs } from 'pinia'

import { useAuthStore } from '@/stores'


const authStore = useAuthStore()
const { user: authUser } = storeToRefs(authStore)

</script>

<template>
    <div>
        <h1>GlobalFurniture-LJJ Muebles </h1>
        <h2>Hola {{authUser?.username}}!</h2>
        <router-link :to="{ name: 'collections' }">Ver Colecciones</router-link>
        <router-link :to="{ name: 'designed-collections' }">Analizar materiales</router-link>
        <router-link :to="{ name: 'dashboard' }">Indicadores</router-link>
    </div>
</template>
