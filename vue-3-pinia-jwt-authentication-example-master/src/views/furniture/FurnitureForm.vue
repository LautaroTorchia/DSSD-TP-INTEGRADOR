<template>
  <div>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" class="form-control" v-model="formData.name" />
      </div>
      <div class="form-group">
        <label for="deadline">Deadline:</label>
        <input type="date" id="deadline" class="form-control" v-model="formData.deadline" @change="updateDeadline" />
        <div class="text-danger" ref="deadlineError"></div>
      </div>
      <div class="form-group">
        <label for="estimated-release">Estimated Release:</label>
        <input type="date" id="estimated-release" class="form-control" v-model="formData.estimated_release" @change="updateEstimatedRelease" />
        <div class="text-danger" ref="estimatedReleaseError"></div>
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" class="form-control" v-model="formData.description"></textarea>
      </div>
      <div class="form-group custom-file">
        <label for="image" class="custom-file-label">{{ formData.image ? formData.image.name : 'Choose Image' }}</label>
        <input type="file" id="image" class="custom-file-input" @change="updateImageFile" />
        <div class="text-danger" ref="imageError"></div>
      </div>
      <div class="form-group custom-file mt-3">
        <label for="manufacturing-plan" class="custom-file-label">{{ formData.manufacturing_plan ? formData.manufacturing_plan.name : 'Choose Manufacturing Plan' }}</label>
        <input type="file" id="manufacturing-plan" class="custom-file-input" @change="updateManufacturingPlanFile" />
        <div class="text-danger" ref="manufacturingPlanError"></div>
      </div>
      <div class="form-group">
        <label for="materials">Materials:</label>
        <textarea id="materials" class="form-control" v-model="formData.materials"></textarea>
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-primary">Crear</button>
      </div>
    </form>
    <BackButton />
  </div>
</template>

<script>
import { reactive } from 'vue';
import BackButton from '@/components/BackButton.vue';
import { getCurrentInstance } from 'vue';

export default {
  components: {
    BackButton,
  },
  props: {
    formData: {
      default: () => ({ name: '', deadline: '', estimated_release: '', description: '', image: '', manufacturing_plan: '', materials: '' }),
    },
  },
  setup(props) {
    const formData = reactive({
      name: props.formData.name,
      deadline: props.formData.deadline,
      estimated_release: props.formData.estimated_release,
      description: props.formData.description,
      image: props.formData.image,
      manufacturing_plan: props.formData.manufacturing_plan,
      materials: props.formData.materials,
    });

    const { emit } = getCurrentInstance();
    const submitForm = () => {
      emit('form-submitted', formData);
    };
    return {
      formData,
      submitForm,
    };
  },

  methods: {
    updateDeadline() {
      const currentDate = new Date();
      const selectedDate = new Date(this.formData.deadline);
      const deadlineErrorElement = this.$refs.deadlineError;

      if (selectedDate <= currentDate) {
        this.displayErrorMessage(deadlineErrorElement, "Deadline must be a date after today.");
        this.formData.deadline = ''; // Clear the input
      } else {
        this.clearErrorMessage(deadlineErrorElement);
      }
    },
    updateEstimatedRelease() {
      const currentDate = new Date();
      const selectedDate = new Date(this.formData.estimated_release);
      const estimatedReleaseErrorElement = this.$refs.estimatedReleaseError;

      if (selectedDate <= currentDate) {
        this.displayErrorMessage(estimatedReleaseErrorElement, "Estimated Release must be a date after today.");
        this.formData.estimated_release = ''; // Clear the input
      } else {
        this.clearErrorMessage(estimatedReleaseErrorElement);
      }
    },
    updateImageFile(event) {
      const inputField = event.target;
      if (inputField.files.length > 0) {
        const file = inputField.files[0];
        const allowedExtensions = ["jpg", "jpeg", "png"];
        const fileExtension = file.name.split('.').pop().toLowerCase();

        if (allowedExtensions.includes(fileExtension)) {
          this.formData.image = file;
          this.clearErrorMessage(this.$refs.imageError);
        } else {
          this.displayErrorMessage(this.$refs.imageError, "Invalid file format. Please upload a .jpg, .jpeg, or .png file.");
        }
      }
    },
    updateManufacturingPlanFile(event) {
      const inputField = event.target;
      if (inputField.files.length > 0) {
        const file = inputField.files[0];
        const allowedExtension = "pdf";
        const fileExtension = file.name.split('.').pop().toLowerCase();

        if (fileExtension === allowedExtension) {
          this.formData.manufacturing_plan = file;
          this.clearErrorMessage(this.$refs.manufacturingPlanError);
        } else {
          this.displayErrorMessage(this.$refs.manufacturingPlanError, "Invalid file format. Please upload a .pdf file.");
        }
      }
    },
    displayErrorMessage(element, message) {
      if (element) {
        element.textContent = message;
      }
    },
    clearErrorMessage(element) {
      if (element) {
        element.textContent = "";
      }
    },
  },
};

</script>
