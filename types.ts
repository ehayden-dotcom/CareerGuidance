export interface StudentProfile {
  name: string;
  yearLevel: number;
  interests: string[];
  strengths: string[];
  academicPerformance: 'High' | 'Medium' | 'Low';
}

export interface Recommendation {
  careerId: string;
  name: string;
  cluster: string;
  confidence: number;
  why: string;
  suggestedSubjects: string[];
  vetOptions: string[];
  nextSteps: string;
}