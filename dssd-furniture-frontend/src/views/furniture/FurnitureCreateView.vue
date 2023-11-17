<script setup>
import { router } from '@/helpers'
import FurnitureForm from './FurnitureForm.vue'
import { useFurnitureStore, useMaterialsStore } from '@/stores'
import { onBeforeMount } from 'vue'

const formData = {
  name: '',
  estimated_days: '',
  estimated_release: '',
  description: '',
  image: '',
  manufacturing_plan: '',
  materials: '',
}

onBeforeMount(async () => {
  const materialsStore = useMaterialsStore()
  const materials = await materialsStore.getAll()
  localStorage.setItem('materialsList', JSON.stringify(materials))
}
)

function handleFormSubmission(formData) {
  let formObj = new FormData()
  formObj.append('nombre', formData.name)
  formObj.append('plazo_fabricacion', formData.estimated_days)
  formObj.append('fecha_lanzamiento_estimada', formData.estimated_release)
  formObj.append('descripcion', formData.description)
  formObj.append('materiales', formData.materials)
  formObj.append('plan_fabricacion', formData.manufacturing_plan)
  formObj.append('imagen', formData.image)
  let collectionId = router.currentRoute.value.params.collection
  formObj.append('coleccion', collectionId)

  const furnitureStore = useFurnitureStore()
  furnitureStore.create(formObj)
  router.push({ name: 'furniture', params: { collection: collectionId } })
}
</script>
<template>
  <div>
    <h2>Crear Mueble de la collección</h2>
    <FurnitureForm @form-submitted="handleFormSubmission" />
  </div>
</template>
