BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "stage" (
	"id"	INTEGER NOT NULL,
	"eleve_id"	INTEGER,
	"niveau_id"	INTEGER,
	"entreprise_id"	INTEGER,
	"contact_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("contact_id") REFERENCES "contact"("id"),
	FOREIGN KEY("eleve_id") REFERENCES "eleve"("id"),
	FOREIGN KEY("entreprise_id") REFERENCES "entreprise"("id"),
	FOREIGN KEY("niveau_id") REFERENCES "niveau"("id")
);
CREATE TABLE IF NOT EXISTS "prof_class" (
	"classe_id"	INTEGER,
	"prof_id"	INTEGER,
	FOREIGN KEY("classe_id") REFERENCES "classe"("id"),
	FOREIGN KEY("prof_id") REFERENCES "professeur"("id")
);
CREATE TABLE IF NOT EXISTS "eleve" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	"firstname"	VARCHAR(64),
	"promotion"	VARCHAR(40),
	"phonenumber"	VARCHAR(10),
	"mail1"	VARCHAR(64),
	"mail2"	VARCHAR(64),
	"active"	BOOLEAN,
	"niveau_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("niveau_id") REFERENCES "niveau"("id")
);
CREATE TABLE IF NOT EXISTS "contact" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	"firstname"	VARCHAR(64),
	"fonction"	VARCHAR(40),
	"active"	BOOLEAN,
	"phonenumber1"	VARCHAR(10),
	"phonenumber2"	VARCHAR(10),
	"mail"	VARCHAR(64),
	"entreprise_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("entreprise_id") REFERENCES "entreprise"("id")
);
CREATE TABLE IF NOT EXISTS "promotion" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	"annee_deb"	INTEGER,
	"annee_fin"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "professeur" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	"firstname"	VARCHAR(64),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "niveau" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "groupe" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "entreprise" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	"adresse1"	VARCHAR(64),
	"adresse2"	VARCHAR(64),
	"CP"	VARCHAR(5),
	"ville"	VARCHAR(20),
	"active"	BOOLEAN,
	"phonenumber"	VARCHAR(10),
	"mail"	VARCHAR(64),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "date" (
	"id"	INTEGER NOT NULL,
	"annee_scolaire"	VARCHAR(64),
	"date_deb1"	DATETIME,
	"date_fin1"	DATETIME,
	"date_deb2"	DATETIME,
	"date_fin2"	DATETIME,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "classe" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num"	VARCHAR(32) NOT NULL,
	CONSTRAINT "alembic_version_pkc" PRIMARY KEY("version_num")
);
INSERT INTO "eleve" VALUES (1,'DUPONT','Bob','2022-2023','605040302','bob.dupont@stfelixlasalle.fr',NULL,'True',1);
INSERT INTO "contact" VALUES (1,'DROUIN','Bob','DSI',1,'','','',3);
INSERT INTO "contact" VALUES (2,'FERNAND','Léa','DRH',1,'','','',2);
INSERT INTO "contact" VALUES (3,'HECTON','Jim','Responsable SI',1,'','','',1);
INSERT INTO "promotion" VALUES (1,'2021-2023',2021,2023);
INSERT INTO "promotion" VALUES (2,'2022-2024',2022,2024);
INSERT INTO "niveau" VALUES (1,'2SN');
INSERT INTO "niveau" VALUES (2,'1SN');
INSERT INTO "niveau" VALUES (3,'TSN');
INSERT INTO "entreprise" VALUES (1,'Zebra','12 rue de la poste','','44000','NANTES',1,'0606060606','');
INSERT INTO "entreprise" VALUES (2,'Vertigo','30 rue de la mer','','85270','ST HILAIRE DE RIEZ',1,'0605040302','');
INSERT INTO "entreprise" VALUES (3,'Bernstein&co','45 rue de la paix','','85300','CHALLANS',1,'0605060506','');
INSERT INTO "date" VALUES (2,'2022-2023','2022-11-30 00:00:00.000000','2022-12-16 00:00:00.000000','2023-01-02 00:00:00.000000','2023-01-20 00:00:00.000000');
INSERT INTO "date" VALUES (3,'2022-2023','2022-11-14 00:00:00.000000','2022-11-25 00:00:00.000000','2023-01-01 00:00:00.000000','2022-11-18 00:00:00.000000');
INSERT INTO "date" VALUES (4,'2021-2022','2022-11-15 00:00:00.000000','2022-11-29 00:00:00.000000','2022-12-14 00:00:00.000000','2023-01-27 00:00:00.000000');
INSERT INTO "alembic_version" VALUES ('e2f84acea161');
CREATE INDEX IF NOT EXISTS "ix_eleve_promotion" ON "eleve" (
	"promotion"
);
CREATE INDEX IF NOT EXISTS "ix_eleve_phonenumber" ON "eleve" (
	"phonenumber"
);
CREATE INDEX IF NOT EXISTS "ix_eleve_name" ON "eleve" (
	"name"
);
CREATE INDEX IF NOT EXISTS "ix_eleve_mail2" ON "eleve" (
	"mail2"
);
CREATE INDEX IF NOT EXISTS "ix_eleve_mail1" ON "eleve" (
	"mail1"
);
CREATE INDEX IF NOT EXISTS "ix_eleve_firstname" ON "eleve" (
	"firstname"
);
CREATE INDEX IF NOT EXISTS "ix_eleve_active" ON "eleve" (
	"active"
);
CREATE INDEX IF NOT EXISTS "ix_contact_phonenumber2" ON "contact" (
	"phonenumber2"
);
CREATE INDEX IF NOT EXISTS "ix_contact_phonenumber1" ON "contact" (
	"phonenumber1"
);
CREATE INDEX IF NOT EXISTS "ix_contact_name" ON "contact" (
	"name"
);
CREATE INDEX IF NOT EXISTS "ix_contact_mail" ON "contact" (
	"mail"
);
CREATE INDEX IF NOT EXISTS "ix_contact_fonction" ON "contact" (
	"fonction"
);
CREATE INDEX IF NOT EXISTS "ix_contact_firstname" ON "contact" (
	"firstname"
);
CREATE INDEX IF NOT EXISTS "ix_contact_active" ON "contact" (
	"active"
);
CREATE INDEX IF NOT EXISTS "ix_promotion_name" ON "promotion" (
	"name"
);
CREATE INDEX IF NOT EXISTS "ix_niveau_name" ON "niveau" (
	"name"
);
CREATE INDEX IF NOT EXISTS "ix_groupe_name" ON "groupe" (
	"name"
);
CREATE INDEX IF NOT EXISTS "ix_entreprise_ville" ON "entreprise" (
	"ville"
);
CREATE INDEX IF NOT EXISTS "ix_entreprise_phonenumber" ON "entreprise" (
	"phonenumber"
);
CREATE INDEX IF NOT EXISTS "ix_entreprise_name" ON "entreprise" (
	"name"
);
CREATE INDEX IF NOT EXISTS "ix_entreprise_mail" ON "entreprise" (
	"mail"
);
CREATE INDEX IF NOT EXISTS "ix_entreprise_adresse2" ON "entreprise" (
	"adresse2"
);
CREATE INDEX IF NOT EXISTS "ix_entreprise_adresse1" ON "entreprise" (
	"adresse1"
);
CREATE INDEX IF NOT EXISTS "ix_entreprise_active" ON "entreprise" (
	"active"
);
CREATE INDEX IF NOT EXISTS "ix_entreprise_CP" ON "entreprise" (
	"CP"
);
CREATE INDEX IF NOT EXISTS "ix_date_annee_scolaire" ON "date" (
	"annee_scolaire"
);
CREATE INDEX IF NOT EXISTS "ix_classe_name" ON "classe" (
	"name"
);
COMMIT;
