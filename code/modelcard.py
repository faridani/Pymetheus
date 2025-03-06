import os
import json
from collections import Counter

def aggregate_fields_in_folder(folder_path):
    """
    Aggregate occurrences of model and title fields in JSON files within a folder.
    
    Args:
        folder_path (str): Path to the folder containing JSON files
        
    Returns:
        tuple: (sorted_models, sorted_titles) where each is a list of tuples 
               (field_value, count) sorted by count in descending order
    """
    # Initialize counters
    model_counter = Counter()
    title_counter = Counter()
    
    # Count files processed and files with errors
    files_processed = 0
    files_with_errors = 0
    
    # Process each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Extract and count the model field if it exists
                if 'model' in data:
                    model_counter[data['model']] += 1
                
                # Extract and count the title field if it exists
                if 'title' in data:
                    title_counter[data['title']] += 1
                
                files_processed += 1
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                files_with_errors += 1
    
    # Sort by count in descending order
    sorted_models = sorted(model_counter.items(), key=lambda x: x[1], reverse=True)
    sorted_titles = sorted(title_counter.items(), key=lambda x: x[1], reverse=True)
    
    # Print summary
    print(f"Processed {files_processed} files ({files_with_errors} with errors)")
    
    return sorted_models, sorted_titles

def main():
    # Ask for the folder path
    folder_path = input("Enter the path to the folder containing JSON files: ")
    
    # Validate folder path
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory")
        return
    
    # Aggregate models and titles
    model_counts, title_counts = aggregate_fields_in_folder(folder_path)
    
    # Print model results
    if model_counts:
        print("\nModel counts (in descending order):")
        for model, count in model_counts:
            print(f"{model}: {count}")
    else:
        print("No models found in the JSON files")
        
    # Print title results
    filtered_titles = [(title, count) for title, count in title_counts if count > 1]
    if filtered_titles:
        print("\nTitle counts (only showing titles that appear more than once):")
        for title, count in filtered_titles:
            print(f"{title}: {count}")
    else:
        print("\nNo titles appear more than once in the JSON files")

if __name__ == "__main__":
    main()