BEGIN TRANSACTION;

DELETE FROM "user";
DELETE FROM restriction;
DELETE FROM vote;
DELETE FROM news;

-- Test users with password 'password'
INSERT INTO "user" (email, name, verified, password, city, admin) VALUES ('aatu@example.com', 'Aatu Admin', TRUE, '$2a$12$OCm372a0jVx3aiyVFF/20ebBPYDuiNbF68trrjXnS.JCdeRaeMkNq', 'Kittilä', TRUE);
INSERT INTO "user" (email, name, verified, password, city, admin) VALUES ('yrjo@example.com', 'Yrjö Ylläpitäjä', TRUE, '$2a$12$SWAvjbRh7R1Zj/vupR1xouP.Vand9t7UhqQjuun4tmbUlFdRirCtO', 'Pori', TRUE);
INSERT INTO "user" (email, name, verified, password, city) VALUES ('matti@example.com', 'Matti Meikäläinen', TRUE, '$2a$12$IRm8gu.pzPZ/PW1ygJryleLNvUmiEaP7hKhgia/xbB5fDa6j1.GmO', 'Espoo');
INSERT INTO "user" (email, verified, password) VALUES ('erkki@example.com', TRUE, '$2a$12$MPNlgEYiL8E642/aoifUI.zFjZ.tZqn6z6M9Q9d4LESLbj6/fOcs6');
INSERT INTO "user" (email, verified, password, city) VALUES ('tiina@example.com', TRUE, '$2a$12$35UNCdILjFVkrtQ6EZxQI.iP657igOG9afCWIGIFiA2yX4vw5V7n6', 'Lempäälä');
INSERT INTO "user" (email, name, verified, password) VALUES ('ville@example.com', 'Ville Virtanen', TRUE, '$2a$12$PQ./SqmlDBN82Zk5.LjgyORD1Au4TVh3AE93YBH0IagQRJaQpmbcK');
INSERT INTO "user" (email, verified, password) VALUES ('teppo@example.com', FALSE, '$2a$12$S..1SMTuQnjgXEEu8gWqN.4hwlaLsEVqaxXPIfW/8oZNkknzdtVvK');

INSERT INTO restriction (title, body, state, approver_id, user_id, user_name, user_city, created) VALUES ('Kännykkään puhuminen julkisissa kulkuvälineissä', 'Rajoitteen kuvaus ja perustelut.', 'APPROVED', 1, 3, 'Matti Meikäläinen', 'Espoo', NOW() - INTERVAL '6 days');
INSERT INTO restriction (title, body, state, approver_id, user_id, user_name, user_city, created) VALUES ('Asioiden kieltäminen', 'Rajoitteen kuvaus ja perustelut.', 'APPROVED', 2, 4, 'Erkki Esimerkki', 'Viitasaari', NOW() - INTERVAL '1 day');
INSERT INTO restriction (title, body, state, approver_id, user_id, user_name, user_city, created) VALUES ('Aamuun asti valvominen', 'Rajoitteen kuvaus ja perustelut.', 'APPROVED', 1, 5, 'Tiina Terävä', 'Sipoo', NOW() - INTERVAL '121 days');
INSERT INTO restriction (title, body, state, approver_id, user_id, user_name, user_city, created) VALUES ('Alasti uiminen', 'Rajoitteen kuvaus ja perustelut.', 'NEW', NULL, 3, 'Matti Meikäläinen', 'Espoo', NOW() - INTERVAL '15 days');
INSERT INTO restriction (title, body, state, approver_id, user_id, user_name, user_city, created) VALUES ('Yksin autoilu', 'Rajoitteen kuvaus ja perustelut.', 'NEW', NULL, 5, 'Tiina Terävä', 'Sipoo', NOW() - INTERVAL '95 days');
INSERT INTO restriction (title, body, state, approver_id, user_id, user_name, user_city, created) VALUES ('Sorsien ruokinta', 'Rajoitteen kuvaus ja perustelut.', 'APPROVED', 1, 6, 'Ville Virtanen', 'Turku', NOW() - INTERVAL '7 hours');
INSERT INTO restriction (title, body, state, approver_id, user_id, user_name, user_city, created) VALUES ('Äänekäs hengittäminen', 'Rajoitteen kuvaus ja perustelut.', 'APPROVED', 2, 1, 'Aatu Admin', 'Kittilä', NOW() - INTERVAL '5 minutes');
INSERT INTO restriction (title, body, state, approver_id, user_id, user_name, user_city, created) VALUES ('Laiton toiminta', 'Rajoitteen kuvaus ja perustelut.', 'REJECTED', 1, 5, 'Tiina Terävä', 'Sipoo', NOW() - INTERVAL '96 days');

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

INSERT INTO news (title, body, user_id) VALUES ('Kansalaisrajoite.fi-verkkopalvelu avataan 11. toukokuuta', 'Verkkopalvelu kansalaisrajoitteiden tekemiseksi ja rajoitteiden kannatuksen keräämiseksi avataan kansalaisten käyttöön sunnuntaina 11. toukokuuta. Palvelu toimii osoitteessa www.kansalaisrajoite.fi. Se tarjoaa kansalaisille mahdollisuuden saada rajoitteensa kannatettavaksi.

Verkkopalvelu on kansalaisille ilmainen. Palvelun ylläpito tarkastaa, että jätetyissä rajoitteissa on tarvittavat tiedot ja ettei aloite sisällä verkossa julkaistavaksi sopimatonta materiaalia. Tämän jälkeen rajoitteelle voi kerätä kannatusta.

Palvelu vaatii rajoitteiden luojilta ja kannattajilta rekisteröitymisen. Rajoite voi koskea mitä tahansa kansalaisen elämän osa-aluetta. Vähintään 101 kansalaisella on oikeus saada rajoite täysin kannatetuksi. Kannatuksen keräämiselle ei ole määräaikaa.

Palveluun liittyviin kysymyksiin vastataan sähköpostitse sekä sosiaalisessa mediassa, Facebookissa.

<a href="http://www.kansalaisrajoite.fi">http://www.kansalaisrajoite.fi</a> 

<a href="https://www.facebook.com/kansalaisrajoite">https://www.facebook.com/kansalaisrajoite</a>', 1);

COMMIT;
