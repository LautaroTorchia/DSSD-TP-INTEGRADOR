<script>
import { router } from '@/helpers'
import FurnitureForm from './FurnitureForm.vue'
import { useFurnitureStore} from '@/stores'

export default {
    components: {
        FurnitureForm,
    },
    data() {
      return {
        formData: {
          name: '',
          estimated_days: '',
          estimated_release: '',
          description: '',
          image: '',
          manufacturing_plan: '',
          materials: '',
        },
      }
    },
    methods: {
        handleFormSubmission(formData) {
            let formObj = new FormData()
            formObj.append('nombre', formData.name)
            formObj.append('plazo_fabricacion', formData.estimated_days)
            formObj.append('fecha_lanzamiento_estimada', formData.estimated_release)
            formObj.append('descripcion', formData.description)
            formObj.append('imagen', formData.image)
            formObj.append('plan_fabricacion', formData.manufacturing_plan)
            formObj.append('materiales', formData.materials)
            ("collectionId: ", this.$route.params.collection)
            let collectionId = Number(this.$route.params.collection)
            ("collectionId_assigned: ", collectionId)
            formObj.append('coleccion', collectionId)
            ("create form: ", formObj)
            const furnitureStore = useFurnitureStore()
            furnitureStore.create(formObj)
            router.push({ name: 'furniture' })
        },
    },
}
</script>
<template>
    <div>
        <h2>Crear Mueble de la collección</h2>
        <FurnitureForm @form-submitted="handleFormSubmission"/>
    </div>
</template>
