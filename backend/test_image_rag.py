from image_rag import TrailMapRAG
from dotenv import load_dotenv
import os

def test_image_rag():
    # Initialize the TrailMapRAG system
    rag = TrailMapRAG()
    
    # Test 1: Basic Query
    print("\nTest 1: Basic Query")
    results = rag.query("ski resort with expert terrain", k=3)
    print("Query Results:")
    for path, score in results:
        print(f"Image: {path}")
        print(f"Similarity Score: {score:.4f}")
        print(f"Metadata: {rag.get_metadata(path)}\n")

    # Test 2: Generate Enhanced Map
    print("\nTest 2: Generate Enhanced Map")
    try:
        result = rag.generate_enhanced_map(
            query="mountain resort with both beginner and expert trails",
            difficulty_level="intermediate",
            size="512x512",
            num_references=2
        )
        print("Generated Map URL:", result["generated_image_url"])
        print("Reference Maps Used:", result["reference_maps"])
        print("Features Incorporated:", result["features_incorporated"])
    except Exception as e:
        print(f"Error generating enhanced map: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    
    # Verify environment variables
    required_vars = ['OPENAI_API_KEY', 'PINECONE_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        exit(1)
        
    test_image_rag() 