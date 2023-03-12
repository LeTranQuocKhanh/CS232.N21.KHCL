class Node(object):
  pass

#Node lá của cây(Code Tree) chứa giá trị của "symbol"
class Leaf(Node):
  def __init__(self, _symbol):
    if _symbol < 0:
      raise ValueError("symbol value need to be a non-nagative!")
      
    self.symbol = _symbol

#Node có ít nhất 1 con
class InternalNode(Node):
  def __init__(self, _leftChild, _rightChild):
    if not isinstance(_leftChild, Node) or not isinstance(_rightChild, Node):
      raise TypeError()
    self.leftchild = _leftChild
    self.rightchild = _rightChild
    

class CodeTree(object):
  #Xây dựng cây từ các node của cây được cho và giới hạn lại các "symbol"
  #Mỗi symbol trong cây phải có giá trị nhỏ hơn giá trị của "symbol" giới hạn
  def __init__(self, root, symbollimit):
        def build_code_list(node, prefix):
            if isinstance(node, InternalNode):
                build_code_list(node.leftchild, prefix + (0,))
                build_code_list(node.rightchild, prefix + (1,))
            elif isinstance(node, Leaf):
                if node.symbol >= symbollimit:
                    raise ValueError('Symbol exceeds symbol limit')
                if self.codes[node.symbol] is not None:
                    raise ValueError('Symbol has more than one code')
                self.codes[node.symbol] = prefix
            else:
                raise AssertionError('Illegal node type')
        if symbollimit < 2:
            raise ValueError("At least 2 symbols needed!")
        self.root = root
        #Với mỗi symbol được cấp một mã code để đại diện (lưu trữ) . Trả về giá trị "None", nếu "symbol" ko có code
        #VD: "5" có mã là 1001 -> code[5] = (1,0,0,1) (code[5] là 1 tuple)
        self.codes = [None] * symbollimit #Tạo một mảng null với số chiều bằng với "symbol limit number"
        build_code_list(root, ()) #Build mã(code) với dữ liệu phù hợp
  
  #Trả về Huffman code cho symbol dc cho - là 1 chuổi giá trị 0 và 1
  def get_code(self,symbol):
        if symbol<0:
            raise  ValueError("Illegal symbol")
        elif self.codes[symbol] is None:
            raise ValueError('No code for given symbol')
        else:
            return self.codes[symbol]
  
  #Trả về một chuỗi (string) đại diện cho cây và hàm này dùng để debug
  def __str__(self):
        def to_str(prefix, node):
            if isinstance(node, InternalNode):
                return to_str(prefix + "0", node.leftchild) + to_str(prefix + "0", node.rightchild)
            elif isinstance(node, Leaf):
                return "Code {}: Symbol {}\n".format(prefix, node.symbol)
            else:
                raise AssertionError("Illegal node type")

        return to_str("", self.root)
