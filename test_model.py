import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from generation_t5 import gen_poem


def test_gen_poem_case_length_not_1():
    key_w = ["chat", "chien", "table"]
    length = 3
    assert len(gen_poem(key_w, length)) > 0


def test_gen_poem_case_length_is_1():
    key_w = ["chat", "chien", "table"]
    length = 1
    assert len(gen_poem(key_w, length)) > 0
