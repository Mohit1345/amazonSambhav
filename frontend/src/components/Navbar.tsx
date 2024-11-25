import { Link } from 'react-router-dom';
import { Globe2, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Globe2 className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">Trade Comply AI</span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <button
                onClick={logout}
                className="flex items-center text-gray-700 hover:text-blue-600"
              >
                <LogOut className="h-5 w-5 mr-2" />
                Sign Out
              </button>
            ) : (
              <div className="space-x-4">
                <Link
                  to="/login"
                  className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                >
                  Sign In
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}