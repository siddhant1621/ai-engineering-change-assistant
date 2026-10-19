function AiAnalysis() {
  return (
    <div>
      <div className="page-header">
        <h1>AI Impact Analysis</h1>
        <p>AI-assisted engineering risk and impact assessment.</p>
      </div>

      <div className="panel">
        <h2>Analysis Result</h2>

        <p>
          <strong>Risk Level:</strong> Medium
        </p>

        <h3>Affected Assemblies</h3>

        <ul>
          <li>ECU Assembly</li>
          <li>Vehicle Electronics Module</li>
        </ul>

        <h3>Potential Risks</h3>

        <ul>
          <li>Replacement part is currently in Prototype lifecycle state.</li>
          <li>Assembly documentation may require updates.</li>
          <li>Additional validation testing may be required.</li>
        </ul>

        <h3>Suggested Reviewers</h3>

        <ul>
          <li>Mechanical Engineering</li>
          <li>Quality Engineering</li>
          <li>Manufacturing Engineering</li>
        </ul>
      </div>
    </div>
  );
}

export default AiAnalysis;