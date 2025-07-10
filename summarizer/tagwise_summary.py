from collections import defaultdict, Counter
from llama_cpp import Llama
import os
import hashlib
import random
from typing import List, Dict, Any

# LLM Initialization
MODEL_PATH = "./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=6,
    verbose=False
)

# Philosophical frameworks for deeper analysis
PHILOSOPHICAL_FRAMEWORKS = [
    "Stoicism", "Existentialism", "Utilitarianism", 
    "Nietzschean", "Buddhist", "Taoist", 
    "Postmodern", "Humanist", "Absurdist"
]

def generate_humanized_themes(tags: List[str]) -> List[str]:
    """Convert raw tags into human-readable themes with philosophical depth"""
    theme_map = {
        'life': 'The Human Condition',
        'love': 'Love & Existential Bonds',
        'inspirational': 'Existential Motivation',
        'humor': 'Absurdity & Irony', 
        'friends': 'Interpersonal Philosophy',
        'change': 'Metaphysics of Change',
        'thinking': 'Epistemological Inquiry',
        'deep-thoughts': 'Fundamental Wisdom',
        'world': 'Social Ontology',
        'choices': 'Agency & Determinism',
        'success': 'Teleological Perspectives',
        'time': 'Temporal Being',
        'truth': 'Epistemic Foundations',
        'science': 'Rationalist Paradigms',
        'art': 'Aesthetic Philosophy'
    }
    return [theme_map.get(tag, tag.title()) for tag in tags]

def generate_llm_response(prompt: str, temperature: float = 0.7) -> str:
    """Enhanced response handler with philosophical prompting"""
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=temperature,
        stop=["</output>"]
    )
    return response['choices'][0]['message']['content'].strip()

def generate_philosophical_analysis(quote: Dict[str, Any]) -> str:
    """Generate a deep philosophical analysis of a single quote"""
    framework = random.choice(PHILOSOPHICAL_FRAMEWORKS)
    prompt = f"""
    Analyze this quote through the lens of {framework} philosophy:
    "{quote['text']}" — {quote['author']}
    
    Provide:
    1. Key philosophical concepts addressed
    2. How {framework} would interpret this
    3. Potential counterarguments from other schools
    4. Modern relevance
    
    Keep analysis under 150 words.
    """
    return generate_llm_response(prompt, temperature=0.8)

def generate_overall_insight(quotes: List[Dict[str, Any]]) -> str:
    """Generate interconnected philosophical insights"""
    sample_quotes = '\n'.join([f'"{q["text"]}" - {q["author"]}' for q in quotes[:3]])
    framework = random.choice(PHILOSOPHICAL_FRAMEWORKS)
    
    prompt = f"""
    Analyze these quotes collectively through {framework} philosophy:
    {sample_quotes}
    
    Identify:
    1. The underlying philosophical thread
    2. How different thinkers approach similar concepts
    3. The evolution of these ideas historically
    4. Practical applications in modern life
    
    Respond in this format:
    Philosophical Insight: [your analysis]
    School of Thought: {framework}
    """
    response = generate_llm_response(prompt, temperature=0.75)
    return response

def generate_quote_synthesis(quotes: List[Dict[str, Any]]) -> str:
    """Create a synthesized philosophical statement"""
    tags_str = ', '.join(sorted({tag for q in quotes for tag in q['tags']}))
    framework = random.choice(PHILOSOPHICAL_FRAMEWORKS)
    
    prompt = f"""
    Synthesize a profound philosophical statement combining these themes: {tags_str}
    Style: {framework} philosophy
    Length: 1-2 sentences (under 20 words)
    Tone: Thought-provoking yet accessible
    
    Format STRICTLY as:
    "statement text" — [school of thought]
    """
    response = generate_llm_response(prompt, temperature=0.9)
    return response

def generate_quote_anthology(quotes: List[Dict[str, Any]], theme: str) -> str:
    """Create a curated collection of quotes around a theme"""
    prompt = f"""
    Select and arrange 3-5 quotes from this collection that best represent:
    {theme}
    
    For each quote:
    1. Include the text and author
    2. Add a brief commentary (1 sentence)
    3. Show how they connect
    
    Format as:
    ✦ Theme: {theme}
    [quote 1 with commentary]
    [quote 2 with commentary]
    ...
    Philosophical Significance: [1-2 sentences]
    """
    return generate_llm_response(prompt, temperature=0.7)

def generate_page_summary(quotes: List[Dict[str, Any]], page_num: int) -> str:
    try:
        # Enhanced statistics with philosophical context
        total_quotes = len(quotes)
        authors = Counter(q['author'] for q in quotes)
        top_authors = [author for author, count in authors.most_common(4)]
        
        # Philosophical tag analysis
        all_tags = [tag for q in quotes for tag in q['tags']]
        tag_counts = Counter(all_tags)
        common_tags = [tag for tag, count in tag_counts.most_common(5)]
        
        # Find most philosophically dense quote
        rep_quote = max(quotes, key=lambda q: len(q['tags']))
        
        # Generate humanized themes with philosophical framing
        themes = generate_humanized_themes(common_tags)
        
        # Format the summary with philosophical sections
        summary = f"""
=== PHILOSOPHICAL ANALYSIS OF QUOTES (PAGE {page_num}) ===

Total Quotes: {total_quotes}

Most Frequent Thinkers:
{'\n'.join(top_authors)}

Key Philosophical Themes:
{'\n'.join(themes)}

Most Conceptually Rich Quote:
"{rep_quote['text']}" — {rep_quote['author']}

Philosophical Analysis:
{generate_philosophical_analysis(rep_quote)}
"""

        # Add thematic philosophical explorations
        tag_groups = defaultdict(list)
        for q in quotes:
            for tag in q['tags']:
                tag_groups[tag].append(q)
        
        for tag, tag_quotes in tag_groups.items():
            if len(tag_quotes) >= 3:
                summary += f"""
✦ {generate_humanized_themes([tag])[0].upper()} ({len(tag_quotes)} quotes)
{'-'*60}
"""
                summary += generate_quote_anthology(tag_quotes[:5], tag) + "\n"

        # Final philosophical synthesis
        summary += "\n" + "="*60 + "\n"
        summary += "PHILOSOPHICAL SYNTHESIS:\n"
        try:
            summary += generate_overall_insight(quotes) + "\n\n"
        except Exception as e:
            summary += f"[Philosophical analysis failed: {str(e)}]\n\n"

        summary += "ESSENTIAL PHILOSOPHICAL STATEMENT:\n"
        try:
            summary += generate_quote_synthesis(quotes) + "\n"
        except Exception as e:
            summary += f"[Synthesis failed: {str(e)}]\n"

        return summary
    except Exception as e:
        return f"Error generating philosophical summary: {str(e)}"

def summarize_by_tag(quotes: List[Dict[str, Any]], page_num: int = 1) -> str:
    try:
        return generate_page_summary(quotes, page_num)
    except Exception as e:
        return f"Error generating philosophical summary: {str(e)}"

__all__ = ['summarize_by_tag']
