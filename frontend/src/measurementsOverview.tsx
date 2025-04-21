import React, {useEffect, useState} from "react";
import axios from "axios";
import MeasurementDto from "./measurementDto.tsx";
import MeasurementsDisplay from "./MeasurementDisplay.tsx";

type RawMeasurementDto = {
    temperature: string;
    pressure: string;
    humidity: string;
    gas_resistance: string;
    timestamp: string;
};

const MeasurementsOverview: React.FC = () => {
    const [data, setData] = useState<MeasurementDto[]>([]);

    useEffect(() => {
        axios.get<RawMeasurementDto[]>("/measurements-weekly").then((res) => {
            const converted: MeasurementDto[] = res.data.map((item) => ({
                temperature: parseFloat(item.temperature),
                pressure: parseFloat(item.pressure),
                humidity: parseFloat(item.humidity),
                gas_resistance: parseFloat(item.gas_resistance),
                timestamp: item.timestamp,
            }));
            setData(converted);
        });
    }, []);
    return (
        <div>
           {/* Other parts of your app */}

           {data.length > 0 ? (
                <MeasurementsDisplay measurements={data} />
           ) : (
                <p>Loading measurements...</p>
           )}

           {/* Other parts of your app */}
        </div>
    );
};
export default MeasurementsOverview;