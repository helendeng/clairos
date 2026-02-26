"""
Create visual charts from database metrics
Generates PNG images showing database performance
"""

import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime
import os


def create_charts():
    """Generate all visualization charts"""
    
    print("=" * 70)
    print("GENERATING VISUALIZATIONS")
    print("=" * 70)
    print()
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Check if files exist
    required_files = ['subdomain_distribution.csv', 'test_scores.csv', 'database_metrics.json']
    missing = [f for f in required_files if not os.path.exists(f)]
    
    if missing:
        print(f"❌ Missing files: {missing}")
        print("   Please run test_database_metrics.py first!")
        return
    
    # 1. Subdomain Distribution Bar Chart
    print("Creating subdomain distribution chart...")
    df_dist = pd.read_csv('subdomain_distribution.csv')
    
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(df_dist)), df_dist['Chunk_Count'], color='steelblue', edgecolor='black')
    plt.xlabel('Subdomain', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Chunks', fontsize=12, fontweight='bold')
    plt.title('Subdomain Distribution', fontsize=14, fontweight='bold')
    plt.xticks(range(len(df_dist)), df_dist['Subdomain'], rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('subdomain_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved subdomain_distribution.png")
    
    # 2. Test Scores Horizontal Bar Chart
    print("Creating test scores chart...")
    df_scores = pd.read_csv('test_scores.csv')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = []
    for score in df_scores['Score']:
        if score >= 90:
            colors.append('#2ecc71')  # Green
        elif score >= 75:
            colors.append('#f39c12')  # Orange
        elif score >= 60:
            colors.append('#e67e22')  # Dark orange
        else:
            colors.append('#e74c3c')  # Red
    
    bars = ax.barh(df_scores['Metric'], df_scores['Score'], color=colors, edgecolor='black')
    ax.set_xlabel('Score (%)', fontsize=12, fontweight='bold')
    ax.set_title('Database Test Scores', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 100)
    
    # Add value labels
    for i, (bar, score) in enumerate(zip(bars, df_scores['Score'])):
        ax.text(score + 2, i, f'{score:.1f}%', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('test_scores.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved test_scores.png")
    
    # 3. Overall Health Gauge
    print("Creating overall health gauge...")
    with open('database_metrics.json', 'r') as f:
        metrics = json.load(f)
    
    overall_score = metrics.get('overall_score', 0)
    health_status = metrics.get('health_status', 'UNKNOWN')
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create gauge chart
    categories = ['0-60\nNeeds\nImprovement', '60-75\nFair', '75-90\nGood', '90-100\nExcellent']
    colors_gauge = ['#e74c3c', '#e67e22', '#f39c12', '#2ecc71']
    values = [60, 15, 15, 10]
    
    wedges, texts = ax.pie(values, colors=colors_gauge, startangle=180, counterclock=False)
    
    # Add center circle for donut effect
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Add score text
    ax.text(0, 0, f'{overall_score:.1f}%', ha='center', va='center', fontsize=36, fontweight='bold')
    ax.text(0, -0.25, health_status, ha='center', va='center', fontsize=14, fontweight='bold')
    
    ax.set_title('Overall Database Health', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('overall_health.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved overall_health.png")
    
    # 4. Search Accuracy Results (if available)
    if os.path.exists('search_results.csv'):
        print("Creating search accuracy chart...")
        df_search = pd.read_csv('search_results.csv')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(len(df_search))
        ax.bar(x, df_search['avg_relevance'], color='teal', edgecolor='black', alpha=0.7, label='Relevance')
        ax2 = ax.twinx()
        ax2.plot(x, df_search['top_score'] * 100, color='coral', marker='o', linewidth=2, markersize=8, label='Similarity Score')
        
        ax.set_xlabel('Query', fontsize=12, fontweight='bold')
        ax.set_ylabel('Relevance (%)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Similarity Score', fontsize=12, fontweight='bold')
        ax.set_title('Search Accuracy by Query', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(df_search['description'], rotation=45, ha='right')
        
        # Add legends
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.tight_layout()
        plt.savefig('search_accuracy.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Saved search_accuracy.png")
    
    # 5. Create summary dashboard
    print("Creating summary dashboard...")
    create_summary_dashboard(metrics, df_scores)
    
    print()
    print("=" * 70)
    print("✓ ALL VISUALIZATIONS CREATED!")
    print("=" * 70)
    print("\nGenerated images:")
    print("  - subdomain_distribution.png")
    print("  - test_scores.png")
    print("  - overall_health.png")
    print("  - search_accuracy.png")
    print("  - summary_dashboard.png")
    print()


def create_summary_dashboard(metrics, df_scores):
    """Create a single dashboard image with all key metrics"""
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Title
    fig.suptitle('DATABASE PERFORMANCE DASHBOARD', fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Overall Score (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    overall_score = metrics.get('overall_score', 0)
    health_status = metrics.get('health_status', 'UNKNOWN')
    
    if overall_score >= 90:
        color = '#2ecc71'
    elif overall_score >= 75:
        color = '#f39c12'
    elif overall_score >= 60:
        color = '#e67e22'
    else:
        color = '#e74c3c'
    
    ax1.text(0.5, 0.6, f'{overall_score:.1f}%', ha='center', va='center', 
             fontsize=48, fontweight='bold', color=color)
    ax1.text(0.5, 0.3, health_status, ha='center', va='center', 
             fontsize=14, fontweight='bold')
    ax1.text(0.5, 0.95, 'Overall Health', ha='center', va='top', 
             fontsize=12, fontweight='bold')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    
    # 2. Key Metrics (top middle)
    ax2 = fig.add_subplot(gs[0, 1])
    dc = metrics.get('data_coverage', {})
    iq = metrics.get('isolation_quality', {})
    dq = metrics.get('data_quality', {})
    
    metrics_text = f"""
    Total Chunks: {dc.get('total_chunks', 0)}
    Subdomains: {dc.get('covered_subdomains', 0)}/{dc.get('total_subdomains', 0)}
    Coverage: {dc.get('coverage_percentage', 0):.1f}%
    Isolation: {'Perfect' if iq.get('perfect_isolation', False) else 'Has Issues'}
    Data Quality: {dq.get('quality_score', 0):.1f}%
    """
    
    ax2.text(0.1, 0.5, metrics_text, ha='left', va='center', fontsize=11, family='monospace')
    ax2.text(0.5, 0.95, 'Key Metrics', ha='center', va='top', fontsize=12, fontweight='bold')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    
    # 3. Timestamp (top right)
    ax3 = fig.add_subplot(gs[0, 2])
    timestamp = metrics.get('timestamp', datetime.now().isoformat())
    collection = metrics.get('collection_name', 'Unknown')
    
    info_text = f"""
    Collection: {collection}
    
    Generated: {timestamp[:10]}
    Time: {timestamp[11:19]}
    """
    
    ax3.text(0.1, 0.5, info_text, ha='left', va='center', fontsize=11, family='monospace')
    ax3.text(0.5, 0.95, 'Info', ha='center', va='top', fontsize=12, fontweight='bold')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    
    # 4. Test Scores (middle row, full width)
    ax4 = fig.add_subplot(gs[1, :])
    
    colors = ['#2ecc71' if s >= 90 else '#f39c12' if s >= 75 else '#e67e22' if s >= 60 else '#e74c3c' 
              for s in df_scores['Score']]
    
    bars = ax4.barh(df_scores['Metric'], df_scores['Score'], color=colors, edgecolor='black', height=0.6)
    ax4.set_xlabel('Score (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Test Scores Breakdown', fontsize=14, fontweight='bold', pad=10)
    ax4.set_xlim(0, 100)
    ax4.grid(axis='x', alpha=0.3)
    
    for i, (bar, score) in enumerate(zip(bars, df_scores['Score'])):
        ax4.text(score + 2, i, f'{score:.1f}%', va='center', fontweight='bold', fontsize=10)
    
    # 5. Subdomain Distribution (bottom row)
    ax5 = fig.add_subplot(gs[2, :])
    
    if os.path.exists('subdomain_distribution.csv'):
        df_dist = pd.read_csv('subdomain_distribution.csv')
        
        # Show top 10 subdomains
        df_top = df_dist.nlargest(10, 'Chunk_Count')
        
        bars = ax5.bar(range(len(df_top)), df_top['Chunk_Count'], color='steelblue', edgecolor='black')
        ax5.set_xlabel('Subdomain', fontsize=12, fontweight='bold')
        ax5.set_ylabel('Chunks', fontsize=12, fontweight='bold')
        ax5.set_title('Top 10 Subdomains by Chunk Count', fontsize=14, fontweight='bold', pad=10)
        ax5.set_xticks(range(len(df_top)))
        ax5.set_xticklabels(df_top['Subdomain'], rotation=45, ha='right', fontsize=9)
        ax5.grid(axis='y', alpha=0.3)
        
        for i, (bar, count) in enumerate(zip(bars, df_top['Chunk_Count'])):
            ax5.text(i, count + 0.5, str(count), ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.savefig('summary_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved summary_dashboard.png")


def main():
    """Generate all visualizations"""
    create_charts()


if __name__ == "__main__":
    main()
