# 按需安装入口

## 基本规则

这是总控 skill 的依赖引导，不是自动安装器。用户只有一个日常调用入口 `$jianying-tutorial-editing`；无需自行决定什么时候切换两个下游 skill。

先决定本次路线，再检查所需工具。优先使用会话已列出的 skill、用户指定目录及当前项目已配置的 checkout；不要把制作者电脑的路径写成所有人的固定位置。路径缺失时进行有限的相关目录查找，不扫描整台电脑。无法找到时只提示缺失项，保留已找到的版本和有效授权。

提示内容包括：缺什么、在本片负责什么、官方安装入口、下一步怎么继续。用户已经安装就不再推荐；同一缺失问题不重复催促。用户请求代装后，使用对应官方安装工作流；安装失败据实报告，不能说依赖已就绪。

## Agent Motion

用于口播语义动效及分配给它的人物段落。它是包含项目内 skill 的完整工程，不能只拷贝一份 SKILL.md 就宣称安装完成。

- [官方项目与下载入口](https://github.com/erduo1998-cell/agent-motion)
- [官方首次使用说明](https://github.com/erduo1998-cell/agent-motion/blob/main/docs/getting-started.md)

缺失时可以直接告诉用户：

> 这次口播包装需要 Agent Motion，目前未找到它。请从上面的官方入口安装；你也可以复制下面这句话让我协助安装，完成后继续当前视频。

可复制的请求：

> 请从 https://github.com/erduo1998-cell/agent-motion 为我安装 Agent Motion，先读它的 AGENTS.md 和官方安装说明，按其流程配置并检查环境。保留我的素材与现有工程，安装后继续当前视频任务。

其官方说明当前使用 Node22+ 和项目内 `node scripts/bootstrap.mjs`；实际执行前读取当时版本，不把本文摘要代替上游完整步骤。账号、许可和商业用途核验按所用版本处理；个人安装成功不等于公司团队、集成或再分发授权已取得。此总控不代签或扩展授权。

## video-shotcraft

用于 B-roll、网页/产品展示、教程画面及解释性动效。

- [官方项目与安装入口](https://github.com/Vincentwei1021/video-shotcraft)
- [动效样片库](https://vincentwei1021.github.io/video-shotcraft/library.html)

本机会话已提供该 skill 时直接读取真实入口。缺失时给官方项目链接与可复制请求：

> 请把 https://github.com/Vincentwei1021/video-shotcraft 安装成 Codex skill，检查实际入口及制作所需依赖，完成后继续当前视频任务。

用户要求代装时按 skill-installer 的 GitHub 安装流程执行；不静默使用浮动远端内容替换用户指定版本。实际使用时仍读取准确镜头卡、变体和 demo，不以安装完成代替镜头理解。

## 剪映及其他依赖

需要原生工程交付时检查目标剪映客户端。未安装或账号状态阻塞时，说明该项并引导用户使用官方客户端；不触发与本片无关的 CapCut 网页 OAuth，不索取密码或 Cookie。

Node、Python、FFmpeg、浏览器、字体等只在下游实际需要时按其工作流检查；不为了预防问题而先安装整套环境。不自动购买会员、接受协议、发布内容或修改系统安全设置。

## 回到当前任务

依赖准备完成后复用已经确认的内容、视觉与时间线，从受阻步骤继续。只验证过安装就说安装通过；只有制作、导出和客户端编辑测试实际做完，才分别确认这些结果。
