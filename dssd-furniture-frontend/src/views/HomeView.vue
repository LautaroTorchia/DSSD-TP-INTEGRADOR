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
        <div class="container">
          <router-link :to="{ name: 'collections' }" class="btn btn-primary me-2">Ver Colecciones</router-link>
          <router-link :to="{ name: 'designed-collections' }" class="btn btn-primary me-2">Analizar materiales</router-link>
          <router-link :to="{ name: 'dashboard' }" class="btn btn-primary me-2">Indicadores</router-link>
          <router-link :to="{ name: 'delivery-order-collection-list' }" class="btn btn-primary me-2">Ordenes de entrega</router-link>
        </div>
    </div>
</template>
