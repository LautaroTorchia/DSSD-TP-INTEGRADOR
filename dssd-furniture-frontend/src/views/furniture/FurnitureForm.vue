<template>
  <div class="d-flex justify-content-center align-items-center">
    <div class="card shadow rounded">
      <div class="card-body">
        <form @submit.prevent="submitForm" enctype="multipart/form-data">
          <div class="form-group">
            <label for="name">Name:</label>
            <input
              type="text"
              id="name"
              class="form-control"
              v-model="formData.name"
              maxlength="100"
              required
            />
          </div>
          <div class="form-group">
            <label for="estimated-days">Estimated Days:</label>
            <input
              type="number"
              id="estimated-days"
              class="form-control"
              v-model="formData.estimated_days"
              @input="validateEstimatedDays"
              required
            />
            <div class="text-danger" ref="estimatedDaysError"></div>
          </div>
          <div class="form-group">
            <label for="description">Description:</label>
            <textarea
              id="description"
              class="form-control"
              v-model="formData.description"
              required
            ></textarea>
          </div>
          <div class="form-group custom-file">
            <label for="image" class="custom-file-label">{{
              formData.image ? formData.image.name : "Choose Image"
            }}</label>
            <input
              type="file"
              id="image"
              class="custom-file-input"
              @change="updateImageFile"
              required
            />
            <div class="text-danger" ref="imageError"></div>
          </div>
          <div class="form-group custom-file mt-3">
            <label for="manufacturing-plan" class="custom-file-label">{{
              formData.manufacturing_plan
                ? formData.manufacturing_plan.name
                : "Choose Manufacturing Plan"
            }}</label>
            <input
              type="file"
              id="manufacturing-plan"
              class="custom-file-input"
              @change="updateManufacturingPlanFile"
              required
            />
            <div class="text-danger" ref="manufacturingPlanError"></div>
          </div>
          <div class="form-group">
            <div v-if="materialsList">
              <label for="materials">Materials:</label>
              <select id="materials" class="form-control" @change="addMaterial">
                <option
                  v-for="material in materialsList"
                  :key="material.id"
                  :value="material.nombre"
                >
                  {{ material.nombre }}
                </option>
              </select>
            </div>
            <div v-if="formData.materials" class="mt-3">
              <span
                v-for="(material, index) in formData.materials.split(',')"
                :key="index"
                class="badge badge-pill badge-primary mr-2"
                >{{ material }}
                <button
                  type="button"
                  class="close ml-2"
                  aria-label="Close"
                  @click="removeMaterial(index)"
                >
                  <span aria-hidden="true">&times;</span>
                </button></span
              >
            </div>
          </div>
          <div class="text-danger" ref="materialsError"></div>
          <div class="form-group text-center">
            <button type="submit" class="btn btn-primary btn-lg">Crear</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeMount, ref } from "vue";
import { getCurrentInstance } from "vue";
import { useMaterialsStore } from "@/stores";

const props = defineProps({
  formData: {
    default: () => ({
      name: "",
      estimated_days: "",
      description: "",
      image: "",
      manufacturing_plan: "",
      materials: "",
    }),
  },
});

const formData = ref({
  name: props.formData.name,
  estimated_days: props.formData.estimated_days,
  description: props.formData.description,
  image: props.formData.image,
  manufacturing_plan: props.formData.manufacturing_plan,
  materials: props.formData.materials,
});

const materialsList = ref([]);
const materialsStore = useMaterialsStore();

const estimatedDaysError = ref(null);
const imageError = ref(null);
const manufacturingPlanError = ref(null);
const materialsError = ref(null);

onBeforeMount(async () => {
  materialsList.value = await materialsStore.getAll();
});

const { emit } = getCurrentInstance();

const submitForm = () => {
  if (formData.value.materials === "") {
    displayErrorMessage(materialsError, "Please select at least one material.");
    return;
  }
  formData.value.materials = formData.value.materials
    .split(",")
    .map((material) => {
      const foundMaterial = materialsList.value.find(
        (m) => m.nombre === material,
      );
      return foundMaterial ? foundMaterial.id : null;
    })
    .filter((id) => id !== null)
    .join(",");
  emit("form-submitted", formData.value);
};

const addMaterial = (event) => {
  const material = event.target.value;
  if (formData.value.materials === "") {
    formData.value.materials = material;
  } else if (!formData.value.materials.includes(material)) {
    formData.value.materials += `,${material}`;
  }
};

const removeMaterial = (index) => {
  const materials = formData.value.materials.split(",");
  materials.splice(index, 1);
  formData.value.materials = materials.join(",");
};

const validateEstimatedDays = () => {
  const estimatedDays = formData.value.estimated_days;

  if (
    estimatedDays === null ||
    estimatedDays === "" ||
    isNaN(estimatedDays) ||
    estimatedDays <= 0
  ) {
    displayErrorMessage(estimatedDaysError, "Please enter a positive integer.");
    formData.value.estimated_days = null;
  } else {
    clearErrorMessage(estimatedDaysError);
  }
};

const updateImageFile = (event) => {
  const inputField = event.target;
  if (inputField.files.length > 0) {
    const file = inputField.files[0];
    const allowedExtensions = ["jpg", "jpeg", "png"];
    const fileExtension = file.name.split(".").pop().toLowerCase();

    if (allowedExtensions.includes(fileExtension)) {
      formData.value.image = file;
      clearErrorMessage(imageError);
    } else {
      displayErrorMessage(
        imageError,
        "Invalid file format. Please upload a .jpg, .jpeg, or .png file.",
      );
    }
  }
};

const updateManufacturingPlanFile = (event) => {
  const inputField = event.target;
  if (inputField.files.length > 0) {
    const file = inputField.files[0];
    const allowedExtension = "pdf";
    const fileExtension = file.name.split(".").pop().toLowerCase();

    if (fileExtension === allowedExtension) {
      formData.value.manufacturing_plan = file;
      clearErrorMessage(manufacturingPlanError);
    } else {
      displayErrorMessage(
        manufacturingPlanError,
        "Invalid file format. Please upload a .pdf file.",
      );
    }
  }
};

const displayErrorMessage = (element, message) => {
  if (element) {
    element.value = message;
  }
};

const clearErrorMessage = (element) => {
  if (element) {
    element.value = "";
  }
};
</script>
