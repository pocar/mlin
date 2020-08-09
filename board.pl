% fa

:- dynamic board/1.

init:-
    retractall(board(_,_)),
    assert(board(1, [_I1, _I2, _I3, _I4, _I5, _I6, _I7, _I8])),
    assert(board(2, [_M1, _M2, _M3, _M4, _M5, _M6, _M7, _M8])),
    assert(board(3, [_O1, _O2, _O3, _O4, _O5, _O6, _O7, _O8])).
:- init.

adjecent(1, 2). adjecent(2, 3). adjecent(4, 5). adjecent(5, 6). adjecent(7, 8).
adjecent(8, 1).
neighbour(X, Y) :- adjecent(X, Y); adjecent(Y, X).

%% place
place(P, 1, [X1|R], [P|R]) :- var(X1).
place(P, 2, [X1,X2|R], [X1,P|R]) :- var(X2).
place(P, 3, [X1,X2,X3|R], [X1,X2,P|R]) :- var(X3).
place(P, 4, [X1,X2,X3,X4|R], [X1,X2,X3,P|R]) :- var(X4).
place(P, 5, [X1,X2,X3,X4,X5|R], [X1,X2,X3,X4,P|R]) :- var(X5).
place(P, 6, [X1,X2,X3,X4,X5,X6|R], [X1,X2,X3,X4,X5,P|R]) :- var(X6).
place(P, 7, [X1,X2,X3,X4,X5,X6,X7|R], [X1,X2,X3,X4,X5,X6,P|R]) :- var(X7).
place(P, 8, [X1,X2,X3,X4,X5,X6,X7,X8|R], [X1,X2,X3,X4,X5,X6,X7,P|R]) :- var(X8).

%% take
take(P, 1, [X1|R], [_|R]) :- \+var(X1), X1=P.
take(P, 2, [X1,X2|R], [X1,_|R]) :- \+var(X2), X2=P.
take(P, 3, [X1,X2,X3|R], [X1,X2,_|R]) :- \+var(X3), X3=P.
take(P, 4, [X1,X2,X3,X4|R], [X1,X2,X3,_|R]) :- \+var(X4), X4=P.
take(P, 5, [X1,X2,X3,X4,X5|R], [X1,X2,X3,X4,_|R]) :- \+var(X5), X5=P.
take(P, 6, [X1,X2,X3,X4,X5,X6|R], [X1,X2,X3,X4,X5,_|R]) :- \+var(X6), X6=P.
take(P, 7, [X1,X2,X3,X4,X5,X6,X7|R], [X1,X2,X3,X4,X5,X6,_|R]) :- \+var(X7), X7=P.
take(P, 8, [X1,X2,X3,X4,X5,X6,X7,X8|R], [X1,X2,X3,X4,X5,X6,X7,_|R]) :- \+var(X8), X8=P.

% drag(+,+,+,-,-,-)
drag(P, Src, Dst, Bin, Bout) :- take(P, Src, Bin, B1), place(P, Dst, B1, Bout).

record(R, B) :- retractall(board(R, _)), assert(board(R, B)).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
showBoard :- 
   board(1, [Z1,Z2,Z3,Z4,Z5,Z6,Z7,Z8]),
   board(2, [X1,X2,X3,X4,X5,X6,X7,X8]),
   board(3, [Y1,Y2,Y3,Y4,Y5,Y6,Y7,Y8]),
   write('    '),mark(Y1),write('--'),mark(Y2),write('--'),mark(Y3),nl,
   write('    |'),mark(X1),write('-'),mark(X2),write('-'),mark(X3),write('|'),nl, 
   write('    ||'),mark(Z1),mark(Z2),mark(Z3),write('||'),nl,
   write('    '),mark(Y8),mark(X8),mark(Z8),write(' '),mark(Z4),mark(X4),mark(Y4),nl,
   write('    ||'),mark(Z7),mark(Z6),mark(Z5),write('||'),nl,
   write('    |'),mark(X7),write('-'),mark(X6),write('-'),mark(X5),write('|'),nl,
   write('    '),mark(Y7),write('--'),mark(Y6),write('--'),mark(Y5),nl.
s :- showBoard.

mark(X) :- 
   var(X),
   write('#').
mark(X) :- 
   \+var(X),
   write(X).
   
p(Player, (X,Y)) :-
    board(X,B),
    place(Player, Y, B, Bout),
    record(X, Bout),
    showBoard.
    
t(Player, (X,Y)) :-
    board(X,B),
    take(Player, Y, B, Bout),
    record(X, Bout),
    showBoard.
    
m(Player, (X0, Y0), (X1, Y1)) :-
    X0 =:= X1, neighbour(Y0, Y1),
    board(X0,B),
    drag(Player, Y0, Y1, B, Bout),
    record(X0, Bout),
    showBoard.
    
m(Player, (X0,Y0), (X1, Y1)) :-
    neighbour(X0, X1), Y0 =:= Y1, 0 is mod(Y0, 2),
    board(X0, B0),
    board(X1, B1),
    take(Player, Y0, B0, B0out),
    place(Player, Y1, B1, B1out),
    record(X0, B0out),
    record(X1, B1out),
    showBoard.