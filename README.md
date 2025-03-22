# RAG Visualization using Manim

This project contains a Manim visualization that explains the Retrieval-Augmented Generation (RAG) process.

## Setup

1. Install system dependencies:
   
   **macOS (using Homebrew):**
   ```bash
   brew install ffmpeg cairo pkg-config
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install ffmpeg libcairo2-dev pkg-config
   ```
   
   **Windows:**
   - Download and install [FFmpeg](https://ffmpeg.org/download.html)
   - Add FFmpeg to your PATH environment variable

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the visualization:
```bash
manim -pqm rag_visualization.py RAGScene
```

## Description

This visualization demonstrates the key components and workflow of Retrieval-Augmented Generation (RAG), including:
- Document corpus and retrieval process
- Query encoding and document retrieval
- Generation process with retrieved context
- Final output generation

Based on the paper: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020) 