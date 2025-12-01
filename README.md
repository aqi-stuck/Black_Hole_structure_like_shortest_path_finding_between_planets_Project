# Celestial Bodies Pathfinding Visualization

![Celestial Pathfinding](https://via.placeholder.com/1000x750/0a0a20/ffffff?text=Celestial+Bodies+Pathfinding+Visualization) [web:42]

Interactive visualization combining orbital mechanics simulation with Dijkstra's shortest path algorithm. Watch planets orbit a central black hole, satellites circle planets, and discover optimal paths between celestial bodies through dynamic graph connections. [web:23]

## ✨ Features

- 🌌 **Realistic Orbital Mechanics**: 5 planets orbit central black hole with variable speeds (0.0015-0.003 rad/frame)
- 🛰️ **Satellite Systems**: 12 satellites orbit planets with motion trails (12-point history)
- ⭐ **Stray Stars**: 40 free-moving stars that get captured into orbits (speed 0.08-0.25 px/frame)
- 📊 **Dynamic Graph Construction**: 18-node graph (5 planets + 12 satellites + 1 black hole) updates every frame
- 🔍 **Dijkstra's Algorithm**: Real-time shortest path computation with heap optimization O((V+E)logV)
- 🎨 **Bezier Curve Paths**: Smooth, colored curved paths (3-color palette cycling)
- 🖱️ **Interactive Querying**: Click any two objects to see shortest path instantly
- ⚡ **60 FPS Performance**: Smooth real-time animations with dynamic edge rendering [web:42]

## 🛠️ Tech Stack

| Technology | Purpose                          |
|------------|----------------------------------|
| **Python 3** | Core language [web:23]          |
| **Pygame**  | Graphics & interaction           |
| **heapq**   | Priority queue for Dijkstra      |
| **math**    | Trigonometry & geometry          |

## 🚀 Quick Start

### Prerequisites
- Python 3.6+
- 1024×768 display or higher

### Installation
Clone/Download project
git clone <your-repo-url>
cd celestial-bodies-pathfinding

Install dependencies
pip install pygame

text

### Run
python space_graph_thing.py

text

**Controls**: Click any **two objects** (planets/yellow glow, satellites/white dots with trails, black hole/dark center) to visualize shortest path! [web:79]

## 🎮 How It Works

1. **Celestial Bodies** continuously orbit following circular orbital mechanics
2. **Graph** auto-builds connecting nearby objects:
   - Planet-Planet: < 350px distance
   - Satellite-Planet: Orbital distance (35-65px)
   - Black Hole-Planet: < 450px distance
3. **Click** first object → **Click** second object
4. **Dijkstra** computes optimal path through weighted graph
5. **Bezier curves** render beautiful colored paths with perpendicular control points

Black Hole ←→ Planets ←→ Satellites (18 total nodes)
↑ ↑ ↑
Weighted Edges (Euclidean Distance)

text

## 📁 Project Structure

celestial-bodies-pathfinding/
├── space_graph_thing.py # Complete single-file implementation
├── README.md # This file
├── LICENSE # MIT License
└── CONTRIBUTING.md # Contribution guide

text

## 🙏 Acknowledgments and Credits

The core **black hole gravity and physics simulation concepts** were inspired by and adapted from the excellent work in the [kavan010/black_hole](https://github.com/kavan010/black_hole) repository [attached_file:1]. This C++ repository provides sophisticated black hole simulation covering gravitational physics and lensing effects.

**My Original Contributions:**
- Complete re-implementation in **Python** with **Pygame**
- Integration of **Data Structures & Algorithms (DSA)**
- **Dijkstra's shortest path algorithm** with heap optimization
- **Dynamic graph construction** (18-node weighted graph)
- **Interactive visualization** with Bezier curve paths
- **Satellite orbital mechanics** and stray star capture system
- **Real-time 60 FPS rendering** with motion trails [web:58]

Special thanks to kavan010 for making their physics work available as foundation for this visualization project.

## 🎓 Learning Outcomes

- **Graph Theory**: Weighted graphs, adjacency matrices, dynamic connectivity
- **Algorithms**: Dijkstra's with heapq O((V+E)logV), path reconstruction
- **Physics**: Circular orbital mechanics \(x = r\cos(\theta), y = r\sin(\theta)\)
- **Graphics**: Pygame rendering pipeline, collision detection, Bezier curves
- **OOP**: Clean class design (BH, P, S, St) with single responsibilities [web:23]

## 🔮 Roadmap

- [ ] A* pathfinding algorithm implementation
- [ ] 3D visualization extension
- [ ] N-body gravitational physics
- [ ] Path length/distance statistics display
- [ ] Simulation speed/pause controls
- [ ] Algorithm comparison visualization
- [ ] Path export to JSON/CSV [web:42]

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details. [web:35]

MIT License
Copyright (c) 2025 [Syed Aqdas Munire] - Harīpur, Khyber Pakhtunkhwa, Pakistan

Permission is hereby granted, free of charge, to any person obtaining a copy...
[Full text in LICENSE file]

text

## 🤝 Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details. [web:36]

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Open Pull Request

**Guidelines:**
- Follow [PEP 8](https://peps.python.org/pep-0008/) Python style
- Add comments for complex algorithms
- Test new features thoroughly
- Update documentation for changes [web:33]

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/celestial-bodies-pathfinding/issues)
- 💬 **Feature Requests**: Discussions or Issues
- 📧 **Contact**: your.email@example.com

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| Nodes | 18 |
| Planets | 5 |
| Satellites | 12 |
| Stray Stars | 40 |
| FPS | 60 |
| Window | 1000×750px [web:69] |

---

⭐ **Star this repository if you found it useful!** ⭐