import { Download, FileText } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Chat from '../components/Chat';
import { api, ComplianceData } from '../services/api';

export default function Results() {
  const location = useLocation();
  const { exportCountry, importCountry, product } = location.state || {};
  const [complianceData, setComplianceData] = useState<ComplianceData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchComplianceData = async () => {
      try {
        const data = await api.getComplianceInfo(exportCountry, importCountry, product);
        setComplianceData(data);
      } catch (err) {
        setError('Failed to fetch compliance information. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchComplianceData();
  }, [exportCountry, importCountry, product]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-gray-600">Loading compliance information...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="bg-red-50 p-4 rounded-lg">
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 relative min-h-screen pb-24">
      <div className="flex justify-end space-x-4 mb-8">
        <button className="inline-flex items-center px-6 py-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 transition-colors">
          <FileText className="h-5 w-5 text-gray-600 mr-2" />
          <span className="text-gray-700 font-medium">PDF Report</span>
        </button>
        <button className="inline-flex items-center px-6 py-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 transition-colors">
          <Download className="h-5 w-5 text-gray-600 mr-2" />
          <span className="text-gray-700 font-medium">Excel Report</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column */}
        <div className="space-y-8">
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl shadow-sm p-8 border border-blue-100">
            <h2 className="text-2xl font-bold text-blue-900 mb-6">Export Requirements</h2>
            <div className="space-y-6">
              <div className="bg-white/80 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-blue-800 mb-4">Required Documentation</h3>
                <ul className="space-y-3">
                  {complianceData?.exportRequirements.documents.map((doc, index) => (
                    <li key={index} className="flex items-center text-blue-700">
                      <div className="h-2 w-2 bg-blue-500 rounded-full mr-3"></div>
                      {doc}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-emerald-50 to-green-50 rounded-2xl shadow-sm p-8 border border-emerald-100">
            <h2 className="text-2xl font-bold text-emerald-900 mb-6">Import Requirements</h2>
            <div className="space-y-6">
              <div className="bg-white/80 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-emerald-800 mb-4">Compliance Requirements</h3>
                <ul className="space-y-3">
                  {complianceData?.importRequirements.documents.map((doc, index) => (
                    <li key={index} className="flex items-center text-emerald-700">
                      <div className="h-2 w-2 bg-emerald-500 rounded-full mr-3"></div>
                      {doc}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-8">
          <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl shadow-sm p-8 border border-purple-100">
            <h2 className="text-2xl font-bold text-purple-900 mb-6">Available Incentives</h2>
            <div className="space-y-6">
              <div className="bg-white/80 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-purple-800 mb-4">Grants and Support</h3>
                <ul className="space-y-3">
                  {complianceData?.incentives.grants.map((grant, index) => (
                    <li key={index} className="flex items-center text-purple-700">
                      <div className="h-2 w-2 bg-purple-500 rounded-full mr-3"></div>
                      {grant}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Chat />
    </div>
  );
}