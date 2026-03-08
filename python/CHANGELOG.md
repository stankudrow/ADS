# Python Algorithms and Data Structures

## v0.7.0

- Add the `Heap` (max and min) data structure.
- Add the `heap_sort`.
- Update docstrings.
- Update imports (searching algorithms).
- Update tests.

Infrastructure:

- pre-commit is removed in favour of CI/CD

## v0.6.0

Reconsider linked lists:

- introduce the SinglyLinkedList
- rework the DoublyLinkedList
- lists are in a separated "lists" directory now -> import updated
- tests revised

## v0.5.0

Fixes the v0.4.0 with some breaking changes.

- Add the `rotate` method to the Deque.
- Make the Deque's `__repr__` method and the `maxlen` property more consistent with the Python's `deque`.
- Reorganise modules.
- Simplify tests.
- Groom the doc comments for "Justfile" recipes.

Bug: the v0.4.1 in the "uv.lock" file - not critical, but inconvenient.

## v0.4.0 (DISCOURAGED)

The implementation of the Deque data structure:

- is incomplete because the `rotate` method implementation is missing
- has discrepancy in comparison with the standard `deque` structure.

Please have a look at the v0.5.0 changelog.

Code:

- Add the "Deque" data structure that enjoys the DoublyLinkedList under the hood.
- Add `__(i)add__`, `__(i)mul__` operations, `__copy__`, `index` and comparision operations via `functools.total_ordering`.
- Update `DoublyLinkedList` (major fixes).
- Lint the `quick_sort` function.
- Update imports.

Infrastructure:

- Replace "Makefile" with "Justfile".
- Update the GHA workflow.
- Update tests.
- Update dependencies.
- Add more "ruff" rules.

## v0.3.0

- Add "F" (pyflakes) rules in effect.
- Change the `__reversed__` method for the `DoublyLinkedList` data structure.

## v0.2.0

- Add "mypy" type checker support.
- Add the `DoublyLinkedList` data structure.
- Extend the set of "ruff" rules
- Lint the code with "mypy" and "ruff".

## v0.1.0

- Common:
  - Python 3.10 as the minimum version.
  - Project manager - [uv>=0.5.10](https://pypi.org/project/uv/).
  - Project (development) configurations and dependencies:
    - formatting and linting - [ruff>=0.9.1](https://pypi.org/project/ruff/);
    - testing framework - [pytest>=8.3.4](https://pypi.org/project/pytest/) with some plug-ins.
  - Git hooks via [pre-commit>=4.1.0](https://pre-commit.com/);
  - Project command (line) automation via [GNU make](https://www.gnu.org/software/make/) (if available).
  - GitHub Actions enabled.
  - The "adspy" project is installable via Python package managers.

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
