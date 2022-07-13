<script setup lang="ts">
import FCard from '@/components/FCard.vue';
import { store } from "@/store"
import { ref } from "vue"
import { onMounted } from 'vue';

let input = ref("")

const handleClickSave = () => {
  store.setApiUrl(input.value);
}

const handleClickReset = () => {
  let defaultApiUrl: string = store.getApiUrlDefault()
  input.value = defaultApiUrl;
  store.setApiUrl(defaultApiUrl);
}

onMounted(() => { input.value = store.apiUrl })
</script>

<template>
  <FCard class="mt-4">
    <h3 class="text-lg font-bold mb-4">Settings</h3>
    <div class="flex flex-row content-center">
      <div class="basis-1/4"></div>

      <div class="basis-2/4">
        <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
              API address
            </label>
            <input v-model="input"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="username" type="text" placeholder="API address">
          </div>
          <div class="flex flex-row justify-center">
            <div>
              <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                type="button" @click="handleClickReset">
                Reset
              </button>
            </div>

            <div class="ml-6">
              <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                type="button" @click="handleClickSave">
                Save
              </button>
            </div>
          </div>
        </form>
      </div>
      <div class="basis-1/4"></div>
    </div>
  </FCard>
</template>

