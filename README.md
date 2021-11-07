# CCCP

Applications and automation scripts often use `xclip`, `xsel`, `wl-clipboard`, `pbcopy` and different alternatives to access clipboard.
CCCP aims to be united frontend for them, allowing to free other users and developers from selecting or detecting them.

This tool was initially created for personal use. But you are welcome to contribute, report issues, suggest features, etc.
I have almost no time to maintain and develop it beyound my personal needs, so the most welcome requests are those coming with pull requests =).

## Usage

* `cccp c` reads `STDIN` and copies it to the clipboard
* `cccp p` pastes from the clipboard to `STDOUT`
* `cccp ac ... ... ...` (Arg Copy) copies `... ... ...` to the clipboard
* `cccp cf ...` (Copy File) copies `...` file contents to the clipboard

## Installation & Configuration

### Installation

`cccp` can be easily symlinked to any location you already have in your `$PATH`, e.g. `~/.local/bin` (this is how I use it).

CCCP is not a standalone tool. For the most platforms, it also depends on tools, which are not always installed by default:

* Linux — `xclip` and/or `wl-clipboard`, depending on your environment.
* Android with Termux — [`termux-api` package](https://github.com/termux/termux-api-package) + [Termux:API](https://github.com/termux/termux-api)
* Windows — any Bash (Cygwin, MSYS, etc.) with `dos2unix` and PowerShell (now it is usually available out of the box).
* Any Unix-like OS accessed remotely via SSH or Telnet – Python 3+ to interact with local clipboard via OSC 52 terminal sequences.

### Configuration

With zero configuration it tries to autodetect the backend. However you can either override or help it (to run faster) by placing simple configuration file like

```
BACKEND=wayland
```

named `~/.config/cccp.conf` (or `$XDG_CONFIG_HOME/cccp.conf` if you have `$XDG_CONFIG_HOME`).

#### Hacker notes 🧔🏻‍♂

* You can temporarily override backend via environment as follows: `CCCP_BACKEND=whatever cccp ...`
* `cccp.conf` is just a shell script, so you can place some logic here, e.g. switchng between XOrg and Wayland in Linux (see `cccp` script itself), etc.
* Like Midnight Commander and its dummy editor? Then paste to it in ant way your terminal allows, and automatically translate its clipfile to the clipboard with `[fswatch](https://github.com/emcrisostomo/fswatch) -0 $XDG_DATA_HOME/mc/mcedit/mcedit.clip | xargs -0 -n 1 cccp cf`

#### OSC 52

Probably the most sane way to deal with clipboard on *remote* hosts is to bridge *local* (where the human is) clipboard to remote apps.
And it is possible.

**Security Note**

*Clipboard sharing is, for example, supported by XWindows apps bridged through SSH for many years.
Console apps can also access clipboard if your terminal supports and accepts
[OSC 52 control sequences](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Operating-System-Commands).
[Many terminals do](https://www.reddit.com/r/vim/comments/k1ydpn/a_guide_on_how_to_copy_text_from_anywhere/).
XWindows apps are now rarely bridged via SSH, but SSHing to the remote shell is quite common.
And that's why clipboard sharing can not be considered 100% safe: imagine yourself using SSH to log into some server with
a sort of hacked shell or other malware running.
If your terminal accepts OSC 52, then this remote malware can insensibly read your local clipboard.
In my opinion the most proper way to handle it is asking user, for example once per session, if (s)he wants to enable OSC 52.
But the only way to manage it I saw was changing usual persistent terminal settings.
So using CCCP or not, use your terminal with care =).*

OSC 52 is supported in CCCP with two helper scripts in Python 3 (thus requiring Python 3 to be installed).
To activate it, tune CCCP, as described above, setting `BACKEND=osc52`. Because of above particularities, this backend is not autodetected.

Also tune your local terminal (considering security note above). For example, my favorite [Kitty](https://sw.kovidgoyal.net/kitty/) can be either tuned via `kitty.conf` for:

* Just copying from remote hosts: `clipboard_control write-primary write-clipboard no-append`
* Copying from and pasting to remote hosts: `clipboard_control write-primary write-clipboard no-append read-primary read-clipboard`;
  new options `read-primary-ask read-clipboard-ask` to ask user about paste will be
  [hopefully introduced soon](https://github.com/kovidgoyal/kitty/commit/b1322fbe04d31b5bf2f91ab2c03056664f9fe351).

## Name

CCCP – Common Clipboard Copy &amp; Paste. Those who know Russian may also read it as [«СССР», which is 'USSR' in Russian](https://en.wikipedia.org/wiki/Soviet_Union) ☭🐻 =).

The reason behind the name was to find some short abbrevation, which is still free. There is another tool — The GNU C-Compatible Compiler Preprocessor — which [theoretically can be invoked as `cccp` on Solaris](https://www.opennet.ru/man.shtml?topic=cccp&category=1), but in the wild life I only met C preprocessor invoked as `cpp`.

## Related Work

No doubt this tool is not the first one in its family.
For example [this one](https://github.com/sindresorhus/clipboard-cli) can be found easily.
Comparing to it, the idea behind CCCP was to keep it as lightweight as possible.
