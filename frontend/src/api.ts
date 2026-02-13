import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export interface Muscle {
  name: string;
  // potentially other fields if backend provides, but unlikely
}

export const getMuscles = async (): Promise<string[]> => {
  const response = await axios.get(`${API_BASE_URL}/muscles`);
  return response.data;
};

export const getVisualization = async (endpoint: string, params: Record<string, any>): Promise<string> => {
  const response = await axios.get(`${API_BASE_URL}/visualize/${endpoint}`, {
    params,
    responseType: 'blob',
  });
  return URL.createObjectURL(response.data);
};

export interface Exercise {
  exerciseId: string;
  name: string;
  imageUrl: string;
  videoUrl?: string;
  equipments?: string[];
  bodyParts?: string[];
  targetMuscles?: string[];
  secondaryMuscles?: string[];
  instructions?: string[];
  exerciseTips?: string[];
  variations?: string[];
  overview?: string;
}

// Helper to extract data handling different response formats
const extractData = (data: any) => {
  if (data && data.success && data.data) {
    return data.data;
  }
  return data;
};

export const searchExercises = async (search: string): Promise<Exercise[]> => {
  const response = await axios.get(`${API_BASE_URL}/edb/exercises/search`, { params: { search } });
  return extractData(response.data);
};

export const getExerciseDetails = async (exerciseId: string): Promise<Exercise> => {
  const response = await axios.get(`${API_BASE_URL}/edb/exercises/${exerciseId}`);
  // Details might be wrapped or not, safe to try extracting
  return extractData(response.data);
};

export const getExercises = async (name?: string, keywords?: string): Promise<Exercise[]> => {
  const params: any = {};
  if (name) params.name = name;
  if (keywords) params.keywords = keywords;
  const response = await axios.get(`${API_BASE_URL}/edb/exercises`, { params });
  return extractData(response.data);
};
