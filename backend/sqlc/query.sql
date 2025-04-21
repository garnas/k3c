-- name: CreateMeasurement :one
INSERT INTO measurements (
    temperature,
    humidity,
    pressure,
    gas_resistance,
    timestamp
) VALUES (
    $1, $2, $3, $4, $5
)
RETURNING *;

-- name: GetMeasurement :one
SELECT * FROM measurements
WHERE measurements_id = $1 LIMIT 1;

-- name: ListMeasurements :many
SELECT * FROM measurements
ORDER BY timestamp DESC; -- Or ASC, depending on desired default order

-- Example: List measurements within a time range
-- name: ListMeasurementsByTime :many
SELECT * FROM measurements
WHERE timestamp >= $1 AND timestamp <= $2
ORDER BY timestamp ASC;

-- name: DeleteMeasurementsByTime :many
SELECT * FROM measurements
WHERE timestamp <= $1;