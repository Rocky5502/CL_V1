from epifair.utils.hashing import stable_id, sha256_text

def test_stable_id_is_stable():
    assert stable_id("x",{"b":2,"a":1})==stable_id("x",{"a":1,"b":2})

def test_sha256():
    assert sha256_text("abc").startswith("ba7816bf")
