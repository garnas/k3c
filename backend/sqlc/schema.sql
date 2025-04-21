create table measurements
(
    measurements_id bigserial,
    temperature     numeric,
    humidity        numeric,
    pressure        numeric,
    gas_resistance  numeric,
    timestamp       timestamp
);