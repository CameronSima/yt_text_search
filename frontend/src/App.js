import { Outlet, Link } from "react-router-dom";
import "./App.css";

function App() {
  return (
    <div className="bg-gray-700 h-screen flex flex-col">
      <Link to="/">
        <div className="p-8 cursor-pointer">
          <span className="text-xl text-white hover:underline">Home</span>
        </div>
      </Link>
      <div className="main container mx-auto flex flex-col flex-1">
        <Outlet />
      </div>
    </div>
  );
}

export default App;
