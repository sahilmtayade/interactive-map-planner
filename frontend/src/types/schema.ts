export interface Place {
  id?: number;
  name: string;
  category: string;
  address: string;
  latitude: number;
  longitude: number;
  notes?: string;
  country: string;
  zone?: string;
}

export interface SearchResult {
  found: boolean;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
}
