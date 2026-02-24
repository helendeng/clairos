# Used during inference

def process_email_with_zero_shot(
                            email_text: str,
                            subject: str,
                            label_groups: dict,  # dict of group_name -> {category_name: description}
                            zero_shot_classify_fn,
                            category_thresholds: dict = None,  # dict of category_name -> threshold
                            default_threshold: float = 0.5,
                            split_by: str = "sentence"  # "sentence" or "paragraph"
                        ) -> dict:
    """
    Controller that splits email into chunks, runs all label groups on each chunk,
    and aggregates results. Uses parallel group classification instead of hierarchical
    two-stage approach - no top-level gating blocks subcategory detection.

    Parameters:
    -----------
    email_text : str
        The full email body text
    subject : str
        Email subject line
    label_groups : dict
        Groups of labels {group_name: {category_name: description}}
    zero_shot_classify_fn : function
        Your zero_shot_classify function
    category_thresholds : dict, optional
        Per-category thresholds {category_name: threshold_value}
        Example: {'Strategic.M&A': 0.5, 'Operational.Project.Technical_Blockers': 0.35}
    default_threshold : float
        Default threshold for categories not in category_thresholds (default 0.5)
    split_by : str
        How to split text: "sentence" or "paragraph"

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

    # Initialize category_thresholds if not provided
    if category_thresholds is None:
        category_thresholds = {}

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
        print("Warning: No chunks found after splitting.")
        return {
            'email_text': email_text,
            'subject': subject,
            'chunks': [],
            'aggregated_tags': []
        }

    print(f"Processing email with {len(chunks)} {split_by}(s)...")

    classified_chunks = []
    all_tags = set()

    for idx, chunk in enumerate(chunks):
        chunk_tags = []
        chunk_scores = {}

        # Run every group on this chunk - no hierarchical gating
        for _, group_labels in label_groups.items():
            candidate_labels = list(group_labels.values())

            result = zero_shot_classify_fn(
                chunk,
                candidate_labels,
                multi_label=True
            )

            # Map descriptions back to category names and apply per-category threshold
            for label_desc, score in zip(result['labels'], result['scores']):
                for cat_name, cat_desc in group_labels.items():
                    if cat_desc == label_desc:
                        chunk_scores[cat_name] = score
                        
                        # Use category-specific threshold if available, otherwise use default
                        threshold = category_thresholds.get(cat_name, default_threshold)
                        
                        if score >= threshold:
                            chunk_tags.append(cat_name)
                            all_tags.add(cat_name)
                        break

        chunk_data = {
            'chunk_id': idx,
            'text': chunk,
            'tags': chunk_tags,
            'scores': chunk_scores
        }

        classified_chunks.append(chunk_data)

        if chunk_tags:
            print(f"Chunk {idx}: {', '.join(chunk_tags)}")
        else:
            print(f"Chunk {idx}: No tags above threshold")

    result = {
        'email_text': email_text,
        'subject': subject,
        'chunks': classified_chunks,
        'aggregated_tags': sorted(list(all_tags))
    }

    print(f"\nEmail processed: {len(classified_chunks)} chunks, {len(all_tags)} unique tags")
    print(f"Final tags: {', '.join(result['aggregated_tags']) if result['aggregated_tags'] else 'None'}")

    return result