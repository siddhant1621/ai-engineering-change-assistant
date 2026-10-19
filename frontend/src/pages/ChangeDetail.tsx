import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

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

interface Part {
  id: number;
  part_number: string;
  name: string;
  revision: string;
  lifecycle_state: string;
}

interface ImpactItem {
  part_number: string;
  name: string;
  level: number;
  quantity: number;
}

interface ImpactResponse {
  source_part: {
    part_number: string;
    name: string;
  };
  impacted_assemblies: ImpactItem[];
}

interface AIAnalysis {
  risk_level: string;
  summary: string;
  potential_risks: string[];
  missing_information: string[];
  suggested_reviewers: string[];
}

function ChangeDetail() {
  const { changeNumber } = useParams();

  const [change, setChange] = useState<EngineeringChange | null>(null);
  const [part, setPart] = useState<Part | null>(null);
  const [impact, setImpact] = useState<ImpactResponse | null>(null);

  const [analysis, setAnalysis] = useState<AIAnalysis | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [analysisError, setAnalysisError] = useState("");

  useEffect(() => {
    if (!changeNumber) {
      setError("Change number is missing.");
      setLoading(false);
      return;
    }

    fetch(`http://127.0.0.1:8000/api/changes/${changeNumber}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Engineering change not found");
        }

        return response.json();
      })
      .then(async (changeData) => {
        setChange(changeData);

        const [partResponse, impactResponse] = await Promise.all([
          fetch(
            `http://127.0.0.1:8000/api/parts/${changeData.affected_part_number}`
          ),
          fetch(
            `http://127.0.0.1:8000/api/parts/${changeData.affected_part_number}/impact`
          ),
        ]);

        if (!partResponse.ok) {
          throw new Error("Could not load affected part");
        }

        if (!impactResponse.ok) {
          throw new Error("Could not load impact analysis");
        }

        const partData = await partResponse.json();
        const impactData = await impactResponse.json();

        setPart(partData);
        setImpact(impactData);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError("Could not load engineering change details.");
        setLoading(false);
      });
  }, [changeNumber]);

  const handleAnalyze = async () => {
    if (!changeNumber) {
      return;
    }

    setAnalyzing(true);
    setAnalysisError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/changes/${changeNumber}/analyze`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error("AI analysis failed");
      }

      const data = await response.json();

      setAnalysis(data);
    } catch (error) {
      console.error(error);
      setAnalysisError("Could not generate AI analysis.");
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return <p>Loading engineering change...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!change) {
    return <p>Engineering change not found.</p>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>{change.change_number}</h1>
        <p>{change.title}</p>
      </div>

      <div className="panel">
        <h2>Change Details</h2>

        <p>
          <strong>Status:</strong> {change.status}
        </p>

        <p>
          <strong>Owner:</strong> {change.owner}
        </p>

        <p>
          <strong>Description:</strong> {change.description}
        </p>

        <p>
          <strong>Reason:</strong> {change.reason}
        </p>
      </div>

      <div className="panel revision-panel">
        <h2>Affected Part</h2>

        {part ? (
          <>
            <p>
              <strong>Part Number:</strong> {part.part_number}
            </p>

            <p>
              <strong>Name:</strong> {part.name}
            </p>

            <p>
              <strong>Revision:</strong> {part.revision}
            </p>

            <p>
              <strong>Lifecycle State:</strong> {part.lifecycle_state}
            </p>
          </>
        ) : (
          <p>No affected part details available.</p>
        )}
      </div>

      <div className="panel revision-panel">
        <h2>Impacted Assemblies</h2>

        {!impact || impact.impacted_assemblies.length === 0 ? (
          <p>No impacted assemblies found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Level</th>
                <th>Part Number</th>
                <th>Assembly Name</th>
                <th>Quantity</th>
              </tr>
            </thead>

            <tbody>
              {impact.impacted_assemblies.map((item) => (
                <tr key={`${item.part_number}-${item.level}`}>
                  <td>{item.level}</td>
                  <td>{item.part_number}</td>
                  <td>{item.name}</td>
                  <td>{item.quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="panel revision-panel">
        <h2>AI Engineering Analysis</h2>

        <button onClick={handleAnalyze} disabled={analyzing}>
          {analyzing ? "Analyzing..." : "Analyze with AI"}
        </button>

        {analysisError && <p>{analysisError}</p>}

        {analysis && (
          <div className="ai-analysis-result">
            <h3>Risk Level</h3>
            <p>
              <strong>{analysis.risk_level}</strong>
            </p>

            <h3>Summary</h3>
            <p>{analysis.summary}</p>

            <h3>Potential Risks</h3>

            <ul>
              {analysis.potential_risks.map((risk, index) => (
                <li key={index}>{risk}</li>
              ))}
            </ul>

            <h3>Missing Information</h3>

            <ul>
              {analysis.missing_information.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>

            <h3>Suggested Reviewers</h3>

            <ul>
              {analysis.suggested_reviewers.map((reviewer, index) => (
                <li key={index}>{reviewer}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChangeDetail;