<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import { onMounted } from 'vue';
import axios from 'axios';
import colors from "tailwindcss/colors";

// components
import SensorChartList from '@/components/SensorChartList.vue'
import FCard from '@/components/FCard.vue';
import SensorTable from '@/components/SensorTable.vue';
import LoadingIndicator from "@/components/LoadingIndicator.vue";

import { SensorChartData } from '@/api';
import { getExampleData, getExampleDataOrdered } from "@/utils/example";
import { store, state } from "@/store"

function addColorToSensorData(sensorChartData: SensorChartData[]) {
  return sensorChartData.map(sensorData => {
    sensorData.color = availableColors[hash(sensorData.name) % availableColors.length][shade]
    return sensorData
  })
}

onMounted(() => {
  state.isLoadingSensorData = true;
  state.isLoadingSensorDataOrdered = true;

  setInterval(() => {
    state.useExampleData = false

    axios.get(`${store.apiUrl}/sensor-data`)
      .then(response => state.sensorData = addColorToSensorData(response.data))
      .catch(error => {
        console.log(error)
        state.sensorData = addColorToSensorData(getExampleData())
        state.useExampleData = true
      })
      .finally(() => state.isLoadingSensorData = false)


    axios.get(`${store.apiUrl}/sensor-data/ordered`)
      .then(
        response => state.sensorDataOrdered = response.data)
      .catch(error => {
        console.log(error)
        state.sensorDataOrdered = getExampleDataOrdered()
        state.useExampleData = true
      }
      )
      .finally(() => {
        state.isLoadingSensorDataOrdered = false
        let mapColorMap = {}
        state.sensorData.forEach((value) => {
          mapColorMap[value.name] = value.color;
        })

        state.sensorDataOrdered.forEach(element => {
          element.color = mapColorMap[element.name]
        });
      })
  }, 5000)
})

const hash = (text: String) => {
  let h = 0;
  for (let index = 0; index < text.length; index++) {
    h += text.codePointAt(index) ?? 1;
  }
  return h;
}

const availableColors = [
  colors.black,
  colors.emerald,
  colors.fuchsia,
  colors.lime,
  colors.pink,
  colors.orange,
  colors.indigo,
  colors.green,
  colors.purple
]
const shade = 500
</script>

<template>
  <div class="flex flex-col lg:flex-row mt-4">
    <div class="basis lg:basis-2/12 mb-4 lg:mb-0 lg:mr-4">
      <FCard>
        <h3 class="text-lg font-bold mb-4">
          <span>
            Sensors
          </span>
          <span v-if="state.useExampleData">
            (Example data)
          </span>
        </h3>
        <template v-if="state.isLoadingSensorData">
          <LoadingIndicator />
        </template>
        <template v-else>
          <template v-for="chartData in state.sensorData" :key="chartData.name">
            <div>
              <fa :color="chartData.color" icon="fa-solid fa-circle"></fa>
              <span class="ml-4">{{ chartData.name }}</span>
            </div>
          </template>
        </template>
      </FCard>
    </div>
    <div class="basis lg:basis-10/12">
      <SensorChartList :state="state" />
      <SensorTable :state="state" />
    </div>
  </div>
</template>
