import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

interface Part {
  id: number;
  part_number: string;
  name: string;
  revision: string;
  lifecycle_state: string;
}

interface PartRevision {
  id: number;
  part_id: number;
  revision: string;
  lifecycle_state: string;
}

interface WhereUsedItem {
  bom_item_id: number;
  parent_part_number: string;
  parent_name: string;
  quantity: number;
}

function PartDetail() {
  const { partNumber } = useParams();

  const [part, setPart] = useState<Part | null>(null);
  const [revisions, setRevisions] = useState<PartRevision[]>([]);
  const [whereUsed, setWhereUsed] = useState<WhereUsedItem[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!partNumber) {
      setError("Part number is missing.");
      setLoading(false);
      return;
    }

    Promise.all([
      fetch(`http://127.0.0.1:8000/api/parts/${partNumber}`),
      fetch(`http://127.0.0.1:8000/api/parts/${partNumber}/revisions`),
      fetch(`http://127.0.0.1:8000/api/parts/${partNumber}/where-used`),
    ])
      .then(async ([partResponse, revisionsResponse, whereUsedResponse]) => {
        if (!partResponse.ok) {
          throw new Error("Part not found");
        }

        if (!revisionsResponse.ok) {
          throw new Error("Could not load revisions");
        }

        if (!whereUsedResponse.ok) {
          throw new Error("Could not load where-used data");
        }

        const partData = await partResponse.json();
        const revisionsData = await revisionsResponse.json();
        const whereUsedData = await whereUsedResponse.json();

        setPart(partData);
        setRevisions(revisionsData);
        setWhereUsed(whereUsedData);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError("Could not load part details.");
        setLoading(false);
      });
  }, [partNumber]);

  if (loading) {
    return <p>Loading part...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!part) {
    return <p>Part not found.</p>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>{part.part_number}</h1>
        <p>{part.name}</p>
      </div>

      <div className="panel">
        <h2>Part Details</h2>

        <p>
          <strong>Part Number:</strong> {part.part_number}
        </p>

        <p>
          <strong>Name:</strong> {part.name}
        </p>

        <p>
          <strong>Current Revision:</strong> {part.revision}
        </p>

        <p>
          <strong>Lifecycle State:</strong> {part.lifecycle_state}
        </p>
      </div>

      <div className="panel revision-panel">
        <h2>Revision History</h2>

        {revisions.length === 0 ? (
          <p>No revision history available.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Revision</th>
                <th>Lifecycle State</th>
              </tr>
            </thead>

            <tbody>
              {revisions.map((revision) => (
                <tr key={revision.id}>
                  <td>{revision.revision}</td>
                  <td>{revision.lifecycle_state}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="panel revision-panel">
        <h2>Where Used</h2>

        {whereUsed.length === 0 ? (
          <p>This part is not currently used in any assembly.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Parent Part</th>
                <th>Assembly Name</th>
                <th>Quantity</th>
              </tr>
            </thead>

            <tbody>
              {whereUsed.map((item) => (
                <tr key={item.bom_item_id}>
                  <td>{item.parent_part_number}</td>
                  <td>{item.parent_name}</td>
                  <td>{item.quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default PartDetail;