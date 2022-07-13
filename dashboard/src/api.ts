interface SensorData {
  value: string;
  sequence: number;
  timestamp: string;
}

interface SensorDataOrdered {
  value: string;
  sequence: number;
  timestamp: string;
  name: string;
  color: string | null;
}

interface SensorChartData {
  name: string;
  values: SensorData[];
  color: string | null;
}

export type { SensorChartData, SensorData, SensorDataOrdered };
