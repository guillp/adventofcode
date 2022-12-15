from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path

content = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

with open("07.txt", "rt") as finput:
    content = finput.read()


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    path: Path
    files: list[File]
    subs: list[Path]

    @property
    def size(self):
        return sum(file.size for file in self.files)


@dataclass
class FileSystem:
    dirs: dict[Path, Directory]

    def size(self, path: Path):
        dir = self.dirs[path]
        s = dir.size
        for sub in dir.subs:
            s += self.size(sub)
        return s

    def __iter__(self):
        for dir in self.dirs:
            yield dir, self.size(dir)


def iter_filesystem(content: str):
    cwd = Path("/")
    lines = content.splitlines()
    while lines:
        line = lines.pop(0)
        if line == "$ cd /":
            cwd = Path("/")
        elif line == "$ cd ..":
            cwd = cwd.parent
        elif line == "$ ls":
            files = []
            subs = []
            while lines:
                if lines[0].startswith("$ "):
                    break
                size, name = lines.pop(0).split()
                if size == "dir":
                    subs.append(cwd / name)
                else:
                    files.append(File(name, int(size)))

            yield Directory(cwd, files, subs)
        elif line.startswith("$ cd"):
            target = line.removeprefix("$ cd ")
            cwd = cwd / target
        else:
            assert False, line


fs = FileSystem({dir.path: dir for dir in iter_filesystem(content)})
print({dir: size for dir, size in fs})

s = 0
for dir, size in fs:
    if size < 100000:
        s += size
print(s)

free_space = 70000000 - fs.size(Path("/"))
size_to_free = 30000000 - free_space

for dir, size in sorted(fs, key=itemgetter(1)):
    if size > size_to_free:
        print(size)
        break
