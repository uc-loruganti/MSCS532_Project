# TrieNode implementation for product name prefix search
# Time complexity : 
#   - insert: O(m) where m is the length of the word
#   - search: O(m) where m is the length of the prefix
#   - delete: O(m) where m is the length of the word
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False
        self.skus: set[str] = set()  # Set of SKUs for products matching this prefix

    def insert(self, word: str, sku: str):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.skus.add(sku)  # Add SKU to the set at each prefix node
        node.is_end_of_word = True

    def search(self, prefix: str) -> set[str]:
        node = self
        for char in prefix:
            if char not in node.children:
                return set()  # No products match this prefix
            node = node.children[char]
        return node.skus  # Return all SKUs matching this prefix
    
    def delete(self, word: str, sku: str):
        node = self
        for char in word:
            if char not in node.children:
                return  # Word not found
            node = node.children[char]
            node.skus.discard(sku)  # Remove SKU from the set at each prefix node 