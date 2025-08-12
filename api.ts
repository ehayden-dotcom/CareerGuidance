import { StudentProfile, Recommendation } from '../types';

/**
 * Post a student profile to the backend and return recommended careers.
 * Throws an error if the response is not OK.
 */
export async function postRecommend(
  profile: StudentProfile
): Promise<Recommendation[]> {
  const response = await fetch('/api/recommend', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(profile)
  });
  if (!response.ok) {
    throw new Error('Failed to fetch recommendations');
  }
  return (await response.json()) as Recommendation[];
}