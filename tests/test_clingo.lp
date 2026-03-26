% % ============================================================
% % Answer Set Programming - Einstein-style Puzzle (3 Houses)
% % ============================================================

% % ============================================================
% % INSTANCE
% % ============================================================

% % Houses numbered 1 to 3
% house(1). house(2). house(3).

% % People
% name(peter). name(eric). name(arnold).

% % Drinks
% drink(tea). drink(water). drink(milk).

% % ============================================================
% % ENCODING
% % ============================================================

% % Assign exactly one name to each house
% 1 { assigned_name(H, N) : name(N) } 1 :- house(H).
% % Each name is assigned to exactly one house
% :- name(N), #count { H, assigned_name(H, N) } != 1.

% % Assign exactly one drink to each house
% 1 { assigned_drink(H, D) : drink(D) } 1 :- house(H).
% % Each drink is assigned to exactly one house
% :- drink(D), #count { H : assigned_drink(H, D) } != 1.

% % ---- Clues ----

% % Clue 1: Peter is in the second house.
% :- not assigned_name(2, peter).

% % % Clue 2: Arnold is directly left of the one who only drinks water.
% % % i.e., there exists a house H such that Arnold is at H and water is at H+1
% % :- assigned_name(H, arnold), not assigned_drink(H+1, water), house(H), house(H+1).
% % :- assigned_drink(H, water), not assigned_name(H-1, arnold), house(H), house(H-1).


% % % Clue 3: The one who only drinks water is directly left of the person who likes milk.
% % % i.e., there exists a house H such that water is at H and milk is at H+1
% % :- assigned_drink(H, water), not assigned_drink(H+1, milk), house(H), house(H+1).
% % :- assigned_drink(H, milk), not assigned_drink(H-1, water), house(H), house(H-1).

% % Clue 2: Arnold is directly left of the one who only drinks water.
% % There must exist a house H where Arnold lives and water is at H+1
% :- not 1 { assigned_name(H, arnold) : assigned_drink(H+1, water), house(H), house(H+1) } 1.

% % Clue 3: The one who only drinks water is directly left of the person who likes milk.
% % There must exist a house H where water is at H and milk is at H+1
% :- not 1 { assigned_drink(H, water) : assigned_drink(H+1, milk), house(H), house(H+1) } 1.


% % ============================================================
% % QUERY
% % ============================================================

% % Display all attributes for each house
% #show assigned_name/2.
% #show assigned_drink/2.








% Zebr% Houses
house(1..3).

% Categories
name(arnold; eric; peter).
vacation(beach; mountain; city).
flower(carnations; daffodils; lilies).
month(april; jan; sept).

% Exactly one value of each category per house
1 { house_name(H,N) : name(N) } 1 :- house(H).
1 { house_vacation(H,V) : vacation(V) } 1 :- house(H).
1 { house_flower(H,F) : flower(F) } 1 :- house(H).
1 { house_month(H,M) : month(M) } 1 :- house(H).

% Each value is used by exactly one house
1 { house_name(H,N) : house(H) } 1 :- name(N).
1 { house_vacation(H,V) : house(H) } 1 :- vacation(V).
1 { house_flower(H,F) : house(H) } 1 :- flower(F).
1 { house_month(H,M) : house(H) } 1 :- month(M).

% Clue 1: Eric is the person who prefers city breaks.
:- house_name(H,eric), not house_vacation(H,city).
:- house_vacation(H,city), not house_name(H,eric).

% Clue 2: Peter is the person who loves beach vacations.
:- house_name(H,peter), not house_vacation(H,beach).
:- house_vacation(H,beach), not house_name(H,peter).

% Clue 3: Arnold is somewhere to the right of the person who loves carnations.
:- house_name(HA,arnold), house_flower(HC,carnations), HA <= HC.

% Clue 4: The person whose birthday is in April is the person who loves daffodils.
:- house_month(H,april), not house_flower(H,daffodils).
:- house_flower(H,daffodils), not house_month(H,april).

% Clue 5: The person who loves carnations is Peter.
:- house_flower(H,carnations), not house_name(H,peter).
:- house_name(H,peter), not house_flower(H,carnations).

% Clue 6: The person whose birthday is in September is somewhere to the left of Peter.
:- house_month(HS,sept), house_name(HP,peter), HS >= HP.

% Query output: list all attributes for each house
#show house_name/2.
#show house_vacation/2.
#show house_flower/2.
#show house_month/2.