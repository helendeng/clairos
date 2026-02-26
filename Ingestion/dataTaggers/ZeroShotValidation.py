import numpy as np
from collections import defaultdict
import time
from typing import List, Dict, Tuple, Any
import pandas as pd

# Import the testing examples list and other needed libraries
from Ingestion.dataTaggers.ZeroShot import zero_shot_classify
from Ingestion.dataTaggers.ZeroShotTestExamples import zero_shot_test_examples
from Ingestion.Schemas.taxonomy import ZERO_SHOT_LABEL_GROUPS, CATEGORY_THRESHOLDS

def evaluate_zero_shot_classifier_parallel(
                    test_examples: List[Dict[str, Any]],
                    label_groups: Dict[str, Dict[str, str]],
                    zero_shot_classify_fn,
                    category_thresholds: Dict[str, float] = None,
                    default_threshold: float = 0.5,
                    multi_label: bool = True
                                ) -> Dict[str, Any]:
    """
    Evaluate parallel-group zero-shot classifier on test examples.

    Parameters:
    -----------
    test_examples : list of dict
        Each dict must have: {'text': str, 'true_labels': list of str}
        Note: true_labels should be subcategory names (e.g., 'Legal.Litigation.Legal_Disputes')

    label_groups : dict
        Maps group_name -> {category_name: description}
        Example: {
            'legal': {'Legal.Litigation.Legal_Disputes': 'Legal dispute...', ...},
            'financial_hr': {'HR.Performance_Reviews': '...', ...},
            ...
        }

    zero_shot_classify_fn : function
        Your zero_shot_classify function

    category_thresholds : dict, optional
        Per-category thresholds {category_name: threshold_value}
        Example: {'Strategic.M&A': 0.5, 'Operational.Project.Technical_Blockers': 0.35}

    default_threshold : float
        Default threshold for categories not in category_thresholds (default 0.5)

    multi_label : bool
        Whether to use multi-label mode

    Returns:
    --------
    results : dict
        Comprehensive evaluation metrics
    """

    # Initialize category_thresholds if not provided
    if category_thresholds is None:
        category_thresholds = {}

    # Build flat dict of all subcategories across all groups
    all_subcategories = {}
    for group_labels in label_groups.values():
        all_subcategories.update(group_labels)

    # Initialize tracking structures
    all_predictions = []
    per_category_stats = {label: {'tp': 0, 'fp': 0, 'fn': 0, 'tn': 0} for label in all_subcategories.keys()}
    confusion_pairs = defaultdict(int)

    start_time = time.time()

    print(f"Evaluating on {len(test_examples)} examples with parallel-group classification...")
    print(f"Label groups: {list(label_groups.keys())}")
    print(f"Total subcategories: {len(all_subcategories)}")
    print(f"Using per-category thresholds: {len(category_thresholds)} custom, default={default_threshold}")

    # Process each test example
    for idx, example in enumerate(test_examples):
        if idx % 10 == 0 and idx > 0:
            print(f"Processed {idx}/{len(test_examples)} examples...")

        text = example['text']
        true_labels = set(example['true_labels'])

        try:
            # Run all groups in parallel - no hierarchical gating
            predicted_subcategories = set()
            all_subcat_scores = {}

            for _, group_labels in label_groups.items():
                candidate_labels = list(group_labels.values())

                result = zero_shot_classify_fn(
                    text,
                    candidate_labels,
                    multi_label=multi_label
                )

                # Map descriptions back to category names and apply per-category threshold
                for label_desc, score in zip(result['labels'], result['scores']):
                    for cat_name, cat_desc in group_labels.items():
                        if cat_desc == label_desc:
                            all_subcat_scores[cat_name] = score
                            
                            # Use category-specific threshold if available, otherwise use default
                            threshold = category_thresholds.get(cat_name, default_threshold)
                            
                            if score >= threshold:
                                predicted_subcategories.add(cat_name)
                            break

            # Calculate correctness
            true_positives = predicted_subcategories & true_labels
            false_positives = predicted_subcategories - true_labels
            false_negatives = true_labels - predicted_subcategories

            # Update per-category statistics
            for label in all_subcategories.keys():
                if label in true_positives:
                    per_category_stats[label]['tp'] += 1
                if label in false_positives:
                    per_category_stats[label]['fp'] += 1
                if label in false_negatives:
                    per_category_stats[label]['fn'] += 1
                if label not in predicted_subcategories and label not in true_labels:
                    per_category_stats[label]['tn'] += 1

            # Track confusion pairs
            for fp_label in false_positives:
                for true_label in true_labels:
                    confusion_pairs[(fp_label, true_label)] += 1

            # Store detailed prediction
            prediction_record = {
                'example_id': idx,
                'text': text[:200] + '...' if len(text) > 200 else text,
                'true_labels': sorted(list(true_labels)),
                'predicted_labels': sorted(list(predicted_subcategories)),
                'all_scores': all_subcat_scores,
                'correct': (predicted_subcategories == true_labels),
                'true_positives': sorted(list(true_positives)),
                'false_positives': sorted(list(false_positives)),
                'false_negatives': sorted(list(false_negatives))
            }
            all_predictions.append(prediction_record)

        except Exception as e:
            print(f"Error processing example {idx}: {e}")
            all_predictions.append({
                'example_id': idx,
                'text': text,
                'error': str(e)
            })

    processing_time = time.time() - start_time

    print(f"\nProcessing complete! Time: {processing_time:.2f}s")
    print("Calculating metrics...\n")

    # Calculate overall metrics
    total_tp = sum(stats['tp'] for stats in per_category_stats.values())
    total_fp = sum(stats['fp'] for stats in per_category_stats.values())
    total_fn = sum(stats['fn'] for stats in per_category_stats.values())

    micro_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    micro_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    micro_f1 = 2 * micro_precision * micro_recall / (micro_precision + micro_recall) if (micro_precision + micro_recall) > 0 else 0

    # Calculate per-category metrics
    per_category_metrics = {}
    precisions = []
    recalls = []
    f1s = []

    for label, stats in per_category_stats.items():
        tp, fp, fn = stats['tp'], stats['fp'], stats['fn']

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        support = tp + fn

        per_category_metrics[label] = {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'support': support,
            'tp': tp,
            'fp': fp,
            'fn': fn,
            'threshold_used': category_thresholds.get(label, default_threshold)  # Track which threshold was used
        }

        if support > 0:
            precisions.append(precision)
            recalls.append(recall)
            f1s.append(f1)

    macro_precision = np.mean(precisions) if precisions else 0
    macro_recall = np.mean(recalls) if recalls else 0
    macro_f1 = np.mean(f1s) if f1s else 0

    # Calculate exact match accuracy
    exact_matches = sum(1 for pred in all_predictions if pred.get('correct', False))
    exact_match_accuracy = exact_matches / len(test_examples) if test_examples else 0

    # Calculate hamming loss
    hamming_losses = []
    for pred in all_predictions:
        if 'error' not in pred:
            total_labels = len(all_subcategories)
            errors = len(pred['false_positives']) + len(pred['false_negatives'])
            hamming_losses.append(errors / total_labels)
    hamming_loss = np.mean(hamming_losses) if hamming_losses else 0

    # Identify confusion patterns
    most_confused_pairs = sorted(confusion_pairs.items(), key=lambda x: x[1], reverse=True)[:10]

    # Identify frequent false positives and false negatives
    fp_counts = defaultdict(int)
    fn_counts = defaultdict(int)
    for pred in all_predictions:
        if 'error' not in pred:
            for fp in pred['false_positives']:
                fp_counts[fp] += 1
            for fn in pred['false_negatives']:
                fn_counts[fn] += 1

    frequent_false_positives = sorted(fp_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    frequent_false_negatives = sorted(fn_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    # Identify failed examples
    low_confidence_correct = []
    high_confidence_wrong = []
    missed_completely = []

    for pred in all_predictions:
        if 'error' in pred:
            continue

        max_score = max(pred['all_scores'].values()) if pred['all_scores'] else 0

        if pred['correct'] and max_score < 0.6:
            low_confidence_correct.append(pred)
        elif not pred['correct'] and max_score > 0.8:
            high_confidence_wrong.append(pred)
        elif len(pred['predicted_labels']) == 0 and len(pred['true_labels']) > 0:
            missed_completely.append(pred)

    # NOTE: Threshold analysis removed since we're using per-category thresholds
    # The global threshold sweep doesn't make sense anymore

    # Calculate summary statistics
    avg_true_labels = np.mean([len(pred['true_labels']) for pred in all_predictions if 'error' not in pred])
    avg_pred_labels = np.mean([len(pred['predicted_labels']) for pred in all_predictions if 'error' not in pred])
    zero_predictions = sum(1 for pred in all_predictions if 'error' not in pred and len(pred['predicted_labels']) == 0)
    perfect_matches = sum(1 for pred in all_predictions if pred.get('correct', False))

    # Categories never predicted
    never_predicted = [label for label, stats in per_category_stats.items() if stats['tp'] + stats['fp'] == 0]

    # Categories never in test set
    never_in_test = [label for label, stats in per_category_stats.items() if stats['tp'] + stats['fn'] == 0]

    # Build results dictionary
    results = {
        'overall_metrics': {
            'micro_precision': micro_precision,
            'micro_recall': micro_recall,
            'micro_f1': micro_f1,
            'macro_precision': macro_precision,
            'macro_recall': macro_recall,
            'macro_f1': macro_f1,
            'exact_match_accuracy': exact_match_accuracy,
            'hamming_loss': hamming_loss,
        },
        'per_category_metrics': per_category_metrics,
        'confusion_analysis': {
            'most_confused_pairs': most_confused_pairs,
            'frequent_false_positives': frequent_false_positives,
            'frequent_false_negatives': frequent_false_negatives
        },
        'predictions': all_predictions,
        'failed_examples': {
            'low_confidence_correct': low_confidence_correct[:5],
            'high_confidence_wrong': high_confidence_wrong[:5],
            'missed_completely': missed_completely[:5]
        },
        'category_thresholds_used': category_thresholds,
        'default_threshold': default_threshold,
        'summary_statistics': {
            'total_examples': len(test_examples),
            'avg_true_labels_per_example': avg_true_labels,
            'avg_predicted_labels_per_example': avg_pred_labels,
            'examples_with_zero_predictions': zero_predictions,
            'examples_with_perfect_match': perfect_matches,
            'categories_never_predicted': never_predicted,
            'categories_never_in_test_set': never_in_test,
            'processing_time_seconds': processing_time,
            'avg_time_per_example': processing_time / len(test_examples) if test_examples else 0
        }
    }

    return results


def print_evaluation_report(results: Dict[str, Any], top_n: int = 10):
    """
    Print a human-readable evaluation report.
    """

    print("=" * 80)
    print("PARALLEL-GROUP ZERO-SHOT CLASSIFIER EVALUATION REPORT")
    print("=" * 80)

    # Overall metrics
    print("\nOVERALL METRICS")
    print("-" * 80)
    om = results['overall_metrics']
    print(f"Micro Precision:              {om['micro_precision']:.3f}")
    print(f"Micro Recall:                 {om['micro_recall']:.3f}")
    print(f"Micro F1:                     {om['micro_f1']:.3f}")
    print(f"Macro Precision:              {om['macro_precision']:.3f}")
    print(f"Macro Recall:                 {om['macro_recall']:.3f}")
    print(f"Macro F1:                     {om['macro_f1']:.3f}")
    print(f"Exact Match Accuracy:         {om['exact_match_accuracy']:.3f}")
    print(f"Hamming Loss:                 {om['hamming_loss']:.3f}")

    # Threshold info
    print(f"\nTHRESHOLD CONFIGURATION")
    print("-" * 80)
    print(f"Default threshold: {results['default_threshold']}")
    print(f"Custom thresholds: {len(results['category_thresholds_used'])} categories")
    if results['category_thresholds_used']:
        print("Custom threshold categories:")
        for cat, thresh in sorted(results['category_thresholds_used'].items()):
            print(f"  {cat}: {thresh}")

    # Summary statistics
    print("\nSUMMARY STATISTICS")
    print("-" * 80)
    ss = results['summary_statistics']
    print(f"Total Examples:                    {ss['total_examples']}")
    print(f"Avg True Labels per Example:       {ss['avg_true_labels_per_example']:.2f}")
    print(f"Avg Predicted Labels per Example:  {ss['avg_predicted_labels_per_example']:.2f}")
    print(f"Examples with Zero Predictions:    {ss['examples_with_zero_predictions']}")
    print(f"Examples with Perfect Match:       {ss['examples_with_perfect_match']}")
    print(f"Processing Time:                   {ss['processing_time_seconds']:.2f}s")
    print(f"Avg Time per Example:              {ss['avg_time_per_example']:.3f}s")

    # Top performing categories
    print(f"\nTOP {top_n} PERFORMING CATEGORIES (by F1)")
    print("-" * 80)
    sorted_categories = sorted(
        results['per_category_metrics'].items(),
        key=lambda x: x[1]['f1'],
        reverse=True
    )

    print(f"{'Category':<50} {'F1':<8} {'Prec':<8} {'Rec':<8} {'Thresh':<8} {'Support':<8}")
    print("-" * 80)
    for cat, metrics in sorted_categories[:top_n]:
        if metrics['support'] > 0:
            print(f"{cat:<50} {metrics['f1']:.3f}    {metrics['precision']:.3f}    {metrics['recall']:.3f}    {metrics['threshold_used']:.2f}     {metrics['support']:<8}")

    # Bottom performing categories
    print(f"\nBOTTOM {top_n} PERFORMING CATEGORIES (by F1)")
    print("-" * 80)
    print(f"{'Category':<50} {'F1':<8} {'Prec':<8} {'Rec':<8} {'Thresh':<8} {'Support':<8}")
    print("-" * 80)
    bottom_categories = [x for x in reversed(sorted_categories) if x[1]['support'] > 0][:top_n]
    for cat, metrics in bottom_categories:
        print(f"{cat:<50} {metrics['f1']:.3f}    {metrics['precision']:.3f}    {metrics['recall']:.3f}    {metrics['threshold_used']:.2f}     {metrics['support']:<8}")

    # Categories never predicted
    if ss['categories_never_predicted']:
        print(f"\nCATEGORIES NEVER PREDICTED")
        print("-" * 80)
        for cat in ss['categories_never_predicted'][:10]:
            print(f"  - {cat}")

    # Confusion analysis
    print(f"\nMOST CONFUSED CATEGORY PAIRS")
    print("-" * 80)
    print(f"{'Predicted':<40} {'Should Be':<40} {'Count':<8}")
    print("-" * 80)
    for (pred_cat, true_cat), count in results['confusion_analysis']['most_confused_pairs'][:5]:
        print(f"{pred_cat:<40} {true_cat:<40} {count:<8}")

    # Frequent false positives
    print(f"\nMOST FREQUENT FALSE POSITIVES")
    print("-" * 80)
    for cat, count in results['confusion_analysis']['frequent_false_positives'][:5]:
        print(f"  {cat:<50} ({count} times)")

    # Frequent false negatives
    print(f"\nMOST FREQUENT FALSE NEGATIVES (Missed)")
    print("-" * 80)
    for cat, count in results['confusion_analysis']['frequent_false_negatives'][:5]:
        print(f"  {cat:<50} ({count} times)")

    print("\n" + "=" * 80)


def export_results_to_csv(results: Dict[str, Any], output_prefix: str = "zero_shot_eval"):
    """Export evaluation results to CSV files."""

    per_cat_df = pd.DataFrame(results['per_category_metrics']).T
    per_cat_df.to_csv(f"{output_prefix}_per_category_metrics.csv")
    print(f"Saved per-category metrics to {output_prefix}_per_category_metrics.csv")

    predictions_df = pd.DataFrame(results['predictions'])
    predictions_df.to_csv(f"{output_prefix}_predictions.csv", index=False)
    print(f"Saved predictions to {output_prefix}_predictions.csv")


# ===== RUN EVALUATION =====
results = evaluate_zero_shot_classifier_parallel(
    test_examples=zero_shot_test_examples,
    label_groups=ZERO_SHOT_LABEL_GROUPS,
    zero_shot_classify_fn=zero_shot_classify,
    category_thresholds=CATEGORY_THRESHOLDS,
    default_threshold=0.5,
    multi_label=True
)

# Print report
print_evaluation_report(results, top_n=24)