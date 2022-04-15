# CCCP

Applications and automation scripts often use `xclip`, `xsel`, `wl-clipboard`, `pbcopy` and different alternatives to access clipboard.
CCCP aims to be united frontend for them, allowing to free other users and developers from selecting or detecting them.

This tool was initially created for personal use. But you are welcome to contribute, report issues, suggest features, etc.
I have almost no time to maintain and develop it beyound my personal needs, so the most welcome requests are those coming with pull requests =).

## Usage

* `cccp c` reads `STDIN` and copies it to the clipboard.
* `cccp p` pastes from the clipboard to `STDOUT`.
* `cccp ca ... ... ...` (Copy Args) copies `... ... ...` to the clipboard.
  * also `cccp ac ... ... ...` (Arg Copy)
* `cccp cf ...` (Copy File) copies `...` file contents to the clipboard.
  * also `cccp fc ...` (File Copy)
* `cccp t` (killer-feature!) converts clipboard to plain text, working as `cccp p | cccp c`.

## Installation & Configuration

### Installation

`cccp` can be easily symlinked to any location you already have in your `$PATH`, e.g. `~/.local/bin` (this is how I use it).

CCCP is not a standalone tool. For the most platforms, it also depends on tools, which are not always installed by default:

* Linux — `xclip` and/or `wl-clipboard`, depending on your environment.
* Android with Termux — [`termux-api` package](https://github.com/termux/termux-api-package) + [Termux:API](https://github.com/termux/termux-api)
* Windows:
  * CygWin and MSYS(2) (including Git Bash) using their own nice `/dev/clipboard` that requires nothing more;
  * any other Windows Bash'es, with `dos2unix` installed and PowerShell (now it is usually available out of the box).
* Any Unix-like OS accessed remotely via SSH or Telnet – Python 3+ to interact with local clipboard via OSC 52 terminal sequences.

To install helper backends, run `git submodule update --init --recursive .` in repo directory.

### Configuration

With zero configuration it tries to autodetect the backend. However you can either override or help it (to run faster) by placing simple configuration file like

```
BACKEND=wayland
```

named `~/.config/cccp.conf` (or `$XDG_CONFIG_HOME/cccp.conf` if you have `$XDG_CONFIG_HOME`).

#### Hacker notes 🧔

* You can temporarily override backend via environment as follows: `CCCP_BACKEND=whatever cccp ...`.
* `cccp.conf` is just a shell script, so you can place some logic here, e.g. switchng between XOrg and Wayland in Linux (see `cccp` script itself), etc.
* Fan of oldschool editors?
  * Like Midnight Commander and its built-in editor as I do? Find `$XDG_CONFIG_HOME/mc/ini` and edit two settings manually: set `clipboard_store=cccp cf` and 
`clipboard_paste=cccp p`. Make sure MC will not owerwrite it (e.g. quit all MCs and use another editor =)).
  * Like Vi(m) as I do too? =) Then `vnoremap <C-F11> y:call system('cccp c', @")<CR>` or use any other shortcut and register you want.
    * *This does not work on remotes with OSC 52 (see below) likely because vim filters command output aggressively. Then use `vnoremap <C-F10> ::w !cccp c<CR><CR>` — it appears to work, but always copies the whole lines with selection. You can also try to give up on cccp and use [this plugin](https://github.com/fcpg/vim-osc52), but it did not copy in my case.*
  * Like something other only using a clipfile? Then take a look at [`watch_clipfile_to_cccp`](utilities/watch_clipfile_to_cccp).

#### OSC 52

Probably the most sane way to deal with clipboard on *remote* hosts is to bridge *local* (where the human is) clipboard to remote apps.
And it is possible. `BACKEND=osc52` is autodetected for SSH sessions with default safe options.

*TL;DR:* If your local and remote software works fine with it and you need a setting for your headless server, I recommend using just `BACKEND=osc52` with bo additional settings.
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

CCCP – Common Clipboard Copy &amp; Paste. Those who know Russian may also read it as [«СССР», which is 'USSR' in Russian](https://en.wikipedia.org/wiki/Soviet_Union) ☭🐻 =).

The reason behind the name was to find some short abbrevation, which is still free. There is another tool — The GNU C-Compatible Compiler Preprocessor — which [theoretically can be invoked as `cccp` on Solaris](https://www.opennet.ru/man.shtml?topic=cccp&category=1), but in the wild life I only met C preprocessor invoked as `cpp`.

## Related Work

No doubt this tool is not the first one in its family.
For example [this one](https://github.com/sindresorhus/clipboard-cli) can be found easily.
Comparing to it, the idea behind CCCP was to keep it as lightweight as possible.
