# API Reference

## POST /optimize

This endpoint performs optimization using the `TTOpt` class.

### Request Body

The request body should be a JSON object with the following fields:

- `dimensions` (int, optional): Number of function dimensions. Default is `100`.
- `lowerBound` (float, optional): Grid lower bound. Default is `-10.0`.
- `upperBound` (float, optional): Grid upper bound. Default is `10.0`.
- `gridSizeFactorP` (int, optional): The grid size factor (there will be `p^q` points). Default is `2`.
- `gridSizeFactorQ` (int, optional): The grid size factor (there will be `p^q` points). Default is `12`.
- `evals` (float, optional): Number of function evaluations. Default is `1.E+5`.
- `funcName` (string, optional): Name of the function to optimize. Default is `Simple`. Possible values are:
    - `Alpine`: \( f(x) = \sum |\sin(x) \cdot x + 0.1 \cdot x| \), \( x \in [-10, 10] \)
      ```python
      def f(X):
          return np.sum(np.abs(X * np.sin(X) + 0.1 * X), axis=1)
      ```
    - `Simple`: \( f(x) = \sin(0.1 \cdot x[0])^2 + 0.1 \cdot \sum x[1:]^2 \), \( x \in [-1, 1] \)
      ```python
      def f(X):
          return np.sin(0.1 * X[:, 0])**2 + 0.1 * np.sum(X[:, 1:]**2, axis=1)
      ```
    - `Tensor`: \( f(i) = (i[0] - 2)^2 + (i[1] - 3)^2 + \sum i[2:]^4 \), \( i \in [0, 1, 2, 3] \)
      ```python
      def f(I):
          return (I[:, 0] - 2)**2 + (I[:, 1] - 3)**2 + np.sum(I[:, 2:]**4, axis=1)
      ```
    - `Rosenbrock`: \( f(x) = \sum 100 \cdot (x[i+1] - x[i]^2)^2 + (1 - x[i])^2 \), \( x \in [-2.048, 2.048] \)
      ```python
      def f(X):
          return np.sum(100 * (X[:, 1:] - X[:, :-1]**2)**2 + (1 - X[:, :-1])**2, axis=1)
      ```
    - `Rastrigin`: \( f(x) = 10 \cdot d + \sum x[i]^2 - 10 \cdot \cos(2 \cdot \pi \cdot x[i]) \), \( x \in [-5.12, 5.12] \)
      ```python
      def f(X):
          return 10 * X.shape[1] + np.sum(X**2 - 10 * np.cos(2 * np.pi * X), axis=1)
      ```
    - `Sphere`: \( f(x) = \sum x^2 \), \( x \in [-5.12, 5.12] \)
      ```python
      def f(X):
          return np.sum(X**2, axis=1)
      ```
    - `Styblinski-Tang`: \( f(x) = 0.5 \cdot \sum x^4 - 16 \cdot x^2 + 5 \cdot x \), \( x \in [-5, 5] \)
      ```python
      def f(X):
          return 0.5 * np.sum(X**4 - 16 * X**2 + 5 * X, axis=1)
      ```
- `isFunc` (bool, optional): Whether the function is a callable. Default is `True`.
- `isVect` (bool, optional): Whether the function is vectorized. Default is `True`.
- `withCache` (bool, optional): Whether to use caching. Default is `False`.
- `withLog` (bool, optional): Whether to log the optimization process. Default is `True`.
- `withOpt` (bool, optional): Whether to use optimization. Default is `False`.

### Response

The response will be a JSON object with the following field:

- `minimum_value` (string): Information about the optimization result.

### Example

#### Request
```json
{
    "dimensions": 10,
    "lowerBound": -10.0,
    "upperBound": 10.0,
    "gridSizeFactorP": 2,
    "gridSizeFactorQ": 12,
    "evals": 100000,
    "funcName": "Alpine",
    "isFunc": true,
    "isVect": true,
    "withCache": false,
    "withLog": true,
    "withOpt": false
}
```

#### Response
```json
{
    "minimum_value": "Optimization result information"
}
```

