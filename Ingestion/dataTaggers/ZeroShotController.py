# Used during inference

def process_email_with_zero_shot(
                            email_text: str,
                            subject: str,
                            high_level_labels: dict,
                            low_level_labels: dict,
                            zero_shot_classify_fn,
                            high_level_threshold: float = 0.5,
                            low_level_threshold: float = 0.5,
                            split_by: str = "sentence"  # "sentence" or "paragraph"
                        ) -> dict:
    """
    Controller that splits email into chunks, classifies each, and aggregates results.
    
    Parameters:
    -----------
    email_text : str: The full email body text
    subject : str: Email subject line
    high_level_labels : dict: High level category labels list -> description mapping
    low_level_labels : dict: Sub-Categories label list -> description mapping
    zero_shot_classify_fn : function: Your zero_shot_classify function
    high_level_threshold : float: Confidence threshold for predictions during high level labeling (default 0.5)
    low_level_threshold : float: Confidence threshold for predictions during low level labeling (default 0.5)
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
    
    # Combine subject and body
    full_text = f"Subject: {subject}\n\n{email_text}"
    
    # Split into chunks
    if split_by == "sentence":
        import re
        chunks = re.split(r'[.!?]+', full_text)
        chunks = [c.strip() for c in chunks if c.strip() and len(c.strip()) > 10]
    elif split_by == "paragraph":
        chunks = [p.strip() for p in full_text.split('\n\n') if p.strip()]
    else:
        raise ValueError(f"Invalid split_by: {split_by}")
    
    if not chunks:
        print("⚠️ No chunks found after splitting.")
        return {
            'email_text': email_text,
            'subject': subject,
            'chunks': [],
            'aggregated_tags': []
        }
    
    print(f"📧 Processing email with {len(chunks)} {split_by}(s)...")
    
    # Process each chunk with hierarchical classification
    classified_chunks = []
    all_tags = set()
    
    for idx, chunk in enumerate(chunks):
        
        # === STAGE 1: Top-level classification ===
        stage1_candidate_labels = list(high_level_labels.values())
        stage1_result = zero_shot_classify_fn(
            chunk,
            stage1_candidate_labels,
            multi_label=True
        )
        
        # Map descriptions back to top-level category names
        detected_top_level = []
        stage1_scores = {}
        
        for label_desc, score in zip(stage1_result['labels'], stage1_result['scores']):
            for cat_name, cat_desc in high_level_labels.items():
                if cat_desc == label_desc:
                    stage1_scores[cat_name] = score
                    if score >= high_level_threshold:
                        detected_top_level.append(cat_name)
                    break
        
        # === STAGE 2: Subcategory classification ===
        chunk_tags = []
        chunk_scores = {}
        
        for top_cat in detected_top_level:
            # Check if this top-level has subcategories
            if top_cat not in low_level_labels:
                # No subcategories - just use top-level tag
                chunk_tags.append(top_cat)
                chunk_scores[top_cat] = stage1_scores[top_cat]
                continue
            
            # Get subcategories for this top-level
            subcat_dict = low_level_labels[top_cat]
            stage2_candidate_labels = list(subcat_dict.values())
            
            # Run zero-shot on subcategories
            stage2_result = zero_shot_classify_fn(
                chunk,
                stage2_candidate_labels,
                multi_label=True
            )
            
            # Map descriptions back to subcategory names
            for label_desc, score in zip(stage2_result['labels'], stage2_result['scores']):
                for subcat_name, subcat_desc in subcat_dict.items():
                    if subcat_desc == label_desc:
                        chunk_scores[subcat_name] = score
                        if score >= low_level_threshold:
                            chunk_tags.append(subcat_name)
                            all_tags.add(subcat_name)
                        break
        
        # Store classified chunk
        chunk_data = {
            'chunk_id': idx,
            'text': chunk,
            'stage1_detected': detected_top_level,
            'stage1_scores': stage1_scores,
            'tags': chunk_tags,
            'scores': chunk_scores
        }
        
        classified_chunks.append(chunk_data)
        
        # "Save to database"
        if chunk_tags:
            print(f"✅ Chunk {idx}: {', '.join(chunk_tags)}")
        else:
            print(f"ℹ️  Chunk {idx}: No tags above threshold")
    
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