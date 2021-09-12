#!/usr/bin/env -S python3
import sys, os, base64

inb = sys.stdin.buffer.read()
os.write(
    sys.stdout.fileno(),
    b"\x1b]52;c;" +
    base64.b64encode(inb) +
    b"\a"
)
