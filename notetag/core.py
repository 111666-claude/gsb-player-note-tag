"""事件重放核心。"""


class Counter:
    """记录本轮检查过的玩家条数。"""

    def __init__(self):
        self.scanned = 0


def _find(view, player_id, counter):
    for player in view["players"]:
        counter.scanned += 1
        if player["id"] == player_id:
            return player
    return None


def replay(events, tag_cap, counter, order=True):
    view = {"players": [], "dropped": 0}
    for event in events:
        player = _find(view, event["player"], counter)
        if player is None:
            player = {"id": event["player"], "name": event["player"], "note": "", "tags": []}
            view["players"].append(player)
        kind = event["kind"]
        if kind == "rename":
            player["name"] = event["value"]
        elif kind == "note":
            player["note"] = event["value"]
        elif kind == "tag-add":
            player["tags"].append(event["value"])
        elif kind == "tag-remove":
            pass
    return view


def read_log(path):
    import json
    events = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                events.append(json.loads(line))
    return events
