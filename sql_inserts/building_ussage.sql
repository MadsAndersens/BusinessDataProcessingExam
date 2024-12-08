INSERT INTO building_usage (usage_code, usage_description)
VALUES
    (110, 'Main house for agricultural property'), -- Stuehus til landbrugsejendom
    (120, 'Detached single-family house'), -- Fritliggende enfamiliehus
    (121, 'Semi-detached single-family house'), -- Sammenbygget enfamiliehus
    (122, 'Detached single-family house in dense-low building area'), -- Fritliggende enfamiliehus i tæt-lav bebyggelse
    (130, '(PHASING OUT) Row house, chain house, or duplex (vertical separation between units)'), -- (UDFASES) Række-, kæde-, eller dobbelthus (lodret adskillelse mellem enhederne)
    (131, 'Row, chain, and cluster house'), -- Række-, kæde- og klyngehus
    (132, 'Duplex'), -- Dobbelthus
    (140, 'Apartment building or two-family house'), -- Etagebolig-bygning, flerfamiliehus eller to-familiehus
    (150, 'Dormitory'), -- Kollegium
    (160, 'Residential building for full-time institutions'), -- Boligbygning til døgninstitution
    (185, 'Annex connected to year-round residence'), -- Anneks i tilknytning til helårsbolig
    (190, 'Other building for year-round residence'), -- Anden bygning til helårsbeboelse
    (210, '(PHASING OUT) Building for agricultural, gardening, or raw material extraction production'), -- (UDFASES) Bygning til erhvervsmæssig produktion vedrørende landbrug, gartneri, råstofudvinding o. lign
    (211, 'Pig stable'), -- Stald til svin
    (212, 'Cattle, sheep, etc. stable'), -- Stald til kvæg, får mv.
    (213, 'Poultry stable'), -- Stald til fjerkræ
    (214, 'Mink shed'), -- Minkhal
    (215, 'Greenhouse'), -- Væksthus
    (216, 'Barn for feed, crops, etc.'), -- Lade til foder, afgrøder mv.
    (217, 'Machine house, garage, etc.'), -- Maskinhus, garage mv.
    (218, 'Barn for straw, hay, etc.'), -- Lade til halm, hø mv.
    (219, 'Other building for agriculture, etc.'), -- Anden bygning til landbrug mv.
    (220, '(PHASING OUT) Building for industrial production, crafts, etc.'), -- (UDFASES) Bygning til erhvervsmæssig produktion vedrørende industri, håndværk m.v. (fabrik, værksted o.lign.)
    (221, 'Industrial building with integrated production apparatus'), -- Bygning til industri med integreret produktionsapparat
    (222, 'Industrial building without integrated production apparatus'), -- Bygning til industri uden integreret produktionsapparat
    (223, 'Workshop'), -- Værksted
    (229, 'Other building for production'), -- Anden bygning til produktion
    (230, '(PHASING OUT) Electricity, gas, water, or heat production facility'), -- (UDFASES) El-, gas-, vand- eller varmeværk, forbrændingsanstalt m.v.
    (231, 'Building for energy production'), -- Bygning til energiproduktion
    (232, 'Building for energy distribution'), -- Bygning til energidistribution
    (233, 'Building for water supply'), -- Bygning til vandforsyning
    (234, 'Building for waste and wastewater handling'), -- Bygning til håndtering af affald og spildevand
    (239, 'Other building for energy production and supply'), -- Anden bygning til energiproduktion og forsyning
    (290, '(PHASING OUT) Other building for agriculture, industry, etc.'), -- (UDFASES) Anden bygning til landbrug, industri etc.
    (310, '(PHASING OUT) Transport and garage facilities'), -- (UDFASES) Transport- og garageanlæg (fragtmandshal, lufthavnsbygning, banegårdsbygning, parkeringshus).
    (311, 'Building for railway and bus operation'), -- Bygning til jernbane- og busdrift
    (312, 'Building for aviation'), -- Bygning til luftfart
    (313, 'Building for parking and transport facilities'), -- Bygning til parkering- og transportanlæg
    (314, 'Building for parking more than two vehicles connected to residences'), -- Bygning til parkering af flere end to køretøjer i tilknytning til boliger
    (315, 'Harbor facilities'), -- Havneanlæg
    (319, 'Other transport facility'), -- Andet transportanlæg
    (320, '(PHASING OUT) Building for office, trade, storage, including public administration'), -- (UDFASES) Bygning til kontor, handel, lager, herunder offentlig administration
    (321, 'Office building'), -- Bygning til kontor
    (322, 'Retail building'), -- Bygning til detailhandel
    (323, 'Storage building'), -- Bygning til lager
    (324, 'Shopping center'), -- Butikscenter
    (325, 'Gas station'), -- Tankstation
    (329, 'Other building for office, trade, and storage'), -- Anden bygning til kontor, handel og lager
    (330, '(PHASING OUT) Building for hotel, restaurant, laundry, hairdresser, and other services'), -- (UDFASES) Bygning til hotel, restaurant, vaskeri, frisør og anden servicevirksomhed
    (331, 'Hotel, inn, or conference center with accommodation'), -- Hotel, kro eller konferencecenter med overnatning
    (332, 'Bed & breakfast, etc.'), -- Bed & breakfast mv.
    (333, 'Restaurant, café, and conference center without accommodation'), -- Restaurant, café og konferencecenter uden overnatning
    (334, 'Private service business such as hairdresser, laundry, internet café, etc.'), -- Privat servicevirksomhed som frisør, vaskeri, netcafé mv.
    (339, 'Other building for service industry'), -- Anden bygning til serviceerhverv
    (390, '(PHASING OUT) Other building for transport, trade, etc.'), -- (UDFASES) Anden bygning til transport, handel etc
    (410, '(PHASING OUT) Building for cinema, theater, exhibition, library, museum, church, etc.'), -- (UDFASES) Bygning til biograf, teater, erhvervsmæssig udstilling, bibliotek, museum, kirke o. lign.
    (411, 'Cinema, theater, concert venue, etc.'), -- Biograf, teater, koncertsted mv.
    (412, 'Museum'), -- Museum
    (413, 'Library'), -- Bibliotek
    (414, 'Church or other building for worship by state-recognized religious communities'), -- Kirke eller anden bygning til trosudøvelse for statsanerkendte trossamfund
    (415, 'Community center'), -- Forsamlingshus
    (416, 'Amusement park'), -- Forlystelsespark
    (419, 'Other building for cultural purposes'), -- Anden bygning til kulturelle formål
    (420, '(PHASING OUT) Building for education and research'), -- (UDFASES) Bygning til undervisning og forskning (skole, gymnasium, forskningslabratorium o.lign.).
    (421, 'Elementary school'), -- Grundskole
    (422, 'University'), -- Universitet
    (429, 'Other building for education and research'), -- Anden bygning til undervisning og forskning
    (430, '(PHASING OUT) Building for hospitals, nursing homes, maternity clinics, etc.'), -- (UDFASES) Bygning til hospital, sygehjem, fødeklinik o. lign.
    (431, 'Hospital'), -- Hospital og sygehus
    (432, 'Hospice, treatment home, etc.'), -- Hospice, behandlingshjem mv.
    (433, 'Health center, doctor''s office, maternity clinic, etc.'), -- Sundhedscenter, lægehus, fødeklinik mv.
    (439, 'Other building for health purposes'), -- Anden bygning til sundhedsformål
    (440, '(PHASING OUT) Daycare building'), -- (UDFASES) Bygning til daginstitution
    (441, 'Daycare'), -- Daginstitution
    (442, 'Service function at full-time institution'), -- Servicefunktion på døgninstitution
    (443, 'Barracks'), -- Kaserne
    (444, 'Prison or detention house'), -- Fængsel, arresthus mv.
    (449, 'Other building for institutional purposes'), -- Anden bygning til institutionsformål
    (451, 'Shelter'), -- Beskyttelsesrum
    (490, '(PHASING OUT) Other institution building, including barracks, prison, etc.'), -- (UDFASES) Bygning til anden institution, herunder kaserne, fængsel o. lign.
    (510, 'Summer house'), -- Sommerhus
    (520, '(PHASING OUT) Building for holiday colony, hostel, etc., except summer house'), -- (UDFASES) Bygning til feriekoloni, vandrehjem o.lign. bortset fra sommerhus
    (521, 'Holiday center, camping center, etc.'), -- Feriecenter, center til campingplads mv.
    (522, 'Building with holiday apartments for commercial rental'), -- Bygning med ferielejligheder til erhvervsmæssig udlejning
    (523, 'Building with holiday apartments for private use'), -- Bygning med ferielejligheder til eget brug
    (529, 'Other building for holiday purposes'), -- Anden bygning til ferieformål
    (530, '(PHASING OUT) Building associated with sports activities (clubhouse, sports hall, swimming pool, etc.)'), -- (UDFASES) Bygning i forbindelse med idrætsudøvelse (klubhus, idrætshal, svømmehal o. lign.)
    (531, 'Clubhouse for leisure and sports'), -- Klubhus i forbindelse med fritid og idræt
    (532, 'Swimming pool'), -- Svømmehal
    (533, 'Sports hall'), -- Idrætshal
    (534, 'Grandstand at stadium'), -- Tribune i forbindelse med stadion
    (535, 'Building for training and housing horses'), -- Bygning til træning og opstaldning af heste
    (539, 'Other building for sports purposes'), -- Anden bygning til idrætformål
    (540, 'Allotment house'), -- Kolonihavehus
    (585, 'Annex connected to leisure or summer house'), -- Anneks i tilknytning til fritids- og sommerhus
    (590, 'Other building for leisure purposes'), -- Anden bygning til fritidsformål
    (910, 'Garage'), -- Garage
    (920, 'Carport'), -- Carport
    (930, 'Shed'), -- Udhus
    (940, 'Greenhouse'), -- Drivhus
    (950, 'Detached covering'), -- Fritliggende overdækning
    (960, 'Detached conservatory'), -- Fritliggende udestue
    (970, 'Leftover agricultural building'), -- Tiloversbleven landbrugsbygning
    (990, 'Dilapidated building'), -- Faldefærdig bygning
    (999, 'Unknown building'); -- Ukendt bygning