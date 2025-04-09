from importlib.machinery import PathFinder
import re
from typing import List, Tuple, Union

class FermionOperator:
    """
    费米子算符类，表示单个费米子算符
    """
    def __init__(self, is_creation: bool, momentum: Union[str, 'Momentum'], spin: Union[str, 'Spin']):
        self.is_creation = is_creation  # 是否为产生算符
        self.momentum = str(momentum) if not isinstance(momentum, str) else momentum  # 动量指标
        self.spin = str(spin) if not isinstance(spin, str) else spin  # 自旋指标
    
    def __repr__(self):
        operator = 'c^\\dagger' if self.is_creation else 'c'
        return f"{operator}_{{{self.momentum},{self.spin}}}"
    
    def to_latex(self) -> str:
        """转换为LaTeX格式"""
        if self.is_creation:
            return f"c^{{\\dagger}}_{{{self.momentum},{self.spin}}}"
        else:
            return f"c_{{{self.momentum},{self.spin}}}"


def parse_fermion_string(expr: str) -> List[FermionOperator]:
    """
    解析费米子算符字符串
    输入格式示例: "c_p1↑ c^\dagger_p2↓ c_p3↑"
    """
    pattern = r"(c\^\\dagger|c)_\{(\w+),(↑|↓)\}|(c\^\\dagger|c)_(\w+)(↑|↓)"
    operators = []
    
    for match in re.finditer(pattern, expr):
        if match.group(1):  # 格式1: c^{\dagger}_{p,↑} 或 c_{p,↑}
            is_creation = match.group(1) == 'c^\\dagger'
            momentum = match.group(2)
            spin = match.group(3)
        else:  # 格式2: c^\dagger_p↑ 或 c_p↑
            is_creation = match.group(4) == 'c^\\dagger'
            momentum = match.group(5)
            spin = match.group(6)
        
        operators.append(FermionOperator(is_creation, momentum, spin))
    
    return operators


def parse_fermion_objects(operators: List[Tuple[bool, Union[str, 'Momentum'], Union[str, 'Spin']]]) -> List[FermionOperator]:
    """
    解析费米子算符对象列表
    输入格式示例: [(False, 'p1', '↑'), (True, 'p2', '↓')]
    """
    return [FermionOperator(is_creation, momentum, spin) for is_creation, momentum, spin in operators]


def normal_order(operators: List[FermionOperator]) -> List[Tuple[int, List[FermionOperator]]]:
    """
    递归实现费米子算符串的正规排序
    返回: [(系数, 算符串), ...]
    """
    if len(operators) <= 1:
        return [(1, operators)]
    
    # 按自旋分类
    spin_groups = {}
    for op in operators:
        if op.spin not in spin_groups:
            spin_groups[op.spin] = []
        spin_groups[op.spin].append(op)
    
    # 如果所有算符自旋相同
    if len(spin_groups) == 1:
        return _normal_order_single_spin(list(spin_groups.values())[0])
    
    # 对不同自旋的算符串分别处理
    results = []
    for spin, group in spin_groups.items():
        sub_results = _normal_order_single_spin(group)
        if not results:
            results = sub_results
        else:
            # 合并不同自旋的结果
            new_results = []
            for coeff1, ops1 in results:
                for coeff2, ops2 in sub_results:
                    new_results.append((coeff1 * coeff2, ops1 + ops2))
            results = new_results
    
    return results


def _normal_order_single_spin(operators: List[FermionOperator]) -> List[Tuple[int, List[FermionOperator]]]:
    """处理单一自旋的算符串"""
    print(f"输入算符: {operators}")
    if len(operators) <= 1:
        # 保留原始系数
        result = [(operators[0].coefficient if hasattr(operators[0], 'coefficient') else 1, operators)]
        print(f"返回结果: {result}")
        return result
    
    last_op = operators[-1]
    if not last_op.is_creation:  # 如果是湮灭算符，跳过这个递归
        remaining_ops = operators[:-1]  # 扣除掉倒序第一个后剩下的算符
        if remaining_ops:
            sub_results = _normal_order_single_spin(remaining_ops)
            # 将扣除的算符加回结果中，并处理系数相乘
            return [(coeff * (last_op.coefficient if hasattr(last_op, 'coefficient') else 1), ops + [last_op]) for coeff, ops in sub_results]
        else:
            # 保留原始系数
            return [(last_op.coefficient if hasattr(last_op, 'coefficient') else 1, operators)]
    
    results = []
    # 倒序遍历湮灭算符
    print(operators)
 
    for i in reversed(range(len(operators))):

        current_op = operators[i]
        print(i,current_op,operators)
        if not current_op.is_creation:
            # 直接处理i+1位置的算符
            next_op = operators[i+1]
            
            delta = 1 if (current_op.momentum == next_op.momentum 
                        and current_op.is_creation != next_op.is_creation) else 0
            
            if delta != 0:

                remaining = operators[:i] + operators[i+2:]
                if remaining:
                    sub_results = _normal_order_single_spin(remaining)
                    results.extend([( coeff, ops) for coeff, ops in sub_results])
                else:
                    results.append((delta, []))

            
            # 交换项处理
            new_ops = operators[:i] + [next_op]+ [current_op] + operators[i+2:]
            sub_results = _normal_order_single_spin(new_ops)
            results.extend([(-1 * coeff, ops ) for coeff, ops in sub_results])
            
            # 处理完成后立即终止循环
            print(f"break 当前i={i}处理结果: {results}")
            break
        
        print(f"当前i={i}处理结果: {results}")
    
    # 如果没有找到湮灭算符，直接返回原始算符序列
    if not results:
        return [(1, operators)]
    
    return results


def to_latex(results: List[Tuple[int, List[FermionOperator]]]) -> str:
    """将排序结果转换为LaTeX格式"""
    if not results:
        return "0"
    
    latex_strs = []
    for coeff, ops in results:
        if coeff == 0:
            continue
            
        if not ops:
            term = str(coeff)
        else:
            if coeff == 1:
                term = " ".join(op.to_latex() for op in ops)
            elif coeff == -1:
                term = "-" + " ".join(op.to_latex() for op in ops)
            else:
                term = f"{coeff} " + " ".join(op.to_latex() for op in ops)
        
        latex_strs.append(term)
    
    return " + ".join(latex_strs).replace(" + -", " - ")


def normal_order_latex(expr: str) -> str:
    """将费米子算符字符串转换为正规排序的LaTeX表达式"""
    operators = parse_fermion_string(expr)
    results = normal_order(operators)
    return to_latex(results)


# 示例用法
#if __name__ == "__main__":
    # 示例1: 使用FermionOperator类直接创建实例
    #ops1 = [
        #FermionOperator(True, 'p2', '↑'),
        #FermionOperator(False, 'p1', '↑'),
        #FermionOperator(False, 'p3', '↑'),
        #FermionOperator(True, 'p3', '↑'),
        #FermionOperator(True, 'p1', '↑'),
        #FermionOperator(False, 'p2', '↑')

    #]
    #print("示例1: 单自旋")
    #print(f"原始算符: {ops1}")
    #print(f"正规排序: {to_latex(normal_order(ops1))}")
