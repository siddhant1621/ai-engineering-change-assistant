function Dashboard() {
  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Overview of engineering changes and product data.</p>
      </div>

      <div className="card-grid">
        <div className="card">
          <span>Total Parts</span>
          <strong>128</strong>
        </div>

        <div className="card">
          <span>Open Changes</span>
          <strong>12</strong>
        </div>

        <div className="card">
          <span>Under Review</span>
          <strong>4</strong>
        </div>

        <div className="card">
          <span>High Risk Changes</span>
          <strong>2</strong>
        </div>
      </div>

      <div className="panel">
        <h2>Recent Engineering Changes</h2>

        <table>
          <thead>
            <tr>
              <th>Change ID</th>
              <th>Title</th>
              <th>Status</th>
              <th>Owner</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>EC-001</td>
              <td>Replace ECU Bracket</td>
              <td>Review</td>
              <td>Siddhanth</td>
            </tr>

            <tr>
              <td>EC-002</td>
              <td>Update Harness Connector</td>
              <td>Draft</td>
              <td>Anna</td>
            </tr>

            <tr>
              <td>EC-003</td>
              <td>Motor Supplier Change</td>
              <td>Approved</td>
              <td>Markus</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;