"""
GPT Usage Analyzer - Self-Contained Version for GPT Code Interpreter
Paste this entire script into the GPT's Code Interpreter or save as analyze_gpt_data.py
"""

import pandas as pd
import json
from datetime import datetime
from collections import defaultdict
import re

# ============================================================================
# CONFIGURATION - Modify these rules as needed
# ============================================================================

EXCLUSION_PATTERNS = [
    'smart pack', 'smartpack', 'smart-pack',
    'candidate letter generator', 
    'psychometric report generator', 
    'psychometric report writing',
    'consultant finder',
    'candidate archetype',
    'prompt coach',
    'psychometric stylist',
    'executive assessment advisor'
]

# Category definitions with keywords and descriptions
CATEGORY_DEFINITIONS = {
    'Writing & Communications': {
        'description': 'Email drafting, content creation, copywriting, translation, and document polishing',
        'keywords': [
            'email', 'polish', 'write', 'writing', 'draft', 'translate', 'translation',
            'compose', 'copy', 'content', 'communications', 'comms', 'ghost writer',
            'speech', 'linkedin', 'social', 'post', 'marketing', 'promotional',
            'promo', 'newsletter', 'article', 'blog', 'editor', 'proofread'
        ],
        'indicators': ['email', 'polish', 'write', 'content', 'copy', 'draft']
    },
    'Research & Intelligence': {
        'description': 'Company research, executive profiling, industry analysis, and intelligence gathering',
        'keywords': [
            'research', 'intelligence', 'intel', 'company', 'profile', 'web digger',
            'search', 'strategy', 'target', 'deck builder', 'asset deck', 'industry',
            'trend', 'analysis', 'analyze', 'data extraction', 'investor', 'credentials',
            'creds', 'logos', 'finder', 'digger'
        ],
        'indicators': ['research', 'company', 'profile', 'finder', 'digger', 'intel']
    },
    'Meeting Notes & Summarization': {
        'description': 'Meeting transcript processing, note-taking, and action item extraction',
        'keywords': [
            'meeting', 'notes', 'summar', 'transcript', 'brief', 'briefing', 'agenda',
            'minutes', 'recap', 'call notes', 'interview notes', 'status', 'update',
            'weekly', 'daily report', 'transcription'
        ],
        'indicators': ['meeting', 'notes', 'transcript', 'brief', 'status', 'update']
    },
    'Leadership & Talent Advisory': {
        'description': 'Executive coaching, organization design, succession planning, and talent strategy',
        'keywords': [
            'leadership', 'coach', 'coaching', 'development', 'talent', 'succession',
            'governance', 'advisor', 'advisory', 'role design', 'organization',
            'potential', 'capstone', 'span', 'versatility', 'growth', 'marshall'
        ],
        'indicators': ['leadership', 'coach', 'talent', 'succession', 'development']
    },
    'Assessment & Reporting': {
        'description': 'Candidate assessments, reference checks, and evaluation report writing',
        'keywords': [
            'assessment', 'evaluation', 'appraisal', 'review', 'feedback', '360',
            'reference', 'candidate report', 'report writer', 'hogan', 'caliper',
            'opq', 'psychometric', 'assess ', 'evaluat'
        ],
        'indicators': ['assessment', 'appraisal', 'review', 'feedback', 'reference', 'report']
    },
    'Productivity & Automation': {
        'description': 'Workflow automation, data processing, coding assistance, and admin tasks',
        'keywords': [
            'automat', 'schedule', 'calendar', 'invoice', 'process', 'extract',
            'coding', 'data tool', 'powershell', 'python', 'excel', 'csv', 'tracker',
            'organize', 'log', 'assistant', 'classifier', 'variance', 'analysis tool'
        ],
        'indicators': ['automat', 'process', 'extract', 'coding', 'data', 'tracker']
    },
    'Testing & Training': {
        'description': 'Test environments, training tools, and onboarding assistance',
        'keywords': [
            'test', 'training', 'practice', 'exercise', 'study', 'learn', 'tutorial',
            'onboarding', 'study mode', 'coach', 'helper'
        ],
        'indicators': ['test', 'training', 'study', 'learn', 'practice']
    },
    'Other / Uncategorized': {
        'description': 'GPTs with unclear function or specialized use cases',
        'keywords': [],
        'indicators': []
    }
}


