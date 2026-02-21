# Used during inference

def process_email_with_zero_shot(
                            email_text: str,
                            subject: str,
                            labels_dict: dict,
                            zero_shot_classify_fn,
                            threshold: float = 0.5,
                            split_by: str = "sentence"  # "sentence" or "paragraph"
                        ) -> dict:
    """
    Controller that splits email into chunks, classifies each, and aggregates results.
    
    Parameters:
    -----------
    email_text : str: The full email body text
    subject : str: Email subject line
    labels_dict : dict: Your category name -> description mapping
    zero_shot_classify_fn : function: Your zero_shot_classify function
    threshold : float: Confidence threshold for predictions (default 0.5)
    split_by : str: How to split text: "sentence" or "paragraph"
    
    Returns:
    --------
    result : dict
        {
            'email_text': full text,
            'subject': subject,
            'chunks': [list of classified chunks],
            'aggregated_tags': [unique tags across all chunks]
        }
    """
    
    # Combine subject and body for processing
    full_text = f"Subject: {subject}\n\n{email_text}"
    
    # Split into chunks
    if split_by == "sentence":
        # Simple sentence splitting (split on ., !, ?)
        import re
        chunks = re.split(r'[.!?]+', full_text)
        chunks = [c.strip() for c in chunks if c.strip() and len(c.strip()) > 10]  # Filter out very short chunks
    elif split_by == "paragraph":
        # Split on double newlines
        chunks = [p.strip() for p in full_text.split('\n\n') if p.strip()]
    else:
        raise ValueError(f"Invalid split_by: {split_by}. Use 'sentence' or 'paragraph'")
    
    if not chunks:
        print("⚠️ No chunks found after splitting. Email might be too short or empty.")
        return {
            'email_text': email_text,
            'subject': subject,
            'chunks': [],
            'aggregated_tags': []
        }
    
    print(f"📧 Processing email with {len(chunks)} {split_by}(s)...")
    
    # Get candidate labels
    candidate_labels = list(labels_dict.values())
    
    # Process each chunk
    classified_chunks = []
    all_tags = set()
    
    for idx, chunk in enumerate(chunks):
        # Run zero-shot classification
        result = zero_shot_classify_fn(
            chunk,
            candidate_labels,
            multi_label=True
        )
        
        # Map descriptions back to category names and apply threshold
        chunk_tags = []
        chunk_scores = {}
        
        for label_desc, score in zip(result['labels'], result['scores']):
            # Find category name from description
            category_name = None
            for cat_name, cat_desc in labels_dict.items():
                if cat_desc == label_desc:
                    category_name = cat_name
                    break
            
            if category_name is None:
                continue
            
            chunk_scores[category_name] = score
            
            # Apply threshold
            if score >= threshold:
                chunk_tags.append(category_name)
                all_tags.add(category_name)
        
        # Store classified chunk
        chunk_data = {
            'chunk_id': idx,
            'text': chunk,
            'tags': chunk_tags,
            'scores': chunk_scores
        }
        
        classified_chunks.append(chunk_data)
        
        # "Save to database" (print statement for now)
        if chunk_tags:
            print(f"✅ Saved chunk {idx} to database domains: {', '.join(chunk_tags)}")
        else:
            print(f"ℹ️  Chunk {idx} had no tags above threshold")
    
    # Aggregate results
    result = {
        'email_text': email_text,
        'subject': subject,
        'chunks': classified_chunks,
        'aggregated_tags': sorted(list(all_tags))
    }
    
    print(f"\n📊 Email processed: {len(classified_chunks)} chunks, {len(all_tags)} unique tags")
    print(f"Final tags: {', '.join(result['aggregated_tags']) if result['aggregated_tags'] else 'None'}")
    
    return result