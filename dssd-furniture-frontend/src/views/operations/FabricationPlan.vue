<template>
  <div v-if="!loading" name="parentdiv" class="d-flex">
    <div name="div1">
      <h1>Plan de fabricación</h1>
      <div class="card">
        <div class="card-body">
          <h2>Lugares de fabricación:</h2>
          <div v-for="(factory, index) in factoryList" :key="index">
            <input
              type="radio"
              :id="'factory-' + index"
              :value="factory"
              v-model="selectedFactory"
            />
            <label :for="'factory-' + index">{{
              factory.nombre || factory.telefono_reserva
            }}</label>
          </div>
          <button @click="clearSelection">Clear</button>
          <div v-if="collection.estimated_launch_date">
            <h2>Fecha de fabricación:</h2>
            {{ collection.estimated_launch_date }}
          </div>
          <div v-else class="date-field form-group">
            <label for="estimatedLaunchDate"
              >Fecha estimada de lanzamiento:</label
            >
            <input
              type="date"
              id="estimatedLaunchDate"
              v-model="estimatedLaunchDate"
              class="form-control"
              :min="new Date().toISOString().split('T')[0]"
            />
          </div>
          <div v-if="estimatedLaunchDate" class="date-field form-group">
            <label for="slot_start_date">Fecha inicio reserva:</label>
            <input
              type="date"
              id="slot_start_date"
              v-model="slot_start_date"
              class="form-control"
              :min="new Date().toISOString().split('T')[0]"
              :max="estimatedLaunchDate"
            />
          </div>
          <div
            v-if="estimatedLaunchDate && slot_start_date"
            class="date-field form-group"
          >
            <label for="slot_end_date">Fecha fin reserva:</label>
            <input
              type="date"
              id="slot_end_date"
              v-model="slot_end_date"
              class="form-control"
              :min="slot_start_date"
              :max="estimatedLaunchDate"
            />
          </div>
        </div>
        <div class="form-group">
          <label for="lotQuantity">Cantidad de lotes:</label>
          <input
            type="number"
            class="form-control"
            v-model.number="lotQuantity"
            min="1"
          />
        </div>
      </div>
    </div>

    <div name="div2">
      <h2>Lista de materiales:</h2>
      <div class="card">
        <div class="card-body">
          <div v-for="material in collectionMaterialList" :key="material.id">
            <h5 class="card-title">Material: {{ material.name }}</h5>
            <h5 class="card-title">Cantidad: {{ material.amount }}</h5>
            <div class="card-text">
              <div
                v-for="materialFromProvider in materialsFromProviders"
                :key="materialFromProvider.material"
              >
                <div v-if="material.id == materialFromProvider.material">
                  <div class="card">
                    <div class="card-body">
                      <h6 class="card-subtitle mb-2 text-muted">
                        Proveedor o reciclador:
                        {{ materialFromProvider.actor_nombre }}
                      </h6>
                      <h6 class="card-subtitle mb-2 text-muted">
                        Cantidad: {{ materialFromProvider.cantidad_disponible }}
                      </h6>
                      <h6
                        class="card-subtitle mb-2 text-muted"
                        v-if="materialFromProvider.es_importado"
                      >
                        Es importado
                      </h6>
                      <h6 class="card-subtitle mb-2 text-muted" v-else>
                        No es importado
                      </h6>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          :id="'materialProvided-' + materialFromProvider.id"
                          v-model="materialFromProvider.checked"
                        />
                        <label
                          class="form-check-label"
                          :for="'materialProvided-' + materialFromProvider.id"
                          >Seleccionar</label
                        >
                        <div v-if="materialFromProvider.checked">
                          <label for="amount">Amount:</label>
                          <input
                            type="number"
                            class="form-control"
                            v-model.number="
                              selectedMaterials[material.id][
                                materialFromProvider.id
                              ]
                            "
                            min="1"
                            :max="materialFromProvider.cantidad_disponible"
                          />

                          <label for="deliveryDate"
                            >Delivery Date (minimo
                            {{
                              materialFromProvider.plazo_entrega_dias
                            }}
                            días):</label
                          >
                          <input
                            type="date"
                            class="form-control"
                            v-model="materialFromProvider.deliveryDate"
                            :min="
                              new Date(
                                Date.now() +
                                  materialFromProvider.plazo_entrega_dias *
                                    24 *
                                    60 *
                                    60 *
                                    1000,
                              )
                                .toISOString()
                                .split('T')[0]
                            "
                          />

                          <div
                            v-if="
                              !validateTotalAmount(material.id, material.amount)
                            "
                          >
                            <p class="text-danger">
                              Total amount for {{ material.name }} must be
                              {{ material.amount }}, but is
                              {{ getTotalAmount(material.id) }}
                            </p>
                          </div>

                          <div
                            v-if="!validateDeliveryDate(materialFromProvider)"
                          >
                            <p class="text-danger">
                              Delivery date is required for selected material
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!validateAllMaterials()">
          <p class="text-danger text-center">
            Total amount for each material must be equal to the amount of the
            material
          </p>
        </div>
      </div>
      <button
        @click="onSubmit"
        style="
          background-color: blue;
          color: white;
          padding: 10px 20px;
          border: none;
          cursor: pointer;
        "
      >
        Submit
      </button>
    </div>
  </div>
  <div v-else class="spinner-border spinner-border-sm"></div>
