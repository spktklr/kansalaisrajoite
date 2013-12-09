BEGIN TRANSACTION;

delete from "user";
delete from restriction;
delete from vote;
delete from news;

insert into "user" (email, name, password, city, admin) values ('aatu@example.com', 'Aatu Admin', '$2a$12$OCm372a0jVx3aiyVFF/20ebBPYDuiNbF68trrjXnS.JCdeRaeMkNq', 'Kittilä', true);
insert into "user" (email, name, password, city, admin) values ('yrjo@example.com', 'Yrjö Ylläpitäjä', '$2a$12$SWAvjbRh7R1Zj/vupR1xouP.Vand9t7UhqQjuun4tmbUlFdRirCtO', 'Pori', true);
insert into "user" (email, name, password, city) values ('matti@example.com', 'Matti Meikäläinen', '$2a$12$IRm8gu.pzPZ/PW1ygJryleLNvUmiEaP7hKhgia/xbB5fDa6j1.GmO', 'Espoo');
insert into "user" (email, password) values ('erkki@example.com', '$2a$12$MPNlgEYiL8E642/aoifUI.zFjZ.tZqn6z6M9Q9d4LESLbj6/fOcs6');
insert into "user" (email, password, city) values ('tiina@example.com', '$2a$12$35UNCdILjFVkrtQ6EZxQI.iP657igOG9afCWIGIFiA2yX4vw5V7n6', 'Lempäälä');
insert into "user" (email, name, password) values ('ville@example.com', 'Ville Virtanen', '$2a$12$PQ./SqmlDBN82Zk5.LjgyORD1Au4TVh3AE93YBH0IagQRJaQpmbcK');

insert into restriction (title, contents, arguments, approved, approver_id, user_id, created) values ('Kännykkään puhuminen julkisissa kulkuvälineissä', 'Rajoitteen kuvaus.', 'Rajoitteen perustelut.', true, 1, 3, NOW() - INTERVAL '6 days');
insert into restriction (title, contents, arguments, approved, approver_id, user_id, created) values ('Asioiden kieltäminen', 'Rajoitteen kuvaus.', 'Rajoitteen perustelut.', true, 2, 4, NOW() - INTERVAL '1 day');
insert into restriction (title, contents, arguments, approved, approver_id, user_id, created) values ('Aamuun asti valvominen', 'Rajoitteen kuvaus.', 'Rajoitteen perustelut.', true, 1, 5, NOW() - INTERVAL '121 days');
insert into restriction (title, contents, arguments, approved, approver_id, user_id, created) values ('Alasti uiminen', 'Rajoitteen kuvaus.', 'Rajoitteen perustelut.', false, null, 3, NOW() - INTERVAL '15 days');
insert into restriction (title, contents, arguments, approved, approver_id, user_id, created) values ('Yksin autoilu', 'Rajoitteen kuvaus.', 'Rajoitteen perustelut.', false, null, 5, NOW() - INTERVAL '95 days');
insert into restriction (title, contents, arguments, approved, approver_id, user_id, created) values ('Sorsien ruokinta', 'Rajoitteen kuvaus.', 'Rajoitteen perustelut.', true, 1, 6, NOW() - INTERVAL '7 hours');
insert into restriction (title, contents, arguments, approved, approver_id, user_id, created) values ('Äänekäs hengittäminen', 'Rajoitteen kuvaus.', 'Rajoitteen perustelut.', true, 2, 1, NOW() - INTERVAL '5 minutes');

insert into vote (restriction_id, user_id) values (1, 3);
insert into vote (restriction_id, user_id) values (1, 2);
insert into vote (restriction_id, user_id) values (1, 4);
insert into vote (restriction_id, user_id) values (2, 4);
insert into vote (restriction_id, user_id) values (2, 1);
insert into vote (restriction_id, user_id) values (3, 5);
insert into vote (restriction_id, user_id) values (6, 1);
insert into vote (restriction_id, user_id) values (6, 2);
insert into vote (restriction_id, user_id) values (6, 3);
insert into vote (restriction_id, user_id) values (6, 4);
insert into vote (restriction_id, user_id) values (6, 5);

insert into news (title, body, user_id) values ('Eka tiedote', 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.', 1);
insert into news (title, body, user_id) values ('Toka tiedote', 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.', 2);

COMMIT;
