"""
Example Workflow: How incremental processing works

This demonstrates creating a piece, finding a hot spot, and spawning child nodes.
"""

from practice_data_model import (
    PracticeNode, NodeType, Rating, PracticeSession,
    update_srs_schedule, calculate_step_difference
)
from datetime import datetime


def create_hot_spot_and_children(parent_node: PracticeNode, hot_spot_measure: str, 
                                  hot_spot_step: int, notes: str = "") -> tuple:
    """
    When a hot spot is discovered, create:
    1. A hot spot card for the difficult measure
    2. A child segment before the hot spot
    3. A child segment after the hot spot
    
    Returns: (hot_spot_node, before_segment, after_segment)
    """
    # Create hot spot node
    hot_spot = PracticeNode(
        node_type=NodeType.HOT_SPOT,
        title=f"{parent_node.title} - m.{hot_spot_measure}",
        measure_start=hot_spot_measure,
        measure_end=hot_spot_measure,
        target_tempo_bpm=parent_node.target_tempo_bpm,
        current_step=hot_spot_step,
        parent_id=parent_node.id,
        hot_spot_measure=hot_spot_measure,
        hot_spot_notes=notes
    )
    
    # Create "before" segment (with 1 measure lead-in to hot spot)
    before_end = str(int(hot_spot_measure) + 1) if hot_spot_measure.isdigit() else f"{hot_spot_measure}+1"
    before_segment = PracticeNode(
        node_type=NodeType.SEGMENT,
        title=f"{parent_node.title} - m.{parent_node.measure_start} to {before_end}",
        measure_start=parent_node.measure_start,
        measure_end=before_end,
        target_tempo_bpm=parent_node.target_tempo_bpm,
        current_step=0,  # Start fresh
        parent_id=parent_node.id
    )
    
    # Create "after" segment (with overlap at hot spot)
    after_start = hot_spot_measure
    after_segment = PracticeNode(
        node_type=NodeType.SEGMENT,
        title=f"{parent_node.title} - m.{after_start} to {parent_node.measure_end}",
        measure_start=after_start,
        measure_end=parent_node.measure_end,
        target_tempo_bpm=parent_node.target_tempo_bpm,
        current_step=0,  # Start fresh
        parent_id=parent_node.id
    )
    
    # Update parent with children
    parent_node.children_ids = [hot_spot.id, before_segment.id, after_segment.id]
    
    # Mark all new nodes as "Easy" on first encounter
    for node in [hot_spot, before_segment, after_segment]:
        update_srs_schedule(node.srs, Rating.EASY, is_first_attempt=True)
    
    return hot_spot, before_segment, after_segment


def simulate_practice_session():
    """Simulate a complete practice session workflow"""
    
    print("="*70)
    print("PRACTICE SESSION SIMULATION")
    print("="*70)
    
    # 1. Create initial piece
    print("\n1. Creating new piece...")
    sonata = PracticeNode(
        node_type=NodeType.PIECE,
        title="Adelaide Coles Sonata, Mvt. 1",
        measure_start="1",
        measure_end="120",
        target_tempo_bpm=144.0,
        current_step=0
    )
    print(f"   Created: {sonata.title}")
    print(f"   Target: {sonata.target_tempo_bpm} BPM")
    print(f"   Due: {sonata.srs.due_date.strftime('%Y-%m-%d')}")
    
    # 2. First practice attempt - find a hot spot
    print("\n2. First practice attempt...")
    print("   Starting at step +4 (19% above target = 171.4 BPM)")
    print("   User runs tempo search...")
    print("   → Error discovered at measure 47")
    print("   → Binary search finds maximum: step -7 (88.6 BPM)")
    
    # Record the session
    session1 = PracticeSession(
        node_id=sonata.id,
        starting_step=4,
        achieved_step=-7,
        hot_spot_discovered=True,
        hot_spot_measure="47",
        notes="Difficult interval leap with awkward fingering"
    )
    sonata.practice_history.append(session1.to_dict())
    sonata.current_step = -7
    
    # First attempt: always marked as "Easy" (successful identification)
    update_srs_schedule(sonata.srs, Rating.EASY, is_first_attempt=True)
    print(f"   First attempt complete! Marked as 'Easy'")
    print(f"   Next review: {sonata.srs.due_date.strftime('%Y-%m-%d')} ({sonata.srs.interval} days)")
    
    # 3. Create hot spot and child segments
    print("\n3. Creating hot spot and child segments...")
    hot_spot, before, after = create_hot_spot_and_children(
        sonata, 
        hot_spot_measure="47",
        hot_spot_step=-7,
        notes="Difficult interval leap with awkward fingering"
    )
    
    print(f"   ✓ Hot spot: {hot_spot.title}")
    print(f"     - Tempo: step {hot_spot.current_step} ({88.6} BPM)")
    print(f"     - Due: {hot_spot.srs.due_date.strftime('%Y-%m-%d')}")
    
    print(f"   ✓ Before segment: {before.title}")
    print(f"     - Due: {before.srs.due_date.strftime('%Y-%m-%d')}")
    
    print(f"   ✓ After segment: {after.title}")
    print(f"     - Due: {after.srs.due_date.strftime('%Y-%m-%d')}")
    
    # 4. Simulate practicing the hot spot again (improved by 2 steps)
    print("\n4. Hot spot comes due again - practice it...")
    print("   Starting at step +4 (171.4 BPM)")
    print("   Binary search finds maximum: step -5 (96.6 BPM)")
    print("   Previous was step -7, now -5 → improved by 2 steps!")
    
    previous_step = hot_spot.current_step
    hot_spot.current_step = -5
    
    # Calculate rating
    rating = calculate_step_difference(previous_step, hot_spot.current_step)
    print(f"   Auto-rating: {rating.value.upper()} (improved by 2 steps)")
    
    # Update SRS
    update_srs_schedule(hot_spot.srs, rating)
    print(f"   Next review: {hot_spot.srs.due_date.strftime('%Y-%m-%d')} ({hot_spot.srs.interval} days)")
    print(f"   Ease factor: {hot_spot.srs.ease_factor:.2f}")
    
    # 5. Parent node eventually comes due again
    print("\n5. Later: Original full piece comes due again...")
    print("   This provides opportunity to practice full passage (reassembly)")
    print("   If successful, children's work has paid off!")
    print("   If new hot spot found, spawn more children...")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Nodes in system: 4 (1 original + 1 hot spot + 2 segments)")
    print(f"All tracked independently in SRS")
    print(f"System naturally focuses practice on weaknesses")
    print(f"Tree self-balances over time")


if __name__ == "__main__":
    simulate_practice_session()
