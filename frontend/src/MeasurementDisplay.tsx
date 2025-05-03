// src/components/MeasurementsDisplay.tsx
import React from 'react';
import MeasurementDto from "./measurementDto.tsx";

interface MeasurementsDisplayProps {
    measurements: MeasurementDto[]; // Expecting the data for the last week
}

// Interface for the calculated average values
interface AverageMeasurements {
    temperature: number | string; // Use string for placeholder '-'
    pressure: number | string;
    humidity: number | string;
    gas_resistance: number | string;
    count: number; // Number of measurements included in the average
}

// Helper function to calculate averages
const calculateAverages = (data: MeasurementDto[]): AverageMeasurements => {
    if (!data || data.length === 0) {
        // Return placeholders if no data
        return {
            temperature: '-',
            pressure: '-',
            humidity: '-',
            gas_resistance: '-',
            count: 0,
        };
    }

    const sums = data.reduce(
        (acc, current) => {
            acc.temperature += current.temperature;
            acc.pressure += current.pressure;
            acc.humidity += current.humidity;
            acc.gas_resistance += current.gas_resistance;
            return acc;
        },
        {temperature: 0, pressure: 0, humidity: 0, gas_resistance: 0}
    );

    const count = data.length;

    // Calculate averages and format to 1 decimal place
    return {
        temperature: parseFloat((sums.temperature / count).toFixed(1)),
        pressure: parseFloat((sums.pressure / count).toFixed(1)),
        humidity: parseFloat((sums.humidity / count).toFixed(1)),
        gas_resistance: parseFloat((sums.gas_resistance / count).toFixed(1)),
        count: count,
    };
};

const MeasurementsDisplay: React.FC<MeasurementsDisplayProps> = ({measurements}) => {
    // Get current time and calculate time thresholds
    const now = new Date();
    const twentyFourHoursAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);
    const sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

    // Filter measurements for each period
    const last24hMeasurements = measurements.filter(m => {
        const measurementDate = new Date(m.timestamp); // Assumes timestamp is parsable by new Date()
        return measurementDate >= twentyFourHoursAgo;
    });

    // Assuming "Last Week" means the same as "Last 7 Days" given the input description
    const last7dMeasurements = measurements.filter(m => {
        const measurementDate = new Date(m.timestamp);
        return measurementDate >= sevenDaysAgo;
    });

    // Calculate averages for each period
    const avgLast24h = calculateAverages(last24hMeasurements);
    const avgLast7d = calculateAverages(last7dMeasurements);
    const avgHourly: AverageMeasurements[] = []
    for (let i = 0; i < 24; i++) {
        const lastHourI = new Date(new Date().getTime() - i * 60 * 60 * 1000);
        const lastHourII = new Date(new Date().getTime() - (i - 1) * 60 * 60 * 1000);
        const lastHourIMeasurements = measurements.filter(m => {
            const measurementDate = new Date(m.timestamp);
            return measurementDate >= lastHourI && measurementDate <= lastHourII;
        });
        avgHourly[i] = calculateAverages(lastHourIMeasurements)
    }

    // Helper to render a table row for averages
    const renderAverageRow = (avgData: AverageMeasurements, periodLabel: string) => (
        <tr key={periodLabel}>
            <td>{periodLabel}</td>
            <td>{avgData.temperature}</td>
            <td>{avgData.pressure}</td>
            <td>{avgData.humidity}</td>
            <td>{avgData.gas_resistance}</td>
            <td>{avgData.count > 0 ? avgData.count : '-'}</td>
        </tr>
    );

    return (
        <div>
            <h1>Average Measurements</h1>

            {/* You can add some basic styling via CSS classes or inline styles */}
            <style>{`
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                    font-family: sans-serif;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: right;
                }
                th {
                    background-color: #f2f2f2;
                    text-align: center;
                }
                 td:first-child {
                    text-align: left;
                    font-weight: bold;
                 }
            `}</style>

            <h2>Summary</h2>
            <table>
                <thead>
                <tr>
                    <th>Period</th>
                    <th>Avg. Temp (°C)</th>
                    {/* Add units if known */}
                    <th>Avg. Pressure (hPa)</th>
                    {/* Add units if known */}
                    <th>Avg. Humidity (%)</th>
                    {/* Add units if known */}
                    <th>Avg. Gas Res. (kOhm)</th>
                    {/* Add units if known */}
                    <th>Data Points</th>
                </tr>
                </thead>
                <tbody>
                {renderAverageRow(avgLast24h, 'Last 24 Hours')}
                {renderAverageRow(avgLast7d, 'Last 7 Days')}
                {/* Loop for the last 24 hours */}
                {Array.from({length: 24}, (_, i) => i + 1) // Creates an array [1, 2, 3, ..., 24]
                    .map(index => {
                        const hour = index - 1
                        // Check if data actually exists for this hour in avgHourly
                        if (avgHourly && avgHourly[hour]) {
                            // Dynamically create the label with pluralization
                            const lastHourI = new Date(new Date().getTime() - hour * 60 * 60 * 1000);
                            const lastHourII = new Date(new Date().getTime() - (hour - 1) * 60 * 60 * 1000);
                            const label = `${lastHourI.getHours()}:${lastHourI.getMinutes()} to ${lastHourII.getHours()}:${lastHourII.getMinutes()}`;
                            // Render the row using your existing function
                            return renderAverageRow(avgHourly[hour], label);
                        }
                        // If no data for this hour, return null (React ignores nulls)
                        return null;
                    })
                    // Optional: .filter(Boolean) // You could add this to remove the nulls explicitly if preferred
                }
                </tbody>
            </table>

            {/* Optional: Display Raw Data if needed
             <h2>Raw Data (Last 10)</h2>
             <ul>
                 {measurements.slice(-10).map((m, index) => (
                    <li key={index}>
                         {new Date(m.timestamp).toLocaleString()}: T:{m.temperature}, P:{m.pressure}, H:{m.humidity}, G:{m.gas_resistance}
                     </li>
                 ))}
             </ul>
             */}
        </div>
    );
};

export default MeasurementsDisplay;