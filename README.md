# Fermion Normal Ordering Tool Documentation

## 中文说明 | English Version

### 概述 | Overview
<mcsymbol name="FermionOperator" filename="fermion_normal_order.py" path="d:\share_files\Obsidian\Code\wick\fermion_normal_order.py" startline="4" type="class"></mcsymbol> 实现了费米子算符的正规排序功能，主要用于量子场论和凝聚态物理中的二次量子化计算。
The <mcsymbol name="FermionOperator" filename="fermion_normal_order.py" path="d:\share_files\Obsidian\Code\wick\fermion_normal_order.py" startline="4" type="class"></mcsymbol> implements normal ordering of fermion operators, primarily used for second quantization calculations in quantum field theory and condensed matter physics.

### 核心功能 | Key Features
1. **费米子算符表示 | Fermion Operator Representation**
   - <mcsymbol name="FermionOperator" filename="fermion_normal_order.py" path="d:\share_files\Obsidian\Code\wick\fermion_normal_order.py" startline="4" type="class"></mcsymbol> 类表示单个费米子算符
   The <mcsymbol name="FermionOperator" filename="fermion_normal_order.py" path="d:\share_files\Obsidian\Code\wick\fermion_normal_order.py" startline="4" type="class"></mcsymbol> class represents a single fermion operator
   - 支持产生(`c^\\dagger`)和湮灭(`c`)算符
   Supports creation (`c^\\dagger`) and annihilation (`c`) operators
   - 包含动量(`momentum`)和自旋(`spin`)指标
   Includes momentum (`momentum`) and spin (`spin`) indices

2. **输入解析 | Input Parsing**
   - <mcsymbol name="parse_fermion_string" filename="fermion_normal_order.py" path="d:\share_files\Obsidian\Code\wick\fermion_normal_order.py" startline="29" type="function"></mcsymbol>: 解析字符串格式的费米子算符
     Parses fermion operators in string format
   - <mcsymbol name="parse_fermion_objects" filename="fermion_normal_order.py" path="d:\share_files\Obsidian\Code\wick\fermion_normal_order.py" startline="50" type="function"></mcsymbol>: 解析元组列表格式的费米子算符
     Parses fermion operators in list-of-tuples format

3. **正规排序 | Normal Ordering**
   - <mcsymbol name="normal_order" filename="fermion_normal_order.py" path="d:\share_files\Obsidian\Code\wick\fermion_normal_order.py" startline="56" type="function"></mcsymbol>: 主排序函数，处理多自旋情况
     Main ordering function handling multiple spin cases
   - <mcsymbol name="_normal_order_single_spin" filename="fermion_normal_order.py" path="d:\share_files\Obsidian\Code\wick\fermion_normal_order.py" startline="84" type="function"></mcsymbol>: 处理单自旋情况的递归实现
     Recursive implementation for single spin case

4. **输出格式 | Output Formatting**
   - <mcsymbol name="to_latex" filename="fermion_normal_order.py" path="d:\share_files\Obsidian\Code\wick\fermion_normal_order.py" startline="147" type="function"></mcsymbol>: 将结果转换为LaTeX格式
     Converts results to LaTeX format
   - <mcsymbol name="normal_order_latex" filename="fermion_normal_order.py" path="d:\share_files\Obsidian\Code\wick\fermion_normal_order.py" startline="172" type="function"></mcsymbol>: 从字符串到LaTeX的完整流程

### 使用示例 | Usage Examples
```python
# 解析字符串
ops = parse_fermion_string("c^\\dagger_p1↑ c_p2↓")

# 正规排序
ordered = normal_order(ops)

# 输出LaTeX
print(to_latex(ordered))
```

```python
# 使用费米子算符列表
ops1 = [
        FermionOperator(True, 'p2', '↑'),
        FermionOperator(False, 'p1', '↑'),
        FermionOperator(False, 'p3', '↑'),
        FermionOperator(True, 'p3', '↑'),
        FermionOperator(True, 'p1', '↑'),
        FermionOperator(False, 'p2', '↑')
    ]
print("示例1: 单自旋")
print(f"原始算符: {ops1}")
print(f"正规排序: {to_latex(normal_order(ops1))}")
```
