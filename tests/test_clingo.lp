% ============================================================
% Answer Set Programming - Einstein-style Puzzle (3 Houses)
% ============================================================

% ============================================================
% INSTANCE
% ============================================================

% Houses numbered 1 to 3
house(1). house(2). house(3).

% People
name(peter). name(eric). name(arnold).

% Drinks
drink(tea). drink(water). drink(milk).

% ============================================================
% ENCODING
% ============================================================

% Assign exactly one name to each house
1 { assigned_name(H, N) : name(N) } 1 :- house(H).
% Each name is assigned to exactly one house
:- name(N), #count { H : assigned_name(H, N) } != 1.

% Assign exactly one drink to each house
1 { assigned_drink(H, D) : drink(D) } 1 :- house(H).
% Each drink is assigned to exactly one house
:- drink(D), #count { H : assigned_drink(H, D) } != 1.

% ---- Clues ----

% Clue 1: Peter is in the second house.
:- not assigned_name(2, peter).

% % Clue 2: Arnold is directly left of the one who only drinks water.
% % i.e., there exists a house H such that Arnold is at H and water is at H+1
% :- assigned_name(H, arnold), not assigned_drink(H+1, water), house(H), house(H+1).
% :- assigned_drink(H, water), not assigned_name(H-1, arnold), house(H), house(H-1).


% % Clue 3: The one who only drinks water is directly left of the person who likes milk.
% % i.e., there exists a house H such that water is at H and milk is at H+1
% :- assigned_drink(H, water), not assigned_drink(H+1, milk), house(H), house(H+1).
% :- assigned_drink(H, milk), not assigned_drink(H-1, water), house(H), house(H-1).

% Clue 2: Arnold is directly left of the one who only drinks water.
% There must exist a house H where Arnold lives and water is at H+1
:- not 1 { assigned_name(H, arnold) : assigned_drink(H+1, water), house(H), house(H+1) } 1.

% Clue 3: The one who only drinks water is directly left of the person who likes milk.
% There must exist a house H where water is at H and milk is at H+1
:- not 1 { assigned_drink(H, water) : assigned_drink(H+1, milk), house(H), house(H+1) } 1.


% ============================================================
% QUERY
% ============================================================

% Display all attributes for each house
#show assigned_name/2.
#show assigned_drink/2.