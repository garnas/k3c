'use client'; // Keep this if using Next.js App Router

import React, {useState, useCallback, useEffect, useRef} from 'react';
import {io, Socket} from 'socket.io-client';
import MeasurementDto from "./measurementDto.tsx";
import LiveMeasurementCard from "./liveMeasurmentCard.tsx";

// Define the component using React.FC
export const WebSocketDemo: React.FC = () => {
    // URL of the Socket.IO server
    // Use http:// because the default Flask server is not HTTPS
    const [messageHistory, setMessageHistory] = useState<string[]>([]);
    const [measurementHistory, setMeasurementHistory] = useState<MeasurementDto[]>([]);
    const [liveMeasurement, setLiveMeasurement] = useState<MeasurementDto | null>(null);
    const [isConnected, setIsConnected] = useState<boolean>(false);
    const [inputValue, setInputValue] = useState<string>('');

    // useRef to hold the socket instance without causing re-renders on change
    const socketRef = useRef<Socket | null>(null);
    const serverUrl = window.location.origin

    useEffect(() => {
        // Initialize the socket connection
        // It automatically tries WebSocket and falls back if needed.
        // `transports: ['websocket']` forces WebSocket only, useful for debugging.
        const socket = io(serverUrl, {
            // transports: ['websocket'], // Optional: Force WebSocket only
            reconnectionAttempts: 5, // Optional: Configure reconnection
        });
        socketRef.current = socket; // Store the socket instance

        // --- Event Listeners ---
        socket.on('connect', () => {
            console.log('Socket.IO connected:', socket.id);
            setIsConnected(true);
            setMessageHistory(prev => [...prev, 'Connected to server!']);
        });

        socket.on('disconnect', (reason: string) => {
            console.log('Socket.IO disconnected:', reason);
            setIsConnected(false);
            setMessageHistory(prev => [...prev, `Disconnected: ${reason}`]);
            // Handle potential cleanup or reconnection logic if needed
        });

        socket.on('connect_error', (error: { message: string; }) => {
            console.error('Socket.IO connection error:', error);
            setMessageHistory(prev => [...prev, `Connection Error: ${error.message}`]);
            setIsConnected(false);
        });

        // Listener for your custom response event from the server
        socket.on('my_response', (data: { data: string }) => {
            console.log('Received my_response:', data);
            setMessageHistory(prev => [...prev, `Server: ${data.data}`]);
        });

        // Listener for your custom response event from the server
        socket.on('live_measurement', (incomingLiveMeasurement: MeasurementDto) => {
            console.log('Received live_measurement:');
            console.log('Received live_measurement:', incomingLiveMeasurement);
            setLiveMeasurement(incomingLiveMeasurement)
        });


        // Listener for the default 'message' event from the server (if you use it)
        socket.on('message', (data: string) => {
            console.log('Received default message:', data);
            setMessageHistory(prev => [...prev, `Server (default): ${data}`]);
        });

        socket.on('server_broadcast', (data: { data: string }) => {
            console.log('Received server broadcast:', data);
            // Add the broadcast message to the history
            setMessageHistory(prev => [...prev, `BROADCAST: ${data.data}`]);
        });

        socket.on('sensor', (data: MeasurementDto) => {
            console.log('Received sensor data:', data);
            // Add the broadcast message to the history
            setMeasurementHistory(prev => [...prev, data]);
        });

        // --- Cleanup on component unmount ---
        return () => {
            console.log('Disconnecting socket...');
            socket.disconnect();
            socketRef.current = null;
            setIsConnected(false);
        };
    }, [serverUrl]); // Re-run effect if serverUrl changes

    // Callback to send a message using the custom event 'my_message'
    const handleClickSendMessage = useCallback(() => {
        if (socketRef.current && isConnected && inputValue.trim()) {
            const messageToSend = inputValue;
            console.log('Sending my_message:', messageToSend);
            // Emit the custom event
            socketRef.current.emit('my_message', {text: messageToSend});
            setMessageHistory(prev => [...prev, `Me: ${messageToSend}`]);
            setInputValue(''); // Clear input after sending
        } else {
            console.log('Cannot send message. Socket not connected or input empty.');
        }
    }, [isConnected, inputValue]);

    // Callback to send using the default 'message' event
    const handleSendDefaultMessage = useCallback(() => {
        if (socketRef.current && isConnected) {
            console.log('Sending default message: Hello Default');
            // Emit the default 'message' event
            socketRef.current.emit('message', 'Hello Default');
            setMessageHistory(prev => [...prev, `Me (default): Hello Default`]);
        } else {
            console.log('Cannot send default message. Socket not connected.');
        }
    }, [isConnected]);


    return (
        <div>
            <h2>Socket.IO Demo</h2>
            <p>Server URL: {serverUrl}</p>
            {/* Add button to manually change URL if needed */}
            {/* <button onClick={() => setServerUrl('http://new-url:port')}>Change URL</button> */}
            <h1>Live Measurment</h1>
            <h1>{liveMeasurement?.temperature}</h1>
            <LiveMeasurementCard measurement={liveMeasurement}/>
            <div>
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Type a message..."
                />
                <button
                    onClick={handleClickSendMessage}
                    disabled={!isConnected || !inputValue.trim()}
                >
                    Send Custom Message ('my_message')
                </button>
                <button
                    onClick={handleSendDefaultMessage}
                    disabled={!isConnected}
                >
                    Send Default Message ('message')
                </button>
            </div>

            <p>Connection Status: <b>{isConnected ? 'Connected' : 'Disconnected'}</b></p>
            <h3>Measurements History:</h3>
            <ul>
                {measurementHistory.map((mst, idx) => (
                    <li key={idx}>{mst.temperature}</li>
                ))}
            </ul>
            <h3>Message History:</h3>
            <ul>
                {messageHistory.map((msg, idx) => (
                    <li key={idx}>{msg}</li>
                ))}
            </ul>
        </div>
    );
};

export default WebSocketDemo;