# AVEVA E3D 管嘴规格转换与批量属性配置插件 (PML Form UI)

## 简介
本插件是专为 AVEVA E3D / PDMS 开发的原生图形化交互工具（PML Form），旨在解决跨项目库导入模型时管嘴规格丢失（`Nulref`）、管嘴不可见、以及需要批量统一管嘴等级元件与属性的高频工程需求。

---

## 核心功能

1. **多作用域扫描与健康诊断**：
   * 支持 `Current Element (CE)`、`Current Zone`、`Current Site`、`Entire World` 四种扫描范围。
   * 自动诊断并高亮标记异常隐形管嘴（`[MISSING] ... (Nulref)`）与正常管嘴（`[OK] ...`）。
2. **批量规格转换与 CATREF 绑定**：
   * 自定义目标等级元件路径（例如 `/150lb_Ansi_Flanged/AAZFBB0YY` 或国标/德标元件）。
   * 支持 **`[x] 仅修复 Nulref/丢失元件管嘴`**，防止误覆盖已有正确规格的管嘴。
3. **批量属性赋能（可选）**：
   * 批量修改管嘴外伸高度（`HEIG`，单位 mm）。
   * 批量修改设计温度（`TEMP`，单位 °C）。
   * 批量修改设计压力（`PRES`，单位 bar）。
4. **一键加载（免配置 PMLLIB）**：
   * 采用内存动态编译机制，无需繁琐配置 E3D 系统环境变量或重索目录。

---

## 使用指南

### 1. 启动插件
在 AVEVA E3D 下方的 **Command** 命令行窗口中输入并回车：
```pml
$M "C:\Users\A\Desktop\launch_nozzle_tool.mac"
```
E3D 界面将立即弹出交互式对话框窗口。

### 2. 操作步骤
1. **选择范围**：在 **1. Scope & Scan** 下拉框中选择扫描范围（如 `Current Element (CE)` 或 `Current Zone`）。
2. **扫描诊断**：点击 **Scan Nozzles** 按钮，中间列表将列出所有检索到的管嘴及绑定状态。
3. **配置目标规格**：在 **3. Target Specification** 中输入目标元件路径（默认已填入标准美标 150lb 元件）。
4. **批量执行**：点击 **Batch Convert / Apply**，三维视图中的管嘴将瞬间批量完成更新并渲染显示。
