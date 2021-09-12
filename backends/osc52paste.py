#!/usr/bin/env -S python3

# derived from https://github.com/tmux/tmux/issues/1477#issue-360205769
from __future__ import annotations

import base64
import copy
import fcntl
import os
import select
import subprocess
import sys
import termios


stdin_bytes = sys.stdin.buffer
stdout_bytes = sys.stdout.buffer

class NoTtyException(Exception):
    pass


def get_active_tmux_tty() -> str:
    try:
        tmux_active_tty = [
            tty
            for is_active, tty in (
                line.split()
                for line in subprocess.check_output(["tmux", "list-panes", "-F", "#{pane_active} #{pane_tty}"])
                .strip()
                .split(b"\n")
            )
            if is_active
        ][0]
    except (subprocess.CalledProcessError, IndexError):
        raise NoTtyException
    return tmux_active_tty


def get_active_tty() -> str:
    if "TMUX" in os.environ:
        active_tty = get_active_tmux_tty()
    else:
        try:
            active_tty = subprocess.check_output(["tty"]).strip()
        except subprocess.CalledProcessError:
            raise NoTtyException
    return active_tty


def toggle_terminal_for_osc_query() -> None:
    self = toggle_terminal_for_osc_query
    active_tty = get_active_tty()
    with open(active_tty, "wb") as tty:
        if not hasattr(self, "terminal_attrs"):
            self.terminal_attrs = termios.tcgetattr(tty)
            modified_terminal_attrs = copy.deepcopy(self.terminal_attrs)
            modified_terminal_attrs[3] &= ~(
                termios.ICANON | termios.ECHO
            )  # Disable echo of input bytes and line buffering
            termios.tcsetattr(tty, termios.TCSANOW, modified_terminal_attrs)
        else:
            termios.tcsetattr(tty, termios.TCSANOW, self.terminal_attrs)
            del self.terminal_attrs


def set_non_blocking_mode(f: IO) -> None:
    fl = fcntl.fcntl(f, fcntl.F_GETFL)
    fcntl.fcntl(f, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def osc_paste() -> str:
    toggle_terminal_for_osc_query()
    try:
        osc_sequence = b"\033]52;c;?\a"
        active_tty = get_active_tty()
        with open(active_tty, "wb") as tty:
            tty.write(osc_sequence)
        with open(active_tty, "rb") as tty:
            set_non_blocking_mode(tty)
            next_bytes = b""
            response_bytes = []
            response_parameter_id = 0
            read_sequence_terminator = False
            while not read_sequence_terminator and tty in select.select([tty], [], [], 0.01)[0]:
                next_bytes = tty.read()
                while True:
                    next_delimiter_index = next_bytes.find(b";")
                    if next_delimiter_index < 0:
                        break
                    response_parameter_id += 1
                    next_bytes = next_bytes[next_delimiter_index + 1 :]
                sequence_terminator_index = next_bytes.find(b"\a")
                if sequence_terminator_index >= 0:
                    next_bytes = next_bytes[:sequence_terminator_index]
                    read_sequence_terminator = True
                if response_parameter_id == 2:
                    response_bytes.append(next_bytes)
    finally:
        toggle_terminal_for_osc_query()
    response = base64.b64decode(b"".join(response_bytes))
    return response


def main() -> None:
    try:
        paste_buffer = osc_paste()
        if paste_buffer:
            stdout_bytes.write(paste_buffer)
            sys.exit(0)
        else:
            # Assume that the terminal does not support OSC 52 reading if the response was empty
            sys.exit(1)
    except NoTtyException:
        sys.exit(2)


if __name__ == "__main__":
    main()
