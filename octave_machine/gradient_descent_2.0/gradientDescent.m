function [theta, J_history] = gradientDescent(X, y, theta, alpha, num_iters)
    m = rows(y); % number of training examples
    J_history = zeros(num_iters, 1);

    for iter = 1:num_iters
        theta = theta - alpha/m*X'*(X*theta - y); %递归,X*theta-y=hθ(xi)-yi;关于X的一组值,*X准导,关于每个θ维度的一视同仁得和
        J_history(iter) = computeCost(X, y, theta)

    end

end