# ============================================================================
# CORE ANALYSIS FUNCTIONS
# ============================================================================

def should_exclude(gpt_name: str) -> dict:
    """
    Check if GPT should be excluded and return reason.
    Returns: {'excluded': bool, 'reason': str}
    """
    name_lower = gpt_name.lower()
    
    # Check exact patterns
    for pattern in EXCLUSION_PATTERNS:
        if pattern in name_lower:
            return {'excluded': True, 'reason': f'Matches exclusion pattern: {pattern}'}
    
    # Check for smart pack variants
    if ('person' in name_lower or 'company' in name_lower) and 'smart' in name_lower:
        return {'excluded': True, 'reason': 'Smart Pack variant'}
    
    # Check for candidate letter variants (not already caught)
    if 'candidate letter' in name_lower:
        return {'excluded': True, 'reason': 'Candidate Letter variant'}
    
    return {'excluded': False, 'reason': None}


def calculate_category_scores(name: str, description: str) -> dict:
    """
    Calculate match scores for each category.
    Returns dict of {category_name: score}
    """
    name_lower = name.lower()
    desc_lower = description.lower() if description else ""
    
    scores = defaultdict(int)
    
    for category, rules in CATEGORY_DEFINITIONS.items():
        if category == 'Other / Uncategorized':
            continue
            
        # Check description (weighted 2x)
        for keyword in rules['keywords']:
            if keyword in desc_lower:
                scores[category] += 2
        
        # Check name (weighted 1x)
        for keyword in rules['keywords']:
            if keyword in name_lower:
                scores[category] += 1
    
    return dict(scores)


def categorize_gpt(name: str, description: str) -> dict:
    """
    Categorize a single GPT and return detailed result.
    """
    # Calculate scores
    scores = calculate_category_scores(name, description)
    
    # Determine best category
    if scores and max(scores.values()) > 0:
        best_category = max(scores, key=scores.get)
        confidence = 'high' if scores[best_category] >= 3 else 'medium'
    else:
        # Fall back to name-based heuristics
        best_category = fallback_categorization(name, description)
        confidence = 'low'
        scores = {best_category: 1}
    
    return {
        'category': best_category,
        'confidence': confidence,
        'scores': scores,
        'name': name,
        'description_preview': description[:150] if description else None
    }


def fallback_categorization(name: str, description: str) -> str:
    """
    Fallback rules when keyword matching fails.
    """
    name_lower = name.lower()
    desc_lower = description.lower() if description else ""
    
    # Name-based fallbacks
    if 'email' in name_lower:
        return 'Writing & Communications'
    if 'notes' in name_lower or 'transcript' in name_lower:
        return 'Meeting Notes & Summarization'
    if 'research' in name_lower or 'digger' in name_lower or 'finder' in name_lower:
        return 'Research & Intelligence'
    if 'assessment' in name_lower or 'appraisal' in name_lower:
        return 'Assessment & Reporting'
    if 'coach' in name_lower and 'leadership' in desc_lower:
        return 'Leadership & Talent Advisory'
    if 'test' in name_lower or 'training' in name_lower:
        return 'Testing & Training'
    if 'automat' in name_lower or 'process' in name_lower:
        return 'Productivity & Automation'
    
    return 'Other / Uncategorized'


# ============================================================================
# MAIN ANALYSIS PIPELINE
# ============================================================================

