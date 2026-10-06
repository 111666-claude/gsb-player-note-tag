"""事件重放核心。"""


class Counter:
    """记录本轮检查过的玩家条数。"""

    def __init__(self):
        self.scanned = 0


def replay(events, tag_cap, counter, order=True):
    view = {"players": [], "dropped": 0}
    index = {}
    ordered = sorted(events, key=lambda event: event["ts"]) if order else events
    for event in ordered:
        counter.scanned += 1
        player_id = event["player"]
        player = index.get(player_id)
        if player is None:
            player = {"id": player_id, "name": player_id, "note": "", "tags": []}
            view["players"].append(player)
            index[player_id] = player
        kind = event["kind"]
        if kind == "rename":
            player["name"] = event["value"]
        elif kind == "note":
            player["note"] = event["value"]
        elif kind == "tag-add":
            tag = event["value"]
            if tag in player["tags"]:
                continue
            if len(player["tags"]) >= tag_cap:
                view["dropped"] += 1
                continue
            player["tags"].append(tag)
        elif kind == "tag-remove":
            tag = event["value"]
            if tag in player["tags"]:
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