</template>

<script setup>
import { onBeforeMount, ref } from "vue";
import {
  getBonitaVariable,
  setBonitaVariable,
  router,
  fetchWrapper,
} from "@/helpers";
import { useCollectionsStore } from "@/stores";
import { storeToRefs } from "pinia";

const collectionStore = useCollectionsStore();
const { collections } = storeToRefs(collectionStore);
const collection = ref(null);
const collectionId = router.currentRoute.value.params.collection;
const caseId = JSON.parse(localStorage.getItem("collections")).collections.find(
  (collection) => collection.id == collectionId,
).caseId;
const materialsFromProviders = ref([]);
const collectionMaterialList = ref([]);
const selectedMaterials = ref([]);
const factoryList = ref([]);
const selectedFactory = ref(null);
const estimatedLaunchDate = ref(null);
const slot_start_date = ref(null);
const slot_end_date = ref(null);
const lotQuantity = ref(1);
const proveedoresUrl = `${import.meta.env.VITE_API_PROVEEDORES_URL}`;
const baseUrl = `${import.meta.env.VITE_API_URL}`;
const renegociated = ref(false);
const loading = ref(true);

const fetchMaterialsFromProviders = async () => {
  let materialsQuery = await getBonitaVariable(caseId, "consulta_materiales");
  if (!materialsQuery) {
    materialsQuery = await fetchWrapper.get(
      `${proveedoresUrl}/proveedores/proveedores-materiales/`,
    );
  } else {
    materialsQuery = JSON.parse(materialsQuery);
  }
  materialsFromProviders.value = materialsQuery;
  materialsFromProviders.value.forEach((material) => {
    material.checked = false;
    material.amount = 0;
    material.deliveryDate = null;
  });
};

const validateMaterialPresence = (
  materialsFromProviders,
  collectionMaterialList,
) => {
  const importedMaterials = materialsFromProviders.value.filter(
    (material) => material.es_importado,
  );
  return (
    importedMaterials.length >= 2 &&
    collectionMaterialList
      .map((material) => material.id)
      .every((id) =>
        materialsFromProviders.value
          .map((material) => material.material)
          .includes(id),
      )
  );
};

