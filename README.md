# beyondlearning
# Beyond Learning 📚🧠
> **Real‑time classroom analytics**

![build](https://img.shields.io/badge/build-passing-brightgreen)
![license](https://img.shields.io/badge/license-MIT-blue)

---

## Table of Contents
1. [About the Project](#about-the-project)
2. [Demo](#demo)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Quick Start](#quick-start)
7. [Configuration](#configuration)
8. [Usage Guide](#usage-guide)
9. [Data & Models](#data--models)
10. [Results](#results)
11. [Roadmap](#roadmap)
12. [Contributing](#contributing)
13. [Testing](#testing)
14. [Deployment](#deployment)
15. [License](#license)
16. [References](#references)
17. [Contact](#contact)
18. [Acknowledgements](#acknowledgements)

---

## About the Project
Beyond Learning helps instructors adapt on the fly by providing **privacy‑aware, real‑time engagement metrics**:

| Feature | Description |
| ------- | ----------- |
| **Live Inference** | Runs on webcam/RTSP at up to ≈ 30 FPS on mid‑tier GPU. |
| **Focus Classification** | LSTM labels each tracked student as *focused* or *unfocused* every ~33 ms. |
| **Metrics Logger** | Auto‑dumps CSVs with labels, frame IDs, timestamps, confidences. |
| **Dashboard** | (Optional) Flask + Plotly app for real‑time charts and lecture summaries. |
| **Modularity** | Swap detectors, trackers, sequence models with minimal refactor. |

---

## Demo
```bash
git clone https://github.com/<YOUR‑ORG>/BeyondLearning.git && cd BeyondLearning
python scripts/download_models.py      # fetch YOLO weights (≈35 MB)
python vision.py --source demo/demo.mp4
