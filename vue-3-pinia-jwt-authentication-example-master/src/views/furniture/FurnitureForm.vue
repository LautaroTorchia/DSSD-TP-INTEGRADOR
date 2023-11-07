<template>
  <div>
    <form @submit.prevent="submitForm" enctype="multipart/form-data">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" class="form-control" v-model="formData.name" maxlength="100" required/>
      </div>
      <div class="form-group">
        <label for="estimated-days">Estimated Days:</label>
        <input type="number" id="estimated-days" class="form-control" v-model="formData.estimated_days" @input="validateEstimatedDays" required/>
        <div class="text-danger" ref="estimatedDaysError"></div>
      </div>
      <div class="form-group">
        <label for="estimated-release">Estimated Release:</label>
        <input type="date" id="estimated-release" class="form-control" v-model="formData.estimated_release" @change="updateEstimatedRelease" required/>
        <div class="text-danger" ref="estimatedReleaseError"></div>
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" class="form-control" v-model="formData.description" required></textarea>
      </div>
      <div class="form-group custom-file">
        <label for="image" class="custom-file-label">{{ formData.image ? formData.image.name : 'Choose Image' }}</label>
        <input type="file" id="image" class="custom-file-input" @change="updateImageFile" required/>
        <div class="text-danger" ref="imageError"></div>
      </div>
      <div class="form-group custom-file mt-3">
        <label for="manufacturing-plan" class="custom-file-label">{{ formData.manufacturing_plan ? formData.manufacturing_plan.name : 'Choose Manufacturing Plan' }}</label>
        <input type="file" id="manufacturing-plan" class="custom-file-input" @change="updateManufacturingPlanFile" required/>
        <div class="text-danger" ref="manufacturingPlanError"></div>
      </div>
      <div class="form-group">
        <label for="materials">Materials:</label>
        <select id="materials" class="form-control"  @change="addMaterial">
          <option v-for="material in materialsList" :key="material.id" :value="material.nombre">{{ material.nombre }}</option>
        </select>
        <div v-if="formData.materials" class="mt-3">
          <span v-for="(material, index) in formData.materials.split(',')" :key="index" class="badge badge-pill badge-primary mr-2">{{ material }} <button type="button" class="close ml-2" aria-label="Close" @click="removeMaterial(index)"><span aria-hidden="true">&times;</span></button></span>
        </div>
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-primary">Crear</button>
      </div>
    </form>
    <BackButton />
  </div>
</template>

<script>
import { reactive } from 'vue'
import BackButton from '@/components/BackButton.vue'
import { getCurrentInstance } from 'vue'

export default {
  name: 'FurnitureForm',
  emits: ['form-submitted'],
  components: {
    BackButton,
  },
  props: {
    formData: {
      default: () => ({ name: '', estimated_days: '', estimated_release: '', description: '', image: '', manufacturing_plan: '', materials: '' }),
    }
  },
  setup(props) {
    const formData = reactive({
      name: props.formData.name,
      estimated_days: props.formData.estimated_days,
      estimated_release: props.formData.estimated_release,
      description: props.formData.description,
      image: props.formData.image,
      manufacturing_plan: props.formData.manufacturing_plan,
      materials: props.formData.materials,
    })
    const materialsList = JSON.parse(localStorage.getItem('materialsList'))
    const { emit } = getCurrentInstance()
    const submitForm = () => {
      formData.materials = formData.materials.split(',').map(material => {
        const foundMaterial = materialsList.find(m => m.nombre === material)
        return foundMaterial ? foundMaterial.id : null
      }).filter(id => id !== null).join(',')
      emit('form-submitted', formData)
    }
    return {
      formData,
      materialsList: materialsList,
      submitForm,
    }
  },

  methods: {
    addMaterial(event) {
      const material = event.target.value
      if (this.formData.materials === '') {
        this.formData.materials = material
      } else if (!this.formData.materials.includes(material)) {
        this.formData.materials += `,${material}`
      }
    },
    removeMaterial(index) {
      const materials = this.formData.materials.split(',')
      materials.splice(index, 1)
      this.formData.materials = materials.join(',')
    },
    validateEstimatedDays() {
      const estimatedDaysErrorElement = this.$refs.estimatedDaysError
      const estimatedDays = this.formData.estimated_days

      if (estimatedDays === null || estimatedDays === '' || isNaN(estimatedDays) || estimatedDays <= 0) {
        this.displayErrorMessage(estimatedDaysErrorElement, "Please enter a positive integer.")
        this.formData.estimated_days = null
      } else {
        this.clearErrorMessage(estimatedDaysErrorElement)
      }
    },
    updateEstimatedRelease() {
      const currentDate = new Date()
      const selectedDate = new Date(this.formData.estimated_release)
      const estimatedReleaseErrorElement = this.$refs.estimatedReleaseError

      if (selectedDate <= currentDate) {
        this.displayErrorMessage(estimatedReleaseErrorElement, "Estimated Release must be a date after today.")
        this.formData.estimated_release = '' // Clear the input
      } else {
        this.clearErrorMessage(estimatedReleaseErrorElement)
      }
    },
    updateImageFile(event) {
      const inputField = event.target
      if (inputField.files.length > 0) {
        const file = inputField.files[0]
        const allowedExtensions = ["jpg", "jpeg", "png"]
        const fileExtension = file.name.split('.').pop().toLowerCase()

        if (allowedExtensions.includes(fileExtension)) {
          this.formData.image = file
          this.clearErrorMessage(this.$refs.imageError)
        } else {
          this.displayErrorMessage(this.$refs.imageError, "Invalid file format. Please upload a .jpg, .jpeg, or .png file.")
        }
      }
    },
    updateManufacturingPlanFile(event) {
      const inputField = event.target
      if (inputField.files.length > 0) {
        const file = inputField.files[0]
        const allowedExtension = "pdf"
        const fileExtension = file.name.split('.').pop().toLowerCase()

        if (fileExtension === allowedExtension) {
          this.formData.manufacturing_plan = file
          this.clearErrorMessage(this.$refs.manufacturingPlanError)
        } else {
          this.displayErrorMessage(this.$refs.manufacturingPlanError, "Invalid file format. Please upload a .pdf file.")
        }
      }
    },
    displayErrorMessage(element, message) {
      if (element) {
        element.textContent = message
      }
    },
    clearErrorMessage(element) {
      if (element) {
        element.textContent = ""
      }
    },
  },
}

</script>
