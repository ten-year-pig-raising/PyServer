# 这个映射关系，是用FontCreator打开美团的字体找到的
ORM = {
    "&#xf74c;": "0",
    "&#xe01c;": "1",
    "&#xf03d;": "2",
    "&#xe18a;": "3",
    "&#xf4ff;": "4",
    "&#xe90d;": "5",
    "&#xf615;": "6",
    "&#xed05;": "7",
    "&#xf808;": "8",
    "&#xf23a;": "9",

    "&#xea11;": "0",
    "&#xe9f1;": "1",
    "&#xf0ad;": "2",
    "&#xf5b6;": "3",
    "&#xee75;": "4",
    "&#xeb69;": "5",
    "&#xf09c;": "6",
    "&#xe283;": "7",
    "&#xe2ce;": "8",
    "&#xe678;": "9",
}


def decode_num(org_str):
    """解码美团数字"""
    if not org_str or org_str == '':
        return org_str
    decode_str = org_str
    for key, value in ORM.items():
        decode_str = decode_str.replace(key, value)
    return decode_str


if __name__ == '__main__':
    print(decode_num(
        '湖南省长沙市天心区新联路&#xe18a;&#xe01c;&#xf23a;号湘水熙园&#xe01c;、&#xe18a;商业层&#xf74c;&#xf4ff;、&#xf74c;&#xe90d;号'))
    print(decode_num(
        "长沙市天心区黑石铺街道雀园路&#xeb69;&#xf09c;&#xe2ce;号创谷产业园B&#xe9f1;栋&#xe9f1;&#xe9f1;&#xf0ad;号"))
    print(decode_num("德思勤城市广场购物中心B&#xe9f1;层&#xf0ad;&#xea11;号（谭城故事美食广场）"))
    print(decode_num(
        "湖南省长沙市天心区湘府西路&#xf0ad;&#xe678;&#xe678;号香芙嘉园&#xe9f1;栋&#xe9f1;&#xe678;、&#xf0ad;&#xea11;号."))
    print(decode_num("湖南省长沙市天心区青园小区B&#xee75;&#xea11;栋五单元"))
    print(decode_num("槐树塘路&#xe678;&#xe678;号现代雅境写字楼临街商铺B&#xe9f1;号"))
    print(decode_num(
        "天心区雀园路&#xeb69;&#xf09c;&#xe2ce;号创谷产业园A&#xf0ad;栋一层&#xe9f1;&#xea11;&#xf0ad;-&#xe9f1;&#xea11;&#xf5b6;号"))
    print(decode_num("湖南省长沙市天心区青园小区B&#xeb43;&#x2f2a;栋五单元"))
