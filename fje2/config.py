# 每一行为一种配置
# 第一个标识中间节点，第二个标识叶子节点
unicode_icons = [
    ['U+0NAN', 'U+0NAN'],
    ['U+2662', 'U+2664'],
    ['U+2655', 'U+2654'],
    ['U+2746', 'U+2729'],
    ['U+2193', 'U+2192'],

]

# 创建一个新列表来存储实际的 Unicode 字符
icon_family = []

# 遍历 icon_family 列表并将每个编码转换为 Unicode 字符
for sublist in unicode_icons:
    unicode_sublist = []
    for code in sublist:
        if code == 'U+0NAN':
            unicode_char = ''
        else:
            try:
                unicode_char = chr(int(code[2:], 16))
            except ValueError:
                print(f"Invalid Unicode code: {code}")
        unicode_sublist.append(unicode_char)
    icon_family.append(unicode_sublist)
