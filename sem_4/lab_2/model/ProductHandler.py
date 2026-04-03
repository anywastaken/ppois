import xml.sax

class ProductHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.products = []  
        self.current_data = {} 
        self.current_tag = ""
        self.content = ""

    def startElement(self, tag, attributes):
        self.current_tag = tag
        self.content = ""

    def characters(self, content):
        self.content += content.strip()

    def endElement(self, tag):
        if tag == "product":
            from model.Product import Product
            new_prod = Product(
                self.current_data.get("name", ""),
                self.current_data.get("manufacturer", ""),
                self.current_data.get("unp", 0),
                self.current_data.get("quantity", 0),
                self.current_data.get("address", "")
            )
            self.products.append(new_prod)
        elif tag != "inventory":
            self.current_data[tag] = self.content