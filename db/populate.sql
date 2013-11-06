BEGIN TRANSACTION;

insert into "user" (email, name, password, admin) values ('aatu@example.com', 'Aatu A. Admin', '$2a$12$OCm372a0jVx3aiyVFF/20ebBPYDuiNbF68trrjXnS.JCdeRaeMkNq', true);
insert into "user" (email, name, password, admin) values ('yrjo@example.com', 'Yrjö Ylläpitäjä', '$2a$12$SWAvjbRh7R1Zj/vupR1xouP.Vand9t7UhqQjuun4tmbUlFdRirCtO', true);
insert into "user" (email, name, password) values ('matti@example.com', 'Matti Meikäläinen', '$2a$12$IRm8gu.pzPZ/PW1ygJryleLNvUmiEaP7hKhgia/xbB5fDa6j1.GmO');
insert into "user" (email, name, password) values ('erkki@example.com', 'Erkki Esimerkki', '$2a$12$MPNlgEYiL8E642/aoifUI.zFjZ.tZqn6z6M9Q9d4LESLbj6/fOcs6');
insert into "user" (email, name, password) values ('tiina@example.com', 'Tiina Terävä', '$2a$12$35UNCdILjFVkrtQ6EZxQI.iP657igOG9afCWIGIFiA2yX4vw5V7n6');

insert into restriction (title, contents, arguments, approved, approver_id, user_id) values ('Eka rajoite', 'Eka kuvaus', 'Ekat perustelut', true, 1, 3);
insert into restriction (title, contents, arguments, approved, approver_id, user_id) values ('Toka rajoite', 'Toka kuvaus', 'Toka perustelut', true, 2, 4);
insert into restriction (title, contents, arguments, approved, approver_id, user_id) values ('Kolmas rajoite', 'Kolmas kuvaus', 'Kolmas perustelut', true, 1, 5);
insert into restriction (title, contents, arguments, approved, approver_id, user_id) values ('Vahvistamaton rajoite', 'Vahvistamaton kuvaus', 'Vahvistamaton perustelut', false, null, 3);

insert into vote (restriction_id, user_id) values (1, 3);
insert into vote (restriction_id, user_id) values (1, 2);
insert into vote (restriction_id, user_id) values (1, 4);
insert into vote (restriction_id, user_id) values (2, 4);
insert into vote (restriction_id, user_id) values (2, 1);
insert into vote (restriction_id, user_id) values (3, 5);

COMMIT;
