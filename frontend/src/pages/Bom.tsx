import { useEffect, useState } from "react";

interface BomItem {
  id: number;
  parent_part_number: string;
  child_part_number: string;
  child_name: string;
  quantity: number;
}

function Bom() {
  const [bomItems, setBomItems] = useState<BomItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/parts/ASSY-100/bom")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load BOM");
        }

        return response.json();
      })
      .then((data) => {
        setBomItems(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError("Could not load BOM from backend.");
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <div className="page-header">
        <h1>BOM Viewer</h1>
        <p>Visualize product and assembly structures.</p>
      </div>

      <div className="panel">
        <h2>ASSY-100 — ECU Assembly</h2>

        {loading && <p>Loading BOM...</p>}

        {error && <p>{error}</p>}

        {!loading && !error && (
          <div className="bom-tree">
            <p>
              <strong>ASSY-100 — ECU Assembly</strong>
            </p>

            {bomItems.map((item, index) => {
              const isLast = index === bomItems.length - 1;

              return (
                <p key={item.id} className="indent-1">
                  {isLast ? "└──" : "├──"} {item.child_part_number}{" "}
                  {item.child_name} × {item.quantity}
                </p>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default Bom;