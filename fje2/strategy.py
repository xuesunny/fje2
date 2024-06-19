# Abstract Product for Style
from abc import ABC, abstractmethod
from config import icon_family

# New class for representing data nodes


class DataNode:
    def __init__(self, name, children=None, index=0, total=0, icon=""):
        self.name = name
        self.pos = index
        self.total = total
        self.icon = icon
        self.children = children or []


class Strategy(ABC):
    @abstractmethod
    def display(self, data_node=None, prefix="", max_width=40, is_last=True):
        pass


# Concrete Products for Tree and Rectangle Styles
class TreeStrategy(Strategy):
    def __init__(self):
        pass

    def display(self, data_node=None, max_width=40, prefix="", is_last=True):
        # Print the current node without prefix for the first one
        if prefix or data_node.name != "root":
            print(prefix + ("└── " if is_last else "├── ") + data_node.icon + " " + data_node.name)

        # Prepare the prefix for children
        if data_node.name != "root":  # 根节点不加前缀
            prefix += "     " if is_last else "│    "
            if data_node.icon != "":
                prefix += " "

        # Display the children
        for i, child in enumerate(data_node.children):
            is_last_child = i == len(data_node.children) - 1
            self.display(child, max_width, prefix, is_last_child)


class RectangleStrategy(Strategy):
    def __init__(self):
        pass

    def display(self, data_node=None, max_width=40, prefix="", is_last=True):
        last = 0 == len(data_node.children) - 1
        if data_node.name != "root":
            if data_node.pos == 1:
                line = f"┌─ {data_node.icon} {data_node.name} {'─' * (max_width - len(data_node.name))}─┐"
            elif data_node.pos == data_node.total - 1:
                line = f"└─ {data_node.icon} {data_node.name} {'─' * (max_width - len(data_node.name))}─┘"
            else:
                line = f"├─ {data_node.icon} {data_node.name} {'─' * (max_width - len(data_node.name))}─┤"
            print(f"{prefix}{line}")

            # Display the children
        for i, child in enumerate(data_node.children):
            last = i == len(data_node.children) - 1
            if data_node.name != "root" and child.pos != child.total - 1:
                new_prefix = prefix + "│   "
                if data_node.icon != "":
                    new_prefix += " "
            elif child.pos == child.total - 1:
                new_prefix = prefix + "└───"
                if data_node.icon != "":
                    new_prefix += "─"
            else:
                new_prefix = ""
            self.display(child, max_width - len(new_prefix) + len(prefix), new_prefix, last)


# 样式上下文类
class StyleContext:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy

    def display(self, data_node: DataNode):
        self._strategy.display(data_node, 40, "")
