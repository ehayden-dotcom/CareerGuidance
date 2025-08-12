import { useState } from 'react';
import { postRecommend } from '../lib/api';
import { StudentProfile, Recommendation } from '../types';

interface StudentFormProps {
  /**
   * Callback invoked with the recommendations when the form is successfully submitted.
   */
  onRecommend: (recommendations: Recommendation[]) => void;
}

const INTEREST_OPTIONS = [
  'STEM',
  'Health',
  'IT',
  'Trades',
  'Creative Arts',
  'Education',
  'Business'
];

const STRENGTH_OPTIONS = [
  'Problem-Solving',
  'Creativity',
  'Communication',
  'Technical Skills',
  'Empathy',
  'Leadership'
];

const YEAR_LEVELS = [7, 8, 9, 10, 11, 12];

export default function StudentForm({ onRecommend }: StudentFormProps) {
  const [formState, setFormState] = useState<StudentProfile>({
    name: '',
    yearLevel: 10,
    interests: [],
    strengths: [],
    academicPerformance: 'Medium'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const toggleCheckbox = (
    field: 'interests' | 'strengths',
    value: string
  ) => {
    setFormState((prev) => {
      const selected = prev[field];
      const exists = selected.includes(value);
      const updated = exists
        ? selected.filter((v) => v !== value)
        : [...selected, value];
      return { ...prev, [field]: updated };
    });
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormState((prev) => ({ ...prev, [name]: name === 'yearLevel' ? Number(value) : value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const recs = await postRecommend(formState);
      onRecommend(recs);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded shadow">
      <div>
        <label htmlFor="name" className="block font-medium mb-1">
          Name
        </label>
        <input
          id="name"
          name="name"
          type="text"
          required
          value={formState.name}
          onChange={handleChange}
          className="w-full border rounded p-2"
        />
      </div>
      <div>
        <label htmlFor="yearLevel" className="block font-medium mb-1">
          Year Level
        </label>
        <select
          id="yearLevel"
          name="yearLevel"
          value={formState.yearLevel}
          onChange={handleChange}
          className="w-full border rounded p-2"
        >
          {YEAR_LEVELS.map((lvl) => (
            <option key={lvl} value={lvl}>
              {lvl}
            </option>
          ))}
        </select>
      </div>
      <div>
        <p className="font-medium mb-1">Interests</p>
        <div className="grid grid-cols-2 gap-2">
          {INTEREST_OPTIONS.map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formState.interests.includes(opt)}
                onChange={() => toggleCheckbox('interests', opt)}
                className="h-4 w-4"
              />
              <span>{opt}</span>
            </label>
          ))}
        </div>
      </div>
      <div>
        <p className="font-medium mb-1">Strengths</p>
        <div className="grid grid-cols-2 gap-2">
          {STRENGTH_OPTIONS.map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formState.strengths.includes(opt)}
                onChange={() => toggleCheckbox('strengths', opt)}
                className="h-4 w-4"
              />
              <span>{opt}</span>
            </label>
          ))}
        </div>
      </div>
      <div>
        <p className="font-medium mb-1">Academic Performance</p>
        <div className="flex items-center space-x-4">
          {(['High', 'Medium', 'Low'] as const).map((level) => (
            <label key={level} className="flex items-center space-x-1">
              <input
                type="radio"
                name="academicPerformance"
                value={level}
                checked={formState.academicPerformance === level}
                onChange={handleChange}
                className="h-4 w-4"
              />
              <span>{level}</span>
            </label>
          ))}
        </div>
      </div>
      {error && <p className="text-red-600">{error}</p>}
      <button
        type="submit"
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        disabled={loading}
      >
        {loading ? 'Loading...' : 'Get Recommendations'}
      </button>
    </form>
  );
}