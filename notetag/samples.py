"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _ev(ts, player, kind, value):
    return {"ts": ts, "player": player, "kind": kind, "value": value}


def _tags(view, player_id):
    for player in view["players"]:
        if player["id"] == player_id:
            return player["tags"]
    return []


def run(name):
    counter = core.Counter()
    if name == "order":
        events = [_ev(200, "p1", "tag-add", "b"), _ev(100, "p1", "tag-add", "a")]
        view = core.replay(events, 4, counter)
        _line({"tags": _tags(view, "p1")})
        return 0
    if name == "cap":
        events = [_ev(100 * i, "p1", "tag-add", "t%d" % i) for i in range(5)]
        view = core.replay(events, 4, counter)
        _line({"tags": _tags(view, "p1"), "dropped": view["dropped"]})
        return 0
    if name == "dup":
        events = [_ev(100, "p1", "tag-add", "a"), _ev(200, "p1", "tag-add", "a")]
        view = core.replay(events, 4, counter)
        _line({"tags": _tags(view, "p1")})
        return 0
    if name == "remove":
        events = [_ev(100, "p1", "tag-add", "a"), _ev(200, "p1", "tag-add", "b"),
                  _ev(300, "p1", "tag-remove", "a")]
        view = core.replay(events, 4, counter)
        _line({"tags": _tags(view, "p1")})
        return 0
    if name == "work":
        events = [_ev(i * 10, "p%03d" % (i % 400), "tag-add", "t") for i in range(2000)]
        core.replay(events, 4, counter)
        _line({"events": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
