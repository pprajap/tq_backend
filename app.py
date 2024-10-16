import logging
import sys
import numpy as np
from flask import Flask, request, jsonify, send_file
from ttopt import TTOpt
from threading import Lock

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

class DynamicFileHandler(logging.FileHandler):
    def __init__(self, filename):
        super().__init__(filename)
        self.filename = filename

    def start_logging(self):
        self.stream = self._open()

    def stop_logging(self):
        self.close()

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')

# Create formatters and add them to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Redirect stdout to the log file
stdout_logger = StreamToLogger(logger, logging.INFO)
sys.stdout = stdout_logger

app = Flask(__name__)

np.random.seed(42)

rank = 4

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
    global log_filename
    log_filename = 'optimize_log.txt'
    open(log_filename, 'w').close()

    # Start fresh logging
    dynamic_file_handler = DynamicFileHandler(log_filename)
    dynamic_file_handler.setFormatter(formatter)
    logger.addHandler(dynamic_file_handler)
    dynamic_file_handler.start_logging()

    try:
    
        print('Optimization request received \n')

        data = request.json
        print('-' * 70 + '\n')
        print(data)
        print('-' * 70 + '\n')
        
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
        forceRecal = data.get('forceRecal', False)
        
        # Create a unique key for the current optimization request
        request_key = (dimensions, lowerBound, upperBound, gridSizeFactorP, gridSizeFactorQ, evals, funcName, isFunc, isVect, withCache, withLog, withOpt)
        
        # Check cache for existing result
        with cache_lock:
            if request_key in cache:
                if not forceRecal:
                    result = cache[request_key]
                    print('Request key found in cache \n')
                    print('-' * 70 + '\n')
                    print(data)
                    print('\n' + '-' * 70 + '\n')
                    print(result + '\n')
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
        try:
            tto.optimize(rank)
            print('Optimization completed successfully')
        except Exception as e:
            print(f'Optimization failed: {e}')
            result = None

        print('-' * 30 + 'calculated info' + '-' * 30 + '\n')
        print(tto.info() + '\n\n')
        
        result = tto.info()
        
        # Cache the result
        with cache_lock:
            cache[request_key] = result
        
        # Return the result as a JSON response
        return jsonify({"minimum_value": result})
    finally:
        # Stop logging
        dynamic_file_handler.stop_logging()
        logger.removeHandler(dynamic_file_handler)

# Flask route for downloading the log file
@app.route('/download_solution', methods=['GET'])
def download_solution():
    print('Download solution request received \n')
    return send_file(log_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
