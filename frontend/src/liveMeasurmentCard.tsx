import React from "react";
import MeasurementDto from "./measurementDto";

const LiveMeasurementCard: React.FC<{ measurement: MeasurementDto | null }> = ({ measurement }) => {
  if (!measurement) {
    return (
      <div className="p-4 bg-gray-100 rounded-2xl shadow-md text-center text-gray-500">
        Waiting for live data...
      </div>
    );
  }

  return (
    <div className="mx-auto bg-white p-6 rounded-2xl shadow-lg border">
      <h2 className="text-xl font-bold mb-4">Live Measurement</h2>
      <div className="grid grid-cols-3 gap-4 text-gray-800">
        <div className="text-left">🌡️ Temperature:</div>
        <div className="text-right font-medium">{measurement.temperature.toFixed(2)} °C</div>

        <div className="text-left">🌬️ Pressure:</div>
        <div className="text-right font-medium">{measurement.pressure.toFixed(2)} hPa</div>

        <div className="text-left">💧 Humidity:</div>
        <div className="text-right font-medium">{measurement.humidity.toFixed(2)} %</div>

        <div className="text-left">🔥 Gas Resistance:</div>
        <div className="text-right font-medium">{measurement.gas_resistance.toFixed(2)} Ω</div>

        <div className="text-left">🕒 Timestamp:</div>
        <div className="text-right font-mono font-medium text-gray-600">{MeasurementDto.toDateString(measurement)}</div>
      </div>
    </div>
  );
};

export default LiveMeasurementCard;