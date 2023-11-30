<template>
  <Navbar />
  <div class="container pt-4 pb-4">
    <div>
      <h2 class="text-center">Crear Colección</h2>
      <CollectionForm @form-submitted="handleFormSubmission" />
    </div>
  </div>
</template>

<script>
import { router } from "../../helpers/router";
import CollectionForm from "./CollectionForm.vue";
import Navbar from "@/components/Navbar.vue"
import { useCollectionsStore } from "@/stores";

export default {
  components: {
    CollectionForm,
  },
  data() {
    return {
      formData: {
        name: "",
        description: "",
      },
    };
  },
  methods: {
    handleFormSubmission(formData) {
      const collectionStore = useCollectionsStore();
      collectionStore.create(formData);
      router.push({ name: "collections" });
    },
  },
};
</script>
