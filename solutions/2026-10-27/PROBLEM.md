# Problem: shutil.rmtree to remove readonly files

**Date:** 2026-10-27

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

I want to use shutil.rmtree in Python to remove a directory. The directory in question contains a .git control directory, which git marks as read-only and hidden. The read-only flag causes rmtree to fail. In Powershell, I would do "del -force" to force removal of the read-only flag. Is there an equivalent in Python? I'd really rather not walk the whole tree twice, but the onerror argument to rmtree doesn't seem to retry the operation, so I can't use def set_rw(operation, name, exc): os.chmod(nam

## Original URL

https://stackoverflow.com/questions/21261132/shutil-rmtree-to-remove-readonly-files
