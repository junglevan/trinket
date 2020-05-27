function J = computeCost(X, y, theta)
    m = rows(y); % number of training examples
    J = 0;
    h = X*theta - y;
    J = 1/(2*m) * sum(h.^2);
end
