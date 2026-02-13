# Backend API Documentation

This document outlines the available API endpoints for the Muscle Visualizer and ExerciseDB integration.

## Base URL
`http://localhost:8000` (for local development)

### **Interactive API Reference**
FastAPI provides automatic interactive documentation:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Authentication
No authentication is required for these endpoints from the frontend. The backend handles the RapidAPI key injection securely.

---

## **1. Muscle Visualization Endpoints**
These endpoints interface with the Muscle Visualizer RapidAPI to generate anatomical visualizations.

### **GET /api/v1/muscles**
**Description:**  
Get the list of available muscle groups that can be visualized.

**Parameters:**  
None

**Response:**  
- **200 OK**: JSON array of strings (muscle names).
  ```json
  [
    "biceps",
    "triceps",
    "calves",
    ...
  ]
  ```

### **GET /api/v1/visualize/muscles**
**Description:**  
Generate an image highlighting specific muscles.

**Query Parameters:**  
- `muscles` (string, **required**): Comma-separated list of muscles to highlight (e.g., "biceps_brachii,triceps_brachii").
- `color` (string, optional): Hex color code for the highlight (e.g., "FF0000"). Default: Red.

**Response:**  
- **200 OK**: Image (JPEG) binary data.

### **GET /api/v1/visualize/heatmap**
**Description:**  
Generate a heatmap visualization for specified muscles.

**Query Parameters:**  
- `muscles` (string, **required**): Comma-separated list of muscles.
- `colors` (string, optional): Comma-separated list of hex color codes corresponding to each muscle, or a single global color.

**Response:**  
- **200 OK**: Image (JPEG) binary data.

### **GET /api/v1/visualize/workout**
**Description:**  
Generate a workout activation visualization, highlighting primary (target) and secondary muscles.

**Query Parameters:**  
- `targetMuscles` (string, **required**): Comma-separated list of primary target muscles.
- `targetMusclesColor` (string, **required**): Hex color code for target muscles (e.g., "#FF0000").
- `secondaryMuscles` (string, optional): Comma-separated list of secondary muscles.
- `secondaryMusclesColor` (string, optional): Hex color code for secondary muscles.

**Response:**  
- **200 OK**: Image (JPEG) binary data.

---

## **2. ExerciseDB Endpoints**
These endpoints interface with the ExerciseDB RapidAPI to provide exercise data.

### **GET /api/v1/edb/muscles**
**Description:**  
Get the list of available muscle groups from ExerciseDB.

**Parameters:**  
None

**Response:**  
- **200 OK**: JSON array of muscle names.

### **GET /api/v1/edb/equipments**
**Description:**  
Get the list of available equipment types (e.g., "dumbbell", "barbell").

**Parameters:**  
None

**Response:**  
- **200 OK**: JSON array of equipment names.

### **GET /api/v1/edb/exercisetypes**
**Description:**  
Get the list of available exercise types (e.g., "strength", "cardio").

**Parameters:**  
None

**Response:**  
- **200 OK**: JSON array of exercise types.

### **GET /api/v1/edb/exercises/search**
**Description:**  
Search for exercises by a keyword.

**Query Parameters:**  
- `search` (string, **required**): The search term (e.g., "bench press").

**Response:**  
- **200 OK**: JSON array of exercise objects.
  ```json
  [
    {
      "id": "123",
      "name": "Barbell Bench Press",
      "target": "pectorals",
      "bodyPart": "chest",
      "equipment": "barbell",
      "gifUrl": "http://...",
      ...
    },
    ...
  ]
  ```

### **GET /api/v1/edb/exercises**
**Description:**  
List exercises with optional filtering by name or keywords.

**Query Parameters:**  
- `name` (string, optional): Filter by exact name.
- `keywords` (string, optional): Filter by keywords.

**Response:**  
- **200 OK**: JSON array of exercise objects.

### **GET /api/v1/edb/exercises/{exercise_id}**
**Description:**  
Get detailed information for a specific exercise by its ID.

**Path Parameters:**  
- `exercise_id` (string, **required**): The unique identifier of the exercise.

**Response:**  
- **200 OK**: JSON object containing exercise details.

---

## **3. Data Models**

### **Exercise Object**
When calling `search`, `list`, or `details` endpoints in the ExerciseDB section, you will receive exercise objects with the following structure:
```typescript
interface Exercise {
  exerciseId: string;    // Unique identifier
  name: string;          // Name of the exercise
  gifUrl: string;        // Animated preview URL
  videoUrl?: string;     // (Optional) Video tutorial link
  equipment: string;     // Primary equipment required
  bodyPart: string;      // Body part targeted (e.g., "chest")
  target: string;        // Primary target muscle
  secondaryMuscles?: string[]; // List of secondary muscles
  instructions?: string[];     // Array of step-by-step instructions
}
```

---

## **4. Implementation Notes**

### **Handling Visualization Responses**
The visualization endpoints (`/visualize/...`) return raw JPEG binary data. In React/Frontend, you should handle these as Blobs:
```javascript
const response = await axios.get(url, { responseType: 'blob' });
const imageUrl = URL.createObjectURL(response.data);
```

### **Response Wrapping**
Some endpoints may return data wrapped in a "success" container (check your network tab). Always handle this pattern:
```javascript
const extractData = (data) => {
  if (data && data.success && data.data) {
    return data.data;
  }
  return data;
};
```

### **Error Handling**
- **400 Bad Request**: Typically missing required query parameters.
- **500 Internal Server Error**: Backend failed to reach RapidAPI or an unexpected error occurred.
- **404 Not Found**: For specific resource IDs that don't exist.

### **CORS**
The backend is configured to allow requests from `http://localhost:5173`. If your dev server runs on a different port, please let the backend team know.
