<template>
  <div>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="formData.name" />
      </div>
      <div class="form-group">
        <label for="deadline">Deadline:</label>
        <input type="text" id="name" v-model="formData.deadline" />
      </div>
      <div class="form-group">
        <label for="estimated-release">Estimated Release:</label>
        <input type="text" id="name" v-model="formData.estimated_release" />
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="formData.description"></textarea>
      </div>
      <div class="form-group">
        <label for="image">Image:</label>
        <input type="text" id="image" v-model="formData.image" />
      </div>
      <div class="form-group">
        <label for="manufacturing-plan">Manufacturing Plan:</label>
        <textarea id="description" v-model="formData.manufacturing_plan"></textarea>
      </div>
      <div class="form-group">
        <label for="materials">Materials:</label>
        <textarea id="description" v-model="formData.materials"></textarea>
      </div>
      <div class="form-group">
        <button type="submit">Confirmar</button>
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
};
</script>
