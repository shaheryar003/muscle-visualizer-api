import React, { useState } from 'react';
import './MuscleSelector.css';

interface MuscleSelectorProps {
    muscles: string[];
    selected: string[];
    toggleMuscle: (muscle: string) => void;
}

const MuscleSelector: React.FC<MuscleSelectorProps> = ({ muscles, selected, toggleMuscle }) => {
    const [term, setTerm] = useState('');

    const filtered = muscles.filter(m => m.toLowerCase().includes(term.toLowerCase()));

    return (
        <div className="muscle-selector-list">
            <input
                type="text"
                className="muscle-search-input"
                placeholder="Search specific muscle..."
                value={term}
                onChange={(e) => setTerm(e.target.value)}
            />
            <div className="scrollable-list">
                {term && filtered.length === 0 && (
                    <div className="no-results">No muscles found matching "{term}"</div>
                )}
                {filtered.map(m => (
                    <div
                        key={m}
                        className={`muscle-option ${selected.includes(m) ? 'selected' : ''}`}
                        onClick={() => toggleMuscle(m)}
                    >
                        <div className="checkbox-indicator"></div>
                        <span>{m}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default MuscleSelector;
