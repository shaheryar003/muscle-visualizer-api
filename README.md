# 🏋️‍♂️ Muscle Visualizer API

Generate dynamic anatomical muscle visualizations for health and fitness applications. Create customizable muscle diagrams with heatmaps, targeted highlights, and workout-specific activation patterns for both male and female body models.

[![API Documentation](https://img.shields.io/badge/API-Documentation-blue)](https://muscle-visualizer.exercisedb.dev/docs)
[![RAPIDAPI](https://img.shields.io/badge/RapidAPI-MuscleVisualizerAPI-red)](https://rapidapi.com/ascendapi/api/muscle-visualizer-api)
[![Website](https://img.shields.io/badge/Website-exercisedb.dev-green)](https://exercisedb.dev)

## 🎨 Visualization Modes

### 🔥 Heatmap Visualization

<img src="https://cdn.exercisedb.dev/exercisedb/heatmap-map.webp" alt="Heatmap Visualization Example" width="400" />

Generate intensity-based muscle visualizations where each muscle group displays a unique color. Perfect for:

- **Intensity mapping** - Show workout difficulty across muscle groups
- **Progress tracking** - Visualize muscle development over time
- **Fatigue mapping** - Display muscle soreness or recovery status
- **Custom color schemes** - Assign any color to each muscle group

### 🎯 Muscle Group Highlighting

<img src="https://cdn.exercisedb.dev/exercisedb/muscle-map.webp" alt="Muscle Group Highlighting Example" width="400" />

Create simple, clear muscle diagrams with specified groups highlighted in a single color. Ideal for:

- **Muscle identification** - Educational content and anatomy guides
- **Exercise targeting** - Show which muscles an exercise works
- **Workout planning** - Visualize muscle group focus
- **Basic visualization** - Clean, straightforward muscle highlighting

### 💪 Workout Activation

<img src="https://cdn.exercisedb.dev/exercisedb/workout-map.png" alt="Workout Activation Example" width="400" />

Display primary and secondary muscle activation with two distinct colors. Perfect for:

- **Exercise demonstrations** - Show primary vs secondary muscle engagement
- **Workout analysis** - Visualize compound vs isolation exercises
- **Training optimization** - Understand muscle recruitment patterns
- **Form guides** - Illustrate proper muscle activation

## ✨ Features

- 🎨 **Custom Colors** - Set any hex/RGB color for muscle groups
- 🖼️ **Background Control** - Customize background colors
- 📐 **Size Options** - Generate images in various dimensions
- 📄 **Format Support** - Export as PNG, JPEG, or WebP
- 👥 **Body Models** - Both male and female anatomical models
- 🎭 **View Angles** - Front and back body views

## 🚀 Quick Start

### 1. Get Your API Key

Subscribe at [RapidAPI Muscle Visualizer API](https://rapidapi.com/ascendapi/api/muscle-visualizer-api)

### 2. Make Your First Request

```bash
curl -X GET "https://muscle-visualizer-api.p.rapidapi.com/v1/visualize/muscles?muscles=biceps,triceps&color=#FF5733" \
  -H "X-RapidAPI-Key: YOUR_API_KEY" \
  -H "X-RapidAPI-Host: muscle-visualizer-api.p.rapidapi.com"
```

### 3. Integrate Into Your App

Use the generated images in your fitness app, workout planner, or educational platform.

## 🔐 Authentication

All production API requests require authentication via RapidAPI:

1. Sign up and subscribe at [RapidAPI Muscle Visualizer API](https://rapidapi.com/ascendapi/api/muscle-visualizer-api)
2. Copy your API key from the RapidAPI dashboard
3. Include the key in your requests via the `X-RapidAPI-Key` header

```bash
curl -X GET "https://muscle-visualizer-api.p.rapidapi.com/v1/visualize/heatmap" \
  -H "X-RapidAPI-Key: YOUR_API_KEY" \
  -H "X-RapidAPI-Host: muscle-visualizer-api.p.rapidapi.com"
```

## 📚 API Endpoints

### Muscle Group Highlighting
```
GET /v1/visualize/muscles
```
Highlight specific muscle groups with a single color.

### Heatmap Visualization
```
GET /v1/visualize/heatmap
```
Generate intensity-based muscle visualizations with unique colors per muscle.

### Workout Activation
```
GET /v1/visualize/workout
```
Display primary and secondary muscle activation patterns.

### Muscle List
```
GET /v1/muscles
```
Retrieve all available muscle groups for visualization.

## 💡 Use Cases

- **Fitness Apps** - Show users which muscles they're targeting
- **Workout Planners** - Visualize muscle group distribution
- **Personal Training** - Create custom exercise diagrams
- **Physical Therapy** - Track rehabilitation progress
- **Education** - Teach anatomy and muscle groups
- **Health Tracking** - Monitor muscle development over time

## 📖 Documentation

- **Interactive API Docs**: [API Documentation](https://muscle-visualizer.exercisedb.dev/docs)
- **OpenAPI Specification**: Available at `/swagger` endpoint
- **LLM-friendly Documentation**: Available at `/llms.txt` endpoint

## 🔗 Related Projects

- **EXERCISEDB WITH VIDEOS AND IMAGES**: [v2.exercisedb.dev/docs](https://rapidapi.com/ascendapi/api/exercise-db-with-videos-and-images-by-ascendapi)
- **Official Website**: [exercisedb.dev](https://exercisedb.dev)

## 📬 Support & Contact

| Type | Contact |
|------|---------|
| **General Inquiries** | [hello@exercisedb.dev](mailto:hello@exercisedb.dev) |
| **Technical Support** | [support@exercisedb.dev](mailto:support@exercisedb.dev) |
| **Live Chat** | [exercisedb.dev/chat](https://t.me/exercisedb) |

---

**Built with ❤️ by [AscendAPI](https://exercisedb.dev)**
