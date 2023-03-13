from api.Huffman.SelfDefineStructs import *

#Dùng để mô tả độ dài code của "symbol" . Độ dài = 0 có nghĩa là không có code cho "symbol" (Độ dài ở đây hiểu là bit biểu diễn cho "symbol" bằng cây HUFFMAN)
#Mã nhị phân của mỗi symbol được xây dựng từ thông tin độ dài 
#VD: CanonicalCode mô tả các chữ sau có độ dài như sau: A: 1  ; B = 3 ; C = 0 ; D = 2 ; E = 3
# Sau khi sắp xếp: A = 1 ; D= 2 ; B = 3 ; E = 3 ; C = 0
# Huffman code : A = 0 ; D = 10 ; B =110 ;  E= 111 ; C = None


class CanonicalCode(object):
    #Có 2 cách xây dựng CanonicalCode
    # - Cách 1: Sử dụng codelength ( độ dài mã)
    # + Xây dựng từ mảng codelength của symbol cho trước
    # + Codelength của symbol này được không âm. Bằng 0 thì có nghĩa là không có code cho symbol
    # + Các codelength được cho trước biểu diễn 1 cây huffman đầy đủ
    # - Cách 2: Xây dựng từ cây đã cho trước
    
    def __init__(self, codelengths=None, tree=None, symbollimit=None):
        if codelengths is not None and tree is None and symbollimit is None:
            #Kiểm tra hợp lệ
            if len(codelengths) < 2:
                raise ValueError("At least 2 symbols needed")
            for code_lenght in codelengths:
                if code_lenght < 0:
                    raise ValueError("Illegal code length")
            # Kiểm tra tính hợp lệ của cây
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
                    #Kiểm tra xem một symbol có nằm trong nhiều node lá hay không
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

    #Trả về symbol limit -> các symbol có giá trị từ 0 -> symbol_limit-1
    def get_symbol_limit(self):
        return len(self.codelengths)

    #Trả về độ dài của symbol đã cho Giá trị trả về >=0
    def get_code_length(self, symbol):
        if 0 <= symbol < len(self.codelengths):
            return self.codelengths[symbol]
        else:
            raise ValueError("Symbol out of range")

    def to_code_tree(self):
        nodes = []
        for i in range(max(self.codelengths), -1, -1): #Giảm dần qua độ dài mã
            assert len(nodes) % 2 == 0
            newnodes = []
            # Nếu độ dại >0 thêm lá cho symbol đó
            if i > 0:
                for (j, codelen) in enumerate(self.codelengths):
                    if codelen == i:
                        newnodes.append(Leaf(j))
            #Nối các node từ các lớp sâu hơn
            for j in range(0, len(nodes), 2):
                newnodes.append(InternalNode(nodes[j], nodes[j + 1]))
            nodes = newnodes
        assert len(nodes) == 1
        return CodeTree(nodes[0], len(self.codelengths))
