import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
interface EngineeringChange {
  id: number;
  change_number: string;
  title: string;
  description: string;
  reason: string;
  status: string;
  owner: string;
  affected_part_number: string;
}

function Changes() {
  const [changes, setChanges] = useState<EngineeringChange[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/changes")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load engineering changes");
        }

        return response.json();
      })
      .then((data) => {
        setChanges(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError("Could not load engineering changes.");
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <div className="page-header">
        <h1>Engineering Changes</h1>
        <p>Review engineering change requests and affected parts.</p>
      </div>

      <div className="panel">
        <h2>Change Requests</h2>

        {loading && <p>Loading changes...</p>}

        {error && <p>{error}</p>}

        {!loading && !error && (
          <>
            {changes.length === 0 ? (
              <p>No engineering changes available.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Change</th>
                    <th>Title</th>
                    <th>Affected Part</th>
                    <th>Status</th>
                    <th>Owner</th>
                  </tr>
                </thead>

                <tbody>
                  {changes.map((change) => (
                    <tr key={change.id}>
                      <td>
  <Link to={`/changes/${change.change_number}`}>
    {change.change_number}
  </Link>
</td>
                      <td>{change.title}</td>
                      <td>{change.affected_part_number}</td>
                      <td>{change.status}</td>
                      <td>{change.owner}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default Changes;