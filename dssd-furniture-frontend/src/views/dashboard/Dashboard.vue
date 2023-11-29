<script setup>
import MaterialsGraph from "./MaterialsGraph.vue";
import QuarterlyCollections from "./QuarterlyCollections.vue";
import AverageDesignTime from "./AverageDesignTime.vue";
import AveragePlanTime from "./AveragePlanTime.vue";
import AverageFabricationAndDistributionTime from "./AverageFabricationAndDistributionTime.vue";
localStorage.setItem("bonitaTasks", "");
</script>

<template>
  <div>
    <h1>Dashboard</h1>

    <div class="row row-separator">
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

    <div class="row row-separator">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <AverageDesignTime />
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <AveragePlanTime />
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="row row-separator">
    <div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <AverageFabricationAndDistributionTime />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.row-separator {
  margin-bottom: 5px;
}
</style>
