# Kalakriti: Empowering Local Artists with AI

<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-blueviolet?style=for-the-badge" alt="AI-Powered"/>
  <img src="https://img.shields.io/badge/Art%20Marketplace-orange?style=for-the-badge" alt="Art Marketplace"/>
  <img src="https://img.shields.io/badge/Inclusive%20Promotion-green?style=for-the-badge" alt="Inclusive Promotion"/>
  <img src="https://img.shields.io/badge/Blockchain%20Valuation-9cf?style=for-the-badge" alt="Blockchain Valuation"/>
  <img src="https://img.shields.io/badge/Next.js-000?style=for-the-badge&logo=next.js" alt="Next.js"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Google%20Vertex%20AI-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white" alt="Vertex AI"/>
</p>

---

> **Kalakriti** is an AI-powered platform designed to support and elevate local artists by transforming their creativity into global opportunities. It combines art education, inclusive promotion, blockchain-based valuation, and a dynamic marketplace to create a holistic ecosystem for artists, collectors, and art lovers.

---

## 🌟 Features & Use Cases

- **AI Art Education**: Personalized, culturally respectful art lessons and tutorials for traditional and digital art forms.
- **Inclusive Promotion**: Special programs for women, rural, and differently-abled artists to ensure equal opportunities.
- **Art Marketplace & Auction**: Buy, sell, and auction artworks with transparent pricing and real-time analytics.
- **Blockchain Valuation**: Secure, transparent art valuation and micro-loan system using blockchain technology.
- **Market Trend Analysis**: AI-driven insights into trending art styles, buyer demographics, and optimal pricing.
- **Supply Chain Network**: Direct connection to verified suppliers for art materials and logistics.
- **Multimodal Experience**: Transform static art into videos, audio descriptions, and interactive experiences for accessibility and engagement.

---

## 🚀 Quick Start

### 1. Prerequisites
- [Node.js](https://nodejs.org/) (v18+ recommended)
- [Python 3.9+](https://www.python.org/)
- [MongoDB](https://www.mongodb.com/) instance (local or cloud)
- [Google Cloud Project](https://cloud.google.com/) (for Vertex AI & RAG)

### 2. Clone the Repository
```bash
git clone https://github.com/your-org/kalakriti.git
cd Kalakriti
```

### 3. Environment Setup
- Copy `.env.example` to `.env` in each relevant subdirectory and fill in your credentials (MongoDB URI, Google Cloud keys, etc).
- Install Python dependencies:
  ```bash
  cd art-valuation/pre-processor
  pip install -r requirements.txt
  ```
- Install Node.js dependencies for the web app:
  ```bash
  cd ../../kalakriti-website
  pnpm install # or npm install
  ```

### 4. Running the Platform
- **Backend (FastAPI, RAG, Pre-Processor):**
  ```bash
  # In art-valuation/pre-processor
  python main.py
  # In art-valuation/analytics (if using FastAPI endpoints)
  uvicorn main:app --reload
  ```
- **Frontend (Next.js):**
  ```bash
  cd kalakriti-website
  pnpm dev # or npm run dev
  ```
- Access the dashboard at [http://localhost:3000](http://localhost:3000)

---

## 🎨 Example Use Cases

- **Artists**: Learn new styles, promote your work, and access micro-loans for art supplies.
- **Collectors**: Discover, bid, and purchase unique artworks with verified provenance.
- **Institutions**: Run inclusive art programs, analyze market trends, and support local talent.
- **Educators**: Access AI-generated lesson plans and interactive art education modules.

---

## 🛠️ Code Structure Overview

```
Kalakriti/
├── ai_art_education/         # AI lesson generation, tutor agents, data models
├── art-valuation/
│   ├── analytics/            # RAG, blockchain valuation, FastAPI services
│   └── pre-processor/        # Image processing, CLIP, metadata extraction
├── kalakriti-website/        # Next.js frontend, dashboard, UI components
├── components.json           # UI config
├── requirements.txt          # Python dependencies
└── README.md
```

- **Agents**: Modular LLM agents for lesson generation, tutoring, and style comparison.
- **RAG Services**: Google Vertex AI-powered retrieval-augmented generation for art insights.
- **Pre-Processor**: Fast image metadata extraction using CLIP and custom pipelines.
- **Frontend**: Modern, responsive dashboard with Tailwind CSS and shadcn/ui components.

---

## 💡 Why Kalakriti?
- **Empowers local artists** with global reach and fair valuation.
- **Bridges tradition and technology** for a new era of art.
- **Promotes inclusivity** and accessibility in the art world.
- **Open, extensible, and community-driven.**

---

## 📄 License

This project is licensed under the [Apache 2.0 License](LICENSE).

---

## ⚠️ Disclaimer

Kalakriti is currently under active development. As such, you may encounter bugs, incomplete features, or unexpected behavior. We appreciate your understanding and welcome feedback as we work to improve and stabilize the platform.

---

<p align="center">
  <b>Kalakriti — Where Art Meets AI, and Every Artist Thrives.</b>
</p>
