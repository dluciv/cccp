# CCCP

[![Shell Check](https://github.com/dluciv/cccp/actions/workflows/shellcheck.yml/badge.svg)](https://github.com/dluciv/cccp/actions/workflows/shellcheck.yml)
[![basher install](https://www.basher.it/assets/logo/basher_install.svg)](https://www.basher.it/)
[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://wtfpl.net/about/)

Applications and automation scripts often use `xclip`, `xsel`, `wl-clipboard`, `pbcopy` and different alternatives to access clipboard.
CCCP (Common Clipboard Copy & Paste) aims to be united frontend for them, allowing to free other users and developers from selecting or detecting them.

This tool was initially created for personal use. But you are welcome to contribute, report issues, suggest features, etc.
I have almost no time to maintain and develop it beyound my personal needs, so the most welcome requests are those coming with pull requests 🤓.

## Usage

* `cccp` displays some help and reports backend used.
* `cccp [switches] c` reads `STDIN` and copies it to the clipboard.
* `cccp [switches] p` pastes from the clipboard to `STDOUT`.
* `cccp [switches] ca ... ... ...` (Copy Args) copies `... ... ...` to the clipboard.
  * also `cccp [switches] ac ... ... ...` (Arg Copy)
* `cccp [switches] cf ...` (Copy File) copies `...` file contents to the clipboard.
  * also `cccp [switches] fc ...` (File Copy)
* `cccp [switches] e` edits clipboard with `$VISUAL`, if set, else with `$EDITOR`
* `cccp [switches] t` (killer-feature!) converts clipboard to plain text, working as `cccp p | cccp c`.
* `cccp u` tries to update itself.

### Switches
* `-p` or `--primary` work with primary selection for backends supporting it (and get error for others).
* `-c` or `--clipboard` work with clipboard (default for backends currently supported).
* `-a` or `--append` append to the end of clipboard (experimental, for the most backends, just copies input to the end of paste).

As CCCP stands for Common Clipboard Copy & Paste, there are also example symlinks in repository,
named `ccap` (... *append* & paste), `cpcp` (common *primary* ...) and `cpap` (common primary append & paste), which
do the work in the way like they already received corresponding switches.
This slightly resembles LISP ([`car`, `cdr`, `cdr`, ...](https://en.wikipedia.org/wiki/CAR_and_CDR)) and
[BusyBox](https://en.wikipedia.org/wiki/BusyBox) (single executable) approaches and can probably shorten CCCP invokation.
However I believe this is rarely needed feature.

## Installation & Configuration

### Installation

#### Manually with Git

You can simply install CCCP by cloning this repository somewhere you like. Then `cccp` can be easily symlinked to any location
you already have in your `$PATH`, e.g. `~/.local/bin` (this is how I use it). When invoked as `cccp u`, it will even try to update itself.
This is also up to you to also symlink `cccp` as `ccap`, `cpcp` and `cpap`.

#### With Basher

If you use [*basher*](https://www.basher.it/) (which I am not a big fan of, but it looks promising overall), you can install CCCP with
`basher install dluciv/cccp` or `basher install github.com/dluciv/cccp`. Then you can further manage (e.g. upgrade, uninstall)
CCCP with basher. Basher appears to be smart enough to handle `ccap`, `cpcp` and `cpap` perfectly, thus creating multiple links
to all of them.

#### Dependencies / Helpers

CCCP is not a standalone tool. For the most platforms, it also depends on tools, which are not always installed by default:

* Linux and FreeBSD running Xorg, X11 and Wayland — `xclip` and/or `wl-clipboard`, depending on your environment.
* Android with Termux — [`termux-api` package](https://github.com/termux/termux-api-package) + [Termux:API](https://github.com/termux/termux-api)
* Windows:
  * CygWin and MSYS(2) (including Git Bash), using their own nice `/dev/clipboard` that does not require anything more;
  * WSL, using PowerShell and requiring `dos2unix` to be installed;
  * any other Windows Bash'es, with above `dos2unix` and PowerShell.
* Any Unix-like OS accessed remotely via SSH or Telnet – Python 3+ to interact with local clipboard via OSC 52 terminal sequences.

To install helper backends, run `git submodule update --init --recursive .` in repo directory.

### Configuration

With zero configuration it tries to autodetect the backend. However you can either override or help it (to run faster) by placing simple configuration file like

```
BACKEND=wayland
```

named `~/.config/cccp.conf` (or `$XDG_CONFIG_HOME/cccp.conf` if you have `$XDG_CONFIG_HOME`).

Also with zero configuration it assumes encoding to be UTF-8. This is important because without specifying mime type, some backends like
`wl-clipboard` or `wayclip` can turn normal Unicode text to `\uXXXX\uXXXX\uXXXX...` when pasting to PTY, e.g. file.
As UTF-8 is now usually used everywhere when ASCII is not enough (e.g. almost everywhere), CCCP by default tells them to use `text/plain;charset=utf-8`.
But you may prefer, for example, `KOI8-R` encoding for your system. I have even seen some people having `LC_ALL=ru_RU.CP1251`, so if they
want to use CCCP, they should place `MIME='text/plain;charset=windows-1251'` or `MIME='text/plain;charset=koi8-r'`, and so on in `cccp.conf`.

#### Hacker notes 🧔

* You can temporarily override backend and/or MIME via environment as follows: `CCCP_BACKEND=whatever CCCP_MIME='text/plain;charset=whatever' cccp ...`.
* `cccp.conf` is just a shell script, so you can place some logic here, e.g. switchng between XOrg and Wayland in Linux (see `cccp` script itself), etc.
* Fan of oldschool editors?
  * Like Midnight Commander and its built-in editor as I do? Find `$XDG_CONFIG_HOME/mc/ini` and edit two settings manually: set `clipboard_store=cccp cf` and 
`clipboard_paste=cccp p`. Make sure MC will not owerwrite it (e.g. quit all MCs and use another editor to edit MC's ini file 🤓).
  * Like Vi(m) as I do too? =) Then `vnoremap <C-F11> y:call system('cccp c', @")<CR>` or use any other shortcut and register you want.
    * *This does not work on remotes with OSC 52 (see below) likely because vim filters command output aggressively. Then use `vnoremap <C-F10> ::w !cccp c<CR><CR>` — it appears to work, but always copies the whole lines with selection. You can also try to give up on cccp and use [this plugin](https://github.com/fcpg/vim-osc52), but it did not copy in my case.*
  * Like something other only using a clipfile? Then take a look at [`watch_clipfile_to_cccp`](utilities/watch_clipfile_to_cccp).

#### OSC 52

Probably the most sane way to deal with clipboard on *remote* hosts is to bridge *local* (where the human is) clipboard to remote apps.
And it is available in CCCP: `BACKEND=osc52` is autodetected for SSH sessions with default safe options.

*TL;DR:* If your local and remote software works fine with it and you need a setting for your headless server, I recommend using just `BACKEND=osc52` with no additional settings.
This allows to copy, and you can paste yourself using your terminal menu, Ctrl+V, Cmd+V, Shift+Insert or any other way you used before.

**Security Note**

Enabling pasting via OSC 52 allows **remote** software to read your **local** clipboard insensibly.
It doesn't matter if you use CCCP at all or not, it is only related to your terminal settings.
Thus make sure you only enable it on completely trusted servers.

For example, my favorite [Kitty](https://sw.kovidgoyal.net/kitty/) can be either tuned via `kitty.conf` for:

* Just copying from remote hosts: `clipboard_control write-primary write-clipboard no-append`.
* Copying from and pasting to remote hosts: `clipboard_control write-primary write-clipboard no-append read-primary read-clipboard`.
* The safer options (instead of above last two) `... read-primary-ask read-clipboard-ask` introduced in kitty [0.24.0](https://github.com/kovidgoyal/kitty/releases/tag/v0.24.0) to [ask user about paste](https://github.com/kovidgoyal/kitty/issues/4022).

**So What?**

Above *TL;DR:* note is still relevant. If you want to go deeper, OSC 52 backend has 3 additional options which can be either tuned via environment or `cccp.conf`.

* `OSC52_ALLOW_PASTE=false|true`, default is `false`. When true, allows pasting. Use with care!
* `OSC52_SHELL_COPY=true|false`, default is `true`. CCCP actually uses two sub-backends for OSC 52:
  * Python module, which requires Python 3 to be installed, and allows the both copying and pasting;
  * built-in piece of shell code (enabled by default with this option) which is only capable of copying and
    is very portable because only depends on `base64` tool which available almost everywhere; to paste,
    above Python module is used.
* `OSC52_BYPASS_MUX=true|false`, default is `true`. When true, tells shell sub-backend to push copy operation
  through terminal multiplexor. tmux and GNU Screen are supported. Python backend has this option always enabled.

You can use above sub-backend options even without specifying the backend, so that they will only be applied when `osc52` backend is autodetected.
This is useful for hosts, which a logged on both locally and remotely: in my case, one of my laptops and (sic!) my mobile.

## Name

CCCP – Common Clipboard Copy &amp; Paste. Those who know Russian may also read it as [«СССР», which is 'USSR' in Russian](https://en.wikipedia.org/wiki/Soviet_Union) ☭🐻🤓.

The reason behind the name was to find some short abbrevation, which is free. I have found some usages of this name years before:

* [Combined Community Codec Pack](http://web.archive.org/web/20211009205455/http://www.cccp-project.net/) — great one, but not expected in the wild any more; also named after USSR;
* the GNU C-Compatible Compiler Preprocessor — which [theoretically can be invoked as `cccp` on Solaris](https://www.opennet.ru/man.shtml?topic=cccp&category=1), but in the wild I only met C preprocessor invoked as `cpp`.

So *this CCCP* now definitely looks more alive than others, and can use this famous name, paying respect to its great predecessors though.

## Related Work

No doubt this tool is not the first one in its family.
For example [this one](https://github.com/sindresorhus/clipboard-cli) can be found easily.
Comparing to it, the idea behind CCCP was to keep it as lightweight as possible.
