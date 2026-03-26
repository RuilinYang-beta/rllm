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








% Zebra-style logic puzzle encoded in Answer Set Programming (ASP)
% Houses are numbered 1..6 from left to right.

%--------------------------------------------------
% Domains
%--------------------------------------------------

house(1..6).

name(peter; eric; carol; arnold; bob; alice).
color(blue; red; green; yellow; purple; white).
vacation(city; beach; cruise; cultural; mountain; camping).
hair(blonde; black; gray; brown; redhair; auburn).
job(artist; lawyer; engineer; teacher; doctor; nurse).
flower(roses; iris; daffodils; carnations; tulips; lilies).

%--------------------------------------------------
% Exactly one value of each category per house
%--------------------------------------------------

1 { house_name(H,N) : name(N) } 1 :- house(H).
1 { house_color(H,C) : color(C) } 1 :- house(H).
1 { house_vacation(H,V) : vacation(V) } 1 :- house(H).
1 { house_hair(H,R) : hair(R) } 1 :- house(H).
1 { house_job(H,J) : job(J) } 1 :- house(H).
1 { house_flower(H,F) : flower(F) } 1 :- house(H).

%--------------------------------------------------
% Each value used exactly once across houses
%--------------------------------------------------

1 { house_name(H,N) : house(H) } 1 :- name(N).
1 { house_color(H,C) : house(H) } 1 :- color(C).
1 { house_vacation(H,V) : house(H) } 1 :- vacation(V).
1 { house_hair(H,R) : house(H) } 1 :- hair(R).
1 { house_job(H,J) : house(H) } 1 :- job(J).
1 { house_flower(H,F) : house(H) } 1 :- flower(F).

%--------------------------------------------------
% Helper relations
%--------------------------------------------------

right_of(H1,H2) :- house(H1), house(H2), H1 > H2.
left_of(H1,H2) :- house(H1), house(H2), H1 < H2.
next_to(H1,H2) :- house(H1), house(H2), H1 = H2 + 1.
next_to(H1,H2) :- house(H1), house(H2), H1 = H2 - 1.
directly_left(H1,H2) :- house(H1), house(H2), H2 = H1 + 1.
one_between(H1,H2) :- house(H1), house(H2), H1 = H2 + 2.
one_between(H1,H2) :- house(H1), house(H2), H2 = H1 + 2.

%--------------------------------------------------
% Clues
%--------------------------------------------------

% 1. The person who loves a bouquet of daffodils is the person who is an artist.
house_job(H,artist) :- house_flower(H,daffodils).
house_flower(H,daffodils) :- house_job(H,artist).

% 2. The person who enjoys camping trips is the person whose favorite color is green.
house_color(H,green) :- house_vacation(H,camping).
house_vacation(H,camping) :- house_color(H,green).

% 3. The person who has brown hair is in the first house.
house_hair(1,brown).

% 4. The person who loves blue is somewhere to the right of the person who enjoys mountain retreats.
:- house_color(H1,blue), house_vacation(H2,mountain), not right_of(H1,H2).

% 5. The person who loves the vase of tulips is the person who enjoys mountain retreats.
house_vacation(H,mountain) :- house_flower(H,tulips).
house_flower(H,tulips) :- house_vacation(H,mountain).

% 6. Eric is in the second house.
house_name(2,eric).

% 7. The person who likes going on cruises and Arnold are next to each other.
:- house_vacation(H1,cruise), house_name(H2,arnold), not next_to(H1,H2).

% 8. The person who loves yellow and the person who enjoys camping trips are next to each other.
:- house_color(H1,yellow), house_vacation(H2,camping), not next_to(H1,H2).

% 9. The person who loves yellow is somewhere to the left of Peter.
:- house_color(H1,yellow), house_name(H2,peter), not left_of(H1,H2).

% 10. The person who is a lawyer and Arnold are next to each other.
:- house_job(H1,lawyer), house_name(H2,arnold), not next_to(H1,H2).

% 11. The person who has red hair is Arnold.
house_name(H,arnold) :- house_hair(H,redhair).
house_hair(H,redhair) :- house_name(H,arnold).

% 12. Alice is the person who is a doctor.
house_job(H,doctor) :- house_name(H,alice).
house_name(H,alice) :- house_job(H,doctor).

% 13. The person who loves purple is directly left of the person who loves the vase of tulips.
:- house_color(H1,purple), house_flower(H2,tulips), not directly_left(H1,H2).

% 14. The person who has brown hair is somewhere to the left of the person who is an engineer.
:- house_hair(H1,brown), house_job(H2,engineer), not left_of(H1,H2).

% 15. The person who has gray hair is somewhere to the left of the person whose favorite color is red.
:- house_hair(H1,gray), house_color(H2,red), not left_of(H1,H2).

% 16. The person who is an artist is somewhere to the right of Arnold.
:- house_job(H1,artist), house_name(H2,arnold), not right_of(H1,H2).

% 17. Alice is the person who loves the boquet of lilies.
house_flower(H,lilies) :- house_name(H,alice).
house_name(H,alice) :- house_flower(H,lilies).

% 18. The person whose favorite color is red is directly left of the person who prefers city breaks.
:- house_color(H1,red), house_vacation(H2,city), not directly_left(H1,H2).

% 19. The person who prefers city breaks is somewhere to the right of the person who has blonde hair.
:- house_vacation(H1,city), house_hair(H2,blonde), not right_of(H1,H2).

% 20. There is one house between Alice and Bob.
:- house_name(H1,alice), house_name(H2,bob), not one_between(H1,H2).

% 21. The person who loves the rose bouquet is directly left of the person who is a nurse.
:- house_flower(H1,roses), house_job(H2,nurse), not directly_left(H1,H2).

% 22. The person whose favorite color is green is in the fourth house.
house_color(4,green).

% 23. The person who loves beach vacations is somewhere to the left of the person who has red hair.
:- house_vacation(H1,beach), house_hair(H2,redhair), not left_of(H1,H2).

% 24. The person who has black hair is Alice.
house_name(H,alice) :- house_hair(H,black).
house_hair(H,black) :- house_name(H,alice).

% 25. The person who loves blue is the person who loves a carnations arrangement.
house_flower(H,carnations) :- house_color(H,blue).
house_color(H,blue) :- house_flower(H,carnations).

%--------------------------------------------------
% Query output
%--------------------------------------------------

#show house_name/2.
#show house_color/2.
#show house_vacation/2.
#show house_hair/2.
#show house_job/2.
#show house_flower/2.