const validateMaterialAmount = (
  materialsFromProviders,
  collectionMaterialList,
) => {
  const materialsFromProvidersWithAmount = materialsFromProviders.value.map(
    ({ material, cantidad_disponible, checked, amount, deliveryDate }) => ({
      id: material,
      amount_available: cantidad_disponible,
      checked,
      amount,
      deliveryDate,
    }),
  );
  const collectionMaterialListWithAmount = collectionMaterialList.map(
    ({ id, amount }) => ({ id, amount }),
  );
  return collectionMaterialListWithAmount.every((material) => {
    const availableMaterial = materialsFromProvidersWithAmount.filter(
      (m) => m.id === material.id && m.checked,
    );
    const totalAmountAvailable = availableMaterial.reduce(
      (total, m) => total + m.amount_available,
      0,
    );
    const totalAmountNeeded = availableMaterial.reduce(
      (total, m) => total + m.amount,
      0,
    );
    return totalAmountAvailable >= totalAmountNeeded;
  });
};

const validateAtLeastTwoImported = () => {
  const atLeastTwoImported =
    materialsFromProviders.value.filter(
      (material) => material.checked && material.es_importado,
    ).length >= 2;
  if (!atLeastTwoImported) {
    alert(
      "Al menos dos materiales importados deben ser seleccionados, " +
        materialsFromProviders.value.filter(
          (material) => material.checked && material.es_importado,
        ).length +
        " están seleccionados",
    );
    return false;
  }
  return true;
};

const fixMatrix = (selectedMaterials) => {
  for (let materialId in selectedMaterials.value) {
    for (let providerId in selectedMaterials.value[materialId]) {
      const amount = selectedMaterials.value[materialId][providerId];
      if (amount === "") {
        selectedMaterials.value[materialId][providerId] = 0;
      }
    }
  }
};

const validateTotalAmount = (materialId, materialAmount) => {
  let totalMaterials = {};
  let totalAmount = 0;
  for (let materialProvided in selectedMaterials.value[materialId]) {
    if (
      materialsFromProviders.value.find((m) => m.id == materialProvided).checked
    ) {
      totalAmount += selectedMaterials.value[materialId][materialProvided];
    }
  }
  totalMaterials[materialId] = totalAmount;
  return totalAmount == materialAmount;
};

const getTotalAmount = (materialId) => {
  let totalAmount = 0;
  for (let materialProvided in selectedMaterials.value[materialId]) {
    totalAmount += selectedMaterials.value[materialId][materialProvided];
  }
  return totalAmount;
};

const validateAllMaterials = () => {
  fixMatrix(selectedMaterials);
  return Object.keys(selectedMaterials.value).every((material) =>
    validateTotalAmount(
      material,
      collectionMaterialList.value.find((m) => m.id == material).amount,
    ),
  );
};

const validateFactorySelected = () => {
  if (!selectedFactory.value) {
    alert("Debe seleccionar un lugar de fabricación");
    return false;
  }
  return true;
};

const validateDeliveryDate = (materialFromProvider) => {
  return (
    materialFromProvider.checked && materialFromProvider.deliveryDate !== null
  );
};

const validateFabricationDates = (finalList) => {
  const startDate = new Date(slot_start_date.value);
  const endDate = new Date(slot_end_date.value);
  const estimatedLaunchDateSelected = new Date(estimatedLaunchDate.value);
  let datesCorrect = true;
  if (startDate >= endDate) {
    alert("La fecha de inicio debe ser anterior a la fecha de fin");
    datesCorrect = false;
  }
  let isOutOfDate = false;
  finalList.forEach((item) => {
    const deliveryDate = new Date(item.deliveryDate);
    if (deliveryDate > startDate) {
      isOutOfDate = true;
    }
  });
  if (isOutOfDate) {
    alert(
      "La fecha de inicio debe ser posterior a la fecha de entrega de los materiales",
    );
    datesCorrect = false;
  }
  if (endDate > estimatedLaunchDateSelected) {
    alert(
      "La fecha de fin debe ser anterior a la fecha estimada de lanzamiento de la colección",
    );
    datesCorrect = false;
  }
  return datesCorrect;
};