def analyze_gpt_data(file_path: str, period: str = None) -> dict:
    """
    Main analysis function.
    
    Args:
        file_path: Path to Excel file
        period: Optional period label (e.g., "December 2025")
    
    Returns:
        Complete analysis results as dictionary
    """
    
    # Read data
    try:
        df = pd.read_excel(file_path, sheet_name='GPTData')
    except ValueError:
        df = pd.read_excel(file_path)  # Fall back to first sheet
    
    # Clean data
    df = df[df['gpt_name'] != 'gpt_name'].copy()
    df = df[df['gpt_name'].notna()].copy()
    
    # Convert numeric columns
    df['messages_workspace'] = pd.to_numeric(df['messages_workspace'], errors='coerce').fillna(0)
    df['unique_messagers_workspace'] = pd.to_numeric(df['unique_messagers_workspace'], errors='coerce').fillna(0)
    
    # Filter to live only
    df = df[df['config_type'] == 'live'].copy() if 'config_type' in df.columns else df
    
    # Apply exclusions
    df['exclusion_info'] = df['gpt_name'].apply(should_exclude)
    df['is_excluded'] = df['exclusion_info'].apply(lambda x: x['excluded'])
    df['exclusion_reason'] = df['exclusion_info'].apply(lambda x: x['reason'])
    
    # Split data
    df_excluded = df[df['is_excluded'] == True].copy()
    df_included = df[df['is_excluded'] == False].copy()
    
    # Categorize included GPTs
    categorization_results = []
    for _, row in df_included.iterrows():
        result = categorize_gpt(row['gpt_name'], row.get('gpt_description'))
        result['messages'] = int(row['messages_workspace'])
        result['users'] = int(row['unique_messagers_workspace'])
        result['creator'] = row.get('gpt_creator_email', 'Unknown')
        categorization_results.append(result)
    
    # Add category to dataframe
    category_map = {r['name']: r['category'] for r in categorization_results}
    confidence_map = {r['name']: r['confidence'] for r in categorization_results}
    df_included['category'] = df_included['gpt_name'].map(category_map)
    df_included['confidence'] = df_included['gpt_name'].map(confidence_map)
    
    # Calculate statistics
    total_included_gpts = len(df_included)
    total_included_messages = int(df_included['messages_workspace'].sum())
    total_included_users = int(df_included['unique_messagers_workspace'].sum())
    
    # Category breakdown
    category_stats = df_included.groupby('category').agg({
        'gpt_name': 'count',
        'messages_workspace': 'sum',
        'unique_messagers_workspace': 'sum'
    }).reset_index()
    category_stats.columns = ['category', 'gpt_count', 'total_messages', 'total_users']
    category_stats['percentage'] = (category_stats['total_messages'] / total_included_messages * 100).round(1)
    category_stats = category_stats.sort_values('total_messages', ascending=False)
    
    # Top GPTs per category
    top_by_category = {}
    for cat in category_stats['category']:
        cat_gpts = df_included[df_included['category'] == cat].nlargest(5, 'messages_workspace')
        top_by_category[cat] = [
            {
                'name': row['gpt_name'],
                'messages': int(row['messages_workspace']),
                'users': int(row['unique_messagers_workspace']),
                'confidence': row.get('confidence', 'unknown'),
                'description': str(row['gpt_description'])[:100] if pd.notna(row['gpt_description']) else None
            }
            for _, row in cat_gpts.iterrows()
        ]
    
    # Confidence distribution
    confidence_dist = df_included['confidence'].value_counts().to_dict()
    
    # Build result
    result = {
        'metadata': {
            'period': period or 'Unknown',
            'analysis_date': datetime.now().isoformat(),
            'file_processed': file_path,
            'total_live_gpts': len(df),
            'excluded_gpts': len(df_excluded),
            'included_gpts': len(df_included)
        },
        'exclusions': {
            'count': len(df_excluded),
            'total_messages': int(df_excluded['messages_workspace'].sum()),
            'top_excluded': [
                {
                    'name': row['gpt_name'],
                    'messages': int(row['messages_workspace']),
                    'reason': row['exclusion_reason']
                }
                for _, row in df_excluded.nlargest(5, 'messages_workspace').iterrows()
            ]
        },
        'summary': {
            'total_gpts_analyzed': total_included_gpts,
            'total_messages': total_included_messages,
            'total_unique_users': total_included_users,
            'confidence_distribution': confidence_dist
        },
        'categories': category_stats.to_dict('records'),
        'top_gpts_by_category': top_by_category,
        'uncategorized_high_volume': [
            {
                'name': row['gpt_name'],
                'messages': int(row['messages_workspace']),
                'description': str(row['gpt_description'])[:100] if pd.notna(row['gpt_description']) else None
            }
            for _, row in df_included[
                (df_included['category'] == 'Other / Uncategorized') & 
                (df_included['messages_workspace'] > 10)
            ].iterrows()
        ],
        'all_categorizations': categorization_results
    }
    
    return result


