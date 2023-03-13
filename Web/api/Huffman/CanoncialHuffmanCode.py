from api.Huffman.SelfDefineStructs import *

class CanonicalCode(object):
    def __init__(self, codelengths=None, tree=None, symbollimit=None):
        if codelengths is not None and tree is None and symbollimit is None:
            if len(codelengths) < 2:
                raise ValueError("At least 2 symbols needed")
            for code_lenght in codelengths:
                if code_lenght < 0:
                    raise ValueError("Illegal code length")

            codelens = sorted(codelengths, reverse=True)
            currentlevel = codelens[0]
            numnodesatlevel = 0
            for cl in codelens:
                if cl == 0:
                    break
                while cl < currentlevel:
                    if numnodesatlevel % 2 != 0:
                        raise ValueError("Under-full Huffman code tree")
                    numnodesatlevel //= 2
                    currentlevel -= 1
                numnodesatlevel += 1
            while cl < currentlevel:
                if numnodesatlevel % 2 != 0:
                    raise ValueError("Under-full Huffman code tree")
                numnodesatlevel //= 2
                currentlevel -= 1
            if numnodesatlevel < 1:
                raise ValueError("Under-full Huffman code tree")
            if numnodesatlevel > 1:
                raise ValueError("Over-full Huffman code tree")
            self.codelengths = list(codelengths)
        elif tree is not None and symbollimit is not None and codelengths is None:
            def build_code_lengths(node, depth):
                if isinstance(node, InternalNode):
                    build_code_lengths(node.leftchild, depth + 1)
                    build_code_lengths(node.rightchild, depth + 1)
                elif isinstance(node, Leaf):
                    if self.codelengths[node.symbol] != 0:
                        raise AssertionError("Symbol has more than one code")
                    if node.symbol >= len(self.codelengths):
                        raise ValueError("Symbol exceeds symbol limit")
                    self.codelengths[node.symbol] = depth
                else:
                    raise AssertionError("Illegal node type")
            if symbollimit < 2:
                raise ValueError("At least 2 symbols needed")
            self.codelengths = [0] * symbollimit
            build_code_lengths(tree.root, 0)
        else:
            raise ValueError("Invalid arguments")


    def get_symbol_limit(self):
        return len(self.codelengths)


    def get_code_length(self, symbol):
        if 0 <= symbol < len(self.codelengths):
            return self.codelengths[symbol]
        else:
            raise ValueError("Symbol out of range")

    def to_code_tree(self):
        nodes = []
        for i in range(max(self.codelengths), -1, -1): 
            assert len(nodes) % 2 == 0
            newnodes = []
            if i > 0:
                for (j, codelen) in enumerate(self.codelengths):
                    if codelen == i:
                        newnodes.append(Leaf(j))

            for j in range(0, len(nodes), 2):
                newnodes.append(InternalNode(nodes[j], nodes[j + 1]))
            nodes = newnodes
        assert len(nodes) == 1
        return CodeTree(nodes[0], len(self.codelengths))
