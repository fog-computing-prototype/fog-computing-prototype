<script setup lang="ts">
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale,
  Plugin
} from 'chart.js'
import { SensorChartData } from "@/api";
import { computed } from "vue";
import FCard from "@/components/FCard.vue";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale
)

const props = defineProps<{ width: number, height: number, chartData: SensorChartData }>()

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}

const sensorChartData = computed(() => {
  const values = props.chartData.values.map((data) => parseFloat(data.value))
  const xLabels = props.chartData.values.map((data) => data.sequence)

  return {
    labels: xLabels,
    datasets: [{
      label: props.chartData.name,
      backgroundColor: props.chartData.color,
      data: values
    }]
  }
})
</script>

<template>
  <FCard>
    <Line :chart-options="chartOptions" :chart-data="sensorChartData" :chart-id="props.chartData.name" :width="width"
      :height="height">

    </Line>
  </FCard>
</template>