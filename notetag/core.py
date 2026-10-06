"""事件重放核心。"""


class Counter:
    """记录本轮检查过的玩家条数。"""

    def __init__(self):
        self.scanned = 0


def replay(events, tag_cap, counter, order=True):
    if order:
        events = sorted(events, key=lambda event: event["ts"])
    view = {"players": [], "dropped": 0}
    by_id = {}
    for event in events:
        counter.scanned += 1
        player = by_id.get(event["player"])
        if player is None:
            player = {"id": event["player"], "name": event["player"], "note": "",
                      "tags": [], "tag_set": set()}
            view["players"].append(player)
            by_id[player["id"]] = player
        kind = event["kind"]
        if kind == "rename":
            player["name"] = event["value"]
        elif kind == "note":
            player["note"] = event["value"]
        elif kind == "tag-add":
            tag = event["value"]
            if tag in player["tag_set"]:
                continue
            if len(player["tags"]) >= tag_cap:
                view["dropped"] += 1
                continue
            player["tags"].append(tag)
            player["tag_set"].add(tag)
        elif kind == "tag-remove":
            tag = event["value"]
            if tag in player["tag_set"]:
                player["tag_set"].remove(tag)
                player["tags"].remove(tag)
    return view


def read_log(path):
    import json
    events = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                events.append(json.loads(line))
    return events
