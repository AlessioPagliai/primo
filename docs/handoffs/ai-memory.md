# Umanoide G1 open hardware - memoria condivisa

Ultimo aggiornamento: 2026-09-19.

> **NOME = "primo" — PUBBLICAZIONE COMPLETATA SU TUTTE LE PIATTAFORME — 2026-09-19 sera (AI + utente) [SUPERA i due bullet sotto]:** l'umanoide si chiama **primo** (scelto dall'utente tra 10 proposte nello stile River Family); titolo dei listing **"Primo open source humanoid robot"** (minuscolo su sito e MakerOnline). Repo GitHub rinominato `AlessioPagliai/primo` (il vecchio URL `umanoide` reindirizza); cartella locale del repo resta `~/Documents/artes/umanoide-release`. **REGOLA COMMIT:** autore SOLO `Alessio Pagliai <alessiopagliai.d@gmail.com>`, MAI trailer `Co-Authored-By: AI` ne' identita' di default del Mac (`utente1`); storia di `primo` e ultimi commit di `RiverFamily` riscritti e force-pushati il 2026-09-19; regola scritta in `~/Desktop/PUBLISH_GITHUB_AS_ALESSIO.md`. Niente etichette "AI made" sulle piattaforme. **URL:** YouTube https://youtu.be/6nTcHpFmKbQ (4K60 H.264 closed-GOP, capitoli; i due upload precedenti sono stati cancellati dall'utente: il master HEVC open-GOP veniva riprodotto da YouTube a blocchi di 4 s ripetuti); sito https://riverfamily.art/#primo (versione App Engine `gallery-primo-20260919`: "more" = solo video, mp4 GCS su desktop / iframe YouTube su mobile come gli altri design; "make" = scarica `primo.zip`); Printables https://www.printables.com/model/1846831 (video incorporato, 26 tag, 35 STL + 2 3MF); Thingiverse https://www.thingiverse.com/thing:7411626; Cults https://cults3d.com/en/3d-model/gadget/primo-open-source-humanoid (immagini 1:1, clip 30 s, CC0, gratis); Creality Cloud https://www.crealitycloud.com/it/model-detail/6aae7192f052c066aeb8dd96 (scheda completa ma RESPINTA dalla moderazione: la cover deve essere una foto reale della stampa; non visibile al pubblico, quindi NON linkata nei doc; quando ci sono le foto: profilo › Modello 3D › ⋯ › Modifica, foto come cover, nome "Primo open source humanoid robot", reinviare); MakerOnline https://www.makeronline.com/en/model/primo%20open%20source%20humanoid/331171.html; MakerWorld: bozza 9688828 reinviata e di nuovo RESPINTA in automatico (nessuna foto reale; sta in Modelli 3D › Fallito › Modifica) — senza FOTO REALE di un pezzo stampato viene sempre respinta (l'utente fara' le foto tra qualche giorno); lo slot video MakerWorld non accetta upload programmatico: trascinare a mano `publishing-upload/video/primo-30s.mp4`. **Cartella condivisa autosufficiente:** `gs://riverfamily/primo/primo.zip` = intero repo (README, AGENTS.md come punto d'ingresso per una nuova sessione AI, questa memoria in `docs/handoffs/ai-memory.md`, BOM + generatore, schema elettrico, `cad/stl/` = SOLO i 20 pezzi da stampare in mm, dx+sx = 35 STL; i componenti comprati stanno nel BOM e le loro mesh solo in `sim/meshes/` per l'URDF `sim/urdf/primo.urdf`, pipeline mirror, handoff Isaac/teleop). MANCA nel repo: il codice di training Isaac Lab, che sta sulla workstation (segnaposto `sim/isaaclab/README.md`). Altri file GCS: `primo/primo-stl.zip`, `primo/videos/{primo-4k60,primo-30s,walk-kneehard,walk-kneetorque}.mp4`, `videos/Primo_720p.mp4` (sito). Testi, tag e lista URL: `umanoide-release/publishing/platform-texts.md`. Policy di camminata scelta: KneeHard.
> **PUBBLICAZIONE OPEN SOURCE — PACCHETTO RELEASE PREPARATO — 2026-09-19 (AI + user):** l'utente pubblica il progetto oggi su GitHub (account `AlessioPagliai`), Printables/MakerWorld/Thingiverse (@River_Family / @RiverFamily), riverfamily.art e YouTube (@art.riverfamily). Stile appreso dai suoi siti: **minimale estremo, nomi in minuscolo, inglese, descrizioni 0-15 parole, nessun marketing, licenza CC0, file grandi sul bucket GCS `gs://riverfamily/`, link a tutte le piattaforme**. Nome di lavoro: `umanoide`. Creata cartella pulita **`/Users/artes/Documents/artes/umanoide-release/`** (repo git locale, 1 commit, 1.6 MB): `README.md` (numeri, fasi/costi, file, sim, punti aperti, licenza), `bom/` (bom.xlsx + bom.csv 108 righe attive + build_bom.py), `electrical/` (scheme md/svg/png), `cad/` (README con link Onshape, `motor_proxy.fs`, `3mf/ankle-gimbal.3mf` = Bambu PPA-CF H2C 1 parete 90% griglia, `3mf/leg-test-plate.3mf` = femore+staffa anca+tibia in PLA su H2S), `sim/` (mirror_urdf.py, ankle_map.py + ankle-transmission.md CON AVVISO "geometria provvisoria da centroidi mesh", g1_joints_reference.csv), `docs/` (hand-design, actuator-tables, references.md con 27 paper arXiv + link vendor, `handoffs/` = isaac/teleop/mirror-debug + **ai-memory.md = copia di questo MEMORY.md**), `publishing/platform-texts.md` (testi pronti per ogni piattaforma, entry catalogue.json, blocco README RiverFamily, lista immagini da fare in Onshape), `LICENSE.md` CC0 (copiato da RiverFamily). **ESCLUSI deliberatamente:** `sources/` (paper, 400 MB: solo elenco), `motors/`+`hands/` (manuali/STEP vendor: solo link), `hydrogen/` e `noetix_manual/` (progetti non correlati), `Asimov 1 BOM`, `G1.blend`, `outputs/`. **Caricati su GCS (pubblici):** `gs://riverfamily/umanoide/umanoide-urdf.zip` (11.8 MB = rl_full: urdf+mesh+handoff) e `videos/walk-kneehard.mp4`, `walk-kneetorque.mp4`. Totali BOM al 2026-09-19 invariati: residuo 10.264,90 / F1 4.008,57 / F2 3.997,95 / F3 2.258,38; massa 33,24 kg. **DA FARE:** immagini/GIF Onshape dall'utente (`images/hero.webp` referenziata nel README), documento Onshape reso pubblico, creazione repo GitHub `AlessioPagliai/umanoide` + push (terminale NON autenticato: serve `gh auth login` o PAT, oppure upload via browser), upload 3MF su Printables/MakerWorld/Thingiverse, video YouTube, entry sito. Nota policy locomozione: `KneeHard.mp4` vs `KneeTorque.mp4` (compare_r5 = sweep KneeDefault/Soft/Hard + KneeTorque); config sul workstation Isaac, non qui.
- **PUBBLICATO — 2026-09-19 (AI, sessione autonoma):** GitHub https://github.com/AlessioPagliai/umanoide (repo locale `umanoide-release/`, branch main); Printables https://www.printables.com/model/1846831-umanoide-open-source-humanoid-in-design (RC & Robotics, CC0, origine "original", flag AI = "AI-assisted" scelto per prudenza: cambiabile in Edit model); Thingiverse https://www.thingiverse.com/thing:7411626 (Hobby › Robotics, Work in Progress, CC0, 2 3MF + 5 immagini); MakerWorld: bozza 9686078 completa (testi, categoria Robotica, tag, cover 4:3+3:4, 4 immagini, profilo di stampa ankle-gimbal.3mf, CC0) INVIATA ma RESPINTA dal controllo automatico: "Il sistema non ha rilevato alcuna foto reale" → serve una FOTO VERA di un pezzo stampato (gimbal o leg test plate) nelle immagini modello e nel profilo di stampa, poi risottomettere da Modelli 3D › Fallito › Modifica (o "Ricorso"); nei doc per ora c'è il link profilo https://makerworld.com/it/@RiverFamily, DA SOSTITUIRE con il link modello appena approvato (README release "Also on", publishing/platform-texts.md, README + catalogue.json del repo RiverFamily, descrizione YouTube); il profilo di stampa MakerWorld ha solo render CAD, MakerWorld chiede una foto reale del pezzo stampato → aggiungerla appena stampato il gimbal, altrimenti può rimuovere il profilo; nome profilo rimasto quello automatico "0.2mm layer, 1 walls, 90% infill". YouTube https://youtu.be/bHGGjXYELUE (CAD tour, descrizione con tutti i link). Sito: versione App Engine `gallery-umanoide-20260919` promossa (slide `#umanoide`, sezione "more" con CAD · files · 3MF · video; il sito non linka le piattaforme per nessun modello, coerente). Repo catalogo RiverFamily (`/Users/artes/Documents/paths/Ben/riverfamily-github`) aggiornato e pushato. GCS: gs://riverfamily/umanoide/ (zip, urdf zip, immagini, video). Staging upload browser: `publishing-upload/` (jpg 4:3/16:9/1:1/3:4 con padding bianco). Policy camminata scelta: **KneeHard** (la più semplice; KneeTorque aggiunge un termine di penalità sulla coppia; i config stanno sulla workstation Isaac, in locale solo i video). Video walk su GCS: videos/walk-kneehard.mp4, videos/walk-kneetorque.mp4.

> **CUSTOM 15-DOF DIRECT-JOINT HAND DEVELOPMENT — 2026-07-19 (AI + user; PLANNED PROJECT WORKSTREAM, ACTUATORS NOT YET LOCKED):**
> - The project explicitly includes designing and open-sourcing its own five-finger hand with **3 independently actuated DoF per digit = 15 actuators/hand**; this is not merely an optional market comparison. For index through little finger: MCP ab/adduction, MCP flexion, PIP flexion; DIP may be passive/coupled. The thumb must instead implement CMC opposition/reposition, CMC/MCP flexion and IP flexion; do not copy the four-finger axes blindly. The preferred design has an actuator physically at each joint, not tendons, if a genuinely suitable commercial module exists.
> - **Development sequence:** start the first humanoid build with the proven `RH56DFX-2L/R` hands, while developing the custom hands in parallel through single-finger prototypes. Do not remove Inspire from the active BOM/CAD until the custom hand is complete and passes force, backlash, heating, impact and lifetime tests. The custom hand is intended as a later replacement and open-source project deliverable; only its actuator selection remains open.
> - `DYNAMIXEL XC330-T288-T` and `XL330-M288-T` share the same `20 x 34 x 26 mm` envelope, absolute magnetic encoder, current feedback/control and TTL multidrop concept, but are not equivalent internally. XC: 23 g, metal gears, coreless motor, 6.5-12 V, 1.00 Nm stall at 12 V, about 0.20 Nm conservative normal-use estimate, about EUR 110.40. XL: 18 g, plastic gears, cored motor, 3.7-6 V, 0.52 Nm stall at 5 V, about 0.104 Nm conservative estimate, about EUR 40.20. XC is roughly 2x stronger and more impact-resistant but about 2.75x the price; XL is the rational choice for protected palm/forearm tendon actuation. **Both are too bulky for a human-scale motor at every PIP:** the 20 mm bare thickness becomes roughly 24-28 mm with structural cheeks/opposite support, and the 34 mm body consumes most of a phalanx.
> - **Current direct-joint retail prototype candidate: `Waveshare SC09` / Feetech `SCS009`.** Exact published values: `23.2 x 12.0 x 25.5 mm`, 12.5 g, 4-6 V, metal gears, carbon-film potentiometer, 1024 positions over 300 deg (0.293 deg), TTL serial to 1 Mbps, position/load/speed/voltage feedback, no measured-current control and no temperature feedback. Published **rated torque = 0.7 kgf.cm = 0.0686 Nm**; stall torque = 2.3 kgf.cm = 0.2256 Nm; no-load speed 100 rpm; stall current 1 A at 6 V; about USD 8.99. Product/CAD/docs: <https://www.waveshare.com/SC09-Servo.htm> and <https://www.waveshare.com/wiki/SC09_Servo>.
> - **Torque comparison must not be lost:** XL330 is about `0.104/0.0686 = 1.52x` stronger in conservative normal use and `0.52/0.2256 = 2.30x` stronger at stall than SC09. Approximate output force using torque/lever (before linkage/contact losses): at a 70 mm MCP lever, SC09 rated/stall = `0.98 / 3.22 N`, XL330 estimated-normal/stall = `1.49 / 7.43 N`; at a 30 mm PIP lever, SC09 = `2.29 / 7.52 N`, XL330 = `3.47 / 17.33 N`. Stall values are momentary and must never be presented as sustainable grip. SC09 wins packaging/cost, not torque or control quality.
> - Fifteen direct SC09s would be about 187.5 g and USD 135 per hand, with a theoretical all-stalled demand of 15 A at 6 V. This is dimensionally plausible but a **light-manipulation hand**, especially because MCP rated fingertip force is only about 1 N per digit. Its reported `load` is not a calibrated torque sensor. XL330 gives better sensing/control and torque but is geometrically poor on the fingers.
> - Other commercial leads: `KST X06` (`20 x 7 x 16.6 mm`, 6 g, 0.04 Nm rated / 0.176 Nm stall, PWM and no runtime telemetry) physically fits but is weak; `AGFRC A20CLS` (`23 x 12 x 27.5 mm`, 20 g, 0.735 Nm advertised stall, PWM/potentiometer, no normal runtime joint/current telemetry) is stronger but poor for state logging; Harmonic Drive `RSF-3C` is a real robot-grade finger actuator (about O20 x 47 mm, 31 g, 0.03-0.11 Nm rated and 0.13-0.30 Nm maximum depending ratio) but requires an external driver and is industrial/quotation-priced; Bonsystems `BCSA Micro` is advertised specifically as an O18 mm cycloidal direct finger actuator but currently has no public torque, mass, length, encoder, bus, price or retail-stock data, so it is not BOM-ready.
> - **Next gate before choosing 30 motors:** buy/build one complete three-DoF finger or at minimum a two-flexion-joint finger, then measure sustained fingertip force (not stall), backlash/deadband, loaded position error, temperature over repeated grasps, impact survival and bus update rate with multiple nodes. Do not freeze CAD around SC09, XL330 or BCSA Micro before this test. A mixed XL330+SC09 hand would require separate protocol/UART handling even if both are powered near 5 V.

