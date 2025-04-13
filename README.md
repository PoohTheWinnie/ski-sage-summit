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
   - The pipeline processes documents through several stages:
     1. **Text Extraction**: Extracts raw text from PDFs and TXT files
     2. **Document Processing**: Processes and stores extracted text with metadata
     3. **Chunking**: Splits documents into smaller, semantically meaningful chunks
     4. **Vector Embedding**: Converts text chunks into vector embeddings
     5. **Storage**: Stores embeddings in Pinecone vector database

3. **Running the Pipeline**
   ```bash
   # Ensure you have set up your environment variables
   export PINECONE_API_KEY='your-api-key'
   
   # Run the processing pipeline
   python backend/text_processor.py
   ```

4. **Configuration**
   - Chunk size: 1000 characters
   - Chunk overlap: 200 characters
   - Embedding model: all-MiniLM-L6-v2 (384 dimensions) from chroma
   - Vector store: Pinecone (serverless, AWS us-east-1)

5. **Output**
   - Processed documents: `data/texts/processed/`
   - Text chunks: `data/texts/chunks/`
   - Vector embeddings: Stored in Pinecone index

The processed data is used by the Ski Encyclopedia Mode to provide accurate, context-aware responses to skiing-related queries.

## Agents

- Ski Encycopedia Mode
- Ski Map Creator Mode

## Roadmap

- Users
- Storage of chats
- Find data sources for ski maps (Legendary Ski Artist James Niehues)
- Document potential RAG model
- Tests?


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