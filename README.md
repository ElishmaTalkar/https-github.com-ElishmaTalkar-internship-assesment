# Assignment: Data Structures & Systems Design (SE Intern)

This repository contains the completed assessment for the Software Engineering Intern position. It covers LRU Cache implementation, Event Scheduling logic, and a detailed systems analysis.

## 📂 Project Structure
- `solutions.py`: Contains the Python implementation for both Problem 1 (LRU Cache) and Problem 2 (Event Scheduler), including block comments for logic and approach.

---

## 📝 Final Discussion & Analysis

### 1. Time & Space Complexity Analysis

| Function | Time Complexity | Space Complexity | Explanation |
| :--- | :--- | :--- | :--- |
| **LRUCache.get** | $O(1)$ | $O(1)$ | Direct hash map lookup and constant-time pointer updates. |
| **LRUCache.put** | $O(1)$ | $O(1)$ | Hash map insertion/deletion and linked list pointer updates. |
| **can_attend_all** | $O(N \log N)$ | $O(N)$ | Sorting $N$ events takes $O(N \log N)$; linear scan takes $O(N)$. |
| **min_rooms_required** | $O(N \log N)$ | $O(N)$ | $O(N \log N)$ for sorting and $N$ heap operations ($O(\log N)$ each). |

**Note**: The LRU Cache as a whole maintains $O(C)$ space complexity, where $C$ is the total capacity.

### 2. Trade-offs: Why Hash Map + Doubly Linked List?
Implementing an LRU cache requires keeping track of the order of usage while maintaining fast access.
- **Why not just a List?** Searching for an item is $O(N)$, and moving an item to the front involves shifting $O(N)$ elements.
- **Why not just a Hash Map?** Hash maps do not inherently preserve order; we wouldn't know which item was least recently used.
- **The Synergy**: The Hash Map provides the speed of access ($O(1)$), while the Doubly Linked List provides the speed of reordering ($O(1)$) without shifting elements.

### 3. Future Proofing: Specific Room Numbers
To modify the scheduler to assign specific room labels (e.g., "Room A", "Room B"):
1.  **Maintain a Pool**: Create a heap or queue of available room identifiers.
2.  **Assign on Start**: Instead of just storing end times, the heap in `min_rooms_required` would store tuples: `(end_time, assigned_room_id)`.
3.  **Release on End**: When a meeting ends, its room ID is popped from the heap and returned to the pool of available rooms to be reused by the next overlapping event.

### 4. Concurrency: Thread-Safe LRU Cache
To make the LRU Cache thread-safe in a multi-threaded environment:
- **Locking Mechanism**: Introduce a `threading.Lock` (or `RLock` if recursion is needed) as a member of the `LRUCache` class.
- **Critical Sections**: All modifications to the hash map and the doubly linked list (inside `get` and `put`) must happen within a `with self.lock:` block.
- **Considerations**: While simple locks ensure safety, they may become a bottleneck under high contention. For high-throughput systems, techniques like **fine-grained locking** or **Read-Write locks** could be used to allow concurrent reads while serializing writes.
