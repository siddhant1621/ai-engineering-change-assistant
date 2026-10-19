import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-title">
        <h2>EC Assistant</h2>
        <p>Engineering Change Management</p>
      </div>

      <nav>
        <NavLink to="/" end>
          Dashboard
        </NavLink>

        <NavLink to="/parts">
          Parts
        </NavLink>

        <NavLink to="/bom">
          BOM Viewer
        </NavLink>

        <NavLink to="/changes">
          Engineering Changes
        </NavLink>

        <NavLink to="/ai-analysis">
          AI Analysis
        </NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;