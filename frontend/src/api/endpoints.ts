import axios from "axios";
import type { Place, SearchResult } from "../types/schema";

// Use environment variable or default to localhost
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const client = axios.create({
  baseURL: API_URL,
});

export const api = {
  // Get all places for a country
  getPlaces: async (country: string): Promise<Place[]> => {
    const response = await client.get<Place[]>(`/places/${country}`);
    return response.data;
  },

  // Save a new place
  addPlace: async (place: Place): Promise<Place> => {
    const response = await client.post<Place>("/places/", place);
    return response.data;
  },

  // Delete a place
  deletePlace: async (id: number): Promise<void> => {
    await client.delete(`/places/${id}`);
  },

  // Search OSM (Proxy via Backend)
  searchLocation: async (
    query: string,
    country: string
  ): Promise<SearchResult> => {
    const response = await client.get<SearchResult>("/search", {
      params: { query, country },
    });
    return response.data;
  },
};
