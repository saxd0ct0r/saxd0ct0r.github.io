"""
Music Practice SRS - Storage Layer
Timothy Owen - February 2026

Simple JSON-based storage for nodes and practice sessions.
Uses a single directory with two files: nodes.json and sessions.json
"""

import json
import os
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

from practice_data_model import PracticeNode, PracticeSession, NodeType


class PracticeDatabase:
    """
    Simple file-based storage for practice nodes and sessions.
    
    Tutorial: This class handles saving and loading your practice data.
    It uses JSON files which are easy to read and debug. Think of it
    as a simple filing cabinet for your practice information.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the database.
        
        Args:
            data_dir: Path to data directory. If None, uses ~/practice_data
        
        Tutorial: When you create a PracticeDatabase, it automatically
        sets up the folder structure if it doesn't exist.
        """
        if data_dir is None:
            # Default to home directory
            home = Path.home()
            data_dir = home / "practice_data"
        
        self.data_dir = Path(data_dir)
        self.nodes_file = self.data_dir / "nodes.json"
        self.sessions_file = self.data_dir / "sessions.json"
        
        # Create directory if it doesn't exist
        self._initialize_storage()
    
    def _initialize_storage(self):
        """
        Create storage directory and initialize empty files if needed.
        
        Tutorial: This runs automatically when you create the database.
        It makes sure the folder exists and creates empty data files
        if this is your first time using the app.
        """
        # Create directory
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize nodes file if it doesn't exist
        if not self.nodes_file.exists():
            with open(self.nodes_file, 'w') as f:
                json.dump([], f)
            print(f"Created new nodes file: {self.nodes_file}")
        
        # Initialize sessions file if it doesn't exist
        if not self.sessions_file.exists():
            with open(self.sessions_file, 'w') as f:
                json.dump([], f)
            print(f"Created new sessions file: {self.sessions_file}")
    
    # ========================================================================
    # NODE OPERATIONS
    # ========================================================================
    
    def save_node(self, node: PracticeNode) -> None:
        """
        Save or update a node.
        
        Tutorial: If the node already exists (same ID), this updates it.
        If it's new, this adds it to the collection.
        
        Args:
            node: The PracticeNode to save
        
        Raises:
            Exception: If the file is corrupted or can't be written
        """
        # Load all nodes
        nodes_data = self._load_json(self.nodes_file)
        
        # Convert node to dictionary
        node_dict = node.to_dict()
        
        # Find if this node already exists (by ID)
        existing_index = None
        for i, existing_node in enumerate(nodes_data):
            if existing_node['id'] == node.id:
                existing_index = i
                break
        
        # Update or append
        if existing_index is not None:
            nodes_data[existing_index] = node_dict
        else:
            nodes_data.append(node_dict)
        
        # Save back to file
        self._save_json(self.nodes_file, nodes_data)
    
    def load_node(self, node_id: str) -> Optional[PracticeNode]:
        """
        Load a specific node by ID.
        
        Args:
            node_id: The unique ID of the node
        
        Returns:
            The PracticeNode if found, None otherwise
        """
        nodes_data = self._load_json(self.nodes_file)
        
        for node_dict in nodes_data:
            if node_dict['id'] == node_id:
                return PracticeNode.from_dict(node_dict)
        
        return None
    
    def get_all_nodes(self) -> List[PracticeNode]:
        """
        Get all nodes in the database.
        
        Returns:
            List of all PracticeNodes
        """
        nodes_data = self._load_json(self.nodes_file)
        return [PracticeNode.from_dict(n) for n in nodes_data]
    
    def get_due_nodes(self) -> List[PracticeNode]:
        """
        Get all nodes that are due for practice (sorted by how overdue).
        
        Tutorial: This is what you'd call at the start of a practice session
        to see what needs to be practiced today.
        
        Returns:
            List of nodes that are due, sorted by most overdue first
        """
        all_nodes = self.get_all_nodes()
        due_nodes = [n for n in all_nodes if n.srs.is_due()]
        
        # Sort by due date (most overdue first)
        due_nodes.sort(key=lambda n: n.srs.due_date)
        
        return due_nodes
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[PracticeNode]:
        """
        Get all nodes of a specific type (PIECE, SEGMENT, or HOT_SPOT).
        
        Args:
            node_type: The type of node to filter by
        
        Returns:
            List of nodes matching that type
        """
        all_nodes = self.get_all_nodes()
        return [n for n in all_nodes if n.node_type == node_type]
    
    def delete_node(self, node_id: str) -> bool:
        """
        Delete a node from the database.
        
        Tutorial: Be careful with this! It permanently removes the node.
        You might want to delete old hot spots that have been mastered,
        or pieces you're no longer working on.
        
        Args:
            node_id: The ID of the node to delete
        
        Returns:
            True if deleted, False if not found
        """
        nodes_data = self._load_json(self.nodes_file)
        
        # Find and remove the node
        original_length = len(nodes_data)
        nodes_data = [n for n in nodes_data if n['id'] != node_id]
        
        if len(nodes_data) < original_length:
            self._save_json(self.nodes_file, nodes_data)
            return True
        
        return False
    
    # ========================================================================
    # SESSION OPERATIONS
    # ========================================================================
    
    def save_session(self, session: PracticeSession) -> None:
        """
        Save a practice session.
        
        Tutorial: Every time you practice a node, you save a session.
        This creates a history of your progress over time.
        
        Args:
            session: The PracticeSession to save
        """
        sessions_data = self._load_json(self.sessions_file)
        sessions_data.append(session.to_dict())
        self._save_json(self.sessions_file, sessions_data)
    
    def get_sessions_for_node(self, node_id: str) -> List[PracticeSession]:
        """
        Get all practice sessions for a specific node.
        
        Tutorial: This lets you see your complete history with a piece.
        You can track how your tempo has improved over time.
        
        Args:
            node_id: The ID of the node
        
        Returns:
            List of sessions for that node, sorted by date (oldest first)
        """
        sessions_data = self._load_json(self.sessions_file)
        
        # Filter to this node
        node_sessions = [
            PracticeSession.from_dict(s) 
            for s in sessions_data 
            if s['node_id'] == node_id
        ]
        
        # Sort by timestamp
        node_sessions.sort(key=lambda s: s.timestamp)
        
        return node_sessions
    
    def get_all_sessions(self) -> List[PracticeSession]:
        """
        Get all practice sessions across all nodes.
        
        Returns:
            List of all sessions, sorted by date
        """
        sessions_data = self._load_json(self.sessions_file)
        sessions = [PracticeSession.from_dict(s) for s in sessions_data]
        sessions.sort(key=lambda s: s.timestamp)
        return sessions
    
    # ========================================================================
    # STATISTICS & QUERIES
    # ========================================================================
    
    def get_stats(self) -> Dict:
        """
        Get summary statistics about your practice.
        
        Tutorial: This gives you a quick overview of your practice library.
        
        Returns:
            Dictionary with statistics
        """
        nodes = self.get_all_nodes()
        sessions = self.get_all_sessions()
        due_nodes = self.get_due_nodes()
        
        pieces = [n for n in nodes if n.node_type == NodeType.PIECE]
        segments = [n for n in nodes if n.node_type == NodeType.SEGMENT]
        hot_spots = [n for n in nodes if n.node_type == NodeType.HOT_SPOT]
        
        return {
            'total_nodes': len(nodes),
            'pieces': len(pieces),
            'segments': len(segments),
            'hot_spots': len(hot_spots),
            'due_nodes': len(due_nodes),
            'total_sessions': len(sessions),
            'data_directory': str(self.data_dir)
        }
    
    # ========================================================================
    # PRIVATE HELPER METHODS
    # ========================================================================
    
    def _load_json(self, filepath: Path) -> list:
        """
        Load JSON file. Crashes if file is corrupted.
        
        Tutorial: This is a private method (starts with _) that handles
        reading JSON files. If the file is corrupted, it crashes and
        tells you - this prevents silent data corruption.
        """
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise Exception(
                f"CORRUPTED FILE: {filepath}\n"
                f"Error: {e}\n"
                f"Please check the file or restore from backup."
            )
        except Exception as e:
            raise Exception(f"Error reading {filepath}: {e}")
    
    def _save_json(self, filepath: Path, data: list) -> None:
        """
        Save data to JSON file with pretty formatting.
        
        Tutorial: This writes the data to disk. We use indent=2 to make
        the files human-readable - you can open them in a text editor
        and see what's inside.
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise Exception(f"Error writing {filepath}: {e}")


# ============================================================================
# COMMAND-LINE TESTING
# ============================================================================

def test_database():
    """Test the database functionality"""
    print("="*70)
    print("TESTING PRACTICE DATABASE")
    print("="*70)
    
    # Create database (will use ~/practice_data)
    print("\n1. Initializing database...")
    db = PracticeDatabase()
    print(f"   Data directory: {db.data_dir}")
    
    # Create a test piece
    print("\n2. Creating test piece...")
    from practice_data_model import PracticeNode, NodeType, PracticeSession, Rating
    
    test_piece = PracticeNode(
        node_type=NodeType.PIECE,
        title="Test Sonata",
        measure_start="1",
        measure_end="100",
        target_tempo_bpm=120.0,
        current_step=-5
    )
    print(f"   Created: {test_piece.title}")
    print(f"   ID: {test_piece.id}")
    
    # Save it
    print("\n3. Saving to database...")
    db.save_node(test_piece)
    print("   ✓ Saved")
    
    # Load it back
    print("\n4. Loading from database...")
    loaded = db.load_node(test_piece.id)
    print(f"   ✓ Loaded: {loaded.title}")
    print(f"   Current step: {loaded.current_step}")
    
    # Save a practice session
    print("\n5. Saving practice session...")
    session = PracticeSession(
        node_id=test_piece.id,
        starting_step=4,
        achieved_step=-5,
        rating=Rating.GOOD,
        notes="First practice - found max tempo"
    )
    db.save_session(session)
    print("   ✓ Session saved")
    
    # Get sessions for this node
    print("\n6. Loading sessions...")
    sessions = db.get_sessions_for_node(test_piece.id)
    print(f"   Found {len(sessions)} session(s)")
    for s in sessions:
        print(f"   - {s.timestamp.strftime('%Y-%m-%d %H:%M')}: Step {s.achieved_step}, {s.rating.value if s.rating else 'unrated'}")
    
    # Get statistics
    print("\n7. Database statistics...")
    stats = db.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Get due nodes
    print("\n8. Checking due nodes...")
    due = db.get_due_nodes()
    print(f"   {len(due)} node(s) due for practice")
    
    print("\n" + "="*70)
    print("✓ ALL TESTS PASSED")
    print("="*70)
    print(f"\nYour practice data is stored at: {db.data_dir}")
    print("You can inspect the JSON files to see your data!")


if __name__ == "__main__":
    test_database()
