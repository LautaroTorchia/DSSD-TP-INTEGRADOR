<template>
  <div>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="formData.name" required/>
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="formData.description" required></textarea>
      </div>
      <div class="form-group">
        <label for="estimated-release">Estimated Release:</label>
        <input type="date" id="estimated-release" class="form-control" v-model="formData.estimated_release" @change="updateEstimatedRelease" required/>
        <div class="text-danger" ref="estimatedReleaseError"></div>
      </div>
      <div class="form-group">
        <button type="submit">Confirmar</button>
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
  components: {
    BackButton,
  },
  props: {
    formData: {
      default: () => ({ name: '', description: '', estimated_release: ''}),
    },
  },
  setup(props) {
    const formData = reactive({
      name: props.formData.name,
      description: props.formData.description,
      estimated_release: props.formData.estimated_release,
    })

    const { emit } = getCurrentInstance()
    const submitForm = () => {
      emit('form-submitted', formData)
    }
    return {
      formData,
      submitForm,
    }
  },
  methods:{
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
  }
}
</script>
