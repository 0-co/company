"""
Semantic Emergence Analyzer for alice-bot conversation.

Analyzes the alice-archaeology-data.json conversation for:
1. Per-exchange vocabulary tracking (new words, running vocab size by author)
2. Concept arcs (word introduced by A, later adopted by B)
3. Cornerstone words (words appearing in 10+ exchanges)
4. Depth score per exchange

Outputs: /home/agent/company/docs/semantic-emergence-data.json
"""

import json
import re
from collections import defaultdict, Counter

INPUT_PATH = "/home/agent/company/docs/alice-archaeology-data.json"
OUTPUT_PATH = "/home/agent/company/docs/semantic-emergence-data.json"

# Base stopwords from fetch_conversation.py
STOPWORDS = {
    'the','a','an','and','or','but','in','on','at','to','for','of','with','by',
    'from','is','it','its','this','that','we','our','i','you','be','are','was',
    'were','have','has','had','do','does','did','not','as','if','so','what','how',
    'when','where','who','which','there','their','they','them','then','than','into',
    'can','will','just','about','up','out','like','more','also','even','still',
    'only','no','one','two','three','all','each','any','some','new','same','other',
    'both','your','my','me','us','he','she','his','her','way','every','after',
    'before','through','between','while','because','without','within','over',
    'under','again','been','very','much','most','own','these','those','here',
    'now','back','get','got','could','would','should','might','make','take',
    'see','come','go','say','know','think','feel','need','want','keep','find','give',
    'something','nothing','anything','everything','part','point',
    # Domain-specific stopwords (filler/acknowledgement words)
    'yes','exactly','right','good','well','too','really','think','know',
    # Common verbs that don't carry semantic content in this context
    'having','talking','trying','proving','prove','tell','telling','once',
    'happening','thinking','saying','looking','asking','putting','letting',
    'always','never','often','maybe','perhaps','actually','basically','literally',
    'just','already','still','almost','enough','further','otherwise',
    # Contractions broken apart (apostrophe-less forms)
    'that','with','from','have','this','they','their','them','then','than',
    'doesn','isn','aren','wasn','weren','haven','hadn','hasn','didn','couldn',
    'wouldn','shouldn','mustn','mightn','shan',
}

def get_words(text):
    """Extract significant words from text, filtering stopwords and contractions."""
    # Only match pure alpha words (no apostrophes — those are contractions, not content)
    raw = re.findall(r"[a-z]+", text.lower())
    return [w for w in raw if len(w) > 3 and w.lower() not in STOPWORDS]

def author_label(author):
    """Normalize author handle to short label."""
    if 'alice' in author:
        return 'alice-bot'
    return '0coceo'

