# 安装Gradle
您可以在Linux、macOS或Windows上安装Gradle构建工具。本文档介绍如何使用SDKMAN！，Homebrew或Scoop等软件包管理器进行安装，以及手动安装。

推荐的升级方式是使用[Gradle Wrapper](https://docs.gradle.org/5.0/userguide/gradle_wrapper.html#sec:upgrading_wrapper)。

您可以在[发行页](https://gradle.org/releases/)上找到所有发行版及其校验和。

## 先决条件
首先，Gradle可以运行在当前主要的操作系统上，但他需要JDK1.8及以上的版本支持；

Gradle附带了自己的Groovy库，因此不需要安装Groovy，Gradle忽略任何现有的Groovy安装。

Gradle使用它在您的路径中找到的任何JDK。或者，您可以将JAVA_HOME环境变量设置为指向所需的JDK的安装目录。

## 使用包管理器进行安装

* **[SDKMAN!](https://sdkman.io/)** 是一个在大多数基于Unix的系统上管理多个软件开发工具包的并行版本的工具。

    > sdk install gradle

* **[Homebrew](https://brew.sh/)**

    > brew install gradle

* **[Scoop](https://scoop.sh/)**

    > scoop install gradle

* **[Chocolatey](https://chocolatey.org/)**

    > choco install gradle

* **[MacPorts](https://www.macports.org/)**

    > sudo port install gradle 

## 手动安装

1. 下载最新的[Gradle发行版](https://gradle.org/releases/)
2. 解压分发包，根据不同的系统
3. 配置系统环境

各个步骤细节可参考[官网](https://docs.gradle.org/5.0/userguide/installation.html#installing_manually)

## 验证安装

打开控制台运行 
> gradle -v

如果遇到任何问题，请参阅[有关安装故障排除的部分](https://docs.gradle.org/5.0/userguide/troubleshooting.html#sec:troubleshooting_installation)。

您可以通过下载SHA-256文件（可从[发布页面](https://gradle.org/releases/)获得）并遵循这些[验证说明](https://docs.gradle.org/5.0/userguide/gradle_wrapper.html#sec:verification)来验证Gradle分发的完整性


