import { reactive } from "vue";
import { FState } from "./types";

export const store = reactive({
  apiUrl: localStorage.getItem("apiUrl") ?? "http://127.0.0.1:8000",

  getApiUrlDefault() {
    return "http://127.0.0.1:8000";
  },

  setApiUrl(value: string) {
    localStorage.setItem("apiUrl", value);
    this.apiUrl = value;
  },
});


export const state: FState = reactive({
  isLoadingSensorData: false,
  sensorData: [],
  isLoadingSensorDataOrdered: false,
  sensorDataOrdered: [],
  useExampleData: false,
})
