"""Trie implementation with configurable memory/time trade-off.

This module provides two abstractions:
- TrieNode: internal node type
- Trie: wrapper that exposes `insert`, `search`, and `delete` with a
  `store_skus_in_nodes` option.

If `store_skus_in_nodes=True` then every node stores the set of SKUs
of all products that share that prefix (fast searches, higher memory).
If False, only end-of-word nodes keep SKUs and `search(prefix)` collects
SKUs by traversing the subtree (lower memory, slower searches).
"""

from typing import Set, Dict


class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False
        # Only used in modes that keep SKUs at nodes or to store at end nodes
        self.skus: Set[str] = set()


class Trie:
    def __init__(self, store_skus_in_nodes: bool = True):
        self.root = TrieNode()
        self.store_skus_in_nodes = store_skus_in_nodes

    def insert(self, word: str, sku: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            if self.store_skus_in_nodes:
                node.skus.add(sku)
        node.is_end_of_word = True
        # Always add sku to end node to support subtree-collection mode
        node.skus.add(sku)

    def _find_node(self, prefix: str):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def search(self, prefix: str) -> Set[str]:
        """Return set of SKUs matching the prefix.

        Complexity:
        - If store_skus_in_nodes=True: O(m) to walk prefix, return stored set
        - If False: O(m) to walk prefix + O(k) to traverse subtree where k is
          number of nodes in subtree (may be proportional to matching words)
        """
        node = self._find_node(prefix)
        if not node:
            return set()
        if self.store_skus_in_nodes:
            return set(node.skus)
        # collect SKUs by traversing subtree
        result: Set[str] = set()

        stack = [node]
        while stack:
            n = stack.pop()
            if n.is_end_of_word:
                result.update(n.skus)
            for child in n.children.values():
                stack.append(child)
        return result

    def delete(self, word: str, sku: str):
        node = self.root
        nodes_stack = []
        for char in word:
            if char not in node.children:
                return  # word not found
            node = node.children[char]
            nodes_stack.append(node)

        # remove sku from end node
        node.skus.discard(sku)
        node.is_end_of_word = node.is_end_of_word and bool(node.skus)

        if self.store_skus_in_nodes:
            # remove sku from all prefix nodes encountered
            for n in nodes_stack:
                n.skus.discard(sku)