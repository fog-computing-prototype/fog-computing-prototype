<script setup lang="ts">
import { FState } from "@/types";
import SensorChart from "@/components/SensorChart.vue";

defineProps<{ state: FState }>()
</script>

<template>
  <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
    <template v-for="sensorData in state.sensorData">
      <SensorChart :chart-data="sensorData" :height="250" :width="200"></SensorChart>
    </template>
  </div>
</template>
