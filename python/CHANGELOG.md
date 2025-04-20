# Python Algorithms and Data Structures

## v0.3.0

Added:

- "pyflakes" rules
- `__reversed__()` protocol for DoublyLinkedList

## v0.2.0

Added:

- `mypy` type checker
- DoublyLinkedList data structure

Changed

- Extend the set of `ruff` rules
- The code linted in accordance with `mypy` and `ruff` rules.

## v0.1.0

The project is an (pip-)installable package.

Added:

- Common:
  - Python 3.10 as the minimum version.
  - Project manager - [uv>=0.5.10](https://pypi.org/project/uv/).
  - Project (development) configurations and dependencies:
    - formatting and linting - [ruff>=0.9.1](https://pypi.org/project/ruff/);
    - testing framework - [pytest>=8.3.4](https://pypi.org/project/pytest/) with some plug-ins.
  - Git hooks via [pre-commit>=4.1.0](https://pre-commit.com/);
  - Project command (line) automation via [GNU make](https://www.gnu.org/software/make/) (if available).
  - GitHub Actions enabled.

- Algorithms:
  - Sorting:
    - [Bubble sort](https://en.wikipedia.org/wiki/Bubble_sort);
    - [Insertion sort](https://en.wikipedia.org/wiki/Insertion_sort);
    - [Merge sort](https://en.wikipedia.org/wiki/Merge_sort);
    - [Quick sort](https://en.wikipedia.org/wiki/Quicksort);
    - [Selection sort](https://en.wikipedia.org/wiki/Selection_sort).

  - Searching:
    - [Binary search](https://en.wikipedia.org/wiki/Binary_search);
    - [Linear search](https://en.wikipedia.org/wiki/Linear_search).
