#!/bin/bash

sudo rsync --archive --verbose --delete /home/maintainer/immich-app/gallery /mnt/backup/immich-app 
sudo rsync --archive --verbose --delete /home/maintainer/immich-app/postgres /mnt/backup/immich-app 
