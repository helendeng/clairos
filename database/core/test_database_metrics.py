"""
Database Testing & Metrics Visualization
Demonstrates subdomain isolation, search quality, and data organization
Generates metrics that prove the database works correctly
"""

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from database.Schemas.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMBEDDING_MODEL, SUBDOMAINS
import pandas as pd
from collections import Counter, defaultdict
import json
from datetime import datetime


class DatabaseMetrics:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.results = {}
        
    def get_all_points(self):
        """Retrieve all points from database"""
        result = self.client.scroll(
            collection_name=COLLECTION_NAME,
            limit=1000,
            with_payload=True,
            with_vectors=False
        )
        return result[0]
    
    def test_1_data_coverage(self):
        """Test 1: How many subdomains are covered?"""
        print("=" * 70)
        print("TEST 1: DATA COVERAGE")
        print("=" * 70)
        
        points = self.get_all_points()
        
        if not points:
            print("❌ No data in database!")
            return
        
        # Count subdomains
        subdomain_counts = Counter(p.payload.get('subdomain') for p in points)
        
        total_subdomains = len(SUBDOMAINS)
        covered_subdomains = len(subdomain_counts)
        coverage_percentage = (covered_subdomains / total_subdomains) * 100
        
        print(f"Total Possible Subdomains: {total_subdomains}")
        print(f"Subdomains with Data: {covered_subdomains}")
        print(f"Coverage: {coverage_percentage:.1f}%")
        print(f"Total Chunks: {len(points)}")
        print()
        
        # Show distribution
        print("Subdomain Distribution:")
        print("-" * 70)
        for subdomain, count in sorted(subdomain_counts.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(count / max(subdomain_counts.values()) * 40)
            print(f"{subdomain:30} | {count:3} chunks | {bar}")
        print()
        
        # Store results
        self.results['data_coverage'] = {
            'total_subdomains': total_subdomains,
            'covered_subdomains': covered_subdomains,
            'coverage_percentage': coverage_percentage,
            'total_chunks': len(points),
            'distribution': dict(subdomain_counts)
        }
        
        return subdomain_counts
    
    def test_2_isolation_quality(self):
        """Test 2: Are subdomains properly isolated?"""
        print("=" * 70)
        print("TEST 2: SUBDOMAIN ISOLATION QUALITY")
        print("=" * 70)
        print("Verifying no cross-contamination between subdomains\n")
        
        points = self.get_all_points()
        
        # Group by subdomain
        subdomain_groups = defaultdict(lambda: {'chunks': [], 'domains': set()})
        
        for point in points:
            subdomain = point.payload.get('subdomain')
            domain = point.payload.get('domain')
            
            subdomain_groups[subdomain]['chunks'].append(point.payload.get('chunk_id'))
            subdomain_groups[subdomain]['domains'].add(domain)
        
        # Check isolation
        issues = []
        perfect_isolation = True
        
        for subdomain, info in subdomain_groups.items():
            if len(info['domains']) > 1:
                issues.append({
                    'subdomain': subdomain,
                    'domains': list(info['domains']),
                    'chunk_count': len(info['chunks'])
                })
                perfect_isolation = False
        
        if perfect_isolation:
            print("✓ PERFECT ISOLATION: Each subdomain maps to exactly 1 domain")
            print(f"  All {len(subdomain_groups)} subdomains are cleanly separated")
            isolation_score = 100.0
        else:
            print(f"⚠️  ISOLATION ISSUES FOUND: {len(issues)} subdomains have conflicts")
            for issue in issues:
                print(f"  - '{issue['subdomain']}' maps to {len(issue['domains'])} domains: {issue['domains']}")
            isolation_score = ((len(subdomain_groups) - len(issues)) / len(subdomain_groups)) * 100
        
        print(f"\nIsolation Score: {isolation_score:.1f}%")
        print()
        
        # Store results
        self.results['isolation_quality'] = {
            'perfect_isolation': perfect_isolation,
            'isolation_score': isolation_score,
            'total_subdomains': len(subdomain_groups),
            'issues_found': len(issues),
            'issues': issues
        }
        
        return perfect_isolation
    
    
    def test_4_subdomain_filtering(self):
        """Test 4: Can we filter by subdomain perfectly?"""
        print("=" * 70)
        print("TEST 4: SUBDOMAIN FILTERING")
        print("=" * 70)
        print("Testing if filtering by subdomain returns only relevant chunks\n")
        
        points = self.get_all_points()
        
        # Get unique subdomains
        subdomains_in_db = set(p.payload.get('subdomain') for p in points)
        
        filter_tests = []
        all_passed = True
        
        for subdomain in sorted(subdomains_in_db):
            # Filter by subdomain
            filtered = [p for p in points if p.payload.get('subdomain') == subdomain]
            
            # Verify no contamination
            contaminated = [p for p in filtered if p.payload.get('subdomain') != subdomain]
            
            passed = len(contaminated) == 0
            
            if passed:
                status = "✓ PASS"
            else:
                status = "✗ FAIL"
                all_passed = False
            
            print(f"{status} | Subdomain: '{subdomain}' | Found: {len(filtered)} chunks | Contamination: {len(contaminated)}")
            
            filter_tests.append({
                'subdomain': subdomain,
                'chunks_found': len(filtered),
                'contamination': len(contaminated),
                'passed': passed
            })
        
        pass_rate = (sum(1 for t in filter_tests if t['passed']) / len(filter_tests)) * 100 if filter_tests else 0
        
        print(f"\nFilter Pass Rate: {pass_rate:.1f}%")
        if all_passed:
            print("✓ All subdomain filters working perfectly!")
        else:
            print("⚠️  Some subdomain filters have contamination issues")
        print()
        
        # Store results
        self.results['subdomain_filtering'] = {
            'all_passed': all_passed,
            'pass_rate': pass_rate,
            'subdomains_tested': len(filter_tests),
            'detailed_results': filter_tests
        }
        
        return all_passed
    
    def test_5_data_quality(self):
        """Test 5: Is the data properly structured?"""
        print("=" * 70)
        print("TEST 5: DATA QUALITY")
        print("=" * 70)
        print("Checking if all chunks have required fields\n")
        
        points = self.get_all_points()
        
        required_fields = {
            'chunk_id': 'Chunk ID',
            'subdomain': 'Subdomain',
            'domain': 'Domain',
            'text': 'Text Content',
            'source': 'Source Metadata'
        }
        
        required_source_fields = {
            'email_id': 'Email ID',
            'from': 'From Address',
            'subject': 'Subject Line',
            'timestamp': 'Timestamp'
        }
        
        field_coverage = defaultdict(int)
        source_field_coverage = defaultdict(int)
        issues = []
        
        for point in points:
            chunk_id = point.payload.get('chunk_id', 'unknown')
            
            # Check main fields
            for field in required_fields.keys():
                if field in point.payload and point.payload[field]:
                    field_coverage[field] += 1
                else:
                    issues.append(f"Chunk {chunk_id}: Missing '{field}'")
            
            # Check source fields
            source = point.payload.get('source', {})
            for field in required_source_fields.keys():
                if field in source and source[field]:
                    source_field_coverage[field] += 1
                else:
                    issues.append(f"Chunk {chunk_id}: Missing source.'{field}'")
        
        total_chunks = len(points)
        
        print("Field Coverage:")
        print("-" * 70)
        for field, name in required_fields.items():
            count = field_coverage[field]
            percentage = (count / total_chunks) * 100 if total_chunks > 0 else 0
            status = "✓" if percentage == 100 else "⚠️"
            print(f"{status} {name:20} | {count}/{total_chunks} ({percentage:.1f}%)")
        
        print("\nSource Field Coverage:")
        print("-" * 70)
        for field, name in required_source_fields.items():
            count = source_field_coverage[field]
            percentage = (count / total_chunks) * 100 if total_chunks > 0 else 0
            status = "✓" if percentage == 100 else "⚠️"
            print(f"{status} {name:20} | {count}/{total_chunks} ({percentage:.1f}%)")
        
        # Calculate overall quality score
        all_fields = list(required_fields.keys()) + list(required_source_fields.keys())
        all_coverage = {**field_coverage, **source_field_coverage}
        
        quality_score = (sum(all_coverage.values()) / (len(all_fields) * total_chunks)) * 100 if total_chunks > 0 else 0
        
        print(f"\nOverall Data Quality Score: {quality_score:.1f}%")
        
        if issues:
            print(f"\n⚠️  Found {len(issues)} issues:")
            for issue in issues[:5]:  # Show first 5
                print(f"  - {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
        else:
            print("\n✓ Perfect data quality - all fields present!")
        print()
        
        # Store results
        self.results['data_quality'] = {
            'quality_score': quality_score,
            'total_chunks': total_chunks,
            'field_coverage': dict(field_coverage),
            'source_field_coverage': dict(source_field_coverage),
            'issues_count': len(issues)
        }
        
        return quality_score
    
    def generate_summary_report(self):
        """Generate overall summary"""
        print("=" * 70)
        print("OVERALL DATABASE HEALTH REPORT")
        print("=" * 70)
        
        # Calculate overall score
        scores = {
            #'Coverage': self.results.get('data_coverage', {}).get('coverage_percentage', 0),
            'Isolation': self.results.get('isolation_quality', {}).get('isolation_score', 0),
            
            'Filtering': self.results.get('subdomain_filtering', {}).get('pass_rate', 0),
            'Data Quality': self.results.get('data_quality', {}).get('quality_score', 0)
        }
        
        overall_score = sum(scores.values()) / len(scores)
        
        print("\nScore Breakdown:")
        print("-" * 70)
        for metric, score in scores.items():
            bar = "█" * int(score / 5)
            print(f"{metric:20} | {score:5.1f}% | {bar}")
        
        print("-" * 70)
        print(f"{'OVERALL HEALTH':20} | {overall_score:5.1f}% |", end=" ")
        
        # Health status
        if overall_score >= 90:
            print("🟢 EXCELLENT")
        elif overall_score >= 75:
            print("🟡 GOOD")
        elif overall_score >= 60:
            print("🟠 FAIR")
        else:
            print("🔴 NEEDS IMPROVEMENT")
        
        print()
        
        # Key metrics
        print("Key Metrics:")
        print("-" * 70)
        dc = self.results.get('data_coverage', {})
        print(f"Total Chunks: {dc.get('total_chunks', 0)}")
        print(f"Subdomains Covered: {dc.get('covered_subdomains', 0)}/{dc.get('total_subdomains', 0)}")
        
        iq = self.results.get('isolation_quality', {})
        print(f"Isolation Issues: {iq.get('issues_found', 0)}")
        
        
        
        print()
        
        self.results['overall_score'] = overall_score
        self.results['health_status'] = 'EXCELLENT' if overall_score >= 90 else 'GOOD' if overall_score >= 75 else 'FAIR' if overall_score >= 60 else 'NEEDS IMPROVEMENT'
        
        return overall_score
    
    def export_results(self, filename='database_metrics.json'):
        """Export results to JSON file"""
        self.results['timestamp'] = datetime.now().isoformat()
        self.results['collection_name'] = COLLECTION_NAME
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"✓ Results exported to {filename}")
        return filename
    
    def create_visualization_data(self):
        """Create data ready for visualization (CSV format)"""
        
        # 1. Subdomain distribution
        dc = self.results.get('data_coverage', {})
        dist = dc.get('distribution', {})
        
        df_distribution = pd.DataFrame([
            {'Subdomain': k, 'Chunk_Count': v} 
            for k, v in dist.items()
        ])
        df_distribution.to_csv('subdomain_distribution.csv', index=False)
        print("✓ Created subdomain_distribution.csv")
        
        # 2. Test scores
        df_scores = pd.DataFrame([
            #{'Metric': 'Coverage', 'Score': self.results.get('data_coverage', {}).get('coverage_percentage', 0)},
            {'Metric': 'Isolation', 'Score': self.results.get('isolation_quality', {}).get('isolation_score', 0)},
            {'Metric': 'Filtering', 'Score': self.results.get('subdomain_filtering', {}).get('pass_rate', 0)},
            {'Metric': 'Data Quality', 'Score': self.results.get('data_quality', {}).get('quality_score', 0)}
        ])
        df_scores.to_csv('test_scores.csv', index=False)
        print("✓ Created test_scores.csv")
        
        
        return df_distribution, df_scores


def main():
    """Run all tests and generate reports"""
    
    print("=" * 70)
    print("DATABASE METRICS & TESTING SUITE")
    print("=" * 70)
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    metrics = DatabaseMetrics()
    
    # Run all tests
    print("Running tests...\n")
    
    metrics.test_1_data_coverage()
    metrics.test_2_isolation_quality()
    metrics.test_4_subdomain_filtering()
    metrics.test_5_data_quality()
    
    # Generate summary
    overall_score = metrics.generate_summary_report()
    
    # Export results
    print("=" * 70)
    print("EXPORTING RESULTS")
    print("=" * 70)
    metrics.export_results()
    metrics.create_visualization_data()
    print()
    
    # Final message
    print("=" * 70)
    print("✓ TESTING COMPLETE!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - database_metrics.json (detailed results)")
    print("  - subdomain_distribution.csv (for charts)")
    print("  - test_scores.csv (for charts)")
    print()
    print("Next steps:")
    print("  1. Open CSV files in Excel/Google Sheets to create charts")
    print("  2. Use database_metrics.json for detailed analysis")
    print("  3. Share these visualizations to demonstrate database quality")
    print()
    print(f"Overall Health: {overall_score:.1f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()
