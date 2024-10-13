# tq_backend

Welcome to the TQ SDK documentation. This SDK provides tools and libraries to help you develop applications efficiently.

## Table of Contents

- [tq\_backend](#tq_backend)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
  - [API Reference](#api-reference)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

The TQ SDK is designed to simplify the development process by providing a comprehensive set of tools and libraries.

## Installation

To install the TQ SDK, use the following command:

```bash
pip install tq-sdk
```

## Usage

Here is a basic example of how to use the TQ SDK:

```python
import tq_backend

# Your code here
```

## API Reference

For detailed API documentation, please refer to the [API Reference](docs/api_reference.md).
<!-- ######## set of different functions ########
# Alpine function
# f(x) = sum(abs(x * sin(x) + 0.1 * x)), x in [-10, 10]
# eg.
# def f(X):
#   return np.sum(np.abs(X * np.sin(X) + 0.1 * X), axis=1)
########
# Simple function
# f(x) = sin(0.1 * x[0])**2 + 0.1 * sum(x[1:]**2), x in [-1, 1] 
# eg. 
# def f(X):
#   return np.sin(0.1 * X[:, 0])**2 + 0.1 * np.sum(X[:, 1:]**2, axis=1)
########
# Tensor function
# f(i) = (i[0] - 2)**2 + (i[1] - 3)**2 + sum(i[2:]**4), i in [0, 1, 2, 3]
# eg.
# def f(I):
#   return (I[:, 0] - 2)**2 + (I[:, 1] - 3)**2 + np.sum(I[:, 2:]**4, axis=1)
########
# Rosenbrock function
# f(x) = sum(100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2), x in [-2.048, 2.048]
# eg.
# def f(X):
#   return np.sum(100 * (X[:, 1:] - X[:, :-1]**2)**2 + (1 - X[:, :-1])**2, axis=1)
########
# Rastrigin function
# f(x) = 10 * d + sum(x[i]**2 - 10 * cos(2 * pi * x[i])), x in [-5.12, 5.12]
# eg.
# def f(X):
#   return 10 * X.shape[1] + np.sum(X**2 - 10 * np.cos(2 * np.pi * X), axis=1)
########
# Sphere function
# f(x) = sum(x**2), x in [-5.12, 5.12]
# eg.
# def f(X):
#   return np.sum(X**2, axis=1)
########
# Styblinski-Tang function
# f(x) = 0.5 * sum(x**4 - 16 * x**2 + 5 * x), x in [-5, 5]
# eg.
# def f(X):
#   return 0.5 * np.sum(X**4 - 16 * X**2 + 5 * X, axis=1)
########
#
# -->

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
