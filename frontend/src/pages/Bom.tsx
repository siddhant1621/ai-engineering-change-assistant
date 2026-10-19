function Bom() {
  return (
    <div>
      <div className="page-header">
        <h1>BOM Viewer</h1>
        <p>Visualize product and assembly structures.</p>
      </div>

      <div className="panel">
        <h2>ECU Assembly</h2>

        <div className="bom-tree">
          <p>ECU Assembly</p>
          <p className="indent-1">├── ECU-100 Main ECU</p>
          <p className="indent-1">├── BRK-001 ECU Bracket</p>
          <p className="indent-1">├── BLT-006 Bolt M6</p>
          <p className="indent-1">└── HAR-201 Wiring Harness</p>
          <p className="indent-2">├── CON-101 Connector A</p>
          <p className="indent-2">└── CON-102 Connector B</p>
        </div>
      </div>
    </div>
  );
}

export default Bom;