# 剪映口播与教程视频剪辑 · v3 轻量版

一个总控入口，协调 Agent Motion、video-shotcraft 与剪映，制作口播、Q&A 和教程，并交付整理好的可编辑剪映工程。

## 安装

在 Codex 中发送：

> 请安装 https://github.com/MilesHuang-EDIT/jianying-tutorial-editing 的 skill。

已有旧版时可以说“请更新这个仓库的 skill，并保留我的其他 skill”。安装后在下一轮继续使用原调用名 `$jianying-tutorial-editing`。

## 怎么用

安装本文件夹中的 skill 后，在 Codex 说：

> 用 $jianying-tutorial-editing 制作这期口播。我提供视频和字幕，请先推荐动效并展示风格预览，最后交付整理好时间线的剪映工程和 MP4。

也可以直接说明“我要做软件教程”“我要做硬件操作演示”。总控按视频类型分配工具，用户无需分别调用两个下游 skill。

## 工具如何接入

- 口播：Agent Motion 做主包装，video-shotcraft 做对应 B-roll，剪映整合。
- 教程：video-shotcraft 做画面与动效；有人物出镜时再接 Agent Motion。
- 已安装的工具直接调用；本次确实需要却尚未安装时，才给出官方安装入口和简短指引。用户希望代装时再协助，不在开场安装全部依赖。

本包不包含第三方工具源码、自动环境安装器、剪映应用或账号。安装入口见 [按需安装说明](references/install-on-demand.md)。公司使用仍需遵守相应工具和素材授权。

## 交付方式

先推荐动效并展示风格预览，再制作和检查。剪映主时间线按章节整理，内部保留原生文字、素材和关键帧；字幕与声音独立。复杂三维效果保留独立层及回源修改方式。实际可编辑范围与验收状态随项目说明。

## 开源与依赖

本仓库自有总控规范和检查脚本采用 [MIT License](LICENSE)。Agent Motion、video-shotcraft、剪映及相关字体、素材和运行库保留各自条款，本仓库的 MIT 许可不会授予这些依赖的使用权。这里不分发第三方源码、账号或用户视频。
