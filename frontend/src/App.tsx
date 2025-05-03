import './App.css'
import WebSocketDemo from "./websockets.tsx";
import MeasurementsOverview from "./measurementsOverview.tsx";

function App() {

  return (
    <>
        <WebSocketDemo/>
        <MeasurementsOverview/>
    </>
  )
}

export default App
