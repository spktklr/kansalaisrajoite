BEGIN TRANSACTION;

DELETE FROM "user";
DELETE FROM restriction;
DELETE FROM vote;
DELETE FROM news;

INSERT INTO "user" (email, name, password, city, admin) VALUES ('aatu@example.com', 'Aatu Admin', '$2a$12$OCm372a0jVx3aiyVFF/20ebBPYDuiNbF68trrjXnS.JCdeRaeMkNq', 'Kittilä', true);
INSERT INTO "user" (email, name, password, city, admin) VALUES ('yrjo@example.com', 'Yrjö Ylläpitäjä', '$2a$12$SWAvjbRh7R1Zj/vupR1xouP.Vand9t7UhqQjuun4tmbUlFdRirCtO', 'Pori', true);
INSERT INTO "user" (email, name, password, city) VALUES ('matti@example.com', 'Matti Meikäläinen', '$2a$12$IRm8gu.pzPZ/PW1ygJryleLNvUmiEaP7hKhgia/xbB5fDa6j1.GmO', 'Espoo');
INSERT INTO "user" (email, password) VALUES ('erkki@example.com', '$2a$12$MPNlgEYiL8E642/aoifUI.zFjZ.tZqn6z6M9Q9d4LESLbj6/fOcs6');
INSERT INTO "user" (email, password, city) VALUES ('tiina@example.com', '$2a$12$35UNCdILjFVkrtQ6EZxQI.iP657igOG9afCWIGIFiA2yX4vw5V7n6', 'Lempäälä');
INSERT INTO "user" (email, name, password) VALUES ('ville@example.com', 'Ville Virtanen', '$2a$12$PQ./SqmlDBN82Zk5.LjgyORD1Au4TVh3AE93YBH0IagQRJaQpmbcK');

INSERT INTO restriction (title, body, approved, approver_id, user_id, created) VALUES ('Kännykkään puhuminen julkisissa kulkuvälineissä', 'Rajoitteen kuvaus ja perustelut.', true, 1, 3, NOW() - INTERVAL '6 days');
INSERT INTO restriction (title, body, approved, approver_id, user_id, created) VALUES ('Asioiden kieltäminen', 'Rajoitteen kuvaus ja perustelut.', true, 2, 4, NOW() - INTERVAL '1 day');
INSERT INTO restriction (title, body, approved, approver_id, user_id, created) VALUES ('Aamuun asti valvominen', 'Rajoitteen kuvaus ja perustelut.', true, 1, 5, NOW() - INTERVAL '121 days');
INSERT INTO restriction (title, body, approved, approver_id, user_id, created) VALUES ('Alasti uiminen', 'Rajoitteen kuvaus ja perustelut.', false, null, 3, NOW() - INTERVAL '15 days');
INSERT INTO restriction (title, body, approved, approver_id, user_id, created) VALUES ('Yksin autoilu', 'Rajoitteen kuvaus ja perustelut.', false, null, 5, NOW() - INTERVAL '95 days');
INSERT INTO restriction (title, body, approved, approver_id, user_id, created) VALUES ('Sorsien ruokinta', 'Rajoitteen kuvaus ja perustelut.', true, 1, 6, NOW() - INTERVAL '7 hours');
INSERT INTO restriction (title, body, approved, approver_id, user_id, created) VALUES ('Äänekäs hengittäminen', 'Rajoitteen kuvaus ja perustelut.', true, 2, 1, NOW() - INTERVAL '5 minutes');

INSERT INTO vote (restriction_id, user_id) VALUES (1, 3);
INSERT INTO vote (restriction_id, user_id) VALUES (1, 2);
INSERT INTO vote (restriction_id, user_id) VALUES (1, 4);
INSERT INTO vote (restriction_id, user_id) VALUES (2, 4);
INSERT INTO vote (restriction_id, user_id) VALUES (2, 1);
INSERT INTO vote (restriction_id, user_id) VALUES (3, 5);
INSERT INTO vote (restriction_id, user_id) VALUES (6, 1);
INSERT INTO vote (restriction_id, user_id) VALUES (6, 2);
INSERT INTO vote (restriction_id, user_id) VALUES (6, 3);
INSERT INTO vote (restriction_id, user_id) VALUES (6, 4);
INSERT INTO vote (restriction_id, user_id) VALUES (6, 5);

INSERT INTO news (title, body, user_id) VALUES ('Eka tiedote', 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.', 1);
INSERT INTO news (title, body, user_id) VALUES ('Toka tiedote', 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.', 2);

COMMIT;
