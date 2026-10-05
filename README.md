# player-note-tag

好友备注与标签：把一条事件日志按时间合并重放，得到每个玩家当前的视图。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m notetag replay --log events.jsonl --tag-cap 4
python3 -m notetag --sample=order|cap|dup|remove|work
```

日志每行一个事件：`{"ts": 毫秒, "player": "玩家号", "kind": "...", "value": "..."}`，
`kind` 取 `rename`、`note`、`tag-add`、`tag-remove`。

## 口径

- **时间线合并**：事件按 `ts` 从小到大重放；`ts` 相同时保持日志里的先后。
- **标签上限**：每个玩家的标签数不超过 `--tag-cap`，超出的事件丢弃并计入 `dropped`。
- **去重**：同一个玩家重复添加同名标签只算一次。
- **移除**：`tag-remove` 把同名标签去掉；不存在的标签无副作用。
- **备注**：后到的 `note` 覆盖先到的。

## 不变量

- 每个玩家的标签数不超过 `tag-cap`，且互不重复。
- 玩家视图只按玩家号聚合，`rename` 只改显示名。
- `scanned` 不随玩家数放大：两千条事件、四百个玩家时不超过 9000。

## 输出契约

`replay` 每个玩家打印一行 JSON：`player`、`name`、`note`、`tags`、`dropped`；
末尾打印一行 `{"players": N, "scanned": N}`。
`--sample=work` 只打印 `{"events": N, "scanned": N}`。
