from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import base64
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _deserialize_bytes_base64(attr):
    if isinstance(attr, (bytes, bytearray)):
        return attr
    padding = "=" * (3 - (len(attr) + 3) % 4)  # type: ignore
    attr = attr + padding  # type: ignore
    encoded = attr.replace("-", "+").replace("_", "/")
    return bytes(base64.b64decode(encoded))

# Strategy for generating inputs
def attr_strategy():
    return st.one_of(
        st.binary(min_size=0, max_size=100),  # bytes or bytearray
        st.text(
            alphabet=st.characters(
                whitelist_categories=('L', 'N', 'P', 'S'),
                whitelist_characters='-_+/='
            ),
            min_size=0, max_size=100
        )  # base64-like strings
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(attr=attr_strategy())
@example(attr=b"")
@example(attr="")
@example(attr="YQ==")  # "a"
@example(attr="YWI=")  # "ab"
@example(attr="YWJj")  # "abc"
@example(attr="YWJjZA==")  # "abcd"
@example(attr="YWJjZGU=")  # "abcde"
@example(attr="YWJjZGVm")  # "abcdef"
@example(attr="YWJjZGVmZw==")  # "abcdefg"
@example(attr="YWJjZGVmZ2g=")  # "abcdefgh"
@example(attr="YWJjZGVmZ2hp")  # "abcdefghi"
@example(attr="YWJjZGVmZ2hpag==")  # "abcdefghij"
@example(attr="YWJjZGVmZ2hpams=")  # "abcdefghijk"
@example(attr="YWJjZGVmZ2hpamts")  # "abcdefghijkl"
@example(attr="YWJjZGVmZ2hpamtsbQ==")  # "abcdefghijklm"
@example(attr="YWJjZGVmZ2hpamtsbW4=")  # "abcdefghijklmn"
@example(attr="YWJjZGVmZ2hpamtsbW5v")  # "abcdefghijklmno"
@example(attr="YWJjZGVmZ2hpamtsbW5vcA==")  # "abcdefghijklmnop"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHE=")  # "abcdefghijklmnopq"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFy")  # "abcdefghijklmnopqr"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFycw==")  # "abcdefghijklmnopqrs"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3Q=")  # "abcdefghijklmnopqrst"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1")  # "abcdefghijklmnopqrstu"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dg==")  # "abcdefghijklmnopqrstuv"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnc=")  # "abcdefghijklmnopqrstuvw"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4")  # "abcdefghijklmnopqrstuvwx"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eQ==")  # "abcdefghijklmnopqrstuvwxy"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo=")  # "abcdefghijklmnopqrstuvwxyz"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpB")  # "abcdefghijklmnopqrstuvwxyA"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQg==")  # "abcdefghijklmnopqrstuvwxyAB"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkM=")  # "abcdefghijklmnopqrstuvwxyABC"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNE")  # "abcdefghijklmnopqrstuvwxyABCD"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERQ==")  # "abcdefghijklmnopqrstuvwxyABCDE"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUY=")  # "abcdefghijklmnopqrstuvwxyABCDEF"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZH")  # "abcdefghijklmnopqrstuvwxyABCDEFG"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSQ==")  # "abcdefghijklmnopqrstuvwxyABCDEFGH"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSkk=")  # "abcdefghijklmnopqrstuvwxyABCDEFGHI"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklK")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJ"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKSw==")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJK"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0w=")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKL"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xN")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLM"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTg==")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMN"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk4=")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNO"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5P")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOP"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5PUA==")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQ"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5PUFE=")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQR"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5PUFFS")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRS"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5PUFFSUw==")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRST"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5PUFFSU1Q=")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTU"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5PUFFSU1RV")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUV"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5PUFFSU1RVVg==")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVW"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5PUFFSU1RVVlc=")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWX"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5PUFFSU1RVVldY")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXY"
@example(attr="YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXpBQkNERUZHSklKS0xNTk5PUFFSU1RVVldYWQ==")  # "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXYZ"
def test_deserialize_bytes_base64(attr):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    attr_copy = copy.deepcopy(attr)

    # Call func0 to verify input validity
    try:
        expected = _deserialize_bytes_base64(attr_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "attr": attr_copy if isinstance(attr_copy, str) else list(attr_copy)
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)