import axios from 'axios';
import type {
  MeetingResponse,
  CarbonPriceData,
  EmissionData,
  EmailRequest,
} from '../types';

const api = axios.create({
  baseURL: '/api',
  timeout: 300000,
});

export const meetingApi = {
  processMeeting: async (audioFile: File): Promise<MeetingResponse> => {
    const formData = new FormData();
    formData.append('audio_file', audioFile);

    const response = await api.post<MeetingResponse>('/meeting/process', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getCarbonPrice: async (): Promise<CarbonPriceData[]> => {
    const response = await api.get('/market/carbon-price');
    return response.data.data;
  },

  getEmissionCurve: async (): Promise<EmissionData[]> => {
    const response = await api.get('/market/emission-curve');
    return response.data.data;
  },

  sendEmail: async (request: EmailRequest): Promise<{ success: boolean; message: string }> => {
    const response = await api.post('/email/send', request);
    return response.data;
  },
};
