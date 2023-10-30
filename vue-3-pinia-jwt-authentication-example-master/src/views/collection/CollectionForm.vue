<template>
  <div>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="formData.name" />
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="formData.description"></textarea>
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
      default: () => ({ name: '', description: '' }),
    },
  },
  setup(props) {
    const formData = reactive({
      name: props.formData.name,
      description: props.formData.description,
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
