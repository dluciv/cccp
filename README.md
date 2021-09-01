# CCCP

Applications and automation scripts often use `xclip`, `xsel`, `wl-clipboard`, `pbcopy` and even `clip.exe` and PowerShell functions to access clipboard.
CCCP aims to be united frontend for them, allowing to free other users and developers from selecting or detecting them.

This tool was initially created for personal use. But you are welcome to contribute, report issues, suggest features, etc.
I have almost no time to maintain and develop it beyound my personal needs, so the most welcome requests are those coming with pull requests =).

## Usage

* `cccp c` reads `STDIN` and copies it to the clipboard
* `cccp p` pastes from the clipboard to `STDOUT`
* `cccp ac ... ... ...` (Arg Copy) copies `... ... ...` to the clipboard

`cccp` can be easily symlinked to any location you already have in your `$PATH`, e.g. `~/.local/bin` (this is how I use it).

## Configuration

With zero configuration it tries to autodetect the backend. However you can either override or help it (to run faster) by placing simple configuration file like

```
BACKEND=wayland
```

named `~/.config/cccp.conf` (or `$XDG_CONFIG_HOME/cccp.conf` if you have `$XDG_CONFIG_HOME`).

Hacker notes =):

* You can temporarily override backend via environment as follows: `CCCP_BACKEND=whatever cccp ...`
* `cccp.conf` is just an SH script, so you can place some logic here, e.g. switchng between XOrg and Wayland in Linux (see `cccp` script itself), etc.

## Name

CCCP – Common Clipboard Copy &amp; Paste. Those who know Russian may also read it as [«СССР», which is 'USSR' in Russian](https://en.wikipedia.org/wiki/Soviet_Union) ☭🐻 =).

The reason behind the name was to find some short abbrevation, which is still free. There is another tool — The GNU C-Compatible Compiler Preprocessor — which [theoretically can be invoked as `cccp` on Solaris](https://www.opennet.ru/man.shtml?topic=cccp&category=1), but in the wild life I only met C preprocessor invoked as `cpp`.
