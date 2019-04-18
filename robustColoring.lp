% Generate
% Max number of colors is number of vertices
colors(X) :- vertex(X).
{ color(X,C) : colors(C) } = 1 :- vertex(X).

% Adjacent vertices have different colors
:- edge(X,Y), color(X,C), color(Y,C).

% Define penalty
penalty(X,Y,P) :- color(X,C), color(Y,C), cost(X,Y,P).

% Minimize the number of colors.
:~ color(X,C). [1@2,C]

% Minimize the penalty.
:~ penalty(X,Y,P). [P@1,X]

% Display
#show color/2.
#show penalty/3.