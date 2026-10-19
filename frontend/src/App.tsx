import { Route, Routes } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Parts from "./pages/Parts";
import PartDetail from "./pages/PartDetail";
import Bom from "./pages/Bom";
import Changes from "./pages/Changes";
import AiAnalysis from "./pages/AiAnalysis";
import ChangeDetail from "./pages/ChangeDetail";

import "./App.css";

function App() {
  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/parts" element={<Parts />} />
          <Route path="/parts/:partNumber" element={<PartDetail />} />
          <Route path="/bom" element={<Bom />} />
          <Route path="/changes" element={<Changes />} />
          <Route path="/changes/:changeNumber" element={<ChangeDetail />} />
          <Route path="/ai-analysis" element={<AiAnalysis />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;