import axios from 'axios';
import { sleep } from './utils';

// Define interfaces for investment allocations and calculation results
export interface InvestmentAllocation {
  ticker: string;
  percentage: number;
  monthly_amount: number;
  expected_return: number;
  risk_level: string;
}

export interface CalculationResults {
  required_annual_return: number;
  total_investment_needed: number;
  expected_future_value: number;
  allocations: InvestmentAllocation[];
  years_to_invest: number;
}

export interface CalculationInput {
  retirementAge: string;
  currentAge: string;
  desiredFund: string;
  monthlyInvestment: string;
  riskCategory: string;
}

// Base URL of your Flask API
const API_BASE_URL = 'https://pensionpath-5vmi.onrender.com';

/**
 * Function to calculate investment strategy using Flask API.
 * @param input - CalculationInput object containing user inputs.
 * @returns Promise resolving to the CalculationResults object.
 */
export async function calculateInvestment(input: CalculationInput): Promise<CalculationResults> {
  // Simulate API delay (optional, for UX purposes)
  await sleep(500);

  try {
    // Prepare the payload for the POST request
    const payload = {
      retirementAge: parseInt(input.retirementAge),
      currentAge: parseInt(input.currentAge),
      desiredFund: parseFloat(input.desiredFund),
      monthlyInvestment: parseFloat(input.monthlyInvestment),
      riskCategory: parseInt(input.riskCategory)
    };

    // Make a POST request to your Flask API endpoint
    const response = await axios.post<CalculationResults>(`${API_BASE_URL}/calculate`, payload);

    // Return the response data
    return response.data;
  } catch (error: any) {
    console.error('Error fetching investment calculation:', error);
    throw new Error(error.response?.data?.error || 'Failed to fetch investment calculation');
  }
}
