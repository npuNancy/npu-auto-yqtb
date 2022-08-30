# npu-auto-yqtb
使用 GitHub Acition 进行西北工业大学自动疫情填报

## 定时

> 更改 [workflow yaml](.github/workflows/main.yml) 中 cron 项即可填报更改时间
>
> ``` yaml
> schedule:
>    - cron: '0 0,16 * * *' 
>       # 此时间为 'UTF时间', +8h 后为 '北京时间'
>       # 每天00:00, 16:00 执行
> ```
> 由于定时任务由Github调度, 实际执行时间可能延迟1-2h不定
> 更多可见 [github docs onschedule](https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions#onschedule)