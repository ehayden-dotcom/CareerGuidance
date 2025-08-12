import { useState } from 'react';
import StudentForm from './components/StudentForm';
import Recommendations from './components/Recommendations';
import { Recommendation } from './types';

export default function App() {
  const [recs, setRecs] = useState<Recommendation[] | null>(null);

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">
        AI Career Pathways Advisor
      </h1>
      <StudentForm
        onRecommend={(recommendations) => {
          setRecs(recommendations);
        }}
      />
      {recs && <Recommendations recommendations={recs} />}
    </div>
  );
}