import React, { useState } from 'react';
import { searchExercises, getExerciseDetails, type Exercise } from '../api';
import './ExerciseLibrary.css'; // We'll create this

export default function ExerciseLibrary() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<Exercise[]>([]);
    const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query) return;

        setLoading(true);
        setError('');
        setSelectedExercise(null);
        try {
            const data = await searchExercises(query);
            setResults(data);
        } catch (err) {
            console.error(err);
            setError('Failed to fetch exercises. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleSelect = async (exerciseId: string) => {
        setLoading(true);
        try {
            const details = await getExerciseDetails(exerciseId);
            setSelectedExercise(details);
        } catch (err) {
            console.error(err);
            setError("Failed to load details");
        } finally {
            setLoading(false);
        }
    };

    if (selectedExercise) {
        return (
            <div className="exercise-library-container">
                <button onClick={() => setSelectedExercise(null)} className="back-btn">← Back to Search</button>

                <div className="detail-header">
                    <h2>{selectedExercise.name}</h2>
                    <div className="tags">
                        {selectedExercise.bodyParts?.map(p => <span key={p} className="tag part">{p}</span>)}
                        {selectedExercise.equipments?.map(e => <span key={e} className="tag equipment">{e}</span>)}
                    </div>
                </div>

                <div className="detail-content">
                    <div className="media-section">
                        {selectedExercise.videoUrl ? (
                            <video
                                src={selectedExercise.videoUrl}
                                controls
                                autoPlay
                                loop
                                className="exercise-video"
                            />
                        ) : (
                            <img src={selectedExercise.imageUrl} alt={selectedExercise.name} className="exercise-image-large" />
                        )}
                    </div>

                    <div className="info-section">
                        {selectedExercise.targetMuscles && (
                            <div className="section-block">
                                <h3>Target Muscles</h3>
                                <p>{selectedExercise.targetMuscles.join(', ')}</p>
                            </div>
                        )}

                        {selectedExercise.secondaryMuscles && selectedExercise.secondaryMuscles.length > 0 && (
                            <div className="section-block">
                                <h3>Secondary Muscles</h3>
                                <p>{selectedExercise.secondaryMuscles.join(', ')}</p>
                            </div>
                        )}

                        {selectedExercise.instructions && (
                            <div className="section-block">
                                <h3>Instructions</h3>
                                <ol>
                                    {selectedExercise.instructions.map((step, i) => (
                                        <li key={i}>{step}</li>
                                    ))}
                                </ol>
                            </div>
                        )}

                        {selectedExercise.exerciseTips && (
                            <div className="section-block tips">
                                <h3>Tips</h3>
                                <ul>
                                    {selectedExercise.exerciseTips.map((tip, i) => (
                                        <li key={i}>{tip}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="exercise-library-container">
            <div className="library-header">
                <h2>Exercise Library</h2>
                <p>Search over 11,000+ exercises with videos and instructions.</p>
            </div>

            <form onSubmit={handleSearch} className="search-form">
                <input
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                    placeholder="Search exercises (e.g., 'bench press', 'squat')"
                    className="search-input"
                />
                <button type="submit" disabled={loading} className="search-btn">
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </form>

            {error && <p className="error-msg">{error}</p>}

            {results.length > 0 && (
                <div className="results-grid">
                    {results.map(ex => (
                        <div key={ex.exerciseId} className="exercise-card" onClick={() => handleSelect(ex.exerciseId)}>
                            <div className="card-image">
                                <img src={ex.imageUrl} alt={ex.name} loading="lazy" />
                            </div>
                            <div className="card-info">
                                <h3>{ex.name}</h3>
                                {ex.bodyParts && ex.bodyParts.length > 0 && (
                                    <span className="card-subtitle">{ex.bodyParts[0]}</span>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
