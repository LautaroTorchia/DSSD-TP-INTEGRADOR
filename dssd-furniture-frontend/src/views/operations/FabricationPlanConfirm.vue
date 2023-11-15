<template>
    <div class="row">
        <div class="col-md-6">
            <div class="card mb-4 shadow">
                <div class="card-body">
                    <h2 class="card-title">Factory Slot</h2>
                    <p class="card-text">Factory: {{ fabricationPlan.factory_slot.factory }}</p>
                    <p class="card-text">Start Date: {{ fabricationPlan.factory_slot.slot_start_date }}</p>
                    <p class="card-text">End Date: {{ fabricationPlan.factory_slot.slot_end_date }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card mb-4 shadow">
                <div class="card-body">
                    <h2 class="card-title">Materials</h2>
                    <div class="overflow-auto" style="max-height: 400px;">
                        <div v-for="(material, index) in fabricationPlan.materials" :key="index" class="card mb-2 shadow">
                            <div class="card-body">
                                <p class="card-text">Actor: {{ material.actor }}</p>
                                <p class="card-text">Material: {{ material.material }}</p>
                                <p class="card-text">Amount: {{ material.amount }}</p>
                                <p class="card-text">Delivery Date: {{ material.deliveryDate }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
const fabricationPlan = JSON.parse(localStorage.getItem('fabricationPlan'));
</script>