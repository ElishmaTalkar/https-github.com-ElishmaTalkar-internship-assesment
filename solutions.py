import heapq
from typing import List, Tuple

# ─────────────────────────────────────────────
# Problem 1: LRU Cache Implementation
# ─────────────────────────────────────────────

"""
LOGIC AND APPROACH:
To achieve O(1) performance for both 'get' and 'put' operations, I chose a combination 
of a Hash Map (Python dictionary) and a Doubly Linked List.

1. Hash Map: Provides O(1) time complexity for looking up a value by its key. It stores 
   references to the nodes in the doubly linked list.
2. Doubly Linked List: Maintains the order of elements based on their usage. 
   - When an element is accessed or added, it is moved to the "head" (Most Recently Used).
   - If the cache exceeds capacity, the element at the "tail" (Least Recently Used) 
     can be removed in O(1) time because we have direct 'prev' and 'next' pointers.
"""

class Node:
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        # Sentinel nodes to simplify boundary logic
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        """Removes a node from the doubly linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: Node):
        """Adds a node immediately after the head sentinel (MRU position)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add_to_front(new_node)
        
        if len(self.cache) > self.capacity:
            # Evict the least recently used (node before tail sentinel)
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]


# ─────────────────────────────────────────────
# Problem 2: Event Scheduler
# ─────────────────────────────────────────────

"""
LOGIC AND APPROACH:
The algorithmic logic for calculating the minimum rooms required is based on a 
Greedy approach using a Min-Heap.

1. Sort: We first sort all events by their start times to process them chronologically.
2. Track End Times: We use a Min-Heap to store the end times of ongoing meetings. 
   Each element in the heap effectively represents a room, with the root being 
   the room that will become free earliest.
3. Allocation Logic:
   - For each new event, if its start time is greater than or equal to the earliest 
     end time (heap root), we can "reuse" that room. We pop the old end time and 
     push the current event's end time.
   - If the start time is earlier, the current room is still busy, so we must 
     allocate a new room (simply push the new end time onto the heap).
4. Result: The final size of the heap is the minimum number of rooms needed.
"""

def can_attend_all(events: List[Tuple[int, int]]) -> bool:
    if not events:
        return True
    
    # Sort by start time
    sorted_events = sorted(events, key=lambda e: e[0])
    
    for i in range(1, len(sorted_events)):
        # Overlap if current start < previous end (adjacent is OK)
        if sorted_events[i][0] < sorted_events[i - 1][1]:
            return False
    return True

def min_rooms_required(events: List[Tuple[int, int]]) -> int:
    if not events:
        return 0
    
    # Sort events by start time
    sorted_events = sorted(events, key=lambda e: e[0])
    
    # Min-heap to store meeting end times
    rooms_heap = []
    
    for start, end in sorted_events:
        # If the earliest ending room is free, reuse it
        if rooms_heap and rooms_heap[0] <= start:
            heapq.heappop(rooms_heap)
            
        heapq.heappush(rooms_heap, end)
        
    return len(rooms_heap)


# ─────────────────────────────────────────────
# Test Demonstrations
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("--- Problem 1: LRU Cache ---")
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    print(f"Get 1: {cache.get(1)}") # 10
    cache.put(3, 30)                # Evicts 2
    print(f"Get 2: {cache.get(2)}") # -1
    
    print("\n--- Problem 2: Event Scheduler ---")
    test_events = [(9, 10), (10, 11), (11, 12)]
    print(f"Can attend {test_events}: {can_attend_all(test_events)}") # True
    
    room_test = [(9, 14), (9, 12), (10, 13), (12, 14)]
    print(f"Min rooms for {room_test}: {min_rooms_required(room_test)}") # 3
