from image_rag import TrailMapRAG

def generate_trail_map_with_rag():
    rag = TrailMapRAG()
    
    # Example query
    result = rag.generate_enhanced_map(
        query="Create a trail map with wide beginner runs and a terrain park",
        difficulty_level="beginner",
        size="512x512",
        num_references=3
    )
    
    # Print results
    print("Generated Image URL:", result["generated_image_url"])
    print("\nReference Maps Used:")
    for ref_map in result["reference_maps"]:
        print(f"- {ref_map}")
    print("\nFeatures Incorporated:", ", ".join(result["features_incorporated"]))
    print("\nPrompt Used:", result["prompt_used"])

if __name__ == "__main__":
    generate_trail_map_with_rag() 