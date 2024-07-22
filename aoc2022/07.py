from collections.abc import Iterator
from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path


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
    def size(self) -> int:
        return sum(file.size for file in self.files)


@dataclass
class FileSystem:
    directories: dict[Path, Directory]

    def size(self, path: Path) -> int:
        directory = self.directories[path]
        s = directory.size
        for sub in directory.subs:
            s += self.size(sub)
        return s

    def __iter__(self) -> Iterator[tuple[Path, int]]:
        for directory in self.directories:
            yield directory, self.size(directory)


def iter_filesystem(content: str) -> Iterator[Directory]:
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


def solve(content: str) -> Iterator[int]:
    fs = FileSystem({d.path: d for d in iter_filesystem(content)})

    part1 = 0
    for directory, size in fs:
        if size < 100000:
            part1 += size
    yield part1

    free_space = 70000000 - fs.size(Path("/"))
    size_to_free = 30000000 - free_space

    for directory, size in sorted(fs, key=itemgetter(1)):
        if size > size_to_free:
            yield size
            return


test_content = """\
$ cd /
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

assert tuple(solve(test_content)) == (95437, 24933642)

with open("07.txt") as finput:
    content = finput.read()
for part in solve(content):
    print(part)
