"""
Music Practice SRS - Data Model
Timothy Owen - February 2026

This module defines the core data structures for tracking musical pieces,
segments, and hot spots with spaced repetition scheduling.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid


# ============================================================================
# ENUMS
# ============================================================================

class NodeType(Enum):
    """Type of practice node"""
    PIECE = "piece"          # Original full piece
    SEGMENT = "segment"      # Child segment from splitting
    HOT_SPOT = "hot_spot"    # Individual difficult measure


class Rating(Enum):
    """SRS rating based on tempo progress"""
    EASY = "easy"      # Improved ≥1 step from previous
    GOOD = "good"      # Maintained same step
    HARD = "hard"      # Dropped 1 step
    AGAIN = "again"    # Dropped ≥2 steps or other failure


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class SRSData:
    """
    Anki SM-2 scheduling data
    
    Tutorial: This tracks when the node is "due" for practice and how
    well you're doing with it. The algorithm automatically spaces out
    practice sessions - things you're good at show up less often.
    """
    interval: int = 1              # Days until next review
    repetitions: int = 0           # Number of successful reviews in a row
    ease_factor: float = 2.5       # Multiplier for interval growth (starts at 2.5)
    due_date: datetime = field(default_factory=datetime.now)
    last_reviewed: Optional[datetime] = None
    
    def is_due(self) -> bool:
        """Check if this node is due for practice"""
        return datetime.now() >= self.due_date
    
    def days_until_due(self) -> int:
        """How many days until this is due (negative = overdue)"""
        delta = self.due_date - datetime.now()
        return delta.days


@dataclass
class PracticeNode:
    """
    A piece, segment, or hot spot that can be practiced
    
    Tutorial: This is the main building block. Every piece starts as one node.
    When you find a hot spot, you create 3 new nodes: the hot spot itself,
    and two child segments (before and after the hot spot).
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_type: NodeType = NodeType.PIECE
    title: str = ""
    
    # Measure range (flexible - can be numbers, rehearsal letters, etc.)
    measure_start: str = "1"
    measure_end: str = "100"
    
    # Tempo tracking (step-based: target tempo = step 0)
    target_tempo_bpm: float = 120.0    # The "correct" tempo for this piece
    current_step: int = 0               # Current achievement relative to target
    
    # Tree structure
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    
    # SRS scheduling
    srs: SRSData = field(default_factory=SRSData)
    
    # Hot spot specific (only used when node_type = HOT_SPOT)
    hot_spot_measure: Optional[str] = None
    hot_spot_notes: str = ""
    
    # History tracking
    practice_history: List[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON storage"""
        return {
            'id': self.id,
            'node_type': self.node_type.value,
            'title': self.title,
            'measure_start': self.measure_start,
            'measure_end': self.measure_end,
            'target_tempo_bpm': self.target_tempo_bpm,
            'current_step': self.current_step,
            'parent_id': self.parent_id,
            'children_ids': self.children_ids,
            'srs': {
                'interval': self.srs.interval,
                'repetitions': self.srs.repetitions,
                'ease_factor': self.srs.ease_factor,
                'due_date': self.srs.due_date.isoformat(),
                'last_reviewed': self.srs.last_reviewed.isoformat() if self.srs.last_reviewed else None
            },
            'hot_spot_measure': self.hot_spot_measure,
            'hot_spot_notes': self.hot_spot_notes,
            'practice_history': self.practice_history,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PracticeNode':
        """Create from dictionary (for loading from JSON)"""
        # Parse SRS data
        srs_data = data.get('srs', {})
        srs = SRSData(
            interval=srs_data.get('interval', 1),
            repetitions=srs_data.get('repetitions', 0),
            ease_factor=srs_data.get('ease_factor', 2.5),
            due_date=datetime.fromisoformat(srs_data['due_date']) if srs_data.get('due_date') else datetime.now(),
            last_reviewed=datetime.fromisoformat(srs_data['last_reviewed']) if srs_data.get('last_reviewed') else None
        )
        
        return cls(
            id=data['id'],
            node_type=NodeType(data['node_type']),
            title=data.get('title', ''),
            measure_start=data.get('measure_start', '1'),
            measure_end=data.get('measure_end', '100'),
            target_tempo_bpm=data.get('target_tempo_bpm', 120.0),
            current_step=data.get('current_step', 0),
            parent_id=data.get('parent_id'),
            children_ids=data.get('children_ids', []),
            srs=srs,
            hot_spot_measure=data.get('hot_spot_measure'),
            hot_spot_notes=data.get('hot_spot_notes', ''),
            practice_history=data.get('practice_history', []),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now()
        )


@dataclass
class PracticeSession:
    """
    Records what happened during a practice session
    
    Tutorial: This is like a journal entry for each time you practice
    a node. It tracks what tempo you achieved and how you rated it.
    """
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    # What happened
    starting_step: int = 0
    achieved_step: int = 0
    rating: Optional[Rating] = None
    
    # Hot spot discovery (if applicable)
    hot_spot_discovered: bool = False
    hot_spot_measure: Optional[str] = None
    
    # Notes
    notes: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            'session_id': self.session_id,
            'node_id': self.node_id,
            'timestamp': self.timestamp.isoformat(),
            'starting_step': self.starting_step,
            'achieved_step': self.achieved_step,
            'rating': self.rating.value if self.rating else None,
            'hot_spot_discovered': self.hot_spot_discovered,
            'hot_spot_measure': self.hot_spot_measure,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PracticeSession':
        """Create from dictionary"""
        return cls(
            session_id=data['session_id'],
            node_id=data['node_id'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            starting_step=data.get('starting_step', 0),
            achieved_step=data.get('achieved_step', 0),
            rating=Rating(data['rating']) if data.get('rating') else None,
            hot_spot_discovered=data.get('hot_spot_discovered', False),
            hot_spot_measure=data.get('hot_spot_measure'),
            notes=data.get('notes', '')
        )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_step_difference(previous_step: int, current_step: int) -> Rating:
    """
    Determine rating based on step progression
    
    Tutorial: This is how we automatically rate your progress.
    If you improved by 1+ steps: Easy
    If you stayed the same: Good
    If you dropped 1 step: Hard
    If you dropped 2+ steps: Again (failed)
    """
    diff = current_step - previous_step
    
    if diff >= 1:
        return Rating.EASY
    elif diff == 0:
        return Rating.GOOD
    elif diff == -1:
        return Rating.HARD
    else:  # diff <= -2
        return Rating.AGAIN


def update_srs_schedule(srs: SRSData, rating: Rating, is_first_attempt: bool = False) -> None:
    """
    Update SRS scheduling based on rating (Anki SM-2 algorithm)
    
    Tutorial: This is the "spaced repetition" magic. Based on how you did,
    it calculates when you should practice this again. Things you're good
    at show up less frequently.
    
    Args:
        srs: The SRS data to update
        rating: How well you did (Easy/Good/Hard/Again)
        is_first_attempt: True if this is the very first time practicing this node
    """
    srs.last_reviewed = datetime.now()
    
    # First attempt: always mark as Easy (you either succeeded or found the hot spot)
    if is_first_attempt:
        srs.interval = 1
        srs.repetitions = 1
        srs.ease_factor = 2.5
        srs.due_date = datetime.now() + timedelta(days=1)
        return
    
    # Anki SM-2 algorithm
    if rating == Rating.AGAIN:
        # Failed - reset repetitions, show again soon
        srs.repetitions = 0
        srs.interval = 1
        srs.due_date = datetime.now() + timedelta(days=1)
    else:
        # Successful review
        srs.repetitions += 1
        
        # Adjust ease factor based on rating
        if rating == Rating.HARD:
            srs.ease_factor = max(1.3, srs.ease_factor - 0.15)
        elif rating == Rating.GOOD:
            srs.ease_factor = max(1.3, srs.ease_factor)  # No change
        elif rating == Rating.EASY:
            srs.ease_factor = srs.ease_factor + 0.15
        
        # Calculate new interval
        if srs.repetitions == 1:
            srs.interval = 1
        elif srs.repetitions == 2:
            srs.interval = 6
        else:
            srs.interval = int(srs.interval * srs.ease_factor)
        
        srs.due_date = datetime.now() + timedelta(days=srs.interval)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Create a new piece
    sonata = PracticeNode(
        node_type=NodeType.PIECE,
        title="Adelaide Coles Sonata, Mvt. 1",
        measure_start="1",
        measure_end="120",
        target_tempo_bpm=144.0,
        current_step=0  # Starting at target tempo (step 0)
    )
    
    print("Created new piece:")
    print(f"  Title: {sonata.title}")
    print(f"  Measures: {sonata.measure_start}-{sonata.measure_end}")
    print(f"  Target tempo: {sonata.target_tempo_bpm} BPM")
    print(f"  Due: {sonata.srs.due_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Days until due: {sonata.srs.days_until_due()}")
    
    # Save to JSON
    piece_json = json.dumps(sonata.to_dict(), indent=2)
    print("\nJSON representation:")
    print(piece_json)
    
    # Load back from JSON
    loaded_sonata = PracticeNode.from_dict(json.loads(piece_json))
    print(f"\nSuccessfully loaded: {loaded_sonata.title}")
