from flask import Flask, request, jsonify  # Import necessary Flask modules
from flask_cors import CORS
from ttopt import TTOpt  # Import the TTOpt class for optimization
import numpy as np  # Import numpy for numerical operations
from threading import Lock  # Import Lock for thread safety

app = Flask(__name__)  # Initialize the Flask application
CORS(app)  # Enable CORS for all routes

np.random.seed(42)  # Set a random seed for reproducibility

rank = 4  # Maximum TT-rank while cross-like iterations

# Define a dictionary to map function names to their implementations
functions = {
    "Alpine": lambda X: np.sum(np.abs(X * np.sin(X) + 0.1 * X), axis=1),
    "Simple": lambda X: np.sin(0.1 * X[:, 0])**2 + 0.1 * np.sum(X[:, 1:]**2, axis=1),
    "Tensor": lambda I: (I[:, 0] - 2)**2 + (I[:, 1] - 3)**2 + np.sum(I[:, 2:]**4, axis=1),
    "Rosenbrock": lambda X: np.sum(100 * (X[:, 1:] - X[:, :-1]**2)**2 + (1 - X[:, :-1])**2, axis=1),
    "Rastrigin": lambda X: 10 * X.shape[1] + np.sum(X**2 - 10 * np.cos(2 * np.pi * X), axis=1),
    "Sphere": lambda X: np.sum(X**2, axis=1),
    "Styblinski-Tang": lambda X: 0.5 * np.sum(X**4 - 16 * X**2 + 5 * X, axis=1)
}
##

# Function to select the appropriate function based on the name
def f(x):
    func_name = request.json.get('funcName', 'Alpine')
    return functions[func_name](x)

# Initialize the cache and lock
cache = {}
cache_lock = Lock()

# Flask route for the optimization
@app.route('/optimize', methods=['POST'])
def optimize():
    print('Optimization request received')
    # Extract the JSON data from the request
    data = request.json
    
    # Extract parameters from the request data
    dimensions = data.get('dimensions', 100)
    lowerBound = data.get('lowerBound', -10.0)
    upperBound = data.get('upperBound', 10.0)
    gridSizeFactorP = data.get('gridSizeFactorP', 2)
    gridSizeFactorQ = data.get('gridSizeFactorQ', 12)
    evals = data.get('evals', 1.E+5)
    funcName = data.get('funcName', 'Simple')
    isFunc = data.get('isFunc', True)
    isVect = data.get('isVect', True)
    withCache = data.get('withCache', False)
    withLog = data.get('withLog', True)
    withOpt = data.get('withOpt', False)
    
    # Create a unique key for the current optimization request
    request_key = (dimensions, lowerBound, upperBound, gridSizeFactorP, gridSizeFactorQ, evals, funcName, isFunc, isVect, withCache, withLog, withOpt)
    
    # Check if the result is already cached
    with cache_lock:
        if request_key in cache:
            result = cache[request_key]
            # Log the final state
            print('-' * 70 + '\n')
            print(data)
            print('-' * 10 + 'fetched from cache' + '-' * 10 + '\n')
            print(result + '\n\n')
            return jsonify({"minimum_value": result})
    
    # Initialize the optimal x values based on the function name
    if funcName == "Tensor":
        x_opt_r = np.zeros(dimensions)
        x_opt_r[0] = 2
        x_opt_r[1] = 3
    elif funcName == "Simple":
        x_opt_r = np.zeros(dimensions)
    elif funcName == "Alpine":
        x_opt_r = np.ones(dimensions)
    else:
        x_opt_r = np.ones(dimensions)

    # Initialize the TTOpt class instance with the correct parameters
    tto = TTOpt(
        f=f,                    # Function for minimization with data.X as parameter
        d=dimensions,           # Number of function dimensions
        a=lowerBound,           # Grid lower bound (number or list of len d)
        b=upperBound,           # Grid upper bound (number or list of len d)
        p=gridSizeFactorP,      # The grid size factor (there will n=p^q points)
        q=gridSizeFactorQ,      # The grid size factor (there will n=p^q points)
        evals=evals,            # Number of function evaluations
        name=funcName,          # Function name for log (this is optional)
        x_opt_real=x_opt_r,     # Real value of x-minima (x; this is for test)
        y_opt_real=0.,          # Real value of y-minima (y=f(x); this is for test)
        is_func=isFunc,         # Whether the function is a callable
        is_vect=isVect,         # Whether the function is vectorized
        with_cache=withCache,   # Whether to use caching
        with_log=withLog,       # Whether to log the optimization process
        with_opt=withOpt        # Whether to use optimization
    )

    # Launch the minimizer
    tto.optimize(rank)

    # Log the final state
    print('-' * 70 + '\n')
    print(data)
    print('-' * 10 + 'calculated' + '-' * 10 + '\n')
    print(tto.info() + '\n\n')
    
    # Run the minimization and get the result
    result = tto.info()
    
    # Cache the result
    with cache_lock:
        cache[request_key] = result
    
    # Return the result as a JSON response
    return jsonify({"minimum_value": result})

if __name__ == '__main__':
    # Run the Flask app on a specific port (e.g., 5000)
    app.run(host='0.0.0.0', port=5000)