def generate_markdown_report(analysis: dict) -> str:
    """
    Generate a formatted markdown report from analysis results.
    """
    
    lines = []
    
    # Header
    lines.append(f"# GPT Usage Analysis Report")
    lines.append(f"**Period**: {analysis['metadata']['period']}")
    lines.append(f"**Generated**: {analysis['metadata']['analysis_date'][:10]}")
    lines.append(f"")
    
    # Executive Summary
    lines.append(f"## Executive Summary")
    lines.append(f"- **Total Live GPTs**: {analysis['metadata']['total_live_gpts']}")
    lines.append(f"- **Excluded (High-Volume)**: {analysis['exclusions']['count']} GPTs ({analysis['exclusions']['total_messages']:,} messages)")
    lines.append(f"- **Analyzed GPTs**: {analysis['summary']['total_gpts_analyzed']} ({analysis['summary']['total_messages']:,} messages)")
    lines.append(f"- **Unique Users**: {analysis['summary']['total_unique_users']}")
    lines.append(f"- **Categorization Confidence**: {analysis['summary']['confidence_distribution']}")
    lines.append(f"")
    
    # Excluded GPTs
    lines.append(f"## Excluded High-Volume GPTs")
    lines.append(f"| GPT | Messages | Exclusion Reason |")
    lines.append(f"|-----|----------|------------------|")
    for gpt in analysis['exclusions']['top_excluded']:
        lines.append(f"| {gpt['name']} | {gpt['messages']:,} | {gpt['reason']} |")
    lines.append(f"")
    
    # Category Breakdown
    lines.append(f"## Category Breakdown")
    lines.append(f"| Category | GPTs | Messages | % of Total | Users |")
    lines.append(f"|----------|------|----------|------------|-------|")
    for cat in analysis['categories']:
        lines.append(f"| {cat['category']} | {cat['gpt_count']} | {cat['total_messages']:,} | {cat['percentage']}% | {cat['total_users']} |")
    lines.append(f"")
    
    # Detailed Category Analysis
    lines.append(f"## Detailed Analysis by Category")
    for cat_name, gpts in analysis['top_gpts_by_category'].items():
        cat_stats = next((c for c in analysis['categories'] if c['category'] == cat_name), None)
        if cat_stats:
            lines.append(f"")
            lines.append(f"### {cat_name}")
            lines.append(f"*{CATEGORY_DEFINITIONS.get(cat_name, {}).get('description', '')}*")
            lines.append(f"")
            lines.append(f"**Stats**: {cat_stats['gpt_count']} GPTs | {cat_stats['total_messages']:,} messages | {cat_stats['percentage']}% of usage")
            lines.append(f"")
            lines.append(f"| GPT | Messages | Users | Confidence |")
            lines.append(f"|-----|----------|-------|------------|")
            for gpt in gpts[:5]:  # Top 5
                conf_emoji = {'high': '🟢', 'medium': '🟡', 'low': '🔴'}.get(gpt.get('confidence', 'unknown'), '⚪')
                lines.append(f"| {gpt['name']} | {gpt['messages']:,} | {gpt['users']} | {conf_emoji} {gpt.get('confidence', 'unknown')} |")
    lines.append(f"")
    
    # Uncategorized high-volume
    if analysis['uncategorized_high_volume']:
        lines.append(f"## ⚠️ Uncategorized High-Volume GPTs")
        lines.append(f"These GPTs have >10 messages but weren't categorized. Review and update keywords.")
        lines.append(f"")
        for gpt in analysis['uncategorized_high_volume']:
            lines.append(f"- **{gpt['name']}** ({gpt['messages']} messages)")
            if gpt['description']:
                lines.append(f"  - Description: {gpt['description']}")
        lines.append(f"")
    
    # Recommendations
    lines.append(f"## Recommendations")
    
    # Find insights
    cats = analysis['categories']
    if cats:
        top_cat = cats[0]
        if top_cat['percentage'] > 40:
            lines.append(f"- ⚠️ **Category Concentration**: {top_cat['category']} dominates with {top_cat['percentage']:.0f}% of usage")
        
        low_usage = [c for c in cats if c['total_messages'] < 100]
        if low_usage:
            lines.append(f"- 💡 **Growth Opportunity**: {len(low_usage)} categories have <100 messages—consider promotion")
    
    if analysis['uncategorized_high_volume']:
        lines.append(f"- 🔧 **Data Quality**: {len(analysis['uncategorized_high_volume'])} high-volume GPTs need manual categorization review")
    
    high_conf = analysis['summary']['confidence_distribution'].get('high', 0)
    total_cat = sum(analysis['summary']['confidence_distribution'].values())
    if total_cat > 0 and high_conf / total_cat < 0.7:
        lines.append(f"- 📊 **Categorization Coverage**: Only {high_conf/total_cat*100:.0f}% high-confidence categorizations—consider enriching descriptions")
    
    return "\n".join(lines)


