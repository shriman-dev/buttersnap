# ButterSnap
Simple CLI tool for taking Btrfs Snapshots.

## Overview
This tool allows you to create, set limit for auto-removal and organize snapshots in specified sub-directories. It is designed to be very minimal and provides a simple way to work with Btrfs snapshots.

## Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
usage: ButterSnap.py [-h] [-k N] [--sub-dir NAME] [--read-only BOOL] -s PATH [-d PATH]

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
