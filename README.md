# ButterSnap

Simple CLI tool for taking Btrfs Snapshots.

## Overview

This tool allows you to create, set limit for auto-removal and organize snapshots in specified sub-directories. It is designed to be very minimal and provides a simple way to work with Btrfs snapshots.

## Options

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
usage: buttersnap [-h] [-k N] [--sub-dir NAME] [--read-only BOOL] -s PATH [-d PATH]

Simple CLI tool for taking Btrfs Snapshots.

options:
  -h, --help            show this help message and exit
  -k N, --keep-snapshots N
                        Keep defined number of snapshots and auto-remove older ones.
                        Disable removal of older snapshots by setting value to 0. (Default: 10)
  --sub-dir NAME        Specify sub-directory to organize snapshots.
  --read-only BOOL      Takes a Boolean value. 'False' enables writable snapshots. (Default: True)
  -s PATH, --src-subvolume PATH
                        Path to the source subvolume to take snapshots.
  -d PATH, --dst-subvolume PATH
                        Path to the destination subvolume to hold snapshots. By default,
                        '.ButterSnap' subvolume will be created inside source subvolume
                        when no path is specified.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Dependencies
* btrfs-progs

## Install

```
git clone https://github.com/shriman-dev/buttersnap.git
cd buttersnap
sudo cp buttersnap.py /usr/bin/buttersnap
buttersnap --help
```

## Usage & Examples

### Take snapshot in specified sub-directory

```
sudo buttersnap --sub-dir manually -s /home/
```

Output:

```
Create subvolume '/home/.ButterSnap'
Create a readonly snapshot of '/home/' in '/home/.ButterSnap/manually/1/13-47_16-09-2023'
```

### Take snapshot of custom subvolume to custom location

For example we have a subvolume mounted on /etc

```
sudo buttersnap -s /etc -d /etc-snaps
```

Output:

```
Create subvolume '//etc-snaps'
Create a readonly snapshot of '/etc' in '/etc-snaps/1/13-50_16-09-2023'
```

### Take periodic snapshots with crontab

run

```
sudo crontab -e
```

hourly snapshots of root /

```
0 * * * * /usr/bin/buttersnap -k 24 --sub-dir hourly -s /
```

daily snapshots of root /

```
0 0 * * * /usr/bin/buttersnap -k 7 --sub-dir daily -s /
```

### For systemd-timers you can refer to arch wiki

[Systemd/Timers](https://wiki.archlinux.org/title/systemd/Timers)

Also

[get systemd service and timers sample files](https://github.com/shriman-dev/buttersnap/tree/main/systemd-sample)
