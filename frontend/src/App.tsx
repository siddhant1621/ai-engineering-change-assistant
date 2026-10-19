import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

function App() {
  return (
    <div style={{ padding: "40px", fontFamily: "Arial, sans-serif" }}>
      <h1>AI Engineering Change Assistant</h1>

      <p>
        A full-stack engineering change management application for parts,
        BOMs, revisions, and AI-assisted impact analysis.
      </p>

      <hr />

      <h2>Planned Modules</h2>

      <ul>
        <li>Dashboard</li>
        <li>Parts</li>
        <li>BOM Viewer</li>
        <li>Engineering Changes</li>
        <li>AI Impact Analysis</li>
      </ul>
    </div>
  );
}

export default App;