const onSubmit = () => {
  const atLeastTwoImported = renegociated.value || validateAtLeastTwoImported();
  const allMaterialsValid = validateAllMaterials();
  const factorySelected = validateFactorySelected();
  const checkedDatesSet = materialsFromProviders.value
    .filter((material) => material.checked)
    .every((material) => validateDeliveryDate(material));

  const finalList = [];
  if (
    atLeastTwoImported &&
    allMaterialsValid &&
    factorySelected &&
    checkedDatesSet
  ) {
    for (let materialId in selectedMaterials.value) {
      for (let providerId in selectedMaterials.value[materialId]) {
        const amount = selectedMaterials.value[materialId][providerId];
        if (amount > 0) {
          const material = collectionMaterialList.value.find(
            (m) => m.id == materialId,
          );
          const materialFromProvider = materialsFromProviders.value.find(
            (m) => m.id == providerId,
          );
          finalList.push({
            actor: providerId,
            material: material.id,
            amount: amount,
            deliveryDate: materialFromProvider.deliveryDate,
          });
        }
      }
    }
  }

  const datesValidated = validateFabricationDates(finalList);

  if (datesValidated && finalList.length > 0) {
    fetchWrapper.patch(`${baseUrl}/coleccion/${collectionId}/`, {
      fecha_lanzamiento_estimada: estimatedLaunchDate.value,
    });
    const fabricationPlan = {
      factory_slot: {
        factory: selectedFactory.value.id,
        slot_start_date: slot_start_date.value,
        slot_end_date: slot_end_date.value,
      },
      lotQuantity: lotQuantity.value,
      materials: finalList,
    };
    advanceToConfirm(fabricationPlan);
  }
};

const advanceToConfirm = (fabricationPlan) => {
  setBonitaVariable(
    caseId,
    "plan_de_fabricacion",
    JSON.stringify(fabricationPlan),
  );
  router.push({ name: "fabrication-plan-confirm" });
};

const clearSelection = () => {
  selectedFactory.value = null;
};

const fechFabricationLocations = async () => {
  let fabricationLocations = await getBonitaVariable(
    caseId,
    "consulta_lugares_fabricacion",
  );

  if (!fabricationLocations) {
    fabricationLocations = await fetchWrapper.get(
      `${proveedoresUrl}/proveedores/lugar-fabricacion/`,
    );
  } else {
    fabricationLocations = JSON.parse(fabricationLocations);
  }
  factoryList.value = fabricationLocations;
};

onBeforeMount(async () => {
  const materialsPromise = fetchMaterialsFromProviders();
  const fabricationsPromise = fechFabricationLocations();
  await collectionStore.getAll();
  collection.value = collections.value.find(
    (collection) => collection.id == collectionId,
  );
  estimatedLaunchDate.value = collection.value.estimated_launch_date;
  renegociated.value =
    (await getBonitaVariable(caseId, "se_renegocio")) == "true";
  await materialsPromise;
  await fabricationsPromise;
  collectionMaterialList.value = JSON.parse(
    await getBonitaVariable(caseId, "cantidad_materiales"),
  );
  const allMaterialsProvided = validateMaterialPresence(
    materialsFromProviders,
    collectionMaterialList.value,
  );
  const canFulfillAllMaterials = validateMaterialAmount(
    materialsFromProviders,
    collectionMaterialList.value,
  );
  if (!allMaterialsProvided || !canFulfillAllMaterials) {
    router.push({ name: "designed-collections" });
  }
  const materials = collectionMaterialList.value;
  const materialsProvided = materialsFromProviders.value;
  selectedMaterials.value = {};
  materials.forEach((material) => {
    selectedMaterials.value[material.id] = {};
    materialsProvided.forEach((materialProvided) => {
      selectedMaterials.value[material.id][materialProvided.id] = 0;
    });
  });
  loading.value = false;
});
</script>
