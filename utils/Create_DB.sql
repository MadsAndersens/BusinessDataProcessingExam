CREATE TABLE roof_material (
  roof_material_id int PRIMARY KEY NOT NULL,
  roof_material_name varchar
);

CREATE TABLE outer_wall_material (
  outer_wall_material_id int PRIMARY KEY NOT NULL,
  outer_wall_material_name varchar
);

CREATE TABLE heating_source (
  heating_source_id int PRIMARY KEY NOT NULL,
  heatning_source_name varchar
);

CREATE TABLE municipality (
  municipality_id varchar PRIMARY KEY NOT NULL,
  muncipality_name varchar
);

CREATE TABLE water_supply (
  water_supply_id int PRIMARY KEY NOT NULL,
  water_supply_name varchar
);

CREATE TABLE drainage (
  drainage_id int PRIMARY KEY NOT NULL,
  drainage_name varchar
);

CREATE TABLE postal_area (
  postal_code int PRIMARY KEY NOT NULL,
  postal_name varchar
);

CREATE TABLE road_name (
  road_name_id SERIAL PRIMARY KEY NOT NULL,
  road_name varchar
);

CREATE TABLE school (
  school_id int PRIMARY KEY NOT NULL,
  school_name varchar,
  school_gpa float,
  lattitude float,
  longitude float
);

CREATE TABLE metro (
  metro_id int PRIMARY KEY NOT NULL,
  metro_name varchar,
  lattitude float,
  longitude float
);

CREATE TABLE s_train (
  s_train_id int PRIMARY KEY NOT NULL,
  s_train_name varchar,
  lattitude float,
  longitude float
);

CREATE TABLE bus (
  bus_id int PRIMARY KEY NOT NULL,
  bus_name varchar,
  lattitude float,
  longitude float
);

CREATE TABLE tram (
  tram_id int PRIMARY KEY NOT NULL,
  tram_name varchar,
  lattitude float,
  longitude float
);

CREATE TABLE building_ussage (
  ussage_code int PRIMARY KEY NOT NULL
  ussage_description varchar
)

CREATE TABLE Buildings (
  building_id varchar PRIMARY KEY NOT NULL,
  construction_year int,
  ussage_code int,
  collected_area int,
  industry_area int,
  housing_area int,
  foot_print_area int,
  outer_wall_material_id int,
  roof_material_id int,
  water_supply_id int,
  drainage_id int,
  floors int,
  heating_source_id int,
  alternate_heating_source_id int,
  carport int,
  plot_id varchar,
  municipality_id varchar,
  longitude float,
  lattitude float,
  asbestos_code int,
  house_number varchar,
  road_name_id int,
  postal_code int,
  school_id int,
  school_distance float,
  metro_id int,
  metro_distance float,
  s_train_id int,
  s_train_distance float,
  bus_id int,
  bus_distance float,
  tram_id int,
  tram_distance float,
  FOREIGN KEY (roof_material_id) REFERENCES roof_material (roof_material_id),
  FOREIGN KEY (outer_wall_material_id) REFERENCES outer_wall_material (outer_wall_material_id),
  FOREIGN KEY (heating_source_id) REFERENCES heating_source (heating_source_id),
  FOREIGN KEY (municipality_id) REFERENCES municipality (municipality_id),
  FOREIGN KEY (water_supply_id) REFERENCES water_supply (water_supply_id),
  FOREIGN KEY (drainage_id) REFERENCES drainage (drainage_id),
  FOREIGN KEY (postal_code) REFERENCES postal_area (postal_code),
  FOREIGN KEY (road_name_id) REFERENCES road_name (road_name_id),
  FOREIGN KEY (school_id) REFERENCES school (school_id),
  FOREIGN KEY (metro_id) REFERENCES metro (metro_id),
  FOREIGN KEY (s_train_id) REFERENCES s_train (s_train_id),
  FOREIGN KEY (tram_id) REFERENCES tram (tram_id),
  FOREIGN KEY (bus_id) REFERENCES bus (bus_id)
  FOREIGN KEY (ussage_code) REFERENCES building_ussage (ussage_code)
);