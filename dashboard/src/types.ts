import { SensorChartData, SensorDataOrdered } from "./api";

interface FState {
  isLoadingSensorData: boolean;
  sensorData: SensorChartData[];
  isLoadingSensorDataOrdered: boolean;
  sensorDataOrdered: SensorDataOrdered[];
  useExampleData: boolean;
}

export type { FState };