> **HANDS-ON-WEHO DECISION + ELECTRONICS AUDIT FIXES — 2026-07-17 (AI + user):**
> - **User decision: le mani RH56DFX-2L/R sono COLLEGATE fin dalla prima build sul singolo rail WEHO 24 V** (supera il "no hands" del lock 2026-07-12 qui sotto). Budget: Thor cap 130 W (5.4 A) + 2 mani a 2 A max pubblicati (96 W) + hub/interfacce ≈ 241 W vs 240 W nominali / OCP 12 A: fuori budget solo a picco totalmente simultaneo. Mitigazioni: abbassare nvpmodel Thor durante lavoro bimane sostenuto, scaglionare i comandi mano in software, bench-log tensione/corrente del rail con entrambe le mani in presa sotto pieno carico GPU. CAVEAT: il manuale di integrazione Inspire raccomanda di provisionare fino a 5 A/mano; se le misure si avvicinano a quel valore il WEHO e' sottodimensionato -> passare a RSD-300C-24 o Cincon CHB350.
> - **PUNTO APERTO (decidere prima di cablare il ramo mani):** con le mani sul ramo NON commutato, l'e-stop NON toglie alimentazione alle mani (il vecchio rele' Omron dedicato era stato rimosso). Se le mani devono rilasciare su e-stop, aggiungere un piccolo rele' 24 V nel ramo mani 15 A pilotato dalla stessa catena e-stop.
> - **Correzioni BOM applicate 2026-07-17 (audit AI, generatore `build_umanoide_tab.py` + rigenerazione):** (1) mani, adattatore Waveshare 2CH RS485, cavo LINDY 36940 e fusibile MINI 15 A mani riattivati qty>0; portafusibili uscita 24 V portati a qty 3 (Thor + mani + hub). (2) Nuova riga design `SEQ-PWR-01` (sequenza precarica + driver bobine): il timer Eaton e il selettore a chiave erano stati rimossi e la carrier board citata dalle note era qty0, quindi NIENTE implementava "precarica prima del main" ne' il blocco riavvio automatico; Thor GPIO non puo' pilotare bobine 24 V direttamente. Fino al rilascio: procedura manuale scritta a due interruttori, mai chiudere il LEV100 su bus scarico. (3) Soppressione bobine ripristinata: nuova riga attiva `1.5KE33CA` sulle bobine 24 V (portata a qty 3 nella stessa giornata: LEV100 + CIT precarica + CIT latch); la vecchia riga 1.5KE68CA (dimensionata per le bobine 48 V rimosse) marcata [REMOVED qty0]. (4) Nuova riga `[TO DESIGN qty0]` condensatore low-ESR >=22 uF all'uscita WEHO (richiesto dal datasheet, prima presente solo nel README). (5) Nuova riga `[ORDER WITH BATTERY qty0]` per il mate XT90-S lato robot (mancava; confermare genere connettore alla consegna del pacco). (6) Fasi corrette per rendere coerente il bring-up a banco: LEV100, CIT, WEHO + fusibile/portafusibile ingresso, fusibile Thor 10 A e portafusibili uscita -> Phase 1 (le bobine sono 24 V: senza WEHO a banco la catena e-stop non esiste). (7) Note obsolete corrette: ramo comando safety ora documentato come ramo 24 V dal rail WEHO (non "48 V con timer e chiave"); nota fusibile mani ora cita il rail WEHO (non CHB350); HAR-ARM-01 ora include coppia potenza mani 24 V + doppino RS485 nel trunk braccio.
> - **TOTALI EXCEL RICALCOLATI E VERIFICATI 2026-07-17** (i totali "31.243,22 / 35,043 kg" scritti il 2026-07-12 erano lo snapshot di mezzogiorno CON mani qty1 e non erano mai stati aggiornati dopo il qty0 serale — errore di handoff): **Umanoide completo EUR 30.395,59; Fase 1 EUR 10.076,77 (di cui Thor 4.026,00); Fase 2 EUR 494,56; Fase 3 EUR 19.824,26; massa acquistata a bordo 33,082 kg** (attuatori 20,913 kg invariati, batteria 2,270 kg). Nota: la riga WEHO attiva ha ancora prezzo 0 in attesa di quotazione, quindi il totale sottostima di qualche decina di EUR.
> - README aggiornato nella stessa sessione: mani nella prima build, link Phidgets corretto (prodid=1205, riga 17 puntava a 1096), righe SEQ-PWR-01/TVS/condensatore, checklist pre-power-up estesa. Le sezioni storiche piu' in basso in questo file ("Elettrico e sicurezza", vecchia nota CANable V2.0) sono marcate come superate.
> - **SEQUENZA PRECARICA RISOLTA IN HARDWARE — 2026-07-17 (stessa sessione, decisione utente "componente semplice"):** niente PCB custom. Catena: `fusibile safety 24 V -> e-stop NC -> pulsante START Schneider XB5AA31 + rele' latch autoritenuta CIT A2K1CSQ24VDC1.6 (seconda unita' dello stesso SKU della precarica) -> bobina CIT precarica + timer ON-delay Omron H3YN-2 DC24 su zoccolo PYF08A-E -> contatto timer -> bobina LEV100`. START avvia precarica e ritardo; il timer chiude il LEV100 su bus gia' carico; il rilascio dell'e-stop NON riavvia mai il bus, solo START. Timer di marca deliberato: un timer che chiude in anticipo vanifica silenziosamente la precarica e puo' saldare il contattore principale. Taratura: misurare la tau reale di precarica osservando la telemetria VBUS dei RobStride a banco, impostare 4-5 tau (guida iniziale 10 s); Thor gata l'enable motori in software ma NON e' nella catena safety. `SEQ-PWR-01` in BOM e' ora il deliverable "disegno di cablaggio". Ingombri (verificare i disegni esatti prima del freeze CAD): latch 26.5 x 32 x 33.5 mm; timer+zoccolo circa 25 x 35 x 80 mm in piedi (o sdraiato); START foro pannello Ø22, circa 45 mm dietro pannello, accanto all'e-stop; massa aggiunta ~0.15 kg, costo ~EUR 66 netti (prezzi XB5AA31/H3YN/PYF08A da verificare all'ordine).
> - **PIPELINE URDF + SCRIPT MIRROR — 2026-07-18:** l'utente modella in Onshape SOLO lato destro + catena centrale (export nel formato `~/Downloads/rl/`: urdf/rl.urdf + meshes STL). Nuovo script repo `mirror_urdf.py`: rinomina i 17 revolute con nomi semantici G1-style (mappa dentro lo script, identificata via FK), converte continuous->revolute con limiti G1 mode_11 sign-corretti + effort dal picco RobStride (caviglia virtuale 72/36 Nm PROVVISORI) + velocity PROVVISORIE, specchia i sottoalberi gamba (subtree part_42) e braccio (part_12, escluso ramo part_49/50) con matematica world-frame per i giunti di attraversamento e coniugazione D=diag(1,-1,1) all'interno, assi (-ax,ay,-az) => stesso comando = moto specchiato e limiti identici, inerzie con Ixy/Iyz flippati, mesh STL specchiate vere (flip y + winding, niente scale negativa), collision di primo giro su pelvi/torso/coscia/stinco/piede. Output `~/Downloads/rl_full/`. VERIFICATO: 30 revolute totali, simmetria 0.000 mm su tutte le coppie. DA FARE IN ONSHAPE: materiali/masse mancanti (export totale 3.63 kg vs ~15 attesi: tutti gli STEP importati - motori, mani, camera - hanno massa ~0; assegnare mass override da manuale), collision vere, conferma identita' part_42/49/50, limiti collo e velocity da datasheet.
> - **FASI RIDEFINITE + POSSEDUTI + FORNITORI — 2026-07-19 (sera; SUPERA il meccanismo "colonna MS1" del bullet sotto):** l'utente ha chiesto che la milestone-1 SIA la Fase 1, non una colonna parallela. Fatto: **colonna MS1 eliminata; la colonna Phase ora segue l'ordine di costruzione reale**: Fase 1 = banco braccio destro + mano + kit caviglia + batteria/dual-source + catena safety + Thor; Fase 2 = gambe e locomozione (RS04/RS03, RS06 caviglia dedicati, cablaggio gambe, IMU); Fase 3 = completamento (braccio/mano sinistri, vita, collo, audio, mobile). Le righe che attraversavano le fasi sono state SDOPPIATE nel generatore (`ROW_SPLIT`: 5 righe motori braccio RIGHT/LEFT, BCCA4011 superiori 8/9, portafusibili MIDI 2/2/2, fusibile braccio 30A 1/1, CANable 1/2); correzioni fase per il resto via `PHASE_TO`. **POSSEDUTI (lab): Thor e ENTRAMBE le mani RH56DFX** — contati a EUR 0 con prezzo di riferimento in nota; Thor si usa SUBITO in Fase 1 (niente piano PC-only; Molex J74 + fusibile 10 A spostati in Fase 1). **FORNITORI (preferenza utente, CORRETTO in serata dopo obiezione giusta dell'utente):** il primo tentativo (cambiare solo la colonna fornitore lasciando articolo/link originali) era INCOERENTE ed e' stato annullato. Regola finale implementata: si cambia fornitore SOLO con un equivalente REALE verificato (articolo+SKU+link+fornitore insieme), altrimenti resta la fonte specialistica. **Swap verificati sul web 2026-07-19:** capicorda Klauke 704F5/703F5/101R5 → **Bürklin** (stessi SKU esatti, ordini 07F1391/07F1381/07F2090, link prodotto verificati); e-stop → **Schneider XB4BS8442 su RS Italia** (RS 7951306: stessa testa fungo Ø40 rosso twist-release 1NC, versione XB4 METALLICA della XB5AS8442 plastica — verificare blocco 1NC e prezzo all'ordine; aggiornati anche README/schema/SVG e MASSA_UNIT 0.070). **Secondo giro su input utente (stessa sera):** Belden → **Farnell 1891187**: il **9841NH e' la versione halogen-free/LSZH del 9841**, venduto AL METRO (ordinare 50 m; prezzo riga ancora quello della bobina Rapid, verificare il totale Farnell all'ordine); **K05 → Bürklin 05L2734** (stesso carrello dei capicorda; anche RS 398-2270); **cavo Schuko → Amazon generico** (commodity: qualsiasi H07RN-F 3G1.5 ≥3 m con spina Schuko, riferimento precedente Craft EHK22146 in nota). Doc sincronizzati (schema md+svg ora citano 9841NH). **Mantenuti deliberatamente (nessun equivalente sensato nei big store):** Nautica Illiano per i cavi 25/16/6 mm² (RS vende il super-flex H01N2-D solo in bobine 50-100 m; Nautica vende al metro) e Accu per il controdado M8 SINISTRO (nicchia; verificare se il kit puntoni AliExpress li include gia'). NOTA DIN 439: le due righe controdadi NON sono un duplicato — una e' filetto DESTRO (per i KARM), una SINISTRO (per i KALM): i puntoni sono tenditori RH+LH; il filetto sinistro e' merce di nicchia (verificare se il kit puntoni AliExpress li include gia'). Nuovi totali = spesa residua: completo 10.264,90 / F1 4.008,57 / F2 3.997,95 / F3 2.258,38.
> - **MS1 = PRIMO ACQUISTO (milestone definita con l'utente) — 2026-07-19 [SUPERATO dal bullet sopra: colonna MS1 rimossa, ora Fase 1]:** primo banco fisico: **1 braccio destro** (motori: RS06 x3 + RS00 x4; i 2 RS06 faranno anche da motori caviglia per le prove — NIENTE RS06 caviglia dedicati e NIENTE RS04), **kit leveraggio 1 caviglia** (shoulder screws 45/16, dadi M6, puntoni 140/40, KARM/KALM, controdadi DIN439), **mano destra RH56DFX-2R** + adattatore 2CH RS485 + LINDY 36940, **batteria P45B + caricatore + mate XT90** e **doppia alimentazione banco: batteria E rete INSIEME** — requisito nuovo: NON si mettono mai in parallelo diretto (l'RSP-3000 flotterebbe il pacco 13S senza controllo, back-feed reciproco) -> nuova riga BOM `[TO SELECT qty0] Dual-source 48 V OR-ing stage` (ideal-diode per ramo, classe LTC4357/LM5050, <=20 A per il banco braccio; INTERIM: scambiare la sorgente all'XT90-S, mai entrambe). Catena safety completa inclusa (e-stop/START/latch/timer/TVS/LEV100/precarica/PDU/fusibili). **Thor NON in MS1**: il banco braccio-fisso si comanda dal PC/workstation con 1 CANable Pro + adattatore debug RobStride (Thor serve solo per la mobilita'). Torso stampato e fissato al tavolo (viti/inserti/filamento non-BOM). D436 inclusa per dati teleop/training. Riga Seeed XT30(2+2) Power Separation Board ATTIVATA qty2 Fase 1 (giunzione power/CAN del daisy-chain braccio + sede terminazioni, finche' non esiste JBOX-CAN-01). **Implementazione: nuova colonna Excel `MS1 qty` (col U)** scritta dal generatore (lista MS1 in `build_umanoide_tab.py`): filtrare la colonna per la lista spesa esatta; le qty MS1 sono FRAZIONI delle qty riga (es. shoulder pitch/roll 2 di 4). **Totale MS1 prezzato: EUR 12.085,36 IVA incl.** (mano 8.099 = 67%; motori 1.298; resto ~2.688), + righe senza prezzo da quotare: igus KARM/KALM, caricatore (con batteria), WEHO, condensatore 22uF, OR-ing stage. GATE ORDINE ancora aperti prima di comprare: batteria (spedizione Italia/BMS/regen), igus KALM disponibilita', pinout GX12 mano DFX da confermare con Inspire, prezzi XB5AA31/H3YN/PYF08A. Totali complessivi aggiornati (separation board attivata): completo 30.489,23 / F1 10.170,41.
> - **TELEOP META QUEST — MODE A SCELTO, HANDOFF AL WORKSTATION — 2026-07-19:** utente vuole teleoperare l'umanoide in Isaac Sim con un Meta Quest, stando lontano (guarda il workstation via AnyDesk, ha il Quest con se'). Decisione: **Mode A** = Quest come SOLO tracker, si guarda il viewport Isaac in 2D via AnyDesk (NON immersivo stereo in cuffia = Mode B/CloudXR, scartato). Fatto chiave: **AnyDesk NON trasporta il tracking del Quest** — le pose servono un percorso di rete separato (Tailscale overlay, oppure tunnel pubblico cloudflared/ngrok). Le pose sono minuscole (~72 Hz) e passano bene su internet; il difficile (video stereo verso la cuffia) non e' in questo design. Split di controllo obbligatorio per un umanoide: **gambe = policy RL autonoma comandata da thumbstick (vx,vy,yaw), NON puppet giunto-per-giunto** (la latenza uccide l'equilibrio); braccia (7/lato)/mani (RH56DFX 6 DOF/lato)/collo = teleop retargettato (latency-tolerant). Scritto `TELEOP_HANDOFF.md` (nel repo) per l'istanza AI sul workstation: architettura, piano a fasi (0 rete -> 1 pose che arrivano -> 2 braccia+grip semplice, gambe ferme -> 3 comando camminata -> 4 mani dexterous+collo), stack consigliato Open-TeleVision/Vuer (WebXR nel browser Quest, pose via WebRTC; usare sessione passthrough/immersive-ar cosi' l'operatore vede ancora lo schermo 2D AnyDesk), dex-retargeting per le mani Inspire (fase 4). Sezione "VERIFY LOCALLY" esplicita: versione Isaac/Isaac Lab e sua API IK, stato repo Open-TeleVision, interfaccia comando della walking policy — da confermare sul workstation, non dare per scontate da memoria. L'esecuzione la fa un'altra conversazione sul workstation; questa sessione Mac ha solo prodotto l'handoff. **ERGONOMIA — DUE SETUP, utente ancora indeciso (2026-07-19):** **A1 = Quest al collo**, testa fuori, guarda lo schermo AnyDesk esterno, solo pose in salita (piu' semplice per il bring-up); vincoli: sensore di prossimita' da disabilitare (nastro + auto-sleep off) o la sessione muore, posa cuffia = riferimento torso (niente head-tracking, niente head->collo), controller tracciati bene solo davanti al torso, calibrazione a timer. **A2 = Quest in testa normale + vista Isaac dentro la cuffia come PANNELLO 2D** (video mono via canale video-back dello stack teleop, NON stereo/CloudXR): questo e' cosa intende l'utente con "streammare lo schermo AnyDesk sul Quest" — si implementa facendo streammare allo stack il viewport Isaac su un pannello, NON facendo girare l'app AnyDesk sul Quest (finestra 2D e sessione immersive di tracking vanno in conflitto). A2 e' PREFERITO: recupera head-tracking (-> head->collo disponibile), FOV controller naturale (mani davanti al viso), niente problema prossimita'; costo = un video mono su internet verso la cuffia (latenza sulla vista tollerabile, le gambe sono autonome). RACCOMANDAZIONE nell'handoff: bring-up con A1 solo-pose (fasi 0-2), poi passare ad A2 aggiungendo lo stream viewport->pannello. Handoff `TELEOP_HANDOFF.md` aggiornato con entrambi.
> - **CAVIGLIA: MAPPA TRASMISSIONE DIFFERENZIALE RICAVATA DAL CAD — 2026-07-19 (grande risultato):** scoperto che l'export Onshape contiene GIA' la geometria dei puntoni: le parti unite da Group mate hanno il frame all'origine globale e la mesh in coordinate globali, quindi le posizioni dei perni (shoulder screws) sono estraibili. Geometria reale estratta (gamba destra, mm): **manovella 47.75 (entrambi i motori, orizzontale a zero), puntoni 208.01 (sup) e 106.01 (inf) occhio-occhio, braccio pitch 47.75, semi-span roll 43.83, puntoni VERTICALI a zero pose con manovelle a 90° (trasmissione ottimale)**. Risolve la vecchia domanda BOM: la lunghezza AliExpress e' del CORPO, occhio-occhio = corpo + ~68 mm. Nuovo file `ankle_map.py` (IK/FK esatte con solve del loop chiuso, Jacobiano, inviluppo coppie, scan workspace; round-trip validato a precisione macchina) + `ANKLE_TRANSMISSION.md`. **Rapporti: pitch = -0.500 x (th1+th2) = 1:1; roll = -0.545 x (th2-th1) = 1.09:1.** Corsa motori per i limiti URDF: ±43° pitch, ±14° roll (dentro RS06). **DECISIONE CONFERMATA: NON simulare i puntoni come corpi** (URDF non fa loop chiusi, Isaac potrebbe ma e' fragile/lento e inutile); la mappa e' analitica e vive fuori dalla policy (deploy: policy (pitch,roll) -> ik() -> 2 RS06; feedback -> fk() -> osservazione). Quello che DEVE entrare in sim e' l'inviluppo coppie ACCOPPIATO.
> - **CAVIGLIA — NUMERI CHIAVE 2026-07-19:** (1) **Coppie: pitch 72.0 Nm / roll 66.1 Nm puri a neutro, accoppiati come diamante `|t_pitch|/72 + |t_roll|/66 <= 1`** (non un box!). URDF corretto: effort roll era 36 Nm a occhio, il valore derivato e' **66 Nm** (era 1.8x troppo conservativo); pitch 72 era giusto. (2) **La coppia pitch DEGRADA in plantarflessione: 72 Nm a neutro -> 66.8 a -15° (toe-off tipico) -> 46.0 a -50°.** Il fabbisogno stimato in push-off a 45 kg e' ~67 Nm: **siamo esattamente al limite**, comodi a 35-40 kg, margine zero a 45 kg. NON toccare il CAD ora: misurare la domanda reale in Isaac (stessa filosofia del gate hip yaw); se satura, la correzione e' una **manovella piu' corta** (40 mm -> 86 Nm) al costo di velocita' caviglia e forza puntone (754 N -> 900 N, KARM-08 CL regge 1.7 kN breve). (3) **Continuo 22 Nm pitch / 20.2 roll**: implica CoM in stazionamento entro ~50 mm dall'asse caviglia, altrimenti problema termico (CoM a 90 mm chiederebbe 40 Nm continui) -> aggiungere termine di reward che tiene il CoP a meta' piede. (4) **ROD-END: allarme rientrato.** Disallineamento per-estremita' peggiore su tutto il workspace = **15.7°** (a roll max) contro i **35°** degli igus KARM/KALM-08 CL; il pitch costa ~0° (rotazione attorno al perno). Quindi il vecchio piano di limitare il roll a ±12° e le vie di upgrade spaziatori conici/ball-stud NON servono: ±15° di roll pieni sono OK. (5) Zero pose irraggiungibili e nessuna singolarita' nel range.
> - **POLICY TRAINATA "SUPER ROTTA" — HANDOFF DEBUG AL PC ISAAC — 2026-07-19:** utente ha allenato una policy su `rl_full.urdf`, risultato rotto; causa non ancora isolata (mirroring? PD/reward/training-side? collision mancanti su braccia? velocity/effort provvisori?). Scritto `MIRROR_DEBUG_HANDOFF.md` (repo + copiato in `~/Downloads/rl_full/`, dentro il nuovo zip `rl_full_isaac.zip`) per l'istanza AI sul PC Isaac: riassume cosa e' GIA' verificato indipendentemente (simmetria 0.000 mm su 13 coppie, convenzione assi "stesso comando = moto specchiato + limiti identici", COM y=0.1mm, catena connessa) cosi' da non ri-derivare tutto da zero, elenca i valori PROVVISORI reali sospetti (tutte le velocity, sforzo caviglia 72/36 Nm, limiti collo, hip yaw 36 Nm RS06 vs gate RS03), i gap noti (niente collision su braccia/polsi, collision piedi = mesh visiva intera non primitiva) e un ordine di debug a step con i 4 test di accettazione di `ISAAC_HANDOFF.md`. Messaggio chiave per l'altra istanza: se i test 1-2 passano ma solo la policy allenata e' rotta, il problema e' quasi certamente reward/PD/action-space lato Isaac Lab, NON il mirroring — non ripartire dall'audit geometria gia' verificato. `mirror_urdf.py` copiato nello zip cosi' l'altra istanza ha il sorgente diretto senza dover chiedere copia-incolla.
> - **URDF COMPLETO PRONTO PER ISAAC + SECONDO AI SUL PC ISAAC — 2026-07-18 (pomeriggio):** `mirror_urdf.py` ora e' completamente automatico e robusto: (1) auto-match dei giunti per POSIZIONE mondo (REF_POS, tolleranza 40 mm — immune a rinumerazioni/rinomini dell'exporter); (2) auto-derivazione dei sottoalberi da specchiare con esclusione dei rami centrali (Thor/WEHO sotto lo statore spalla); (3) AUTO-RIPARAZIONE gamba appesa: l'exporter Onshape perde un edge dei Group mate (il CAD e' corretto!) e appende la gamba al mondo con catena invertita — lo script la ri-radica (pitch->roll->yaw) e la riaggancia alla pelvi dalle pose mondo preservate, con warning; (4) masse iniettate per token nel nome (rs04/rs03/rs06/rs00/rs05/rh56/d435/battery/thor/weho/eaton/lev100/imu — i rename utente in Onshape hanno identificato tutta l'elettronica in CAD); l'override di massa del pannello Properties Onshape NON viene esportato: mai fidarsi, le masse le mette lo script; (5) floor di sicurezza 0.05 kg sui link mobili <5 g; (6) collisioni token-based (15 corpi: pelvi/ribcage/piedi/gamba). VERIFICATO: 30 revolute, simmetria 0.000 mm su 13 coppie, massa totale 32.25 kg, catena anca corretta. Output `~/Downloads/rl_full/` + `ISAAC_HANDOFF.md` (anche nel repo) + zip `rl_full_isaac.zip` per il PC Isaac (secondo AI attivo li', monitorato via AnyDesk; le sessioni NON si trasferiscono tra macchine: l'handoff passa da MEMORY.md + ISAAC_HANDOFF.md). Divisione dei ruoli: Mac = CAD/BOM/genera rl_full; PC Isaac = import USD + Isaac Lab + training. Il AI Isaac NON deve ripulire il raw rl.urdf (meta' robot, masse placeholder): usare SOLO rl_full.
> - **AUDIT HIP YAW RS06-vs-RS03 — 2026-07-18 (richiesto dall'utente; CAD monta RS06, mappa bloccata dice RS03):** asse verticale ≈ zero coppia gravitazionale, conta solo il picco dinamico (girata + attrito pivot piede). Stime memoria: ~28 Nm a massa classe G1, ~36 Nm a 45 kg girata aggressiva = ESATTAMENTE il picco RS06 -> zero margine (motivo dell'upgrade RS03 del 2026-06-21: 60 Nm, +0.259 kg e +Ø10 mm cad.). DECISIONE RIMANDATA AL SIM GATE (ora possibile con Isaac): URDF con effort 36 Nm (RS06 come da CAD); loggare la coppia hip-yaw in curva a ~32+ kg; se satura >2-5% dei passi ai turn-rate target -> RS03 (ordine + CAD Ø98); altrimenti si declassa la riga BOM a RS06. Nota gate scritta anche nella riga BOM RS03 hip yaw. Il gate BLOCCA l'ordine motori gambe Fase 1.
> - **MANUALI MANI INSPIRE SCARICATI E CONNESSIONE VERIFICATA — 2026-07-18:** nuova cartella `hands/` con 5 PDF ufficiali: RH56 SERIES USER MANUAL V1.0.9 (2024-01, pinout + protocollo registri/MODBUS), DEXTEROUS HANDS INSTRUCTIONS, PC INSTRUCTIONS, RH56DFTP User Manual V1.0.0 (riferimento generazione recente) e Selection Guide 2026-02. Fatti verificati: **RH56DFX = RS485/CAN, DC 24 V ±10%, quiescente 0.09 A, PICCO 2 A (conferma ufficiale DFX del budget WEHO; il "5 A" era solo raccomandazione di provisioning), 540 g.** Interfaccia dal manuale serie: UN solo connettore aviation **GX12 5 pin** per mano che porta potenza e RS485 insieme (1 GND, 2 VCC 24 V, 3 A+, 4 B−, 5 GND); RS485 default 115200 bps 8N1, protocollo registri 0xEB90 oppure MODBUS RTU, HAND_ID per mano (assegnare sx=1, dx=2), fino a 254 mani per bus. GATE: confermare all'ordine che il connettore/pinout DFX sia invariato (manuale DFX dedicato non pubblicato — chiederlo a Inspire). Schema elettrico (md+svg), note BOM mani e adattatore RS485 aggiornati con questi dati.
> - **SCHEMA ELETTRICO COMPLETO 2026-07-17:** nuovo deliverable `ELECTRICAL_SCHEME.md` (schema scritto: sorgenti, distribuzione 48 V con i 5 rami motore e i 30 attuatori, rail 24 V, catena safety, port map Thor completa, regole CAN, gate pre-cablaggio) + disegno `electrical_scheme.svg` / `electrical_scheme.png` (3 zone: POWER 48 V, SAFETY CHAIN 24 V, DATA). Aggiornare entrambi insieme alla BOM quando cambiano componenti o topologia. Totali dopo TVS qty3: EUR 30.477,03 / Fase 1 10.158,21 / massa 33,233 kg.

> **CURRENT POWER / PACKAGING LOCK — 2026-07-12 (AI + user):** [AGGIORNATO 2026-07-17: le mani sono ora COLLEGATE al rail WEHO per decisione utente — vedi blocco sopra; resta valido tutto il resto.] The active first mobile walking configuration is **no hands** and uses one `WEHO WH-C482410` sealed non-isolated 48 V -> 24 V, 10 A, 240 W converter (`74 x 74 x 32 mm`, `0.300 kg`, manufacturer-direct link: <https://www.wehopower.com/product/48v-to-24v-10a-240w-dc-to-dc-converter>). It powers Thor capped to 130 W, the powered USB hub and small interfaces only. It does **not** have enough verified power margin for Thor plus two RH56DFX hands. Bench validation is mandatory: Thor boot transient, sustained GPU load, converter thermal rise, 24 V ripple and EMI. WEHO requires an external low-ESR capacitor >=22 uF at its output; have an electrical engineer select/mount it at the converter output.
>
> - [SUPERATO 2026-07-17: mani, scheda dual-RS485 e cavo USB-C-B sono di nuovo ATTIVI qty1 sul rail WEHO — vedi blocco in testa.] Hands `RH56DFX-2L/R`, Waveshare dual-RS485 board and its USB-C-to-B cable were **deferred qty0** in the BOM on 2026-07-12.
> - `Cincon CHB350-48S24` + `UHG-PWR-001` are **qty0 alternatives**, not active: very compact but require a properly designed/released carrier PCB. The off-the-shelf no-custom-PCB fallback is `MEAN WELL RSD-300C-24`, `216 x 96.5 x 40 mm`, `1.19 kg`; it supports later hands but has a severe rear-torso packaging penalty. Do not widen the torso for it unless hands are required.
> - Front electrical bay `100 x 100 x 90 mm`: reserve it only for the 48 V motor switch/precharge/PDU, not Thor or WEHO. One `TE LEV100A5ANG` (CAD reserve `50 x 50 x 60 mm`, 0.190 kg), **one** `Eaton Bussmann 16220-2` (`76.2 x 50.8 x 25.4 mm`, 0.151 kg), `Vishay RHA050100R0FE02` (mounting envelope `70.6 x 21.4 x 16 mm`, 0.050 kg), `CIT A2K1CSQ24VDC1.6` (`26.5 x 32 x 33.5 mm`, 0.040 kg), and the main `Littelfuse BF1 70A + 04980921GXM5 holder` belong there. Exactly **one** Eaton block is needed. Put the five motor-branch fuse holders at cable exits/on a removable rear or underside panel, not all in the 100 mm cube. E-stop is externally accessible.
> - Topology: `battery -> 70A main fuse -> split`; protected **unswitched** branch -> WEHO -> 24 V fuses -> Thor/hub; **switched** branch -> precharge resistor/relay -> LEV100 -> one Eaton block -> motor branch fuses -> harnesses. E-stop interrupts the LEV100 coil independently of Thor; Thor stays live to log the event.
> - New concise build document: `README.md`. `MEMORY.md` remains the agent handoff/source-of-truth.
> - Screw/CAD mass correction: ISO 4762 standard lengths selected: `M3x10` (8 installed), `M3x15` (184), `M4x15` (201), `M4x20` (12); M3x20, M4x10 and M4x25 remain catalogue qty0. Fractional `7.5/12.5/17.5/22.5 mm` lengths are not normal ISO stock and are intentionally not listed. Motor assembly masses, including only the stated screws: RS06 `0.642930 kg`; RS04 `1.452625 kg`; RS03 `0.912625 kg` (uses the 0.880 kg manual base); RS00 `0.323320 kg`; RS05 `0.211620 kg`. Screw purchase rows deliberately have no BOM mass to avoid double counting.
> - Pushrod mass correction: the 40 mm and 140 mm links are no longer identical. Pending a scale measurement of the delivered AliExpress part, BOM CAD body estimates assume a 6061-class aluminium tube OD12/ID8: `6.8 g` for 40 mm and `23.8 g` for 140 mm, each excluding separately listed igubal ends/jam nuts. Replace these values after verifying delivered tube geometry and advertised length definition.

> **TABELLE SPEC MOTORI (scannabili) = file separato `MOTORI_TABELLE.md`** (Encos planetari+armonici, RobStride, ZeroErr, CubeMars, Steadywin, Dynamixel, Damiao, opzioni sensori). Da aggiornare insieme a questa memoria quando si trovano spec nuove.

> **CURRENT ACTUATOR DECISION 2026-06-20: QDD architecture, RobStride supplier. Unitree G1 is the actual reference; K-Scale K-Bot is observation only.**
> The previous CubeMars choice was based on a dimensional error. `AK70-9` is **Ø89 x 49 mm**, not Ø70; `AKE90-8` is **Ø107.5 x 43.5 mm**, not Ø90. CubeMars therefore has no decisive diameter advantage over RS06/RS04 for this robot. RobStride is retained because dimensions and torque class are comparable, price is lower, and its data are already in the CAD/BOM workflow.
> **BALANCED ACTUATOR MAP LOCKED / CURRENT 2026-06-21 (30 actuators):** `RS04 x6` = hip pitch/roll + knees; `RS03 x3` = hip yaw x2 + waist roll x1; `RS06 x11` = ankle A/B drives x4 + waist yaw x1 + shoulder pitch/roll x4 + elbows x2; `RS00 x8` = shoulder yaw x2 + wrists x6; `RS05 x2` = neck pan/tilt. Waist has roll + yaw and **no waist pitch**; as of 2026-06-27 CAD order is **waist roll below waist yaw**. Sagittal torso motion is produced by hip pitch.
> Selected actuator mass is approximately `20.913 kg`. This is the current RobStride BOM map; do not reintroduce the older `RS06 x13 / RS03 x1` map.
> RobStride and CubeMars are outer-rotor low-reduction QDD actuators. Unitree G1 remains the geometry and power baseline even though its internal motor construction is not being copied literally.
>
> **ELECTRONICS / THOR / IMU UPDATE 2026-07-12 (SUPERSEDES OLDER ELECTRONICS NOTES):**
> - The project is open source and must be reproducible by universities and makers. Prefer exact, orderable components with public dimensions and Linux support; do not require a component merely because another open robot used it.
> - Initial onboard controller is **one NVIDIA Jetson AGX Thor Developer Kit only**. RobStride actuators already contain the FOC driver and local current/position/velocity loops, so there are no 30 external motor drivers and Thor must not recreate the 10-40 kHz FOC loop. Thor runs perception, state estimation, policy and a high-priority `250 Hz` target-refresh process. Use PREEMPT_RT, CPU affinity/priority and SocketCAN. A separate low-level computer remains qty 0 and is added only if measured latency/jitter or USB-CAN reliability fails.
> - Thor developer-kit envelope is `243.19 x 112.40 x 56.88 mm`, about `1.94 kg`; reserve at least `255 x 125 x 72 mm` including cables and airflow. Set a `<=130 W` nvpmodel. Thor is the dominant unavoidable backpack dimension.
> - Five physical RobStride CAN 2.0B buses at `1 Mbps`: Thor native CAN0 = left leg (6), native CAN1 = right leg (6), three exact isolated `MKS CANable Pro` STM32F072/candleLight interfaces = left arm (7), right arm (7), waist+neck (4). Use exactly two `120 ohm` terminations per bus (`10` total), bus topology and short stubs. Do not substitute the unsupported STM32G431 MKS V2.0 silently. At 250 Hz command+feedback the conservative estimated loads are about 45%/45%/53%/53%/30%.
> - RobStride CAN timeout protection is documented but disabled at `CAN_TIMEOUT=0` by default. Set a nonzero timeout on every actuator and bench-test the resulting safe stop; the manual example `20000` corresponds to about `1 s`. A CAN timeout is not a substitute for the hardwired e-stop.
> - **Strict-minimum onboard power architecture, 2026-07-12:** `13S battery -> 70 A BF1 main fuse`; from there the two compact 24 V converter inputs remain available for compute, while the motor path goes through precharge and one exact `TE Connectivity KILOVAC LEV100A5ANG / 9-1618389-8` contactor, then one `Eaton Bussmann 16220-2` block and five branch fuses. The latching e-stop directly interrupts the LEV100 24 V coil independently of Thor. Exact LEV envelope: body Ø39.5 mm, flange width 46.3 mm, height 57.96 mm, mass 0.190 kg.
> - Removed from the active onboard BOM: Albright SW80, ED250 manual disconnect, Mean Well RSD-500C-24, second Eaton block, DIN timer, key selector, Omron hand relay, external 12,000 uF capacitors, and the ODrive Regen Clamp/plate/resistor assembly. The XT90-S battery connector is the physical service disconnect and must only be separated with the robot stopped and LEV100 open. Ground-only equipment includes the RSP-3000 bench supply, battery charger, debug PC and tools.
> - **Power correction 2026-07-12:** use one `Cincon CHB350-48S24`, exact 36-75 V input / 24 V 14.6 A / 350 W half-brick, `61.0 x 57.9 x 13.2 mm`, for Thor, both RH56DFX hands and interfaces. Thor should use its locking Micro-Fit 9-28 V input, not USB-C PD. At 130 W Thor is about 5.4 A on 24 V; the hands document 2 A maximum each. Bench-test Thor transient current and converter temperature. `UHG-PWR-001` is not a purchasable SKU: it is a required **to-design** small carrier PCB, reserve `90 x 85 x 30 mm`, mass budget `0.150 kg`, containing manufacturer-required capacitors/filtering, fuse interfaces, connectors, coil suppression, heat spreading and mechanical support. Do not represent it as purchase-ready until schematic, exact component BOM and thermal/creepage review exist.
> - **Power/packaging alternatives 2026-07-12, not yet final BOM lock:** (A) `MEAN WELL RSD-300C-24`, enclosed 24 V / 12.5 A / 300 W, 33.6-62.4 V input, `216 x 96.5 x 40 mm`, 1.19 kg. No custom PCB, can support Thor plus both RH56DFX hands in normal operation, but requires realistic rear width about 225 mm beside Thor (bare widths 112 + 96.5 = 208.5 mm). (B) compact enclosed `WEHO WH-C482410`, 30-60 V -> 24 V / 10 A / 240 W, `74 x 74 x 32 mm`, about 300 g, claimed sealed/non-isolated. Its stated range covers 13S 42-54.6 V and it is electrically suitable for Thor alone at 130 W plus interfaces; it gives a narrow back module about 200-205 mm wide beside Thor. It is **not** sufficient for Thor at 130 W plus two RH56DFX hands at their documented 2 A maxima: approximately 241 W with interfaces exceeds 240 W. It may work with Thor capped 90-100 W plus hands only after current/thermal/EMI bench validation. WEHO is a manufacturer-direct generic converter, less traceable/confident than Mean Well; treat it as a prototype candidate, not proven infrastructure. (C) Cincon plus custom carrier is compact and has full 350 W margin but needs electrical design. User prefers not to widen torso unless strictly necessary. Current recommended first walking iteration: no hands, WEHO candidate after bench validation; add hands later or move to Cincon/Mean Well choice.
> - Regen hardware is now qty 0 to meet the strict compact baseline, not because regen risk vanished. Before dynamic walking, confirm the battery BMS accepts regenerative charge, avoid full-SOC dynamic tests, and scope the motor bus. Reactivate/resize a clamp only if measurements require it. External bulk capacitors remain measurement-only qty 0.
> - USB compacted 2026-07-12: D436 directly to one Thor USB-A port; exact powered `Waveshare USB3.2-Gen1-HUB-4U`, SKU 27837, on the second USB-A. The hub is only `86.0 x 47.8 x 27.6 mm`, USD 17.99, accepts `7-36 VDC` and serves exactly three USB-CAN adapters + the pelvis IMU. The dual RS485 hand adapter connects directly to a host-capable Thor USB-C through exact `LINDY 36940`, USB-C to USB-B, 0.5 m. This supersedes the `139 x 69 x 25 mm`, EUR 105 DIGITUS seven-port hub. Keep camera bandwidth off the hub. Separate USB/data and CAN harnesses from high-current cables, add grommets, strain relief and service loops.
> - Packaging correction: the proposed internal electronics bay may be `100 x 100 x 90 mm` only if moving neck yaw out of the ribcage creates it. It fits the Cincon carrier, LEV100, precharge parts, one Eaton block and interfaces, but **cannot fit Thor** (`243.19 x 112.40 x 56.88 mm`). Reserve a separate ventilated outer rear shell/backpack for Thor of at least `125 W x 255 H x 75 D mm` if oriented vertically; allow cable and airflow space. CAD must make a component-level layout before declaring fit.
> - **Harness update 2026-07-12:** a new BOM section `5A - MOTOR HARNESS / CAN BUS` contains exact Seeed `BCCA4011 / SKU 100066605` reference lead and explicit qty0 manufacturing deliverables: left/right arm trunk, waist/neck trunk, inline CAN/power branch junction, RS03/RS04 custom harness set, strain-relief/grommet plan and final motor connector/CAN-ID map. Do not guess cut lengths: use CAD centreline length + 10% service slack + connector bend allowance, then freeze a drawing containing every connector/pin/wire gauge/branch/fuse/CAN ID/termination endpoint before buying cut-to-length harnesses. BCCA4011 is a 300 mm 16AWG power + 26AWG signal combined lead and must be physically verified against RobStride connector gender/keying.
> - **Audio selection 2026-07-12:** baseline basic voice I/O is exact `Waveshare USB TO AUDIO / SKU 18833` plus `PUI Audio AS03604AR` bare 36 mm / 4 ohm / 3 W speaker. Waveshare is USB/Linux driver-free, includes basic microphone and a PH2.0 speaker output rated 2.6 W/channel at 4 ohm. It uses Thor USB-C #2 through exact `LINDY 41899` USB-C male to USB-A female adapter; port map remains: USB-A#1 D436, USB-A#2 4-port hub (three CANable + IMU), USB-C#1 dual RS485 hands, USB-C#2 audio, debug USB-C recovery only. Speaker has no mounting holes: `AUD-MNT-01` visible BOM design deliverable specifies a printed pocket/retaining ring/grille, 1 mm diaphragm clearance, shallow rear cavity and strain-relieved wire exit. This baseline does not have far-field mic-array/AEC quality: begin with push-to-talk/half duplex. Possible later upgrade is Seeed ReSpeaker XVF3800 4-mic array (USB/Linux, AEC/beamforming/DoA) after its speaker output path is selected.
> - Selected pelvis IMU is **Phidgets MOT0110_0 PhidgetSpatial Precision 3/3/3**, exact enclosed size `38.989 x 37.846 x 13.380 mm`, CAD mass `0.030 kg`, USB/Linux Phidget22, synchronized timestamps, up to `1 kHz`, accelerometer `+/-16 g`, gyro `+/-2000 deg/s`, magnetometer `+/-8 G`. Exact short cable is `CBL4011_0`, USB-A to right-angle Mini-B, `280 mm`. Mount rigidly on the pelvis below the articulated waist, document axes, and isolate structurally from cable pull. Use gyro+accelerometer for locomotion; magnetic yaw near QDD motors/high-current wiring is untrusted until in-situ calibration. The D436 head IMU is not a pelvis-IMU substitute because the neck moves.
> - Isaac Sim/Isaac Lab work can begin now, but train on a desktop/workstation GPU rather than Thor. Gate before RL: one rigid link per body, correct revolute axes/limits/zero pose, measured masses/inertias, simplified collision meshes, foot friction and selected self-collisions, actuator torque/speed/sign limits, and stable standing PD. The offset ankle gimbal is two serial revolute joints (pitch above roll), not a ball joint. For the first URDF/RL model use virtual ankle pitch/roll joints with the real axis offset; omit the closed pushrod loop from dynamics or keep it visual-only, then apply the measured motor-to-joint differential/Jacobian map and domain randomization later.
> - The BOM “purchased onboard mass” excludes the 4 kg bench supply but conservatively counts full purchased cable lengths. It is therefore not the final CAD mass; replace cable rows with installed lengths after harness routing.
>
> **CAMERA, HANDS AND BATTERY UPDATE 2026-07-11 (AI + user; shared handoff for AI):**
> - Camera selected: `RealSense D436`, SKU `99CWHP`, `90 x 25 x 25 mm`, `75 g`, global-shutter stereo depth + global-shutter RGB + IMU. The official D400 CAD archive does not yet contain D436; use the same-envelope D435i CAD provisionally and verify the physical camera before releasing the bracket.
> - Hands selected: `Inspire RH56DFX-2L` + `RH56DFX-2R`, **without Inspire wrist** because the robot already has RS00 3-axis wrists. Each hand is `540 g`, `217.8 mm` long, about `80.7 mm` palm width, 6 actuators / 12 moving joints, `24 V`, RS485. Cleaned one-file visual meshes for Onshape are `cad_reference/RH56DFX-2L_reference.stl` and `cad_reference/RH56DFX-2R_reference.stl`; they are packaging meshes, not watertight manufacturing solids. Their dedicated `CHB300W-48S24` rail is disabled through hardware remote-on/off during e-stop; no separate Omron relay. Communication remains one isolated two-channel Waveshare USB-RS485 adapter.
> - **Battery superseded again 2026-07-11 after the user rejected the Tattu envelope as too large.** Current CAD/procurement baseline is the commercial Bicycle Motor Works `48 V 9 Ah Molicel P45B` pack: `13S2P`, `46.8 V` nominal / `54.6 V` full, exactly `421.2 Wh` like G1, integrated BMS `45 A continuous / 100 A maximum`, XT90-S discharge, XT60 charge, published `165.1 x 101.6 x 76.2 mm`. Published mass is “under 5 lb”; use conservative `2.27 kg` until the supplier gives the exact finished mass. This is smaller than the G1 battery (`182 x 120 x 80 mm`) in every oriented dimension. CAD reserve `170 x 106 x 81 mm` plus `35-50 mm` cable bend at the connector face. ORDER GATE: confirm Italy lithium shipment, exact mass, duration of the 100 A rating, BMS trip curve, short-circuit current, regen charge-current limit, charger and lead lengths. The original Unitree G1 battery remains unsuitable because its load detection prevents generic standalone power-on. The previous Tattu and 25 Ah ENERprof selections are superseded.
> - EU fallback: Tõuksi Vabrik in Estonia publishes the same `13S2P / P45B / 9 Ah / 421.2 Wh` architecture with a `60 A BMS`, `2.04 kg` and EUR 416 VAT included. It is qty 0 until they provide a drawing and guarantee a finished envelope no larger than about `165 x 102 x 76 mm`; use it if Bicycle Motor Works cannot legally ship to Italy.
> - Secondary EU softpack fallback is Dan-Tech `13S2P 48 V 10 Ah 60 A`, `280 x 35 x 130 mm`, `2.2 kg`, EUR 347 VAT included. It remains qty 0 because it is longer than desired and its page contradicts itself: the selected configuration says `No BMS`, while the feature list claims full BMS/CAN/RS485/UART protection.
> **2026-06-21 — CubeMars 36:1 (AK45-36, Ø55x54, 24/8 Nm) EVALUATED and REJECTED. STAY ALL-QDD, no high-reduction anywhere.** User's 3 questions settled it: (1) QDD is more FUTUREPROOF — 36:1 permanently closes force/impedance control + compliance + impact tolerance on that joint (hardware life sentence, not sw-upgradeable). (2) 36:1 is WORST on the ANKLE (contact joint, wants compliance most) -> keep ankle QDD. (3) On the arms 36:1 helps only today's position-based ACT/diffusion, but kills future contact-rich/compliant manipulation. User values futureproofing -> all-QDD. Chunky Ø88 arms/ankle = cosmetic + ~2.5 kg, does NOT cap capability; 36:1 does. RobStride QDD map (AI lock) STANDS; CubeMars-QDD AKE90 only if stronger legs wanted (170 vs 120 Nm, same Ø). AI over-sold AK45-36 the prior turn; user correctly pushed back.
> **2026-06-21 — REAL PROJECTED MASS ≈ 45 kg, HEIGHT ≈ 1.40 m (user's numbers, agreed). SIZE AGAINST THESE, not the old 35 kg / 1.2 m.** Why heavier than G1's 35 kg: RobStride ≈ 84 Nm/kg (RS04) vs Unitree custom ≈ 189 Nm/kg, so ~2× actuator mass per Nm. 20.35 kg motors + structure + on-board battery + push-rod/shaft/bearing hardware -> 40–45 kg; budget the top. Height rises to ~1.40 m partly from the 2× Ø88 ankle stack lengthening the shin.
> **TORQUE re-scaled (first-pass rules of thumb, ±25%, NO CAD mass model yet — re-validate after CAD):** 35->45 kg (×1.29) and 1.2->1.4 m (longer levers, ×~1.17) push proximal-joint torque ~1.3–1.5× above the old estimates. Binding joints @45 kg/1.4 m (hold/peak Nm vs motor rated/peak):
>   - Ankle pitch: ~40 / **~67** push-off vs RS06 11/36 -> **needs ~1.9:1 push-rod leverage** (was 1.45). MANDATORY. Less leverage = flat-foot ZMP only, no energetic toe-off.
>   - Ankle roll: ~20 / ~24 vs RS06 11/36 -> OK; **RS02 (17) now too small, do NOT shrink ankle roll.**
>   - Knee: ~43 / ~53 vs RS04 40/120 -> peak fine; **continuous ~43 ≈ rated 40** -> marginal for SUSTAINED deep-knee holds.
>   - Hip roll: ~41 / ~50 vs RS04 40/120 -> peak fine; **continuous ~41 ≈ rated 40** -> marginal for PROLONGED single-leg stance.
>   - Hip pitch: ~35 / ~78 vs RS04 40/120 -> OK. Shoulder pitch/roll: sustained arm+payload-out ~22 Nm > RS06 rated 11 -> go **RS03** only if sustained extended-load holds are required; else RS06 ok for motion.
> **CONSEQUENCE: RS04 legs are now RIGHT-sized, NOT oversized — RETRACT the earlier "shrink legs to RS03" idea; keep RS04.** Only safe shrink left = **wrists RS00 -> RS05** (~0.7 kg). Robot WALKS fine: walking single-support is brief/dynamic, lives in PEAK numbers (RS04 120 ≫ 78); only SUSTAINED static high-torque poses (long single-leg, deep squat, payload at arm's length) are thermally marginal.
> **Roll < Pitch at the ankle CONFIRMED (physics):** pitch CoP travels the foot LENGTH (half ~0.10 m) + has push-off (1.5 Nm/kg); roll CoP travels the foot WIDTH (half ~0.045 m, ~2.2× shorter lever) and has NO sideways push-off. Heavy lateral balance in single-support is the HIP roll (RS04), not the ankle. -> in the 2-push-rod ankle the PITCH rod can carry MORE leverage than the ROLL rod (need not be symmetric even with 2× RS06).
> **ANKLE ARCH (corrected by user 2026-06-21): DIFFERENTIAL / parallel, NOT serial.** 2 push-rods from 2 shin motors to the SAME shaft on the foot: both push/pull = PITCH, opposed = ROLL (sum=pitch, diff=roll). Both motors drive BOTH DOFs. Map = clean sum/diff mix (m1 = pitch/2k + roll/2k', m2 = pitch/2k - roll/2k') + geometric corrections; RL trains in (pitch,roll), the map converts at deploy. **BONUS: pitch = SUM of both motors -> up to ~72 Nm (2× RS06) -> covers the 45 kg push-off (~67 Nm) with NO leverage; flat-foot now, push-off-capable later.** Diamond torque envelope (can't max pitch+roll simultaneously; fine in practice). Body weight rides a CENTRAL 2-DOF pivot; rods carry only torque. (My earlier serial/"triangular" description was WRONG.)
> **2026-06-21 — HIP YAW upgraded RS06 -> RS03 (user).** Reason: at 45 kg projected mass the aggressive-turn peak (~36 Nm) sat exactly at RS06's 36 Nm limit; RS03 = 60 Nm peak gives headroom for snappy turns (gravity-free axis, so only peak matters). **NEW LOCKED MAP (30): RS04 x6** (hip pitch/roll + knees) | **RS03 x3** (waist roll x1 + hip yaw x2) | **RS06 x11** (ankle pitch/roll x4, waist yaw x1, shoulder pitch/roll x4, elbows x2) | **RS00 x8** (shoulder yaw x2 + wrists x6) | **RS05 x2** (neck). New actuator mass ≈ **20.913 kg** (+0.558 vs 20.355). RS03 body drawing from the RobStride 2025-06-26 PDF is OD 98 x length 54.1 mm; RS04 is OD 120 x length 56 mm; RS06 OD 88 x 49 mm; RS00 OD 57 x 51 mm; RS05 OD 46 x 44 mm. BOM Excel re-synced 2026-06-27.
>
> **ROBSTRIDE vs CUBEMARS CONTENDERS BY TORQUE CLASS (2026-06-23, comparison only, NOT a BOM switch).** `Height`
> means actuator axial thickness. Use real outer actuator dimensions, not model names (`AK70` is not Ø70; `AKE90` is
> not Ø90). CubeMars `AKE` motors may require external driver packaging; RobStride modules are integrated.
>
> | Torque class / project use | RobStride contender | RobStride dimensions / mass / torque | CubeMars contender | CubeMars dimensions / mass / torque | Verdict |
> |---|---|---|---|---|---|
> | ~5 Nm, neck | `RS05` | Ø46 x 44 mm, 191 g, 5.5 peak / 1.6 rated Nm | `AK40-10` | Ø53 x 37 mm, 185 g, 4.1 peak / 1.3 rated Nm | Keep `RS05`: smaller diameter and stronger; CubeMars only thinner. |
> | ~10-15 Nm, wrists + shoulder yaw | `RS00` | Ø57 x 51 mm, 310 g, 14 peak / 5 rated Nm | `AKE60-8` or `AK45-10` | `AKE60-8`: Ø69 x 25 mm, 260 g, 12.5 / 5 Nm. `AK45-10`: Ø53 x 43 mm, 260 g, 7 / 2.5 Nm | `RS00` remains simplest and smaller than AKE in diameter. `AKE60-8` is attractive only if axial thickness is the binding CAD problem; `AK45-10` is too weak for the same class. |
> | ~25-36 Nm, ankles + shoulder pitch/roll + elbows | `RS06` | Ø88 x 49 mm, 621 g, 36 peak / 11 rated Nm | `AK70-9 V3.0` or `AKE80-8` | `AK70-9`: Ø89 x 49 mm, 540 g, 29.2 / 8.5 Nm. `AKE80-8`: Ø87 x 32 mm, 570 g, 30 / 12 Nm | No strong CubeMars win. `AK70-9` is same size but weaker; `AKE80-8` is thinner but external-driver and still weaker peak. |
> | ~50-60 Nm, hip yaw + waist roll | `RS03` | Ø98 x 54.1 mm body, 900 g, 60 peak / 20 rated Nm | `AK10-9 V3.0` | Ø98 x 61.7 mm, 940 g, 53 peak / 18 rated Nm | `RS03` wins on same diameter, lower mass, shorter length and more torque. |
> | ~120-170 Nm, hip pitch/roll + knee | `RS04` | Ø106 face / about Ø120 envelope x about 56 mm, 1420 g, 120 peak / 40 rated Nm | `AKE90-8` | Ø107.5 x 43.5 mm, 1400 g, 170 peak / 55 rated Nm | Only serious CubeMars upgrade: same weight/diameter class, thinner and much stronger. Tradeoff = external driver + mixed software/spares. |
>
> Ranking summary: diameter smallest->largest = `RS05` 46 < `AK40/AK45` 53 < `RS00` 57 < `AKE60` 69 < `AK60-6` 79
> < `AKE80` 87 < `RS06` 88 < `AK70-9` 89 < `RS03/AK10/AK80` 98 < `RS04/AKE90` ~106-120. Weight smallest->largest =
> `AK40` 185g ~= `RS05` 191g < `AK45/AKE60` 260g < `RS00` 310g < `AK60-6` 380g < `AK80-9` 490g < `AK70-9`
> 540g < `AKE80` 570g < `RS06` 621g < `RS03` 900g < `AK10` 940g < `AKE90` 1400g ~= `RS04` 1420g.

> **SPECIFIC-TORQUE AUDIT 2026-06-20.** Formula: `specific torque [Nm/kg] = output torque [Nm] / complete actuator mass [kg]`. The stated major-joint target `>10 Nm/kg` normally uses peak torque. Rated values are also recorded as a conservative thermal check. Source: official RobStride Product Specification 2025-06-26.
>
> | Model | Peak / rated Nm | Mass kg | Peak Nm/kg | Rated Nm/kg | Result |
> |---|---:|---:|---:|---:|---|
> | RS04 | 120 / 40 | 1.420 | 84.5 | 28.2 | PASS peak and rated |
> | RS03 | 60 / 20 | 0.900 | 66.7 | 22.2 | PASS peak and rated; reserve, not selected |
> | RS06 | 36 / 11 | 0.621 | 58.0 | 17.7 | PASS peak and rated |
> | RS00 | 14 / 5 | 0.310 | 45.2 | 16.1 | PASS peak and rated |
> | RS05 | 5.5 / 1.6 | 0.191 | 28.8 | 8.4 | PASS peak; FAIL rated, neck only and not a major load-bearing joint |
>
> All selected models meet the quoted target on the usual peak basis. RS05 must not be promoted to a continuous major-joint role based on this metric.
>
> **Torque rationale for balanced substitutions:** hip yaw and waist yaw remain RS06 because gravity torque is approximately zero and the estimated aggressive dynamic demand near G1 mass is about `28 Nm < 36 Nm peak`; this becomes borderline if the finished robot approaches `46 kg`. Waist roll remains RS03 because an estimated `12-17 Nm` continuous demand at 30 degrees fits its `20 Nm rated`, while RS06 has only `11 Nm rated`. Shoulder yaw uses RS00: at the approximately `0.24 m` G1 shoulder-yaw-to-palm lever it supplies about `21 N/hand` rated and `58 N/hand` peak, sufficient for roughly a 1 kg box with friction and safety margin. Elbows stay RS06 because RS00 would be near rated torque with a 1 kg payload.
>
> **ACTUATOR-MODEL AUDIT 2026-06-21, against MIT Humanoid paper `sources/2104.09025v1.pdf`:** the MIT flips/spins are strictly simulation results, but the actuator hardware tests are real. MIT used a custom dynamometer with a FUTEK TRS300 torque sensor to measure current-vs-output-torque and the 60 V torque-speed envelope; an impedance analyzer for resistance/inductance; measured battery impedance for voltage sag; and included output/rotor inertia plus estimated friction and damping in simulation. RobStride's local manuals/specification provide mass, ratio, rated/peak torque, current limits, scalar torque constant, back-EMF, line resistance, scalar inductance, 48 V torque-speed plots, overload-duration plots, temperature limits, dual encoders, FOC/MIT/current modes and CAN telemetry. They do **not** provide output/reflected rotor inertia, friction/stiction maps, damping, backlash/compliance/gear efficiency, current-loop bandwidth, guaranteed command-to-torque latency, a full thermal RC model, battery/bus sag, or raw numerical curve data. Active reporting is documented down to 10 ms (100 Hz), but this is not a guaranteed internal-control or request-response bandwidth.
> Documentation inconsistencies must be bench-resolved: RS03 mass is `880 g +/-20 g` in its later user manual but `900 g +/-20 g` in the 2025-06-26 family specification; RS00 rated speed is `260 rpm` in its later manual but `100 rpm` in the family specification. RS04 has no separate local user manual, only the family sheet.
> **Required test level:** calm first walking can begin with conservative datasheet limits plus domain randomization; do not wait for an MIT-grade dynamometer. Before serious sim-to-real tuning, identify one sample per load-bearing model in priority order `RS04 -> RS06 -> RS03`: output torque versus reported `Iq` in both directions, breakaway/Coulomb/viscous friction versus speed and temperature, command/feedback latency and frequency response, effective output inertia, thermal derating, and bus-voltage sag. RS00/RS05 can be characterized later. Full high-speed torque-speed dynamometer testing is required only before acrobatics or planning close to actuator limits. Never assume the plotted datasheet curves constitute a complete validated actuator model.
>
> **ACTUATOR-ARCHITECTURE CHECK AGAINST FIRGELLI GUIDE 2026-06-20.** The guide does not invalidate QDD for this project: it explicitly places Unitree G1/H1 in the QDD class and reserves harmonic + planetary-roller-screw systems mainly for high-payload continuous-duty factory humanoids. Important correction to its loose wording: a planetary roller screw is resistant to impact because line contact distributes Hertzian stress; it is still a rigid, high-reduction transmission and does not inherently absorb impact energy. True passive absorption requires a separate compliant element, for example a Series Elastic Actuator spring. High-reduction harmonic actuators normally need an output torque sensor for accurate force control; this is commonly a strain-gauged flexure. A linear screw actuator analogously uses an axial force sensor/load cell, commonly strain gauges, or an SEA spring measured by encoders. These sensors are optional for position control but required for accurate output-force control when current estimation is corrupted by friction.

> **CAVIGLIA - DIREZIONE CAD CORRENTE (aggiornata 2026-06-27, SUPERA la nota Ø12 del 2026-06-21):**
> L'utente ha disegnato una soluzione a gimbal/cardano stampato 3D con due pin da 45 mm uno sopra l'altro in Z. Non e' un
> cardano matematico a centro singolo: e' un gimbal offset. Pin piu alto = pitch; pin un po' piu basso = roll. Direzione
> corrente BOM/CAD: usare shoulder screws `Ø8 mm` con filetto `M6` sia per i due assi del gimbal caviglia sia per i pivot
> dei rod-end dei puntoni. La precedente
> direzione "assi caviglia Ø12/M10 e perni puntoni Ø12" e' superata per la caviglia; resta solo nello storico. Anche il
> vecchio perno idle Ø12/M10 della waist roll e' ora disattivato qty0: non ci sono Ø12/M10 attivi nel CAD/BOM corrente.
>
> Hardware selezionato in BOM 2026-06-27:
> - First-choice shoulder screw listing: `https://it.aliexpress.com/item/1005007885495357.html`.
> - Old shoulder screw listing kept only as second source / backup: `https://it.aliexpress.com/item/1005007481484485.html`.
> - Offset-gimbal ankle axes: `2 x` shoulder screws `Ø8 x M6 x 45 mm`; upper-Z pin = pitch, lower-Z pin = roll.
> - Pushrod rod-end pivots: `4 x` shoulder screws `Ø8 x M6 x 16 mm`.
> - Retaining nuts: `6 x` M6 nuts/locknuts for the shoulder screws only; nut must clamp the shoulder stack, not crush the
>   spherical bearing. Geometry noted in BOM: M6 hex AF 10 mm, circumscribed diameter about 11.55 mm, normal locknut
>   height about 6 mm.
> - Pushrods: AliExpress adjustable aluminum M8 rods from `https://it.aliexpress.com/item/1005008935554718.html`,
>   active variants `2 x 140 mm` and `2 x 40 mm`. CAD must confirm whether advertised length is body length or eye-to-eye.
> - Pushrod rod ends: `2 x` igus `KARM-08 CL / KARM_08_CL_1` right-hand male M8 + `2 x` igus `KALM-08 CL` left-hand
>   male M8. This is for turnbuckle adjustment: rotating the aluminum rod body changes length only with RH/LH threads.
>   Availability of KALM-08 CL must be confirmed before ordering.
> - Pushrod length locknuts: `2 x` DIN 439 M8 right-hand thin jam nuts + `2 x` DIN 439 M8 left-hand thin jam nuts.
>   Standard geometry in BOM: height 4.0 mm, across flats 13 mm, circumscribed hex diameter about 15.0 mm. These are M8,
>   not M6, because they lock on the rod-end external thread.
>
> GIMBAL / CARDAN MODEL: use the real Z offset between pitch and roll pins in CAD/simulation. Do not use an ideal
> intersecting-axis Cardan map unless a later CAD revision makes the axes intersect. The offset does not add a DoF, but
> it moves the foot center slightly during combined pitch/roll and changes the motor-to-pitch/roll geometry. The current
> BOM quantities above are the user's literal current prototype quantities, not an automatically doubled full-robot estimate;
> revisit after left/right CAD is frozen.
>
> MOTORI CAVIGLIA: `RS06 x2` per leg are still the active actuator choice. Physical ankle motors are A/B differential
> drives through pushrods, not direct pitch/roll labels. Virtual pitch/roll comes from the linkage map. Keep the two
> RS06 close to the knee/proximal shin when possible; verify collisions, cable exits, crank geometry and conditioning of
> the motor-to-pitch/roll matrix in CAD.
>
> ROD-ENDS: the M8 rod ends run on Ø8 shoulders. Perfect perpendicularity of the threaded heads is not required because
> the spherical joints compensate, but the actual misalignment angle must stay inside the joint limit across the full
> ankle workspace and must not contact screws, foot or tibia. Active BOM rod ends are `2 x` igus `KARM-08 CL /
> KARM_08_CL_1` right-hand male M8 plus `2 x` igus `KALM-08 CL` left-hand male M8, both with Ø8 E10 ball bore and target
> ±35 deg pivot. KARM mass is 6.2 g each; KALM assumed same until supplier data is confirmed. Price is still `0` in the
> sheet until the exact igus cart/quote is confirmed.

> **CHIARIMENTO CHIAVE 2026-06-20 (correzione di una mia sovra-enfasi): CAMMINARE IN RL NON RICHIEDE SENSORI DI COPPIA.** Le policy RL (Unitree, ToddlerBot, ecc.) prendono in input posizioni/velocita' giunto + IMU (NON coppie), emettono target di POSIZIONE, tracciati da PD a giunto, coppia applicata OPEN-LOOP dalla corrente. Nessun sensore di coppia, su NESSUN motore. ToddlerBot lo fa con Dynamixel 288:1 (piu' rigido degli Encos) e cammina + manipola. **Quindi Encos SENZA sensori = robot valido** (controllo di posizione + RL Isaac Lab, gia' nel piano utente); l'alta riduzione e' anzi BUONA per il controllo di posizione (rigido/preciso, l'attrito lo assorbe la policy con domain randomization). I sensori di coppia servono SOLO per FORCE/IMPEDANCE control, task contact-rich, sicurezza-forza — NON per camminare. -> Encos-vs-RobStride NON e' "sensore si/no" (entrambi zero sensori per RL), ma **compatto-rigido (Encos, classe ASIMO/ToddlerBot) vs ingombrante-compliant (RobStride QDD, classe Unitree)**. Caveat scala: ToddlerBot 3.4 kg (perdona tutto), noi ~20 kg (fattibile, ASIMO a ~50 kg, ma tenere leggero/piano/gait prudente). Tutta la saga vestizione/UKF/Bota = NON necessaria per l'obiettivo "cammina calmo + task base".

## Regola di collaborazione AI

Questo progetto viene seguito alternativamente da AI quando uno dei due termina il contesto disponibile.
Questo file e l'unica fonte di verita per il passaggio di consegne: aggiornarlo a fine sessione con decisioni, modifiche,
fonti e dubbi aperti. Non ricreare un secondo file di stato. Il prossimo agente deve leggere tutto, verificare le fonti
e criticare le scelte tecniche deboli prima di aggiungere componenti o ordinare materiale.

Regola meccanica obbligatoria: non trasformare un'ipotesi in una scelta BOM. Se CAD, carichi, sedi, spessori, tolleranze
o sistema di ritegno non sono noti, lasciare la riga `DA DIMENSIONARE qty0`, elencare i dati mancanti e chiedere conferma
all'utente prima di proporre SKU, quantita o geometrie. Non dedurre dettagli costruttivi da immagini parziali.

Workspace:

```text
/Users/artes/Documents/artes/umanoide
```

Deliverable aggiornato:

```text
BOM umanoide G1 - RobStride.xlsx
```

Totali BOM verificati, IVA inclusa. ATTENZIONE 2026-07-19: i totali sono ora la SPESA RESIDUA
(Thor + entrambe le mani RH56DFX sono GIA' POSSEDUTI in laboratorio e contati a EUR 0 con prezzo
di riferimento nelle note; le FASI sono state RIDEFINITE sull'ordine di costruzione reale):

| Scope | Totale (da spendere) |
|---|---:|
| Umanoide completo (residuo) | EUR 10.264,90 |
| Fase 1 - banco braccio+mano teleop | EUR 4.008,57 |
| Fase 2 - gambe e locomozione | EUR 3.997,95 |
| Fase 3 - completamento (braccio sx, vita, collo, mobile) | EUR 2.258,38 |

(Totali Excel ricalcolati e verificati 2026-07-17 dopo la riattivazione delle mani sul rail WEHO, le nuove righe
SEQ-PWR-01/TVS 33CA/condensatore/XT90 e le correzioni di fase; la riga WEHO attiva ha prezzo 0 in attesa di quotazione.
I precedenti totali 31.243,22 / 35,043 kg erano lo snapshot 2026-07-12 di mezzogiorno con mani qty1, mai riallineato
dopo il qty0 serale.
ATTENZIONE: la massa acquistata esclude il telaio PA-CF; con circa 10 kg di telaio il robot finito puo superare
45 kg. A quella massa caviglie, knee/hip roll in continuo e waist roll vanno rivalutati dopo CAD/mass budget reale.)

Massa acquistata a bordo stimata: `33,233 kg`, escluso telaio stampato PA-CF. Di questi, i soli attuatori selezionati
pesano circa `20,913 kg`. La massa e prudente perche conta le lunghezze complete acquistate dei cavi di potenza; sostituire
con le lunghezze realmente installate dopo il routing. La bobina completa di cavo CAN da 50 m e gli elementi da banco
non sono conteggiati come massa a bordo.

Generatore:

```text
python3 build_umanoide_tab.py
```

Il generatore crea ora un workbook vergine con la sola scheda `umanoide`; non copia piu l'Excel storico in `~/Downloads`
e non genera piu schede `G1 joints CAD`, `MOTORI premium`, `MOTORI Encos (quote)` o `MOTORI RobStride`. Backup locale
pre-pulizia: `BOM umanoide G1 - RobStride.backup-before-single-sheet-20260623.xlsx`.
Aggiornamento 2026-06-26: lo stile righe e' ora guidato solo dalla colonna `Unita`: `0` = grigio automatico, quantita
diversa da zero = nero. Anche righe etichettate `[SCELTO qty0]` restano grigie finche non vengono davvero quantificate.
Aggiornamento 2026-06-27: workbook `BOM umanoide G1 - RobStride.xlsx` tradotto in inglese nella vista attiva; colonna
`Uniqueness` eliminata; intestazioni ora `Item/Supplier/Unit cost/...`; filtro Excel su `Qty != 0` (`A1:T164`) e righe
`Qty=0` nascoste automaticamente all'apertura. I link sulle righe `Qty=0` non restano blu: tutta la riga e' grigia se
viene sbloccata. Aggiornamento ulteriore 2026-06-27: rod-end caviglia ora `2 x KARM-08 CL` destra + `2 x KALM-08 CL`
sinistra, piu `4 x` controdadi sottili DIN 439 M8 per bloccare la regolazione; `6002-2RS` waist-roll bearing e il relativo `Ø12/M10` idle-side pin sono stati
disattivati qty `0` perche' appartenevano al vecchio supporto idle della vita e non servono nel CAD corrente. Le righe
storiche qty0 possono ancora contenere note miste IT/EN, ma la vista attiva filtrata e in inglese.

## Obiettivo

Costruire un umanoide stampabile in PA-CF il piu possibile, con architettura, geometrie e potenze prese dal riferimento
Unitree G1. Unitree G1 e l'unica baseline del progetto. K-Scale K-Bot non e un riferimento dimensionale o cinematico:
puo essere consultato solo come esempio open hardware secondario per packaging, producibilita e problemi pratici di
cablaggio. Non inventare simulazioni dinamiche: non sono disponibili. Prima degli acquisti servono CAD e verifiche
geometriche sui componenti reali.

## Baseline Unitree G1 ufficiale

Usare il modello G1 aggiornato `g1_29dof_mode_11`, non il vecchio `g1_29dof` marcato deprecated.

Fonti ufficiali:

- Repository e README: <https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description>
- URDF corrente: <https://github.com/unitreerobotics/unitree_ros/blob/master/robots/g1_description/g1_29dof_mode_11.urdf>
- Mesh: <https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description/meshes>
- Pagina prodotto G1: <https://www.unitree.com/g1/>
- Pagina ufficiale G1-Comp con testa 2 DOF: <https://www.unitree.com/robocup/>
- Manuale ufficiale G1-EDU Waist Fastener: <https://marketing.unitree.com/article/en/G1/Lumbar_fasteners.html>

Limiti `effort` del modello ufficiale corrente:

| Asse | Nm |
|---|---:|
| Hip pitch / roll | 139 |
| Hip yaw | 88 |
| Knee | 139 |
| Ankle pitch / roll | 35 |
| Waist yaw | 88 |
| Waist roll / pitch | 35 |
| Shoulder pitch / roll / yaw | 25 |
| Elbow | 25 |
| Wrist roll | 25 |
| Wrist pitch / yaw | 5 |

L'URDF fornisce origini dei giunti, limiti e mesh esterne. Per la caviglia descrive i due assi cinematici virtuali pitch
e roll, ma non espone il CAD interno del leveraggio. Non trattare i valori virtuali come somma banale delle coppie dei
due motori paralleli.

Lo stesso vale per la vita: la catena cinematica virtuale `yaw -> roll -> pitch` dell'URDF non dimostra che i tre
attuatori fisici siano montati in serie. La scelta CAD corrente di questo progetto e diversa dal vecchio schema a
puntoni: vita seriale diretta con `roll` sotto `yaw`, nessun waist pitch e nessun puntone vita. Il pitch del busto viene
dagli hip pitch.

Il modello `g1_29dof_mode_11` non include il collo. La pagina ufficiale G1-Comp dichiara invece `Head 2 degrees of
freedom = 2`, ma non pubblica la coppia dei due motori. Il collo di questo progetto usa quindi due RS05 come scelta
provvisoria compatta, non come equivalenza di coppia certificata Unitree.

### Posizioni esatte giunti G1 e CAD (estratti 2026-06-04)

Estratti dall'URDF ufficiale `g1_29dof_mode_11.urdf` (scaricato e salvato nel progetto). File nel workspace:
`g1_29dof_mode_11.urdf` e `g1_joints.csv` (offset relativi padre-figlio + rpy + posizioni assolute + assi + limiti).
Convenzione: X avanti, Y sinistra, Z su; origine = pelvis; mm. 29 DOF; il collo (2 DOF) NON e nel modello, va aggiunto
a parte. Usare per disegnare lo skeleton Onshape: un mate connector per giunto, nome = nome G1.

Posizioni assolute (frame pelvis, mm) - lato sinistro; destro speculare in Y:

| Giunto | x | y | z | asse | limiti rad |
|---|--:|--:|--:|---|---|
| hip_pitch | 0 | 64.4 | -102.7 | Y | -2.53..2.88 |
| hip_roll | 0 | 116.5 | -133.2 | 0.98,0,0.17 cantato | -0.52..2.97 |
| hip_yaw | 46.2 | 116.5 | -251.0 | -0.17,0,0.98 cantato | -2.76..2.76 |
| knee | 0 | 118.6 | -439.3 | Y | -0.09..2.88 |
| ankle_pitch | 0 | 118.5 | -739.3 | Y | -0.87..0.52 |
| ankle_roll | 0 | 118.5 | -756.9 | X | -0.26..0.26 |
| waist_yaw | 0 | 0 | 0 | Z | -2.62..2.62 |
| waist_roll | -4 | 0 | 44 | X | -0.52..0.52 |
| waist_pitch | -4 | 0 | 44 | Y | -0.52..0.52 |
| shoulder_pitch | 0 | 100.2 | 291.8 | 0,0.96,0.28 cantato | -3.09..2.67 |
| shoulder_roll | 0 | 140.6 | 289.0 | X | -1.59..2.25 |
| shoulder_yaw | 0 | 146.8 | 185.8 | Z | -2.62..2.62 |
| elbow | 15.8 | 146.8 | 105.2 | Y | -1.05..2.09 |
| wrist_roll | 115.8 | 148.7 | 95.2 | X | -1.97..1.97 |
| wrist_pitch | 153.8 | 148.7 | 95.2 | Y | -1.61..1.61 |
| wrist_yaw | 199.8 | 148.7 | 95.2 | Z | -1.61..1.61 |

Note: anche e spalle hanno assi CANTATI (non ortogonali); ankle pitch/roll a 17,6 mm in Z (e il cardano dei 2 perni Ø12);
waist roll e pitch coincidenti. Coppie giunto (effort URDF, Nm): hip pitch/roll 139, hip yaw 88, knee 139, ankle 35,
waist yaw 88, waist roll/pitch 35, spalla 25, gomito 25, polso roll 25, polso pitch/yaw 5. Massa totale G1 (somma link
URDF) 33,3 kg.

**Offset z hip pitch->roll (G1: ~30 mm, linea che li collega inclinata ~30 gradi verso il basso secondo calcolo
utente).** NON e lunghezza morta: e un compromesso reale.
- La coppia pitch = m*g*D*sin(theta), con D = profondita' del CoM gamba sotto l'asse pitch. L'offset fa parte di D:
  appena il pitch ruota, il blocco sotto il roll assume una quota X = offset*sin(theta) che da allineati non avrebbe
  (correzione utente: il mio "x=0 quindi non conta" valeva solo a theta=0, posa in cui la coppia e' nulla a prescindere).
- Allineare pitch/roll in z -> CoM gamba 30 mm piu' in alto -> -2,1 Nm di picco = ~10% di coppia pitch in meno
  (gamba ~7,3 kg, CoM ~305 mm sotto il pitch). Reale ma modesto (il braccio dominante e' la lunghezza gamba).
- MA allineare avvicina le carcasse: in adduzione il motore di YAW sbatte contro il PITCH a un angolo di rollio molto
  piu' piccolo -> si perde ROM in adduzione. Coi RobStride (carcasse PIU' GROSSE delle attuazioni Unitree) il problema
  peggiora. Quindi tenere lo sfalsamento G1 (o un filo di piu') e' probabilmente giusto: il ~10% di coppia pitch e' un
  prezzo basso per il ROM di rollio + niente collisione.
- DA DECIDERE in CAD con gli ingombri reali dei tre motori (pitch+roll+yaw): trovare l'offset minimo che evita la
  collisione all'adduzione massima richiesta; quello fissa anche la coppia pitch. (Posizioni esatte: utente le passera'.)

### Skeleton Onshape: coordinate CAD semplificate

Decisione CAD 2026-06-05, corretta dopo revisione utente: la scheda `G1 joints CAD` mantiene le coordinate G1 esatte e
aggiunge colonne CAD semplificate per disegnare lo skeleton in Onshape senza rumore geometrico inutile.

- `exact_x/y/z`: coordinate assolute URDF G1;
- `cad_x/y/z`: coordinate CAD primarie; `-` significa uguale alla rispettiva coordinata `exact_*`, non zero;
- `pose_down_x/y/z`: solo colonna ausiliaria per visualizzare le braccia lungo il corpo; `-` significa uguale alla posa
  CAD primaria `cad_*`.

Regola CAD primaria:

- `X`: portata a `0` quando l'URDF ha avanzamenti/arretramenti che disturbano lo skeleton;
- `Y`: nelle colonne verticali viene allineata al primo giunto alto della catena. Gamba: da `hip_roll` a `ankle_roll`
  usare la `Y` di `hip_roll`. Braccio: da `shoulder_yaw` a `wrist_yaw` usare la `Y` di `shoulder_yaw`;
- `Z`: resta la quota esatta G1 nella tabella primaria. Non abbassare `hip_yaw` e non redistribuire la sua `X` sulla `Z`;
- `axis_preciso`: non viene semplificato. Gli assi cantati restano annotati come dato URDF.

Coordinate CAD primarie lato sinistro, frame pelvis, mm. Il lato destro e speculare in `Y`.

| Giunto | x CAD | y CAD sx | z CAD | Nota |
|---|--:|--:|--:|---|
| hip_pitch | 0.0 | 64.5 | -102.7 | solo X=0 |
| hip_roll | 0.0 | 116.5 | -133.2 | solo X=0 |
| hip_yaw | 0.0 | 116.5 | -251.0 | exact_x 46.2 -> 0 |
| knee | 0.0 | 116.5 | -439.3 | Y allineata a hip_roll |
| ankle_pitch | 0.0 | 116.5 | -739.3 | Y allineata a hip_roll |
| ankle_roll | 0.0 | 116.5 | -756.9 | Y allineata a hip_roll |
| waist_yaw | 0.0 | 0.0 | 0.0 | solo X=0 |
| waist_roll | 0.0 | 0.0 | 44.0 | exact_x -4 -> 0 |
| waist_pitch | 0.0 | 0.0 | 44.0 | exact_x -4 -> 0 |
| shoulder_pitch | 0.0 | 100.2 | 291.8 | solo X=0 |
| shoulder_roll | 0.0 | 140.6 | 289.0 | solo X=0 |
| shoulder_yaw | 0.0 | 146.8 | 185.8 | solo X=0 |
| elbow | 0.0 | 146.8 | 105.2 | Y allineata a shoulder_yaw |
| wrist_roll | 0.0 | 146.8 | 95.2 | Y allineata a shoulder_yaw |
| wrist_pitch | 0.0 | 146.8 | 95.2 | Y allineata a shoulder_yaw |
| wrist_yaw | 0.0 | 146.8 | 95.2 | Y allineata a shoulder_yaw |

Per disegnare o controllare visivamente le braccia appese lungo il corpo, usare solo le colonne ausiliarie `pose_down_*`.
In quelle colonne gomito e polso vengono calcolati convertendo la lunghezza relativa `X/Z` della posa URDF in discesa `Z`.
Questa non e la tabella primaria dei giunti e non va usata come nuova cinematica G1.

Significato fisico dei punti: sono origini dei frame giunto URDF, quindi centri cinematici degli assi di rotazione. In
Onshape trattarli come mate connector del giunto: il punto attraversato dall'asse `axis_preciso`. Non sono automaticamente
il centro del cilindro del motore e non sono automaticamente il centro della faccia esterna del cilindro. Per un motore
coassiale, il cilindro motore va posizionato rispetto a questo mate connector con l'offset reale tra piano/flangia di uscita,
corpo motore e centro geometrico del cilindro. Per caviglia e vita a puntoni, questi punti sono giunti virtuali G1 e non
posizioni dei motori fisici.

CAD motori RobStride: STEP scaricabile dalle pagine Seeed (in BOM nella colonna "Link acquisto" e ora anche "CAD 3D").
Fonte STEP diretta per modello: AIFITLAB `aifitlab.com/products/robstride-0X-motor` (STEP + disegno installazione col
pattern bulloni). Alternative: download center robstride.com, GrabCAD (RS06).

## K-Scale K-Bot: nota secondaria, non baseline

Fonti:

- Meccanica e CAD pubblico: <https://docs.kscale.dev/robots/k-bot/mechanical/>
- Motor mapping: <https://docs.kscale.dev/robots/k-bot/motor-id-mapping>
- Repository: <https://github.com/kscalelabs/kbot>

Non copiare geometrie, motori o cinematica K-Bot nella baseline. La sua caviglia e diversa; il nostro progetto replica
invece il concetto G1 con due attuatori nel polpaccio e due puntoni per ottenere pitch e roll. K-Bot resta utile solo per
osservare soluzioni costruttive e per ricordare che il cablaggio dinamico richiede progettazione accurata. La sua
documentazione e in sviluppo: non usarla per dimensionare componenti.

## Decisione motori: solo RobStride

Damiao e CubeMars sono stati eliminati dalla distinta scelta. L'ecosistema unico riduce firmware, tool di debug, ricambi
e varianti di cablaggio. La distinta contiene solo le alternative RobStride rilevanti.

### Gambe, fase 1

| Posizione | Motore | Quantita | Picco | Dimensioni | Nota |
|---|---|---:|---:|---|---|
| Hip pitch / roll + knee | RS04 | 6 | 120 Nm | 120 x 120 x 56 mm | massimo disponibile RobStride |
| Hip yaw | RS06 | 2 | 36 Nm | 88 x 88 x 49 mm | asse verticale: gravita 0, ~28 Nm in girata aggressiva a massa G1; borderline se il robot arriva a 46 kg |
| Caviglia a puntoni, un motore per asse | RS06 | 4 | 36 Nm picco | 88 x 88 x 49 mm | eguaglia i 35 Nm G1 per asse al picco; rapporto leveraggio minimo 1:1, preferibile 1.3-1.6:1 se il robot diventa pesante |
| Alternativa caviglia alleggerita | RS00 a riduzione ~2:1 | qty 0 | 14 Nm picco | 57 x 57 x 51 mm | risparmia 1.244 kg ma riduce velocita e margine; non selezionata |

Limite noto: il RS04 resta sotto del 13.7% rispetto ai 139 Nm G1 su hip pitch, hip roll e knee. Copiare esattamente la
potenza G1 non e possibile restando nella gamma RobStride corrente. Il compromesso e esplicito, non va nascosto.

Nodo densita di coppia (analisi 2026-06-04, sollevata dall'utente): il G1 ottiene ~120 Nm in un attuatore Unitree da
~80 mm (misura mesh utente); RobStride per ~120 Nm richiede l'RS04 da ~110-120 mm. Quindi NON si possono rispettare insieme
le posizioni giunto G1 (pensate per motori ~80 mm) e la coppia G1. Riferimento crudo: il link hip_pitch del G1 pesa
1,35 kg (motore+struttura), quanto UN solo RS04 (1,4 kg) -> con RS04 le gambe diventano piu pesanti del G1. E non esiste
un RobStride intermedio: tra RS03 (60 Nm picco, 106 mm) e RS04 (120 Nm picco, ~110 mm) non c'e nulla, e RS03 e appena
piu piccolo (declassare a RS03 risparmia massa, non diametro). Opzioni reali sulle gambe: (a) tenere RS04 -> coppia vicina
al G1 ma gambe piu grosse/pesanti, geometria anca da riadattare (i joint G1 esatti non entrano); (b) RS06 ~88 mm -> vicino
alla geometria G1 ma solo ~36 Nm picco, un quarto del G1, adatto solo a robot piu leggero/meno dinamico. La scelta dipende
dall'ambizione (locomozione dinamica tipo G1 vs camminata + RL su piano): 139/120 Nm servono per il dinamico, per la
camminata lenta il fabbisogno e piu basso. NON cambiare i motori gamba in BOM finche l'utente non decide l'ambizione.

La caviglia conserva l'architettura richiesta: due attuatori nel polpaccio, due puntoni regolabili e un giunto a due
assi tra piede e stinco. Sono sottosistemi distinti:

- I quattro puntoni caviglia M8 restano selezionati: due per gamba. Spingono su un perno trasversale solidale al piede.
- Il perno trasversale dei puntoni ha diametro 8 mm, coerente con i fori delle teste a snodo M8. Lunghezza, materiale,
  tolleranza, distanza laterale tra le sfere e ritegno restano da definire nel CAD.
- Il giunto piede-stinco permette pitch e roll e porta i carichi strutturali del piede. Usa due perni ortogonali di
  diametro 12 mm per caviglia: servono solo come assi di rotazione del giunto e non ricevono i puntoni. Lunghezza,
  materiale, tolleranze, ritegni, tipo e quantita dei supporti restano da definire nel CAD.
- I due puntoni vita M10 restano selezionati: il totale del robot e quindi sei puntoni, quattro M8 alle caviglie e due
  M10 alla vita.

Geometria chiarita dall'utente per entrambi gli assi diametro 12 mm: le due orecchie esterne sono fisse rispetto al perno;
il pezzo centrale della caviglia ruota sul perno. Non mettere automaticamente supporti radiali sia nel centro sia nelle
orecchie: sarebbe ridondante e rischierebbe disallineamenti. Le orecchie devono portare e trattenere il perno fisso; il
pezzo centrale mobile contiene il supporto radiale.

DECISIONE FINALE caviglia (2026-06-03) - radente igus flangiato, assiale nella flangia. Vale per ciascuno dei due assi
diametro 12 mm. E la soluzione scelta come la piu semplice e sostituisce le ipotesi NKI / manicotto-colonna / ralle
separate descritte sotto, ora archiviate come alternative.

- Perno = vite a colletto ISO 7379 `Ø12 / M10`. Fa da perno, da pista su cui scorre l'igus e da ritegno. E reso solidale
  alle orecchie dal SERRAGGIO ASSIALE (colletto da un lato, dado autobloccante M10 + Loctite 243 sul filetto dall'altro),
  non da un piantaggio forte. Accoppiamento gambo-foro orecchia: scorrevole-bloccato (snug), giusto per togliere il gioco
  radiale ed evitare fretting; niente interferenza forte nel PA-CF stampato (crepa i layer ed e dura da montare su due fori
  coassiali). Quasi nessuna coppia arriva al perno perche il pezzo mobile gira sull'igus a basso attrito: il serraggio
  basta a tenerlo fermo. Variante pulita: filettare il capo lontano in un inserto metallico/dado annegato nell'orecchia,
  cosi il serraggio reagisce su metallo. Antirotazione extra (flat sul gambo) solo se serve.
- Supporto = boccola flangiata igus nel pezzo mobile. PRIMARIO scelto dall'utente: boccola STAMPATA multimateriale J260+PA-CF
  integrale al pezzo mobile in FDM (J260 sia sul foro sia sulle facce di flangia; filamento gia acquistato). FALLBACK
  acquistabile se la stampa non regge: `GFM-1214` iglidur G (drop-in `Q2FM-1214` per urti/sporco o
  `JFM-1214` basso attrito) piantate a PRESSIONE nel pezzo centrale mobile, flange verso l'esterno. La boccola porta il
  RADIALE; la FLANGIA porta l'ASSIALE, una per verso. Quindi niente ralle separate, niente reggispinta, niente
  manicotto/colonna. Ritegno boccola: interferenza nella sede + flangia di battuta. Su PA-CF stampato il foro non e
  preciso: stampare, provare il fit, aggiustare il Ø in CAD; riserva `Loctite 603/638` (bloccante anaerobico per
  accoppiamenti). Mai cianoacrilato (Attak): fragile e sbagliato per trattenere boccole.
- Serraggio = dado M10 autobloccante DIN 985 + rondella larga DIN 9021.
- Controfaccia su cui striscia la flangia = OPZIONALE. PARTENZA scelta dall'utente: spallamento PA-CF ricavato dalle orecchie verso l'interno, su cui striscia la
  flangia igus stampata (contatto PA-CF contro igus, non PA-CF contro PA-CF su tutta la faccia, concentrato sull'anello di
  flangia). In alternativa la flangia striscia diretta sulla faccia PA-CF
  dell'orecchia (assiale stimato ~1,3 MPa, oscillazione lenta, ok per prototipo, validare usura sul provino). Upgrade se
  il PA-CF si consuma: una bussola flangiata METALLICA piantata a pressione in ciascuna orecchia (`DIN 172-B12-20` o
  simile), solidale per interferenza come l'igus (niente colla), la sua flangia e la controfaccia metallica e il foro
  guida e protegge il perno. NON usare una rondella sfusa in tasca: non resta solidale all'orecchia, gira e finisce per
  strisciare comunque su PA-CF su una faccia.
- Verifiche di carico: radiale ~8 MPa, assiale ~1,3 MPa sull'igus, contro limite iglidur G `>60 MPa`, margini ~10x e ~45x.
  Il tipo di supporto non e guidato dal carico (irrisorio) ma dalla semplicita e dall'oscillazione: i rullini rischiano
  false brinelling sotto moto oscillante, il radente no.
- Quantita: 2 perni per caviglia x 2 caviglie = 4 assi. Per asse: 1 vite a colletto, 2 boccole flangiate igus, 1 dado +
  1 rondella larga, piu (opzionale) 2 bussole flangiate metalliche.
- Resta al CAD: lunghezza delle due boccole = spessore reale del pezzo mobile (es. due da 9 mm in 20 mm); lunghezza
  colletto = pacco forcella reale (~60-70 mm); gioco assiale 0,1-0,3 mm (boccole + mobile un filo piu strette del vano
  fra le orecchie).

Fornitori verificati 2026-06-03 (piu scelte, roba comune):

| Pezzo | SKU / famiglia | Fornitori |
|---|---|---|
| Boccola flangiata igus | `GFM-1214` iglidur G, Ø12/Ø14, flangia ~Ø20x1, L da CAD ~9-10 | igus diretto, RS, Misumi, Minetti, F.lli Bono, Solema, ERIKS |
| Vite a colletto | ISO 7379 `Ø12-M10`, L colletto da CAD | RS PRO `292-417` (12x60), Rubix `GN.35185`, Elesa, Puntoviti, Berardi, KIPP |
| Bussola flangiata metallica (opzionale) | `DIN 172-B12-20` | Verzolla `Y1137`, Best4Automation, KIPP `K1022.A1200X20` |
| Dado + rondella | M10 DIN 985 autobloccante + DIN 9021 | ovunque |
[ALTERNATIVA ARCHIVIATA - superata dalla DECISIONE FINALE caviglia sopra; tenuta solo come opzione a rullini se un giorno
servisse] Prima architettura semplice da disegnare in CAD, richiesta dall'utente:

- orecchio esterno PA-CF circa `20 mm`;
- pezzo centrale mobile circa `20 mm`, con SKF `NKI 12/16` largo `16 mm` nella propria sede;
- secondo orecchio esterno PA-CF circa `20 mm`;
- pacco strutturale preliminare circa `60 mm`, esclusi piccoli giochi e dettagli di ritegno.

Con `NKI 12/16` l'anello interno separabile va serrato tra gli spallamenti integrati delle due orecchie PA-CF e resta fisso
insieme al perno; l'anello esterno resta nella sede del pezzo centrale mobile. Il gioco di funzionamento va lasciato tra
le orecchie e il pezzo centrale mobile, non tra spallamenti e anello interno. Gli spallamenti non devono schiacciare la
parte mobile. Verificare in CAD area di battuta, creep del PA-CF e serraggio: se la pressione locale e eccessiva, interporre
spessori metallici di ripartizione oppure passare agli inserti metallici flangiati documentati sotto.

Attenzione: `NKI 12/16` porta il radiale ma non sostituisce un reggispinta. Se il pezzo centrale mobile arriva a toccare
assialmente le orecchie sotto carico, prevedere una tasca per ralla igus sottile e registrata oppure un reggispinta separato.
Non lasciare PA-CF contro PA-CF come superficie di usura.

Serraggio preliminare dell'asse con `NKI 12/16`: non usare il bullone per flettere le orecchie verso l'interno fino a
recuperare un errore dimensionale. La catena fissa deve risultare chiusa gia a quota nominale; le correzioni fini si fanno
con rasamenti selezionati dopo la prova del primo prototipo. Sequenza dall'esterno verso l'esterno: testa del bullone a
colletto e rondella larga, orecchia PA-CF, spallamento anulare integrato nell'orecchia, anello interno `NKI`, secondo
spallamento anulare integrato, seconda orecchia PA-CF, rondella larga e dado autobloccante. Il corpo centrale mobile e
l'anello esterno del cuscinetto devono restare esclusi dalla catena serrata e conservare un piccolo gioco assiale controllato
rispetto alle orecchie. Il filetto non deve lavorare nella zona di taglio o nella pista del cuscinetto. Usare rondelle larghe
per distribuire il carico sul PA-CF; coppia di serraggio e creep vanno verificati sul provino reale. Se la pressione locale e
eccessiva, aggiungere distanziali metallici di ripartizione oppure passare alla variante con bussole DIN 172.

Riferimenti preliminari da confermare sulla quota finale del pacco:

| Componente | Dimensioni utili | Link |
|---|---|---|
| RS PRO `292-417`, bullone a colletto ISO 7379 | colletto liscio `12 x 60 mm`, filetto `M10 x 16 mm`, lunghezza totale `84 mm` | <https://it.rs-online.com/web/p/viti-a-colletto/0292417> |
| RS PRO `797-6254`, rondella larga DIN 9021 | foro `10,5 mm`, diametro esterno `30 mm`, spessore `2,5 mm` | <https://it.rs-online.com/web/p/rondelle/7976254> |

Il colletto liscio da `60 mm` e coerente con il pacco strutturale preliminare `20 + 20 + 20 mm`, ma la misura definitiva
dipende da giochi, rasamenti e sedi reali.

Non selezionare ancora definitivamente cuscinetti, boccole o rullini per il giunto caviglia: prima servono CAD, carichi,
sedi, spessori e tolleranze. Le precedenti ipotesi `6001-2RS` e `6801-2RS` sono state rimosse dalla BOM perche premature.
Se mancano dati meccanici, chiedere conferma all'utente invece di proporre una soluzione come se fosse gia definita.

Prima alternativa da valutare per i due assi diametro 12 mm: boccole radenti lunghe, non necessariamente cuscinetti
volventi. Il giunto caviglia compie rotazioni limitate e oscillanti, con urti e velocita ridotte: una boccola radente
composita metallo/PTFE oppure polimerica heavy-duty puo risultare piu semplice, compatta e tollerante dei rullini.
Per separare correttamente i compiti:

- la boccola cilindrica nel pezzo centrale mobile porta il carico radiale;
- una ralla radente dedicata per lato porta il carico assiale e deve essere registrata, non lasciata libera tra due facce;
- un inserto metallico flangiato fisso in ciascuna orecchia, simile a una boccola a cappello, contiene o guida il perno
  diametro 12 mm e offre alla ralla igus una controfaccia assiale liscia e sostituibile;
- eventuali rasamenti DIN 988 correggono solo il gioco residuo dopo il montaggio: non sono la superficie primaria di usura.

Non lasciare lavorare igus direttamente contro il PA-CF dell'orecchia e non usare direttamente il PA-CF stampato come
superficie di scorrimento. Non lasciare una rondella libera di ruotare casualmente contro entrambe le facce. La ralla puo
essere registrata in una tasca poco profonda del pezzo mobile; l'inserto metallico e invece solidale all'orecchia.

Gli inserti metallici a cappello non sono piu la prima architettura da disegnare, ma restano un'alternativa standard facile
da acquistare se si usa una boccola igus centrale stampata oppure se gli spallamenti PA-CF non bastano. La misura reale
individuata e Elesa+Ganter `DIN 172-B12-20-A` / `GN.12825`: foro `12 mm F7`, esterno `18 mm n6`, flangia diametro `22 mm`,
corpo lungo `20 mm`, flangia spessa `4 mm`. Va usato un cappello su entrambe le orecchie. Il foro guida il perno ma non lo
blocca automaticamente in rotazione: progettare antirotazione e ritegno assiale. Se si mantiene il riferimento strutturale
`20 + 20 + 20 = circa 60 mm`, incassare la flangia da `4 mm` nell'orecchia; altrimenti le due flange aggiungono ingombro.

Fornitori verificati il 2026-06-02 per cappelli standard foro 12 mm, lunghezza 20 mm:

| Fornitore | SKU | Prezzo | Disponibilita dichiarata | Link |
|---|---|---:|---|---|
| Verzolla Italia | Elesa+Ganter `DIN172-B12-20-A`, codice `Y1137` | EUR 6,89 cad | 5 disponibili | <https://www.verzolla.com/elesa-bussola-di-guida-flangiata-din172-b12-20-a-y1137> |
| Best4Automation | Otto Ganter `172-B12-20-A` | EUR 5,26 netto cad | spedibile in 2-3 giorni lavorativi, B2B | <https://www.best4automation.com/positionierbuchse-mit-bund-bohrung-eins.-gerundet-sc-4042-172-b12-20-a/> |
| Normteile Leinigen | KIPP `K1022.A1200X20`, equivalente DIN 172 forma A | EUR 4,50 netto / EUR 5,36 IVA inclusa cad | disponibile, 2-5 giorni | <https://www.normteile-leinigen.de/Bundbohrbuchse-12-x-20-DIN-172-Form-A/K1022.A1200X20> |
| TME | Elesa+Ganter `DIN172-B12-20-A` | USD 10,04 cad | stock zero: usare come scheda tecnica o backup richiesta | <https://www.tme.eu/en/details/din172-b12-20-a/indexing-plungers/elesa-ganter/din-172-b12-20-a/> |

Scheda ufficiale Elesa+Ganter: <https://www.elesa.com/siteassets/PDF/PDF_IT/DIN%20172.pdf>.

Cataloghi utili per perni e ritegni caviglia, mantenuti in BOM a quantita zero per verificare cosa esiste realmente prima
di chiudere le quote del CAD:

| Famiglia | Riferimento | Link |
|---|---|---|
| Viti a spallamento assortite | set storico AliExpress `M3-M10` | <https://it.aliexpress.com/item/1005007481484485.html> |
| Bullone a colletto corto | RS PRO `822-9316`, `12 x 20 mm`, filetto `M10` | <https://it.rs-online.com/web/p/viti-a-colletto/8229316> |
| Bullone a colletto asse completo | RS PRO `292-417`, `12 x 60 mm`, filetto `M10 x 16 mm` | <https://it.rs-online.com/web/p/viti-a-colletto/0292417> |
| Albero rettificato da tagliare | Motedis `12 mm h6`, temprato e rettificato | <https://www.motedis.it/it/Albero-di-precisione-12-mm-h6-acciaio-temprato-e-rettificato> |
| Spina cilindrica corta | Wurth DIN 6325 / ISO 8734 `12 x 20 mm` | <https://eshop.wurth.fr/Goupille-cylindrique-DIN-6325-acier-brut-GOUPILLE-CYL-DIN6325-M6-12X20/025201220.sku/fr/FR/EUR/> |
| Ritegni elastici | assortimento anelli Seeger interni ed esterni | <https://www.amazon.it/ANELLI-ELASTICI-INTERNI-ESTERNI-ASSORTITI/dp/B09CZKWD5J> |
| Collare apribile asse `12 mm` | Ruland `MSP-12-F` | <https://www.ruland.com/msp-12-f.html> |
| Albero rettificato da tagliare per perno puntoni | Motedis `8 mm h6`, temprato e rettificato | <https://www.motedis.it/it/Albero-di-precisione-8-mm-h6-acciaio-temprato-e-rettificato> |
| Collare apribile asse `8 mm` | Ruland `MSP-8-F` | <https://www.ruland.com/msp-8-f.html> |

Se si valuta invece un cuscinetto radiale a rullini:

- SKF `HK 1216.2RS` e compatto ma non ha anello interno: richiede una pista perno temprata e rettificata;
- SKF `NKI 12/16` include l'anello interno: gli spallamenti fissi delle orecchie possono serrare quell'anello mentre
  l'anello esterno resta nella sede del pezzo centrale mobile;
- un cuscinetto radiale a rullini non sostituisce automaticamente la battuta assiale: per l'assiale serve ancora una
  interfaccia radente dedicata oppure un reggispinta separato. Non serrare il pezzo centrale mobile tra gli spallamenti.

Non scegliere ancora SKU o lunghezza `20-25 mm`: servono carico radiale massimo, carico assiale, angolo e frequenza di
oscillazione, diametro esterno massimo della sede, materiale del perno, finitura superficiale, tolleranze e spazio assiale.

Esempi reali aggiunti in BOM come alternative `qty 0`, non ancora selezionate:

| SKU | Tipo | Dimensioni | Prezzo verificato 2026-06-02 | Nota |
|---|---|---|---:|---|
| SKF `PCM 121420 E` | metallo/PTFE | 12 x 14 x 20 mm | EUR 2,13 netto | prima candidata semplice |
| SKF `PCM 121425 E` | metallo/PTFE | 12 x 14 x 25 mm | EUR 2,94 netto | dimostra che 25 mm e una lunghezza standard |
| igus `Q2SM-1214-20` | polimero heavy-duty | 12 x 14 x 20 mm | circa EUR 6,15 netto | candidato per oscillazione, urti e sporco |
| igus `Q2FM-1214-12` | polimero heavy-duty flangiato | 12 x 14 x 12 mm, flangia 20 x 1 mm | da verificare | solo se il CAD consente la flangia |
| igus `GTM-1224-015` | ralla radente separata | 12 x 24 x 1,5 mm | EUR 1,49 IVA inclusa | una per lato da registrare, non libera |
| SKF `HK 1216.2RS` | rullini radiale senza anello interno | 12 x 18 x 16 mm | quotazione | richiede pista perno temprata |
| SKF `NKI 12/16` | rullini radiale con anello interno | 12 x 24 x 16 mm | EUR 22,15 netto | coerente con spallamenti fissi, ma non regge da solo l'assiale |
| SKF `AXK 1226` + `AS 1226` | reggispinta a rullini con piste | 12 x 26 x 4 mm per lato | EUR 4,10 + 2 x EUR 1,86 netto | alternativa piu ingombrante alla ralla igus |
| HGI `PS12X18X1` DIN 988 | rasamento di registro | 12 x 18 x 1 mm | EUR 0,48 netto | solo correzione finale del gioco |
| Elesa+Ganter `DIN 172-B12-20-A` / `GN.12825` | inserto metallico flangiato fisso alternativo | 12 x 18 x 20 mm, flangia 22 x 4 mm | EUR 6,89 cad Verzolla | cappello standard per entrambe le orecchie se si sceglie la strada igus |

L'utente sta acquistando tre tribofilamenti igus stampabili per fare prove comparative: `iglidur i150`, `iglidur i190`
e `iglidur J260-PF`. Sono state aggiunte tre righe `[ALT CUSTOM qty0]` separate. Le boccole custom possono essere utili
per iterare rapidamente lunghezza, flangia e gioco, ma non sono ancora una scelta dimensionata ne una sostituzione
automaticamente equivalente alle boccole SKF metallo/PTFE o igus `Q2` stampate a iniezione. Stampare provini confrontabili
e validare pressione superficiale, usura, orientamento di stampa, finitura del perno, tolleranze e gioco. `i150` e il piu
facile da processare; `i190` privilegia resistenza e usura ed e sensibile all'umidita; `J260-PF` e piu esigente da stampare
ma va confrontato per attrito, usura e temperatura.

### Corpo superiore, fase 3

La vita mantiene l'architettura fisica richiesta: un motore yaw verticale sotto che ruota tutto il busto, poi cardano
centrale e due attuatori collegati a due puntoni per produrre pitch e roll. Il motore yaw e piu grosso; i due motori a
puntoni sono piu piccoli ma non vanno dimensionati assumendo automaticamente meta carico ciascuno.

| Posizione | Motore | Quantita | Dimensioni | Peso | Coppia RobStride | Riferimento G1 |
|---|---|---:|---|---:|---|---|
| Waist yaw | RS06 (declassato da RS03) | 1 | 88 x 88 x 49 mm | 0.621 kg | 11 nom / 36 picco | 88 Nm; verif ~28 Nm torsione aggressiva < 36 |
| Waist pitch / roll via 2 puntoni | RS06 (declassato da RS03) | 2 | 88 x 88 x 49 mm | 0.621 kg | 11 nom / 36 picco | 35 Nm/asse; giunto ~18-37, condiviso dai 2 puntoni |
| Shoulder pitch / roll prossimali | RS00 (declassato da RS02, 2026-06-16) | 4 | 57 x 57 x 51 mm | 0.310 kg | 5 nom / 14 picco | 25 Nm; dinamico ~12 < 14; hold orizzontale 6.8 non continuo (gia' cosi' con RS02). -95 g e Ø57 vs 78.5. Dual encoder. RS06 alt qty0 |
| Shoulder yaw distale | RS00 (declassato da RS02) | 2 | 57 x 57 x 51 mm | 0.310 kg | 5 nom / 14 picco | 25 Nm; gravita 0, ~4-6 Nm. dual encoder |
| Elbow | RS00 (declassato da RS02, 2026-06-16) | 2 | 57 x 57 x 51 mm | 0.310 kg | 5 nom / 14 picco | 25 Nm; ~6.9 con 2 kg -> ~1.2 kg continui / 2 kg picco. -95 g, Ø57. Dual enc. RS06 se serve 2 kg continui |
| Wrist roll + pitch/yaw uniformi | RS00 | 6 | 57 x 57 x 51 mm | 0.310 kg | 5 nom / 14 picco | roll 25 / pitch-yaw 5; regge 2 kg in mano, dual encoder |
| Collo pan / tilt G1-Comp | RS05 | 2 | 46 x 46 x 44 mm | 0.191 kg | 1.6 nom / 5.5 picco | coppia non pubblicata |

Riserve qty0: spalla pitch/roll RS06; spalla yaw RS02; polso RS02 (robusta) + RS05 (ultraleggera pitch/yaw); caviglia RS03.

**TRAPPOLA RS01 (verificata 2026-06-08).** RS01 e RS02 hanno la STESSA coppia (6/17 Nm) ma RS01 ha **1 solo encoder
(lato motore)**, RS02 ne ha **2 (motore + uscita)**. L'encoder d'uscita legge l'angolo vero del giunto dopo il riduttore
(compensa il backlash) -> serve per RL e manipolazione. RS01 e' la versione tagliata: solo 36V, niente IP, -$15 e -5.5mm.
Quindi sui giunti controllati (spalla, gomito) si tiene **RS02**, NON RS01. RS00 (polso, spalla yaw) ha dual encoder.
**RS01 non usato.** RS00 verificato dual encoder, 5 nom / 14 picco, 57x57x51, 0.310 kg, ~$125.

**Verifica braccio (posizioni reali G1, polso alleggerito a RS00).** Tenere il braccio disteso orizzontale = **6,8 Nm
statici**, picco dinamico ~12 Nm < 17. Il motore GOMITO a braccio teso conta 1,14 Nm (leva X = 187 mm a braccio disteso,
non i 16 mm a riposo). RS02 copre: l'hold a braccio orizzontale e' posa occasionale (non continua), dinamica 12 < 17.
Gomito con payload a 90 gradi: ~4,7 Nm con 1 kg, ~6,9 con 2 kg -> RS02 regge ~1,5 kg continui / 2 kg di picco; RS06 riserva.

**Caviglia + vita pitch/roll = LEVERAGGI, non presa diretta (correzione utente 2026-06-08).** La coppia al GIUNTO e' fissa
dal carico (caviglia ~46 Nm = peso x leva punta 130 mm); la coppia MOTORE = giunto x (crank_motore / crank_piede). I
puntoni spingono ~40 mm dal perno: spingere vicino al perno NON riduce la coppia motore (alza la forza nell'asta ~1150 N);
a ridurla e' il crank motore piu corto del crank piede (riduzione), che costa velocita di giunto. SCELTA FINALE
(2026-06-16, vedi bullet sessione punto e): solo cammino -> caviglia = 2x RS00 a riduzione ~2:1 (BOM). A 1:1 servirebbero
2x RS06 (alt qty0, per gait dinamici); l'RS02 e' eliminato. Crank esatti (per asse) DA FISSARE in CAD col Jacobiano 2x2.

Il corpo G1 EDU resta una baseline da 29 DOF. Aggiungendo il collo G1-Comp selezionato il progetto sale a 31 assi
motorizzati, esclusi eventuali motori delle mani. La coppia collo G1-Comp non e pubblica: RS05 `5.5 Nm picco / 1.6 Nm
nominali` e una scelta provvisoria basata su compattezza e massa. Il polso e' tutto RS00 (dual encoder, 57 mm, 5 nom /
14 picco): regge 2 kg in mano e dimezza l'ingombro vs RS02. Riserve qty0: RS02 (robusta) e RS05 (ultraleggera pitch/yaw).

## Confronto marche motori a parita' di coppia (ingombro, peso, costo) - 2026-06-14

Confronto chiesto dall'utente: a PARITA' DI COPPIA conta prima ingombro+peso, poi costo, poi reperibilita'.
Spec verificate via web (Seeed, CubeMars, ROBOTIS emanual, Foxtech). Dynamixel aggiunto al confronto.

**CLASSE ~36 Nm - caviglia (4) + hip yaw (2) + vita puntoni (3) = 9 motori. QUI sta il risparmio di peso.**

| Marca / modello | Picco Nm | Ingombro mm | Peso | Nm/kg | Tipo + encoder | Costo cad | Reperibilita' |
|---|---:|---|---:|---:|---|---|---|
| RobStride RS06 | 36 | Ø88 x 49 | 621 g | 58 | QDD, dual enc | ~200 EUR | buona (Seeed, AliExpress) |
| **Encos EC-A4310-P2-36** | 36 | Ø56 x 60.5 | **382 g** | 94 | QDD 36:1, dual enc | ~700 USD | **scarsa (solo Foxtech, a preventivo)** |
| CubeMars AK10-9 v3 | ~48-53 | Ø98 x 62 | 940 g | ~53 | QDD, dual enc | ~700 USD | ottima (T-Motor) |
| Dynamixel PH42-020-S300 | ~25 (max) | 42 x 84 x 42 | 340 g | ~74 | cicloidale >300:1, NON backdrivabile | ~900-1100 USD | ottima (ROBOTIS) |

**CLASSE ~120-170 Nm - gambe: hip pitch/roll + ginocchio = 6 motori. CubeMars qui e' CAPACITA', non peso.**

| Marca / modello | Picco Nm | Ingombro mm | Peso | Nm/kg | Tipo + encoder | Costo cad | Reperibilita' |
|---|---:|---|---:|---:|---|---|---|
| RobStride RS04 | 120 | Ø106 x 56 | 1420 g | 85 | QDD, dual enc, INTEGRATO | **~255 USD** | buona (8+ rivenditori) |
| **CubeMars AKE90-8** | **170** | Ø107.5 x **43.5** | 1400 g | 121 | planet. 9 arcmin, dual enc, NUDO (+driver) | ~484 USD + driver | ottima (T-Motor) |
| Encos A10020 | 150 | non pubblicato | 1350 g | 111 | QDD | ~2250 USD | scarsa (Foxtech) |
| Dynamixel PH54-200-S500 | 44 (rated) | 54 x 126 x 54 | 855 g | 52 | cicloidale ~500:1, NON backdriv. | **3541 USD** | ottima (ROBOTIS) |

(Dynamixel PH54 = flagship e NON arriva alla coppia gamba: 44 Nm vs 120-170 richiesti. Fuori gioco per le gambe.)

**CLASSE <=17 Nm - spalle/gomito/polso/collo. RobStride imbattibile, niente premium.**

| RobStride RS00 | 14 | Ø57 | 310 g | 45 | QDD dual enc | ~116 EUR | buona |
| RobStride RS02 | 17 | Ø78.5 x 45.5 | 405 g | 42 | QDD dual enc | ~135 EUR | buona |
| RobStride RS05 | 5.5 | compatto | 191 g | 29 | QDD | ~100 EUR | buona |

(Sotto i ~20 Nm nessun premium batte RobStride su peso+costo+integrazione. RS00 310 g e' piu' leggero di qualunque alternativa a quella taglia.)

**DOVE risparmiamo davvero, in chiaro:**
- **Peso = SOLO Encos sui 36 Nm**: -244 g x 9 motori = **-2,2 kg**, e tutto DISTALE (caviglia/gamba) -> oro per le dinamiche di camminata. Costo: ~700 USD vs ~200 EUR cad (~3,5x) e reperibilita' pessima.
- **CubeMars AKE90-8 sulle gambe = NON peso** (1,40 vs 1,42 kg, uguale): e' +50 Nm (supera il G1, toglie lo 0,86x dell'RS04) e **13 mm piu' sottile** (43,5 vs 56) -> packaging anca migliore. Costo ~2x e "nudo" (driver+encoder a parte).
- **Piccoli (<=17 Nm)**: nessun guadagno, RobStride resta.

**REPERIBILITA' worldwide (ordine):** Dynamixel (ROBOTIS, distributori globali) > CubeMars/T-Motor (retail mondiale) > RobStride (Seeed + 8 rivenditori, AliExpress, in crescita) > **Encos (Foxtech, solo a preventivo, non pubblica nemmeno le quote)**. Quindi SI: RobStride e' MOLTO piu' facile da reperire di Encos.

**Dynamixel = CLASSE SBAGLIATA per noi.** Sono servo di POSIZIONE con riduttore cicloidale alto (300-500:1): coppia densa ma NON backdrivabili, lenti (29-33 rpm), backlash basso ma controllo in forza/impedenza scarso, e carissimi (PH54 = 3541 USD, 14x un RS04). Ottimi per bracci lenti in posizione, INADATTI a un clone G1 con locomozione RL e manipolazione in forza, che vuole QDD backdrivabili (RobStride/Encos/CubeMars). Reperibilita' top, ma irrilevante se la categoria e' sbagliata. (NB: il paper ToddlerBot - Stanford - usa proprio i Dynamixel ed e' infatti piccolo/lento/servo di posizione, conferma della categoria.)

**NB "T-Motor" = CubeMars.** Stessa azienda (Sanrui Intelligent): CubeMars e' il brand-sorella robotico di T-Motor, e i manuali della serie AK sono ospitati su store.tmotor.com. Le AK10-9 / AKE90-8 gia' in tabella SONO i "T-Motor": non esiste un'opzione T-Motor separata da valutare. Le altre linee T-Motor (U/Antigravity) sono motori RC/droni, non attuatori robotici.

## Due-diligence motori premium / fornitori + reference ASIMOV (2026-06-16)

Ricerca di mercato per "umanoide leggero + elegante + potente + force control", dopo decisione CORRENTE A MURO
(tethered, batteria a terra per i picchi, NIENTE batteria di bordo -> robot ~28-30 kg -> gambe e caviglie chiedono
meno coppia). Direzione: motori PICCOLI e DENSI ovunque, tutti CAN + dual-encoder + controllo di COPPIA (omogenei per RL).

**REFERENCE = ASIMOV v1 (il nostro gemello open-source).** 1,2 m, 35 kg, 25 DOF, **caviglia RSU parallela identica
alla nostra**, **motori ENCOS ovunque**, CAD meccanico+elettrico + BOM completi pubblici. Attuatori ~$7.000 per 25
(~$280 medio). I MODELLI ENCOS esatti per ogni giunto sono nel loro BOM Tally (link da docs.menlo.ai/asimov/v1/bom);
CAD su github.com/asimovinc/asimov-1 (file mechanical/FABRICATION_MANIFEST.csv + modello sim). DA COPIARE giunto-per-giunto.
Conferma: Encos sta su ASIMOV (non X-Humanoids, l'utente si era corretto). Compute Asimov = Raspberry Pi 5 + Radxa CM5.

**ENCOS (il piu' leggero a 36 Nm: A4310 377 g).** Reperibile: Foxtech (store.foxtech.com) + aifitlab.com +
arcsecondrobo.net (tutti rivenditori cinesi). Spedizione internazionale dichiarata, Italia DA CONFERMARE (utente ha
mandato inquiry Foxtech il 2026-06-16: chiedere prezzo shipped-to-Italy + file CAD STEP + tempi/dogana). Affidabilita':
validato da Asimov; dati guasto indipendenti scarsi. PUNTO DEBOLE = documentazione: NIENTE CAD/quote pubblici ->
CAD da RICHIEDERE a Foxtech o misurare campione. Lineup (modulo Ø): A2806 (12 Nm, Ø44, 162 g) / A4310 (36 Nm, Ø56, 382 g) /
A4315 (75 Nm, Ø56, 485 g) / A6416 (120 Nm, Ø88, 805 g) / A8112 (Ø81) / A10020 (Ø100) / A13715-720 (Ø137).
CORREZIONE 2026-06-19 (datasheet V3.15): l'A2806 Ø44 esiste -> Encos HA un'opzione polso (smentito il vecchio "sotto Ø60 niente").

**STEADYWIN (micro, cheap, MIT protocol).** Reperibile: steadywin-motor.com, OpenELAB, Alibaba, aifitlab (niche ma ok).
Driver: integrato CAN/UART, **protocollo MIT open-source** (standard Mini-Cheetah, codice community) o SHS; pilotabile
pure con Arduino+MCP2515. CAD 2D+3D + manuali su steadywin-motor.com/products/document-download. ROS2 testato (Ubuntu/
Iron, SOLO Linux). **POLSO IDEALE = GIM3510-64: Ø35 mm, riduzione 64:1, dual encoder, FOC** = micro + tanta coppia +
lento (esattamente il requisito polso). Niche ma integrabile, nessun red flag grave.

**MYACTUATOR (la meglio SUPPORTATA).** ROS2 maturo (github 2b-t/myactuator_rmd_ros) + SDK C++17 SocketCAN + Python +
CAD ufficiali; Amazon/RobotShop/Dings (USA/EU). Dual encoder. MA i piccoli RMD-L sono DIRECT-DRIVE deboli (5015=0,7 Nm,
9015=3,4 Nm); per coppia servono gli RMD-X planetari (un filo piu' grossi). Vince sul supporto, non sulla taglia minima.

**SURVEY "il migliore per categoria" (piccolo+potente+force control):**
- GAMBE 120-170 Nm: fisica = ~Ø100 minimo, NON si rimpicciolisce. Encos A10020 (Ø100, 150) o **CubeMars AKE90-8**
  (Ø107, 170, 9 arcmin, $484, CAD pronti). Col tether l'RS04 (120) torna pure comodo.
- MID 36 Nm (anca-yaw, vita, spalla p/r, caviglia): **Encos A4310** (Ø60, 377 g) = il piu' leggero; alt CubeMars
  AK10-9 (Ø98, 940 g) / Steadywin GIM8108-36.
- POLSO/piccoli force-control: **Steadywin GIM3510-64** (Ø35, 64:1) o MyActuator RMD-X (CAD/ROS top) o **Harmonic Drive
  RH-mini** (premium, zero gioco, €€€). Dynamixel SCARTATO (servo di posizione, niente force control).

**TENSIONE chiave:** i migliori a peso/taglia (Encos A4310, Steadywin micro) sono NICHE (Cina, supporto/CAD scarsi);
i meglio supportati (MyActuator, CubeMars) sono un filo piu' grossi/cari ma con CAD+driver pronti. Asimov dimostra che
la via niche (Encos + protocollo MIT) si costruisce davvero.

**CAD/manuali:** CubeMars (pagina prodotto) / Steadywin (document-download) / MyActuator (myactuator.com/dowload +
ROS driver) hanno CAD pubblici. Encos NO -> richiedere a Foxtech. Asimov intero: github.com/asimovinc/asimov-1.

**SEQUENZA:** 1) copiare i modelli dal BOM Tally di Asimov; 2) aspettare quote Foxtech (prezzo Italia + CAD + tempi);
3) se Encos ok -> Encos (gambe A10020 + mid A4310) + Steadywin GIM3510-64 ai polsi; 4) se no -> ripiego CubeMars +
Steadywin (CAD pronti). Polso pista principale = Steadywin GIM3510-64. BOM RobStride attuale resta intatto come baseline.

**MAPPA MOTORI ASIMOV completa (ricostruita 2026-06-16: BOM gambe v0 CERTO + matching `armature` nel sim model v1
sim-model/xmls/asimov.xml -> giunti con stessa armature = stesso attuatore). Naming Encos = EC-A[Ø frame][h]-[P plan /
H armonico][riduzione]:**
- Hip pitch: **EC-A6416-P2-25** (Ø64, planetario) | Hip roll: **EC-A5013-H17-100** (Ø50, ARMONICO 100:1) |
  Hip yaw: **EC-A3814-H14-107** (Ø38, ARMONICO 107:1) | Knee: **EC-A4315-P2-36** (Ø43) |
  Ankle A+B (RSU parallela pitch+roll): **EC-A4310-P2-36** (Ø43, 377 g) x2  [tutti CERTI dal BOM v0]
- CONFERMATO dal BOM Excel Asimov ("Asimov 1 BOM.xlsx" in cartella, qty tornano: A4310x10, A6416x3, A5013x4, A4315x4,
  A3814x4 = 25): Waist yaw = A6416 (Ø64) | Shoulder pitch = A5013-H armonico (Ø50) | Shoulder roll = A4315 (Ø43) |
  Shoulder yaw = A3814-H armonico (Ø38) | **Elbow + Wrist yaw + Neck = EC-A4310 (Ø43)** [stesso dell'ankle, qty 10 =
  ankle4+elbow2+wrist2+neck2]. Quindi Asimov usa SOLO 5 MODELLI, 4 taglie frame (Ø38/43/50/64); l'A4310 Ø43 fa il grosso.
- FORNITORE vero: **ENCOS = Nanjing Inks Intelligent Technology (Nanjing)**, rivenduto da Foxtech/aifitlab. BOM Asimov
  ~$15k target, "shipment in a few months". **CAD STEP intero robot: mechanical/ASV1/ASIMOV_V1.STEP** + mesh STL per
  giunto in sim-model/assets/meshes -> base CAD. Tally BOM: tally.so/r/jaG0va.
- IMPORTANTE: hip pitch/knee/ankle = PLANETARI (backdrivable a sufficienza per camminare); SOLO hip/spalla roll-yaw =
  armonici. Quindi le gambe NON sono rigide-armoniche (mio errore precedente corretto). Per CAMMINARE il planetario
  25-36:1 basta; il QDD 9:1 (RobStride) serve solo per correre/saltare, che non ci serve.

**NOSTRO LISTINO TUTTO-ENCOS = 3 MODELLI (scelta utente 2026-06-19, FINALIZZATA; 3a scheda Excel "MOTORI Encos (quote)"; 30 nel robot + 4 trial = 34 acquistati):**
- **EC-A6416-P2-25 (gambe) x6: hip pitch x2 + hip roll x2 + knee x2.** (Ø88, 805 g, 120 Nm picco)
- **EC-A4315-P2-36 (mid) x16: caviglia x4 + spalle x6 + gomito x2 + hip yaw x2 + vita x2.** (Ø56, 485 g, 75 Nm picco)
- **EC-A2806-P2-36 (polso+collo) x8: polso 3 DOF x2 + collo x2.** (Ø44, 162 g, 12 Nm picco, 220 RPM) <- COLLO spostato qui (75 Nm inutili in alto, alleggerisce la testa).
- **EC-A4310-P2-36 (trial) x4: comprati per PROVARE le caviglie** (planetario lento OK: il robot NON deve correre). Baseline caviglia resta A4315.
- A4315 = unica taglia mid (Ø56). Caviglia = ibrida FIGURE (pitch a puntone PROSSIMALE nello stinco + roll diretto piede, A4315 tenuta apposta). Vita = yaw+roll.

**OPZIONE RIAPERTA 2026-06-20 dall'utente: RobStride LIGHT, NO SENSORI (via Unitree pura).** RS06 (Ø88, 36/11 Nm) su hip/knee/shoulder; RS00 (Ø57, 14/5 Nm) sul resto INCLUSA la caviglia; RS05 collo. **NIENTE sensori di coppia, nemmeno al piede** (= QDD 9:1, corrente=coppia, come Unitree G1 che cammina/corre senza torque-sensor ne' F/T piede). Questa singola scelta CANCELLA tutto il problema vestizione/UKF/sensori piede.
- RISOLVE 2 problemi storici insieme: (1) caviglia = RS00 Ø57 (piccolo, NON RS06 Ø88) -> via il problema packaging che ci aveva spinti su Encos; (2) sensori -> nessuno (QDD).
- MATH (robot ~20 kg; i soli motori ~12 kg, struttura PA-CF leggerissima): hip/knee/shoulder RS06 36/11 = OK comodo per cammino piano (RMS << 11). Ankle = l'UNICO punto critico: RS00 diretto 14 Nm < ~16 Nm di equilibrio a 20 kg -> SERVE ~2:1, che pero' lo da' GRATIS il puntone/linkage caviglia (gia' previsto) -> ~28/10 Nm. OK.
- CAVEAT onesti: tenerlo LEGGERO (~20 kg); e' un CAMMINATORE non accovacciatore (RS06 11 Nm continui NON reggono squat profondo statico/scale); dinamica modesta (ZMP piano, stile Asimo, non Cheetah); = ottimizzazione SEMPLICITA' (~EUR 4k, zero sensori, provato) NON "massima qualita'" (piu' debole/ingombrante di Encos, niente torque-control fine). Scelta consapevole.
- LINEUP RobStride VERIFICATO (web 2026-06-20): RS05 Ø46/5.5Nm/191g | RS00 Ø57/14Nm/10:1/310g | RS02 Ø78/17Nm/7.75:1/405g | RS06 Ø88/36Nm/9:1/621g | **RS03 Ø106/60Nm/9:1/880g** | RS04 Ø110/120Nm/40 rated/9:1/1400g. (RS01 = encoder singolo, evitare.) **RS03 = scoperta utile = HIP sweet-spot** (tra RS06 36 e RS04 120; piu' leggero di RS04).
- **CAVIGLIA ASIMMETRICA (idea utente 2026-06-20, VALIDATA):** pitch = RS06 (36 Nm) nello STINCO via puntone (serve ~30: equilibrio M·g·mezza-lunghezza-piede + push-off); roll = RS00 (14 Nm) sul PIEDE diretto (serve solo ~9: piede STRETTO -> mezza-larghezza ~4.5cm = meta' leva del pitch, e NIENTE push-off in roll). RS00 basta col margine. Packaging: motore grosso prossimale (stinco), piccolo distale (piede). Caveat: CoM sul piede d'appoggio (RS00 5 Nm continui sottili in single-leg statico, ok in cammino).
- "RS05 sull'anca" = REFUSO utente: RS05 e' 5.5 Nm (troppo poco per QUALSIASI DOF d'anca, servono 16-40+). Per l'anca: RS03 (60) o RS04 (120).
- Mapping HEAVY RobStride: hip pitch/roll RS03 (o RS04) | knee RS03/RS06 | ankle pitch RS06 + roll RS00 | shoulder RS06 | elbow RS00/RS02 | wrist RS05 | neck RS05 | hip-yaw RS00/RS02 | waist RS06/RS03.

**ToddlerBot (Stanford 2025, domanda utente): NON QDD.** Usa **Dynamixel XC330/XM** = servo di POSIZIONE ad alta riduzione (~288:1 cicloidale), non backdrivabili, niente force-control da corrente. Robot ~0.5m/3-4kg da tavolo per ML research, piccolo/lento/economico. Angolo opposto del design space rispetto al G1-class dinamico dell'utente -> non e' la nostra via. (Conferma il vecchio appunto: Dynamixel = categoria sbagliata per noi.)

**EMAIL preparate (2026-06-20): ZeroErr, Leaderdrive, Honpine, Laifual** (turnkey torque-sensored harmonic: spec, torque sensor fisico vs encoder, datasheet+STEP, prezzo/MOQ/lead, EtherCAT/CAN, spedizione Italia).

**CHIARIMENTI CONTROLLO (2026-06-20, domande utente):**
- RL locomotion (Unitree/ToddlerBot/G1) = policy NN (MLP piccolo) con OSSERVAZIONI pos/vel giunto + IMU (NON coppia) -> target di POSIZIONE -> PD -> coppia applicata da corrente. **Nessun sensore di coppia, la coppia NON e' un input della policy.** Runtime = NN deterministico ~50-200 Hz + PD ~1 kHz. (Alternativa deterministica classica = ZMP/MPC model-based, stile ASIMO; il moderno e' la policy NN appresa.)
- G1 Unitree: NIENTE sensori coppia; robustezza = COMPLIANCE MECCANICA del QDD (backdrivabile), non dati di coppia. RobStride uguale, MA il QDD tiene la PORTA APERTA (corrente=coppia pulita -> puoi aggiungere force control/contact detection dopo). Encos planetario rigido CHIUDE quella porta.
- ACT / Diffusion Policy (manipolazione): dati = IMMAGINI + posizioni giunto -> azioni di POSIZIONE. Coppia NON usata (solo branch contact-rich la aggiunge). Posizione = spina dorsale, coppia = specializzazione opzionale.
- Encos "middle 25-36:1": BUONO per controllo di POSIZIONE (rigido a sufficienza, preciso, meno inerzia riflessa di un armonico); AWKWARD MIDDLE solo per FORCE control (troppo rigido per corrente=coppia come QDD, non auto-sensa per deflessione come armonico). Siccome RL cammina in POSIZIONE, Encos e' nel suo regime BUONO.

**RACCOMANDAZIONE AI (2026-06-20) - RAFFINATA dopo che l'utente ha chiarito l'OBIETTIVO: "umanoide che cammina (calmo) + manipola con policy ACT/diffusion".**
- MECCANISMO (chiarito all'utente): la policy emette sempre POSIZIONE; la differenza QDD vs alta-riduzione = quanto RIGIDO insegue. (1) Servo rigido (Dynamixel/Encos): loop di posizione brute-force, torque-accuracy IRRILEVANTE, giunto RIGIDO. (2) QDD + PD basso guadagno: coppia piccola ∝ errore = MOLLA cedevole; torque-accuracy SERVE (la coppia E' la molla). QDD = puoi DOSARE la rigidezza (rigido o compliant); alta-riduzione = SOLO rigido. ToddlerBot cammina rigido perche' piccolo(3.4kg)+piano+RL.
- SVOLTA: ACT/Diffusion emettono POSIZIONE e girano su hardware RIGIDO a posizione (ALOHA = bracci Dynamixel rigidi). RIGIDO = PIU' PRECISO in free-space (il QDD compliant CEDE/flette = meno preciso). Quindi per la MANIPOLAZIONE dell'utente, la rigidezza Encos e' un PREGIO. Cammino calmo = ok rigido.
- **Per l'obiettivo ESATTO dell'utente (cammino calmo + manipolazione ACT/diffusion in ambiente controllato) -> ENCOS e' il fit MIGLIORE**: preciso dove conta (manipolazione), compatto/elegante, zero sensori, cammino sufficiente. (Correzione del lean "RobStride" precedente, che valeva per capacita' DINAMICA non richiesta.)
- **RobStride SE** vuoi l'OPZIONE futura: locomozione robusta/dinamica (terreno vario, spinte, corsa) o manipolazione CONTACT-RICH (inserimento, contatto sicuro) -> solo il QDD permette di dosare compliance dopo. Bulkier, future-proof.
- DECISIONE NETTA aperta: massima precisione-manipolazione + compattezza ORA (Encos) vs poter diventare robusto/contact-capable/dinamico DOPO (RobStride). Per "walk + ACT/diffusion" come detto: lean ENCOS. (ZeroErr = fuori: pesante/caro/lento, e la sua compliance/torque non serve a una manipolazione a posizione.)
- STATO: ipotesi forte, NON ancora BOM. Confronto diretto vs piano Encos da fare. NON ho ancora ricostruito il foglio Excel per questa (offerto).

**OPZIONE RIVISITATA 2026-06-20: ZeroErr eRob (turnkey torque-sensored).** L'utente riapre ZeroErr come via "compra il giunto completo, zero DIY". Modulo eRob = motore frameless + armonico + DOPPIO encoder + TORQUE SENSOR + freno + driver, tutto integrato (CAN/EtherCAT). Lineup verificato (zeroerr.com): 70F Ø70/35Nm/0.77kg, 70I Ø70/70Nm/0.88kg, 80F Ø80/71Nm/0.89kg, 80I Ø80/112Nm/1.09kg, 90I Ø90/191Nm/1.64kg, 110I Ø110/408Nm/2.68kg; max 60 RPM (40 sui grossi). Serie T = versioni ad ANGOLO RETTO (piu' pesanti). **Minimo Ø70 -> NIENTE per il POLSO** (serve piccolo a parte: Steadywin GIM3510 Ø46 / RS05 Ø46 / Encos A2806 Ø44).
- Mapping utente: 70F caviglia, 80I knee/hip (lo "strong"), 70F/70I spalle/gomito/vita, polso = altro.
- VERDETTO ONESTO: risolve il sensing turnkey, MA = **opzione PIU' PESANTE e PIU' CARA**: ~19-21 kg di soli attuatori -> robot ~35-40 kg (piu' del G1!), prezzo premium (~$700-1500 cad, ~$20k+). CONTRADDICE il "light humanoid" e il rifiuto di Bota per peso/costo. 60 RPM = ok cammino calmo, borderline ginocchio cadenza normale. Vale solo se l'utente paga peso+soldi per azzerare ogni DIY.
- ALTERNATIVE stessa categoria (turnkey torque-sensored): **Honpine** (peer diretto, CN, piu' economico), **Leaderdrive** (= supplier RobotEra, gia' contattato), **Laifual**, **HEBI X-series** (US, SEA, API top, premium), **Innfos/DAMIAO SCA** (QDD, piu' leggero). Consiglio: quote Honpine+Leaderdrive prima di ZeroErr.
- EMAIL preparate per ZeroErr + Leaderdrive (spec+quote: torque sensor fisico vs encoder, datasheet+STEP, prezzo/MOQ/lead, EtherCAT/CAN, spedizione Italia).

**SPEC ENCOS (decode nome + dati trovati). NOME = EC-A[Ø statore][h statore]-[P plan / H arm][stadi]-[RIDUZIONE]; il numero
finale e' la RIDUZIONE, non la coppia. Coppia = motore x riduzione.**
- IMPORTANTE: il Ø nel nome e' lo STATORE; il MODULO reale e' piu' grosso. A6416 -> Ø88 (come RS06); A4310/A4315 -> **Ø56 (= come RS00 Ø57!)**; A2806 -> Ø44.

**SPEC REALI DAL DATASHEET V3.15EAP (letto 2026-06-19, basta stime):**
| Modello | Riduz | Ø mod | Lungh | Peso | Nom Nm | Picco Nm | Nom/Picco RPM | Kt | Nm/kg |
|---|---|---|---|---|---|---|---|---|---|
| EC-A2806-P2-36 | 36:1 | Ø44 | 44 | 162 g | 3 | 12 | 207/220 | 1.35 | 74 |
| EC-A4310-P2-36 | 36:1 | Ø56 | 60.5 | 382 g | 12 | 36 | 75/89* | 1.4 | 94 |
| EC-A4315-P2-36 | 36:1 | Ø56 | 69.5 | 485 g | 25 | 75 | 109/117 | 2.8 | **155** |
| EC-A6416-P2-25 | 25:1 | Ø88 | 67.5 | 805 g | 40 | 120 | 107/120 | 2.74 | 149 |

Tutti: doppio encoder, CAN/CAN FD 1M, cuscinetto cross-roller in uscita. *(A4310 misurato a 24V -> a 48V vel. ~1.5-2x.)*
- **3 SCOPERTE dal datasheet:** (1) A4310/A4315 sono **Ø56** (non Ø63 come stimavo) = come un RS00 -> vantaggio caviglia ANCORA piu' netto vs RS06 Ø88.
  (2) **A4315 = stesso Ø56 dell'A4310, +9mm/+103g, ma DOPPIA coppia (75 vs 36 Nm)** e densita' MAX 155 Nm/kg -> e' LA "2 modelli sempre 43" (A4310 leggero + A4315 forte, stesso diametro).
  (3) **A2806 esiste** (Ø44, 162g, 12Nm, 220 RPM): NON era a catalogo Foxtech -> opzione polso/mani "piccina" (3a taglia).
- GAMBE A6416 vs RS04 (datasheet): A6416 piu' piccolo (Ø88 vs Ø106), piu' leggero (805 vs 1420 g = **-3.7 kg sulle 6 giunture**), +coppia continua (40 vs 30 Nm);
  RS04 piu' veloce (~333 vs 120 RPM) e backdrivable (9:1 vs 25:1, inerzia riflessa ~8x meno). 120 RPM A6416 = 12.6 rad/s = OK cammino (anche trotto leggero), Encos NON e' lento come ZeroErr.
- DECISIONE TAGLIE APERTA: (A) 2 moduli A6416+A4310 (caviglia con A4310 36Nm al limite, o A6416 Ø88 grosso) | (B) 3 moduli +A4315 caviglia (Ø56/75Nm perfetta). Spec tecniche = ABBIAMO. Da chiedere a Foxtech: solo prezzo cad Italia + CAD STEP + lead time + MOQ.

**ENCOS ARMONICI (datasheet V3.15, letti 2026-06-19; tutti DOPPIO ENCODER + CAN/CAN-FD, backlash ~10 ARCSEC = 60x meno dei planetari):**
- A3814-H14-107: 107:1, Ø53x78.5, 434g, 20/60 Nm, 47/52 RPM, Kt 4.2. | A5013-H17-100: 100:1, Ø63x81.5, 630g, 30/90 Nm, 33/38 RPM, Kt 5.9. | A6013-H20-100: 100:1, Ø73x84, 906g, 40/130 Nm, 45/47 RPM, Kt 5.6.
- PUNTO CHIAVE: il flexspline armonico e' CEDEVOLE -> il doppio encoder PUO' stimare coppia da deflessione (come ZeroErr), cosa che sui planetari Encos (rigidi) NON funziona. MA: armonici LENTI (33-52 RPM, come ZeroErr) e Encos non da' funzione torque turnkey (DIY, marginale con encoder 0.1-0.2 deg). Sono quelli che Asimov usa su hip-roll/yaw/shoulder.

**PAPER "UKF Sensor Fusion for Joint-Torque SENSORLESS Humanoids" (Sorrentino/Romualdi/Pucci, IIT, ICRA 2024; arxiv 2402.18380; letto 2026-06-19) = POSSIBILE SOLUZIONE FORTE:**
- Stima le coppie di giunto SENZA sensori di coppia, fondendo (UKF) corrente motore + encoder + IMU + **F/T ai PIEDI**. Modella l'attrito del riduttore (Coulomb+viscoso). Gestisce contatti esterni (batte RNEA: 1.96 vs 18.3 Nm sotto contatto). RMSE 0.05-2.5 Nm. Testato su ergoCub. **CODICE OPEN-SOURCE** (github ami-iit).
- PER NOI: invece di vestire 10-18 giunti, GRF al piede + corrente+encoder Encos (gia' c'e') + IMU -> osservatore stima TUTTE le coppie. Sidestep totale della vestizione. Costo = software + identificazione attrito (i controllisti dell'utente). Caveat: validato su robot su palo (non camminata libera ancora), serve buon modello attrito, accuratezza < sensore dedicato (ok gambe, per manipolazione fine forse sensori dopo). = la "4a carta" ora concreta e provata.
- REPO (github ami-iit/paper_sorrentino_2024_icra...): Python su **bipedal-locomotion-framework** (IIT), dataset+esempio ergoCub gamba dx. Per portarlo: URDF nostro + framework + dataset loggato dai nostri motori + **identificazione attrito per giunto** + tuning covarianze UKF. Lavoro sw definito (roba da controllisti), MA il pezzo difficile (lo stimatore) e' gia' scritto e open.
- ergoCub (robot del paper) = ARMONICO + frameless (IIT-custom, come RobotEra; paper attrito armonici arxiv 2410.12685). ATTENZIONE: il modello d'attrito UKF e' per ARMONICI; i nostri Encos sono PLANETARI -> ri-identificare l'attrito (il metodo generalizza: tau_j = rid*tau_m - tau_attrito).
- **BOTA SCARTATO dall'utente 2026-06-19 (costo + PESO distale).** Sostituto: il paper vuole soprattutto **forza verticale + centro di pressione (ZMP)** al piede -> bastano **4 celle di carico agli angoli del piede**, o meglio **estensimetri sulla PIASTRA del piede** (gia' c'e' -> ~zero massa, ~50 EUR di gauge). Da' Fz+2 momenti (il grosso del wrench); manca lo shear orizzontale (secondario su piano). Approccio humanoid standard (4 load cell).

**CORREZIONE 2026-06-19 "armonici/ZeroErr troppo lenti" = ERA TROPPO ASSOLUTO.** Dipende dalla cadenza. Giunto critico = GINOCCHIO in swing: cadenza NORMALE ~50-67 RPM, cadenza LENTA ~25-40 RPM.
- ZeroErr 60 RPM = borderline a cadenza normale, ok lento. Encos-H 38-52 RPM = sotto a cadenza normale (ginocchio), ok lento. NON un "troppo lento" piatto.
- I VERI motivi per NON mettere armonici alle gambe restano: (1) INERZIA RIFLESSA ∝ rid^2: 100:1 armonico riflette ~10.000x (vs 625x del nostro planetario 25:1, 81x del QDD 9:1) -> gambe sorde agli urti/disturbi se non aggiungi una molla SEA (trucco ANYmal); (2) ZeroErr Ø70 troppo grosso/pesante per caviglia. Il nostro A6416 PLANETARIO (120 RPM, 625x) = piu' margine di velocita' E meno inerzia riflessa -> scelta giusta per le gambe.
- "Stima coppia da doppio-encoder marginale per encoder 0.1-0.2 deg" = FACILE da provare (sw, gratis), DIFFICILE da rendere usabile: segnale (windup armonico 0.2-0.5 deg a coppia piena) / rumore (diff. 2 encoder ~0.15-0.3 deg) = solo 1-3x a pieno carico, SOTTO rumore a coppia bassa/media -> stima grezza (ok collision detection, inutile per force control fine). ZeroErr ci riesce con encoder migliori + calibrazione stiffness/isteresi. Sui PLANETARI Encos non funziona del tutto (rigidi).

**CONFRONTO MARCHE per marca-unica (ricerca 2026-06-17, IMPORTANTE):**
- **CubeMars HA UN BUCO nel mid ~36 Nm**: salta da AK40-10 (Ø46, 4 Nm) ad AK70-10 (Ø89, 25 Nm) / AK10-9 (Ø98, 50 Nm,
  940 g!). Niente di compatto a 36 Nm. Il nostro robot ha ~14 giunti da 36 Nm (caviglia4+hip-yaw2+vita2+spalle6) ->
  con CubeMars sarebbero tutti Ø89-98 = ASSURDO. **All-CubeMars SCARTATO** (buono solo polso AK40 + gambe AKE90).
- Compattezza a 36 Nm: **Encos A4310 Ø56 < Steadywin GIM6010-36 Ø70 (ma 36:1 rigido) < RobStride RS06 Ø88 < CubeMars Ø98.**
  Encos vince proprio dove abbiamo piu' motori. RobStride = famiglia COMPLETA senza buchi (RS00->RS06->RS04).
- CubeMars NON fu scartato per controllo (mia confusione utente): fu tolto per ECOSISTEMA UNICO (riga 215). Il problema
  di controllo era l'RS01 (encoder SINGOLO). CubeMars con versioni DUAL-encoder (AK10-9 v3) e' ok. Regola universale:
  prendere SEMPRE la versione a 2 encoder, di qualunque marca (vale RS01 vs RS02, base-AK vs AK-dual, ecc.).
- FOXTECH RESPONSIVE: ha risposto subito (mail + WhatsApp), datasheet+CAD in arrivo -> il sourcing Encos NON e' il
  patimento temuto. Resta da valutare solo la RIDUZIONE (sotto).

**MIT CHEETAH = origine del QDD (background per l'intervista utente, 2026-06-19):** Lab = MIT Biomimetic Robotics, PI **Sangbae Kim**.
Robot Cheetah 1/2/3 -> **Mini Cheetah (2019)**. Idea pionieristica = "ATTUAZIONE PROPRIOCETTIVA": motore BLDC ad alto raggio di traferro +
riduzione SINGOLA bassa (~6:1, "quasi"-direct-drive) -> trasmissione BACKDRIVABLE, inerzia riflessa minima (∝ N^2) = mitiga gli urti, e
**coppia di giunto = Kt*I*N letta dalla CORRENTE, senza sensore di coppia**. Paper canonico = **Wensing, Wang, Seok, Otten, Lang, Kim,
"Proprioceptive Actuator Design in the MIT Cheetah", IEEE T-RO 2017** (+ Seok et al. T-Mech 2015 sull'efficienza). **Ben Katz (tesi MS 2018)**
= attuatore QDD modulare low-cost + il "MIT mode" CAN (pacchetto pos/vel/torque-ff/Kp/Kd). DA LI' discendono CubeMars/T-Motor AK, **RobStride**,
Damiao, MyActuator e i motori Unitree - e tutti parlano il "MIT mode" (anche l'Encos lo implementa). PUNCHLINE intervista: RobStride (~9:1) =
la filosofia MIT-Cheetah pura (corrente=coppia); Encos (25-36:1) = ALLONTANAMENTO dal QDD (compatto) che per riavere il force control deve
RI-AGGIUNGERE il sensore di coppia (come Tesla: alta riduzione + torque sensor). OpenTorque (Gabrael Levine) = lo schema MIT QDD + molla SEA.

**VERDETTO RIDUZIONE per la CAMMINATA (ricerca 2026-06-17, paper QDD/biomimetics MIT) - DECISIVO:**
- QDD sweet-spot = **6-9:1**; RobStride (~9:1) e' proprio li'. La ricerca dice "9:1 = equilibrio tra densita' di coppia
  e mitigazione impatti per la camminata dinamica".
- **Inerzia riflessa ∝ riduzione².** Quindi vs RobStride 9:1: **Encos 25:1 = ~8x inerzia riflessa, 36:1 = ~16x.** NON marginale.
- Effetto: piu' riduzione -> meno backdrivable, meno responsivo agli urti, peggio a regolare il contatto. La ricerca:
  "20-30:1 aumenta molto l'inerzia riflessa e riduce la risposta agli impatti".
- VERDETTO: Encos 25-36:1 **PUO' camminare** (lenta, piana, tethered = il nostro caso) ma e' un **vero passo indietro
  vs 9:1, non marginale.** Il punto PEGGIORE = la **caviglia a 36:1** (giunto d'impatto/contatto: heel-strike, terreno).
  -> Per QUALITA' di camminata RobStride 9:1 e' genuinamente meglio; la compattezza Encos la paghi in compliance/impatti.
  Se vai Encos, valuta un motore a BASSA riduzione almeno sulla CAVIGLIA (RobStride o opzione 1-stadio), li' i 36:1 fanno male.

**RISOLUZIONE "ma Tesla cammina da Dio con alta riduzione!" (2026-06-17, VERIFICATO) - chiude la scelta marca:**
Tesla Optimus = alta riduzione (vite a rulli, NON backdrivable) MA con **SENSORE DI COPPIA non-contact in OGNI attuatore**
+ sensori di posizione in INGRESSO e USCITA -> force control ATTIVO (misura la forza reale all'uscita, controlla veloce).
Quindi ci sono DUE strade per camminare bene: (a) **QDD bassa riduzione** (RobStride ~9:1 / Unitree / MIT) = force control
per TRASPARENZA, GRATIS, niente sensore; (b) **alta riduzione + SENSORE di coppia** (Tesla) = force control attivo.
ENCOS e' alta riduzione (25-36:1) **MA SENZA sensore di coppia** (solo dual-encoder, scarso per stimare coppia su un
planetario rigido) -> non puo' fare NE' l'uno NE' l'altro = il compromesso che cammina PEGGIO dei due.
**CONCLUSIONE (decisiva, un po' ironica):** per "camminare come gli umanoidi del FUTURO" con roba ACCESSIBILE (niente
team di controllo Tesla, approccio RL), la strada e' il **QDD bassa-riduzione = RobStride (9:1)**, che e' ESATTAMENTE
cio' che usano **Unitree G1/H2** (i migliori camminatori accessibili: capriole, corsa, tutto RL). Il "futuribile che
cammina bene" si ottiene con RobStride, NON con l'Encos. Encos = solo se vuoi compatto e accetti camminata meno morbida.
La via Tesla (alta riduzione + sensore di coppia integrato) NON e' accessibile: attuatori col torque-sensor costano un
occhio e l'Encos non li ha.

**AGGIORNAMENTO 2026-06-19 (intervista utente + scelta sensore) - "magnetico" sono DUE cose diverse, distinzione CHIAVE:**
- TESLA confermato (web): rotary = motore frameless + **riduttore ARMONICO** + **torque sensor non-contact** + encoder + cross-roller;
  linear = vite a rulli planetaria. Quindi Tesla = ALTA RIDUZIONE (NON QDD) + sensore di coppia non-contact (famiglia MAGNETOELASTICA).
  E' ESATTAMENTE il campo dove va l'utente con Encos+sensore: l'Encos+magnetico = versione DIY/economica della ricetta Tesla.
- FIGURE: architettura attuatori NON divulgata; fonti secondarie dicono "QDD" ma poco affidabili (le stesse sbagliano dicendo Tesla=QDD). Non affermare numeri.
- QDD camp (corrente=coppia, niente sensore) = Unitree G1/H1 (= lineage RobStride), MIT Cheetah. POLO opposto a Tesla.
- **"MAGNETICO" = 2 sensori diversi:** (a) **doppio encoder magnetico su flexure di torsione** = LEGGERO/ECONOMICO/DIY (~$30-50/giunto,
  AS5047/MT6701), MA per avere segnale serve twist ~1-2 deg a fondo scala -> flexure CEDEVOLE (~2000 Nm/rad) -> il giunto diventa un
  **SEA rigido** (compliance ok/utile per camminare, NON per manipolazione rigida). (b) **MAGNETOELASTICO** (NCTE/Magcanica, = Tesla):
  non-contact, shaft RIGIDO (niente compliance), elegante MA DIY = ricerca (magnetizzazione shaft, fluxgate, temp/isteresi) -> di fatto si COMPRA.
- L'utente ha capito bene: i sensori ready-made grossi (Bota/FUTEK flangia) RI-BLOATANO i giunti in-linea (knee/hip) = rovinano il vantaggio Encos.
  ECCEZIONE = il PIEDE: li' vuoi F/T 6-assi comunque (GRF/ZMP), monta SOTTO la caviglia, e sono solo 2 -> Bota Rokubi ai piedi resta giustificato.
- LEAN UTENTE = via magnetica (a) = SEA rigido leggero/economico sui giunti gamba. 4a CARTA (controllisti): stima coppia MODEL/LEARNING-based dal
  solo dual-encoder + modello attrito (zero hardware, arxiv 2410.16591) -> prototipare A/B vs il flexure. NB: la (a) e' SEA, non il sensore rigido di Tesla.

**CHI USA COSA - sensing di coppia per marca (web 2026-06-19). CORREZIONE di una mia SOVRA-GENERALIZZAZIONE: NON e' vero che "quasi tutti i giunti premium usano estensimetri".**
- ESTENSIMETRI su elemento dedicato all'uscita harmonic = standard nei BRACCI COLLABORATIVI premium: **DLR LWR -> KUKA LBR iiwa, Franka Emika Panda** (torque sensor in OGNI giunto);
  UR/Yaskawa/Fanuc (F/T a flangia/base). Sono BRACCI, non umanoidi. (NON instrumentano un pezzo a caso: razza/anello DEDICATO all'uscita del riduttore.)
- **ANYmal (ANYbotics/ETH) = SEA, NON estensimetri**: motore + harmonic + MOLLA in serie + 2 encoder assoluti (pos uscita + deflessione molla) -> coppia da deflessione.
  Ris. coppia ~8 mNm, pos 0.025 deg, +protezione impatti. = analogo PIU' VICINO al piano Encos+magnetico-deflessione dell'utente (alta riduzione + lettura deflessione).
  PAPER: Hutter et al., "ANYmal - A Highly Mobile and Dynamic Quadrupedal Robot", IROS 2016 (DOI 10.1109/IROS.2016.7758092; open access SciSpace/ETH). Bonus: arxiv 2511.06796 "Human-Level Actuation for Humanoids".
- TESLA = magnetoelastico non-contact. UNITREE(G1/H1)/MIT = QDD da corrente (NESSUN sensore). Molti umanoidi = SENSORLESS (stima da osservatore/learning: UKF arxiv 2402.18380, PINN 2507.10105).
- **RobotEra = motori LEADERDRIVE (detto dall'utente, che POSSIEDE il robot; web 2026-06-19 conferma): Leaderdrive = ARMONICO (strain-wave), uno dei 2 big cinesi con Laifual.**
  Rapporti 30-500:1 (moduli giunto tipici 50-160:1) -> RobotEra = ALTA RIDUZIONE ARMONICA = campo GEARED (Tesla/ANYmal/DLR), NON QDD Unitree. Conferma: l'utente sente i giunti
  (a motore spento) "muovibili ma con resistenza, non liberi" = coerente con armonico, NON col QDD 9:1 (che gira quasi libero). NB: il test a motore SPENTO dice solo la MECCANICA
  (geared vs QDD), NON se c'e' un sensore di coppia (= comportamento attivo, a motore ACCESO). Leaderdrive offre moduli con torque-sensor INTEGRATO opzionale; inoltre il flexspline armonico
  e' cedevole -> stima coppia da doppio-encoder FUNZIONA (a differenza del planetario Encos rigido). Sensore RobotEra = da confermare col MODELLO esatto / SDK (campo coppia misurata vs corrente).
  IMPLICAZIONE per noi: RobotEra valida la via compatta ad alta riduzione per un umanoide serio, MA loro = ARMONICO (torque-sensing facile via flexspline) vs noi = PLANETARIO rigido (sensore da AGGIUNGERE). Tradeoff reale.
- **X-Humanoid/Tiangong(TienKung): tipo di sensore NON pubblico** (cercato, non trovato; NON inventare). Tiangong parz. OPEN-SOURCE -> si puo' cercare nei loro repo/SDK.
- NET: non esiste "lo fanno tutti cosi'". Bracci->gauge; ANYmal->SEA; Tesla->magnetoelastico; Unitree->niente. I 3 metodi candidati hanno ciascuno un precedente premium -> scegliere sui NOSTRI vincoli, non per imitazione.

**CORREZIONE 2026-06-17 (l'utente dice di poter avere i controllisti): riapre l'Encos.** (1) Ero troppo tranchant su
"Encos senza sensore": il DUAL-ENCODER e' proprio per stimare la coppia (posizione motore vs uscita -> deflessione sul
riduttore = coppia). Su planetario rigido il segnale e' rumoroso ma C'E', ed e' cio' che un bravo controllista sfrutta
(+ modelli attrito). (2) SPETTRO: Encos+sola corrente = force control scarso; Encos+dual-encoder+bravi controllisti =
DECENTE (cammina bene); Encos + SENSORE di coppia dedicato aggiunto = Tesla-grade. RobStride QDD 9:1 = buono out-of-the-box
con poco sforzo di controllo. (3) Per Tesla-grade aggiungere coppia VERA: load-cell di reazione a ogni giunto, OPPURE
SEA (elemento elastico in serie -> il dual-encoder legge la molla = coppia pulita, costa banda/rigidezza), OPPURE attuatori
col torque-sensor integrato (cari, non Encos). (4) CONCLUSIONE aggiornata: SE l'utente ha davvero il team di controllo,
l'Encos compatto + dual-encoder + controllo torna scelta valida per "piccolo + cammina bene"; i torque-sensor si aggiungono
al passaggio HW. In sim (adesso) il force control si modella comunque -> si puo' procedere col CAD senza decidere oggi i
sensori. Resta il bivio: QDD/RobStride (semplice, grosso) vs Encos+controllo (compatto, piu' lavoro di controllo).

**APPROFONDIMENTO 2026-06-17 (verificato, RIDIMENSIONA la stima da dual-encoder):** la ricerca conferma che sulle ALTE
riduzioni l'attrito del riduttore rende INAFFIDABILE la stima di coppia da corrente -> servono estensimetri dedicati. Il
dual-encoder stima la coppia dalla DEFLESSIONE: decente su ARMONICO (flexspline cedevole), **SCARSO su PLANETARIO rigido**
(A4310/A6416 = quasi tutti i nostri: deflessione minima + non cattura l'attrito). Quindi il dual-encoder Encos **NON
sostituisce un sensore di coppia** sui planetari (avevo sovrastimato). Steadywin GIM3510 = dual-encoder SI + **8:1 bassa
riduzione** -> li' la stima da CORRENTE funziona (quasi QDD), force control ok. Vs sensore vero: estensimetro ~1-2% errore,
banda alta, cattura l'attrito; la deflessione su planetario e' rumorosa e sistematicamente sbagliata -> non paragonabile.
**MOTORI gia' col sensore di coppia INTEGRATO (trovati ma PREMIUM, ~1000-3000 EUR/giunto -> 30 giunti = 30-90k):**
SensoDrive SENSO-Joint (DE: sensore+HarmonicDrive+motore+driver, certificato, 5 taglie), TQ-RoboDrive ILM (DE, eredita'
DLR), Kinova (torque-sensored ma venduti come bracci), Harmonic Drive FHA. **NON esiste un attuatore col torque-sensor
integrato ED economico** (CubeMars/Unitree/RobStride/Encos = corrente+encoder, niente sensore).
**REGOLA FINALE - pick 2 su 3:** piccolo+economico = force control MEDIOCRE; piccolo+force-control-TOP = CARO (Encos+sensori
o SensoDrive); economico+force-control-BUONO = piu' GROSSO (RobStride QDD 9:1, corrente basta come Unitree). I controllisti
dell'utente NON bastano da soli: serve il SEGNALE di coppia = HARDWARE (sensore), o caro o DIY estensimetri x30.

**OPZIONE 1 PREFERITA dall'utente (2026-06-17): ENCOS compatto + VESTIZIONE coppia DIY (l'utente conosce ragazzi che la
sanno fare, da confermare).** Non servono 30 sensori, solo i giunti GAMBA dove il force control conta. PRIORITA':
1) CAVIGLIA (4: pitch+roll x2) = giunto di contatto + il piu' rigido (36:1), il piu' importante. Meglio ancora un SEA
(elemento elastico in serie): il dual-encoder legge la molla = coppia pulita E assorbe l'urto -> 2 piccioni. 2) GINOCCHIO
(2) + HIP PITCH (2). 3) HIP ROLL (2). -> set "cammina bene" = 10 giunti (gambe escluso hip yaw). NON sensorizzare: hip
yaw (gravita 0), POLSO (Steadywin 8:1 bassa riduzione, la corrente gia' basta), collo, spalle/gomito (opzionali per
manipolazione fine, dopo). Componenti sensore DIY: Bota Systems (F/T 6 assi), FUTEK (torque sensor).

**VESTIZIONE - METODI DIY concreti (2026-06-19, domanda utente "se voglio farlo da solo come si fa"):** principio = aggiungere
un elemento che si deforma in modo MISURABILE tra uscita riduttore e link (il dual-encoder interno NON basta: deflessione < rumore). 3 vie:
1) FLANGIA ESTENSIMETRICA: disco a razze (taglio), 4 gauge a +-45 in ponte di Wheatstone COMPLETO (rigetta flex/assiale/temp),
   dim. per ~1000-1500 ue a fondo scala; ampli INA826/AD8421 + ADC 24-bit (ADS1235/1262) a >=1 kHz -> CAN. Rigido, banda alta;
   incollaggio = arte. Niente slip-ring se ROM limitato (ansa cavo). E' cio' che intendono i suoi amici. (HX711 solo proto, lento.)
2) SEA (molla nota + 2 encoder, tipo ANYmal ANYdrive): molla torsionale -> a fondo scala 5-15 deg = deflessione GRANDE, letta da
   2 encoder magnetici 14-bit (AS5047/MT6701), niente gauge. +PROTEZIONE IMPATTI (oro su gamba). Costa banda posizione + risonanza.
   RIFERIMENTO DIY perfetto: **OpenTorque Actuator** (Gabrael Levine, open-source QDD+SEA per gambe).
3) TORSIONE MAGNETICA NON-CONTATTO: barra di torsione + encoder magnetico ai 2 capi, differenza angoli = twist (tara ~1-3 deg a
   fondo scala). Via di mezzo (no incollaggi/slip-ring); sensibile a concentricita'/temperatura. E' la "via Tesla" semplificata.
INTEGRAZIONE: l'Encos in MIT-mode NON regala il loop di coppia -> lo chiudi TU (leggi stato via CAN + sensore -> comandi corrente/Tff)
a ~1 kHz, bassa latenza, sensore sincronizzato con la telemetria. DIFFICOLTA': 1 giunto = 1-2 settimane (chi sa estensimetrare);
~18 giunti = sotto-progetto da mesi = IL lavoro che RobStride 9:1 si risparmia. Strategia solo: prototipa 1 giunto gamba, SEA sulle
gambe, braccia a corrente all'inizio. Massa distale del sensore conta (sul piede).
**READY-TO-MOUNT (buy & bolt-on, NO DIY; richiesti dall'utente 2026-06-19):** PRIMA SCELTA = **Bota Systems (CH, spin-off ETH)**: F/T 6-assi
robot-grade, CAN-FD/EtherCAT/ROS -> **Rokubi** (gambe/caviglia = forza di reazione al suolo; manipolazione), **PixONE** (giunti umanoidi),
**MiniONE** (30 g, polpastrelli/mani). Al PIEDE e alle MANI vuoi comunque F/T a 6 assi (GRF/ZMP, contatto) -> Bota li'. Per coppia 1-asse a
ginocchio/anca/vita = flangia cava: **Sunrise Instruments** (CN, valore) / **FUTEK** (US, facile da ordinare) / **ME-Mess.** (DE) / **HBK-Kistler**
(metrologia premium). Non-contatto magnetoelastico (no molla/incollaggio): **NCTE** (DE) / **Magcanica** (US). Costo ready-made ~$1-3k/giunto x ~10 = $10-30k.

**MOTORI GIA' "VESTITI" col sensore di coppia, ready-made (2026-06-17, scoperti con l'utente):**
- **ZeroErr eRob** (I-type, taglie 70I/80I/90I/110I = Ø70-110): ARMONICO + dual-encoder + "VIRTUAL torque sensor"
  (stima coppia da deflessione flexspline + modello stiffness/hysteresis). EU-cert + prima CR-cert per giunti umanoidi.
  PLUG-AND-PLAY, niente DIY. INSIGHT chiave: il virtual-torque-sensor da dual-encoder FUNZIONA sull'ARMONICO (flexspline
  cedevole = deflessione misurabile), ed e' SCARSO sul planetario rigido -> quindi gli ARMONICI (ZeroErr, o gli Encos-H
  A3814/A5013) danno torque sensing "gratis"; i planetari (A4310/A6416) no. PERO' armonico = alta riduzione = alta inerzia
  riflessa = camminata CONTROLLATA/precisa (stile Tesla/Figure/DLR-HRP), NON dinamica come il QDD. Premium di prezzo.
- Honpine / Makongear / Oz Robotics: armonici cinesi con torque-sensor FISICO ma customizable (MOQ, non a scaffale), piu'
  economici di ZeroErr, meno plug-and-play. SensoDrive/TQ/Kinova/HarmonicDrive = premium tedeschi (gia' in lista sopra).
- DAMIAO (Dynamic-Motion) DM-J4310-2EC: QDD economico ($116) dual-encoder MIT-mode -> e' nel campo QDD (come RobStride),
  NON ha sensore di coppia fisico. (Damiao era gia' stato escluso per ecosistema-unico.)

**SCHEDE EXCEL: ora 4 fogli motori - "umanoide" (BOM RobStride completo), "MOTORI RobStride" (lista motori pulita),
"MOTORI Encos (quote)" (3 modelli: A6416/A4315/A2806), "MOTORI premium" (mix CubeMars/Encos).**
**VERSIONE INGLESE (per intervista utente lun 2026-06-22): script SEPARATO build_umanoide_en.py -> "BOM umanoide G1 - EN.xlsx",**
**5 fogli: Summary | Joint map (30 DOF) | Motors-Encos (chosen) | Motors-RobStride (alt) | Torque sensing. Da tenere in sync a mano con quello IT.**

**TRE CAMPI DI CAMMINATA (sintesi):** (a) QDD bassa-rid (RobStride/Unitree) = dinamico/agile, force control da corrente,
economico, piu' grosso; (b) ARMONICO+virtual-torque (ZeroErr / Encos-H) = camminata controllata-precisa stile Tesla/
Figure, ready-made ma premium, meno dinamico (inerzia riflessa); (c) PLANETARIO+DIY-sensori (Encos-P + estensimetri) =
compatto ma tanto lavoro. Per "Unitree-dinamico" -> (a). Per "Tesla/Figure-controllato compatto" -> (b) ZeroErr.

**ZeroErr CADUTO per le GAMBE (2026-06-17, dalla pagina ufficiale eRob):** lineup eRob 70F(Ø70,35Nm,0.77kg)/70I(70Nm,
0.88kg)/80I(Ø80,112Nm,1.09kg)/90I(Ø90,191Nm,1.64kg)/110I(Ø110,408Nm,2.68kg)... MA **velocita' MAX = 60 RPM** (tutti).
Il ginocchio in camminata normale tocca ~300-400 gradi/s = 50-67 RPM -> ZeroErr e' GIA' al limite per camminare piano,
troppo lento per dinamica. Sono attuatori da COBOT di precisione, NON da locomozione. E sotto Ø70 non esiste (niente polso).
Inoltre ZeroErr != Tesla: Tesla usa VITI A RULLI (veloci) + sensore; ZeroErr usa ARMONICO (lento). -> ZeroErr fuori dalle
gambe. Per camminare serve VELOCITA' = bassa riduzione = QDD. CONCLUSIONE: il default sano e' RobStride QDD (veloce/dinamico,
force control da corrente, economico, completo); l'unica alternativa = Encos+sensori-DIY se il compatto vale il lavoro.

**MANUALE UFFICIALE ENCOS letto (Motor Debugging Manual V1.18, 2026-06-17) - CONFERMA e RAFFORZA:**
- ENCODER: doppio (motore + uscita), 14-bit, MA accuratezza reale solo **0.1-0.2 gradi** ("quality issues"). -> la
  deflessione su un planetario rigido (a coppia nominale) e' minima e VIENE SOMMERSA dall'errore encoder (0.1-0.2 deg) ->
  **la stima di coppia da dual-encoder NON e' usabile sull'Encos planetario** (confermato: avevo ragione a ridimensionarla).
  Output encoder single-turn (perde i giri allo spegnimento).
- CONTROLLO: ha MIT mode (Power-Position Mixed: i=(Kp*(p_des-p)+Kd*(v_des-v)+Tff)/Kt, "per foot-type robots") + Current/
  Torque mode + Servo pos/speed. MA la **coppia e' SEMPRE da CORRENTE x Kt (open-loop), NESSUN sensore di coppia**. Force
  control = come RobStride (da corrente) -> sull'alta riduzione e' inaffidabile per l'attrito -> per coppia vera SERVE un
  sensore FISICO aggiunto (la vestizione DIY e' obbligatoria, il dual-encoder NON la sostituisce). CAN 1M, 2 kHz, fb 0.4ms.
- TERMICO: derating coppia sopra 105 gradi C bobina (max 120 stop); l'alta coppia continua scalda -> derating. XT30 15A/30A
  picco; SERVONO condensatori per l'energy-return (regen) o si brucia il driver. Tensione 20-57V.
- MODELLI nel manuale = EC-4310 / 8112 / 10020-24 / 13715 / 13720 (serie P planetaria). Gli A6416/A4315/A5013-H/A3814-H di
  Asimov NON sono nel manuale -> potrebbero essere CUSTOM/non-standard: VERIFICARE disponibilita' con Foxtech (il catalogo
  standard gambe e' A8112 94Nm / A10020 150Nm). Per il debug VESC serve cacciavite M2 per aprire il retro su 4310/8112/10020/13715/13720.

**CORREZIONE "gambe = Ø100 obbligato" (ERRATA):** Asimov fa hip pitch + waist in **Ø64** (A6416, planetario 25:1) su
35 kg, "fino a 120 Nm picco". Le gambe NON devono essere Ø100: con riduzione piu' alta (25:1 o armonico) si fanno
~120 Nm in **Ø64**, meno backdrivable ma OK per SOLO CAMMINO. Il nostro tethered (~28-30 kg) ci sta. -> gambe eleganti
Ø64 possibili. L'armonico (H) Encos da' alta riduzione + ZERO gioco in frame piccoli (Ø38-50): ottimo per giunti compatti.

**Range giunti Asimov (dal sim):** hip pitch -120/+57, hip roll/yaw ±45, knee 0-86, ankle pitch ±20 / roll ±5.7 (PICCOLI),
waist yaw ±90, shoulder pitch -50/+180, elbow 0-140, wrist yaw ±180 (gradi). NB la caviglia Asimov ha range piu' ridotto del nostro.

## Metodo di calcolo coppie + verifica finale post-downsizing (2026-06-08)

**Come calcolare la coppia richiesta a un giunto (per AI e per ogni ricalcolo).** Regola base: hold continuo ->
confronta col NOMINALE; movimento/picco breve -> confronta col PICCO. Un motore "regge" se statico < nominale E
dinamico < picco.

1. STATICO (tenere fermo nella posa peggiore): `tau_stat = g * SOMMA(m_i * b_i)`, con `b_i` = braccio di leva
   ORIZZONTALE della massa i dall'asse del giunto nella posa peggiore. g = 9.81.
2. DINAMICO (bang-bang: accelera meta corsa, decelera meta): `tau_dyn = tau_stat + I*alpha`, con `I = SOMMA(m_i * b_i^2)`
   e `alpha = 4*theta / t^2` (theta = ampiezza in rad, t = tempo). Velocita realistiche: 90 gradi in 0.5 s = moderato;
   0.3 s = veloce (la manipolazione non lo richiede); 0.8 s = lento.
3. ASSI VERTICALI (yaw): gravita ~= 0 -> solo dinamica (inerzia attorno alla verticale).
4. LEVERAGGI (caviglia, vita a puntoni): la coppia al GIUNTO e fissa dal carico; `tau_motore = tau_giunto *
   (crank_motore/crank_piede)`, poi / n motori che condividono. A 1:1 con 2 motori -> tau_giunto/2 a motore.

**Input usati.**
- Masse motori (diventano bracci di leva quando sono distali): RS00 0.310, RS02 0.405, RS04 1.420, RS05 0.191,
  RS06 0.621 kg.
- POSIZIONI GIUNTI dal G1 mode_11 (`g1_joints.csv`) -> danno i bracci. Es. braccio: spalla->spalla_yaw 0.106,
  spalla->gomito **0.187** (proiezione a braccio TESO, non i 16 mm a riposo!), spalla->polsi 0.287/0.325/0.371,
  spalla->mano 0.412 m; gomito->payload 0.22 m.
- Masse segmenti stimate PA-CF: omero ~0.30, avambraccio ~0.25, mano ~0.30 kg.
- Masse globali: robot ~35 kg; gamba sotto il pitch ~7.0 kg (CoM 0.305 m sotto l'asse); upper body sopra la vita
  ~10-14 kg (dipende dalla batteria, CoM ~0.25 m sopra il giunto); braccio sotto la spalla ~2.9 kg.

**Pose peggiori considerate per giunto (cosa entra nel conto).**
- Spalla pitch: BRACCIO DISTESO ORIZZONTALE in avanti, ogni massa al suo braccio, incluso il motore gomito (0.405 kg
  a 0.187 m: si solleva) -> 6.3 Nm statici.
- Spalla roll: braccio disteso orizzontale di lato (abduzione) = uguale al pitch.
- Spalla yaw: braccio ALZATO, payload 2 kg a 0.20 m dall'asse omero (a braccio basso la gravita e 0).
- Gomito: avambraccio a 90 gradi, payload a 0.22 m dal gomito.
- Hip pitch: gamba a sbalzo orizzontale, CoM gamba 0.305 m sotto l'asse.
- Hip roll: monoappoggio, massa sopra l'anca ~28 kg x offset laterale 0.10 m.
- Knee: squat, peso robot x braccio (0.04 dritto / 0.15 mezzo / 0.22 profondo).
- Ankle: ribaltamento, peso robot x leva caviglia-punta 0.13 m = ~46 Nm al giunto, /2 motori (a 1:1).
- Waist pitch/roll: upper body x 0.25 m x sin(piega), /2 puntoni.
- Yaw (hip/waist/shoulder): gravita 0, solo dinamica (girata/torsione).

**Esiti coi motori finali** (stat% sul nominale, din% sul picco):

| Giunto | Motore | Esito | Numeri |
|---|---|---|---|
| Hip pitch/roll | RS04 | OK | stat 52-69%, din 58-75% (max RobStride, 86% del G1) |
| Hip yaw | RS06 | OK/TIGHT | ~28 Nm a massa G1 = 78% picco; ~37 Nm se scalato a 46 kg = oltre il picco |
| Knee | RS04 | ATTENZIONE | in piedi/cammina OK (34%); squat profondo TENUTO 129-189% nom (max motor, limite inerente) |
| Ankle pitch/roll | RS06, uno per asse | OK con CAD | 36 Nm picco vs 35 G1; cammino normale stimato 17-32 Nm. Caso bordo punta 45-59 Nm: serve vantaggio meccanico o va evitato |
| Waist yaw | RS06 | OK/TIGHT | ~28 Nm a massa G1 < 36 picco; asse verticale, nessun carico gravitazionale |
| Waist roll | RS03 | OK | 12-17 Nm stimati a 30 gradi < 20 nominali; 21-30 Nm a 60 gradi solo intermittenti < 60 picco |
| Waist pitch | nessuno | RIMOSSO | il pitch del busto viene dagli hip pitch, scelta Figure-like |
| Spalla pitch/roll | RS06 | OK/TIGHT | ~10.8 Nm statici con braccio orizzontale + payload 1 kg, appena sotto 11 nominali; 36 picco > 25 G1 |
| Spalla yaw | RS00 | OK per 1 kg | ~21 N per mano continui al braccio G1 da 0.24 m; circa 1 kg di box affidabile con attrito e SF2 |
| Gomito | RS06 | OK | ~4.4 Nm statici con 1 kg, ~6.6 Nm con 2 kg < 11 nominali |
| Polso x3 | RS00 | OK | 51% nom con 2 kg in mano |
| Collo x2 | RS05 | OK | testa 1.5 kg, 46% nom |

**3 regole d'uso perche tutto regga:** (1) gambe quasi dritte, niente squat profondo tenuto; (2) batteria BASSA nel
bacino + non tenere il busto piegato a lungo; (3) braccia <=1.5 kg comodi / 2 kg a velocita moderata, niente fling.

**2 verifiche obbligatorie in CAD:** (a) rapporto crank caviglia >=1:1; (b) rapporto crank vita pitch/roll + posizione
batteria (decidono se RS06 basta o serve RS03). Riserve gia in BOM: vita->RS03, gomito->RS06. Nessun motore e bocciato
per l'uso non-acrobatico previsto; le gambe (RS04 non declassati) reggono in piedi e in camminata.

## Regola montaggio motori (decisione utente 2026-06-08)

**TUTTI i motori si montano dal DAVANTI (faccia uscita).** Universale: ogni QDD esce dal davanti, solo alcuni offrono
anche il retro -> standardizzando sul davanti vai bene con qualsiasi marca (RobStride/CubeMars/MyActuator). Schema:
l'osso fisso e' un piatto avvitato ai fori STATORE della faccia uscita, con foro centrale di luce; il corpo motore sta
dietro il piatto; l'uscita (rotore) sporge attraverso il foro; l'osso mobile si avvita al rotore davanti. Il retro NON
e' interfaccia di montaggio (sul disegno RS06 il Ø70 retro e' tra parentesi = riferimento/coperchio; le viti retro
tengono insieme il motore, non si usano). Interfaccia quotata RS06 = faccia uscita: 6xM4 (rotore) + 8xM3 su Ø82
(statore) + 3xØ4 spine.

NIENTE adattatori o pezzi in piu' (l'utente ristampa volentieri; ingombri maggiori non sono un problema). Le POSIZIONI
DEI GIUNTI le fissano i MOTORI col loro ingombro (packing), come nel G1: cambiando motore i giunti si spostano, e va
bene -> l'RL si rifa' DA ZERO (scelta utente accettata, non e' una tragedia). NON si congela l'asse del giunto: si
impacchettano i motori reali e i giunti cadono dove cadono. Le coordinate giunti G1 mode_11 (`g1_joints.csv`) sono un
RIFERIMENTO di proporzioni (lunghezza gamba, larghezza bacino...), NON un target rigido da centrare (erano per motori
~80 mm). L'UNICA cosa che resta fissa e' la TOPOLOGIA di montaggio: front-mount per tutti -> un cambio motore resta
"ri-impacchetta lo stesso tipo di scheletro + RL da zero", mai un mount che flippa davanti/dietro e stravolge la forma
delle ossa.

Link acquisto e schede:

- RS04: <https://www.seeedstudio.com/Robostride-04-Actuator-p-6775.html>
- RS03: <https://www.seeedstudio.com/Robostride-03-Actuator-p-6774.html>
- RS06: <https://www.seeedstudio.com/Robostride-06-Actuator-p-6668.html>
- RS02: <https://www.seeedstudio.com/Robostride-02-Actuator-p-6665.html>
- RS05: <https://www.seeedstudio.com/Robostride-05-Actuator-p-6666.html>
- RS00: <https://www.seeedstudio.com/Robostride-00-Actuator-p-6664.html>
- Debug USB-CAN RobStride: <https://www.seeedstudio.com/Robostride-CAN-USB-Driver-Board-p-6708.html>
- Specifica famiglia RobStride con prezzi CNY: <https://files.seeedstudio.com/products/RobStride/%E7%81%B5%E8%B6%B3%E6%97%B6%E4%BB%A3%E4%BA%A7%E5%93%81%E8%A7%84%E6%A0%BC%E4%BB%8B%E7%BB%8D%20RobStride%20Product%20Specification%20Document%2020250626.pdf>

## Prezzi RobStride: chiarimento

Il `1199` visibile per RS04 nella specifica RobStride e in yuan cinesi (`CNY`), non in dollari USA. Il PDF riporta anche
RS06 a `849 CNY`, RS05 a `499 CNY` e RS00 a `598 CNY`. Per un ordine reale non usare automaticamente il valore piu basso visto su
AliExpress: verificare SKU, versione, accessori, IVA, spedizione, dazio, reso e garanzia.

Prezzi retail Seeed verificati il 2026-06-02:

| Modello | Prezzo retail |
|---|---:|
| RS04 | USD 255, sconto quantita USD 242 |
| RS03 | USD 225, sconto quantita USD 214 |
| RS06 | USD 210, sconto quantita USD 200 |
| RS02 | USD 145, sconto quantita USD 138 |
| RS05 | USD 110, sconto quantita USD 105 |
| RS00 | USD 125, sconto quantita USD 119 |
| Debug USB-CAN | USD 15 |

La BOM usa stime EUR nette prudenti, poi applica IVA al 22%. Rivalutare il preventivo prima dell'ordine.

## Elettrico e sicurezza

> **ATTENZIONE 2026-07-17: SEZIONE STORICA.** Descrive l'architettura bench 2026-06 (SW200/SW80, timer Eaton, selettore
> a chiave, bobine 48 V, condensatori KEMET, bleeder RobStride, ED250, SD-200C/RSD-300C) superata dal lock 2026-07-12
> e dalla decisione mani-su-WEHO 2026-07-17. La fonte corrente sono i blocchi datati in testa a questo file, il
> README e la BOM Excel. Non ordinare componenti da questa sezione.

La parte elettrica non e un elenco decorativo: prima del primo power-up va realizzato e controllato un pannello 48 V.
La BOM contiene ora una baseline elettrica concreta con SKU specifici, fusibili e sezioni cavo. E dimensionata sulla
sorgente bench da `62,5 A`; la baseline mobile candidata e ora P45B 13S2P con BMS `45 A continui / 100 A massimo`, con durata del massimo ancora da
confermare per iscritto. Non sommare le
correnti di fase massime dei singoli RobStride come se fossero tutte correnti DC assorbite contemporaneamente dal pacco.

Questa e una baseline prototipo per bring-up e prove progressive, non una certificazione di sicurezza macchina. Prima
della camminata dinamica misurare correnti, cadute di tensione e temperature dei fasci; verificare serraggi e isolamento;
confermare con il fornitore del pacco corrente di corto prospettica, soglie di trip e comportamento del BMS. Il fusibile principale BF1 scelto ha
interrupting rating `1 kA`: non dichiararlo sufficiente al corto del pacco senza la conferma del costruttore.

Catena di potenza, in ordine:

1. A banco il `MEAN WELL RSP-3000-48` converte 230 VAC in 48 VDC. Usa morsetti L/N/terra, non una presa IEC C13.
2. Sul positivo 48 V mettere vicino alla sorgente il fusibile principale `Littelfuse BF1 142.5631.5702`, `70 A 58 VDC
   M5`, nel portafusibile isolato `04980921GXM5`. Il tronco principale positivo e negativo e da `25 mm2`.
3. L'e-stop `Schneider XB5AS8442` e il selettore a chiave `Schneider XB5AG21` portano solo il circuito di comando. La
   chiave evita che il semplice rilascio del fungo riaccenda automaticamente il bus. Il contattore DC `Albright SW200-20`
   con bobina 48 V e blowouts apre fisicamente il positivo motori. In mobile aggiungere il sezionatore manuale
   `Albright ED250B-1`, `250 A 96 VDC`, per manutenzione e distacco fisico di emergenza: non sostituisce il contattore.
4. Prima della chiusura piena del contattore serve precarica. Il rele `CIT A2K1CSQ48VDC1.6` collega la resistenza chassis
   `Vishay Dale RHA050100R0FE02`, `100 ohm 50 W`, in parallelo allo SW200. Il timer ON-delay `Eaton 262684 / ETR2-11`,
   alimentato a 48 VDC e impostato a circa `10 s`, abilita poi la bobina dello SW200, che bypassa la resistenza. Con i due
   condensatori gia scelti: `C = 24.000 uF`, `Vmax = 54,6 V`, `I0 = 0,546 A`, `P0 = 29,8 W`, `tau = 2,4 s`; dopo `10 s`
   il bus e circa al `98,5%`. Montare la resistenza sul pannello metallico. I TVS `Littelfuse 1.5KE68CA` vanno direttamente
   ai terminali delle bobine SW200 e CIT.
5. Il blocco distribuzione `Eaton Bussmann 16220-2` riceve positivo e negativo e divide sei rami: gamba sinistra, gamba
   destra, vita-collo, braccio sinistro, braccio destro e servizi/DC-DC Thor. I portafusibili non restano sospesi ai cavi:
   fissarli sul pannello sotto una cover isolante ventilata.
6. Due condensatori bulk `KEMET ALS80A123KE100` da 12000 uF 100 V con terminali a vite vanno in parallelo vicino alla
   distribuzione, con tratte corte e capicorda ad anello. Non stanno sospesi: ciascuno usa clamp `KEMET V4`, pannello
   rigido e cover isolante ventilata da progettare. Il rating 100 V lascia margine rispetto ai 54.6 V della batteria piena
   e ai transitori rigenerativi; sono stati scelti al posto degli snap-in per evitare una PCB potenza.
7. Il `ROBSTRIDE Bleeder Module` limita la sovratensione rigenerativa dissipando energia quando i motori frenano.
   L'alimentatore Mean Well da banco non va assunto capace di assorbire rigenerazione.
8. In mobile il candidato selezionato/order-gated e Bicycle Motor Works `13S2P P45B`: 46.8 V nominali, 54.6 V piena,
   9 Ah / 421.2 Wh, BMS 45 A continui / 100 A massimo, 165.1 x 101.6 x 76.2 mm, massa CAD prudente 2.27 kg.
   Non ordinarlo prima della conferma su spedizione Italia, massa esatta, durata del massimo, trip BMS, regen e charger.
   Tõuksi Vabrik e il fallback UE da 60 A / 2.04 kg se garantisce per disegno lo stesso envelope. `ENERprof TN13S5P`
   resta qty 0: 1200 Wh e 5.2 kg sono eccessivi rispetto al G1 per il prototipo corrente.
9. Thor non va collegato al bus 48 V: il `MEAN WELL SD-200C-24` crea il rail 24 V. Thor accetta `9-28 V DC` al Micro-fit.
10. Le due mani RH56DFX usano un secondo convertitore `MEAN WELL RSD-300C-24`, 24 V / 12.5 A / 300 W, su ramo 48 V
    dedicato e fusibile MINI 10 A. Non usare il ramo Thor da 10 A per entrambi i convertitori. Il punto di split servizi
    positivo/negativo deve essere un componente dimensionato e fissato, non due conduttori infilati nello stesso morsetto.

Segmentazione positiva selezionata:

| Ramo | Fusibile | Cavo | Nota |
|---|---|---|---|
| Principale | `BF1 142.5631.5702`, 70 A 58 VDC | `25 mm2` | baseline P45B; ricontrollare coordinamento con BMS 45/100 A prima del mobile |
| Comando safety | `MINI 0997002.WXN`, 2 A 58 VDC | pigtail `12 AWG` del portafusibile `0FHM0002XP` | e-stop, chiave, timer e bobine |
| Gamba sinistra | `BF1 142.5631.5702`, 70 A 58 VDC | `16 mm2` | verificare temperatura in prova |
| Gamba destra | `BF1 142.5631.5702`, 70 A 58 VDC | `16 mm2` | verificare temperatura in prova |
| Vita-collo | `BF1 142.5631.5402`, 40 A 58 VDC | `6 mm2` | attivo in fase 3 |
| Braccio sinistro | `BF1 142.5631.5302`, 30 A 58 VDC | `6 mm2` | attivo in fase 3 |
| Braccio destro | `BF1 142.5631.5302`, 30 A 58 VDC | `6 mm2` | attivo in fase 3 |
| Servizi Thor | `MINI 0997010.WXN`, 10 A 58 VDC | pigtail `12 AWG` | solo SD-200C-24 |
| Servizi mani | `MINI 0997010.WXN`, 10 A 58 VDC | pigtail `12 AWG` | solo RSD-300C-24; split servizi da definire |
La somma dei fusibili di ramo puo superare `70 A`: ciascun fusibile protegge il proprio cavo e isola il guasto del ramo;
non costituisce una riserva di potenza contemporanea. Il limite complessivo resta il ramo principale e, in mobile, il BMS.

Schema funzionale minimo del pannello:

```text
BENCH: 230 VAC -> RSP-3000-48 -> BF1 principale 70 A -----------\
                                                                  +-> nodo sorgente protetto -> SW200-20 -> bus motori
MOBILE: batteria -> BF1 principale 70 A -> ED250B sezionatore ---/

nodo sorgente protetto -> fusibile MINI 2 A -> e-stop NC -> chiave enable NO
                                              +-> rele CIT -> resistenza 100 ohm -> bus motori
                                              +-> timer Eaton 10 s -> bobina SW200-20

bus motori -> bleeder + due condensatori KEMET + PDU Eaton
PDU -> BF1 70 A gamba sx / BF1 70 A gamba dx / BF1 40 A vita-collo
    -> BF1 30 A braccio sx / BF1 30 A braccio dx / MINI 10 A servizi Thor
```

La resistenza e il rele CIT costituiscono il percorso temporaneo di precarica in parallelo allo SW200: non vanno messi
permanentemente in serie con i motori. Premendo l'e-stop cadono sia il CIT sia lo SW200. In mobile il fusibile principale
deve restare il piu vicino possibile alla batteria; il sezionatore manuale ED250B viene dopo il fusibile.

I cavi potenza selezionati sono Nautica Illiano `CABATR25/CABATN25`, `CABATR16/CABATN16` e `CABATR06/CABATN06`. I capicorda
sono scelti per conduttore flessibile e foro reale: Klauke `704F5`, `704F10`, `703F5`, `101R5`; la crimpatrice e
`Klauke K05`, range `6-50 mm2`. Le quantita BOM dei capicorda includono due pezzi di scorta per le prove di crimpatura.

Ingombri principali gia riportati anche nelle note Excel per disegnare il pannello: RSP-3000-48 `278 x 177,8 x 63,5 mm`
solo banco; PDU Eaton `76,2 x 50,8 x 25,4 mm`; condensatori KEMET `diametro 51 x H84 mm` ciascuno; resistenza RHA050
`circa 50,0 x 21,4 x 16,0 mm`, interassi montaggio `circa 70,6 mm`; timer Eaton `17,5 x 63 x 70 mm`; CIT A2K
`26,5 x 32,0 x 33,5 mm`; DC/DC Thor `215 x 115 x 50 mm`; Jetson AGX Thor dev kit `243,19 x 112,40 x 56,88 mm`,
con modulo T5000 configurabile `40-130 W`.

Nota datasheet importante per il passaggio di consegne: per il portafusibile `04980921GXM5` circola ancora un vecchio PDF
Littelfuse che riporta `32 V DC`. La pagina ufficiale Littelfuse corrente identifica invece la stessa parte come
`MIDI 498-IL Series 58 V In-Line Fuse Holder`, compatibile BF1/MIDI M5. Usare come fonte corrente:
<https://www.littelfuse.com/products/fuse-blocks-fuseholders-and-fuse-accessories/automotive-and-commercial-vehicle-fuse-holders/midi-498-il/04980921gxm5.aspx>.

Cablaggio e CAN:

- RS03 e RS04 usano lato linea potenza `AMASS XT30UW-F` e CAN `GH1.25-T`. In BOM ci sono SKU acquistabili
  `AMASS XT30UW-F.G.Y`, housing `JST GHR-02V-S` e contatti `JST MINI-SSHL-002T-P0.2`; comprare un campione e verificare
  fisicamente l'accoppiamento GH prima del lotto, perche esistono cloni non intercambiabili.
- RS02, RS05 e RS06 usano il cavo pronto Seeed `BCCA4011`, XT30 `(2+2)` femmina-femmina da 300 mm con un capo diritto e
  uno a 90 gradi. Il vecchio BCCA4009 e stato rimosso perche la pagina Seeed restituisce 404. Verificare nel CAD
  orientamento, raggio di piega ed eventuali estensioni con strain relief.
- Non esiste un harness completo acquistabile per questo umanoide: i fasci RS03/RS04 vanno progettati e costruiti su
  misura dopo il CAD. La vecchia riga generica "Harness RobStride XT30 + GH1.25 CAN" era fuorviante ed e stata eliminata.
  Per i microcontatti JST GH commissionare preferibilmente i fasci a un cablatore con prova di trazione e test continuita:
  la pinza ufficiale JST `YRS-1590` e elencata qty 0 per trasparenza ma costa oltre EUR 1.500.
- RobStride usa CAN 2.0B a 1 Mbps. Usare doppino schermato 120 ohm `Belden 9841LSZH`, topologia a bus e una resistenza
  `YAGEO MFR-25FBF52-120R` alle sole due estremita fisiche di ogni bus.
- Thor Dev Kit espone due bus CANH/CANL sul connettore J47: non servono transceiver SN65HVD230 esterni sul kit. Harness
  J47 e cavo Micro-fit Thor restano qty 0 finche mating connector e pinout non sono verificati sul kit fisico.
- [CORREZIONE 2026-07-17: questa riga e' SUPERATA. Usare esattamente `MKS CANable Pro / CANable-MKS 1.0` con
  STM32F072 (candleLight/gs_usb); NON il "V2.0" STM32G431, non supportato dal firmware candleLight upstream —
  vedi nota ELECTRONICS 2026-07-12 in testa al file.] Vecchio testo: per i bus aggiuntivi del corpo superiore usare
  `MKS Makerbase CANable Pro V2.0`: isolato, disponibile e compatibile
  `candleLight / SocketCAN`. Sostituisce il CANable OpenLight non ordinabile dal sito ufficiale non raggiungibile.

### Architettura controllo: baseline Thor-only, controller low-level opzionale

I RobStride contengono gia i loop locali dell'attuatore: il computer di bordo non deve implementare direttamente il
controllo di corrente del motore. Deve leggere feedback e IMU, eseguire la policy o il controllo articolare e inviare
setpoint periodici via CAN con limiti, heartbeat e watchdog.

Per ridurre componenti, la baseline iniziale usa solo `NVIDIA Jetson AGX Thor`: processo realtime isolato, SocketCAN
diretto, priorita realtime, core CPU dedicati e safety hardware indipendente dal software. Thor dispone di due controller
CAN nativi e NVIDIA fornisce un kernel realtime per Jetson Thor, ma nella documentazione corrente il supporto RT e
indicato come Developer Preview. Non assumere quindi che l'esecuzione Linux condivisa con AI, telecamere e logging sia
automaticamente deterministica.

Un computer low-level separato non e obbligatorio per il primo prototipo ed e presente in BOM come `OPZIONE qty0`.
Diventa raccomandabile se i test Thor-only mostrano jitter, latenze non accettabili, saturazione dei bus, dipendenza da
interfacce USB-CAN non abbastanza robuste oppure se si vuole mantenere damping/watchdog e gestione attuatori isolati da
crash, reboot o aggiornamenti del software AI. Non scegliere ancora Raspberry Pi, MCU o SBC: prima misurare frequenza
loop, latenza e jitter con tutti i 31 assi e definire numero di bus, IMU, I/O e strategia safety.

NODO "1 o 2 computer?" RISOLTO 2026-06-14 (dopo ToddlerBot, Stanford CoRL 2025, arXiv 2502.00893). ToddlerBot e' un
umanoide open-source 30 DoF con UN SOLO computer (Jetson Orin NX, 2.5 TFLOPS) che gira locomozione E manipolazione/vista
con "concurrent policy inferences" sullo stesso acceleratore CUDA: NON due computer. Il low-level lo fanno gli attuatori
(Dynamixel smart-servo col loop interno) come da noi i RobStride (FOC interno + CAN); a bordo c'e' solo Orin NX + una
"comm board" (interfaccia bus, NON un secondo cervello) + IMU/power. LEZIONE: l'asse vero non e' "computer locomozione
vs computer manipolazione" (loco-RL e manip-VLA sono due reti che girano insieme su 1 GPU), ma CERVELLO high-level
(percezione + RL loco + VLA manip, 10-200 Hz) vs LOOP real-time low-level (~1 kHz giunti + safety). Quel low-level puo'
stare sullo STESSO Thor come processo RT isolato, oppure su un piccolo co-controller dedicato (= la nostra OPZIONE qty0),
ma NON e' un secondo computer AI. DECISIONE "massima qualita'": UN solo Thor come cervello (gira loco+manip+vista con
margine enorme: Thor >> Orin NX, e se un Orin NX da 2.5 TFLOPS basta per ToddlerBot, Thor ci sta larghissimo); NIENTE
secondo computer per la manipolazione; il co-controller RT/safety resta opzione da attivare solo a misura su HW reale.
Caveat: ToddlerBot e' piccolo/lento (3.4 kg, servo di posizione) -> esigenze RT piu' leggere di un clone G1 dinamico,
quindi il rischio jitter sul loop RT va comunque misurato. Per il PROTOTIPO VIRTUALE e' irrilevante: in sim non conta il
compute di bordo, mettere 1 Thor e non far condizionare il CAD dal suo ingombro. (Supera la spinta di AI a togliere
il Thor: sotto "massima qualita'" il Thor singolo si tiene come cervello unico e futuro-VLA a bordo.)

Fonti NVIDIA:

- CAN Jetson: <https://docs.nvidia.com/jetson/archives/r38.2.1/DeveloperGuide/HR/ControllerAreaNetworkCan.html>
- Layout Thor e ingresso Micro-fit: <https://docs.nvidia.com/jetson/agx-thor-devkit-4fed1671/user-guide/latest/hardware_layout.html>

## Modifiche effettuate in questa sessione

- Unificati i motori su RobStride; rimossi Damiao e CubeMars dalla selezione.
- Corretta la baseline G1 passando al modello ufficiale corrente `g1_29dof_mode_11`.
- Corretta l'interpretazione meccanica della vita: RS04 yaw verticale + RS03 x2 su puntoni per pitch/roll.
- Ripristinati cardano vita, due puntoni M10 e perno condiviso lato busto nella BOM.
- Ripristinati i 7 DOF per braccio della variante G1 29 DOF.
- Scelti RS05 x2 per collo pan/tilt usando come riferimento la pagina ufficiale G1-Comp; coppia collo da validare.
- Differenziata la ladder braccia per ridurre la massa distale: RS03 shoulder pitch/roll, RS06 shoulder yaw e gomito,
  RS02 wrist roll, RS05 wrist pitch/yaw. RS06 wrist roll resta alternativa qty 0.
- Uniformate tutte le righe motore Excel: dimensioni, peso, coppia nominale/picco RobStride e riferimento G1 obbligatori.
- Corretta la formattazione Excel: il grigio chiaro si applica solo alle righe con quantita numerica zero, non ai titoli blu.
- Rimosse le ipotesi premature `6001-2RS` e `6801-2RS` per il giunto caviglia: supporti, ritegni e lunghezze perni restano
  qty 0 fino al CAD.
- Spostata la catena di sicurezza in fase 1 bench.
- Rimossi RUBIK LINK CubeMars e transceiver Thor esterni; aggiunto debugger USB-CAN RobStride.
- Chiusa una baseline elettrica acquistabile: tronco `25 mm2`, fusibile principale BF1 `125 A`, comando safety `2 A`,
  rami gambe `70 A / 16 mm2`, vita-collo `40 A / 6 mm2`, braccia `30 A / 6 mm2`, servizi Thor `10 A`; aggiunti
  portafusibili 58 VDC specifici.
- Dimensionata la precarica sui due condensatori KEMET: Vishay `100 ohm 50 W`, rele CIT 48 V, timer Eaton ON-delay
  impostato a circa 10 s, selettore a chiave Schneider e TVS bobine. Aggiunto sezionatore batteria manuale ED250B-1.
- Eliminati cavo generico 12 AWG e XT90 generico: aggiunti cavi Nautica Illiano per sezione, capicorda Klauke per foro
  reale e crimpatrice K05. Il connettore estraibile ENERprof resta qty 0 finche il produttore non conferma la controparte.
- Eliminati i falsi harness completi: aggiunti cavi Seeed BCCA4011, connettori XT30UW-F, housing/terminali JST GH,
  cavo CAN Belden e terminatori YAGEO; harness custom e J47 restano qty 0.
- Auditati i link selezionati: corretti il vecchio cavo Seeed BCCA4009 rimosso, il caricatore ENERprof ritirato e il
  CANable OpenLight non raggiungibile. Il caricatore nuovo resta candidato qty 0 finche ENERprof non approva interfaccia.
- Sostituita la batteria generica Danenergy con il link diretto al pacco ENERprof selezionato; aggiunta alternativa
  Dan-Tech Energy softpack qty 0 con nota obbligatoria Smart BMS + AS150U.
- Rimossi i link a categorie RS dalle righe acquistabili e reso `umanoide` il foglio attivo all'apertura Excel.
- Ribadito che Unitree G1 e l'unica baseline: K-Bot resta solo una nota open hardware secondaria per packaging e
  cablaggio, non va usato per dimensionare geometrie, caviglia o motori.
- Chiarita la caviglia: i due perni ortogonali diametro 12 mm per caviglia sono esclusivamente assi di rotazione del
  giunto piede-stinco; il perno trasversale diametro 8 mm riceve invece le due teste dei puntoni M8. Restano selezionati
  sei puntoni totali, quattro M8 alle caviglie e due M10 alla vita.
- Aggiunti esempi `qty 0` di boccole radenti standard SKF e igus Q2 e tre provini custom stampati in iglidur `i150`,
  `i190` e `J260-PF`; la scelta finale resta subordinata a CAD e prove sul perno reale.
- Chiarita la struttura dei supporti caviglia: perno diametro 12 mm fisso nelle orecchie, supporto radiale nel pezzo
  centrale mobile, ralla assiale dedicata e registrata per lato, inserto metallico flangiato fisso nelle orecchie come
  controfaccia sostituibile. Aggiunte alternative `qty 0` igus `Q2FM`, `GTM`, SKF `HK`, `NKI`, `AXK`, `AS`, rasamento
  DIN 988 e famiglia Elesa+Ganter `DIN 172`; non attivare nessuna variante prima delle quote CAD.
- Documentata la prima pila di serraggio per la variante semplice `NKI 12/16`: rondelle larghe, spallamenti integrati
  delle orecchie che serrano solo l'anello interno, parte mobile esclusa dalla compressione e bullone a colletto RS PRO
  `292-417` `12 x 60 mm` come riferimento preliminare `qty 0`. Recuperati in BOM i cataloghi per perni e ritegni.
- 2026-06-03: chiusa la DECISIONE FINALE caviglia (vedi blocco dedicato in "Gambe, fase 1"). Architettura radente la piu
  semplice: vite a colletto ISO 7379 `Ø12-M10` come perno/pista (solidale alle orecchie via serraggio assiale, non
  piantaggio), due boccole flangiate igus `GFM-1214` piantate nel pezzo mobile con la flangia che fa l'assiale (eliminate
  ralle separate, manicotto/colonna e reggispinta), dado M10 + rondella larga. Bussola flangiata metallica nell'orecchia
  (`DIN 172-B12-20`) resa OPZIONALE come upgrade anti-usura se la flangia igus consuma il PA-CF. NKI 12/16 e
  manicotto/colonna archiviati come alternative. Aggiunti fornitori multipli verificati. Boccola PRIMARIA = STAMPATA
  multimateriale J260+PA-CF integrale al pezzo mobile (filamento gia acquistato), `GFM-1214` acquistata come fallback;
  partenza assiale con spallamento PA-CF dalle orecchie che striscia sulla flangia igus stampata. Allineate le righe BOM
  caviglia (tag SCELTO/PRIMARIO/FALLBACK/ARCHIVIATO/OPZIONALE) e rigenerato l'Excel. Disegni di sezione non piu mantenuti.
- 2026-06-04: vita yaw declassata da RS04 a RS03 (scelta utente) -> BOM 8 RS04 + 7 RS03, totale EUR 16.228,27, massa
  40,355 kg. Aggiunta colonna "CAD 3D" con i link Seeed (STEP scaricabile) per ogni motore. Estratte e loggate le posizioni
  esatte dei 29 giunti G1 dall'URDF (`g1_joints.csv` + `g1_29dof_mode_11.urdf` nel workspace). Documentato il nodo densita
  di coppia RobStride vs Unitree: motori gamba (RS04 vs RS06) da decidere con l'utente in base all'ambizione.
- 2026-06-05: aggiunta e poi corretta la regola skeleton Onshape. La scheda `G1 joints CAD` contiene `exact_*`, `cad_*`
  e `pose_down_*`: `cad_x` viene portata a zero, `cad_y` viene allineata nelle catene verticali a `hip_roll` per la gamba
  e `shoulder_yaw` per il braccio, `cad_z` resta la quota G1. Gli assi di rotazione non vengono semplificati. `pose_down_*`
  resta solo un aiuto visivo per braccia lungo corpo. Il trattino `-` significa "uguale al riferimento", non zero.
- 2026-06-05: il workbook e stato ripulito da tab inutili. Il generatore ora elimina intenzionalmente `ARTES4.0@Olbia_`,
  `Speso-Impegnato`, `pivot-finali`, `Acquisti` e `Budget`; `umanoide` viene inserito dopo `ARTES4.0@Olbia_NoIVA` e
  `G1 joints CAD` subito dopo `umanoide`.
- 2026-06-05 (AI): consolidamento arretrato di piu giri.
  (1) MOTORI BRACCIA: polso ora 3 assi UNIFORMI RS02 (era roll RS02 + pitch/yaw RS05; Unitree fa il polso uniforme).
  Spalla yaw resta RS06 (piu leggera dei pitch/roll RS03, ridotta massa distale). BOM = 8 RS04, 8 RS06, 7 RS03, 6 RS02,
  2 RS05 = 31 assi; totale EUR 16.399,07; massa 41,211 kg. Riserve grigie [SECONDA SCELTA qty0]: RS03 spalla-yaw uniforme,
  RS06 polso potente, RS05 polso pitch/yaw leggero.
  (2) ASSI SEMPLIFICATI: aggiunta colonna `axis_cad_semplif` alla scheda `G1 joints CAD` (hip_roll->X, hip_yaw->Z,
  shoulder_pitch->Y, resto principale) su richiesta utente. Skeleton CAD = posizioni `cad_*` + assi `axis_cad_semplif`
  (coerente, ortogonale). Supera la nota AI "assi non semplificati".
  (3) VERIFICA G1 (workflow 5 agenti): posizioni/assi/massa SOLIDI, triplo-confermati (<0,1 mm; massa totale 33,340 kg;
  coscia 336,6 / stinco 317,6 / gamba 654,2 mm; cant anca 10,021 deg). Coppie: combaciano col file `mode_11` ma DIVERGONO
  dall'URDF pubblico `unitree_rl_gym` su 3 giunti: hip pitch/roll mode_11=139 vs rl_gym=88; ankle 35 vs 50; waist roll/pitch
  35 vs 50. Knee 139 in entrambi. wrist pitch/yaw=5 confermato (il "8" trovato dall'utente era errato). Per dimensionare i
  motori usare il valore PIU ALTO (139 hip/knee, 50 ankle/waist) con margine. Vero collo di bottiglia = GINOCCHIO (139,
  RS04 14% sotto). Caviglia 2xRS06 confermata giusta (reale ~50, non 35). Le posizioni sono identiche tra le due release.
  (4) COMPUTE: raccomandata architettura G1-style = controller real-time piccolo (uC o SBC RT-Linux) per policy + loop CAN
  + safety, PIU computer AI (Orin NX class, NON Thor) aggiunto DOPO per la vista. La policy RL per camminare e minuscola:
  non serve Thor per il bring-up. Riconsiderare/togliere Thor dalla baseline; non far condizionare il CAD dal suo ingombro.
  (5) POSA e LIMITI: disegnare e assemblare a BRACCIA LUNGO IL CORPO (home); la posa e solo la default config in sim, non
  e incisa nella geometria (link length pose-indipendenti). Limiti giunto = SOFTWARE, ricavati dal proprio CAD
  (auto-collisione ruotando i giunti in assieme + avvolgimento cavi per gli yaw), non copiati dal G1. Fermi fisici solo
  dove critico per sicurezza. CAD motori: scaricabili dalle pagine Seeed (colonna "CAD 3D" in BOM) o AIFITLAB (STEP per modello).
- 2026-06-05 (AI): hip yaw gamba declassato da RS04 a RS03 (scelta utente: in CAD gli RS04 risultano troppo
  grossi/pesanti). Pitch, roll e ginocchio restano RS04 — il roll e l'asse dell'equilibrio laterale (critico) e il robot
  a 41 kg e piu pesante del G1 (33 kg), quindi non si declassa. BOM ora: 6 RS04 + 9 RS03 + 8 RS06 + 6 RS02 + 2 RS05 = 31
  assi; totale EUR 16.330,75; massa 40,131 kg (-1,08 kg). Hip yaw RS03 = 60 Nm picco vs G1 88: accettabile perche lo yaw
  e l'asse anca meno sollecitato (non combatte la gravita, domanda reale bassa).
- 2026-06-05 (AI): spalla pitch/roll declassata da RS03 a RS06 (spalla ora tutta uniforme RS06), VERIFICATO a calcolo
  (non solo G1): braccio 3.26 kg, CoM 0.236 m -> statico 7.5 Nm, picco su gesto veloce ~22 Nm. RS06 (36/11) copre con 1.6x
  sul picco e regge il braccio teso in continuo (7.5 < 11 nom); RS02 troppo debole (non tiene il teso, scalda); RS03 era
  2.7x = sovradimensionato. BOM ora: 6 RS04 + 5 RS03 + 12 RS06 + 6 RS02 + 2 RS05 = 31 assi; totale EUR 16.296,59; massa
  39,095 kg. VITA invece NON ridotta (verificata a calcolo): regge tutto il corpo superiore ~15-20 kg; pitch/roll ~32-64 Nm
  al GIUNTO (gravita + dinamico, secondo inclinazione busto e posizione batteria) e passano per i 2 puntoni (coppia motore
  != coppia giunto, serve geometria leve dal CAD) -> resta RS03, non si tocca. Waist yaw ~9-31 Nm (solo inerziale): in
  teoria RS06 ma margine troppo risicato (single motore, ruolo equilibrio) -> tenuto RS03, rivedere dopo CAD + batteria.
- 2026-06-05 (AI): shoulder yaw declassato da RS06 a RS02, verificato col PAYLOAD nella postura reale. Chiarimento
  utente: il carico si tiene a braccio PIEGATO (omero verticale, avambraccio a 90 gradi), non disteso. Conseguenze a
  calcolo: (a) lo shoulder yaw ha l'asse omero verticale -> gravita 0, solo inerzia -> ~4-11 Nm anche con 3 kg in mano ->
  RS02 (17 picco) basta con margine; (b) spalla pitch/roll e gomito tengono il carico alla leva dell'AVAMBRACCIO ~0.20 m
  (non 0.37 m di braccio teso) -> RS06 regge ~4.3 kg a braccio piegato, quindi NON serve RS03 sulla spalla (resta RS06) e
  il gomito RS06 va bene cosi. Il braccio porta ~4 kg in postura carico. BOM: 6 RS04 + 5 RS03 + 10 RS06 + 8 RS02 + 2 RS05
  = 31 assi; totale EUR 16.137,99; massa 38,663 kg [snapshot 06-05, SUPERATO dal 2026-06-08, vedi sotto]. Le riduzioni
  verificate a calcolo (spalla pitch/roll, hip yaw, shoulder yaw) hanno tolto ~2,5 kg restando sopra i fabbisogni reali.
- Impostato Thor-only come baseline iniziale; il computer low-level separato resta un'opzione `qty 0` da attivare solo
  se le misure mostrano jitter, bus insufficienti o la necessita di isolamento dai crash del software AI.
- Consolidata la documentazione in questo singolo file; `STATO.md` eliminato.
- 2026-06-08 (AI): revisione motori completa con le specifiche RobStride REALI (tabella verificata via Seeed/AIFITLAB/
  OpenELAB). Polso 3 assi RS02->RS00 (dual encoder, 57 mm, 5 nom/14 picco, regge 2 kg in mano). Spalla yaw RS02->RS00.
  Spalla pitch/roll RS06->RS02 e gomito RS06->RS02 -- NON RS01: trovato che RS01 ha encoder SINGOLO (solo 36V, niente IP),
  RS02 ha DUAL encoder (feedback in uscita, serve per RL/manipolazione); RS01 scartato ovunque. Hip yaw gamba RS03->RS06;
  vita yaw e vita pitch/roll RS03->RS06 (assi verticali / a domanda dinamica bassa, robot non acrobatico, verif ~28 Nm <
  36 picco). Caviglia resta 2x RS06: correzione utente -> caviglia e vita pitch/roll sono LEVERAGGI, la coppia giunto e'
  fissa dal carico ma la coppia motore dipende dal rapporto crank (in CAD); RS06 = tetto sicuro. BOM ora: 6 RS04 + 9 RS06
  + 6 RS02 + 8 RS00 + 2 RS05 = 31 assi (spariti tutti gli RS03 e RS01 dagli attivi). Totale EUR 15.434,05; massa 35,312 kg
  (-3,35 kg sui motori vs 06-05). Sorgente py + MEMORY aggiornati; Excel rigenerato e CONFERMATO: completo 15.434,05,
  Fase1 10.519,00, Fase2 1.465,45, Fase3 3.449,60, massa 35,312 kg, 31 motori (RS00x8, RS02x6, RS04x6, RS05x2, RS06x9).
- 2026-06-08 (AI): VERIFICA COPPIE completa post-downsizing (metodo + numeri nella sezione dedicata sopra). Esito:
  nessun motore bocciato per uso non-acrobatico; gambe RS04 (non declassate) reggono in piedi e camminata. 3 ATTENZIONE
  recuperabili: ginocchio (no squat profondo tenuto, e' il max motor), vita pitch (batteria bassa + leveraggio),
  gomito (<=1.5 kg comodo / 2 kg solo a velocita moderata). 2 verifiche CAD: rapporto crank caviglia e vita >=1:1.
  Scritto il METODO di calcolo (statico g*Sum(m*b), dinamico I*alpha bang-bang, yaw=solo inerzia, leveraggi) + input
  (masse motori come bracci, posizioni giunti G1, braccio disteso) cosi AI puo' rifare i conti.
- 2026-06-09 (two AI sessions): cross-check AI sulla SPALLA -> AI ha ragione, mio numero era ottimista. Errore mio:
  avevo usato mano 0,30 kg; in realta' e' 0,50 kg col CoM oltre il polso (~0,48 m). Corretto: braccio TESO orizzontale
  ~7,8-8,6 Nm > 6 nominale -> RS02 NON tiene il braccio disteso in CONTINUO (ok solo qualche s sotto i 17 picco); 2 kg a
  reach pieno sfora anche il picco. A gomito PIEGATO invece ok (~2,6 senza payload / ~6,9 con 2 kg). AI ha anche
  alzato la MASSA reale: lui usa ~46 kg (telaio PA-CF ~10 kg incluso), io avevo verificato a 35 (senza telaio). A 46 kg
  le GAMBE RS04 (gia' il max) vanno SOPRA il nominale camminando (~45 vs 40) -> la leva e' la MASSA, non il motore.
  Conclusioni: tenere braccia leggere (no upsize spalla, peggiorerebbe le gambe) + CONTROLLARE la massa (target telaio
  ~6 kg, robot ~40 kg). Decisioni aperte: ruolo del braccio (solo piegato vs reggere disteso) e target massa telaio.
- 2026-06-09 (utente) [SUPERATO in parte 2026-06-27: caviglia e vita hanno nuova ferramenta attiva]: swap ferramenta puntoni. Puntoni caviglia E vita -> rod-end ALLUMINIO M8 regolabili varie
  lunghezze (AliExpress 1005008935554718), su perni Ø8xM6. Viti a colletto NERE AliExpress (set tutte le misure,
  1005007481484485) usate per TUTTO: Ø12xM10 per gli assi rotazione (caviglia + cardano vita), Ø8xM6 per i perni dove
  spingono i puntoni (caviglia + vita). RS PRO 292-417 retrocesso ad alternativa. Lunghezze al CAD. Regen: completo
  15.425,51 EUR, massa 35,012 kg.
- 2026-06-09 (utente) [SUPERATO in parte 2026-06-27: corrente = Ø8/M6 x45 gimbal caviglia, KARM destro qty2 + KALM sinistro qty2, no cardano vita]: definito l'ASSIEME giunti. CAVIGLIA (pitch+roll) = pezzo centrale stampato 3D a croce con igus
  integrale (foro cilindrico pitch in alto, foro perpendicolare roll in basso), 2 viti a colletto Ø12xM10 come assi +
  dadi M10 neri che serrano le orecchie; pezzo centrale con leggero gioco. Fallback igus: cilindri flangiati stampati
  separati -> boccole igus flangiate comprate. PERNO PUNTONI piede = vite a colletto Ø8xM6 trasversale + 1 dado M6 nero,
  2 teste a snodo dei puntoni + parte centrale stampata 3D. Dadi neri nylock aggiunti al BOM (Amazon B0C8ZCR6B1, set
  M3-M16): M6 (perni puntoni) e M10 (assi caviglia+vita). NOTA CRITICA (AI): i rod-end devono restare LIBERI di
  oscillare (la caviglia fa 2 DOF, il roll richiede lo snodo sferico) -> il colletto Ø8 va in BATTUTA cosi il dado
  precarica sul metallo e NON schiaccia le sfere; la parte centrale stampata fa solo da spaziatore (il colletto regge il
  carico, cosi non va in creep). Spaziatori alu OD13 scartati: OD troppo grande, toccherebbero il corpo del rod-end.
- 2026-06-09 (AI+utente): CINEMATICA caviglia parallela. G1 (da URDF): pitch -50/+30 = 80 deg, ROLL solo +/-15 = 30
  deg. Rod-end: il PITCH (80 deg) usa la rotazione ILLIMITATA attorno al perno (perni lungo l'asse pitch/trasversale) ->
  zero disallineamento; il ROLL (+/-15) usa il TILT della sfera, LIMITATO. Tilt richiesto ~ ordine dell'angolo di roll
  ma RIDUCIBILE con geometria (puntoni LUNGHI + attacco vicino al piano dell'asse roll). Rod-end economici ~+/-12-16 deg
  -> marginali a +/-15; usare high-misalignment (+/-20-25) o verificare il tilt reale in CAD. LEVE: roll = moto piccolo,
  puntone resta ~perpendicolare -> rapporto ~COSTANTE, progettare crank=foot per 1:1; pitch = moto grande, sweep ->
  rapporto VARIA (nonlineare ~1.5-2x), dimensionare sul caso peggiore. CRANK/lancetta motore = pezzo PIU' CARICATO
  (~1+ kN forza asta a leva corta): farlo TOZZO o in METALLO, non sottile stampato. Motori impilati (uno su/uno giu) ->
  rod di lunghezze diverse + accoppiamento pitch/roll (matrice non diagonale); side-by-side stessa quota = piu' pulito.
- 2026-06-09 (AI): COSA C'E' NELL'URDF per i giunti a puntoni. L'URDF e' un ALBERO seriale: la caviglia e' 2 giunti
  revolute VIRTUALI (ankle_pitch + ankle_roll, effort 35 Nm ciascuno), la vita 3 (yaw 88, roll 35, pitch 35). NON ci sono
  posizioni motori, aste, crank, ne mimic/transmission/loop (verificato a grep). La sim NON simula la trasmissione: muove
  giunti ideali, l'RL comanda le coppie ai GIUNTI virtuali; le masse motori sono incluse nell'inerzia del link padre
  (stinco), non come corpi separati. La mappa coppia-giunto -> coppia-motore (Jacobiano del leveraggio) sta nel
  CONTROLLER del robot, NON nell'URDF. Conseguenza: NON si possono ricavare i bracci del G1 dall'URDF. Distinzione utile:
  giunti DIRETTI (hip/knee/yaw/spalle/gomito) -> effort URDF = coppia MOTORE (usabile diretta); giunti a LEVERAGGIO
  (caviglia, vita roll/pitch) -> effort URDF = coppia GIUNTO, la coppia motore = giunto/rapporto, rapporto = scelta tua.
  Si dimensiona il leveraggio per erogare la coppia GIUNTO dai propri motori: target caviglia ~46 Nm (robot 46 kg, piu'
  del G1 33 kg che chiede 35!), 2x RS06 = 72 Nm a 1:1 -> coperto con margine. NON copiare i 35 del G1 (e' piu' leggero).
- 2026-06-09 (utente): organizzazione BOM. (1) Colore testo righe AUTOMATICO: NERO se qty>0 oppure tag [SCELTO];
  GRIGIO (A6A6A6) se alternativa/catalogo/archiviata a qty0. Niente grassetto. Logica in build_umanoide_tab.py
  (is_active = unita>0 or "[SCELTO" in nome). (2) TUTTA la ferramenta meccanica dei giunti (perni, viti a colletto,
  dadi, rod-end, cuscinetti) sta in sezione "1 - PROTOTIPIA MECCANICA", inclusa quella della VITA (spostata da 2b);
  le sezioni motori contengono SOLO motori. La ferramenta vita mantiene fase=Fase 3 (costo corretto), cambia solo
  la posizione visiva. Totali invariati 15.425,51 EUR / 35,012 kg.
- 2026-06-11 (AI+utente): STUDIO altri robot + motori premium (budget potenzialmente rilassato, "massima qualita'",
  fara' un prototipo virtuale). ARCHITETTURA: (a) VITA -> [SUPERATO il 2026-06-14: l'R1 in serie e' stato SCARTATO per
  geometria, si resta sui PUNTONI G1 yaw+pitch+roll; vedi bullet 2026-06-14] l'ipotesi era schema UNITREE R1 = yaw +
  roll (NO pitch), 2 motori diretti. R1 confermato yaw +-150 / roll +-30. Tesla: ~2 DOF torso, assi non pubblici (mi
  ero sbilanciato a dire 'solo yaw', ritrattato). Figure: niente pitch torso (brevetto WO2025213141A1), HA
  leg-twist/hip-yaw cantato in basso (NON toglie l'hip yaw). Asimov (gemello 35kg, github asimovinc/asimov-1): 6
  DOF/gamba CON hip yaw, vita solo yaw.
  -> CONCLUSIONE: TIENI hip yaw (tutti ce l'hanno), vita = SERIALE yaw+roll diretta (vedi 2026-06-16, i puntoni vita SUPERATI), pitch anca FUORI (G1/R1) non dentro (Figure) perche'
  i QDD grossi (Ø88-107) si scontrano nell'inguine e bloccano l'adduzione. (b) MOTORI premium: CubeMars AKE90-8 (170 Nm,
  1.4 kg, 9 arcmin, ~$484 nudo) supera il G1 sulle gambe (via lo 0.86x). MA il PESO lo taglia ENCOS, non CubeMars:
  Encos EC-A4310-P2-36 = 36 Nm in 377 g vs RS06 621 g -> -244 g/motore. CubeMars piu' DISPONIBILE (retail) e piu'
  economico, Encos piu' LEGGERO ma a preventivo (Foxtech). Specifiche: AKE80-8 30Nm/570g/Ø87x32/$340; AK10-9 53Nm/dual
  enc/$699; Encos A10020 150Nm/1.35kg/$2250, A13715 320Nm/$2250. Encos/CubeMars > RobStride in densita' ma RobStride
  resta il piu' leggero SOTTO i ~20 Nm (RS00 310g, RS05 191g) -> sui piccoli si tiene RobStride anche nel premium.
  Creata 2a scheda Excel "MOTORI premium" (mix ottimale: AKE90-8 gambe + Encos A4310 sui 36Nm + RobStride piccoli):
  16,14 kg vs 18,21 RobStride = -2,07 kg (TUTTI da Encos), ~$8504 + 1824 EUR (30 assi, vita seriale, braccio RS00).
  Affianca il BOM RobStride, non sostituisce.
- 2026-06-16 (AI+utente): LOWER-BODY BLOCCATO per il CAD, dopo studio Tien Kung 2.0/3.0, Unitree H2, ToddlerBot.
  (a) VITA = SERIALE DIRETTA yaw(basso) + roll(alto sopra lo yaw, asse X), NIENTE pitch, NIENTE puntoni. Supera i
  puntoni del 2026-06-14. Motivo: RL-FRIENDLY (Unitree stessa e' passata dai puntoni del G1 al seriale Z-Y-X sull'H2,
  "more RL-friendly"; noi facciamo RL in Isaac Lab; i meccanismi paralleli = catena chiusa + gioco rod-end = gap
  sim-to-real). Stack 2 DOF ~130-150 mm accettato (Tien Kung 3.0 lo fa). Pitch del busto lo fanno le ANCHE. -1 RS06 ->
  30 motori. Totali (dopo RS02->RS00 punto d E caviglia->RS00 punto e): completo 14.594,69 EUR (Fase1 10.113,96 /
  Fase3 3.015,28), massa 32,227 kg, lineup RS00x18 / RS04x6 / RS05x2 / RS06x4 (RS06 solo hip-yaw+vita; RS02 ELIMINATO).
  (b) ANCA = F-A-R ortogonale (Flexion-Abduction-Rotation, come H2), pitch nel BACINO verso l'ESTERNO (G1/R1), assi
  ortogonali puliti, NIENTE canting. Idea utente "stella 60°" (cantare i pitch gamba) valutata a fondo e scartata MA
  con onesta': se canti ENTRAMBI gli assi i due motori SI SOMMANO sul pitch puro (regione di coppia a ROMBO: pitch puro
  fino a 2*tau*cos(phi), es. 208 Nm a 30deg, > ortogonale; ma il combinato pitch+roll cade dentro il rombo, peggio del
  quadrato ortogonale). Il caso che dimensiona = gamba d'appoggio = pitch+roll INSIEME -> vince l'ortogonale. E noi
  siamo torque-starved (RS04 0,86x), non possiamo scommettere; l'H2 canta perche' ha 360 Nm di surplus, noi no. Per
  uccidere il collo di bottiglia dei 139 la via pulita = motore piu' grosso (AKE90-8 170 Nm), non il canting. DA
  VALIDARE in sim: loggare la traiettoria di coppia (pitch,roll) all'anca; se i gait risultano pitch-dominanti, il
  canting si riapre. Per ora CAD ortogonale (reversibile: cambia solo l'orientamento sedi motore).
  (c) CAVIGLIA = PARALLELA, motori NELLO STINCO. Motore = RS00 a riduzione ~2:1 [AGGIORNATO 2026-06-16, vedi punto e:
  prima avevo messo RS06 1:1 "per la potenza", ma il REQUISITO e' solo CAMMINO + 1 kg/braccio, NIENTE salti/corsa ->
  potenza caviglia modesta, RS00 basta; gli RS06 Ø88 impilati sotto il ginocchio arrivavano quasi a terra]. Precedente
  forte: RoboEra ~70 kg usa motori piccoli con riduzione ~2:1 roll / ~1.5:1 pitch e SALTA. A ~2:1 i 2 RS00 sommano:
  2x14x2=56 Nm picco (ok 33-40 kg; a 46 kg ~2.5:1->70). RS06 1:1 resta alt qty0 SE servono gait dinamici/salti. Asse
  motore lungo X (stile G1), scelta utente. Rod-end: con gli SPHERICAL gia' scelti (igubal ±35°) basta orientare il perno cosi' che il
  PITCH grande = rotazione LIBERA attorno al perno (illimitata) e il ROLL piccolo (±15°) = tilt entro ±35°. NON fare
  teste revolute-revolute pure (si impunta = sovravincolo spaziale); ricetta sicura = RSU (Revolute-Spherical-Universal,
  come il paper IIT), tenere almeno uno snodo sferico/universale. Bloccaggio lunghezza puntone: controdado sottile
  (mezzo spessore M8 ~4 mm) + Loctite 243; se manca spazio, tarare con la regolabile poi SOSTITUIRE con asta FISSA
  tagliata a misura (piu' rigida, meno gioco -> meglio sim-to-real). Ibrida "roll diretto nel piede" = Piano B solo se
  il sim-to-real del 2-DOF parallelo si rivela un incubo (e in tal caso roll con motore leggero Encos 377 g).
  (d) RS02 ELIMINATO da tutto il BOM (scelta utente 2026-06-16). Insight utente (CORRETTO): nella gamma RobStride l'RS02
  e' DOMINATO. Quote: RS00 Ø57 / 5 nom-14 picco / 310 g; RS02 Ø78.5 / 6 nom-17 picco / 405 g; RS06 Ø88 / 11 nom-36
  picco / 621 g. Da RS00->RS02 paghi +21,5 mm di Ø per soli +3 Nm picco; da RS02->RS06 paghi solo +9,5 mm per +19 Nm
  (2x). Quindi RS02 e' quasi grosso come RS06 ma con meta' coppia: REGOLA = "se basta RS00 metti RS00 (molto piu'
  piccolo), senno' salta a RS06; mai RS02". Applicato: BRACCIO tutto RS00 (spalla pitch/roll + gomito declassati da RS02;
  spalla yaw + polso gia' RS00). Tien Kung (70 kg) ha motori ~Ø60 = TAGLIA di un RS00 ma sono ENCOS DENSI (~36 Nm), NON
  un RS00 (14 Nm): taglia != coppia. CAVIGLIA: RS00 NO (giunto di POTENZA) -> resta RS06 a 1:1 (la coppia si moltiplica
  con la riduzione, la POTENZA no: un motore piccolo + riduzione da' tanta coppia ma a bassa velocita', e al toe-off
  serve coppia E velocita' insieme = potenza, che solo un motore fisicamente piu' grande -RS06- o denso -Encos- ha). Per
  caviglia compatta E potente = Encos A4310 premium (la via di Tien Kung). Spalla con RS00 OK: e' giunto LENTO, conta
  solo la coppia, e RS00 (14 picco) copre il dinamico ~12; l'hold orizzontale continuo non lo faceva nemmeno l'RS02
  (6<6.8 nom). Gomito: RS00 ~1,2 kg continui / 2 kg picco (poco meno dell'RS02); RS06 solo se serve 2 kg continui.
  Lineup finale: vedi punto (e).
  (e) CAVIGLIA -> RS00 a ~2:1 + CATALOGO ENCOS + MIXING (2026-06-16). REQUISITO confermato dall'utente: cammino normale
  + stare in piedi stabile + 1 kg per braccio, NIENTE salti/corsa. Con questo la caviglia NON e' un giunto ad alta
  potenza -> RS00 a riduzione ~2:1 basta (vedi punto c). LINEUP FINALE: RS00x18 (braccio 14 + caviglia 4) / RS04x6
  (gambe) / RS05x2 (collo) / RS06x4 (SOLO hip-yaw 2 + vita 2). 30 motori, 32,227 kg, 14.594,69 EUR.
  CATALOGO ENCOS spulciato (Foxtech): il piu' piccolo e' l'EC-A4310-P2-36 (36 Nm, 377 g, ~Ø60, frame Ø43). Sotto i
  43 mm Encos NON ha niente -> per polso/braccio (5-14 Nm) nessun Encos: l'A4310 sarebbe overkill, piu' pesante
  dell'RS00 (377 vs 310 g) e ~6x il prezzo. Gli altri Encos sono tutti PIU' GROSSI: A6408 (Ø64), A8112 (Ø81, ~94 Nm,
  830 g), A10020 (Ø100, ~150 Nm), A13715/A13720 (Ø137, ~320 Nm). Quindi l'UNICO Encos utile = A4310, e solo dove c'e'
  l'RS06 (hip-yaw/vita) o per una caviglia DINAMICA. CASCATA: con "solo cammino" la caviglia va a RS00 (310 g, piu'
  leggero E piu' economico dell'A4310 377 g/$700) -> l'Encos perde la sua applicazione migliore (la massa distale della
  caviglia). Restano hip-yaw+vita (4 motori): -244 g x4 = ~1 kg, ma ~$2800 + 3a marca. Quindi per il NOSTRO uso il
  premium Encos e' poco interessante. MIXING Encos+RobStride: FATTIBILE (entrambi CAN), ma costo SOFTWARE non nullo =
  2 driver di protocollo + 2 modelli attuatore in sim + 2 calibrazioni + connettori diversi; ~GRATIS in sim (basta
  parametri diversi per giunto), pesa solo sull'HW reale. "Tutto uguale" e' nettamente piu' semplice per build e
  sim-to-real (1 driver, 1 modello, ricambi uniformi). Conclusione: tutto RobStride (RS00/04/05/06) -> niente mixing,
  problema evitato. Scheda premium: aggiunta colonna DIMENSIONI per tutti i motori (richiesta utente).
- 2026-06-14 (AI+utente) [SUPERATO il 2026-06-16: vita ora SERIALE diretta, NON piu' puntoni - vedi bullet sotto]: VITA - R1 in serie VALUTATO e SCARTATO, si resta sui PUNTONI (schema G1). Motivo
  geometrico (numeri veri dal BOM): il roll vita e' un RS06 Ø88; in serie roll-sotto-yaw il DIAMETRO Ø88 mangia
  altezza -> base busto/yaw a ~190 mm sopra l'asse anca = torso mozzo per batteria+compute. R1 se lo permette solo
  perche' ha motori minuscoli, noi no. Scartata anche la "bomba dietro" stile Figure (abbassa lo yaw ma da' solo
  ROLL, niente pitch, e la staffa a sbalzo porta tutto il momento flettente del busto). PUNTONI = scelta giusta per
  motori grandi: stessa logica della caviglia (motori pesanti BASSI nel bacino, asse trasversale, zero stack
  verticale, massa giu' per CoM) e in piu' si riprende il PITCH del busto (chinarsi/raccogliere da terra; R1 non
  ce l'ha). Costo: vita resta a 3 motori (yaw + 2 puntoni), 31 assi totali, 35,012 kg. BOM e scheda premium gia'
  ri-allineati ai puntoni. NB: confermato anche hip pitch nel bacino verso l'ESTERNO (schema G1/R1, non Figure).
- 2026-06-10 (AI+utente): BUDGET DISALLINEAMENTO rod-end caviglia (da foto giunti X-Humanoid ~±45° e RobotEra ~±30°,
  che pero' usano BALL-STUD automotive, non rod-end). Fisica: il perno piede ROLLA col piede -> il tilt richiesto agli
  occhi LATO PIEDE e' ~1:1 col roll (+~3 margine); il pitch costa 0 (rotazione attorno al perno); gli occhi in alto
  (lancetta) ~0-2. CORREZIONE: i puntoni lunghi tolgono solo la parte fuori piano (~1-2 deg), non la componente
  principale. Rod-end economici AliExpress: tilt tipico ±12-15 (MISURARE all'arrivo con inclinometro). Piano: (1) partire
  con limite roll ±12 nei fine-corsa e nell'URDF (camminata piana usa ±5-10 -> basta); (2) upgrade quasi gratis =
  spaziatori conici high-misalignment sui 2 occhi lato piede -> ±20-25, copre target G1 ±15 con margine, compatibile col
  passante M6; (3) upgrade estremo = ball-stud (perno conico verticale nel piede, ridisegno locale) -> ±30-45, non ora.
- 2026-06-10 (AI): SUPERATO il punto (3) sopra — trovato in catalogo igus l'igubal **KBRM-08 CL** (2a gen, corpo
  esagonale + controdado): **pivot ±35 gradi**, foro sfera Ø8 E10, filetto femmina M8, 8.6 g, carichi 2.1 kN breve /
  1.05 kN continuo (aste nostre ~0.6-1.2 kN picco breve -> OK). Drop-in TOTALE: stesse aste alluminio M8 + stesso perno
  vite a colletto Ø8xM6, da montare solo sui 2 occhi LATO PIEDE (lato lancetta tilt ~0-2 -> resta standard). Eguaglia i
  ball-stud RobotEra (±30) restando a catalogo; KBLM-08 CL = filetto sinistro. Nota 2026-06-27: BOM corrente usa invece
  **KARM-08 CL / KARM_08_CL_1 maschio M8 destro qty2 + KALM-08 CL maschio M8 sinistro qty2**; questa vecchia nota resta
  solo come storia della selezione. Il vecchio percorso qty0 era: spaziatori conici M8->M6 (Competition Supplies/McGill, ±20-25)
  sui rod-end metallici. Scoperta collaterale: gli
  snodi angolari industriali DIN 71802 fanno solo 15-18 gradi, NON sono i giunti delle foto RobotEra/X-Humanoid.
  Scaletta roll caviglia: ±13 stock -> ±20-25 spacers -> ±35 igubal CL. Nota igubal: e' plastica igumid G, verificare
  prezzo dal configuratore e niente alte temperature.
- 2026-06-10 (AI+utente): ARCHITETTURA PUNTONE definitiva (domande: perno a 10? barra filettata come corpo?).
  (a) Il PERNO resta Ø8xM6: non e' l'anello debole (flessione ~70-90 MPa vs >900 snervamento 12.9; il limite e' la
  testa plastica igubal). Salire a Ø10 NON rinforza la testa e costringe filetti M10 -> corpo asta M10 piu' pesante.
  Riserva: KARM-10 CL (2.5 kN breve, ±35) solo se il CAD tiene bracci piede mini e il caso peggiore supera 1.2 kN.
  (b) NIENTE barra filettata come corpo del puntone: M8 acciaio filettata (anima ~6.5) a 250 mm ha Pcr ~2.7 kN -> SF
  ~2.3 sul picco 1.15 kN, MA e' 4x meno rigida a flessione dell'esagono alluminio (EI 1.7e7 vs 7.1e7 Nmm2) = 'ballerina'
  (vibra/flette), filetto = intaglio a fatica, peso simile. Il corpo GIUSTO e' l'esagono ALLUMINIO del kit AliExpress
  (femmina M8 DX+SX, Pcr ~10+ kN, SF ~9-18): si tiene quello.
  (c) Testa lato piede = igubal KARM-08 CL MASCHIO M8 (±35, 1.7 kN breve / 0.85 continuo, 6.2 g): si avvita nel corpo
  alluminio al posto della testa metallica stock. Lato lancetta = testa stock (tilt ~0-2), che fa anche da lato
  sinistro per la regolazione (KALM CL 'in preparation' a catalogo, disponibilita' da verificare). BOM aggiornata
  2026-06-27: `2 x KARM-08 CL` maschio destro + `2 x KALM-08 CL` maschio sinistro, con `4 x` controdadi sottili DIN
  439 M8. KBRM/KBLM femmina resta solo variante storica/catalogo e non va usata senza cambiare il corpo puntone.

## Punti aperti da criticare prima degli acquisti

1. Disegnare la caviglia in CAD e calcolare la matrice tra coppie motori RS06 e coppie virtuali pitch/roll. Se il margine
   non basta provare RS03; se invece il rapporto crank da' riduzione si puo' scendere a RS02 (caviglia piu lenta, asta ~1
   kN). La taglia caviglia esce dal rapporto crank reale, non dal carico (che fissa solo la coppia GIUNTO). Baseline corrente:
   giunto gimbal caviglia stampato con due shoulder screws Ø8/M6 x 45 mm impilati in Z (pitch sopra, roll sotto) e
   quattro pivot puntoni Ø8/M6 x 16 mm; i rod-end attivi sono igus KARM-08 CL qty 2 destro + KALM-08 CL qty 2 sinistro.
   Tenere volume aperto per un eventuale
   Cardan piu pulito, ma il CAD/sim deve modellare l'offset reale finche esiste. Separare nel CAD i due assi piede-stinco
   dai perni su cui spingono i puntoni. Per ciascun asse/perno quotare larghezza del pezzo centrale, spazio assiale,
   volume spazzato dalle orecchie e dai rod-end, diametro esterno sede, lunghezza colletto, fit, boccole, antirotazione
   e ritegno; solo allora scegliere eventuali boccole, inserti metallici e rasamenti finali.
2. Disegnare la vita in CAD con roll sotto yaw: RS03 waist roll sotto, RS06 waist yaw sopra, nessun waist pitch e nessun
   puntone/cardano vita nel CAD corrente. Verificare stack verticale, cavi, supporto del torso e momento flettente sul
   roll; il vecchio 6002-2RS idle bearing e il pin Ø12/M10 sono disattivati qty0 e non vanno comprati salvo revisione CAD.
3. Trovare una fonte fisica affidabile o misurare i motori collo G1-Comp. Fino ad allora RS05 x2 resta una scelta
   provvisoria, non un dato G1 verificato.
4. Polso tutto RS00 (5 nom/14 picco, dual encoder): verificare in CAD/uso che basti sul roll (G1 25 Nm, ma gravita ~0 e
   payload sull'asse). Riserve qty0: RS02 (robusta) e RS05 (ultraleggera pitch/yaw).
5. Ricostruire la geometria gambe dalle origini giunti e mesh ufficiali G1 `mode_11`, senza confondere mesh esterne e CAD
   interno degli attuatori.
6. Verificare fisicamente l'ingombro RS04 `120 x 120 x 56 mm` nelle anche e al ginocchio: la potenza e vicina al G1, ma
   il packaging non e automaticamente equivalente.
7. Progettare harness e strain relief. K-Scale segnala esplicitamente che il cablaggio e una delle parti meno affidabili.
8. Chiedere a Bicycle Motor Works conferma di spedizione Italia, massa finita, connettori/charger, durata dei 100 A,
   corrente di corto, limite di carica rigenerativa e soglie BMS; in parallelo chiedere a Tõuksi Vabrik un disegno del
   fallback UE 60 A entro 165 x 102 x 76 mm. Confermare che il BF1 principale da 70 A sia coordinato col BMS.
   Prima della camminata misurare correnti e temperature
   e dimensionare energia/soglia del bleeder sulla frenata reale: quello selezionato e sufficiente solo per bring-up
   progressivo finche non esistono misure dinamiche.
9. Valutare se Thor e gia posseduto o se va mantenuto nel costo: per il solo bring-up e sovradimensionato.
