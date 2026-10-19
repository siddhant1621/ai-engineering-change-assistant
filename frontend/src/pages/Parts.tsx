import { useEffect, useState } from "react";

interface Part {
  part_number: string;
  name: string;
  revision: string;
  lifecycle_state: string;
}

function Parts() {
  const [parts, setParts] = useState<Part[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/parts")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load parts");
        }

        return response.json();
      })
      .then((data) => {
        setParts(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError("Could not load parts from backend.");
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <div className="page-header">
        <h1>Parts</h1>
        <p>Manage engineering parts and revisions.</p>
      </div>

      <div className="panel">
        <h2>Parts List</h2>

        {loading && <p>Loading parts...</p>}

        {error && <p>{error}</p>}

        {!loading && !error && (
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
              {parts.map((part) => (
                <tr key={part.part_number}>
                  <td>{part.part_number}</td>
                  <td>{part.name}</td>
                  <td>{part.revision}</td>
                  <td>{part.lifecycle_state}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Parts;