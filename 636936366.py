"""
https://www.zhihu.com/question/636936366
Licence: WTFPL
"""

import random
import sys
from operator import add, mul, sub, truediv
from string import ascii_letters, digits
from typing import Callable, LiteralString, NoReturn, TypeAlias

OPERATORS: dict[str, Callable] = {"+": add, "-": sub, "*": mul, "/": truediv}
SEP_LINE: LiteralString = "=" * 20
CheckFunc: TypeAlias = Callable[[str], bool]


def _generate_verify_code(length: int) -> str:
    assert length in {4, 5}
    return "".join(random.choices(ascii_letters + digits, k=length))


def _get_input(prompt: str, *, rules: CheckFunc | list[CheckFunc]) -> str:
    if not isinstance(rules, list):
        rules = [rules]

    while True:
        v = input(prompt)
        if all(r(v) for r in rules):
            return v
        print("无效输入，请重试")


def _is_number(x: str) -> bool:
    try:
        float(x)
        return True
    except:
        return False


class Functions:
    @staticmethod
    def verify_code() -> None:
        """生成验证码"""
        l: str = _get_input(
            "请输入要生成验证码的位数(4/5): ",
            rules=lambda x: len(x) == 1 and x.isdigit() and int(x) in {4, 5},
        )
        print("验证码:", _generate_verify_code(int(l)))

    @staticmethod
    def calculator() -> None:
        """计算器"""
        v1 = float(_get_input("请输入第一个数: ", rules=_is_number))
        v2 = float(_get_input("请输入第二个数: ", rules=_is_number))
        op = _get_input(
            f"请输入运算符({''.join(OPERATORS.keys())}):",
            rules=lambda x: x in OPERATORS.keys(),
        )
        op_func = OPERATORS[op]
        try:
            print(f"{v1} {op} {v2} = {op_func(v1,v2)}")
        except ZeroDivisionError:
            print("除数不能为0")
        except:
            print("数学错误")

    @staticmethod
    def quit() -> NoReturn:
        """退出程序"""
        sys.exit()

    menu: list[Callable] = [verify_code, calculator, quit]

    @classmethod
    def print_menu(cls) -> None:
        for idx, func in enumerate(cls.menu):
            print(f"{idx}: {func.__doc__}")

    @classmethod
    def select_menu(cls) -> None:
        choice: str = _get_input(
            "请选择功能 (输入对应序号): ",
            rules=lambda x: x.isdigit() and 0 <= int(x) <= len(cls.menu),
        )

        cls.menu[int(choice)]()
        print(SEP_LINE)


def main() -> NoReturn:
    while True:
        Functions.print_menu()
        Functions.select_menu()


if __name__ == "__main__":
    main()
