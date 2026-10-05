import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notetag import core


def ev(ts, player, kind, value):
    return {"ts": ts, "player": player, "kind": kind, "value": value}


class NoteTagTest(unittest.TestCase):
    def test_single_player_is_created(self):
        view = core.replay([ev(100, "p1", "tag-add", "a")], 4, core.Counter())
        self.assertEqual(len(view["players"]), 1)
        self.assertEqual(view["players"][0]["tags"], ["a"])

    def test_rename_keeps_player_id(self):
        view = core.replay([ev(100, "p1", "rename", "小明")], 4, core.Counter())
        self.assertEqual(view["players"][0]["id"], "p1")
        self.assertEqual(view["players"][0]["name"], "小明")

    def test_note_is_stored(self):
        view = core.replay([ev(100, "p1", "note", "老队友")], 4, core.Counter())
        self.assertEqual(view["players"][0]["note"], "老队友")

    def test_two_players_stay_separate(self):
        view = core.replay([ev(100, "p1", "tag-add", "a"), ev(200, "p2", "tag-add", "b")],
                           4, core.Counter())
        self.assertEqual(len(view["players"]), 2)

    def test_empty_log(self):
        view = core.replay([], 4, core.Counter())
        self.assertEqual(view["players"], [])


if __name__ == "__main__":
    unittest.main()
