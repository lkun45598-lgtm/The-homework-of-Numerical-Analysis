# SHUZHIFENXI（数值分析）作业/实验整理

这个仓库主要是数值分析相关的 Jupyter Notebook 练习（按周整理：`week01.ipynb` ~ `week12.ipynb`），包含插值、方程求根、线性代数数值计算、数值积分/微分、常微分方程数值解、SVD/特征值等内容。

本次整理的目标是**不改算法/不改解题思路**，仅做：

- 代码风格与结构的规范化（`isort + black` 自动格式化 Notebook 代码单元）
- 目录结构归档（notebooks/assets/data/scripts/tools）
- 补齐项目说明文档与依赖清单

## 目录结构

```
.
├─ notebooks/              # 主要内容：Jupyter Notebooks（week01.ipynb ~ week12.ipynb）
├─ assets/                 # 图片等静态资源（如 mandrill.jpg）
├─ data/                   # 数据文件（如 *.jld2）
└─ tools/                  # 项目工具脚本（如 Notebook 格式化）
```

## 环境与依赖

你说“跑代码用 conda 的 PyTorch 环境”，推荐直接把 Notebook 依赖装进你的 `pytorch` 环境里，并让 Jupyter 使用该环境的 kernel。

### 用 conda（推荐）

```bash
conda activate pytorch

# 安装本项目常用依赖（如已存在可跳过）
conda install -c conda-forge numpy matplotlib scipy sympy pillow scikit-image jupyterlab ipykernel
```

如果你更习惯用 pip，也可以在该环境里：

```bash
conda activate pytorch
pip install -r requirements.txt
```

为了保证 Jupyter 能选到这个环境，注册一个 kernel（只需一次）：

```bash
conda activate pytorch
python -m ipykernel install --user --name pytorch --display-name "Python (pytorch)"
```

之后启动 Jupyter：

```bash
conda activate pytorch
jupyter lab
```

打开 Notebook 后，在右上角 Kernel 选择 `Python (pytorch)` 即可。

### 用 venv（可选）

如果你不想用 conda，也可以用 venv：

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

如果你也想使用仓库内的格式化工具（格式化 `.ipynb` 代码单元）：

```bash
pip install -r requirements-dev.txt
```

## 运行方式

在仓库根目录启动 Jupyter：

```bash
jupyter lab
# 或
jupyter notebook
```

然后打开 `notebooks/` 下的 Notebook。

## Notebook 内容概览（按周）

- `notebooks/week01.ipynb`：误差/数值稳定性、简单计算题
- `notebooks/week02.ipynb`：多项式插值/范德蒙德矩阵求解等
- `notebooks/week03.ipynb`：范数、条件数、Hilbert/Vandermonde 等数值性质实验
- `notebooks/week04.ipynb`：数据拟合/最小二乘、Householder 等
- `notebooks/week05.ipynb`：非线性方程求根（牛顿法、弦截法、不动点迭代等）
- `notebooks/week06.ipynb`：非线性方程组（牛顿法、LM/阻尼/数值雅可比等）
- `notebooks/week07.ipynb`：插值（多项式/样条）、差分权重等
- `notebooks/week08.ipynb`：数值微分与数值积分（梯形/Simpson/自适应等）
- `notebooks/week09.ipynb`：ODE 初值问题（Euler/RK4/`solve_ivp` 等）
- `notebooks/week10.ipynb`：更系统的常微分方程数值方法与误差/步长实验
- `notebooks/week11.ipynb`：矩阵/SVD 与图像示例（依赖 `assets/mandrill.jpg`）
- `notebooks/week12.ipynb`：稀疏矩阵/特征值（幂迭代等）

## 代码格式化（可选）

仓库提供了一个小工具：对 Notebook 的每个代码单元执行 `isort + black`（会跳过包含 IPython magic 的单元）。

```bash
python tools/format_notebooks.py notebooks
```

只检查不写入：

```bash
python tools/format_notebooks.py notebooks --check
```
