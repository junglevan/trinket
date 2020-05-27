clc
pause
data=load('test.txt');
m=rows(data)
n=columns(data)
X=[ones(m,1),data(:,1:n-1)]
y=data(:,n)
alpha=0.000001
iterations=1500
theta=zeros(n,1)
theta = gradientDescent(X, y, theta, alpha, iterations);
%==========only for 2 dimension==============
plot(X(:,2),X*theta,'-','LineWidth',3);
hold on;
plot(X(:,2),y,'rx','MarkerSize',10);
xlabel('size');
ylabel('price');
