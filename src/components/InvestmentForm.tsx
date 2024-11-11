import { useState } from 'react';
import { Calculator, Loader2 } from 'lucide-react';
import type { CalculationInput } from '../lib/mockApi';

interface InvestmentFormProps {
  onSubmit: (data: CalculationInput) => Promise<void>;
  loading: boolean;
}

export default function InvestmentForm({ onSubmit, loading }: InvestmentFormProps) {
  const [formData, setFormData] = useState<CalculationInput>({
    retirementAge: '',
    currentAge: '',
    desiredFund: '',
    monthlyInvestment: '',
    riskCategory: '2'
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Retirement Age
          </label>
          <input
            type="number"
            value={formData.retirementAge}
            onChange={(e) => setFormData({...formData, retirementAge: e.target.value})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Current Age
          </label>
          <input
            type="number"
            value={formData.currentAge}
            onChange={(e) => setFormData({...formData, currentAge: e.target.value})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Desired Retirement Fund (₹)
          </label>
          <input
            type="number"
            value={formData.desiredFund}
            onChange={(e) => setFormData({...formData, desiredFund: e.target.value})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Monthly Investment (₹)
          </label>
          <input
            type="number"
            value={formData.monthlyInvestment}
            onChange={(e) => setFormData({...formData, monthlyInvestment: e.target.value})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>

        <div className="sm:col-span-2">
          <label className="block text-sm font-medium text-gray-700">
            Risk Category
          </label>
          <select
            value={formData.riskCategory}
            onChange={(e) => setFormData({...formData, riskCategory: e.target.value})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
            <option value="1">High Risk-High Return</option>
            <option value="2">Medium Risk-Medium Return</option>
            <option value="3">Low Risk-Low Return</option>
          </select>
        </div>
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={loading}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? (
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          ) : (
            <Calculator className="w-4 h-4 mr-2" />
          )}
          {loading ? 'Calculating...' : 'Calculate Investment Strategy'}
        </button>
      </div>
    </form>
  );
}