def compare_periods(current_analysis: dict, previous_analysis: dict) -> dict:
    """
    Compare two analysis periods and generate MoM insights.
    """
    
    comparison = {
        'periods': {
            'current': current_analysis['metadata']['period'],
            'previous': previous_analysis['metadata']['period']
        },
        'overall': {
            'current_gpts': current_analysis['summary']['total_gpts_analyzed'],
            'previous_gpts': previous_analysis['summary']['total_gpts_analyzed'],
            'gpt_change': current_analysis['summary']['total_gpts_analyzed'] - previous_analysis['summary']['total_gpts_analyzed'],
            'current_messages': current_analysis['summary']['total_messages'],
            'previous_messages': previous_analysis['summary']['total_messages'],
            'message_change': current_analysis['summary']['total_messages'] - previous_analysis['summary']['total_messages'],
            'pct_change': round(
                (current_analysis['summary']['total_messages'] - previous_analysis['summary']['total_messages']) / 
                previous_analysis['summary']['total_messages'] * 100, 1
            ) if previous_analysis['summary']['total_messages'] > 0 else 0
        }
    }
    
    # Category comparison
    curr_cats = {c['category']: c for c in current_analysis['categories']}
    prev_cats = {c['category']: c for c in previous_analysis['categories']}
    all_cats = set(curr_cats.keys()) | set(prev_cats.keys())
    
    category_changes = []
    for cat in all_cats:
        curr = curr_cats.get(cat, {'total_messages': 0, 'percentage': 0, 'gpt_count': 0})
        prev = prev_cats.get(cat, {'total_messages': 0, 'percentage': 0, 'gpt_count': 0})
        
        change = {
            'category': cat,
            'current_messages': curr.get('total_messages', 0),
            'previous_messages': prev.get('total_messages', 0),
            'absolute_change': curr.get('total_messages', 0) - prev.get('total_messages', 0),
            'pct_change': round(
                (curr.get('total_messages', 0) - prev.get('total_messages', 0)) / prev.get('total_messages', 0) * 100, 1
            ) if prev.get('total_messages', 0) > 0 else None,
            'current_gpts': curr.get('gpt_count', 0),
            'previous_gpts': prev.get('gpt_count', 0),
            'status': 'new' if cat not in prev_cats else ('removed' if cat not in curr_cats else 'existing')
        }
        category_changes.append(change)
    
    comparison['category_changes'] = sorted(category_changes, key=lambda x: abs(x.get('absolute_change', 0)), reverse=True)
    
    # Growth/decline flags
    comparison['growing_categories'] = [c for c in category_changes if c.get('pct_change', 0) and c['pct_change'] > 20]
    comparison['declining_categories'] = [c for c in category_changes if c.get('pct_change', 0) and c['pct_change'] < -20]
    
    return comparison


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Example usage
    print("GPT Usage Analyzer - Self-Contained Version")
    print("=" * 50)
    print()
    print("To use this script:")
    print("1. Upload your Excel file to the GPT")
    print("2. Run: result = analyze_gpt_data('your_file.xlsx', 'December 2025')")
    print("3. Generate report: print(generate_markdown_report(result))")
    print()
    print("For month-over-month comparison:")
    print("comparison = compare_periods(current_analysis, previous_analysis)")