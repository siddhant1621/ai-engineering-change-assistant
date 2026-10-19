function Changes() {
  return (
    <div>
      <div className="page-header">
        <h1>Engineering Changes</h1>
        <p>Create and review engineering change requests.</p>
      </div>

      <div className="panel">
        <h2>EC-001 - Replace ECU Bracket</h2>

        <p>
          <strong>Status:</strong> Review
        </p>

        <p>
          <strong>Reason:</strong> Existing bracket showed vibration failures
          during endurance testing.
        </p>

        <p>
          <strong>Affected Part:</strong> BRK-001
        </p>

        <button>Analyze Change with AI</button>
      </div>
    </div>
  );
}

export default Changes;