import {RawMeasurementDto} from "./rawMeasurementDto.tsx";

export default class MeasurementDto {
    temperature: number;
    pressure: number;
    humidity: number;
    gas_resistance: number;
    timestamp: Date;

    constructor({temperature, pressure, humidity, gas_resistance, timestamp}: {
        temperature: number;
        pressure: number;
        humidity: number;
        gas_resistance: number;
        timestamp: number;
    }) {
        this.temperature = temperature;
        this.pressure = pressure;
        this.humidity = humidity;
        this.gas_resistance = gas_resistance;
        this.timestamp = new Date(timestamp * 1000); // <- convert to Date
    }

    static fromRaw(raw: RawMeasurementDto): MeasurementDto {
        return new MeasurementDto({
            temperature: parseFloat(raw.temperature),
            pressure: parseFloat(raw.pressure),
            humidity: parseFloat(raw.humidity),
            gas_resistance: parseFloat(raw.gas_resistance),
            timestamp: parseFloat(raw.timestamp),
        });
    }

}