
<script setup>
import MaterialsGraph from './MaterialsGraph.vue'
import QuarterlyCollections from './QuarterlyCollections.vue'
import AverageDesignTime from './AverageDesignTime.vue'
</script>

<template>
  <div>
    <h1>Dashboard</h1>
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <QuarterlyCollections />
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <MaterialsGraph />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

