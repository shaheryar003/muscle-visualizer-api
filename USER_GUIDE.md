# 📖 Muscle Visualizer & Exercise Explorer - User Guide

Welcome to the **Muscle Visualizer & Exercise Explorer**! This application combines anatomical visualization with a comprehensive exercise database to help you understand muscle engagement and discover new workouts.

---

## 🌟 Features

### 1. Muscle Visualizer
*   **Highlight Mode**: Select specific muscles and highlight them in your choice of color.
*   **Heatmap Mode**: Visualize muscle intensity or focus using a color-coded map.
*   **Workout Mode**: Display primary (target) and secondary muscle activation patterns.
*   **Customization**: Fully adjustable colors and real-time generation.

### 2. Exercise Explorer
*   **Search**: Find exercises by name or keyword from a database of 5,000+ movements.
*   **Details**: View step-by-step instructions, target muscles, and equipment for each exercise.
*   **Visual Integration**: Directly see which muscles an exercise targets using the visualizer.

---

## 🚀 Getting Started

### Prerequisites
*   **Node.js** (v18 or higher)
*   **Python** (v3.9 or higher)
*   **RapidAPI Keys**: You need keys for [Muscle Visualizer API](https://rapidapi.com/ascendapi/api/muscle-visualizer-api) and [ExerciseDB API](https://rapidapi.com/ascendapi/api/exercise-db-with-videos-and-images-by-ascendapi).

### Configuration
1.  Navigate to the `backend` folder.
2.  Create a `.env` file (see `.env.example` if available) with the following:
    ```env
    RAPID_API_KEY=your_key_here
    RAPID_API_HOST=muscle-visualizer-api.p.rapidapi.com
    EDB_API_KEY=your_key_here
    EDB_API_HOST=exercisedb.p.rapidapi.com
    ```

---

## 🛠️ Installation & Setup

### Option 1: Local Development (Separate Terminals)

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

### Option 2: Docker (Recommended for Production)
Build and run the entire stack with a single command:
```bash
docker build -t muscle-visualizer .
docker run -p 8000:8000 --env-file backend/.env muscle-visualizer
```
Access the app at `http://localhost:8000`.

---

## 🖥️ Using the Application

### 🎨 Generating Muscle Visualizations
1.  Click the **Visualizer** tab in the sidebar.
2.  Choose a **Mode**:
    *   **Highlight**: Highlights selected muscles in a solid color.
    *   **Heatmap**: Creates a gradient-based intensity map.
    *   **Workout**: Differentiates between primary and secondary muscle groups.
3.  Choose an **Accent Color** using the color picker.
4.  **Select Muscles**: Click on muscle names in the list to add them to your selection.
5.  Click **Generate Visualization**. The image will appear in the main viewport.

### 🔍 Exploring Exercises
1.  Click the **ExerciseDB** tab in the sidebar.
2.  Use the **Search Bar** in the main area to find exercises (e.g., "Deadlift", "Bench Press").
3.  Click on an exercise card to view:
    *   **Animated GIF**: Proper form demonstration.
    *   **Instructions**: How to perform the movement safely.
    *   **Muscle Info**: Target and secondary muscles.

---

## ❓ Troubleshooting

*   **"Failed to generate visualization"**: Usually indicates an invalid API key or exceeding rate limits on RapidAPI.
*   **Fallback Muscles**: If the backend is unavailable, the frontend will automatically use a fallback list of common muscles so you can still test the UI.
*   **CORS Errors**: If running locally, ensure the backend allows `http://localhost:5173` (configured in `main.py`).

---

**Built with ❤️ for Fitness Enthusiasts.**
