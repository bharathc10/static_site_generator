
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    
    def __repr__(self):
        return (
            f"HTMLNode("
            f"tag = {self.tag!r}, "
            f"value = {self.value!r}, "
            f"children = {self.children!r}, "
            f"props = {self.props!r}"
            f")"
        )
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag = tag, value = value, props = props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return (
            f"HTMLNode("
            f"tag = {self.tag!r}, "
            f"value = {self.value!r}, "
            f"props = {self.props!r}"
            f")"
        )