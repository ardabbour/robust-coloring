% k is the maximum number of colors defined
{ color(X,1..k) } = 1 :- vertex(X).

% Adjacent vertices have different colors
:- edge(X,Y), color(X,C), color(Y,C).

% Define penalty
penalty(X,Y,P) :- color(X,C), color(Y,C), cost(X,Y,P).

% Minimize the penalty.
:~ penalty(X,Y,P). [P@1,X]

% Display
% #show color/2.
% #show penalty/3.
