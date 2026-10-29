import { FormEvent, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

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

function Changes() {
  const navigate = useNavigate();

  const [changes, setChanges] = useState<EngineeringChange[]>([]);
  const [parts, setParts] = useState<Part[]>([]);

  const [changeNumber, setChangeNumber] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [reason, setReason] = useState("");
  const [owner, setOwner] = useState("");
  const [affectedPartNumber, setAffectedPartNumber] = useState("");

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [formError, setFormError] = useState("");

  const loadChanges = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/changes"
      );

      if (!response.ok) {
        throw new Error("Could not load engineering changes.");
      }

      const data = await response.json();
      setChanges(data);
    } catch (error) {
      console.error(error);
      setError("Could not load engineering changes.");
    }
  };

  const loadParts = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/parts"
      );

      if (!response.ok) {
        throw new Error("Could not load parts.");
      }

      const data = await response.json();
      setParts(data);
    } catch (error) {
      console.error(error);
      setError("Could not load parts.");
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);

      await Promise.all([
        loadChanges(),
        loadParts(),
      ]);

      setLoading(false);
    };

    loadData();
  }, []);

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    setFormError("");

    if (
      !changeNumber ||
      !title ||
      !description ||
      !reason ||
      !owner ||
      !affectedPartNumber
    ) {
      setFormError("Please complete all fields.");
      return;
    }

    setSubmitting(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/changes",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            change_number: changeNumber,
            title,
            description,
            reason,
            status: "Draft",
            owner,
            affected_part_number: affectedPartNumber,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
          errorData.detail || "Could not create engineering change."
        );
      }

      const newChange: EngineeringChange =
        await response.json();

      navigate(`/changes/${newChange.change_number}`);
    } catch (error) {
      console.error(error);

      if (error instanceof Error) {
        setFormError(error.message);
      } else {
        setFormError(
          "Could not create engineering change."
        );
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <p>Loading engineering changes...</p>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>Engineering Changes</h1>
        <p>
          Create and review engineering changes and their
          product impact.
        </p>
      </div>

      {error && <p>{error}</p>}

      <div className="panel">
        <h2>Create Engineering Change</h2>

        <form
          className="change-form"
          onSubmit={handleSubmit}
        >
          <div className="form-group">
            <label htmlFor="change-number">
              Change Number
            </label>

            <input
              id="change-number"
              type="text"
              value={changeNumber}
              onChange={(event) =>
                setChangeNumber(event.target.value)
              }
              placeholder="Example: EC-002"
            />
          </div>

          <div className="form-group">
            <label htmlFor="title">
              Title
            </label>

            <input
              id="title"
              type="text"
              value={title}
              onChange={(event) =>
                setTitle(event.target.value)
              }
              placeholder="Example: Replace wiring harness"
            />
          </div>

          <div className="form-group">
            <label htmlFor="affected-part">
              Affected Part
            </label>

            <select
              id="affected-part"
              value={affectedPartNumber}
              onChange={(event) =>
                setAffectedPartNumber(event.target.value)
              }
            >
              <option value="">
                Select a part
              </option>

              {parts.map((part) => (
                <option
                  key={part.id}
                  value={part.part_number}
                >
                  {part.part_number} — {part.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="owner">
              Owner
            </label>

            <input
              id="owner"
              type="text"
              value={owner}
              onChange={(event) =>
                setOwner(event.target.value)
              }
              placeholder="Example: Siddhanth"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">
              Description
            </label>

            <textarea
              id="description"
              value={description}
              onChange={(event) =>
                setDescription(event.target.value)
              }
              placeholder="Describe the proposed engineering change."
              rows={4}
            />
          </div>

          <div className="form-group">
            <label htmlFor="reason">
              Reason
            </label>

            <textarea
              id="reason"
              value={reason}
              onChange={(event) =>
                setReason(event.target.value)
              }
              placeholder="Why is this change required?"
              rows={4}
            />
          </div>

          <div className="form-group">
            <label>Status</label>
            <input
              type="text"
              value="Draft"
              disabled
            />
          </div>

          {formError && (
            <p className="form-error">
              {formError}
            </p>
          )}

          <button
            type="submit"
            disabled={submitting}
          >
            {submitting
              ? "Creating..."
              : "Create Engineering Change"}
          </button>
        </form>
      </div>

      <div className="panel revision-panel">
        <h2>Change Requests</h2>

        {changes.length === 0 ? (
          <p>No engineering changes found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Change Number</th>
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
                    <Link
                      to={`/changes/${change.change_number}`}
                    >
                      {change.change_number}
                    </Link>
                  </td>

                  <td>
                    {change.title}
                  </td>

                  <td>
                    {change.affected_part_number}
                  </td>

                  <td>
                    {change.status}
                  </td>

                  <td>
                    {change.owner}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Changes;