import { Recommendation } from '../types';

interface RecommendationsProps {
  recommendations: Recommendation[];
}

export default function Recommendations({ recommendations }: RecommendationsProps) {
  return (
    <div className="mt-6 space-y-4">
      <h2 className="text-xl font-semibold">Top Recommendations</h2>
      {recommendations.map((rec) => (
        <div
          key={rec.careerId}
          className="border rounded p-4 bg-white shadow-sm"
        >
          <h3 className="text-lg font-bold">
            {rec.name} <span className="text-sm text-gray-500">({rec.cluster})</span>
          </h3>
          <p className="text-sm text-gray-600 mb-1">
            Confidence: {(rec.confidence * 100).toFixed(0)}%
          </p>
          <p className="mb-2">{rec.why}</p>
          <ul className="list-disc list-inside text-sm mb-2">
            <li>
              <strong>Suggested Subjects:</strong> {rec.suggestedSubjects.join(', ')}
            </li>
            <li>
              <strong>VET Options:</strong> {rec.vetOptions.join(', ')}
            </li>
          </ul>
          <p className="text-sm text-gray-700">{rec.nextSteps}</p>
        </div>
      ))}
    </div>
  );
}