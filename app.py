import streamlit as st
import random
import time
from datetime import datetime, timedelta

# ==============================================================================
# QUESTION DATABASE (300 Questions - 50 per Lecture)
# ==============================================================================
QUESTIONS = [
    # --- LECTURE 01: Review of Essentials (Q1-50) ---
    {"id": 1, "lec": 1, "q": "In a regression model, what is the dependent variable?", "opts": ["A) The variable that explains changes", "B) The variable to be explained", "C) The error term", "D) The intercept"], "ans": "B", "exp": "The dependent variable is the one whose variation is to be explained by independent variables."},
    {"id": 2, "lec": 1, "q": "What does β₁ represent in the linear regression equation y = β₀ + β₁x + ε?", "opts": ["A) The y-intercept", "B) The error term", "C) The slope of the line", "D) The predicted value"], "ans": "C", "exp": "β₁ represents the slope, indicating how much y changes for a unit change in x."},
    {"id": 3, "lec": 1, "q": "Which method is commonly used to estimate regression parameters?", "opts": ["A) Maximum likelihood", "B) Least squares", "C) Random search", "D) Grid search"], "ans": "B", "exp": "Least squares minimizes the sum of squared errors between predicted and actual values."},
    {"id": 4, "lec": 1, "q": "What does the error term (ε) represent in regression?", "opts": ["A) The slope", "B) The intercept", "C) Unexplained/random variation", "D) The predicted value"], "ans": "C", "exp": "The error term captures random variation not explained by the model."},
    {"id": 5, "lec": 1, "q": "In the office rentals dataset example, what was the independent variable?", "opts": ["A) Rental Price", "B) Floor number", "C) Size", "D) Energy Rate"], "ans": "C", "exp": "Size was used as the independent variable to predict rental price."},
    {"id": 6, "lec": 1, "q": "What is 'y-hat' (ŷ) in regression notation?", "opts": ["A) Actual value", "B) Predicted value", "C) Error value", "D) Weight value"], "ans": "B", "exp": "ŷ represents the predicted values of the dependent variable."},
    {"id": 7, "lec": 1, "q": "How many parameters does simple linear regression estimate?", "opts": ["A) One", "B) Two", "C) Three", "D) Four"], "ans": "B", "exp": "Two parameters: slope (β₁) and intercept (β₀)."},
    {"id": 8, "lec": 1, "q": "What is the purpose of the error function in model training?", "opts": ["A) To initialize weights", "B) To judge model performance", "C) To select features", "D) To normalize data"], "ans": "B", "exp": "The error function evaluates how well the model performs on training data."},
    {"id": 9, "lec": 1, "q": "What does the error surface represent?", "opts": ["A) Data distribution", "B) Error values for all weight combinations", "C) Training examples", "D) Model architecture"], "ans": "B", "exp": "The error surface shows error values for every possible combination of weights."},
    {"id": 10, "lec": 1, "q": "What is the goal of gradient descent?", "opts": ["A) Maximize the error", "B) Find the highest point on error surface", "C) Find the lowest point on error surface", "D) Randomize weights"], "ans": "C", "exp": "Gradient descent finds the minimum error point on the error surface."},
    {"id": 11, "lec": 1, "q": "What does the learning rate (α) control in gradient descent?", "opts": ["A) Number of iterations", "B) How quickly the algorithm converges", "C) Number of features", "D) Model complexity"], "ans": "B", "exp": "Learning rate controls the step size and convergence speed."},
    {"id": 12, "lec": 1, "q": "What happens if the learning rate is too large?", "opts": ["A) Convergence is too slow", "B) May overshoot the minimum", "C) No effect on training", "D) Model becomes too simple"], "ans": "B", "exp": "A large learning rate can cause the algorithm to overshoot the minimum."},
    {"id": 13, "lec": 1, "q": "In multivariate regression, what is the dummy feature d[0] typically set to?", "opts": ["A) 0", "B) 1", "C) -1", "D) Random value"], "ans": "B", "exp": "The dummy feature is always set to 1 to represent the intercept term."},
    {"id": 14, "lec": 1, "q": "What is the L2 loss function also known as?", "opts": ["A) Mean Absolute Error", "B) Sum of Squared Errors", "C) Cross-Entropy", "D) Hinge Loss"], "ans": "B", "exp": "L2 loss is the Sum of Squared Errors."},
    {"id": 15, "lec": 1, "q": "Which feature was NOT included in the multivariate office rental model?", "opts": ["A) Size", "B) Floor", "C) Energy Rate", "D) One categorical feature"], "ans": "D", "exp": "One categorical feature (like Energy Rate) was excluded to avoid dummy variable trap."},
    {"id": 16, "lec": 1, "q": "What is the main difference between linear and logistic regression?", "opts": ["A) Number of parameters", "B) Target variable type", "C) Training algorithm", "D) Error function only"], "ans": "B", "exp": "Logistic regression handles binary targets, linear handles continuous."},
    {"id": 17, "lec": 1, "q": "What function does logistic regression use?", "opts": ["A) Linear function", "B) Step function", "C) Sigmoid/Logistic function", "D) ReLU function"], "ans": "C", "exp": "Logistic regression uses the sigmoid function for binary classification."},
    {"id": 18, "lec": 1, "q": "Why is a step function problematic for learning?", "opts": ["A) Too complex", "B) Non-differentiable", "C) Too simple", "D) Requires too much data"], "ans": "B", "exp": "Step functions are non-differentiable, making gradient-based optimization impossible."},
    {"id": 19, "lec": 1, "q": "What is the range of the sigmoid function?", "opts": ["A) [-1, 1]", "B) [0, ∞]", "C) [0, 1]", "D) [-∞, ∞]"], "ans": "C", "exp": "Sigmoid outputs values between 0 and 1."},
    {"id": 20, "lec": 1, "q": "What loss function is used for logistic regression?", "opts": ["A) Sum of Squared Errors", "B) Cross-Entropy Loss", "C) Hinge Loss", "D) Mean Absolute Error"], "ans": "B", "exp": "Cross-Entropy Loss is appropriate for binary classification."},
    {"id": 21, "lec": 1, "q": "What is the big idea behind parameterized prediction models?", "opts": ["A) Use fixed parameters", "B) Initialize randomly and iteratively adjust", "C) Use pre-trained values only", "D) Avoid error functions"], "ans": "B", "exp": "Models start with random parameters and iteratively adjust based on error."},
    {"id": 22, "lec": 1, "q": "In the error surface plot, what does the x-y plane represent?", "opts": ["A) Data space", "B) Weight space", "C) Output space", "D) Error space"], "ans": "B", "exp": "The x-y plane represents the weight space."},
    {"id": 23, "lec": 1, "q": "What is the convergence criterion in gradient descent?", "opts": ["A) Fixed number of iterations only", "B) When error stops decreasing significantly", "C) When weights become zero", "D) When learning rate becomes zero"], "ans": "B", "exp": "Convergence occurs when error reduction becomes negligible."},
    {"id": 24, "lec": 1, "q": "What does the partial derivative of L2 with respect to weights give?", "opts": ["A) The error value", "B) The gradient of error surface", "C) The predicted output", "D) The learning rate"], "ans": "B", "exp": "Partial derivatives give the gradient direction for weight updates."},
    {"id": 25, "lec": 1, "q": "For multiple training instances, how is the gradient calculated?", "opts": ["A) Use one instance only", "B) Sum over all instances", "C) Average of random instances", "D) Ignore instances"], "ans": "B", "exp": "The gradient sums contributions from all training instances."},
    {"id": 26, "lec": 1, "q": "What type of problem is multinomial logistic regression for?", "opts": ["A) Binary classification", "B) Multi-class classification", "C) Regression", "D) Clustering"], "ans": "B", "exp": "Multinomial logistic regression handles multiple classes."},
    {"id": 27, "lec": 1, "q": "What visualization shows the relationship between Size and Rental Price?", "opts": ["A) Bar chart", "B) Scatter plot", "C) Pie chart", "D) Histogram"], "ans": "B", "exp": "Scatter plots show relationships between two continuous variables."},
    {"id": 28, "lec": 1, "q": "What does the contour plot of error surface show?", "opts": ["A) Data distribution", "B) Lines of equal error", "C) Weight values", "D) Learning rate"], "ans": "B", "exp": "Contour plots show lines connecting points of equal error."},
    {"id": 29, "lec": 1, "q": "In gradient descent, what direction do we move weights?", "opts": ["A) Up the slope", "B) Down the slope", "C) Random direction", "D) Perpendicular to slope"], "ans": "B", "exp": "We move down the slope to minimize error."},
    {"id": 30, "lec": 1, "q": "What is the formula for weight update in gradient descent?", "opts": ["A) w = w - α × gradient", "B) w = w + α × gradient", "C) w = w × α", "D) w = α / gradient"], "ans": "B", "exp": "Weights are updated by adding learning rate times the error delta."},
    {"id": 31, "lec": 1, "q": "Why normalize input signals for sigmoid activation?", "opts": ["A) To speed up computation", "B) To avoid saturation at high/low ends", "C) To reduce memory", "D) To increase accuracy"], "ans": "B", "exp": "Sigmoid saturates at extremes, normalization helps avoid this."},
    {"id": 32, "lec": 1, "q": "What does bivariate regression mean?", "opts": ["A) Two dependent variables", "B) Two independent variables", "C) One independent and one dependent variable", "D) Two error terms"], "ans": "C", "exp": "Bivariate means one independent and one dependent variable."},
    {"id": 33, "lec": 1, "q": "What is the purpose of the random error component?", "opts": ["A) To make model complex", "B) To capture unexplained variation", "C) To increase predictions", "D) To reduce training time"], "ans": "B", "exp": "Random error captures variation not explained by the model."},
    {"id": 34, "lec": 1, "q": "Which database was cited for the gasoline price example?", "opts": ["A) World Bank", "B) CANSIM II", "C) IMF", "D) Federal Reserve"], "ans": "B", "exp": "CANSIM II Database was cited for the Canadian price data."},
    {"id": 35, "lec": 1, "q": "What is the dependent variable in the gasoline price example?", "opts": ["A) Crude oil price", "B) Retail price of gasoline", "C) Time", "D) Location"], "ans": "B", "exp": "Retail price of gasoline is explained by crude oil price."},
    {"id": 36, "lec": 1, "q": "What is the independent variable in the gasoline price example?", "opts": ["A) Retail price", "B) Crude oil price", "C) Taxes", "D) Demand"], "ans": "B", "exp": "Crude oil price is the explanatory variable."},
    {"id": 37, "lec": 1, "q": "What does the symbol 'ε' stand for in regression?", "opts": ["A) Slope", "B) Intercept", "C) Error component", "D) Prediction"], "ans": "C", "exp": "ε represents the unexplained or random error component."},
    {"id": 38, "lec": 1, "q": "What is the equation for a simple linear regression line?", "opts": ["A) y = mx + c", "B) y = β₀ + β₁x + ε", "C) y = ax² + bx + c", "D) y = log(x)"], "ans": "B", "exp": "The standard form includes intercept, slope, and error term."},
    {"id": 39, "lec": 1, "q": "What is the 'Big Idea' of parameterized models?", "opts": ["A) Fixed parameters", "B) Iterative adjustment based on error", "C) No error function", "D) Manual tuning"], "ans": "B", "exp": "Parameters are initialized randomly and adjusted iteratively."},
    {"id": 40, "lec": 1, "q": "What is the office rentals dataset used for in Lecture 01?", "opts": ["A) Classification", "B) Regression example", "C) Clustering", "D) Reinforcement Learning"], "ans": "B", "exp": "It is used to demonstrate simple linear regression."},
    {"id": 41, "lec": 1, "q": "What is the value of the dummy feature d[0]?", "opts": ["A) 0", "B) 1", "C) -1", "D) 10"], "ans": "B", "exp": "It is always equal to 1 to handle the intercept."},
    {"id": 42, "lec": 1, "q": "What happens to the error surface as weights change?", "opts": ["A) It stays flat", "B) It forms a 3D surface", "C) It disappears", "D) It becomes linear"], "ans": "B", "exp": "Error values for weight combinations form a surface."},
    {"id": 43, "lec": 1, "q": "What is the 'white dot' in the error surface contour plot?", "opts": ["A) Starting point", "B) Global minimum", "C) Maximum error", "D) Outlier"], "ans": "B", "exp": "It marks the global minimum error point."},
    {"id": 44, "lec": 1, "q": "What is the learning rate symbol in the slides?", "opts": ["A) β", "B) α", "C) ε", "D) w"], "ans": "B", "exp": "α controls the convergence speed."},
    {"id": 45, "lec": 1, "q": "What is the target variable in logistic regression?", "opts": ["A) Continuous", "B) Binary", "C) Categorical (many)", "D) Text"], "ans": "B", "exp": "Logistic regression is for binary targets."},
    {"id": 46, "lec": 1, "q": "What function is used to model binary problems instead of linear?", "opts": ["A) Step", "B) Logistic/Sigmoid", "C) Polynomial", "D) Exponential"], "ans": "B", "exp": "Logistic function avoids step function issues."},
    {"id": 47, "lec": 1, "q": "Why is the Step Function non-differentiable?", "opts": ["A) It is smooth", "B) It has a sharp jump", "C) It is linear", "D) It is complex"], "ans": "B", "exp": "The sharp jump prevents gradient calculation."},
    {"id": 48, "lec": 1, "q": "What is the cost function for Logistic Regression?", "opts": ["A) L2 Loss", "B) Cross-Entropy", "C) Hinge Loss", "D) MAE"], "ans": "B", "exp": "Cross-Entropy is used for classification costs."},
    {"id": 49, "lec": 1, "q": "What does Multinomial Logistic Regression handle?", "opts": ["A) 2 classes", "B) Multiple classes", "C) Regression", "D) Time series"], "ans": "B", "exp": "It extends logistic regression to >2 classes."},
    {"id": 50, "lec": 1, "q": "What is the range of the Hyperbolic Tangent (tanh)?", "opts": ["A) [0, 1]", "B) [-1, 1]", "C) [0, ∞]", "D) [-∞, ∞]"], "ans": "B", "exp": "Tanh ranges from -1 to +1."},

    # --- LECTURE 02: Neural Networks - A (Q51-100) ---
    {"id": 51, "lec": 2, "q": "What is a 'black box' model?", "opts": ["A) Easy to interpret", "B) Makes great predictions but hard to explain", "C) Uses simple rules", "D) Requires no training"], "ans": "B", "exp": "Black box models like neural networks make good predictions but are hard to interpret."},
    {"id": 52, "lec": 2, "q": "Which is an example of a white box model?", "opts": ["A) Neural Networks", "B) Random Forests", "C) Decision Trees", "D) Deep Learning"], "ans": "C", "exp": "Decision Trees are interpretable and considered white box models."},
    {"id": 53, "lec": 2, "q": "What critical ingredient enabled recent deep learning successes?", "opts": ["A) Smaller models", "B) Larger quantities of data", "C) Less parameters", "D) Manual feature engineering"], "ans": "B", "exp": "Large datasets were crucial for deep learning success."},
    {"id": 54, "lec": 2, "q": "How many general approaches to machine learning are described?", "opts": ["A) Two", "B) Three", "C) Four", "D) Five"], "ans": "B", "exp": "Classical ML, Representation Learning, and Deep Learning."},
    {"id": 55, "lec": 2, "q": "What is deep learning a form of?", "opts": ["A) Classical machine learning", "B) Representation learning", "C) Unsupervised learning", "D) Reinforcement learning"], "ans": "B", "exp": "Deep learning is a form of representation learning with multiple transformation steps."},
    {"id": 56, "lec": 2, "q": "What is associated with each input into a neuron?", "opts": ["A) Bias only", "B) Weight", "C) Activation function", "D) Output value"], "ans": "B", "exp": "Each input has an associated weight that gets adjusted during training."},
    {"id": 57, "lec": 2, "q": "What type of number is a weight?", "opts": ["A) Integer", "B) Floating point", "C) Binary", "D) Complex"], "ans": "B", "exp": "Weights are floating point numbers."},
    {"id": 58, "lec": 2, "q": "When was the perceptron developed?", "opts": ["A) 1930s-1940s", "B) 1950s-1960s", "C) 1970s-1980s", "D) 1990s-2000s"], "ans": "B", "exp": "Perceptron was developed in the 1950s and 1960s."},
    {"id": 59, "lec": 2, "q": "What type of output does a perceptron produce?", "opts": ["A) Continuous", "B) Binary (0 or 1)", "C) Multi-class", "D) Probability distribution"], "ans": "B", "exp": "Perceptron produces binary output based on threshold."},
    {"id": 60, "lec": 2, "q": "In a feedforward network, how does information flow?", "opts": ["A) Backwards only", "B) Both directions", "C) Forward only", "D) Randomly"], "ans": "C", "exp": "Information flows forward from input to output in feedforward networks."},
    {"id": 61, "lec": 2, "q": "How many inputs would a neural net need for an 8×8 light panel?", "opts": ["A) 8", "B) 16", "C) 64", "D) 128"], "ans": "C", "exp": "8×8 = 64 inputs, one for each cell."},
    {"id": 62, "lec": 2, "q": "How are neural network weights typically initialized?", "opts": ["A) All zeros", "B) All ones", "C) Random values", "D) Pre-trained values"], "ans": "C", "exp": "Weights are initialized with random values before training."},
    {"id": 63, "lec": 2, "q": "What does MLP stand for?", "opts": ["A) Multi-Layer Perceptron", "B) Maximum Likelihood Perceptron", "C) Multi-Path Learning", "D) Matrix Linear Processing"], "ans": "A", "exp": "MLP = Multi-Layer Perceptron."},
    {"id": 64, "lec": 2, "q": "How many layers does a three-layer network have (by weight layer convention)?", "opts": ["A) 2", "B) 3", "C) 4", "D) 5"], "ans": "B", "exp": "Three layers of adaptive weights (input-hidden, hidden-hidden, hidden-output)."},
    {"id": 65, "lec": 2, "q": "What is the bias in a perceptron equivalent to?", "opts": ["A) Weight", "B) Negative threshold", "C) Input", "D) Output"], "ans": "B", "exp": "Bias b ≡ -threshold."},
    {"id": 66, "lec": 2, "q": "What can a single perceptron learn?", "opts": ["A) Any function", "B) Linearly separable functions only", "C) XOR function", "D) Non-convex boundaries"], "ans": "B", "exp": "Single perceptron can only learn linearly separable functions."},
    {"id": 67, "lec": 2, "q": "Which function CANNOT be implemented by a single layer perceptron?", "opts": ["A) AND", "B) OR", "C) XOR", "D) NOT"], "ans": "C", "exp": "XOR is not linearly separable."},
    {"id": 68, "lec": 2, "q": "Who offered the solution to the XOR problem?", "opts": ["A) LeCun", "B) Minsky & Papert", "C) Hinton", "D) Bengio"], "ans": "B", "exp": "Minsky & Papert (1969) showed multi-layer solution for XOR."},
    {"id": 69, "lec": 2, "q": "What does a 2nd layer in MLP do?", "opts": ["A) Receives input", "B) Combines boundaries from 1st layer", "C) Produces final output only", "D) Normalizes data"], "ans": "B", "exp": "Second layer combines linear boundaries from first layer."},
    {"id": 70, "lec": 2, "q": "What can a 3rd layer generate?", "opts": ["A) Linear boundaries only", "B) Convex boundaries only", "C) Arbitrarily complex boundaries", "D) No boundaries"], "ans": "C", "exp": "Three layers can generate arbitrarily complex decision boundaries."},
    {"id": 71, "lec": 2, "q": "What is the output of a sigmoid neuron?", "opts": ["A) w·x + b", "B) σ(w·x + b)", "C) max(0, w·x + b)", "D) tanh(w·x + b)"], "ans": "B", "exp": "Sigmoid neuron outputs σ(w·x + b)."},
    {"id": 72, "lec": 2, "q": "What values can sigmoid neuron inputs have?", "opts": ["A) Only 0 or 1", "B) Between 0 and 1", "C) Only integers", "D) Only positive"], "ans": "B", "exp": "Sigmoid neurons can handle continuous inputs between 0 and 1."},
    {"id": 73, "lec": 2, "q": "Why is sigmoid function smoothness important?", "opts": ["A) Faster computation", "B) Small weight changes produce small output changes", "C) Reduces memory", "D) Increases accuracy"], "ans": "B", "exp": "Smoothness ensures gradual output changes for gradual weight changes."},
    {"id": 74, "lec": 2, "q": "Which activation function has a steady state at 0?", "opts": ["A) Sigmoid", "B) Hyperbolic tangent (tanh)", "C) ReLU", "D) Step function"], "ans": "B", "exp": "Tanh ranges from -1 to +1 with steady state at 0."},
    {"id": 75, "lec": 2, "q": "What is ReLU short for?", "opts": ["A) Recurrent Linear Unit", "B) Rectified Linear Unit", "C) Random Linear Unit", "D) Regularized Linear Unit"], "ans": "B", "exp": "ReLU = Rectified Linear Unit."},
    {"id": 76, "lec": 2, "q": "What advantage does ReLU provide?", "opts": ["A) Dense activations", "B) Sparseness property", "C) Always positive output", "D) Complex gradient"], "ans": "B", "exp": "ReLU produces sparse activations (many zeros)."},
    {"id": 77, "lec": 2, "q": "What is the gradient of ReLU?", "opts": ["A) Always 0", "B) Always 1", "C) Either 0 or 1", "D) Variable"], "ans": "C", "exp": "ReLU gradient is 0 for negative input, 1 for positive."},
    {"id": 78, "lec": 2, "q": "Who developed the Backpropagation algorithm (published 1986)?", "opts": ["A) LeCun, Bengio, Hinton", "B) Rumelhart, Hinton, Williams", "C) Minsky, Papert", "D) Goodfellow, Pouget-Abadie"], "ans": "B", "exp": "Rumelhart, Hinton, and Williams published BP in 1986."},
    {"id": 79, "lec": 2, "q": "What are the two phases of backpropagation?", "opts": ["A) Training and Testing", "B) Forward pass and Backward pass", "C) Initialization and Update", "D) Encoding and Decoding"], "ans": "B", "exp": "Forward pass computes outputs, backward pass propagates errors."},
    {"id": 80, "lec": 2, "q": "What does the forward pass compute?", "opts": ["A) Error signal", "B) Functional signal", "C) Weight updates", "D) Gradient"], "ans": "B", "exp": "Forward pass computes the functional signal (outputs)."},
    {"id": 81, "lec": 2, "q": "What does the backward pass compute?", "opts": ["A) Output values", "B) Error signal", "C) Input values", "D) Activation values"], "ans": "B", "exp": "Backward pass computes and propagates the error signal."},
    {"id": 82, "lec": 2, "q": "What is one epoch in neural network training?", "opts": ["A) One weight update", "B) One complete presentation of training set", "C) One layer update", "D) One iteration"], "ans": "B", "exp": "One epoch = one complete pass through the entire training set."},
    {"id": 83, "lec": 2, "q": "What is the Generalized Delta Rule also known as?", "opts": ["A) Forward Propagation", "B) Back Propagation algorithm", "C) Gradient Descent", "D) Weight Initialization"], "ans": "B", "exp": "Generalized Delta Rule = Back Propagation algorithm."},
    {"id": 84, "lec": 2, "q": "What is the output of a perceptron?", "opts": ["A) Continuous value", "B) 0 or 1", "C) Probability", "D) Vector"], "ans": "B", "exp": "Perceptron outputs binary 0 or 1."},
    {"id": 85, "lec": 2, "q": "What is the equation for perceptron output?", "opts": ["A) w·x", "B) sgn(w·x + b)", "C) σ(w·x)", "D) max(0, x)"], "ans": "B", "exp": "It uses the sign function on the weighted sum plus bias."},
    {"id": 86, "lec": 2, "q": "What is the 'Credit Assignment Problem' solved by?", "opts": ["A) Gradient Descent", "B) Backpropagation", "C) Pooling", "D) Dropout"], "ans": "B", "exp": "Backprop solves credit assignment in MLP."},
    {"id": 87, "lec": 2, "q": "What is the 'Functional Signal'?", "opts": ["A) Error", "B) Input/Output propagation", "C) Weight update", "D) Loss"], "ans": "B", "exp": "It is the forward propagation of input patterns."},
    {"id": 88, "lec": 2, "q": "What is the 'Error Signal'?", "opts": ["A) Forward propagation", "B) Backward propagation", "C) Weight init", "D) Activation"], "ans": "B", "exp": "It is the backward propagation of errors."},
    {"id": 89, "lec": 2, "q": "What is the learning rate symbol in Backprop?", "opts": ["A) α", "B) η", "C) β", "D) λ"], "ans": "B", "exp": "η (eta) is commonly used for learning rate in BP."},
    {"id": 90, "lec": 2, "q": "What is the first step in Backprop?", "opts": ["A) Update weights", "B) Initialize weights", "C) Compute error", "D) Normalize"], "ans": "B", "exp": "Weights are initialized at random."},
    {"id": 91, "lec": 2, "q": "What is the last step in Backprop loop?", "opts": ["A) Forward pass", "B) Update weights", "C) Initialize", "D) Stop"], "ans": "B", "exp": "Weights are updated via gradient descent."},
    {"id": 92, "lec": 2, "q": "What is 'Early Stopping'?", "opts": ["A) Stopping when training error is 0", "B) Stopping when validation loss deteriorates", "C) Stopping after 1 epoch", "D) Stopping randomly"], "ans": "B", "exp": "It prevents overfitting by monitoring validation loss."},
    {"id": 93, "lec": 2, "q": "What data is used for Early Stopping?", "opts": ["A) Training set", "B) Validation set", "C) Test set", "D) None"], "ans": "B", "exp": "Validation set loss is monitored."},
    {"id": 94, "lec": 2, "q": "What is the Test Set used for?", "opts": ["A) Training", "B) Tuning hyperparameters", "C) Final evaluation", "D) Early stopping"], "ans": "C", "exp": "Test set is for final unbiased evaluation."},
    {"id": 95, "lec": 2, "q": "Why hide Test Set labels in competitions?", "opts": ["A) To make it hard", "B) To prevent overfitting to test data", "C) To save space", "D) No reason"], "ans": "B", "exp": "Prevents participants from tuning specifically to test data."},
    {"id": 96, "lec": 2, "q": "What are Hyperparameters?", "opts": ["A) Weights", "B) Biases", "C) Settings like learning rate/layers", "D) Inputs"], "ans": "C", "exp": "They are configuration settings tuned before training."},
    {"id": 97, "lec": 2, "q": "What is a 'White Box' model example?", "opts": ["A) Neural Net", "B) Decision Tree", "C) CNN", "D) LSTM"], "ans": "B", "exp": "Decision Trees are interpretable."},
    {"id": 98, "lec": 2, "q": "What is a 'Black Box' model example?", "opts": ["A) Linear Regression", "B) Neural Network", "C) Decision Tree", "D) Rules"], "ans": "B", "exp": "Neural Networks are hard to interpret."},
    {"id": 99, "lec": 2, "q": "What is the main benefit of Deep Learning?", "opts": ["A) Simple models", "B) Exploiting massive datasets", "C) Less data", "D) Manual features"], "ans": "B", "exp": "It exploits information in massive datasets."},
    {"id": 100, "lec": 2, "q": "What is Representation Learning?", "opts": ["A) Manual features", "B) Transforming features automatically", "C) Clustering", "D) Regression"], "ans": "B", "exp": "It transforms features into intermediate representations."},

    # --- LECTURE 03: Neural Networks - B (Q101-150) ---
    {"id": 101, "lec": 3, "q": "What type of method are ANNs typically?", "opts": ["A) Unsupervised white box", "B) Supervised black box", "C) Unsupervised black box", "D) Supervised white box"], "ans": "B", "exp": "ANNs are supervised black box methods."},
    {"id": 102, "lec": 3, "q": "Which is NOT a typical ANN application?", "opts": ["A) Time series analysis", "B) Signal processing", "C) Database management", "D) Classification"], "ans": "C", "exp": "Database management is not a typical ANN application."},
    {"id": 103, "lec": 3, "q": "What are ANNs composed of?", "opts": ["A) Decision trees", "B) Layers of artificial neurons", "C) Support vectors", "D) Clusters"], "ans": "B", "exp": "ANNs are composed of layers of artificial neurons/perceptrons."},
    {"id": 104, "lec": 3, "q": "What differentiates ANNs from perceptrons in SVM context?", "opts": ["A) Number of layers", "B) Presence of activation function", "C) Training data", "D) Output type"], "ans": "B", "exp": "Activation function is the key difference."},
    {"id": 105, "lec": 3, "q": "What does an activation function do?", "opts": ["A) Initializes weights", "B) Transforms net input to output signal", "C) Calculates error", "D) Selects features"], "ans": "B", "exp": "Activation function transforms neuron's net input into output signal."},
    {"id": 106, "lec": 3, "q": "What is network topology?", "opts": ["A) Training algorithm", "B) Architecture describing neurons and layers", "C) Error function", "D) Data preprocessing"], "ans": "B", "exp": "Topology describes number of neurons, layers, and interconnections."},
    {"id": 107, "lec": 3, "q": "What type of graph is an ANN?", "opts": ["A) Undirected graph", "B) Directed acyclic graph", "C) Cyclic graph only", "D) Random graph"], "ans": "B", "exp": "Feedforward ANNs are directed acyclic graphs."},
    {"id": 108, "lec": 3, "q": "What is NOT a main layer type in ANN?", "opts": ["A) Input layer", "B) Output layer", "C) Processing layer", "D) Hidden layer"], "ans": "C", "exp": "The three main layers are input, hidden, and output."},
    {"id": 109, "lec": 3, "q": "What defines a single layer network?", "opts": ["A) Only input layer", "B) Input and output layers", "C) Only hidden layer", "D) Input, hidden, and output"], "ans": "B", "exp": "Single layer network has only input and output (no hidden)."},
    {"id": 110, "lec": 3, "q": "What defines a 'deep learner'?", "opts": ["A) One hidden layer", "B) More than one hidden layer", "C) No hidden layers", "D) Only output layer"], "ans": "B", "exp": "Deep learners have more than one hidden layer."},
    {"id": 111, "lec": 3, "q": "What can a two-layer feedforward network with step activation implement?", "opts": ["A) Any continuous function", "B) Any Boolean function", "C) Only linear functions", "D) Only XOR"], "ans": "B", "exp": "Two-layer network with step activation can implement any Boolean function."},
    {"id": 112, "lec": 3, "q": "What is the universality property of MLP?", "opts": ["A) Works on any hardware", "B) Can approximate any continuous decision boundary", "C) Trains very fast", "D) Requires no data"], "ans": "B", "exp": "2-layer MLP with sigmoid can approximate any continuous decision boundary."},
    {"id": 113, "lec": 3, "q": "What is the standard form of ANN?", "opts": ["A) Recurrent network", "B) Feedforward network", "C) Random network", "D) Fully connected only"], "ans": "B", "exp": "Feedforward network is the standard form."},
    {"id": 114, "lec": 3, "q": "What do recurrent networks allow?", "opts": ["A) Forward signals only", "B) Signals in both directions with loops", "C) No hidden layers", "D) Binary outputs only"], "ans": "B", "exp": "Recurrent networks allow feedback loops for sequential data."},
    {"id": 115, "lec": 3, "q": "What is best practice for network size?", "opts": ["A) Use maximum nodes possible", "B) Use fewest nodes with adequate performance", "C) Always use 3 hidden layers", "D) Match input size exactly"], "ans": "B", "exp": "Use minimum nodes needed for adequate performance."},
    {"id": 116, "lec": 3, "q": "How many hidden layers are suggested as sufficient for most problems?", "opts": ["A) Zero", "B) One", "C) Three", "D) Ten"], "ans": "B", "exp": "Single hidden layer with sufficient neurons works for most problems."},
    {"id": 117, "lec": 3, "q": "What were two issues with perceptron training?", "opts": ["A) Too fast, too accurate", "B) No convergence if not linearly separable, no quality notion", "C) Too many parameters", "D) Cannot handle binary data"], "ans": "B", "exp": "Perceptron doesn't converge for non-linearly separable data."},
    {"id": 118, "lec": 3, "q": "What rule converges towards best-fit approximation?", "opts": ["A) Perceptron Rule", "B) Delta Rule", "C) XOR Rule", "D) Step Rule"], "ans": "B", "exp": "Delta Rule finds best-fit approximation for non-separable data."},
    {"id": 119, "lec": 3, "q": "What is the basis of the Delta Rule?", "opts": ["A) Random search", "B) Gradient Descent", "C) Grid search", "D) Genetic algorithms"], "ans": "B", "exp": "Delta Rule is based on Gradient Descent."},
    {"id": 120, "lec": 3, "q": "What is removed from perceptron for Delta Rule?", "opts": ["A) Weights", "B) Threshold", "C) Inputs", "D) Bias"], "ans": "B", "exp": "Threshold is removed for unthresholded perceptron."},
    {"id": 121, "lec": 3, "q": "What is the common error function for ANN training?", "opts": ["A) Mean Absolute Error", "B) Half sum of squared errors", "C) Cross-Entropy", "D) Hinge Loss"], "ans": "B", "exp": "E(w) = ½Σ(y_d - o_d)² is commonly used."},
    {"id": 122, "lec": 3, "q": "Why is the ½ factor included in the error function?", "opts": ["A) To reduce error", "B) For convenient mathematical property (derivative)", "C) To normalize", "D) No reason"], "ans": "B", "exp": "The ½ simplifies the derivative calculation."},
    {"id": 123, "lec": 3, "q": "What does ∇E(w) represent?", "opts": ["A) Error value", "B) Gradient of error function", "C) Weight vector", "D) Learning rate"], "ans": "B", "exp": "∇E(w) is the gradient (vector of partial derivatives)."},
    {"id": 124, "lec": 3, "q": "What is the gradient descent update rule?", "opts": ["A) w ← w + η∇E(w)", "B) w ← w - η∇E(w)", "C) w ← w × η", "D) w ← η / ∇E(w)"], "ans": "B", "exp": "Weights move opposite to gradient direction (minus sign)."},
    {"id": 125, "lec": 3, "q": "What problem occurs with too large learning rate?", "opts": ["A) Too slow convergence", "B) Overstepping the minimum", "C) No convergence guarantee", "D) Local minima only"], "ans": "B", "exp": "Large learning rate can overshoot the minimum."},
    {"id": 126, "lec": 3, "q": "What is incremental gradient descent also called?", "opts": ["A) Batch gradient descent", "B) Stochastic gradient descent", "C) Full gradient descent", "D) Parallel gradient descent"], "ans": "B", "exp": "Incremental = Stochastic Gradient Descent (SGD)."},
    {"id": 127, "lec": 3, "q": "What's the main difference between batch and SGD?", "opts": ["A) Number of layers", "B) When weights are updated", "C) Activation function", "D) Error function"], "ans": "B", "exp": "Batch updates after all examples, SGD after each example."},
    {"id": 128, "lec": 3, "q": "What advantage does SGD have with local minima?", "opts": ["A) Always finds global minimum", "B) Can sometimes avoid local minima", "C) No advantage", "D) Creates more local minima"], "ans": "B", "exp": "SGD's noisy updates can help escape local minima."},
    {"id": 129, "lec": 3, "q": "What does backpropagation allow?", "opts": ["A) Linear decision surfaces only", "B) Rich variety of non-linear decision surfaces", "C) No hidden layers", "D) Binary outputs only"], "ans": "B", "exp": "Backprop enables training networks with non-linear decision boundaries."},
    {"id": 130, "lec": 3, "q": "What property makes sigmoid favorable for backprop?", "opts": ["A) Linear and non-differentiable", "B) Non-linear and differentiable", "C) Binary and discrete", "D) Random and variable"], "ans": "B", "exp": "Sigmoid is both non-linear and differentiable."},
    {"id": 131, "lec": 3, "q": "What is the derivative of sigmoid σ(x)?", "opts": ["A) σ(x)", "B) σ(x)(1 - σ(x))", "C) 1 - σ(x)", "D) e^(-x)"], "ans": "B", "exp": "dσ/dx = σ(x)(1 - σ(x))."},
    {"id": 132, "lec": 3, "q": "What does the error term δ represent in backprop?", "opts": ["A) Learning rate", "B) Error contribution of a unit", "C) Weight value", "D) Input value"], "ans": "B", "exp": "δ captures error contribution similar to (y-o) in Delta Rule."},
    {"id": 133, "lec": 3, "q": "How is validation data used in ANN training?", "opts": ["A) To update weights", "B) To compute error without training", "C) To initialize weights", "D) To select architecture only"], "ans": "B", "exp": "Validation data computes error for monitoring, not weight updates."},
    {"id": 134, "lec": 3, "q": "What is Overfitting?", "opts": ["A) Model too simple", "B) Model too complex for data", "C) Model too fast", "D) Model too slow"], "ans": "B", "exp": "Overfitting occurs when model learns noise in training data."},
    {"id": 135, "lec": 3, "q": "How to prevent Overfitting?", "opts": ["A) More training", "B) Validation data/Early Stopping", "C) Less data", "D) Larger model"], "ans": "B", "exp": "Validation data helps detect overfitting."},
    {"id": 136, "lec": 3, "q": "What is the Delta Rule also known as?", "opts": ["A) Widrow-Hoff rule", "B) Hebbian rule", "C) Perceptron rule", "D) Hopfield rule"], "ans": "A", "exp": "It is sometimes called the Adaline or Widrow-Hoff rule."},
    {"id": 137, "lec": 3, "q": "What is the hypothesis space of Backprop?", "opts": ["A) Discrete", "B) Continuous", "C) Binary", "D) Fixed"], "ans": "B", "exp": "Weights form a continuous n-dimensional space."},
    {"id": 138, "lec": 3, "q": "What does Backprop search?", "opts": ["A) Data space", "B) Hypothesis space", "C) Input space", "D) Output space"], "ans": "B", "exp": "It searches for the best weight hypothesis."},
    {"id": 139, "lec": 3, "q": "What is the output range of Sigmoid?", "opts": ["A) [-1, 1]", "B) [0, 1]", "C) [0, ∞]", "D) [-∞, ∞]"], "ans": "B", "exp": "Sigmoid outputs between 0 and 1."},
    {"id": 140, "lec": 3, "q": "What is the output range of Tanh?", "opts": ["A) [-1, 1]", "B) [0, 1]", "C) [0, ∞]", "D) [-∞, ∞]"], "ans": "A", "exp": "Tanh outputs between -1 and 1."},
    {"id": 141, "lec": 3, "q": "What is the output range of Linear?", "opts": ["A) [-1, 1]", "B) [0, 1]", "C) [0, ∞]", "D) [-∞, ∞]"], "ans": "D", "exp": "Linear function has unlimited range."},
    {"id": 142, "lec": 3, "q": "What is a 'Hidden Unit'?", "opts": ["A) Input node", "B) Output node", "C) Internal processing node", "D) Bias node"], "ans": "C", "exp": "Hidden units are internal nodes not directly connected to input/output."},
    {"id": 143, "lec": 3, "q": "What is the 'Credit Assignment Problem'?", "opts": ["A) Who gets paid", "B) Which weight caused the error", "C) Data labeling", "D) Model selection"], "ans": "B", "exp": "It determines how much each weight contributed to the error."},
    {"id": 144, "lec": 3, "q": "What is the 'Universality Property'?", "opts": ["A) Works on all data", "B) Approximates any continuous function", "C) Fast training", "D) No error"], "ans": "B", "exp": "MLPs can approximate any continuous function."},
    {"id": 145, "lec": 3, "q": "How many layers for Universality?", "opts": ["A) 1", "B) 2", "C) 3", "D) 4"], "ans": "B", "exp": "2-layer MLP with sufficient neurons."},
    {"id": 146, "lec": 3, "q": "What is a Recurrent Network good for?", "opts": ["A) Images", "B) Time series/Sequences", "C) Tabular data", "D) Clustering"], "ans": "B", "exp": "Loops allow memory of sequences."},
    {"id": 147, "lec": 3, "q": "What is the 'Weight Space'?", "opts": ["A) Data storage", "B) X-Y plane of error surface", "C) Network layers", "D) Input features"], "ans": "B", "exp": "It represents all possible weight combinations."},
    {"id": 148, "lec": 3, "q": "What is the 'Error Surface'?", "opts": ["A) Data plot", "B) 3D plot of error vs weights", "C) Network graph", "D) Loss function"], "ans": "B", "exp": "It visualizes error for weight combinations."},
    {"id": 149, "lec": 3, "q": "What is the goal of Training?", "opts": ["A) Maximize Error", "B) Minimize Error", "C) Randomize Weights", "D) Fix Weights"], "ans": "B", "exp": "Training minimizes the error function."},
    {"id": 150, "lec": 3, "q": "What is 'Cross Validation'?", "opts": ["A) Using test set for training", "B) Multiple validation splits", "C) No validation", "D) Manual tuning"], "ans": "B", "exp": "It helps avoid overfitting by using multiple splits."},

    # --- LECTURE 04: CNNs (Q151-200) ---
    {"id": 151, "lec": 4, "q": "What are CNNs particularly successful for?", "opts": ["A) Text classification", "B) Image analysis", "C) Time series only", "D) Tabular data"], "ans": "B", "exp": "CNNs have proven extremely successful for image analysis."},
    {"id": 152, "lec": 4, "q": "How many weights for 256×256 RGB image fully connected to 128 neurons?", "opts": ["A) 256,000", "B) 1 million", "C) 25 million", "D) 100 million"], "ans": "C", "exp": "256×256×3×128 ≈ 25 million weights."},
    {"id": 153, "lec": 4, "q": "What is Problem 1 with fully connected layers for images?", "opts": ["A) Too few parameters", "B) Computational explosion", "C) Too simple", "D) No activation functions"], "ans": "B", "exp": "Fully connected layers have too many parameters (computational explosion)."},
    {"id": 154, "lec": 4, "q": "What property do interesting things in images usually have?", "opts": ["A) Position dependent", "B) Translation invariant", "C) Color dependent", "D) Size dependent only"], "ans": "B", "exp": "Objects are translation invariant (can appear anywhere)."},
    {"id": 155, "lec": 4, "q": "What do early CNN layers focus on?", "opts": ["A) Global features", "B) Local features", "C) Output classification", "D) Final predictions"], "ans": "B", "exp": "Early layers focus on local features, global features come later."},
    {"id": 156, "lec": 4, "q": "What can edges be thought of as in CNNs?", "opts": ["A) Noise", "B) Useful spatially organized features", "C) Errors", "D) Outputs"], "ans": "B", "exp": "Edges are useful spatially organized features."},
    {"id": 157, "lec": 4, "q": "How is a filter implemented in CNN?", "opts": ["A) Full image multiplication", "B) Small spatial zone × weights + activation", "C) Random sampling", "D) Average pooling only"], "ans": "B", "exp": "Filter multiplies small spatial zone by weights, feeds to activation."},
    {"id": 158, "lec": 4, "q": "Why can filtering be implemented using convolution?", "opts": ["A) Same weights repeated around image", "B) Different weights for each position", "C) Random weights", "D) No weights needed"], "ans": "A", "exp": "Same weights repeated = convolution operation."},
    {"id": 159, "lec": 4, "q": "What algorithm is used to learn CNN filters?", "opts": ["A) K-means", "B) SGD and backpropagation", "C) Decision trees", "D) Random forest"], "ans": "B", "exp": "CNNs use SGD and backpropagation for learning."},
    {"id": 160, "lec": 4, "q": "What is aggregation in CNNs also called?", "opts": ["A) Convolution", "B) Pooling", "C) Activation", "D) Normalization"], "ans": "B", "exp": "Aggregation across spatial regions = pooling."},
    {"id": 161, "lec": 4, "q": "What does pooling provide?", "opts": ["A) More parameters", "B) Invariance to small position differences", "C) Less accuracy", "D) Slower training"], "ans": "B", "exp": "Pooling gives invariance to exact feature location."},
    {"id": 162, "lec": 4, "q": "With max pooling, when is a feature activated?", "opts": ["A) Only if detected everywhere", "B) If detected anywhere in pooling zone", "C) Never", "D) Only at edges"], "ans": "B", "exp": "Max pooling activates if feature detected anywhere in zone."},
    {"id": 163, "lec": 4, "q": "What is the typical CNN architecture flow?", "opts": ["A) MLP → Conv → Pool → Output", "B) Conv → Pool → Conv → Pool → MLP", "C) Pool → Conv → MLP → Conv", "D) Output → Conv → Pool → Input"], "ans": "B", "exp": "Conv and Pool layers repeat, ending with MLP for classification."},
    {"id": 164, "lec": 4, "q": "Which are canonical CNN models?", "opts": ["A) SVM and KNN", "B) LeNet and AlexNet", "C) Random Forest and XGBoost", "D) LSTM and GRU"], "ans": "B", "exp": "LeNet and AlexNet are canonical CNN architectures."},
    {"id": 165, "lec": 4, "q": "What technique increases CNN performance significantly?", "opts": ["A) Reducing data", "B) Data augmentation (e.g., cropping trick)", "C) Removing layers", "D) Using CPU only"], "ans": "B", "exp": "Data augmentation through transformations increases performance."},
    {"id": 166, "lec": 4, "q": "What computing hardware is typically essential for CNNs?", "opts": ["A) CPU only", "B) GPU", "C) TPU only", "D) FPGA only"], "ans": "B", "exp": "GPU computing is typically essential for CNN acceleration."},
    {"id": 167, "lec": 4, "q": "What was the ImageNet 2012 classification task?", "opts": ["A) 100 categories", "B) 500 categories", "C) 1000 categories", "D) 10000 categories"], "ans": "C", "exp": "ImageNet ILSVRC had 1000 object categories."},
    {"id": 168, "lec": 4, "q": "How many training images in ImageNet?", "opts": ["A) 100,000", "B) 500,000", "C) 1.2 million", "D) 10 million"], "ans": "C", "exp": "ImageNet has 1.2 million training images."},
    {"id": 169, "lec": 4, "q": "What is 'Top-5 error'?", "opts": ["A) % of correct predictions", "B) % where target not in top 5 predictions", "C) Number of wrong classes", "D) Training error rate"], "ans": "B", "exp": "Top-5 error = % where true label not among top 5 predictions."},
    {"id": 170, "lec": 4, "q": "What plateau did non-CNN methods hit on ImageNet?", "opts": ["A) 10% Top-5 error", "B) 25% Top-5 error", "C) 50% Top-5 error", "D) 5% Top-5 error"], "ans": "B", "exp": "Non-CNN methods plateaued at ~25% Top-5 error."},
    {"id": 171, "lec": 4, "q": "What is human performance on ImageNet (Top-5 error)?", "opts": ["A) 1.0%", "B) 5.1%", "C) 10.0%", "D) 25.0%"], "ans": "B", "exp": "Human agreement measured at 5.1% Top-5 error."},
    {"id": 172, "lec": 4, "q": "What filter size leads to superior results in deep networks?", "opts": ["A) 11×11", "B) 7×7", "C) 5×5", "D) 3×3"], "ans": "D", "exp": "Smaller 3×3 filters found to lead to superior results."},
    {"id": 173, "lec": 4, "q": "What is the output size formula for convolution?", "opts": ["A) (n - f + 1)", "B) (n + 2p - f + 1)", "C) (n + p - f)", "D) (n × f)"], "ans": "B", "exp": "Output = (n + 2p - f + 1) where p = padding."},
    {"id": 174, "lec": 4, "q": "What are Sobel filters used for?", "opts": ["A) Color detection", "B) Edge detection", "C) Object classification", "D) Pooling"], "ans": "B", "exp": "Sobel filters are well-known for edge detection."},
    {"id": 175, "lec": 4, "q": "What do early CNN layers typically learn?", "opts": ["A) Complete objects", "B) Edge-like and texture-like filters", "C) Class labels", "D) Output predictions"], "ans": "B", "exp": "Early layers learn edge-like and texture-like filters."},
    {"id": 176, "lec": 4, "q": "What happens to receptive fields as you move up CNN layers?", "opts": ["A) Stay the same", "B) Become smaller", "C) Become larger", "D) Disappear"], "ans": "C", "exp": "Receptive fields become larger in higher layers."},
    {"id": 177, "lec": 4, "q": "What do higher-level CNN layers detect?", "opts": ["A) Simple edges only", "B) Larger features, textures, object pieces", "C) Raw pixels", "D) Noise"], "ans": "B", "exp": "Higher layers detect larger features and object parts."},
    {"id": 178, "lec": 4, "q": "In max pooling 2×2, how many values become one?", "opts": ["A) 2", "B) 4", "C) 8", "D) 16"], "ans": "B", "exp": "2×2 max pooling takes 4 values and outputs 1 (the maximum)."},
    {"id": 179, "lec": 4, "q": "What happens during decimation?", "opts": ["A) Resolution increases", "B) Resolution decreases", "C) No change", "D) Colors change"], "ans": "B", "exp": "Decimation reduces resolution (subsampling)."},
    {"id": 180, "lec": 4, "q": "In backprop through max pooling, which units get the gradient?", "opts": ["A) All units equally", "B) The 'winning units' (maximum)", "C) No units", "D) Random units"], "ans": "B", "exp": "Only the units that produced the maximum get the gradient."},
    {"id": 181, "lec": 4, "q": "What is average pooling mathematically?", "opts": ["A) Special convolution with fixed kernel", "B) Max operation", "C) Random sampling", "D) No operation"], "ans": "A", "exp": "Average pooling is convolution with fixed averaging kernel."},
    {"id": 182, "lec": 4, "q": "How much can GPUs accelerate convolutions vs CPU?", "opts": ["A) 2×", "B) 5×", "C) 10× or more", "D) No acceleration"], "ans": "C", "exp": "GPUs can accelerate convolutions by an order of magnitude or more."},
    {"id": 183, "lec": 4, "q": "What architecture uses residual layers?", "opts": ["A) LeNet", "B) AlexNet", "C) ResNet", "D) VGG"], "ans": "C", "exp": "ResNet uses residual (skip) connections."},
    {"id": 184, "lec": 4, "q": "What does Inception architecture use?", "opts": ["A) Single filter size", "B) Multi-scale feature extraction", "C) No pooling", "D) Only fully connected layers"], "ans": "B", "exp": "Inception uses multiple filter sizes for multi-scale features."},
    {"id": 185, "lec": 4, "q": "What is 'Decimation'?", "opts": ["A) Increasing resolution", "B) Subsampling/Lowering resolution", "C) Adding layers", "D) Removing weights"], "ans": "B", "exp": "Decimation yields a lower-resolution layer."},
    {"id": 186, "lec": 4, "q": "What is the 'Cropping Trick'?", "opts": ["A) Removing data", "B) Data augmentation", "C) Model pruning", "D) Weight clipping"], "ans": "B", "exp": "It is a synthetic transformation for augmentation."},
    {"id": 187, "lec": 4, "q": "What is the Input size in convolution formula?", "opts": ["A) f", "B) n", "C) p", "D) k"], "ans": "B", "exp": "n represents the input dimension."},
    {"id": 188, "lec": 4, "q": "What is the Filter size in convolution formula?", "opts": ["A) n", "B) f", "C) p", "D) s"], "ans": "B", "exp": "f represents the filter dimension."},
    {"id": 189, "lec": 4, "q": "What is the Padding in convolution formula?", "opts": ["A) n", "B) f", "C) p", "D) k"], "ans": "C", "exp": "p represents the padding added."},
    {"id": 190, "lec": 4, "q": "What is the Stride in convolution?", "opts": ["A) Step size of filter", "B) Filter size", "C) Padding size", "D) Output size"], "ans": "A", "exp": "Stride is how much the filter moves."},
    {"id": 191, "lec": 4, "q": "What is Commutative in Convolution?", "opts": ["A) I * K = K * I", "B) I + K = K + I", "C) I - K = K - I", "D) I / K = K / I"], "ans": "A", "exp": "Convolution operation is commutative."},
    {"id": 192, "lec": 4, "q": "What do CNN implementations often use instead of Convolution?", "opts": ["A) Correlation", "B) Addition", "C) Subtraction", "D) Division"], "ans": "A", "exp": "Cross-correlation is often used."},
    {"id": 193, "lec": 4, "q": "What is the formula for Cross-Correlation?", "opts": ["A) Sum K(m,n)I(i-m,j-n)", "B) Sum K(m,n)I(i+m,j+n)", "C) Sum K(m,n)I(i,j)", "D) Sum K(m,n)I(m,n)"], "ans": "B", "exp": "Cross-correlation uses + signs in indices."},
    {"id": 194, "lec": 4, "q": "What is Gx in Sobel filtering?", "opts": ["A) Vertical edges", "B) Horizontal edges", "C) Diagonal edges", "D) Color"], "ans": "B", "exp": "Wx detects horizontal gradients."},
    {"id": 195, "lec": 4, "q": "What is Gy in Sobel filtering?", "opts": ["A) Vertical edges", "B) Horizontal edges", "C) Diagonal edges", "D) Color"], "ans": "A", "exp": "Wy detects vertical gradients."},
    {"id": 196, "lec": 4, "q": "What is the final layer of a typical CNN?", "opts": ["A) Conv", "B) Pool", "C) MLP", "D) Input"], "ans": "C", "exp": "MLP is used for final prediction."},
    {"id": 197, "lec": 4, "q": "What is the validation set size in ImageNet?", "opts": ["A) 10,000", "B) 50,000", "C) 100,000", "D) 1 million"], "ans": "B", "exp": "50,000 images used for validation."},
    {"id": 198, "lec": 4, "q": "What is the test set size in ImageNet?", "opts": ["A) 10,000", "B) 50,000", "C) 100,000", "D) 1 million"], "ans": "C", "exp": "100,000 images used for testing."},
    {"id": 199, "lec": 4, "q": "How many images per class in ImageNet training?", "opts": ["A) 100-500", "B) 732-1300", "C) 2000-5000", "D) 10,000+"], "ans": "B", "exp": "732-1300 training images per class."},
    {"id": 200, "lec": 4, "q": "What is the main benefit of GPU for CNNs?", "opts": ["A) Less memory", "B) Faster convolution", "C) Better accuracy", "D) Easier coding"], "ans": "B", "exp": "GPUs accelerate convolution operations significantly."},

    # --- LECTURE 05: Representation & Transfer Learning (Q201-250) ---
    {"id": 201, "lec": 5, "q": "What is the basic question about media representation?", "opts": ["A) How to store media", "B) How to represent media for neural network processing", "C) How to compress media", "D) How to display media"], "ans": "B", "exp": "Key question is how to represent media for NN processing."},
    {"id": 202, "lec": 5, "q": "What do ASCII and UTF8 capture?", "opts": ["A) Semantic meaning", "B) Literal text", "C) Word relationships", "D) Context"], "ans": "B", "exp": "ASCII/UTF8 capture literal text, not information-centric representation."},
    {"id": 203, "lec": 5, "q": "What is a problem with Bag of Words?", "opts": ["A) Too short vectors", "B) Order of words lost", "C) Too semantic", "D) Too dense"], "ans": "B", "exp": "Bag of Words loses word order information."},
    {"id": 204, "lec": 5, "q": "What is a problem with One-Hot Encoding?", "opts": ["A) Too dense", "B) Sparsity and no semantic meaning", "C) Too short", "D) Captures order"], "ans": "B", "exp": "One-hot encoding is sparse and lacks semantic meaning."},
    {"id": 205, "lec": 5, "q": "What is the solution to capture word similarity?", "opts": ["A) One-hot encoding", "B) Distributed embeddings", "C) Bag of words", "D) ASCII"], "ans": "B", "exp": "Distributed embeddings capture semantic similarity."},
    {"id": 206, "lec": 5, "q": "In distributed representations, what dimension is typical?", "opts": ["A) 3", "B) 10", "C) 128 or higher", "D) 1000"], "ans": "C", "exp": "Embeddings use high dimensions like 128+."},
    {"id": 207, "lec": 5, "q": "How are word embeddings learned?", "opts": ["A) Manually assigned", "B) Through standard learning (lookup tables)", "C) Random initialization only", "D) Fixed values"], "ans": "B", "exp": "Embeddings are learned through standard training methods."},
    {"id": 208, "lec": 5, "q": "What is Word2Vec?", "opts": ["A) A text editor", "B) A method for learning word embeddings", "C) A CNN architecture", "D) A database"], "ans": "B", "exp": "Word2Vec is a popular method for learning word embeddings."},
    {"id": 209, "lec": 5, "q": "What can autoencoders be used for?", "opts": ["A) Only image classification", "B) Learning embeddings", "C) Only text generation", "D) Database queries"], "ans": "B", "exp": "Autoencoders can learn distributed representations/embeddings."},
    {"id": 210, "lec": 5, "q": "What does Keras allow for embeddings?", "opts": ["A) Only pre-trained", "B) Training lookup table embeddings easily", "C) No embedding support", "D) Only one-hot encoding"], "ans": "B", "exp": "Keras allows easy training of embedding lookup tables."},
    {"id": 211, "lec": 5, "q": "What is a con of on-the-fly embeddings?", "opts": ["A) Too general", "B) Cluster words based on training task only", "C) Too large", "D) Too slow"], "ans": "B", "exp": "On-the-fly embeddings cluster based on specific task, not general semantics."},
    {"id": 212, "lec": 5, "q": "What is generally available for major embedding architectures?", "opts": ["A) No pre-trained options", "B) Pre-trained embeddings", "C) Only random embeddings", "D) Fixed embeddings"], "ans": "B", "exp": "Pre-trained embeddings are available for major architectures."},
    {"id": 213, "lec": 5, "q": "How can embeddings be used with CNNs?", "opts": ["A) Not possible", "B) 1D convolutions through embeddings", "C) Only 2D convolutions", "D) Only pooling"], "ans": "B", "exp": "1D convolutions can be applied through word embeddings."},
    {"id": 214, "lec": 5, "q": "What is transfer learning?", "opts": ["A) Transferring data between systems", "B) Using model from one task for another task", "C) Copying weights randomly", "D) Training from scratch"], "ans": "B", "exp": "Transfer learning uses a model trained on one task for another."},
    {"id": 215, "lec": 5, "q": "In transfer learning, what is typically done to the original network?", "opts": ["A) Use entire network as-is", "B) Split off top layer(s) as head", "C) Remove all layers", "D) Double all layers"], "ans": "B", "exp": "Top layer(s) are split off as task-specific head."},
    {"id": 216, "lec": 5, "q": "What does 'freeze' mean in transfer learning?", "opts": ["A) Delete weights", "B) Don't let weights change during training", "C) Double the weights", "D) Randomize weights"], "ans": "B", "exp": "Freezing means keeping weights fixed during new training."},
    {"id": 217, "lec": 5, "q": "What is 'fine-tuning'?", "opts": ["A) Deleting layers", "B) Allowing imported weights to change", "C) Freezing all weights", "D) Training from scratch"], "ans": "B", "exp": "Fine-tuning allows pre-trained weights to update with new data."},
    {"id": 218, "lec": 5, "q": "Which layers are assumed more application-specific?", "opts": ["A) Early layers", "B) Middle layers", "C) Top/head layers", "D) All layers equally"], "ans": "C", "exp": "Top/head layers are more task-specific."},
    {"id": 219, "lec": 5, "q": "Which layers capture more general features?", "opts": ["A) Top layers", "B) Early/lower layers", "C) Output layer only", "D) None"], "ans": "B", "exp": "Early layers capture general features useful across tasks."},
    {"id": 220, "lec": 5, "q": "When should you fine-tune vs freeze?", "opts": ["A) Always freeze", "B) Depends on task similarity and data amount", "C) Always fine-tune", "D) Randomly decide"], "ans": "B", "exp": "Decision depends on task similarity and available data."},
    {"id": 221, "lec": 5, "q": "What is the benefit of pre-trained embeddings?", "opts": ["A) Task-specific only", "B) General language understanding", "C) No benefit", "D) Slower training"], "ans": "B", "exp": "Pre-trained embeddings capture general language semantics."},
    {"id": 222, "lec": 5, "q": "What is a problem with Bag of Words vectors?", "opts": ["A) Too short", "B) Vectors are long", "C) Too semantic", "D) Captures order"], "ans": "B", "exp": "Bag of Words creates very long (high-dimensional) vectors."},
    {"id": 223, "lec": 5, "q": "What does 'distributed' mean in distributed embeddings?", "opts": ["A) Across multiple computers", "B) Meaning spread across vector dimensions", "C) Random distribution", "D) Distributed training only"], "ans": "B", "exp": "Meaning is distributed across multiple vector dimensions."},
    {"id": 224, "lec": 5, "q": "In meaning space, what should semantically similar words have?", "opts": ["A) Very different vectors", "B) Similar vectors (close in space)", "C) Same vector exactly", "D) Random vectors"], "ans": "B", "exp": "Similar words should have similar/close vectors."},
    {"id": 225, "lec": 5, "q": "What is Option 1 for using embeddings?", "opts": ["A) Pre-trained only", "B) Learning embeddings on the fly", "C) No embeddings", "D) Fixed embeddings"], "ans": "B", "exp": "Option 1 is learning embeddings during task training."},
    {"id": 226, "lec": 5, "q": "What is Option 2 for using embeddings?", "opts": ["A) Random embeddings", "B) Use pre-trained embeddings", "C) No embeddings", "D) One-hot only"], "ans": "B", "exp": "Option 2 is using pre-trained embeddings."},
    {"id": 227, "lec": 5, "q": "What architecture is mentioned as more complex for embeddings?", "opts": ["A) Simple lookup tables", "B) Transformers", "C) Decision trees", "D) Linear regression"], "ans": "B", "exp": "Transformers are more complex architectures for learning embeddings."},
    {"id": 228, "lec": 5, "q": "What is re-using embeddings beneficial for?", "opts": ["A) Tasks with little data", "B) Tasks with infinite data", "C) No benefit", "D) Only image tasks"], "ans": "A", "exp": "Re-use is especially beneficial when task data is limited."},
    {"id": 229, "lec": 5, "q": "What happens to on-the-fly embeddings for words B and C that should be similar?", "opts": ["A) Always similar", "B) May not capture semantic similarity", "C) Always identical", "D) No effect"], "ans": "B", "exp": "On-the-fly may not capture general semantic similarity."},
    {"id": 230, "lec": 5, "q": "What is knowledge transfer in transfer learning?", "opts": ["A) Copying data", "B) Using learned representations from original model", "C) Random weight initialization", "D) Training separate models"], "ans": "B", "exp": "Knowledge transfer uses learned representations from source task."},
    {"id": 231, "lec": 5, "q": "What is typically large in transfer learning scenario?", "opts": ["A) Application labels", "B) Original training data", "C) New network", "D) Test set only"], "ans": "B", "exp": "Original task typically has large training data."},
    {"id": 232, "lec": 5, "q": "What is the new network in transfer learning called?", "opts": ["A) Original network", "B) Application network/model", "C) Training network", "D) Validation network"], "ans": "B", "exp": "The target task uses the application network/model."},
    {"id": 233, "lec": 5, "q": "What can become considerably more complex for embeddings?", "opts": ["A) Simple lookup tables", "B) Architectures for learning embeddings", "C) Text input", "D) Output labels"], "ans": "B", "exp": "Embedding architectures can become very complex (e.g., Transformers)."},
    {"id": 234, "lec": 5, "q": "What is the 'Head' of a network?", "opts": ["A) Input layer", "B) Top layer(s)", "C) Hidden layers", "D) Weights"], "ans": "B", "exp": "The head is the top layer split off for new tasks."},
    {"id": 235, "lec": 5, "q": "What is the 'Body' of a network?", "opts": ["A) Output layer", "B) Lower/Early layers", "C) Head", "D) Bias"], "ans": "B", "exp": "The body contains the general feature layers."},
    {"id": 236, "lec": 5, "q": "What is 'Averaging Rather than Flattening'?", "opts": ["A) Pooling", "B) Embedding technique", "C) Loss function", "D) Optimizer"], "ans": "B", "exp": "It refers to how word vectors are combined."},
    {"id": 237, "lec": 5, "q": "What is the dimension of Word2Vec vectors?", "opts": ["A) 10", "B) 128+", "C) 2", "D) 1"], "ans": "B", "exp": "Embeddings are high dimensional (e.g., 128)."},
    {"id": 238, "lec": 5, "q": "What is the problem with ASCII for ML?", "opts": ["A) Too semantic", "B) Not information-centric", "C) Too short", "D) Too fast"], "ans": "B", "exp": "ASCII captures literal text, not meaning."},
    {"id": 239, "lec": 5, "q": "What is the problem with UTF8 for ML?", "opts": ["A) Too semantic", "B) Not information-centric", "C) Too short", "D) Too fast"], "ans": "B", "exp": "UTF8 captures literal text, not meaning."},
    {"id": 240, "lec": 5, "q": "What is the 'First Pass Solution' for text?", "opts": ["A) Embeddings", "B) Bag of Words", "C) Transformers", "D) RNN"], "ans": "B", "exp": "Bag of Words is a classical solution."},
    {"id": 241, "lec": 5, "q": "What is the 'Second Pass Solution' for text?", "opts": ["A) Bag of Words", "B) Distributed Embeddings", "C) ASCII", "D) One-Hot"], "ans": "B", "exp": "Distributed embeddings capture semantics."},
    {"id": 242, "lec": 5, "q": "What is One-Hot Encoding?", "opts": ["A) Dense vector", "B) Sparse vector", "C) Semantic vector", "D) Continuous vector"], "ans": "B", "exp": "One-hot vectors are very sparse."},
    {"id": 243, "lec": 5, "q": "What is the 'Meaning Space'?", "opts": ["A) Physical space", "B) Vector space for embeddings", "C) Data space", "D) Weight space"], "ans": "B", "exp": "Words are indexed in high-dimensional meaning space."},
    {"id": 244, "lec": 5, "q": "What is 'Lookup Table' embedding?", "opts": ["A) Fixed", "B) Learned", "C) Random", "D) Manual"], "ans": "B", "exp": "Lookup tables are learned during training."},
    {"id": 245, "lec": 5, "q": "What is '1D Convolution' used for in text?", "opts": ["A) Images", "B) Embeddings", "C) Audio", "D) Video"], "ans": "B", "exp": "1D convolutions work on word embeddings."},
    {"id": 246, "lec": 5, "q": "What is the 'Original Network' in Transfer Learning?", "opts": ["A) New model", "B) Pre-trained model", "C) Test model", "D) Validation model"], "ans": "B", "exp": "It is the model trained on the original task."},
    {"id": 247, "lec": 5, "q": "What is the 'Application Network'?", "opts": ["A) Pre-trained model", "B) New model for target task", "C) Old model", "D) Test model"], "ans": "B", "exp": "It is the model adapted for the new task."},
    {"id": 248, "lec": 5, "q": "What is 'Freezing' weights?", "opts": ["A) Updating them", "B) Keeping them fixed", "C) Deleting them", "D) Randomizing them"], "ans": "B", "exp": "Freezing prevents weight updates."},
    {"id": 249, "lec": 5, "q": "What is 'Fine-Tuning' weights?", "opts": ["A) Keeping them fixed", "B) Allowing them to update", "C) Deleting them", "D) Ignoring them"], "ans": "B", "exp": "Fine-tuning allows weight updates."},
    {"id": 250, "lec": 5, "q": "What is the trend in Embedding Architectures?", "opts": ["A) Simpler", "B) More Complex (Transformers)", "C) Static", "D) Removed"], "ans": "B", "exp": "Architectures are becoming more complex."},

    # --- LECTURE 06: RNNs (Q251-300) ---
    {"id": 251, "lec": 6, "q": "What type of data are RNNs designed for?", "opts": ["A) Independent samples", "B) Time series and sequential data", "C) Images only", "D) Tabular data only"], "ans": "B", "exp": "RNNs are designed for sequential/time series data."},
    {"id": 252, "lec": 6, "q": "Which is an example of sequential categorical data?", "opts": ["A) Images", "B) Language/text", "C) Numbers", "D) Coordinates"], "ans": "B", "exp": "Language is sequential categorical data."},
    {"id": 253, "lec": 6, "q": "What is language modelling?", "opts": ["A) Drawing language trees", "B) Building model of language's statistical properties", "C) Translating languages", "D) Counting words"], "ans": "B", "exp": "Language modelling describes statistical properties of language."},
    {"id": 254, "lec": 6, "q": "What can language models do?", "opts": ["A) Only translate", "B) Predict next word and sentence probability", "C) Only count words", "D) Only classify"], "ans": "B", "exp": "Language models predict next word and sentence probabilities."},
    {"id": 255, "lec": 6, "q": "What connections do RNNs have?", "opts": ["A) Only feedforward", "B) Connections forming directed cycles", "C) No connections", "D) Random connections"], "ans": "B", "exp": "RNNs have connections forming directed cycles."},
    {"id": 256, "lec": 6, "q": "What does having cycles give RNNs?", "opts": ["A) No state", "B) Internal state", "C) Only output state", "D) Fixed state"], "ans": "B", "exp": "Cycles give RNNs internal state for sequential processing."},
    {"id": 257, "lec": 6, "q": "What are RNNs prime candidates for?", "opts": ["A) Image classification", "B) Sequence learning problems", "C) Clustering", "D) Dimensionality reduction"], "ans": "B", "exp": "RNNs excel at sequence learning (speech, translation, etc.)."},
    {"id": 258, "lec": 6, "q": "How can a feedforward network become recurrent?", "opts": ["A) Remove layers", "B) Add connections from hidden units to hidden units", "C) Add more inputs", "D) Remove outputs"], "ans": "B", "exp": "Add connections from hidden units back to hidden units."},
    {"id": 259, "lec": 6, "q": "What can each hidden unit in RNN connect to?", "opts": ["A) Only itself", "B) Itself and other hidden units", "C) Only output", "D) Only input"], "ans": "B", "exp": "Hidden units connect to themselves and other hidden units."},
    {"id": 260, "lec": 6, "q": "What does 'unfolding' an RNN mean?", "opts": ["A) Compressing the network", "B) Following sequence of computation steps over time", "C) Removing layers", "D) Adding more inputs"], "ans": "B", "exp": "Unfolding shows the RNN across time steps."},
    {"id": 261, "lec": 6, "q": "What is an unwrapped RNN similar to?", "opts": ["A) CNN", "B) Hidden Markov Model", "C) Decision Tree", "D) K-Means"], "ans": "B", "exp": "Unwrapped RNN is similar to Hidden Markov Model."},
    {"id": 262, "lec": 6, "q": "What's different about RNN hidden units vs HMM?", "opts": ["A) RNN units are stochastic", "B) RNN units are not stochastic", "C) No difference", "D) HMM has more units"], "ans": "B", "exp": "RNN hidden units are deterministic, not stochastic like HMM."},
    {"id": 263, "lec": 6, "q": "What is used at each time step in RNN?", "opts": ["A) Different weights", "B) Same weights and biases", "C) Random weights", "D) No weights"], "ans": "B", "exp": "Same weights and biases are replicated at each time step."},
    {"id": 264, "lec": 6, "q": "What is the RNN hidden state equation?", "opts": ["A) h_t = Wx_t", "B) h_t = act(W_h x_t + U_h h_{t-1} + b_h)", "C) h_t = x_t + h_{t-1}", "D) h_t = W_o h_t"], "ans": "B", "exp": "h_t = act(W_h x_t + U_h h_{t-1} + b_h)."},
    {"id": 265, "lec": 6, "q": "What influences h_t computation?", "opts": ["A) Only current input", "B) Current input and previous hidden state", "C) Only previous state", "D) Random values"], "ans": "B", "exp": "h_t depends on current input x_t and previous state h_{t-1}."},
    {"id": 266, "lec": 6, "q": "Where is the output layer computed from?", "opts": ["A) Input directly", "B) Linear transformation of hidden units", "C) Previous output", "D) Random values"], "ans": "B", "exp": "Output is computed from transformation of hidden units."},
    {"id": 267, "lec": 6, "q": "When can loss be computed in RNN?", "opts": ["A) Only at end of sequence", "B) At each time step or at end", "C) Only at beginning", "D) Never"], "ans": "B", "exp": "Loss can be computed at each step or just at sequence end."},
    {"id": 268, "lec": 6, "q": "What problem occurs over many processing steps?", "opts": ["A) Too fast training", "B) Vanishing or exploding gradients", "C) No gradients", "D) Perfect gradients"], "ans": "B", "exp": "Many steps cause vanishing or exploding gradient problems."},
    {"id": 269, "lec": 6, "q": "Why do gradients vanish or explode in RNN?", "opts": ["A) Different weights each step", "B) Same matrix used at each step (like powers)", "C) No activation functions", "D) Too many layers"], "ans": "B", "exp": "Same matrix repeated is like taking a number to large power."},
    {"id": 270, "lec": 6, "q": "What can mitigate exploding gradients?", "opts": ["A) Larger learning rate", "B) L1 or L2 regularization", "C) More layers", "D) Less data"], "ans": "B", "exp": "Regularization encourages smaller weights, mitigating explosion."},
    {"id": 271, "lec": 6, "q": "What is gradient clipping?", "opts": ["A) Removing gradients", "B) Scaling down gradients if norm exceeds threshold", "C) Doubling gradients", "D) Random gradients"], "ans": "B", "exp": "Gradient clipping scales gradients when they exceed threshold."},
    {"id": 272, "lec": 6, "q": "What is T in gradient clipping?", "opts": ["A) Temperature", "B) Threshold hyperparameter", "C) Time step", "D) Training epoch"], "ans": "B", "exp": "T is the threshold hyperparameter for clipping."},
    {"id": 273, "lec": 6, "q": "What architecture was created to address vanishing gradients?", "opts": ["A) CNN", "B) LSTM", "C) MLP", "D) Autoencoder"], "ans": "B", "exp": "LSTM was specifically designed to address vanishing gradients."},
    {"id": 274, "lec": 6, "q": "What does LSTM use to control memory?", "opts": ["A) Single gate", "B) Gates controlling memory cells", "C) No gates", "D) Random connections"], "ans": "B", "exp": "LSTM uses gates to control memory cells."},
    {"id": 275, "lec": 6, "q": "What are memory cells designed to do?", "opts": ["A) Forget everything", "B) Retain information without modification for long periods", "C) Store only recent info", "D) Compress information"], "ans": "B", "exp": "Memory cells retain information for long periods."},
    {"id": 276, "lec": 6, "q": "What gates does LSTM have?", "opts": ["A) Only input gate", "B) Input, output, and forget gates", "C) Only output gate", "D) No gates"], "ans": "B", "exp": "LSTM has input, output, and forget gates."},
    {"id": 277, "lec": 6, "q": "What controls the gates in LSTM?", "opts": ["A) Fixed values", "B) Learnable weights based on input and previous hidden state", "C) Random values", "D) User input"], "ans": "B", "exp": "Gates are controlled by learnable weights."},
    {"id": 278, "lec": 6, "q": "What does the sigmoid function do in LSTM gates?", "opts": ["A) Outputs any value", "B) Forces values close to 0 or 1", "C) Always outputs 0.5", "D) Random output"], "ans": "B", "exp": "Sigmoid forces gate values close to 0 (block) or 1 (pass)."},
    {"id": 279, "lec": 6, "q": "What happens when sigmoid result multiplies another vector?", "opts": ["A) Always zeros it", "B) Allows info to pass through or blocks it", "C) Doubles it", "D) No effect"], "ans": "B", "exp": "Gate values control whether information passes or is blocked."},
    {"id": 280, "lec": 6, "q": "What was added to original LSTM formulation later?", "opts": ["A) Input gates", "B) Forget gates and peephole weights", "C) Output gates", "D) Memory cells"], "ans": "B", "exp": "Forget gates and peephole weights were added later."},
    {"id": 281, "lec": 6, "q": "What results has LSTM produced?", "opts": ["A) Poor results", "B) State-of-the-art on wide variety of problems", "C) Only good for images", "D) Only good for text"], "ans": "B", "exp": "LSTM has produced state-of-the-art results on many problems."},
    {"id": 282, "lec": 6, "q": "Which is NOT an LSTM application mentioned?", "opts": ["A) Neural Machine Translation", "B) Image Classification", "C) Chatbots", "D) Video Processing"], "ans": "B", "exp": "Image classification is typically CNN, not primary LSTM application."},
    {"id": 283, "lec": 6, "q": "What is ASR in LSTM applications?", "opts": ["A) Automatic System Recognition", "B) Automatic Speech Recognition", "C) Audio Signal Routing", "D) Advanced Sound Recording"], "ans": "B", "exp": "ASR = Automatic Speech Recognition."},
    {"id": 284, "lec": 6, "q": "What is the 'Cell State' in LSTM?", "opts": ["A) Output", "B) Memory highway", "C) Input", "D) Gate"], "ans": "B", "exp": "Cell state carries information across time steps."},
    {"id": 285, "lec": 6, "q": "What is the 'Forget Gate'?", "opts": ["A) Adds info", "B) Removes info from cell state", "C) Outputs info", "D) Resets network"], "ans": "B", "exp": "Forget gate decides what to remove from cell state."},
    {"id": 286, "lec": 6, "q": "What is the 'Input Gate'?", "opts": ["A) Removes info", "B) Adds new info to cell state", "C) Outputs info", "D) Resets network"], "ans": "B", "exp": "Input gate decides what new information to store."},
    {"id": 287, "lec": 6, "q": "What is the 'Output Gate'?", "opts": ["A) Removes info", "B) Adds info", "C) Decides what to output", "D) Resets network"], "ans": "C", "exp": "Output gate decides what to output based on cell state."},
    {"id": 288, "lec": 6, "q": "What function is used in LSTM gates?", "opts": ["A) ReLU", "B) Sigmoid", "C) Linear", "D) Step"], "ans": "B", "exp": "Sigmoid is used for gating (0 to 1)."},
    {"id": 289, "lec": 6, "q": "What function is used for Cell Candidate?", "opts": ["A) Sigmoid", "B) Tanh", "C) ReLU", "D) Linear"], "ans": "B", "exp": "Tanh is used to create candidate values (-1 to 1)."},
    {"id": 290, "lec": 6, "q": "What is 'Peephole Weights'?", "opts": ["A) Input weights", "B) Connection from cell to gates", "C) Output weights", "D) Bias"], "ans": "B", "exp": "Peephole weights allow cell state to influence gates."},
    {"id": 291, "lec": 6, "q": "What is the main advantage of LSTM?", "opts": ["A) Faster training", "B) Long-term dependency learning", "C) Less parameters", "D) Simpler architecture"], "ans": "B", "exp": "LSTMs handle long-term dependencies better than standard RNNs."},
    {"id": 292, "lec": 6, "q": "What is 'Unfolding' also known as?", "opts": ["A) Compressing", "B) Unwrapping", "C) Pruning", "D) Clipping"], "ans": "B", "exp": "Unfolding is unwrapping the RNN over time."},
    {"id": 293, "lec": 6, "q": "What is the 'Hidden Markov Model' similarity?", "opts": ["A) Stochastic units", "B) Unwrapped structure", "C) Convolution", "D) Pooling"], "ans": "B", "exp": "Unwrapped RNN looks like HMM structure."},
    {"id": 294, "lec": 6, "q": "What is the 'Vanishing Gradient' problem?", "opts": ["A) Gradient gets too large", "B) Gradient gets too small", "C) Gradient is zero", "D) Gradient is random"], "ans": "B", "exp": "Gradients diminish to zero over many steps."},
    {"id": 295, "lec": 6, "q": "What is the 'Exploding Gradient' problem?", "opts": ["A) Gradient gets too large", "B) Gradient gets too small", "C) Gradient is zero", "D) Gradient is random"], "ans": "A", "exp": "Gradients increase indefinitely over many steps."},
    {"id": 296, "lec": 6, "q": "What is the solution to Exploding Gradients?", "opts": ["A) LSTM", "B) Gradient Clipping", "C) More layers", "D) Less data"], "ans": "B", "exp": "Clipping scales down large gradients."},
    {"id": 297, "lec": 6, "q": "What is the solution to Vanishing Gradients?", "opts": ["A) Clipping", "B) LSTM", "C) More layers", "D) Less data"], "ans": "B", "exp": "LSTM architecture addresses vanishing gradients."},
    {"id": 298, "lec": 6, "q": "What is 'Video Processing' in RNNs?", "opts": ["A) Image classification", "B) Sequence of frames", "C) Static images", "D) Audio only"], "ans": "B", "exp": "Video is a sequence of image frames."},
    {"id": 299, "lec": 6, "q": "What is 'Neural Machine Translation'?", "opts": ["A) Image to Text", "B) Sequence to Sequence", "C) Text to Image", "D) Audio to Image"], "ans": "B", "exp": "It translates one sequence (language) to another."},
    {"id": 300, "lec": 6, "q": "What is the 'Hyperbolic Tangent' used for in RNN?", "opts": ["A) Gates", "B) Activation/Cell State", "C) Weights", "D) Bias"], "ans": "B", "exp": "Tanh is used for activation and cell state values."}
]

