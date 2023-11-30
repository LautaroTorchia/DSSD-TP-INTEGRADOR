<template>
  <div class="card-container">
    <div class="card">
      <form @submit.prevent="submitForm" class="form">
        <div class="form-group">
          <label for="name" class="label">Name:</label>
          <input
            type="text"
            id="name"
            v-model="formData.name"
            required
            class="form-input"
            style="border: 1px solid #ccc; padding: 5px"
          />
          <p class="error-message">{{ errors.name }}</p>
        </div>
        <div class="form-group">
          <label for="description" class="label">Description:</label>
          <textarea
            id="description"
            v-model="formData.description"
            required
            class="form-textarea"
            style="border: 1px solid #ccc; padding: 5px"
          ></textarea>
          <p class="error-message">{{ errors.desc }}</p>
        </div>
        <div class="form-group">
          <button type="submit" class="btn btn-primary">Confirmar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style>
.card-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.label {
  margin-bottom: 10px;
}

.form-group {
  margin-bottom: 20px;
}

.error-message {
  color: red;
}
</style>

<style>
.card-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>

<script setup>
import { ref } from "vue";
import { getCurrentInstance } from "vue";

const formData = ref({
  name: "",
  description: "",
});

const errors = ref({
  name: "",
  desc: "",
});

const { emit } = getCurrentInstance();

const validateName = () => {
  if (formData.value.name.trim() === "") {
    errors.value.name = "El nombre es requerido";
    return false;
  }
  return true;
};

const validateDesc = () => {
  if (formData.value.description.trim() === "") {
    errors.value.desc = "La descripción es requerida";
    return false;
  }
  return true;
};

const submitForm = () => {
  if (!validateName() || !validateDesc()) {
    return;
  }
  emit("form-submitted", formData.value);
};
</script>
