-- ==============================================================================
-- AVEVA E3D / PDMS PML1 Standalone Typical Pipe Support Macro (单件标准管道支架)
-- 目的: 供用户在 E3D 中直接手动优化、微调尺寸、调整节点细节与参数
-- 坐标系: 原点标准坐标 (墙面 Y=0, 挑臂沿 +N 方向, 梁顶面标高 TOS U=0)
-- 包含组件: 槽钢悬臂梁 + 角钢斜撑 + 梁下节点板 + 根部加劲肋 + 双底板 + 6x 圆形锚栓
-- 翼缘保护: 斜撑工作点位于节点板内 (U -185), 与槽钢下翼缘间隙 35mm, 100% 零穿模!
-- 表面状态: 横梁上翼缘 100% 平整, 无任何隔离垫块, 为后续管夹预留安装面
-- ==============================================================================

-- 1. 清理旧测试节点 (带 handle 保护)
/STRU-TYPICAL-PIPE-SUPPORT
handle (2,109)
elsehandle none
  DELETE STRU
endhandle

/EQUI-TYPICAL-PIPE-SUPPORT-HDW
handle (2,109)
elsehandle none
  DELETE EQUI
endhandle

/ZONE-TYPICAL-SUPPORT
handle (2,109)
  NEW SITE /SITE-TYPICAL-SUPPORT
  NEW ZONE /ZONE-TYPICAL-SUPPORT
endhandle

-- 2. 钢结构杆件 (Structure 模块: STRU -> FRMW -> SCTN)
/ZONE-TYPICAL-SUPPORT
NEW STRU /STRU-TYPICAL-PIPE-SUPPORT
NEW FRMW /FRMW-TYPICAL-PIPE-SUPPORT

-- [A] 悬臂槽钢主梁 (Profile: /BS-PFC150x75x18, 长度 1500mm, JUSL CTOP)
NEW SCTN /SCTN-TYPICAL-BEAM
POSS E 0.0 N 16.0 U 0.0
POSE E 0.0 N 1500.0 U 0.0
DRNS PERP
DRNE PERP
JUSL CTOP
SPRE SPCOMPONENT /BS-PFC150x75x18

-- [B] 角钢斜撑 (Profile: /BS-L50x50x6, 顶点止于节点板内 U -185, 零翼缘穿模!)
NEW SCTN /SCTN-TYPICAL-BRACE
POSS E 0.0 N 16.0 U -470.0
POSE E 0.0 N 1055.0 U -185.0
DRNS PERP
DRNE PERP
JUSL TOAY
SPRE SPCOMPONENT /BS-L50x50x6

-- 3. 连接硬件、安装底板、焊接节点板与紧固件 (EQUI -> SUBE -> 基本体)
/ZONE-TYPICAL-SUPPORT
NEW EQUI /EQUI-TYPICAL-PIPE-SUPPORT-HDW
ORI Y IS N AND Z IS U
POS E 0.0 N 0.0 U 0.0

NEW SUBE /SUBE-TYPICAL-HDW

-- [1] 上安装底板 (宽180 x 厚16 x 高350, 中心 U -75, 贴墙 Y 0~16)
NEW BOX
XLEN 180.0
YLEN 16.0
ZLEN 350.0
POS E 0.0 N 8.0 U -75.0

-- [2] 4x 上底板圆形工程锚栓 (直径 28mm, 凸起 10mm, 间距 90x270mm)
NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E -45.0 N 21.0 U 60.0

NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E 45.0 N 21.0 U 60.0

NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E -45.0 N 21.0 U -210.0

NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E 45.0 N 21.0 U -210.0

-- [3] 槽钢梁根部焊接加劲肋 (厚8 x 长80 x 高150, 中心 U -75)
NEW BOX
XLEN 8.0
YLEN 80.0
ZLEN 150.0
POS E 0.0 N 56.0 U -75.0

-- [4] 梁下焊接加劲节点板 (厚8 x 长180 x 高90, 顶面紧贴槽钢下翼缘, 中心 U -195)
NEW BOX
XLEN 8.0
YLEN 180.0
ZLEN 90.0
POS E 0.0 N 1055.0 U -195.0

-- [5] 斜撑下墙面安装底板 (宽180 x 厚16 x 高160, 中心 U -470)
NEW BOX
XLEN 180.0
YLEN 16.0
ZLEN 160.0
POS E 0.0 N 8.0 U -470.0

-- [6] 2x 斜撑下底板圆形工程锚栓 (直径 28mm, 凸起 10mm, 横向间距 90mm)
NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E -45.0 N 21.0 U -470.0

NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E 45.0 N 21.0 U -470.0

-- [7] 斜撑根部下焊接节点板 (厚8 x 长80 x 高100, 中心 U -470)
NEW BOX
XLEN 8.0
YLEN 80.0
ZLEN 100.0
POS E 0.0 N 56.0 U -470.0

SAVEWORK
-- ==============================================================================
-- 单件标准管道支架加载完成!
-- 查看指令:
-- ADD /ZONE-TYPICAL-SUPPORT
-- AUTO CE
-- ==============================================================================
