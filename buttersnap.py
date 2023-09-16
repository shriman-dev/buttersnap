#!/usr/bin/env python3
import os
import datetime
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Simple CLI tool for taking Btrfs Snapshots.')

parser.add_argument("-k", "--keep-snapshots", type=int, default=10, metavar="N",
                    help="Keep defined number of snapshots and auto-remove older ones. Disable removal of older snapshots by setting value to 0. (Default: %(default)s)")
parser.add_argument("--sub-dir", type=str, metavar="NAME",
                    help="Specify sub-directory to organize snapshots.")
parser.add_argument('--read-only', metavar="BOOL", action="store", default=True,
                    help="Takes a Boolean value. 'False' enables writable snapshots. (Default: %(default)s)")
parser.add_argument("-s", "--src-subvolume", type=str, nargs=1, required=True, metavar=("PATH"),
                    help="Path to the source subvolume to take snapshots.")
parser.add_argument("-d", "--dst-subvolume", type=str, nargs=1, metavar=("PATH"),
                    help="Path to the destination subvolume to hold snapshots. By default, '.ButterSnap' subvolume will be created inside source subvolume when no path is specified.")

args = parser.parse_args()

def is_root():
    if not os.geteuid() == 0:
        print('Error: Requires root access to create or remove BTRFS snapshots.')
        exit(1)


def take_snapshot(ro, src, dst):
    try:
        subprocess.run(f'btrfs subvolume snapshot {ro} {src} {dst}', shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to take snapshot")


def remove_snapshot(snap_path):
    try:
        subprocess.run(f'btrfs subvolume delete {snap_path}', shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to remove snapshot")


def ro_flag():
    if args.read_only == True:
        return '-r'
    else:
        return ''


def prepare_destination():
    src_path = args.src_subvolume[0]
    if args.dst_subvolume:
        dst_path = args.dst_subvolume[0]
        not os.path.isdir(dst_path) and subprocess.run(f'btrfs subvolume create {dst_path}', shell=True, check=True)
    else:
        dst_path = os.path.join(src_path, '.ButterSnap')
        not os.path.isdir(dst_path) and subprocess.run(f'btrfs subvolume create {dst_path}', shell=True, check=True)

    if args.sub_dir:
        dst_path = os.path.join(dst_path, args.sub_dir)
        not os.path.isdir(dst_path) and os.makedirs(dst_path, exist_ok=True)

    return dst_path

#make function to sortdir

def take_numbered_snapshots(ro, src, dst):
    dt = datetime.datetime.now().strftime('%H-%M_%d-%m-%Y')
    list_old_to_new = sorted(os.listdir(dst), key=lambda x: os.path.getmtime(os.path.join(dst, x)), reverse=False)
    create_numbered_dir = int(os.listdir(dst) and list_old_to_new[-1] or 0) + 1
    os.mkdir(os.path.join(dst, str(create_numbered_dir)))
    get_newest_numbered_dir = os.path.join(dst, os.listdir(dst)[-1])
    take_snapshot(ro, src, f'{get_newest_numbered_dir}/{dt}')


def remove_older_snapshots(dst, keep):
    if len(os.listdir(dst)) > keep:
       list_old_to_new = sorted(os.listdir(dst), key=lambda x: os.path.getmtime(os.path.join(dst, x)), reverse=False)
       for i in range(len(os.listdir(dst)) - keep):
           remove_snapshot(f'{os.path.join(dst, list_old_to_new[i])}/*')
           os.rmdir(os.path.join(dst, list_old_to_new[i]))


if __name__ == "__main__":
    is_root()
    src_path = args.src_subvolume[0]
    dst_path = prepare_destination()
    ro = ro_flag()
    take_numbered_snapshots(ro, src_path, dst_path)
    if args.keep_snapshots:
        remove_older_snapshots(dst_path, args.keep_snapshots)