# ==============================================================================
# STREAMLIT APP - ENHANCED VERSION
# ==============================================================================

st.set_page_config(
    page_title="Deep Learning Quiz Master",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        padding: 1rem 0;
    }
    .question-counter {
        font-size: 1.2rem;
        font-weight: bold;
        color: #424242;
        background: #E3F2FD;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        display: inline-block;
    }
    .timer-box {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FFFFFF;
        background: #F44336;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        display: inline-block;
    }
    .timer-warning {
        background: #FF9800;
    }
    .timer-danger {
        background: #F44336;
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    .question-nav {
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }
    .flagged {
        border: 2px solid #FF9800;
        background: #FFF3E0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'selected_lecture' not in st.session_state:
    st.session_state.selected_lecture = "All"
if 'timer_enabled' not in st.session_state:
    st.session_state.timer_enabled = False
if 'time_limit' not in st.session_state:
    st.session_state.time_limit = 30  # minutes
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'flagged_questions' not in st.session_state:
    st.session_state.flagged_questions = set()
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = "practice"  # practice or exam

# Helper functions
def format_time(seconds):
    """Format seconds as MM:SS"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

def get_timer_color(time_left, total_time):
    """Get timer color based on remaining time"""
    if time_left <= 0:
        return "timer-danger"
    elif time_left < total_time * 0.2:
        return "timer-danger"
    elif time_left < total_time * 0.4:
        return "timer-warning"
    return ""

def init_quiz(lecture_selection, time_limit_minutes, mode):
    """Initialize quiz with selected parameters"""
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.show_result = False
    st.session_state.selected_lecture = lecture_selection
    st.session_state.time_limit = time_limit_minutes
    st.session_state.quiz_mode = mode
    st.session_state.flagged_questions = set()
    
    # Filter questions
    if lecture_selection == "All":
        st.session_state.quiz_questions = QUESTIONS.copy()
    else:
        lec_num = int(lecture_selection.split()[1])
        st.session_state.quiz_questions = [q for q in QUESTIONS if q['lec'] == lec_num]
    
    # Shuffle questions
    random.shuffle(st.session_state.quiz_questions)
    
    # Set start time
    if st.session_state.timer_enabled:
        st.session_state.start_time = datetime.now()

# Sidebar
with st.sidebar:
    st.title("🎓 Quiz Settings")
    st.markdown("---")
    
    # Lecture Selection
    lecture_options = ["All"] + [f"Lecture {i:02d}" for i in range(1, 7)]
    selected_lecture = st.selectbox(
        "📚 Select Lecture:",
        lecture_options,
        index=0
    )
    
    # Timer Settings
    st.markdown("### ⏱️ Timer Settings")
    timer_enabled = st.checkbox("Enable Timer", value=False)
    
    if timer_enabled:
        time_limit = st.selectbox(
            "Time Limit:",
            [10, 15, 20, 30, 45, 60],
            index=3  # Default 30 minutes
        )
        st.session_state.timer_enabled = True
        st.session_state.time_limit = time_limit
    else:
        st.session_state.timer_enabled = False
    
    # Quiz Mode
    st.markdown("### 🎯 Quiz Mode")
    quiz_mode = st.radio(
        "Select Mode:",
        ["Practice", "Exam"],
        help="Practice: Show answers immediately. Exam: Show results at end."
    )
    
    st.markdown("---")
    
    # Action Buttons
    if st.button("🚀 Start New Quiz", type="primary", use_container_width=True):
        init_quiz(selected_lecture, st.session_state.time_limit, quiz_mode.lower())
        st.rerun()
    
    if st.button("📊 View Summary", disabled=not st.session_state.quiz_started, use_container_width=True):
        st.session_state.show_result = True
        st.rerun()
    
    if st.button("🏠 Reset Quiz", use_container_width=True):
        st.session_state.quiz_started = False
        st.session_state.show_result = False
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = {}
        st.rerun()
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📈 Statistics")
    st.metric("Total Questions", len(QUESTIONS))
    if st.session_state.quiz_started:
        st.metric("Quiz Questions", len(st.session_state.quiz_questions))
        answered = len(st.session_state.answers)
        st.metric("Answered", f"{answered}/{len(st.session_state.quiz_questions)}")
    
    # Flagged Questions
    if st.session_state.flagged_questions:
        st.markdown("### 🚩 Flagged Questions")
        for q_num in sorted(st.session_state.flagged_questions):
            st.write(f"• Question {q_num + 1}")

# Main Content
st.markdown('<p class="main-header">🎓 Deep Learning & Gen AI Quiz Master</p>', unsafe_allow_html=True)
st.markdown("---")

if not st.session_state.quiz_started:
    # Welcome Screen
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Total Questions", "300")
    with col2:
        st.metric("📖 Lectures", "6")
    with col3:
        st.metric("✅ Passing Score", "60%")
    
    st.markdown("""
    ### 📋 Quiz Features
    
    | Feature | Description |
    |---------|-------------|
    | ⏱️ **Timer** | Optional countdown timer (10-60 minutes) |
    | 📊 **Question Counter** | Track progress (e.g., 15/50) |
    | ⬅️➡️ **Navigation** | Move between questions freely |
    | 🚩 **Flag Questions** | Mark questions for review |
    | 📝 **Two Modes** | Practice (instant feedback) or Exam (results at end) |
    | 📈 **Progress Bar** | Visual progress indicator |
    | 📊 **Question Grid** | Jump to any question quickly |
    | 💾 **Auto-save** | Answers saved automatically |
    | 📤 **Export Results** | Download results as CSV |
    
    ### 🎯 How to Use
    
    1. **Select Lecture** - Choose specific lecture or all
    2. **Enable Timer** (optional) - Set time limit
    3. **Choose Mode** - Practice or Exam
    4. **Start Quiz** - Begin answering questions
    5. **Navigate** - Use Previous/Next buttons
    6. **Submit** - View results when done
    """)
    
    st.info("💡 **Tip:** Use Practice mode for learning, Exam mode for testing!")
    
else:
    questions = st.session_state.quiz_questions
    total_questions = len(questions)
    
    # Timer Display
    if st.session_state.timer_enabled and st.session_state.start_time:
        elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
        total_seconds = st.session_state.time_limit * 60
        time_left = max(0, total_seconds - elapsed)
        
        timer_class = get_timer_color(time_left, total_seconds)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.markdown(f"**Quiz Mode:** {st.session_state.quiz_mode.title()}")
        with col2:
            st.markdown(f'<p class="timer-box {timer_class}">⏱️ {format_time(int(time_left))}</p>', unsafe_allow_html=True)
        with col3:
            st.markdown(f"**Lecture:** {st.session_state.selected_lecture}")
        
        if time_left <= 0:
            st.error("⏰ Time's up! Submitting your answers...")
            st.session_state.show_result = True
            st.rerun()
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Quiz Mode:** {st.session_state.quiz_mode.title()}")
        with col2:
            st.markdown(f"**Lecture:** {st.session_state.selected_lecture}")
    
    st.markdown("---")
    
    if st.session_state.show_result:
        # Results Page
        st.markdown("## 📊 Quiz Results")
        
        # Calculate score
        correct_count = 0
        for q_idx, answer_data in st.session_state.answers.items():
            if q_idx < len(questions):
                if answer_data.get('answer') == questions[q_idx]['ans']:
                    correct_count += 1
        
        percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        # Score Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Questions", total_questions)
        with col2:
            st.metric("Correct", correct_count)
        with col3:
            st.metric("Incorrect", total_questions - correct_count)
        with col4:
            st.metric("Score", f"{percentage:.1f}%")
        
        # Progress Bar
        st.progress(percentage / 100)
        
        # Performance Message
        if percentage >= 80:
            st.success("🎉 Excellent! You've mastered this material!")
        elif percentage >= 60:
            st.info("👍 Good job! Review incorrect topics to improve.")
        else:
            st.warning("📚 Keep studying! Review the lectures and try again.")
        
        # Time Taken
        if st.session_state.timer_enabled and st.session_state.start_time:
            time_taken = (datetime.now() - st.session_state.start_time).total_seconds()
            st.info(f"⏱️ **Time Taken:** {format_time(int(time_taken))}")
        
        # Detailed Results
        with st.expander("📋 View Detailed Results", expanded=True):
            for i, q in enumerate(questions):
                answer_data = st.session_state.answers.get(i, {})
                user_answer = answer_data.get('answer', 'Not answered')
                is_correct = user_answer == q['ans']
                
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**Q{i+1}.** {q['q']}")
                        st.markdown(f"- Your Answer: **{user_answer}**")
                        st.markdown(f"- Correct Answer: **{q['ans']}**")
                        if not is_correct:
                            st.markdown(f"- 💡 {q['exp']}")
                    with col2:
                        if is_correct:
                            st.success("✅")
                        else:
                            st.error("❌")
                    st.markdown("---")
        
        # Export Results
        st.markdown("### 📤 Export Results")
        
        # Create CSV data
        csv_data = "Question ID,Lecture,Question,Your Answer,Correct Answer,Explanation\n"
        for i, q in enumerate(questions):
            answer_data = st.session_state.answers.get(i, {})
            user_answer = answer_data.get('answer', 'Not answered')
            csv_data += f"{q['id']},{q['lec']},\"{q['q']}\",{user_answer},{q['ans']},\"{q['exp']}\"\n"
        
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv_data,
            file_name=f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Try Again", type="primary", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.show_result = False
                st.rerun()
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.show_result = False
                st.rerun()
    
    else:
        # Quiz Page
        q = questions[st.session_state.current_question]
        
        # Question Counter & Progress
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown(f'<p class="question-counter">📍 Question {st.session_state.current_question + 1}/{total_questions}</p>', unsafe_allow_html=True)
        with col2:
            st.progress((st.session_state.current_question + 1) / total_questions)
        with col3:
            is_flagged = st.session_state.current_question in st.session_state.flagged_questions
            if st.button("🚩 Flag" if not is_flagged else "✅ Unflag", key="flag_btn"):
                if is_flagged:
                    st.session_state.flagged_questions.discard(st.session_state.current_question)
                else:
                    st.session_state.flagged_questions.add(st.session_state.current_question)
                st.rerun()
        
        st.markdown("---")
        
        # Question Navigation Grid
        with st.expander("📍 Question Navigator", expanded=False):
            cols_per_row = 10
            total_rows = (total_questions + cols_per_row - 1) // cols_per_row
            
            for row in range(total_rows):
                cols = st.columns(cols_per_row)
                for col_idx in range(cols_per_row):
                    q_num = row * cols_per_row + col_idx
                    if q_num < total_questions:
                        with cols[col_idx]:
                            is_answered = q_num in st.session_state.answers
                            is_current = q_num == st.session_state.current_question
                            is_flagged = q_num in st.session_state.flagged_questions
                            
                            button_label = f"{q_num + 1}"
                            if is_flagged:
                                button_label = f"🚩{q_num + 1}"
                            
                            if st.button(button_label, key=f"nav_{q_num}", 
                                       use_container_width=True,
                                       type="primary" if is_current else "secondary"):
                                st.session_state.current_question = q_num
                                st.rerun()
        
        st.markdown("---")
        
      # Question Display
        st.markdown(f"### 📝 Question {st.session_state.current_question + 1}")
        st.markdown(f"**Lecture {q['lec']}**")
        st.markdown(f"**{q['q']}**")
        
        # Get current answer if exists
        current_answer = st.session_state.answers.get(st.session_state.current_question, {}).get('answer')
        
        # Display options with full text
        option_labels = q['opts']  # Full option text like "A) The variable..."

        current_index = None
        if current_answer:
            for idx, opt in enumerate(option_labels):
                if opt.startswith(f"{current_answer})"):
                    current_index = idx
                    break

        selected = st.radio(
            "Select your answer:",
            options,
            index=default_index,
            key=f"question_{st.session_state.current_question}_{len(st.session_state.answers)}"
        )
        
        # Save answer immediately when selection changes
        if selected:
            answer_letter = selected.split(')')[0].strip()
            # Only update if different from stored
            if st.session_state.answers.get(st.session_state.current_question, {}).get('answer') != answer_letter:
                st.session_state.answers[st.session_state.current_question] = {
                    'answer': answer_letter,
                    'question': q['q'],
                    'correct_answer': q['ans']
                }
                st.rerun() 
        
        st.markdown("---")
        
        # Navigation Buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⬅️ Previous", disabled=st.session_state.current_question == 0, use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
        
        with col2:
            if st.button("➡️ Next", disabled=st.session_state.current_question >= total_questions - 1, use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
        
        with col3:
            if st.button("💾 Save & Continue", use_container_width=True):
                st.success("Answer saved!")
                if st.session_state.current_question < total_questions - 1:
                    st.session_state.current_question += 1
                    st.rerun()
        
        with col4:
            if st.button("📤 Submit Quiz", type="primary", use_container_width=True):
                st.session_state.show_result = True
                st.rerun()
        
        # Practice Mode Feedback
        if st.session_state.quiz_mode == "practice":
            # Get answer from session state instead of radio button
            answer_data = st.session_state.answers.get(st.session_state.current_question, {})
            selected_letter = answer_data.get('answer')
            
            if selected_letter:
                st.markdown("---")
                is_correct = selected_letter == q['ans']
                if is_correct:
                    st.success(" Correct!")
                else:
                    st.error(f" Incorrect. Correct answer: **{q['ans']}**")
                
                st.info(f" **Explanation:** {q['exp']}")
        
        # Jump to Section
        st.markdown("---")
        st.markdown("### 🎯 Quick Navigation")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⏮️ First Question", use_container_width=True):
                st.session_state.current_question = 0
                st.rerun()
        with col2:
            unanswered = [i for i in range(total_questions) if i not in st.session_state.answers]
            if unanswered and st.button("🔍 Next Unanswered", use_container_width=True):
                for q_num in unanswered:
                    if q_num > st.session_state.current_question:
                        st.session_state.current_question = q_num
                        st.rerun()
        with col3:
            if st.session_state.flagged_questions and st.button("🚩 Next Flagged", use_container_width=True):
                flagged_sorted = sorted(st.session_state.flagged_questions)
                for q_num in flagged_sorted:
                    if q_num > st.session_state.current_question:
                        st.session_state.current_question = q_num
                        st.rerun()
                st.session_state.current_question = flagged_sorted[0]
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ using Streamlit | Deep Learning & Gen AI Course</p>
    <p>© 2026 Quiz Master | All 300 Questions from 6 Lectures</p>
</div>
""", unsafe_allow_html=True)
