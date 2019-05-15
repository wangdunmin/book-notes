命令详情可查看[Git官方文档](!https://git-scm.com/book/zh/v2)
* 新建并切换分支
```
git checkout -b fenzhi
```
* 删除本地分支
```
git branch -d fenzhi
```
* 切换分支
```
git checkout master
```
* 合并分支 
```
git merge fenzhi
```
* 查看已经合并的分支
```
git branch --merged
```
* 查看分支
```
git branch
```
* 更新本地当前分支到远程分支的关联
```
git branch -u origin/master
```
* 提交分支到远程
```
git push origin fenzhi
```
* 删除远程分支(删除远程分支后本地分支不会被删除)
```
git push origin --delete fenzhi
```
* 切换跟踪分支(本地分支和远程分支的关联)
```
git checkout  --track origin/fenzhi

git checkout -b fenzhi origin/fenzhi
```
* 查看分支与远程分支关联
```
git branch -vv
```
* 从远程仓库克隆分支
```
git clone -b 分支名 仓库地址
```

> 注意：
> 在测试中，由于本地仓库和远程仓库分支信息不同步，导致切换跟踪分支时出现如下异常
> ```
> fatal: 'origin/fenzhi' is not a commit and a branch 'fenzhi1' cannot be created from it
> ```
> 这时可通过以下命令将本地仓库和远程仓库信息同步
> ``` 
> git fetch
> ```




