"""命令行入口。"""

import argparse
import json

from . import core


def main(argv=None):
    ap = argparse.ArgumentParser(prog="notetag")
    ap.add_argument("--sample", choices=["order", "cap", "dup", "remove", "work"])
    sub = ap.add_subparsers(dest="cmd")
    replay_parser = sub.add_parser("replay")
    replay_parser.add_argument("--log", required=True)
    replay_parser.add_argument("--tag-cap", type=int, default=4)
    args = ap.parse_args(argv)

    if args.sample:
        from . import samples
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    counter = core.Counter()
    view = core.replay(core.read_log(args.log), args.tag_cap, counter)
    for player in sorted(view["players"], key=lambda item: item["id"]):
        print(json.dumps({"player": player["id"], "name": player["name"], "note": player["note"],
                          "tags": player["tags"], "dropped": view["dropped"]}, ensure_ascii=False))
    print(json.dumps({"players": len(view["players"]), "scanned": counter.scanned},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
