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
    <div className="max-w-sm mx-auto bg-white p-6 rounded-2xl shadow-lg border">
      <h2 className="text-xl font-bold text-center mb-4">Live Measurement</h2>
      <div className="grid grid-cols-2 gap-4 text-gray-800">
        <div>🌡️ Temperature:</div>
        <div className="text-right font-medium">{measurement.temperature} °C</div>

        <div>🌬️ Pressure:</div>
        <div className="text-right font-medium">{measurement.pressure} hPa</div>

        <div>💧 Humidity:</div>
        <div className="text-right font-medium">{measurement.humidity} %</div>

        <div>🔥 Gas Resistance:</div>
        <div className="text-right font-medium">{measurement.gas_resistance} Ω</div>

        <div>🕒 Timestamp:</div>
        <div className="text-right font-mono text-sm text-gray-600">{new Date(measurement.timestamp).toLocaleString()}</div>
      </div>
    </div>
  );
};

export default LiveMeasurementCard;