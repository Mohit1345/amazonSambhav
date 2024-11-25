import axios from 'axios';

// Mock data for development
const mockComplianceData = {
  exportRequirements: {
    documents: [
      'Certificate of Origin',
      'Commercial Invoice',
      'Export License',
      'Packing List'
    ],
    regulations: [
      'Export Control Classification',
      'Customs Declaration',
      'Safety Standards Compliance'
    ]
  },
  importRequirements: {
    documents: [
      'Import License',
      'Bill of Lading',
      'Customs Declaration Form',
      'Insurance Certificate'
    ],
    regulations: [
      'Import Duties Payment',
      'Local Safety Standards',
      'Product Certification'
    ]
  },
  incentives: {
    grants: [
      'Export Development Fund',
      'Small Business Export Grant',
      'Market Development Grant'
    ],
    support: [
      'Trade Finance Support',
      'Export Insurance Coverage',
      'Technical Assistance'
    ]
  }
};

export interface ComplianceData {
  exportRequirements: {
    documents: string[];
    regulations: string[];
  };
  importRequirements: {
    documents: string[];
    regulations: string[];
  };
  incentives: {
    grants: string[];
    support: string[];
  };
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

const isDevelopment = process.env.NODE_ENV === 'development';
const API_BASE_URL = isDevelopment ? '/api' : 'https://api.example.com';

export const api = {
  async getComplianceInfo(exportCountry: string, importCountry: string, product: string): Promise<ComplianceData> {
    if (isDevelopment) {
      // Simulate API delay in development
      await new Promise(resolve => setTimeout(resolve, 1000));
      return mockComplianceData;
    }

    try {
      const response = await axios.get(`${API_BASE_URL}/compliance`, {
        params: { exportCountry, importCountry, product }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching compliance info:', error);
      throw new Error('Failed to fetch compliance information');
    }
  },

  async sendChatMessage(message: string): Promise<string> {
    if (isDevelopment) {
      // Simulate API delay in development
      await new Promise(resolve => setTimeout(resolve, 1000));
      return `This is a mock response for: "${message}"`;
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, { message });
      return response.data.reply;
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw new Error('Failed to send chat message');
    }
  }
};