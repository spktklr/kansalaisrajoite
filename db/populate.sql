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

insert into news (title, body, user_id) values ('Eka tiedote', 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.', 1);
insert into news (title, body, user_id) values ('Toka tiedote', 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.', 2);

COMMIT;