def run():
    with open(INPUT_PATH) as f:
        data = json.load(f)

    exchanges = data['exchanges']
    total = len(exchanges)

    # -----------------------------------------------------------------------
    # 1. Per-exchange vocabulary tracking
    # -----------------------------------------------------------------------

    # Track: set of all words seen so far (globally), and per-author
    global_seen = set()
    ours_seen = set()
    alice_seen = set()

    # Per-exchange: new words introduced (globally first time), running vocab
    exchange_analysis = []

    # Word -> first occurrence info: {exchange_num, author}
    word_first = {}  # word -> {exchange_num (1-indexed), author_label}

    # Per-word: list of exchanges where it appears (by index, 0-based)
    word_exchange_list = defaultdict(list)

    # Per-exchange: which words appear
    exchange_words = []

    for i, ex in enumerate(exchanges):
        exnum = i + 1
        author = author_label(ex['author'])
        words = get_words(ex['text'])
        word_set = set(words)

        exchange_words.append({'exnum': exnum, 'author': author, 'words': words, 'word_set': word_set})

        # Track word-level first occurrences
        for w in word_set:
            word_exchange_list[w].append(exnum)
            if w not in word_first:
                word_first[w] = {'exchange_num': exnum, 'author': author}

        # New words introduced globally this exchange
        new_global = word_set - global_seen
        global_seen.update(word_set)

        if author == '0coceo':
            ours_seen.update(word_set)
        else:
            alice_seen.update(word_set)

        exchange_analysis.append({
            'exchange_num': exnum,
            'author': author,
            'new_words_count': len(new_global),
            'new_words': sorted(list(new_global)),
            'running_vocab_size': len(global_seen),
            'running_ours_size': len(ours_seen),
            'running_alice_size': len(alice_seen),
            'total_words_in_exchange': len(words),
        })

    # -----------------------------------------------------------------------
    # 2. Concept arcs
    #    - Word first introduced by author A
    #    - Later used by author B (the other party)
    #    - Word appears 3+ times total across all exchanges
    #    - Track lag (exchanges between introduction and first adoption)
    # -----------------------------------------------------------------------

    concept_arcs = []

    # For each word, find if the OTHER author eventually used it
    for word, first_info in word_first.items():
        if len(word_exchange_list[word]) < 3:
            # Skip hapax legomena and low-frequency words
            continue

        introducer = first_info['author']
        intro_exchange = first_info['exchange_num']

        # Find first use by the OTHER author
        other_author = 'alice-bot' if introducer == '0coceo' else '0coceo'
        other_first = None

        for exnum in word_exchange_list[word]:
            ex_idx = exnum - 1
            ex = exchange_words[ex_idx]
            if ex['author'] == other_author and word in ex['word_set']:
                if other_first is None or exnum < other_first:
                    other_first = exnum
                break  # already sorted by exnum

        if other_first is not None and other_first > intro_exchange:
            lag = other_first - intro_exchange
            total_uses = len(word_exchange_list[word])
            concept_arcs.append({
                'word': word,
                'introduced_by': introducer,
                'intro_exchange': intro_exchange,
                'adopted_by': other_author,
                'adoption_exchange': other_first,
                'lag': lag,
                'total_uses': total_uses,
            })

    # Sort by lag descending (longest = most interesting)
    concept_arcs.sort(key=lambda x: (-x['lag'], -x['total_uses']))

    # -----------------------------------------------------------------------
    # 3. Cornerstone words
    #    - Words used in 10+ separate exchanges
    # -----------------------------------------------------------------------

    # word_exchange_list already has deduplicated-per-exchange counts
    # (since we used word_set per exchange, each exchange is counted once)
    cornerstone_words = []
    for word, ex_list in word_exchange_list.items():
        unique_exchanges = len(set(ex_list))
        if unique_exchanges >= 10:
            cornerstone_words.append({
                'word': word,
                'exchange_count': unique_exchanges,
                'total_uses_approx': sum(
                    exchange_words[e - 1]['words'].count(word)
                    for e in ex_list
                ),
                'introduced_by': word_first[word]['author'],
                'intro_exchange': word_first[word]['exchange_num'],
            })

    cornerstone_words.sort(key=lambda x: (-x['exchange_count'], -x['total_uses_approx']))

    # -----------------------------------------------------------------------
    # 4. Depth score per exchange
    #    depth = (new_concepts * 0.5) + (adopted_concepts * 1.5) + (cornerstone_concepts * 2.0)
    #    Normalized to 0-10
    # -----------------------------------------------------------------------

    cornerstone_set = {cw['word'] for cw in cornerstone_words}
    # For concept arcs: adoption_exchange -> list of adopted words
    adoption_at = defaultdict(list)
    for arc in concept_arcs:
        adoption_at[arc['adoption_exchange']].append(arc['word'])

    raw_depths = []
    for ea in exchange_analysis:
        exnum = ea['exchange_num']
        word_set = exchange_words[exnum - 1]['word_set']

        new_count = ea['new_words_count']
        adopted_count = len([w for w in adoption_at.get(exnum, []) if w in word_set])
        cornerstone_count = len([w for w in word_set if w in cornerstone_set])

        raw = (new_count * 0.5) + (adopted_count * 1.5) + (cornerstone_count * 2.0)
        raw_depths.append(raw)

    max_depth = max(raw_depths) if raw_depths else 1.0
    if max_depth == 0:
        max_depth = 1.0

    for i, ea in enumerate(exchange_analysis):
        exnum = ea['exchange_num']
        word_set = exchange_words[exnum - 1]['word_set']
        new_count = ea['new_words_count']
        adopted_count = len([w for w in adoption_at.get(exnum, []) if w in word_set])
        cornerstone_count = len([w for w in word_set if w in cornerstone_set])

        normalized = round((raw_depths[i] / max_depth) * 10, 2)
        ea['depth_score'] = normalized
        ea['depth_new'] = new_count
        ea['depth_adopted'] = adopted_count
        ea['depth_cornerstone'] = cornerstone_count

    # -----------------------------------------------------------------------
    # Build output
    # -----------------------------------------------------------------------

    # Vocabulary growth curve: per exchange, cumulative ours vs alice
    growth_curve = []
    ours_running = 0
    alice_running = 0
    ours_seen2 = set()
    alice_seen2 = set()

    for ex in exchange_words:
        if ex['author'] == '0coceo':
            new_ours = len(ex['word_set'] - ours_seen2)
            ours_seen2.update(ex['word_set'])
            ours_running += new_ours
        else:
            new_alice = len(ex['word_set'] - alice_seen2)
            alice_seen2.update(ex['word_set'])
            alice_running += new_alice

        growth_curve.append({
            'exchange_num': ex['exnum'],
            'author': ex['author'],
            'ours_cumulative': ours_running,
            'alice_cumulative': alice_running,
            'global_cumulative': exchange_analysis[ex['exnum'] - 1]['running_vocab_size'],
        })

    # Top 20 concept arcs for display
    top_arcs = concept_arcs[:20]

    output = {
        'generated_at': '2026-03-11',
        'total_exchanges': total,
        'total_unique_words': len(global_seen),
        'total_cornerstone_words': len(cornerstone_words),
        'total_concept_arcs': len(concept_arcs),
        'exchange_analysis': exchange_analysis,
        'concept_arcs': top_arcs,
        'all_arcs_count': len(concept_arcs),
        'cornerstone_words': cornerstone_words,
        'growth_curve': growth_curve,
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Done.")
    print(f"  Exchanges analyzed: {total}")
    print(f"  Unique words tracked: {len(global_seen)}")
    print(f"  Concept arcs found: {len(concept_arcs)}")
    print(f"  Cornerstone words (10+ exchanges): {len(cornerstone_words)}")
    if cornerstone_words:
        print(f"  Top cornerstone: {cornerstone_words[0]['word']} ({cornerstone_words[0]['exchange_count']} exchanges)")
    if concept_arcs:
        arc = concept_arcs[0]
        print(f"  Longest arc: '{arc['word']}' ({arc['introduced_by']} → {arc['adopted_by']}, lag={arc['lag']} exchanges)")
    print(f"  Output: {OUTPUT_PATH}")

if __name__ == '__main__':
    run()
