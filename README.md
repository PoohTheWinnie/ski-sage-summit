<p align="center">
  <img src="frontend/public/logo.png" height="200" style="border-radius: 20px;">
  <h3 align="center">
    <a href="">Ski Sage Summit</a>
  </h3>
</p>


## Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![FastAPI][FastAPI]][FastAPI-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![TailwindCSS][TailwindCSS]][TailwindCSS-url]


## Getting Started Locally

First, create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then, install the dependencies:

```bash
npm install
# or
yarn
# or
pnpm install
```

### Environment Variables

Create a `.env` file in the root directory:

```bash

```

Then, run the development server (python dependencies will be installed automatically here):

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

The FastApi server will be running on [http://127.0.0.1:8000](http://127.0.0.1:8000) – feel free to change the port in `package.json` (you'll also need to update it in `next.config.js`).

## Data Sources

### Text Processing Pipeline

The project uses a sophisticated text processing pipeline to prepare documents for the RAG (Retrieval-Augmented Generation) system. Here's how it works:

1. **Document Collection**
   - Place your source documents (PDF or TXT files) in the `data/texts` directory
   - Supported formats: PDF and TXT files
   - Documents can contain ski-related information, guides, or encyclopedic content

2. **Processing Pipeline**
   The pipeline processes documents through several stages:

   a. **Text Extraction & Processing**
      - Extracts raw text from PDFs and TXT files
      - Preserves document structure
      - Stores processed documents with metadata

   b. **Text Chunking**
      - Chunk Size: 1000 characters
      - Overlap: 200 characters
      - Intelligent splitting using recursive character text splitter
      - Preserves semantic boundaries using multiple separators:
        - Paragraphs (\n\n)
        - Lines (\n)
        - Sentences (., !, ?)
        - Clauses (,)
        - Words ( )

   c. **Vector Embedding**
      - Uses all-MiniLM-L6-v2 (384 dimensions) from chroma
      - Batch processing (100 chunks per batch)
      - Each chunk stored with:
        - Unique ID
        - Vector embedding
        - Metadata (title, source, chunk index)

   d. **Storage**
      - Vector store: Pinecone (serverless, AWS us-east-1)
      - Processed documents: `data/texts/processed/`
      - Text chunks: `data/texts/chunks/`
      - Vector embeddings: Stored in Pinecone index

3. **Running the Pipeline**
   ```bash
   # Ensure you have set up your environment variables
   export PINECONE_API_KEY='your-api-key'
   
   # Run the processing pipeline
   python backend/text_processor.py
   ```

The processed data is used by the Ski Encyclopedia Mode to provide accurate, context-aware responses to skiing-related queries.

## Encyclopedia RAG Model

The Ski Encyclopedia Mode uses a sophisticated Retrieval-Augmented Generation (RAG) system to provide accurate, context-aware responses to skiing-related queries. Here's a detailed breakdown of how it works:

### Architecture Overview

1. **Embedding Model**
   - Model: all-MiniLM-L6-v2 (384 dimensions)
   - Implementation: SentenceTransformer via ChromaDB
   - Purpose: Converts text chunks and queries into semantic vectors

2. **Vector Database**
   - Platform: Pinecone (Serverless)
   - Index Configuration:
     - Metric: Cosine Similarity
     - Dimensions: 384
     - Region: AWS us-east-1

3. **Language Model**
   - Model: GPT-4 Turbo
   - Role: Expert skiing instructor and guide
   - Temperature: 0.7 (balanced between creativity and accuracy)

### Processing Pipeline

1. **Document Processing**
   - Supports PDF and TXT formats
   - Extracts clean text while preserving structure
   - Stores processed documents with metadata

2. **Text Chunking**
   - Chunk Size: 1000 characters
   - Overlap: 200 characters
   - Intelligent splitting using recursive character text splitter
   - Preserves semantic boundaries using multiple separators:
     - Paragraphs (\n\n)
     - Lines (\n)
     - Sentences (., !, ?)
     - Clauses (,)
     - Words ( )

3. **Vector Embedding**
   - Batch processing (100 chunks per batch)
   - Each chunk stored with:
     - Unique ID
     - Vector embedding
     - Metadata (title, source, chunk index)

### Query Pipeline

1. **Query Processing**
   - User query converted to embedding vector
   - Semantic search in Pinecone index
   - Retrieves top 5 most relevant chunks

2. **Context Assembly**
   - Combines retrieved chunks
   - Maintains original text integrity
   - Preserves source attribution

3. **Response Generation**
   - System prompt enforces:
     - Practical, actionable advice
     - Clear technical explanations
     - Safety considerations
     - Proper skiing terminology
   - Generates responses grounded in retrieved context


[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[TailwindCSS]: https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white
[TailwindCSS-url]: https://tailwindcss.com/