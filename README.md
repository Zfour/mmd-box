# mmd-box
简介：一个桌面mmd伪全息投影盒子的websocket练习项目

# 进度：

## 2022/7/26 

1.按照B站教程<a href="https://www.bilibili.com/video/BV1aV411o7N6">【伪全息播放盒】会动的手办了解一下</a> 手工diy了伪全息投影盒子，并计划开发相应网页端支持控制脚本。

<img style="width:auto;height:500px;" src="https://github.com/Zfour/mmd-box/blob/master/picture/1.gif">

2.完成了网页端的简单开发，将hexo clock插件进行了移植及盒子界面自适应。

<a href="https://zfour.github.io/mmd-box/templates/box_view/index.html">预览地址</a> 

3.初步尝试python flask socketio 并跑通本地局域网通信。

### 提出初步需求：

1.实现手机端控制切换播放视频

2.实现手机端控制列表播放和单个视频循环的功能

3.实现手机端控制界面UI隐藏的纯享模式功能

4.封装flask python网页程序实现win/linux环境独立运行和关闭，脱离ide部署

5.将程序导入香橙派ubantu脱离电脑运行

6.尝试其他可交互指令以及服务端消息推送开发，例如添加代办事项，rss订阅查询推送

7.桌宠模式，通过手机控制单一mmd角色实现手机控制，对应mmd动画的响应以及视频制作

8.游戏模式，桌面俄罗斯方块，通过手机手柄进行游戏控制（待定）

## 2022/7/27 

1.初步跑通局域网通过ios快捷指令控制视频切换的功能，目前逻辑为通过config.json存储用户切换数据存储本地，每次重启时默认读取上次历史视频id数据。

2.待开发视频循环模式的选择，当前为单视频循环，后期考虑是否拉取列表选择（必要性不大感觉）。

## 2022/7/28

1.实现了UI的显示和隐藏，考虑到更多模式的需求采用的是多路由多状态对应触发。

## 2022/7/31
1.实现了单个视频循环和列表播放功能
2.部分修复了视频文件夹文件修改造成的bug
3.香橙派方案out，百元板子带不动视频，需要300+预算不划算

## 2022/8/4
1.1.0版本图形界面开发完成，目前打包遇见bug，尚未跑通，ide版本刷新网页有概率触发bug待修复
2.图形界面如下
![image](https://user-images.githubusercontent.com/19563906/182721739-2bfad9e1-ab27-4cb5-bec7-acdc33a839eb.png)
