<div align="center">
    <pre>
    ██████╗  █████╗  ██████╗ ███████╗██╗     
    ██╔══██╗██╔══██╗██╔════╝ ██╔════╝██║     
    ██████╔╝███████║██║  ███╗█████╗  ██║     
    ██╔══██╗██╔══██║██║   ██║██╔══╝  ██║     
    ██████╔╝██║  ██║╚██████╔╝███████╗███████╗
    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
    ︵‿︵‿୨♡୧‿︵‿︵
    your shortcut to smooth OCaml coding
  </pre>

  [![License: GNU](https://img.shields.io/badge/License-GNU-yellow?style=for-the-badge)](https://www.gnu.org/)
  [![Ocaml: 4.13.1](https://img.shields.io/badge/Ocaml-4.13.1-ee6a1a?style=for-the-badge)](https://ocaml.org/)

</div>

Ocaml syntax is... weird. Let's use a better syntax !

# Overview

#### Type Declarations
```ocaml
let x: int = 1;;

let y = 5;;
```
to

```cpp
int x = 1;

// Type Inference: reducing the need for explicit type declarations
auto y = 5;
```

#### Curly Braces for Scopes
```ocaml
let add (a, b : int * int) {
    a + b
};;

let main () : unit = (
    ...
);;
```
to

```cpp
int add(int a, int b) {
    return a + b;
}

void main() {
    ...
}
```

#### Pointers

```ocaml
let x: int ref = ref 0;;
!x;;
x := 1;
```
to
```cpp
int* x = &0;
x.get();
x.set(1);
```

#### Nullability

```ocaml
let find_value (key : int) : int option;;
let divide (numerator, denominator : int * int) : (int, error) result;;
```
to
```cpp
Option<int> find_value(int key);
Result<int, Error> divide(int numerator, int denominator);
```

# Ideas
```cpp
// Namespaces & class definitions that resemble C++
namespace Math {
    int add(int a, int b) {
        return a + b;
    }
}

class Point {
public:
    int x;
    int y;

    Point(int x, int y) {
        this->x = x;
        this->y = y;
    }

    void move(int dx, int dy) {
        x += dx;
        y += dy;
    }
}

// Recursive functions
#[recursive, debug]
int fibo(int n) {
    if (n <= 1) {
        return n;
    }
    return fibo(n - 1) + fibo(n - 2);
}


// Anonymous functions
auto inc = [](int x) {
    return x + 1;
};

// Maps
auto squares = map([1, 2, 3], [](int x) { return x * 2; });
```

# Notes
While loops are faster than for, local and blocks loops
