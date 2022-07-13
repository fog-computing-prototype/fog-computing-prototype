<script setup lang="ts">
import { FState } from "@/types";
import { reactive } from 'vue';

// components
import FCard from "@/components/FCard.vue";
import LoadingIndicator from "@/components/LoadingIndicator.vue";

const props = defineProps<{ state: FState }>()

const sensorColorMap = reactive({})
</script>

<template>
  <FCard class="mt-4">
    <template v-if="state.isLoadingSensorData">
      <LoadingIndicator />
    </template>
    <template v-else>
      <div class="flex flex-col">
        <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="py-2 inline-block min-w-full sm:px-6 lg:px-8">
            <div class="overflow-hidden">
              <table class="min-w-full">
                <thead class="border-b">
                  <tr>
                    <th scope="col" class="text-sm font-medium text-gray-900 px-6 py-4 text-left">
                      #
                    </th>
                    <th scope="col" class="text-sm font-medium text-gray-900 px-6 py-4 text-left">
                      Name
                    </th>
                    <th scope="col" class="text-sm font-medium text-gray-900 px-6 py-4 text-left">
                      Sequence
                    </th>
                    <th scope="col" class="text-sm font-medium text-gray-900 px-6 py-4 text-left">
                      Timestamp
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(data, index) in state.sensorDataOrdered">
                    <tr class="border-b">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ index }}</td>
                      <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                        <div>
                          <fa :color="data.color" icon="fa-solid fa-circle"></fa>
                          <span class="ml-4">{{ data.name }}</span>
                        </div>
                      </td>
                      <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                        {{ data.sequence }}
                      </td>
                      <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                        {{ new Date(data.timestamp).toUTCString() }}
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </template>
  </FCard>
</template>