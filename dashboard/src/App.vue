<script setup lang="ts">
import FCard from '@/components/FCard.vue';

import { store, state } from "@/store";
import { computed } from 'vue';

const dataFrom = computed(() => state.useExampleData ? "example data" : store.apiUrl)
</script>

<template>
  <!-- This example requires Tailwind CSS v2.0+ -->
  <nav>
    <FCard>
      <div class="container-fluid w-full flex flex-wrap justify-between px-6 relative">
        <div>
          <router-link to="/">Fog Computing - Graph Dashboard</router-link>
        </div>
        <div class="flex place-content-end">
          <div v-if="!state.isLoadingSensorData && !state.isLoadingSensorDataOrdered"
            class="mr-4 font-light text-slate-400">
            Data from: {{ dataFrom }}
          </div>
          <div>
            <router-link to="/settings">Settings</router-link>
          </div>
        </div>
      </div>
    </FCard>
  </nav>
  <v-main>
    <router-view />
  </v-main>
</template>

<style>
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */

#app {
  padding: 12px;
}

html {
  background-color: rgb(248, 249, 250);
}
</style>
