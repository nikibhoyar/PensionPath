import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { calculateInvestment, type CalculationResults } from '../lib/mockApi';
import Navbar from '../components/Navbar';
import InvestmentForm from '../components/InvestmentForm';
import InvestmentResults from '../components/InvestmentResults';

export default function Dashboard() {
  const { user } = useAuth();
  const [results, setResults] = useState<CalculationResults | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (formData: any) => {
    setLoading(true);
    setError(null);

    try {
      const results = await calculateInvestment(formData);
      setResults(results);
    } catch (error) {
      setError('Failed to calculate investment strategy. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar userEmail={user?.email} />

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Retirement Calculator</h2>
            
            {error && (
              <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}
            
            <InvestmentForm onSubmit={handleSubmit} loading={loading} />
          </div>

          {results && (
            <div className="mt-6 bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Investment Strategy Results</h3>
              <InvestmentResults results={results} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}