# beyondlearning
# Beyond Learning 📚🧠
> **Real‑time classroom analytics**



---

## Table of Contents
1. [About the Project](#about-the-project)
2. [Demo](#demo)
---

## About the Project
Beyond Learning helps instructors adapt on the fly by providing **privacy‑aware, real‑time engagement metrics**:

| Feature | Description |
| ------- | ----------- |
| **Live Inference** | Runs on webcam/RTSP at up to ≈ 30 FPS on mid‑tier GPU. |
| **Focus Classification** | Custom model trained on (yolov8n) labels each tracked student as *focused* or *unfocused* every frame |
| **Metrics Logger** | Auto‑dumps CSVs with labels, frame IDs, timestamps, and confidences. |
| **Insights Review** | Uses classical regression and classification modelling on collected metrics to generate insights *coming soon...*|
| **Dashboard** | (Optional) Flask + Plotly app for real‑time charts and lecture summaries. *coming soon...*|
| **Modularity** | Swap detectors, trackers, sequence models with minimal refactoring. |

---

## Demo
```bash
git clone https://github.com/tatendajoes/BeyondLearning.git && cd BeyondLearning
pip install -r requirements.txt
python dashboard.py 
"Open New Terminal"
python client.py
"navigate to dashboard http://127.0.0.1:8050/classes"


