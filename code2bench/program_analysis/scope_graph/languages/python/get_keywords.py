import keyword
import builtins

# 获取 Python 的所有关键字
python_keywords = set(keyword.kwlist)
# 获取 Python 的所有内置函数和异常
builtin_functions = set(dir(builtins))
# print(builtin_functions)
# print(python_keywords)

keyword_and_builtin = {
    "keyword_and_builtin": list(python_keywords.union(builtin_functions))
}

from code2bench.program_analysis.utils import save_json
save_json("keyword_and_builtin.json", keyword_and_builtin)
