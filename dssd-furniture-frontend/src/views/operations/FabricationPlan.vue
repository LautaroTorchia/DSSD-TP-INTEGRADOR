<template>
    <div>
        <h1>Plan de fabricación</h1>
        <h2>Lugares de fabricación:</h2>
        <div class="card">
            <div class="card-body">
                <div v-for="(factory, index) in factoryList" :key="index">
                    <input type="radio" :id="'factory-' + index" :value="factory" v-model="selectedFactory">
                    <label :for="'factory-' + index">{{ factory.nombre }}</label>
                </div>
                <button @click="clearSelection">Clear</button>
            </div>
        </div>

        <h2>Lista de materiales:</h2>
        <div class="card">
            <div class="card-body">
                <div v-for="material in collectionMaterialList" :key="material.id">
                    <h5 class="card-title">Material: {{ material.name.charAt(0).toUpperCase() + material.name.slice(1) }}
                    </h5>
                    <h5 class="card-title">Cantidad: {{ material.amount }} </h5>
                    <div class="card-text">
                        <div v-for="materialFromProvider in materialsFromProviders" :key="materialFromProvider.material">
                            <div v-if="material.id === materialFromProvider.material">
                                <div class="card">
                                    <div class="card-body">
                                        {{ materialFromProvider }}
                                        <h6 class="card-subtitle mb-2 text-muted"> Proveedor o reciclador: {{
                                            materialFromProvider.actor_nombre }}</h6>
                                        <h6 class="card-subtitle mb-2 text-muted"> Proveedor o reciclador: {{
                                            materialFromProvider.actor }}</h6>

                                        <h6 class="card-subtitle mb-2 text-muted"> Cantidad: {{
                                            materialFromProvider.cantidad_disponible }}</h6>
                                        <h6 class="card-subtitle mb-2 text-muted" v-if="materialFromProvider.es_importado">
                                            Es importado </h6>
                                        <h6 class="card-subtitle mb-2 text-muted" v-else> No es importado </h6>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox"
                                                :id="'materialProvided-' + materialFromProvider.id"
                                                v-model="materialFromProvider.checked">
                                            <label class="form-check-label"
                                                :for="'materialProvided-' + materialFromProvider.id">Seleccionar</label>
                                            <div v-if="materialFromProvider.checked">
                                                <label for="amount">Amount:</label>
                                                <input type="number" class="form-control"
                                                    v-model.number="selectedMaterials[material.id][materialFromProvider.id]"
                                                    min="1" :max="materialFromProvider.cantidad_disponible">

                                                <label for="deliveryDate">Delivery Date:</label>
                                                <input type="date" class="form-control"
                                                    v-model="materialFromProvider.deliveryDate"
                                                    :min="new Date(Date.now() + materialFromProvider.plazo_entrega_dias * 24 * 60 * 60 * 1000).toISOString().split('T')[0]">

                                                <div v-if="!validateTotalAmount(material.id, material.amount)">
                                                    <p class="text-danger">Total amount for {{ material.name }} must be {{
                                                        material.amount }}, but is {{ getTotalAmount(material.id) }}</p>
                                                </div>

                                                <div v-if="!validateDeliveryDate(materialFromProvider)">
                                                    <p class="text-danger">Delivery date is required for selected material
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
        </div>
        <button @click="onSubmit">Submit</button>

    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchWrapper, router } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}`
const collectionId = router.currentRoute.value.params.collection
const caseId = JSON.parse(localStorage.getItem('collections')).collections.find((collection) => collection.id == collectionId).caseId

const materialsFromProviders = ref([])
const collectionMaterialList = ref([])
const selectedMaterials = ref([])
const factoryList = ref([])
const selectedFactory = ref(null)


const fetchMaterialsFromProviders = async () => {
    try {
        materialsFromProviders.value = await fetchWrapper.get(`${baseUrl}/proveedores/proveedores-materiales/`)
        materialsFromProviders.value.forEach((material) => {
            material.checked = false
            material.amount = 0
            material.deliveryDate = null
        })
    } catch (error) {
        console.error(error)
    }
}

const validateMaterialPresence = (materialsFromProviders, collectionMaterialList) => {
    const importedMaterials = materialsFromProviders.value.filter((material) => material.es_importado)
    return importedMaterials.length >= 2 && collectionMaterialList.map((material) => material.id).every((id) => materialsFromProviders.value.map((material) => material.material).includes(id))
}

const validateMaterialAmount = (materialsFromProviders, collectionMaterialList) => {
    const materialsFromProvidersWithAmount = materialsFromProviders.value.map(({ material, cantidad_disponible, checked, amount, deliveryDate }) => ({ id: material, amount_available: cantidad_disponible, checked, amount, deliveryDate }))
    const collectionMaterialListWithAmount = collectionMaterialList.map(({ id, amount }) => ({ id, amount }))
    return collectionMaterialListWithAmount.every((material) => {
        const availableMaterial = materialsFromProvidersWithAmount.filter((m) => m.id === material.id && m.checked)
        const totalAmountAvailable = availableMaterial.reduce((total, m) => total + m.amount_available, 0)
        const totalAmountNeeded = availableMaterial.reduce((total, m) => total + m.amount, 0)
        return totalAmountAvailable >= totalAmountNeeded
    })
}

const validateAtLeastTwoImported = () => {
    const atLeastTwoImported = materialsFromProviders.value.filter((material) => material.checked && material.es_importado).length >= 2
    if (!atLeastTwoImported) {
        alert("Al menos dos materiales importados deben ser seleccionados, " + materialsFromProviders.value.filter((material) => material.checked && material.es_importado).length + " están seleccionados")
        return false
    }
    return true
}

const fixMatrix = (selectedMaterials) => {
    for (let materialId in selectedMaterials.value) {
        for (let providerId in selectedMaterials.value[materialId]) {
            const amount = selectedMaterials.value[materialId][providerId]
            if (amount === "") {
                selectedMaterials.value[materialId][providerId] = 0
            }
        }
    }
}

const validateTotalAmount = (materialId, materialAmount) => {
    fixMatrix(selectedMaterials)
    let totalMaterials = {}
    let totalAmount = 0
    for (let materialProvided in selectedMaterials.value[materialId]) {
        if (materialsFromProviders.value.find(m => m.id == materialProvided).checked) {
            totalAmount += selectedMaterials.value[materialId][materialProvided]
        }
    }
    totalMaterials[materialId] = totalAmount
    return totalAmount == materialAmount
}

const getTotalAmount = (materialId) => {
    let totalAmount = 0
    for (let materialProvided in selectedMaterials.value[materialId]) {
        totalAmount += selectedMaterials.value[materialId][materialProvided]
    }
    return totalAmount
}

const validateAllMaterials = () => {
    return Object.keys(selectedMaterials.value).every(material => validateTotalAmount(material, collectionMaterialList.value.find(m => m.id == material).amount))
}

const validateFactorySelected = () => {
    if (!selectedFactory.value) {
        alert("Debe seleccionar un lugar de fabricación")
        return false
    }
    return true
}

const validateDeliveryDate = (materialFromProvider) => {
    return materialFromProvider.checked && materialFromProvider.deliveryDate !== null
}

const onSubmit = () => {
    const atLeastTwoImported = validateAtLeastTwoImported()
    const allMaterialsValid = validateAllMaterials()
    const factorySelected = validateFactorySelected()
    const checkedDatesSet = materialsFromProviders.value.filter(material => material.checked).every(material => validateDeliveryDate(material))
    console.log(checkedDatesSet, "checkedDatesSet")

    const finalList = []
    if (atLeastTwoImported && allMaterialsValid && factorySelected && checkedDatesSet) {
        for (let materialId in selectedMaterials.value) {
            for (let providerId in selectedMaterials.value[materialId]) {
                const amount = selectedMaterials.value[materialId][providerId]
                if (amount > 0) {
                    const material = collectionMaterialList.value.find(m => m.id == materialId)
                    const materialFromProvider = materialsFromProviders.value.find(m => m.id == providerId)
                    finalList.push({
                        actor: providerId,
                        material: material.id,
                        amount: amount,
                        deliveryDate: materialFromProvider.deliveryDate
                    })
                }
            }
        }
    }
    if (finalList.length > 0) {
        console.log(finalList)
        console.log(factorySelected)
    }

}

const clearSelection = () => {
    selectedFactory.value = null
}

onMounted(async () => {
    await fetchMaterialsFromProviders()
    collectionMaterialList.value = await fetchWrapper.get(`${baseUrl}/bonita/case-variable/${caseId}/cantidad_materiales/`)
    factoryList.value = await fetchWrapper.get(`${baseUrl}/reservas/lugar-fabricacion/`)
    console.log("factoryList", factoryList.value)
    collectionMaterialList.value = JSON.parse(collectionMaterialList.value.value)
    const allMaterialsProvided = validateMaterialPresence(materialsFromProviders, collectionMaterialList.value)
    const canFulfillAllMaterials = validateMaterialAmount(materialsFromProviders, collectionMaterialList.value)

    if (!allMaterialsProvided && !canFulfillAllMaterials) {
        router.push({ name: 'designed-collections' })
    }
    const materials = collectionMaterialList.value
    const materialsProvided = materialsFromProviders.value

    selectedMaterials.value = {}

    materials.forEach(material => {
        selectedMaterials.value[material.id] = {}
        materialsProvided.forEach(materialProvided => {
            selectedMaterials.value[material.id][materialProvided.id] = 0
        })
    })

})
</script>
