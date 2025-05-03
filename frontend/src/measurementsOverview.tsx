import React, {useEffect, useState} from "react";
import axios from "axios";
import MeasurementDto from "./measurementDto.tsx";
import MeasurementsDisplay from "./MeasurementDisplay.tsx";
import {RawMeasurementDto} from "./rawMeasurementDto.tsx";


const MeasurementsOverview: React.FC = () => {
    const [data, setData] = useState<MeasurementDto[]>([]);

    useEffect(() => {
        axios.get<RawMeasurementDto[]>("/measurements-weekly").then((res) => {
            const converted: MeasurementDto[] = res.data.map(
                (item) => MeasurementDto.fromRaw(item)
            );
            setData(converted);
        });
    }, []);
    console.log(data)
    return (
        <div>
            {/* Other parts of your app */}

            {data.length > 0 ? (
                <MeasurementsDisplay measurements={data}/>
            ) : (
                <p>Loading measurements...</p>
            )}
        </div>
    );
};
export default MeasurementsOverview;