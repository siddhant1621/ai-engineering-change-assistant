function Parts() {
  return (
    <div>
      <div className="page-header">
        <h1>Parts</h1>
        <p>Manage engineering parts and revisions.</p>
      </div>

      <div className="panel">
        <h2>Parts List</h2>

        <table>
          <thead>
            <tr>
              <th>Part Number</th>
              <th>Name</th>
              <th>Revision</th>
              <th>Lifecycle State</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>BRK-001</td>
              <td>ECU Bracket</td>
              <td>A</td>
              <td>Released</td>
            </tr>

            <tr>
              <td>BRK-002</td>
              <td>New ECU Bracket</td>
              <td>A</td>
              <td>Prototype</td>
            </tr>

            <tr>
              <td>ECU-100</td>
              <td>Main ECU</td>
              <td>C</td>
              <td>Released</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Parts;