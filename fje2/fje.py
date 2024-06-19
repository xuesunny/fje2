import json
import argparse
from strategy import *
from config import *


class Iterator:
    def __init__(self):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass


class JSONIterator(Iterator):
    def __init__(self, root):
        self.stack = [(root, -1)]  # 一个栈，一个数据含有两个元素（节点，再数组的位置）

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            data_node, index = self.stack.pop()
            if index == -1:  # 新加入的节点
                self.stack.append((data_node, 0))
                return data_node
            elif index < len(data_node.children):
                self.stack.append((data_node, index + 1))
                child = data_node.children[index]
                self.stack.append((child, -1))
                return child
        raise StopIteration


# 讲json输入转为节点
def convert_to_data_node(name, obj, index, total, icon_num):
    pos = index+1
    if isinstance(obj, dict):
        children = []
        count = 1
        for key, value in obj.items():
            num, children_node = convert_to_data_node(key, value, pos, total, icon_num)
            children.append(children_node)
            pos = pos + num
            count = count + num
        return count, DataNode(name, children, index, total,icon_family[icon_num][0])
    elif obj is not None:
        final_name = name + ":" + obj
        return 1, DataNode(final_name, None, index, total, icon_family[icon_num][1])
    else:
        return 1, DataNode(name, None, index, total, icon_family[icon_num][1])


# 获取节点总数
def get_total(obj):
    if isinstance(obj, dict):
        count = 1
        for key, value in obj.items():
            num = get_total(value)
            count = count + num
        return count
    else:
        return 1


# Main Function
def main():
    parser = argparse.ArgumentParser(description='Funny JSON Explorer (FJE)')
    parser.add_argument('-f', '--file', required=True, help='JSON file')
    parser.add_argument('-s', '--style', choices=['tree', 'rectangle'], required=True, help='style')
    parser.add_argument('-i', '--icon', choices=list(map(str, range(len(icon_family)))), required=True,help='Icon')
    args = parser.parse_args()
    # Client Code
    with open(args.file, "r", encoding='utf-8') as file:
        input_json = file.read()

    # Parse the JSON input
    input_obj = json.loads(input_json)

    # Convert the parsed JSON object to DataNode
    total = get_total(input_obj)
    icon_num = int(args.icon)
    num_, data = convert_to_data_node("root", input_obj,0, total, icon_num)
    # print(input_obj)
    if args.style == 'tree':
        my_strategy = TreeStrategy()

    elif args.style == 'rectangle':
        my_strategy = RectangleStrategy()

    context = StyleContext(my_strategy)
    context.set_strategy(my_strategy)
    context.display(data)

if __name__ == "__main__":
    main()