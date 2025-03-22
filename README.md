# RAG Visualization

A Manim-based visualization explaining the Retrieval-Augmented Generation (RAG) pipeline using LlamaIndex concepts.

## About This Project

This project demonstrates an efficient workflow for creating research paper and technical concept visualizations using [Cursor](https://cursor.sh) and [Manim](https://www.manim.community/). While one-shot prompt generation with AI assistants can be challenging, this project shows how iterative refinement with Cursor can produce high-quality technical visualizations.

The workflow combines Cursor's AI capabilities with Manim's powerful animation features to create clear, educational content. This repository serves as a practical example of this approach, specifically for explaining the RAG (Retrieval-Augmented Generation) concept.

## Overview

This project creates an educational animation that breaks down the RAG pipeline into its key stages:
1. Loading Stage
2. Indexing Stage
3. Querying Stage

The visualization helps understand how RAG enhances Large Language Models (LLMs) by incorporating external knowledge through efficient retrieval mechanisms.

## Video

[![RAG Visualization](https://img.youtube.com/vi/9J_VWE08yCo/maxresdefault.jpg)](https://youtu.be/9J_VWE08yCo?si=h4JcaHEWv4yGqZG8)

## Requirements

- Python 3.7+
- Manim (Community Edition)
- LaTeX (for mathematical equations)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rag-visualization.git
cd rag-visualization
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install LaTeX (if not already installed):
- For macOS: `brew install --cask mactex`
- For Ubuntu: `sudo apt-get install texlive-full`

## Usage

To run the visualization:

```bash
manim -pqm rag_visualization_v2.py RAGVisualizationV2
```

The `-pqm` flags mean:
- `-p`: Preview the animation
- `-q`: Medium quality
- `-m`: Don't leave the terminal open

## Project Structure

- `rag_visualization_v2.py`: Main visualization script
- `requirements.txt`: Project dependencies
- `media/`: Generated animation files (not tracked in git)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 