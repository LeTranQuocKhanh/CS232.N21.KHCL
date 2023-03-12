from api.Huffman.SelfDefineStructs import *

class HuffmanEncoder(object):
    # Xây dựng bộ mã hóa Huffman dựa trên luồng đầu ra bit đã cho
    def __init__(self, _bitout):
        # Luồng đầu ra bit cơ bản
        self.output = _bitout
        # Giá trị được cho phải phù hợp
        # value before calling write()
        # Cây có thể được thay đổi sau mỗi symbol được encoder, miễn là encoder và decoder có cùng một cây
        self.codetree = None  # Định nghĩa

    # Encodes symbol được cho và viết Huffman-coded output stream
    def write(self, symbol):
        if not isinstance(self.codetree, CodeTree):
            raise ValueError('Current code tree is invalid')
        bits = self.codetree.get_code(symbol)
        for bit in bits:
            self.output.write(bit)
          
# Đọc từ luồng bit được mã hóa Huffman và giải mã "symbols"
class HuffmanDecoder(object):
    def __init__(self, _bitin):
        # Luồng đầu vào bit cơ bản
        self.input = _bitin
        self.codetree = None

    def read(self):
        if not isinstance(self.codetree, CodeTree):
            raise ValueError('Invalid current code tree')
        currentnode = self.codetree.root
        while True:
            temp = self.input.read_no_eof()
            if temp == 0:
                nextnode = currentnode.leftchild
            elif temp == 1:
                nextnode = currentnode.rightchild
            else:
                raise AssertionError('Invalid value from read_no_eof()')
            if isinstance(nextnode, Leaf):
                return nextnode.symbol
            elif isinstance(nextnode, InternalNode):
                currentnode = nextnode
            else:
                raise AssertionError('Illegal node type')    
