import { useState, useEffect } from 'react';
import { getMuscles, getVisualization } from './api';
import MuscleSelector from './components/MuscleSelector';
import ExerciseLibrary from './components/ExerciseLibrary';
import './App.css';

function App() {
  const [muscles, setMuscles] = useState<string[]>([]);
  const [selectedMuscles, setSelectedMuscles] = useState<string[]>([]);
  const [mode, setMode] = useState<'muscles' | 'heatmap' | 'workout'>('muscles');

  // Customization
  const [primaryColor, setPrimaryColor] = useState('#646cff');
  const [secondaryColor, setSecondaryColor] = useState('#ff646c');

  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [muscleError, setMuscleError] = useState(false);

  useEffect(() => {
    getMuscles()
      .then(data => {
        if (Array.isArray(data)) setMuscles(data);
        else throw new Error("Invalid format");
      })
      .catch(err => {
        console.error("Failed to fetch muscles from API, using fallback list.", err);
        // Fallback list of common muscles so UI is usable
        setMuscles([
          "abdominals", "abductors", "adductors", "biceps",
          "calves", "chest", "forearms", "glutes",
          "hamstrings", "lats", "lower_back", "middle_back",
          "neck", "quadriceps", "shoulders", "traps", "triceps"
        ]);
        setMuscleError(false); // Consider it "pseudo-success" for UI purposes
      });
  }, []);

  const toggleMuscle = (m: string) => {
    setSelectedMuscles(prev =>
      prev.includes(m) ? prev.filter(x => x !== m) : [...prev, m]
    );
  };

  const clearSelection = () => {
    setSelectedMuscles([]);
    setImageUrl(null);
  };

  const handleVisualize = async () => {
    setLoading(true);
    try {
      let params: Record<string, any> = {};
      if (mode === 'muscles') {
        params = { muscles: selectedMuscles.join(','), color: primaryColor };
      } else if (mode === 'heatmap') {
        // Backend now expects 'colors' as comma separated list of colors matching muscles.
        // For simple UI, we'll repeat the primary color for all muscles or just send one if backend handles it?
        // Let's replicate the primaryColor for each selected muscle
        const colorsList = selectedMuscles.map(() => primaryColor).join(',');
        params = { muscles: selectedMuscles.join(','), colors: colorsList };
      } else if (mode === 'workout') {
        // Workout mode: Primary = selected, Secondary = empty for now or we could add UI
        params = {
          targetMuscles: selectedMuscles.join(','),
          targetMusclesColor: primaryColor,
          // secondaryMuscles: '',
          // secondaryMusclesColor: secondaryColor 
        };
        // If we wanted to use secondary color, we'd need a secondary selection list.
        // For now, adhering to the UI which selects "muscles", we treat them as target/primary.
      }

      const url = await getVisualization(mode, params);
      setImageUrl(url);
    } catch (err) {
      console.error(err);
      alert('Failed to generate visualization. Please try selecting fewer muscles or checking your network.');
    } finally {
      setLoading(false);
    }
  };

  // ... existing code ...
  const [activeTab, setActiveTab] = useState<'visualizer' | 'library'>('visualizer');

  // ... existing useEffect ...

  // ... existing handlers ...

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>💪 MuscleVis</h2>
          <span className="version-badge">v2.0</span>
        </div>

        <div className="sidebar-content">
          <div className="tool-selector">
            <label>Tools</label>
            <div className="mode-buttons">
              <button
                className={activeTab === 'visualizer' ? 'active' : ''}
                onClick={() => setActiveTab('visualizer')}
              >
                Visualizer
              </button>
              <button
                className={activeTab === 'library' ? 'active' : ''}
                onClick={() => setActiveTab('library')}
              >
                ExerciseDB
              </button>
            </div>
          </div>

          <div className="separator" style={{ margin: '1rem 0', borderBottom: '1px solid #333' }}></div>

          {activeTab === 'visualizer' && (
            <>
              <div className="mode-selector">
                <label>Visualization Mode</label>
                <div className="mode-buttons">
                  <button
                    className={mode === 'muscles' ? 'active' : ''}
                    onClick={() => setMode('muscles')}
                  >
                    Highlight
                  </button>
                  <button
                    className={mode === 'heatmap' ? 'active' : ''}
                    onClick={() => setMode('heatmap')}
                  >
                    Heatmap
                  </button>
                  <button
                    className={mode === 'workout' ? 'active' : ''}
                    onClick={() => setMode('workout')}
                  >
                    Workout
                  </button>
                </div>
              </div>

              <div className="color-controls">
                <div className="control-row">
                  <label>Accent Color</label>
                  <input
                    type="color"
                    value={primaryColor}
                    onChange={(e) => setPrimaryColor(e.target.value)}
                    title="Select Primary Color"
                  />
                </div>
                {mode === 'workout' && (
                  <div className="control-row">
                    <label>Secondary Color</label>
                    <input
                      type="color"
                      value={secondaryColor}
                      onChange={(e) => setSecondaryColor(e.target.value)}
                      title="Select Secondary Color"
                    />
                  </div>
                )}
              </div>

              <div className="muscle-picker-container">
                <div className="picker-header">
                  <label>Select Muscles ({selectedMuscles.length})</label>
                  {selectedMuscles.length > 0 && (
                    <button className="clear-btn" onClick={clearSelection}>Clear</button>
                  )}
                </div>
                {muscleError ? (
                  <div style={{ padding: '1rem', color: '#ef4444', fontSize: '0.875rem' }}>
                    Failed to load muscles. Check API.
                  </div>
                ) : (
                  <MuscleSelector
                    muscles={muscles}
                    selected={selectedMuscles}
                    toggleMuscle={toggleMuscle}
                  />
                )}
              </div>
            </>
          )}

          {activeTab === 'library' && (
            <div className="sidebar-info">
              <p style={{ color: '#a1a1aa', fontSize: '0.9rem', lineHeight: '1.5' }}>
                Browse through thousands of exercises with detailed instructions and videos.
              </p>
            </div>
          )}
        </div>

        {activeTab === 'visualizer' && (
          <div className="sidebar-footer">
            <button
              className="visualize-btn"
              onClick={handleVisualize}
              disabled={loading || selectedMuscles.length === 0}
            >
              {loading ? 'Processing...' : 'Generate Visualization'}
            </button>
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <main className="main-viewport">
        <header className="top-bar">
          <div className="breadcrumbs">
            <span>Dashboard</span> / <span className="current-mode">
              {activeTab === 'visualizer'
                ? `${mode.charAt(0).toUpperCase() + mode.slice(1)} Mode`
                : 'Exercise Library'
              }
            </span>
          </div>
          <div className="user-profile">
            <div className="avatar">U</div>
          </div>
        </header>

        <section className={`canvas-wrapper ${activeTab === 'library' ? 'scrollable' : ''}`}>
          {activeTab === 'visualizer' ? (
            imageUrl ? (
              <div className="visualization-output">
                <img src={imageUrl} alt="Generated Visualization" />
                <div className="canvas-actions">
                  <button onClick={() => window.open(imageUrl, '_blank')}>Open Full Size</button>
                  <button onClick={() => setImageUrl(null)}>Close</button>
                </div>
              </div>
            ) : (
              <div className="empty-state">
                <div className="icon">🎨</div>
                <h3>Ready to Visualize</h3>
                <p>Select muscles from the sidebar and customize colors to generate your anatomical diagram.</p>
              </div>
            )
          ) : (
            <ExerciseLibrary />
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
