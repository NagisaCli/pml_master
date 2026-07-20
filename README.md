# AVEVA E3D AI Agent 智能建模系统

![AVEVA E3D AI Agent](https://img.shields.io/badge/AVEVA%20E3D-Mk3.1.11.0-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.11%2B-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

`e3d_agent` 是一套专为 **AVEVA E3D (Everything 3D Design Mk3.1.11.0)** 打造的智能 AI 建模编排与 PML (Plant Management Language) 代码生成系统。系统支持将**自然语言描述**、**PDF P&ID 图纸**及 **SVG 系统图**一键解析并自动生成符合 E3D 严苛规范的 PML1 宏脚本。

---

## 目录
- [核心特性](#核心特性)
- [系统架构](#系统架构)
- [E3D 大模型建模核心规范](#e3d-大模型建模核心规范)
- [快速开始](#快速开始)
- [使用指南 (CLI)](#使用指南-cli)
- [预置复杂 3D 模型生成器](#预置复杂-3d-模型生成器)
- [项目结构](#项目结构)
- [许可证](#许可证)

---

## 核心特性

- **多模态输入解析**：支持自然语言描述、PDF P&ID 管道仪表图、SVG 工艺图纸自动识别解析。
- **100% 规范化 PML1 生成**：严格遵循 E3D Mk3.1 实机验证规则，杜绝 PML2 语法报错、基本体变形与坐标轴向飘移。
- **高面数防卡死控制**：自动注入 `SUSPEND` / `RESUME` 渲染挂起与恢复控制指令，支持上万至 10 万级基本体宏极速无卡顿加载。
- **自适应记忆与错误恢复**：内置 `MemoryStore` 数据库，自动收集 E3D 运行错误与历史反馈，实现自我优化迭代。
- **丰富工业/复杂构件模板库**：预置精馏塔、航空发动机、工业电机、大型造纸机、汽车模型及十万级成套工厂 3D 模型生成器。

---

## 系统架构

```mermaid
graph TD
    A[输入: 自然语言 / PDF / SVG] --> B[Drawing Parser / NL Parser]
    B --> C[Design Intent 意图对象]
    C --> D[PML Knowledge Base 知识库检索]
    D --> E[PML Generator 生成引擎]
    E --> F[PML1 宏脚本 (.pml)]
    F --> G[E3D Interface 执行/加载]
    G --> H[Memory Store 记忆库/错误自愈]
```

- **`drawing_parser`**：负责提取图纸或自然语言中的设备节点、管道连接与几何尺寸。
- **`pml_knowledge`**：提供 PML 基本体规范、工业设备标准与尺寸推算数学模型。
- **`pml_generator`**：依照 `EQUI -> SUBE -> Primitive` 三层架构构造 PML 代码。
- **`e3d_interface`**：负责与 AVEVA E3D 进行命令行交互或宏文件挂载。
- **`memory`**：存储生成历史、解析性能统计与错误自愈记录。

---

## E3D 大模型建模核心规范

为确保生成的 PML 宏在 E3D 3.1 中 100% 正确加载，系统强制执行以下铁律（详见 [AGENTS.md](file:///D:/AVEVA/Projects/E3D3.1/e3d_agent/AGENTS.md)）：

1. **基本体定位顺序**：`NEW CYLI` 等基本体必须**先指定 `ORI` 方向，后指定 `POS` 位置**，防止局部坐标轴旋转导致空间绝对坐标飘移。
2. **三层节点结构**：严格遵循 `NEW EQUI /设备` -> `NEW SUBE /子系统` -> `NEW BOX/CYLI/CONE/DISH` 基本体层级。
3. **禁用 PML2 语法**：0 次出现 `!!Alert`、`COLLECT`、`!var =` 等会导致 E3D 加载崩溃的 PML2 关键字。
4. **渲染保护控制**：大脚本开头包含 `SUSPEND`，末尾包含 `RESUME` & `RECREATE`。

---

## 快速开始

### 环境依赖
- **Python**: 3.11+
- **AVEVA E3D**: Design Mk3.1.11.0 (可选，仅在需实机加载执行时调用)

### 环境配置与激活
```bash
# 进入工作目录
cd D:\AVEVA\Projects\E3D3.1

# 激活虚拟环境 (Windows)
.venv\Scripts\activate
```

---

## 使用指南 (CLI)

### 1. 从自然语言生成 E3D 模型
```bash
python -m e3d_agent.agent "在 AREA_100 创建一台直径2m高5m的储罐 T-101"
```

### 2. 解析 SVG / PDF 图纸并生成 PML
```bash
python -m e3d_agent.agent --svg "AvevaMarineSample/amsdia/process.svg"
```

### 3. 查询 PML 知识库
```bash
python -m e3d_agent.agent --query "如何在 E3D 中正确创建 DISH 封头？"
```

### 4. 查看系统记忆与错误统计
```bash
# 查看历史错误日志
python -m e3d_agent.agent --errors

# 查看 Agent 统计数据
python -m e3d_agent.agent --summary
```

---

## 预置复杂 3D 模型生成器

项目中内置了多个高精度 3D PML 宏生成器，可直接运行生成相应的 PML 脚本并导入 E3D 中验证：

| 生成器脚本 | 说明 | 基本体数量 |
| :--- | :--- | :--- |
| `paper_mill_mega_100k_plant.py` | **10 万基本体特大型造纸厂全景模型** | ~100,000 |
| `paper_machine_model.py` | PM1 大型成套造纸机设备 | ~10,000 |
| `car_model.py` | 高精细汽车模型（含轮轴、座舱、大灯等） | ~5,000 |
| `cfm56_model.py` | CFM56-7B 航空涡扇发动机模型 | ~3,000 |
| `distillation_column_model.py` | 工业精馏塔及配套管道平台系统 | ~1,500 |
| `motor_model.py` | 500kW 工业电机模型 | ~500 |

#### 运行示例：
```bash
# 生成 10 万基本体造纸厂模型
python -m e3d_agent.paper_mill_mega_100k_plant

# 生成高精汽车模型宏
python -m e3d_agent.car_model
```
生成的 `.pml` 文件将自动存入 `output/` 目录中。

---

## 项目结构

```
e3d_agent/
├── agent.py                      # AI Agent 主编排器
├── AGENTS.md                     # LLM E3D 建模强制规范 v3
├── config.py                     # 全局配置与路径定义
├── drawing_parser/               # 自然语言与图纸解析引擎 (PDF, SVG)
├── pml_knowledge/                # E3D PML 语法与装备知识库
├── pml_generator/                # PML1 脚本生成器
├── e3d_interface/                # E3D 软件交互接口
├── memory/                       # 历史记忆与错误自愈数据库
├── car_model.py                  # 汽车模型生成器
├── cfm56_model.py                # 航空发动机模型生成器
├── distillation_column_model.py  # 精馏塔模型生成器
├── motor_model.py                # 工业电机模型生成器
├── paper_machine_model.py        # 造纸机模型生成器
├── paper_mill_mega_100k_plant.py # 10万基本体造纸厂全景生成器
├── output/                       # PML 宏输出目录
└── tests/                        # 单元测试与稳定性测试集
```

---

## 许可证

本项目遵循 [MIT License](LICENSE)。
