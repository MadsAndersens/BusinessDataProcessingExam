INSERT INTO drainage (drainage_id, drainage_name)
VALUES
    (1, 'Combined sewer: wastewater + rain and surface water'), -- Fælleskloakeret: spildevand + tag- og overfladevand
    (10, 'Discharge to public sewer system'), -- Afløb til offentligt kloaksystem
    (101, 'SOP: Mini-treatment plant with direct discharge'), -- SOP: Minirenseanlæg med direkte udledning
    (102, 'SOP: Mini-treatment plant with discharge to field drain'), -- SOP: Minirenseanlæg med udledning til markdræn
    (103, 'SOP: Mini-treatment plant with infiltration in soakaway'), -- SOP: Minirenseanlæg med nedsivning i faskine
    (104, 'SOP: Infiltration to soakaway'), -- SOP: Nedsivning til sivedræn
    (105, 'SOP: Septic tank'), -- SOP: Samletank
    (106, 'SOP: Willow plant with infiltration (no membrane)'), -- SOP: Pileanlæg med nedsivning (uden membran)
    (107, 'SOP: Willow plant without discharge (with membrane)'), -- SOP: Pileanlæg uden udledning (med membran)
    (108, 'SOP: Vegetated filter system with infiltration in soakaway'), -- SOP: Beplantede filteranlæg med nedsivning i faskine
    (109, 'SOP: Sand filter with P-precipitation in sedimentation tank and direct discharge'), -- SOP: Sandfiltre med P-fældning i bundfældningstanken og direkte udledning
    (11, 'Discharge to shared private sewer system'), -- Afløb til fællesprivat kloaksystem
    (110, 'SOP: Sand filter with P-precipitation in sedimentation tank and discharge to field drain'), -- SOP: Sandfiltre med P-fældning i bundfældningstanken og udledning til markdræn
    (12, 'Discharge to shared private sewer system connected to wastewater utility system'), -- Afløb til fællesprivat kloaksystem med tilslutning til spildevandsforsyningens kloaksystem
    (190, 'SOP: Other'), -- SOP: Andet
    (2, 'Combined sewer: wastewater + partial rain and surface water'), -- Fælleskloakeret: spildevand + delvis tag- og overfladevand
    (20, 'Discharge to septic tank'), -- Afløb til samletank
    (201, 'SO: Biological sand filter with direct discharge'), -- SO: Biologisk sandfilter med direkte udledning
    (202, 'SO: Biological sand filter with discharge to field drain'), -- SO: Biologisk sandfilter med udledning til markdræn
    (203, 'SO: Mini-treatment plant with direct discharge'), -- SO: Minirenseanlæg med direkte udledning
    (204, 'SO: Mini-treatment plant with discharge to field drain'), -- SO: Minirenseanlæg med udledning til markdræn
    (205, 'SO: Vegetated filter system with direct discharge'), -- SO: Beplantede filteranlæg med direkte udledning
    (206, 'SO: Vegetated filter system with discharge to field drain'), -- SO: Beplantede filteranlæg med udledning til markdræn
    (21, 'Discharge to septic tank for toilet wastewater and mechanical treatment of other wastewater'), -- Afløb til samletank for toiletvand og mekanisk rensning af øvrigt spildevand
    (29, 'Mechanical treatment with infiltration system with permission'), -- Mekanisk rensning med nedsivningsanlæg med tilladelse
    (290, 'SO: Other'), -- SO: Andet
    (3, 'Combined sewer: wastewater'), -- Fælleskloakeret: spildevand
    (30, 'Mechanical treatment with infiltration system (permission not required)'), -- Mekanisk rensning med nedsivningsanlæg (tilladelse ikke påkrævet)
    (301, 'OP: Mini-treatment plant with direct discharge'), -- OP: Minirenseanlæg med direkte udledning
    (302, 'OP: Mini-treatment plant with discharge to field drain'), -- OP: Minirenseanlæg med udledning til markdræn
    (31, 'Mechanical treatment with private discharge directly to streams, lakes, or sea'), -- Mekanisk rensning med privat udledning direkte til vandløb, søer eller havet
    (32, 'Mechanical and biological treatment (older systems without treatment classification)'), -- Mekanisk og biologisk rensning (ældre anlæg uden renseklasse)
    (390, 'OP: Other'), -- OP: Andet
    (4, 'Combined sewer: rain and surface water'), -- Fælleskloakeret: tag- og overfladevand
    (401, 'O: Root zone system with direct discharge'), -- O: Rodzoneanlæg med direkte udledning
    (402, 'O: Root zone system with discharge to field drain'), -- O: Rodzoneanlæg med udledning til markdræn
    (403, 'O: Mini-treatment plant with direct discharge'), -- O: Minirenseanlæg med direkte udledning
    (404, 'O: Mini-treatment plant with discharge to field drain'), -- O: Minirenseanlæg med udledning til markdræn
    (490, 'O: Other'), -- O: Andet
    (5, 'Separate sewer: wastewater + rain and surface water'), -- Separatkloakeret: spildevand + tag- og overfladevand
    (501, 'Other treatment solutions: Mechanical with direct discharge'), -- Øvrige renseløsninger: Mekanisk med direkte udledning
    (502, 'Other treatment solutions: Mechanical with discharge to field drain'), -- Øvrige renseløsninger: Mekanisk med udledning til markdræn
    (503, 'Other treatment solutions: Older infiltration systems with infiltration to soakaway'), -- Øvrige renseløsninger: Ældre nedsivningsanlæg med nedsivning til sivebrønd
    (504, 'Discharge to soil surface'), -- Udledning til jordoverfladen
    (505, 'Discharge untreated'), -- Udledning urenset
    (590, 'Other treatment solutions: Other'), -- Øvrige renseløsninger: Andet
    (6, 'Separate sewer: wastewater + partial rain and surface water'), -- Separatkloakeret: spildevand + delvis tag- og overfladevand
    (601, 'Other type of drainage (greater than 30 PE with own discharge)'), -- Anden type afløb (større end 30 PE med egen udledning)
    (7, 'Separate sewer: wastewater'), -- Separatkloakeret: spildevand
    (70, 'Discharge without treatment directly to streams, lakes, or sea'), -- Udledning uden rensning direkte til vandløb, søer eller havet
    (701, 'No drainage'), -- Intet afløb
    (75, 'Mixed drainage conditions on the property (specified on the building)'), -- Blandet afløbsforhold på ejendommen (er specificeret på bygningen)
    (8, 'Separate sewer: rain and surface water'), -- Separatkloakeret: tag- og overfladevand
    (80, 'Other type of drainage'), -- Anden type afløb
    (9, 'Sewage drained: Wastewater'), -- Spildevandskloakeret: Spildevand
    (90, 'No discharge'); -- Ingen udledning