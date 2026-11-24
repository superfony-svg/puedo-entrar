// Textos de la portada en varios idiomas. Las normas de cada ciudad (datos de la DGT y ayuntamientos) se quedan en español.
const IDIOMAS = {
  es: "Español", ca: "Català / Valencià", eu: "Euskara", gl: "Galego", oc: "Aranés", en: "English", fr: "Français",
  de: "Deutsch", pl: "Polski", pt: "Português", it: "Italiano", ro: "Română", ar: "العربية"
};
const TXT = {
es: {nav_home:"Inicio",nav_cities:"Ciudades",nav_open:"Ciudades abiertas",nav_guides:"Guías",nav_faq:"Preguntas",nav_legal:"Aviso legal",
h1:"¿Puedo entrar con mi coche?",sub:"Escribe tu matrícula y te decimos tu etiqueta de la DGT y en qué zonas de bajas emisiones de España puedes entrar.",install:"Instalar como app en el móvil",
h_plate:"Tu matrícula",check:"Comprobar",nostore:"No guardamos las matrículas que escribes.",exc_legend:"¿Tienes alguna excepción? (la DGT no la indica en su fichero)",hist:"Mi vehículo es histórico",pmr:"Tengo tarjeta de estacionamiento para personas con movilidad reducida",
res_label:"Opcional: ¿en qué municipio paga tu coche el impuesto de circulación? Algunas ciudades dejan entrar a los coches de sus vecinos.",res_none:"No lo sé o prefiero no decirlo",choose_label:"Prefiero elegir mi etiqueta",share:"Compartir por WhatsApp",
h_map:"Mapa de las zonas",choose_city:"Elige una ciudad",where0:"Pulsa el botón para ver si estás dentro de una zona.",locate:"¿Dónde estoy?",
h_route:"Planifica tu viaje",route_help:"Escribe de dónde sales y a dónde vas. Te decimos qué zonas de bajas emisiones atraviesa la ruta en coche y si puedes entrar con tu etiqueta.",orig_ph:"Origen: calle, ciudad o pueblo",dest_ph:"Destino: calle, ciudad o pueblo",route_btn:"Ver la ruta",route_note:"La ruta es orientativa (calculada con OpenStreetMap y OSRM): tu navegador puede llevarte por otro camino. Para buscarla, el origen y el destino se envían a esos servicios.",
h_cities:"Zonas de bajas emisiones por ciudad",h_guides:"Guías",lang_note:"",
l0:"Cero emisiones",lE:"ECO",lC:"C (verde)",lB:"B (amarilla)",lN:"Sin etiqueta",label_x:"Etiqueta {x}",chosen:"Elegida por ti",plate_src:"Matrícula {p} según la DGT",
v_ok:"Puedes entrar",v_no:"No puedes entrar",v_warn:"Sí, salvo aviso de contaminación",v_unk:"Datos poco claros: consulta",v_pend:"Sin datos aún: consulta al ayuntamiento",v_exc:"Puede que tengas excepción: compruébalo",unverified:" · dato sin verificar",
summary:"Según los datos publicados, puedes entrar siempre en {ok} de {n} ciudades con zona de bajas emisiones",watch:"Ojo en estas:",all:"Ver todas las ciudades",disclaimer:"Información orientativa y no oficial. Las normas cambian y cada ayuntamiento tiene la última palabra: antes de entrar, confírmalo en su web. ",legal:"Aviso legal",
bad_t:"Matrícula incompleta",bad_s:"Escríbela entera, por ejemplo 1234BCD o M1234AB.",notfound_t:"No encontramos {p}",notfound_s:"No aparece en el fichero de la DGT. Revisa que esté bien escrita o consúltala en la sede de la DGT.",
dest_city:"¿A dónde vas? (opcional) Ej.: Granada",dest_nf:"No tenemos esa ciudad. Elige una de la lista o mira «Ver todas las ciudades».",dest_more:"Ver normas y mapa",others:"De otros {n} municipios obligados aún no tenemos las normas: están en «Ver todas las ciudades»."},

ca: {nav_home:"Inici",nav_cities:"Ciutats",nav_open:"Ciutats obertes",nav_guides:"Guies",nav_faq:"Preguntes",nav_legal:"Avís legal",
h1:"Puc entrar amb el meu cotxe?",sub:"Escriu la matrícula i et diem l'etiqueta de la DGT i en quines zones de baixes emissions d'Espanya pots entrar.",install:"Instal·lar com a app al mòbil",
h_plate:"La teua matrícula",check:"Comprovar",nostore:"No guardem les matrícules que escrius.",exc_legend:"Tens alguna excepció? (la DGT no ho indica al seu fitxer)",hist:"El meu vehicle és històric",pmr:"Tinc targeta d'aparcament per a persones amb mobilitat reduïda",
res_label:"Opcional: en quin municipi paga el teu cotxe l'impost de circulació? Algunes ciutats deixen entrar els cotxes dels seus veïns.",res_none:"No ho sé o prefereixo no dir-ho",choose_label:"Prefereixo triar la meua etiqueta",share:"Compartir per WhatsApp",
h_map:"Mapa de les zones",choose_city:"Tria una ciutat",where0:"Prem el botó per veure si estàs dins d'una zona.",locate:"On soc?",
h_route:"Planifica el teu viatge",route_help:"Escriu d'on surts i on vas. Et diem quines zones de baixes emissions travessa la ruta i si hi pots entrar amb la teua etiqueta.",orig_ph:"Origen: carrer, ciutat o poble",dest_ph:"Destinació: carrer, ciutat o poble",route_btn:"Veure la ruta",route_note:"La ruta és orientativa (calculada amb OpenStreetMap i OSRM): el teu navegador et pot portar per un altre camí. Per buscar-la, l'origen i la destinació s'envien a aquests serveis.",
h_cities:"Zones de baixes emissions per ciutat",h_guides:"Guies",lang_note:"Les normes de cada ciutat es mostren en castellà.",
l0:"Zero emissions",lE:"ECO",lC:"C (verda)",lB:"B (groga)",lN:"Sense etiqueta",label_x:"Etiqueta {x}",chosen:"Triada per tu",plate_src:"Matrícula {p} segons la DGT",
v_ok:"Pots entrar",v_no:"No pots entrar",v_warn:"Sí, llevat d'avís de contaminació",v_unk:"Dades poc clares: consulta",v_pend:"Encara sense dades: consulta l'ajuntament",v_exc:"Potser tens excepció: comprova-ho",unverified:" · dada sense verificar",
summary:"Segons les dades publicades, pots entrar sempre en {ok} de {n} ciutats amb zona de baixes emissions",watch:"Compte amb aquestes:",all:"Veure totes les ciutats",disclaimer:"Informació orientativa i no oficial. Les normes canvien i cada ajuntament té l'última paraula: abans d'entrar, confirma-ho al seu web. ",legal:"Avís legal",
bad_t:"Matrícula incompleta",bad_s:"Escriu-la sencera, per exemple 1234BCD o M1234AB.",notfound_t:"No trobem {p}",notfound_s:"No apareix al fitxer de la DGT. Revisa que estiga ben escrita o consulta-la a la seu de la DGT.",
dest_city:"On vas? (opcional) Ex.: Granada",dest_nf:"No tenim aquesta ciutat. Tria'n una de la llista o mira «Veure totes les ciutats».",dest_more:"Veure normes i mapa",others:"D'altres {n} municipis obligats encara no tenim les normes: són a «Veure totes les ciutats»."},

eu: {nav_home:"Hasiera",nav_cities:"Hiriak",nav_open:"Hiri irekiak",nav_guides:"Gidak",nav_faq:"Galderak",nav_legal:"Lege-oharra",
h1:"Sar naiteke nire autoarekin?",sub:"Idatzi zure matrikula eta DGTren etiketa eta Espainiako zein emisio gutxiko gunetan sar zaitezkeen esango dizugu.",install:"Instalatu aplikazio gisa mugikorrean",
h_plate:"Zure matrikula",check:"Egiaztatu",nostore:"Ez ditugu idazten dituzun matrikulak gordetzen.",exc_legend:"Salbuespenik baduzu? (DGTk ez du bere fitxategian adierazten)",hist:"Nire ibilgailua historikoa da",pmr:"Mugikortasun murriztuko pertsonentzako aparkatzeko txartela daukat",
res_label:"Aukerakoa: zein udalerritan ordaintzen du zure autoak zirkulazio-zerga? Hiri batzuek beren bizilagunen autoei sartzen uzten diete.",res_none:"Ez dakit edo nahiago dut ez esan",choose_label:"Nahiago dut nire etiketa aukeratu",share:"Partekatu WhatsApp bidez",
h_map:"Guneen mapa",choose_city:"Aukeratu hiri bat",where0:"Sakatu botoia gune baten barruan zauden ikusteko.",locate:"Non nago?",
h_route:"Planifikatu zure bidaia",route_help:"Idatzi nondik irteten zaren eta nora zoazen. Ibilbideak zein emisio gutxiko gune zeharkatzen dituen eta zure etiketarekin sar zaitezkeen esango dizugu.",orig_ph:"Jatorria: kalea, hiria edo herria",dest_ph:"Helmuga: kalea, hiria edo herria",route_btn:"Ikusi ibilbidea",route_note:"Ibilbidea gutxi gorabeherakoa da (OpenStreetMap eta OSRMrekin kalkulatua). Bilatzeko, jatorria eta helmuga zerbitzu horietara bidaltzen dira.",
h_cities:"Emisio gutxiko guneak hiriz hiri",h_guides:"Gidak",lang_note:"Hiri bakoitzeko arauak gaztelaniaz agertzen dira.",
l0:"Zero emisio",lE:"ECO",lC:"C (berdea)",lB:"B (horia)",lN:"Etiketarik gabe",label_x:"{x} etiketa",chosen:"Zuk aukeratua",plate_src:"{p} matrikula, DGTren arabera",
v_ok:"Sar zaitezke",v_no:"Ezin zara sartu",v_warn:"Bai, kutsadura-abisurik ez badago",v_unk:"Datu ez oso argiak: kontsultatu",v_pend:"Daturik ez oraindik: galdetu udalari",v_exc:"Agian salbuespena duzu: egiaztatu",unverified:" · egiaztatu gabeko datua",
summary:"Argitaratutako datuen arabera, emisio gutxiko gunea duten {n} hirietatik {ok}tan sar zaitezke beti",watch:"Kontuz hauekin:",all:"Ikusi hiri guztiak",disclaimer:"Informazio orientagarria eta ez ofiziala. Arauak aldatu egiten dira eta udal bakoitzak du azken hitza: sartu aurretik, berretsi bere webgunean. ",legal:"Lege-oharra",
bad_t:"Matrikula osatu gabe",bad_s:"Idatzi osorik, adibidez 1234BCD edo M1234AB.",notfound_t:"Ez dugu {p} aurkitu",notfound_s:"Ez da DGTren fitxategian agertzen. Egiaztatu ondo idatzita dagoela edo kontsultatu DGTren egoitzan.",
dest_city:"Nora zoaz? (aukerakoa) Adib.: Granada",dest_nf:"Ez dugu hiri hori. Aukeratu zerrendako bat edo begiratu «Ikusi hiri guztiak».",dest_more:"Arauak eta mapa ikusi",others:"Behartutako beste {n} udalerriren arauak ez ditugu oraindik: «Ikusi hiri guztiak» atalean daude."},

gl: {nav_home:"Inicio",nav_cities:"Cidades",nav_open:"Cidades abertas",nav_guides:"Guías",nav_faq:"Preguntas",nav_legal:"Aviso legal",
h1:"Podo entrar co meu coche?",sub:"Escribe a túa matrícula e dicímosche a túa etiqueta da DGT e en que zonas de baixas emisións de España podes entrar.",install:"Instalar como app no móbil",
h_plate:"A túa matrícula",check:"Comprobar",nostore:"Non gardamos as matrículas que escribes.",exc_legend:"Tes algunha excepción? (a DGT non o indica no seu ficheiro)",hist:"O meu vehículo é histórico",pmr:"Teño tarxeta de estacionamento para persoas con mobilidade reducida",
res_label:"Opcional: en que concello paga o teu coche o imposto de circulación? Algunhas cidades deixan entrar os coches da súa veciñanza.",res_none:"Non o sei ou prefiro non dicilo",choose_label:"Prefiro escoller a miña etiqueta",share:"Compartir por WhatsApp",
h_map:"Mapa das zonas",choose_city:"Escolle unha cidade",where0:"Preme o botón para ver se estás dentro dunha zona.",locate:"Onde estou?",
h_route:"Planifica a túa viaxe",route_help:"Escribe de onde saes e a onde vas. Dicímosche que zonas de baixas emisións atravesa a ruta e se podes entrar coa túa etiqueta.",orig_ph:"Orixe: rúa, cidade ou vila",dest_ph:"Destino: rúa, cidade ou vila",route_btn:"Ver a ruta",route_note:"A ruta é orientativa (calculada con OpenStreetMap e OSRM). Para buscala, a orixe e o destino envíanse a eses servizos.",
h_cities:"Zonas de baixas emisións por cidade",h_guides:"Guías",lang_note:"As normas de cada cidade móstranse en castelán.",
l0:"Cero emisións",lE:"ECO",lC:"C (verde)",lB:"B (amarela)",lN:"Sen etiqueta",label_x:"Etiqueta {x}",chosen:"Escollida por ti",plate_src:"Matrícula {p} segundo a DGT",
v_ok:"Podes entrar",v_no:"Non podes entrar",v_warn:"Si, agás aviso de contaminación",v_unk:"Datos pouco claros: consulta",v_pend:"Aínda sen datos: consulta o concello",v_exc:"Pode que teñas excepción: compróbao",unverified:" · dato sen verificar",
summary:"Segundo os datos publicados, podes entrar sempre en {ok} de {n} cidades con zona de baixas emisións",watch:"Ollo con estas:",all:"Ver todas as cidades",disclaimer:"Información orientativa e non oficial. As normas cambian e cada concello ten a última palabra: antes de entrar, confírmao na súa web. ",legal:"Aviso legal",
bad_t:"Matrícula incompleta",bad_s:"Escríbea enteira, por exemplo 1234BCD ou M1234AB.",notfound_t:"Non atopamos {p}",notfound_s:"Non aparece no ficheiro da DGT. Revisa que estea ben escrita ou consúltaa na sede da DGT.",
dest_city:"A onde vas? (opcional) Ex.: Granada",dest_nf:"Non temos esa cidade. Escolle unha da lista ou mira «Ver todas as cidades».",dest_more:"Ver normas e mapa",others:"Doutros {n} concellos obrigados aínda non temos as normas: están en «Ver todas as cidades»."},

oc: {nav_home:"Inici",nav_cities:"Ciutats",nav_open:"Ciutats dubèrtes",nav_guides:"Guides",nav_faq:"Questions",nav_legal:"Avís legau",
h1:"Pòdi entrar damb eth mèn còche?",sub:"Escriu era tua matricula e te dideram era tua etiqueta dera DGT e en quines zònes de baishes emissions d'Espanha pòts entrar.",install:"Installar coma app en mobil",
h_plate:"Era tua matricula",check:"Verificar",nostore:"Non guardam es matricules que escrius.",exc_legend:"As quauque excepcion? (era DGT non l'indica en sòn fichèr)",hist:"Eth mèn veïcul ei istoric",pmr:"È carta d'estacionament entà persones damb mobilitat redusida",
res_label:"Opcionau: en quin municipi pague eth tòn còche er impòst de circulacion? Quauques ciutats dèishen entrar es còches des sòns vesins.",res_none:"Non ac sai o prefereishi non díder-ac",choose_label:"Prefereishi triar era mia etiqueta",share:"Partejar per WhatsApp",
h_map:"Mapa des zònes",choose_city:"Tria ua ciutat",where0:"Sarra eth boton entà veir se ès laguens d'ua zòna.",locate:"A on sò?",
h_route:"Planifica eth tòn viatge",route_help:"Escriu d'a on parts e a on vas. Te dideram quines zònes de baishes emissions trauèsse era rota e se i pòts entrar damb era tua etiqueta.",orig_ph:"Origina: carrèr, ciutat o pòble",dest_ph:"Destinacion: carrèr, ciutat o pòble",route_btn:"Veir era rota",route_note:"Era rota ei orientativa (calculada damb OpenStreetMap e OSRM). Entà cercar-la, era origina e era destinacion s'envien a aguesti servicis.",
h_cities:"Zònes de baishes emissions per ciutat",h_guides:"Guides",lang_note:"Es normes de cada ciutat se mòstren en castelhan.",
l0:"Zèro emissions",lE:"ECO",lC:"C (verda)",lB:"B (jauna)",lN:"Sense etiqueta",label_x:"Etiqueta {x}",chosen:"Triada per tu",plate_src:"Matricula {p} segontes era DGT",
v_ok:"Pòts entrar",v_no:"Non pòts entrar",v_warn:"Òc, exceptat avís de contaminacion",v_unk:"Donades pòc clares: consulta",v_pend:"Encara sense donades: consulta er ajuntament",v_exc:"Pòt èster qu'ages excepcion: verifica-ac",unverified:" · donada sense verificar",
summary:"Segontes es donades publicades, pòts entrar tostemp en {ok} de {n} ciutats damb zòna de baishes emissions",watch:"Compde damb aguestes:",all:"Veir totes es ciutats",disclaimer:"Informacion orientativa e non oficiau. Es normes cambien e cada ajuntament a era darrèra paraula: abans d'entrar, confirma-ac en sòn web. ",legal:"Avís legau",
bad_t:"Matricula incompleta",bad_s:"Escriu-la sancera, per exemple 1234BCD o M1234AB.",notfound_t:"Non trobam {p}",notfound_s:"Non apareish en fichèr dera DGT. Revisa qu'estigue ben escrita o consulta-la ena sedença dera DGT.",
dest_city:"A on vas? (opcionau) Ex.: Granada",dest_nf:"Non auem aguesta ciutat. Tria-ne ua dera lista o guarda «Veir totes es ciutats».",dest_more:"Veir normes e mapa",others:"D'auti {n} municipis obligats encara non auem es normes: son en «Veir totes es ciutats»."},

en: {nav_home:"Home",nav_cities:"Cities",nav_open:"Most open cities",nav_guides:"Guides",nav_faq:"FAQ",nav_legal:"Legal notice",
h1:"Can my car enter?",sub:"Type your Spanish number plate and we'll tell you its DGT environmental label and which low emission zones in Spain you can enter.",install:"Install as an app on your phone",
h_plate:"Your number plate",check:"Check",nostore:"We don't store the plates you type.",exc_legend:"Do you have an exemption? (the DGT file doesn't show it)",hist:"My vehicle is a historic vehicle",pmr:"I have a disabled parking card",
res_label:"Optional: in which Spanish town does your car pay road tax? Some cities let local residents' cars in.",res_none:"I don't know / prefer not to say",choose_label:"I'd rather choose my label",share:"Share on WhatsApp",
h_map:"Zone map",choose_city:"Choose a city",where0:"Press the button to see if you are inside a zone.",locate:"Where am I?",
h_route:"Plan your trip",route_help:"Type where you start and where you're going. We'll tell you which low emission zones the driving route crosses and whether your label can enter.",orig_ph:"From: street, city or town",dest_ph:"To: street, city or town",route_btn:"Show route",route_note:"The route is approximate (calculated with OpenStreetMap and OSRM). To find it, your start and destination are sent to those services.",
h_cities:"Low emission zones by city",h_guides:"Guides",lang_note:"City rules are shown in Spanish. Foreign-registered cars have no DGT label: see the guide for foreign cars.",
l0:"Zero emissions",lE:"ECO",lC:"C (green)",lB:"B (yellow)",lN:"No label",label_x:"Label {x}",chosen:"Chosen by you",plate_src:"Plate {p} according to the DGT",
v_ok:"You can enter",v_no:"You can't enter",v_warn:"Yes, except during pollution alerts",v_unk:"Unclear data: check",v_pend:"No data yet: ask the city council",v_exc:"You may be exempt: check",unverified:" · unverified data",
summary:"According to published data, you can always enter {ok} of {n} cities with a low emission zone",watch:"Watch out for these:",all:"See all cities",disclaimer:"Unofficial information for guidance only. Rules change and each city council has the final say: check its website before entering. ",legal:"Legal notice",
bad_t:"Incomplete plate",bad_s:"Type the whole plate, e.g. 1234BCD or M1234AB.",notfound_t:"We couldn't find {p}",notfound_s:"It isn't in the DGT file. Check it's typed correctly.",
dest_city:"Where are you going? (optional) e.g. Granada",dest_nf:"We don't have that city. Pick one from the list or see «See all cities».",dest_more:"See rules and map",others:"For {n} other municipalities that must have a zone we don't have the rules yet: see «See all cities»."},

fr: {nav_home:"Accueil",nav_cities:"Villes",nav_open:"Villes les plus ouvertes",nav_guides:"Guides",nav_faq:"Questions",nav_legal:"Mentions légales",
h1:"Puis-je entrer avec ma voiture ?",sub:"Saisissez votre plaque espagnole : nous vous indiquons votre vignette environnementale de la DGT et dans quelles zones à faibles émissions d'Espagne vous pouvez entrer.",install:"Installer comme appli sur le téléphone",
h_plate:"Votre plaque",check:"Vérifier",nostore:"Nous ne conservons pas les plaques saisies.",exc_legend:"Avez-vous une dérogation ? (le fichier de la DGT ne l'indique pas)",hist:"Mon véhicule est un véhicule historique",pmr:"J'ai une carte de stationnement pour personnes handicapées",
res_label:"Facultatif : dans quelle commune espagnole votre voiture paie-t-elle la taxe de circulation ? Certaines villes laissent entrer les voitures de leurs habitants.",res_none:"Je ne sais pas / je préfère ne pas le dire",choose_label:"Je préfère choisir ma vignette",share:"Partager sur WhatsApp",
h_map:"Carte des zones",choose_city:"Choisissez une ville",where0:"Appuyez sur le bouton pour savoir si vous êtes dans une zone.",locate:"Où suis-je ?",
h_route:"Préparez votre trajet",route_help:"Indiquez votre point de départ et votre destination. Nous vous disons quelles zones à faibles émissions traverse l'itinéraire et si votre vignette peut y entrer.",orig_ph:"Départ : rue, ville ou village",dest_ph:"Arrivée : rue, ville ou village",route_btn:"Voir l'itinéraire",route_note:"L'itinéraire est indicatif (calculé avec OpenStreetMap et OSRM). Pour le trouver, le départ et l'arrivée sont envoyés à ces services.",
h_cities:"Zones à faibles émissions par ville",h_guides:"Guides",lang_note:"Les règles de chaque ville sont affichées en espagnol. Les voitures immatriculées à l'étranger n'ont pas de vignette DGT : voir le guide des voitures étrangères.",
l0:"Zéro émission",lE:"ECO",lC:"C (verte)",lB:"B (jaune)",lN:"Sans vignette",label_x:"Vignette {x}",chosen:"Choisie par vous",plate_src:"Plaque {p} selon la DGT",
v_ok:"Vous pouvez entrer",v_no:"Vous ne pouvez pas entrer",v_warn:"Oui, sauf alerte pollution",v_unk:"Données peu claires : vérifiez",v_pend:"Pas encore de données : renseignez-vous à la mairie",v_exc:"Vous avez peut-être une dérogation : vérifiez",unverified:" · donnée non vérifiée",
summary:"D'après les données publiées, vous pouvez toujours entrer dans {ok} des {n} villes avec zone à faibles émissions",watch:"Attention à celles-ci :",all:"Voir toutes les villes",disclaimer:"Information indicative et non officielle. Les règles changent et chaque mairie a le dernier mot : vérifiez sur son site avant d'entrer. ",legal:"Mentions légales",
bad_t:"Plaque incomplète",bad_s:"Saisissez la plaque entière, par ex. 1234BCD ou M1234AB.",notfound_t:"Nous ne trouvons pas {p}",notfound_s:"Elle ne figure pas dans le fichier de la DGT. Vérifiez la saisie.",
dest_city:"Où allez-vous ? (facultatif) Ex. : Grenade",dest_nf:"Nous n'avons pas cette ville. Choisissez-en une dans la liste ou voyez «Voir toutes les villes».",dest_more:"Voir règles et carte",others:"Pour {n} autres communes concernées, nous n'avons pas encore les règles : voir «Voir toutes les villes»."},

de: {nav_home:"Start",nav_cities:"Städte",nav_open:"Offenste Städte",nav_guides:"Ratgeber",nav_faq:"Fragen",nav_legal:"Impressum",
h1:"Darf ich mit meinem Fahrzeug hinein?",sub:"Geben Sie Ihr spanisches Kennzeichen ein: Wir zeigen Ihre Umweltplakette der DGT und in welche Umweltzonen in Spanien Sie fahren dürfen.",install:"Als App auf dem Handy installieren",
h_plate:"Ihr Kennzeichen",check:"Prüfen",nostore:"Wir speichern die eingegebenen Kennzeichen nicht.",exc_legend:"Haben Sie eine Ausnahme? (steht nicht in der DGT-Datei)",hist:"Mein Fahrzeug ist ein Oldtimer (historisch)",pmr:"Ich habe einen Parkausweis für Menschen mit Behinderung",
res_label:"Optional: In welcher spanischen Gemeinde zahlt Ihr Fahrzeug die Kfz-Steuer? Manche Städte lassen Fahrzeuge ihrer Einwohner hinein.",res_none:"Weiß ich nicht / möchte ich nicht sagen",choose_label:"Ich wähle meine Plakette lieber selbst",share:"Über WhatsApp teilen",
h_map:"Karte der Zonen",choose_city:"Stadt wählen",where0:"Drücken Sie den Knopf, um zu sehen, ob Sie in einer Zone sind.",locate:"Wo bin ich?",
h_route:"Route planen",route_help:"Geben Sie Start und Ziel ein. Wir zeigen, welche Umweltzonen die Route durchquert und ob Sie mit Ihrer Plakette hinein dürfen.",orig_ph:"Start: Straße, Stadt oder Ort",dest_ph:"Ziel: Straße, Stadt oder Ort",route_btn:"Route anzeigen",route_note:"Die Route ist nur ein Richtwert (berechnet mit OpenStreetMap und OSRM, für Pkw). Start und Ziel werden dafür an diese Dienste gesendet. Für Lkw gelten oft eigene Regeln.",
h_cities:"Umweltzonen nach Stadt",h_guides:"Ratgeber",lang_note:"Die Regeln der Städte werden auf Spanisch angezeigt. Fahrzeuge mit ausländischem Kennzeichen haben keine DGT-Plakette: siehe Ratgeber für ausländische Fahrzeuge.",
l0:"Null Emissionen",lE:"ECO",lC:"C (grün)",lB:"B (gelb)",lN:"Keine Plakette",label_x:"Plakette {x}",chosen:"Von Ihnen gewählt",plate_src:"Kennzeichen {p} laut DGT",
v_ok:"Einfahrt erlaubt",v_no:"Einfahrt nicht erlaubt",v_warn:"Ja, außer bei Smog-Alarm",v_unk:"Unklare Daten: bitte prüfen",v_pend:"Noch keine Daten: bei der Stadt nachfragen",v_exc:"Eventuell Ausnahme: bitte prüfen",unverified:" · ungeprüfte Angabe",
summary:"Laut veröffentlichten Daten dürfen Sie immer in {ok} von {n} Städten mit Umweltzone fahren",watch:"Achtung bei diesen:",all:"Alle Städte anzeigen",disclaimer:"Unverbindliche, nicht amtliche Information. Regeln ändern sich, das letzte Wort hat die Stadt: vor der Einfahrt auf ihrer Website prüfen. ",legal:"Impressum",
bad_t:"Kennzeichen unvollständig",bad_s:"Bitte vollständig eingeben, z. B. 1234BCD oder M1234AB.",notfound_t:"{p} nicht gefunden",notfound_s:"Nicht in der DGT-Datei. Bitte Schreibweise prüfen.",
dest_city:"Wohin fahren Sie? (optional) z. B. Granada",dest_nf:"Diese Stadt haben wir nicht. Wählen Sie eine aus der Liste oder sehen Sie «Alle Städte anzeigen».",dest_more:"Regeln und Karte ansehen",others:"Für {n} weitere verpflichtete Gemeinden haben wir die Regeln noch nicht: siehe «Alle Städte anzeigen»."},

pl: {nav_home:"Start",nav_cities:"Miasta",nav_open:"Najbardziej otwarte miasta",nav_guides:"Poradniki",nav_faq:"Pytania",nav_legal:"Nota prawna",
h1:"Czy mogę wjechać swoim pojazdem?",sub:"Wpisz hiszpański numer rejestracyjny, a pokażemy naklejkę ekologiczną DGT i do których stref niskiej emisji w Hiszpanii możesz wjechać.",install:"Zainstaluj jako aplikację w telefonie",
h_plate:"Twój numer rejestracyjny",check:"Sprawdź",nostore:"Nie zapisujemy wpisanych numerów.",exc_legend:"Masz wyjątek? (plik DGT tego nie podaje)",hist:"Mój pojazd jest zabytkowy",pmr:"Mam kartę parkingową dla osób z niepełnosprawnością",
res_label:"Opcjonalnie: w której hiszpańskiej gminie twój pojazd płaci podatek drogowy? Niektóre miasta wpuszczają pojazdy swoich mieszkańców.",res_none:"Nie wiem / wolę nie mówić",choose_label:"Wolę sam wybrać naklejkę",share:"Udostępnij przez WhatsApp",
h_map:"Mapa stref",choose_city:"Wybierz miasto",where0:"Naciśnij przycisk, aby sprawdzić, czy jesteś w strefie.",locate:"Gdzie jestem?",
h_route:"Zaplanuj trasę",route_help:"Wpisz skąd i dokąd jedziesz. Powiemy, przez które strefy niskiej emisji przechodzi trasa i czy możesz wjechać ze swoją naklejką.",orig_ph:"Skąd: ulica, miasto lub miejscowość",dest_ph:"Dokąd: ulica, miasto lub miejscowość",route_btn:"Pokaż trasę",route_note:"Trasa jest orientacyjna (obliczona z OpenStreetMap i OSRM, dla samochodów osobowych). Punkt startu i celu są wysyłane do tych usług. Dla ciężarówek często obowiązują osobne zasady.",
h_cities:"Strefy niskiej emisji według miast",h_guides:"Poradniki",lang_note:"Zasady miast są podane po hiszpańsku. Pojazdy z zagraniczną rejestracją nie mają naklejki DGT: zobacz poradnik dla pojazdów zagranicznych.",
l0:"Zero emisji",lE:"ECO",lC:"C (zielona)",lB:"B (żółta)",lN:"Bez naklejki",label_x:"Naklejka {x}",chosen:"Wybrana przez ciebie",plate_src:"Numer {p} według DGT",
v_ok:"Możesz wjechać",v_no:"Nie możesz wjechać",v_warn:"Tak, poza alarmem smogowym",v_unk:"Niejasne dane: sprawdź",v_pend:"Brak danych: zapytaj w urzędzie miasta",v_exc:"Możesz mieć wyjątek: sprawdź",unverified:" · dane niezweryfikowane",
summary:"Według opublikowanych danych zawsze możesz wjechać do {ok} z {n} miast ze strefą niskiej emisji",watch:"Uwaga na te:",all:"Zobacz wszystkie miasta",disclaimer:"Informacja orientacyjna i nieoficjalna. Zasady się zmieniają, a ostatnie słowo ma miasto: sprawdź na jego stronie przed wjazdem. ",legal:"Nota prawna",
bad_t:"Niepełny numer",bad_s:"Wpisz cały numer, np. 1234BCD lub M1234AB.",notfound_t:"Nie znaleziono {p}",notfound_s:"Nie ma go w pliku DGT. Sprawdź pisownię.",
dest_city:"Dokąd jedziesz? (opcjonalnie) np. Granada",dest_nf:"Nie mamy tego miasta. Wybierz z listy albo zobacz «Zobacz wszystkie miasta».",dest_more:"Zobacz zasady i mapę",others:"Dla {n} innych zobowiązanych gmin nie mamy jeszcze zasad: zobacz «Zobacz wszystkie miasta»."},

pt: {nav_home:"Início",nav_cities:"Cidades",nav_open:"Cidades mais abertas",nav_guides:"Guias",nav_faq:"Perguntas",nav_legal:"Aviso legal",
h1:"Posso entrar com o meu carro?",sub:"Escreva a matrícula espanhola e dizemos-lhe o dístico ambiental da DGT e em que zonas de baixas emissões de Espanha pode entrar.",install:"Instalar como app no telemóvel",
h_plate:"A sua matrícula",check:"Verificar",nostore:"Não guardamos as matrículas escritas.",exc_legend:"Tem alguma exceção? (o ficheiro da DGT não a indica)",hist:"O meu veículo é histórico",pmr:"Tenho cartão de estacionamento para pessoas com mobilidade reduzida",
res_label:"Opcional: em que município espanhol paga o seu carro o imposto de circulação? Algumas cidades deixam entrar os carros dos seus moradores.",res_none:"Não sei / prefiro não dizer",choose_label:"Prefiro escolher o meu dístico",share:"Partilhar no WhatsApp",
h_map:"Mapa das zonas",choose_city:"Escolha uma cidade",where0:"Carregue no botão para ver se está dentro de uma zona.",locate:"Onde estou?",
h_route:"Planeie a sua viagem",route_help:"Escreva de onde parte e para onde vai. Dizemos-lhe que zonas de baixas emissões a rota atravessa e se pode entrar com o seu dístico.",orig_ph:"Origem: rua, cidade ou localidade",dest_ph:"Destino: rua, cidade ou localidade",route_btn:"Ver a rota",route_note:"A rota é indicativa (calculada com OpenStreetMap e OSRM). Para a encontrar, a origem e o destino são enviados para esses serviços.",
h_cities:"Zonas de baixas emissões por cidade",h_guides:"Guias",lang_note:"As regras de cada cidade aparecem em espanhol. Carros com matrícula estrangeira não têm dístico da DGT: veja o guia de carros estrangeiros.",
l0:"Zero emissões",lE:"ECO",lC:"C (verde)",lB:"B (amarelo)",lN:"Sem dístico",label_x:"Dístico {x}",chosen:"Escolhido por si",plate_src:"Matrícula {p} segundo a DGT",
v_ok:"Pode entrar",v_no:"Não pode entrar",v_warn:"Sim, exceto em alerta de poluição",v_unk:"Dados pouco claros: confirme",v_pend:"Ainda sem dados: pergunte à câmara municipal",v_exc:"Pode ter exceção: confirme",unverified:" · dado não verificado",
summary:"Segundo os dados publicados, pode entrar sempre em {ok} de {n} cidades com zona de baixas emissões",watch:"Atenção a estas:",all:"Ver todas as cidades",disclaimer:"Informação indicativa e não oficial. As regras mudam e cada câmara tem a última palavra: confirme no seu site antes de entrar. ",legal:"Aviso legal",
bad_t:"Matrícula incompleta",bad_s:"Escreva-a completa, por exemplo 1234BCD ou M1234AB.",notfound_t:"Não encontrámos {p}",notfound_s:"Não aparece no ficheiro da DGT. Verifique se está bem escrita.",
dest_city:"Para onde vai? (opcional) Ex.: Granada",dest_nf:"Não temos essa cidade. Escolha uma da lista ou veja «Ver todas as cidades».",dest_more:"Ver regras e mapa",others:"De outros {n} municípios obrigados ainda não temos as regras: estão em «Ver todas as cidades»."},

it: {nav_home:"Inizio",nav_cities:"Città",nav_open:"Città più aperte",nav_guides:"Guide",nav_faq:"Domande",nav_legal:"Note legali",
h1:"Posso entrare con la mia auto?",sub:"Scrivi la targa spagnola e ti diciamo il bollino ambientale della DGT e in quali zone a basse emissioni della Spagna puoi entrare.",install:"Installa come app sul telefono",
h_plate:"La tua targa",check:"Verifica",nostore:"Non salviamo le targhe inserite.",exc_legend:"Hai un'esenzione? (il file della DGT non la indica)",hist:"Il mio veicolo è storico",pmr:"Ho il contrassegno per persone con disabilità",
res_label:"Facoltativo: in quale comune spagnolo la tua auto paga il bollo? Alcune città fanno entrare le auto dei residenti.",res_none:"Non lo so / preferisco non dirlo",choose_label:"Preferisco scegliere il mio bollino",share:"Condividi su WhatsApp",
h_map:"Mappa delle zone",choose_city:"Scegli una città",where0:"Premi il pulsante per vedere se sei dentro una zona.",locate:"Dove sono?",
h_route:"Pianifica il viaggio",route_help:"Scrivi da dove parti e dove vai. Ti diciamo quali zone a basse emissioni attraversa il percorso e se puoi entrare con il tuo bollino.",orig_ph:"Partenza: via, città o paese",dest_ph:"Arrivo: via, città o paese",route_btn:"Vedi il percorso",route_note:"Il percorso è indicativo (calcolato con OpenStreetMap e OSRM). Per trovarlo, partenza e arrivo vengono inviati a questi servizi.",
h_cities:"Zone a basse emissioni per città",h_guides:"Guide",lang_note:"Le regole di ogni città sono in spagnolo. Le auto con targa straniera non hanno il bollino DGT: vedi la guida per le auto straniere.",
l0:"Zero emissioni",lE:"ECO",lC:"C (verde)",lB:"B (gialla)",lN:"Senza bollino",label_x:"Bollino {x}",chosen:"Scelto da te",plate_src:"Targa {p} secondo la DGT",
v_ok:"Puoi entrare",v_no:"Non puoi entrare",v_warn:"Sì, salvo allerta inquinamento",v_unk:"Dati poco chiari: verifica",v_pend:"Ancora nessun dato: chiedi al comune",v_exc:"Potresti essere esente: verifica",unverified:" · dato non verificato",
summary:"Secondo i dati pubblicati, puoi entrare sempre in {ok} delle {n} città con zona a basse emissioni",watch:"Attenzione a queste:",all:"Vedi tutte le città",disclaimer:"Informazione indicativa e non ufficiale. Le regole cambiano e ogni comune ha l'ultima parola: verifica sul suo sito prima di entrare. ",legal:"Note legali",
bad_t:"Targa incompleta",bad_s:"Scrivila intera, ad es. 1234BCD o M1234AB.",notfound_t:"Non troviamo {p}",notfound_s:"Non compare nel file della DGT. Controlla di averla scritta bene.",
dest_city:"Dove vai? (facoltativo) Es.: Granada",dest_nf:"Non abbiamo questa città. Scegline una dall'elenco o vedi «Vedi tutte le città».",dest_more:"Vedi regole e mappa",others:"Per altri {n} comuni obbligati non abbiamo ancora le regole: sono in «Vedi tutte le città»."},

ro: {nav_home:"Acasă",nav_cities:"Orașe",nav_open:"Orașe cele mai deschise",nav_guides:"Ghiduri",nav_faq:"Întrebări",nav_legal:"Informații legale",
h1:"Pot intra cu mașina mea?",sub:"Scrie numărul de înmatriculare spaniol și îți spunem eticheta ecologică DGT și în ce zone cu emisii scăzute din Spania poți intra.",install:"Instalează ca aplicație pe telefon",
h_plate:"Numărul tău",check:"Verifică",nostore:"Nu păstrăm numerele introduse.",exc_legend:"Ai o excepție? (fișierul DGT nu o arată)",hist:"Vehiculul meu este istoric",pmr:"Am card de parcare pentru persoane cu mobilitate redusă",
res_label:"Opțional: în ce localitate din Spania plătește mașina ta impozitul auto? Unele orașe lasă să intre mașinile localnicilor.",res_none:"Nu știu / prefer să nu spun",choose_label:"Prefer să-mi aleg eticheta",share:"Trimite pe WhatsApp",
h_map:"Harta zonelor",choose_city:"Alege un oraș",where0:"Apasă butonul ca să vezi dacă ești într-o zonă.",locate:"Unde sunt?",
h_route:"Planifică drumul",route_help:"Scrie de unde pleci și unde mergi. Îți spunem prin ce zone cu emisii scăzute trece traseul și dacă poți intra cu eticheta ta.",orig_ph:"Plecare: stradă, oraș sau localitate",dest_ph:"Destinație: stradă, oraș sau localitate",route_btn:"Vezi traseul",route_note:"Traseul este orientativ (calculat cu OpenStreetMap și OSRM). Pentru căutare, plecarea și destinația sunt trimise acestor servicii.",
h_cities:"Zone cu emisii scăzute pe orașe",h_guides:"Ghiduri",lang_note:"Regulile fiecărui oraș sunt afișate în spaniolă. Mașinile cu numere străine nu au etichetă DGT: vezi ghidul pentru mașini străine.",
l0:"Zero emisii",lE:"ECO",lC:"C (verde)",lB:"B (galbenă)",lN:"Fără etichetă",label_x:"Eticheta {x}",chosen:"Aleasă de tine",plate_src:"Numărul {p} conform DGT",
v_ok:"Poți intra",v_no:"Nu poți intra",v_warn:"Da, cu excepția alertelor de poluare",v_unk:"Date neclare: verifică",v_pend:"Încă fără date: întreabă la primărie",v_exc:"Poate ai excepție: verifică",unverified:" · date neverificate",
summary:"Conform datelor publicate, poți intra mereu în {ok} din {n} orașe cu zonă cu emisii scăzute",watch:"Atenție la acestea:",all:"Vezi toate orașele",disclaimer:"Informație orientativă și neoficială. Regulile se schimbă și primăria are ultimul cuvânt: verifică pe site-ul ei înainte să intri. ",legal:"Informații legale",
bad_t:"Număr incomplet",bad_s:"Scrie-l complet, de ex. 1234BCD sau M1234AB.",notfound_t:"Nu găsim {p}",notfound_s:"Nu apare în fișierul DGT. Verifică dacă e scris corect.",
dest_city:"Unde mergi? (opțional) Ex.: Granada",dest_nf:"Nu avem acest oraș. Alege unul din listă sau vezi «Vezi toate orașele».",dest_more:"Vezi regulile și harta",others:"Pentru alte {n} localități obligate nu avem încă regulile: sunt la «Vezi toate orașele»."},

ar: {nav_home:"الرئيسية",nav_cities:"المدن",nav_open:"المدن الأكثر انفتاحًا",nav_guides:"أدلة",nav_faq:"أسئلة",nav_legal:"إشعار قانوني",
h1:"هل يمكنني الدخول بسيارتي؟",sub:"اكتب رقم لوحة سيارتك الإسبانية وسنخبرك بالملصق البيئي الخاص بها من مديرية المرور (DGT) وبالمناطق منخفضة الانبعاثات في إسبانيا التي يمكنك دخولها.",install:"ثبّت الموقع كتطبيق على هاتفك",
h_plate:"رقم لوحتك",check:"تحقّق",nostore:"لا نحتفظ بأرقام اللوحات التي تكتبها.",exc_legend:"هل لديك استثناء؟ (ملف DGT لا يذكره)",hist:"مركبتي تاريخية",pmr:"لدي بطاقة وقوف لذوي الإعاقة",
res_label:"اختياري: في أي بلدية إسبانية تدفع سيارتك ضريبة السير؟ بعض المدن تسمح بدخول سيارات سكانها.",res_none:"لا أعرف / أفضّل عدم القول",choose_label:"أفضّل اختيار ملصقي بنفسي",share:"شارك عبر واتساب",
h_map:"خريطة المناطق",choose_city:"اختر مدينة",where0:"اضغط الزر لتعرف إن كنت داخل منطقة.",locate:"أين أنا؟",
h_route:"خطّط لرحلتك",route_help:"اكتب من أين تنطلق وإلى أين تذهب. سنخبرك بالمناطق منخفضة الانبعاثات التي يمر بها الطريق وإن كان ملصقك يسمح بالدخول.",orig_ph:"الانطلاق: شارع أو مدينة أو بلدة",dest_ph:"الوجهة: شارع أو مدينة أو بلدة",route_btn:"اعرض الطريق",route_note:"الطريق تقريبي (محسوب باستخدام OpenStreetMap وOSRM). للبحث عنه تُرسَل نقطة الانطلاق والوجهة إلى هذه الخدمات.",
h_cities:"المناطق منخفضة الانبعاثات حسب المدينة",h_guides:"أدلة",lang_note:"قواعد كل مدينة معروضة باللغة الإسبانية. السيارات ذات اللوحات الأجنبية ليس لها ملصق DGT: راجع دليل السيارات الأجنبية.",
l0:"صفر انبعاثات",lE:"ECO",lC:"C (أخضر)",lB:"B (أصفر)",lN:"بدون ملصق",label_x:"ملصق {x}",chosen:"اخترته أنت",plate_src:"اللوحة {p} حسب DGT",
v_ok:"يمكنك الدخول",v_no:"لا يمكنك الدخول",v_warn:"نعم، إلا عند إنذار التلوث",v_unk:"بيانات غير واضحة: تحقّق",v_pend:"لا بيانات بعد: اسأل البلدية",v_exc:"قد يكون لديك استثناء: تحقّق",unverified:" · معلومة غير مؤكدة",
summary:"حسب البيانات المنشورة، يمكنك الدخول دائمًا إلى {ok} من أصل {n} مدينة فيها منطقة منخفضة الانبعاثات",watch:"انتبه لهذه:",all:"اعرض كل المدن",disclaimer:"معلومات إرشادية وغير رسمية. القواعد تتغير والكلمة الأخيرة للبلدية: تحقّق من موقعها قبل الدخول. ",legal:"إشعار قانوني",
bad_t:"رقم غير مكتمل",bad_s:"اكتبه كاملًا، مثل 1234BCD أو M1234AB.",notfound_t:"لم نجد {p}",notfound_s:"غير موجود في ملف DGT. تأكد من كتابته بشكل صحيح.",
dest_city:"إلى أين تذهب؟ (اختياري) مثال: غرناطة",dest_nf:"ليست لدينا هذه المدينة. اختر واحدة من القائمة أو انظر «اعرض كل المدن».",dest_more:"عرض القواعد والخريطة",others:"لا نملك بعد قواعد {n} بلدية أخرى ملزمة: انظر «اعرض كل المدن»."}
};
let LANG = "es";
function t(k, v) {
  let s = (TXT[LANG] && TXT[LANG][k] != null && TXT[LANG][k] !== "") ? TXT[LANG][k] : (TXT.es[k] || "");
  if (v) for (const [a, b] of Object.entries(v)) s = s.split("{" + a + "}").join(b);
  return s;
}
function elegirIdioma() {
  let l = new URLSearchParams(location.search).get("lang");
  if (!l) try { l = localStorage.getItem("puedo-lang"); } catch (e) {}
  if (!l) { const n = (navigator.language || "es").slice(0, 2).toLowerCase(); l = TXT[n] ? n : "es"; }
  return TXT[l] ? l : "es";
}
function aplicarIdioma(l) {
  LANG = TXT[l] ? l : "es";
  try { localStorage.setItem("puedo-lang", LANG); } catch (e) {}
  document.documentElement.lang = LANG === "oc" ? "oc-aranes" : LANG;
  document.documentElement.dir = LANG === "ar" ? "rtl" : "ltr";
  document.querySelectorAll("[data-t]").forEach(e => { e.textContent = t(e.dataset.t); });
  document.querySelectorAll("[data-tph]").forEach(e => { e.placeholder = t(e.dataset.tph); });
  const nota = document.getElementById("langnote");
  if (nota) { nota.textContent = t("lang_note"); nota.hidden = !t("lang_note") || LANG === "es"; }
}
