from textnode import TextNode

def main():
    a = TextNode("Scott", "Brittany", "NoriGigi")
    b = TextNode("Scott", "Brittany", "oriGigi")
    print(a.__repr__())
    print(b.__repr__())
    print(b.__eq__(a))
    print(a.__eq__(b))

main()
