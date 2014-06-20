create table comment (
  id SERIAL,
  restriction_id SERIAL REFERENCES "restriction"(id) on delete cascade on update cascade,
  user_id INTEGER REFERENCES "user"(id) ON DELETE cascade ON UPDATE CASCADE,
  created TIMESTAMP NOT NULL DEFAULT(NOW()),
  comment text not null,
  primary key (id)
)