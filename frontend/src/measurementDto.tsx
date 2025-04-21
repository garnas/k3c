export default class MeasurementDto {
    temperature: number;
    pressure: number;
    humidity: number;
    gas_resistance: number;
    timestamp: string;

    constructor({temperature, pressure, humidity, gas_resistance, timestamp}: {
        temperature: number;
        pressure: number;
        humidity: number;
        gas_resistance: number;
        timestamp: string
    }) {
        this.temperature = temperature;
        this.pressure = pressure;
        this.humidity = humidity;
        this.gas_resistance = gas_resistance;
        this.timestamp = timestamp;
    }
}