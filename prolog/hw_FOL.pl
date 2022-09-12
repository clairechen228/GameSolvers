%KB
parent(charles, william).
parent(charles, harry).
parent(elizabeth, charles).
parent(george, elizabeth).
parent(george, margaret).
parent(elizabeth, anne).
parent(elizabeth, andrew).
parent(elizabeth, edward).
parent(anne, peter).
parent(anne, zara).
parent(andrew, beatrice).
parent(andrew, eugenie).
parent(edward, louise).
parent(edward, james).

child(X,Y) :- parent(Y,X).
sibling(X,Y) :- parent(P,X), parent(P,Y), X\=Y.
cousin(X,Y) :- parent(PX,X), parent(PY,Y), sibling(PX,PY).
ancestor(A,X) :- parent(A,X);(parent(A,Z), ancestor(Z,X)).

%Lists and Sorting
len([], 0).
len([_ | T], N) :- len(T, M), N is M+1.
%sorted(L)
sorted([]).
sorted([_]).
sorted([X,Y|T]) :- X=<Y, sorted([Y|T]).
%perm(L,M)
perm([],[]).
perm([H|T],M) :- perm(T,Z),append(X,Y,Z),append(X,[H|Y],M).
%mysort(L, M) 
mysort(L,M) :- perm(L,M),sorted(M).
