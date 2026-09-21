#!/usr/bin/env python3
"""Regenerate the "umanoide" tab with Unitree G1 baseline and RobStride motors."""
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.filters import CustomFilter, CustomFilters, FilterColumn


ROOT = Path(__file__).resolve().parent
DST = ROOT / "BOM umanoide G1 - RobStride.xlsx"
IVA = 0.22
H = "#H"

wb = Workbook()
ws = wb.active
ws.title = "umanoide"

headers = [
    "Item", "Supplier", "Unit cost", "VAT/Duties", "VAT/Duties amount",
    "Qty", "Total", "Weeks", "Destination", "Delivery", "Test",
    "Status", "Serial", "Description / purpose", "Notes", "Category",
    "Purchase link", "Phase", "Mass (kg)", "CAD 3D",
]
ws.append(headers)

# ---- PHASE RE-PLAN 2026-07-19 (user decision): phases now follow the REAL build order.
# Phase 1 = arm+hand teleop bench (right arm, right hand, ankle linkage kit using the arm's
#           RS06s, battery + dual-source, full safety chain, Thor [owned], torso on a table).
# Phase 2 = legs & locomotion (RS04/RS03/dedicated ankle RS06, leg wiring, IMU).
# Phase 3 = completion (left arm, left hand [owned], waist, neck, audio, mobile integration).
# Filter the Phase column for the shopping list of each stage.

# rows whose quantity spans phases are SPLIT into per-stage rows here (name suffix, qty, fase)
ROW_SPLIT = {
    "RobStride 06 - proximal shoulder pitch/roll": [(" - RIGHT arm", 2, "Fase 1"), (" - LEFT arm", 2, "Fase 3")],
    "RobStride 00 - light shoulder yaw": [(" - RIGHT arm", 1, "Fase 1"), (" - LEFT arm", 1, "Fase 3")],
    "RobStride 06 - elbow": [(" - RIGHT arm", 1, "Fase 1"), (" - LEFT arm", 1, "Fase 3")],
    "RobStride 00 - uniform 3-axis wrist: roll": [(" - RIGHT arm", 1, "Fase 1"), (" - LEFT arm", 1, "Fase 3")],
    "RobStride 00 - uniform 3-axis wrist: pitch/yaw": [(" - RIGHT arm", 2, "Fase 1"), (" - LEFT arm", 2, "Fase 3")],
    "per RS00/RS05/RS06 superiori": [(" - RIGHT arm", 8, "Fase 1"), (" - left arm + waist/neck", 9, "Fase 3")],
    "04980921GXM5 - portafusibile": [(" - main + right arm", 2, "Fase 1"), (" - legs", 2, "Fase 2"), (" - waist + left arm", 2, "Fase 3")],
    "fusibile ramo braccio": [(" - RIGHT arm", 1, "Fase 1"), (" - LEFT arm", 1, "Fase 3")],
    "MKS CANable Pro": [(" - right arm bus", 1, "Fase 1"), (" - left arm + waist/neck buses", 2, "Fase 3")],
}
# phase corrections for un-split rows (matched on the final English name, first hit wins)
PHASE_TO = [
    ("Molicel P45B compact battery", "Phase 1"), ("Supplier-matched 54.6V charger", "Phase 1"),
    ("XT90S anti-spark", "Phase 1"), ("Dual-source 48 V OR-ing", "Phase 1"),
    ("USB TO 2CH RS485", "Phase 1"), ("LINDY 36940", "Phase 1"),
    ("MINI fuse for both hands", "Phase 1"), ("0430250400", "Phase 1"),
    ("0430300040", "Phase 1"), ("RH56DFX-2R", "Phase 1"),
    ("RobStride 04 - legs", "Phase 2"), ("RobStride 03 - leg hip yaw", "Phase 2"),
    ("ankle pushrod/differential drive", "Phase 2"), ("cable for leg RS06 motors", "Phase 2"),
    ("XT30UW-F.G.Y", "Phase 2"), ("GHR-02V-S", "Phase 2"), ("MINI-SSHL", "Phase 2"),
    ("9841", "Phase 2"), ("leg branch fuse", "Phase 2"),
    ("CABATR16", "Phase 2"), ("CABATN16", "Phase 2"), ("Klauke 703F5", "Phase 2"),
    ("MOT0110", "Phase 2"), ("CBL4011", "Phase 2"),
    ("USB TO AUDIO", "Phase 3"), ("AS03604AR", "Phase 3"), ("LINDY 41899", "Phase 3"),
]
def phase_to(final_name, fase):
    low = final_name.lower()
    for k, ph in PHASE_TO:
        if k.lower() in low:
            return ph
    return fase

# commodity items -> big mainstream suppliers (user preference 2026-07-19); old verified
# source stays in the note and the old exact link stays as technical reference
SUPPLIER_SWAP = {}  # blanket swap reverted 2026-07-19: equivalents must be REAL products,
# verified per row (item+SKU+link+supplier together); rows without a verified common-store
# equivalent keep their original specialist supplier

# data tuple:
# (nome, fornitore, costo netto stimato EUR, unita, categoria, fase, descrizione, note, link)
rows = [
    (H, "1 - MECHANICAL PROTOTYPE - 2-axis ankle offset gimbal + M8 pushrods"),
    (
        "[SELECTED qty0] Ankle foot-shin 2-axis offset gimbal - igus sliding bush concept (decision 2026-06-03, updated to Ø8/M6 pins)",
        "internal print + standard hardware", 0, 0, "Meccanica", "Fase 1",
        "Selected architecture: compact 2-axis ankle gimbal with two Ø8/M6 shoulder screws stacked in Z, not a perfect intersecting-axis universal joint. Higher-Z 45 mm pin = pitch axis; lower-Z 45 mm pin = roll axis. The gimbal pins are not the same function as the pushrods: gimbal pins define the foot-shin joint axes; pushrod pins carry the rod-end spherical bearings.",
        "Current pin choice from user update 2026-06-27: Ø8/M6 black shoulder screws from AliExpress, 2 x 45 mm for the ankle gimbal and 4 x 16 mm for the pushrod rod-end pivots, plus 6 M6 retaining nuts. Pushrod length adjustment uses M8 right-hand/left-hand rod-end threads plus 4 x M8 DIN 439 thin jam nuts. Model the real pitch/roll Z offset in CAD/simulation; do not assume an ideal single-center Cardan map. Bushing/bearing choice still depends on the CAD stack-up.",
        "https://github.com/unitreerobotics/unitree_ros/blob/master/robots/g1_description/g1_29dof_mode_11.urdf",
    ),
    (
        "[ALT qty0] SKF PCM 121420 E - boccola radente PTFE composito 12x14x20 mm",
        "Cuscinetti e Componenti", 2.13, 0, "Meccanica", "Fase 1",
        "Esempio reale di boccola radente sottile per un asse diametro 12 mm del giunto piede-stinco: foro 12 mm, esterno 14 mm, lunghezza 20 mm.",
        "SKU esatto SKF PCM121420E. Prezzo verificato 2026-06-02: EUR 2.13 netto. Alternativa candidata per oscillazione lenta; qty 0 finche CAD, carichi, accoppiamento perno-sede e controllo assiale non sono definiti.",
        "https://cuscinettiecomponenti.it/prodotto/pcm-121420-e-boccole-di-usura-12x14x20-skf/",
    ),
    (
        "[ALT qty0] SKF PCM 121425 E - boccola radente PTFE composito 12x14x25 mm",
        "Cuscinetti e Componenti", 2.94, 0, "Meccanica", "Fase 1",
        "Esempio reale piu lungo della stessa famiglia: foro 12 mm, esterno 14 mm, lunghezza 25 mm. Dimostra che una boccola unica lunga 25 mm e un componente standard.",
        "SKU esatto SKF PCM121425E. Prezzo verificato 2026-06-02: EUR 2.94 netto. Qty 0: la maggiore lunghezza non e automaticamente migliore se introduce disallineamento o se il CAD non offre una sede corretta.",
        "https://cuscinettiecomponenti.it/prodotto/pcm-121425-e-boccole-di-usura-12x14x25-skf/",
    ),
    (
        "[ALT qty0] igus iglidur Q2SM-1214-20 - boccola polimerica heavy-duty 12x14x20 mm",
        "igus / EBMiA", 6.15, 0, "Meccanica", "Fase 1",
        "Esempio polimerico autolubrificante per asse diametro 12 mm: esterno 14 mm, lunghezza 20 mm. Il materiale Q2 e sviluppato per applicazioni pivotanti con carichi dinamici, urti e sporco.",
        "SKU esatto igus Q2SM-1214-20. Prezzo verificato 2026-06-02: PLN 25.89 netto, circa EUR 6.15. Qty 0: verificare pressione superficiale, usura, sede e tolleranze con il tool igus prima della selezione.",
        "https://www.ebmia.pl/tuleje-slizgowe-iglidur-q2/199876-tuleja-slizgowa-q2sm-1214-20.html",
    ),
    (
        "[ALT qty0] igus iglidur Q2FM-1214-12 - boccola flangiata heavy-duty 12x14x12 mm",
        "igus", 0, 0, "Meccanica", "Fase 1",
        "Esempio di boccola radente flangiata per perno diametro 12 mm: guida il carico radiale e offre una battuta assiale integrata. Dimensioni: foro 12 mm, esterno 14 mm, lunghezza 12 mm, flangia diametro 20 mm spessa 1 mm.",
        "SKU esatto igus Q2FM-1214-12. Qty 0: utile se il CAD permette una boccola inserita da ciascun lato del pezzo mobile; non assumere che due pezzi da 12 mm entrino nella larghezza disponibile. Q2 e indicato da igus per carichi elevati, urti, sporco e applicazioni pivotanti fortemente sollecitate.",
        "https://www.igus.co.uk/iglidur-ibh/flanged-bearings/product-details/iglidur-q2-m?artnr=Q2FM-1214-12",
    ),
    (
        "[ARCHIVIATO qty0] igus GTM-1224-015 - ralla separata (superata: assiale ora nella flangia) 12x24x1.5 mm",
        "Conrad", 1.22, 0, "Meccanica", "Fase 1",
        "Ralla radente separata da registrare sul pezzo centrale mobile tra questo e ciascuna orecchia esterna quando la boccola radiale non ha flangia. Porta lo strisciamento assiale su una superficie progettata allo scopo.",
        "SKU esatto igus GTM-1224-015: foro 12 mm, esterno 24 mm, spessore 1.5 mm. Prezzo verificato 2026-06-02: EUR 1.49 IVA inclusa su Conrad. Qty 0: non lasciarla libera tra due facce PA-CF. Prevedere una sede di registrazione e una controfaccia metallica fissa, liscia e sostituibile nell'orecchia; definire gioco assiale nel CAD.",
        "https://www.conrad.com/en/p/igus-gtm-1224-015-shim-ring-bore-diameter-12-mm-1416586.html",
    ),
    (
        "[ARCHIVIATO qty0] SKF HK 1216.2RS - rullini senza anello interno (superato) 12x18x16 mm",
        "Cuscinetti e Componenti", 0, 0, "Meccanica", "Fase 1",
        "Alternativa volvente compatta per il solo carico radiale del perno diametro 12 mm. Va alloggiata nel pezzo mobile oppure nella coppia di orecchie, non contemporaneamente in entrambi. Non possiede un anello interno da serrare tra gli spallamenti delle orecchie.",
        "SKU esatto SKF HK1216.2RS: foro 12 mm, esterno 18 mm, lunghezza 16 mm, tenute su entrambi i lati. Disponibilita verificata 2026-06-02: 21 pezzi, prezzo su quotazione. Qty 0: richiede che il perno fisso sia una pista interna temprata e rettificata adeguata; non far lavorare automaticamente i rullini su una vite o un perno grezzo. Non e la prima scelta se si vogliono serrare spallamenti contro un vero anello interno.",
        "https://cuscinettiecomponenti.it/prodotto/hk-1216-2rs-cuscinetti-a-rullini-12x18x16-skf/",
    ),
    (
        "[ARCHIVIATO qty0] SKF NKI 12/16 - rullini con anello interno (superato dal radente igus flangiato) 12x24x16 mm",
        "Klium", 22.15, 0, "Meccanica", "Fase 1",
        "Prima architettura semplice da disegnare: cuscinetto nel pezzo centrale mobile; anello interno separabile serrato tra gli spallamenti integrati delle due orecchie PA-CF; anello esterno in sede nel centro mobile. Porta il carico radiale senza richiedere cappelli metallici nelle orecchie.",
        "SKU esatto SKF NKI 12/16: foro 12 mm, esterno 24 mm, larghezza 16 mm, anello interno incluso. Prezzo verificato 2026-06-02: EUR 22.15 netto su Klium. Qty 0 fino al CAD. Gli spallamenti devono serrare l'anello interno senza schiacciare il pezzo centrale mobile; il gioco di funzionamento e tra parte mobile e orecchie, non tra spallamenti e anello interno. NKI non e un reggispinta: se i test mostrano contatto assiale, aggiungere ralle igus registrate oppure un reggispinta separato.",
        "https://www.klium.nl/en/skf-nki-12-16-needle-roller-bearing-with-inner-ring-12x24x16-mm-41676",
    ),
    (
        "[ARCHIVIATO qty0] SKF AXK 1226 - reggispinta (superato: assiale ora nella flangia) 12x26x2 mm",
        "RS Italia", 4.10, 0, "Meccanica", "Fase 1",
        "Alternativa volvente per carico assiale: una gabbia reggispinta per ciascun lato del pezzo centrale mobile se il CAD richiede attrito assiale molto ridotto.",
        "SKU esatto SKF AXK 1226: foro 12 mm, esterno 26 mm, spessore 2 mm, carico dinamico 9.15 kN e statico 30 kN. Prezzo verificato 2026-06-02: EUR 4.10 netto su RS Italia. Qty 0: tra facce stampate usare due ralle temprate AS 1226 per ciascuna gabbia.",
        "https://it.rs-online.com/web/p/cuscinetti-a-rulli/0514243",
    ),
    (
        "[ARCHIVIATO qty0] SKF AS 1226 - ralla temprata per AXK (superato) 12x26x1 mm",
        "Cuscinetti e Componenti", 1.86, 0, "Meccanica", "Fase 1",
        "Pista assiale temprata per la gabbia AXK 1226. Con facce PA-CF o polimeriche non usare direttamente il pezzo stampato come pista dei rullini.",
        "SKU esatto SKF AS1226: foro 12 mm, esterno 26 mm, spessore 1 mm. Prezzo e stock verificati 2026-06-02: EUR 1.86 netto, 13 pezzi disponibili. Qty 0: una soluzione completa per lato occupa 1 + 2 + 1 = 4 mm: AS 1226 + AXK 1226 + AS 1226.",
        "https://cuscinettiecomponenti.it/prodotto/as-1226-cuscinetti-a-rullini-12x26x1-skf/",
    ),
    (
        "[ARCHIVIATO qty0] HGI PS 12x18x1 DIN 988 - rasamento di registro (superato) ",
        "Cuscinetti.net", 0.48, 0, "Meccanica", "Fase 1",
        "Rasamento metallico per calibrare il gioco assiale residuo dopo aver scelto la superficie reggispinta. Non sostituisce una ralla radente igus o una pista temprata per AXK.",
        "SKU esatto HGI12X18X1 / PS12X18X1: foro 12 mm, esterno 18 mm, spessore 1 mm. Prezzo e stock verificati 2026-06-02: EUR 0.48 netto, 57 pezzi. Qty 0: scegliere la combinazione finale solo dopo misura dell'assieme; DIN 988 esiste anche in spessori piu fini, ad esempio 0.2 mm.",
        "https://www.cuscinetti.net/e-catalogue/181768-rondella-di-spessoramento-ps-12x18x1-din-988-hgi.html",
    ),
    (
        "[ALT DA DIMENSIONARE qty0] Inserti metallici flangiati fissi nelle orecchie caviglia - controfacce per asse diam. 12 mm",
        "Elesa+Ganter DIN 172 / lavorazione custom", 0, 0, "Meccanica", "Fase 1",
        "Due inserti a cappello per asse, pressati o registrati nelle orecchie esterne PA-CF: il foro interno guida o contiene il perno fisso diametro 12 mm; la flangia rivolta verso il pezzo centrale offre una controfaccia assiale metallica liscia alla ralla igus.",
        "Alternativa da tenere documentata se si usa la boccola igus centrale stampata oppure se gli spallamenti PA-CF non risultano sufficienti. Riferimento preliminare CAD: orecchio sinistro circa 20 mm + pezzo centrale mobile con boccola circa 20 mm + orecchio destro circa 20 mm = circa 60 mm di corpi strutturali. I cappelli vanno su entrambe le orecchie. Attenzione: una flangia sporgente aumenta il pacco; incassarla nell'orecchia se si vuole restare vicini ai 60 mm. Il foro del cappello guida il perno ma non lo rende automaticamente solidale alle orecchie: progettare anche antirotazione e ritegno assiale.",
        "https://www.elesa.com/siteassets/PDF/PDF_IT/DIN%20172.pdf",
    ),
    (
        "[OPZIONALE UPGRADE qty0] Elesa+Ganter GN.12825 / DIN 172-B12-20-A - controfaccia metallica nell'orecchia, foro 12 L20",
        "Verzolla Italia", 6.89, 0, "Meccanica", "Fase 1",
        "Candidato standard per ciascuna orecchia se si stampa la boccola centrale igus: bussola guida temprata a cappello, foro interno 12 mm F7, esterno 18 mm n6, flangia diametro 22 mm, corpo lungo 20 mm e flangia spessa 4 mm.",
        "SKU esatto Elesa+Ganter DIN172-B12-20-A / GN.12825, codice Verzolla Y1137. Prezzo e disponibilita verificati 2026-06-02: EUR 6.89 cad, 5 disponibili. Qty 0: quantita attesa se usata su entrambi gli assi e su entrambe le caviglie = 8 pezzi, ma attivare solo dopo CAD. Per mantenere il riferimento circa 60 mm incassare la flangia da 4 mm nell'orecchia; verificare inoltre controfaccia, fit nel PA-CF e antirotazione del perno.",
        "https://www.verzolla.com/elesa-bussola-di-guida-flangiata-din172-b12-20-a-y1137",
    ),
    (
        "[ALT FORNITORE qty0] Otto Ganter 172-B12-20-A - cappello metallico flangiato foro 12 mm, L20",
        "Best4Automation", 5.26, 0, "Meccanica", "Fase 1",
        "Secondo fornitore dello stesso cappello normalizzato DIN 172-B12-20-A: acciaio, foro 12 mm, esterno 18 mm, flangia 22 mm, lunghezza corpo 20 mm, flangia 4 mm.",
        "Prodotto esatto Ganter 172-B12-20-A. Prezzo e consegna verificati 2026-06-02: EUR 5.26 netto cad, indicato spedibile in 2-3 giorni lavorativi; vendita B2B. Qty 0: alternativa di approvvigionamento allo stesso componente Verzolla.",
        "https://www.best4automation.com/positionierbuchse-mit-bund-bohrung-eins.-gerundet-sc-4042-172-b12-20-a/",
    ),
    (
        "[ALT EQUIVALENTE qty0] KIPP K1022.A1200X20 - cappello metallico flangiato DIN 172 foro 12 mm, L20",
        "Normteile Leinigen", 4.50, 0, "Meccanica", "Fase 1",
        "Equivalente DIN 172 forma A di altro produttore per lo stesso dimensionamento preliminare: bussola a cappello in acciaio con foro interno 12 mm e lunghezza 20 mm.",
        "SKU esatto KIPP K1022.A1200X20. Prezzo e disponibilita verificati 2026-06-02: EUR 4.50 netto / EUR 5.36 IVA inclusa cad, indicato disponibile con consegna 2-5 giorni. Qty 0: alternativa standard da verificare dimensionalmente contro il disegno KIPP prima dell'ordine.",
        "https://www.normteile-leinigen.de/Bundbohrbuchse-12-x-20-DIN-172-Form-A/K1022.A1200X20",
    ),
    (
        "[SCHEDA qty0] Elesa+Ganter DIN 172-B12-20-A - pagina tecnica TME",
        "TME", 9.27, 0, "Meccanica", "Fase 1",
        "Pagina tecnica di un ulteriore distributore per lo stesso cappello Ganter: acciaio temprato, foro interno 12 mm, esterno 18 mm, flangia 22 mm, lunghezza 20 mm.",
        "SKU esatto TME DIN172-B12-20-A. Verificato 2026-06-02: USD 10.04 circa EUR 9.27 cad, ma stock TME indicato zero. Tenerlo come catalogo tecnico e backup di richiesta disponibilita, non come fornitore primario immediato.",
        "https://www.tme.eu/en/details/din172-b12-20-a/indexing-plungers/elesa-ganter/din-172-b12-20-a/",
    ),
    (
        "[ALT CUSTOM qty0] Boccola radente stampata 3D in igus iglidur i150",
        "igus / stampa interna", 0, 0, "Meccanica", "Fase 1",
        "Primo provino custom stampabile per gli assi diametro 12 mm del giunto piede-stinco. Permette di iterare lunghezza, flangia e gioco. i150 e il tribofilamento igus piu facile da processare.",
        "Materiale confermato tra quelli che l'utente sta acquistando per confronto. Qty 0: non e ancora la scelta finale. Validare pressione superficiale, usura, orientamento di stampa, finitura del perno, tolleranze e gioco; non assumere automaticamente equivalenza con Q2 stampato a iniezione o SKF metallo/PTFE.",
        "https://www.igus.eu/product/iglidur_I150_PF",
    ),
    (
        "[ALT CUSTOM qty0] Boccola radente stampata 3D in igus iglidur i190",
        "igus / stampa interna", 0, 0, "Meccanica", "Fase 1",
        "Secondo provino custom stampabile per gli assi diametro 12 mm del giunto piede-stinco. i190 e il candidato da confrontare quando servono maggiore resistenza meccanica e resistenza all'usura.",
        "Materiale confermato tra quelli che l'utente sta acquistando per confronto. Qty 0: non e ancora la scelta finale. Il filamento e sensibile all'umidita: seguire essiccazione e istruzioni igus. Validare pressione superficiale, usura, orientamento, tolleranze e gioco.",
        "https://www.igus.eu/product/iglidur_I190_PF",
    ),
    (
        "[SCELTO PRIMARIO qty0] Boccola STAMPATA multimateriale J260+PA-CF integrale (radiale + flangia assiale)",
        "igus / stampa interna", 0, 0, "Meccanica", "Fase 1",
        "Approccio PRIMARIO scelto: stampare la boccola direttamente integrale al pezzo mobile PA-CF in FDM multimateriale, con J260 sia sul foro (radiale) sia sulle facce di flangia (assiale). Nessun acquisto se la stampa regge.",
        "Filamento J260-PF gia acquistato dall'utente. igus indica estrusione ~280 C, piano ~120 C, preferibile camera riscaldata. Da validare in modo specifico: adesione all'interfaccia J260/PA-CF (rischio principale del multimateriale), orientamento di stampa per roundness e usura del foro, finitura e Ø reale (prevedere alesatura/taratura), pressione superficiale, gioco. Qty 0: gestita dal filamento, non da uno SKU. i150 e i190 restano provini di confronto.",
        "https://www.igus.eu/product/716",
    ),
    (
        "[SCELTO FALLBACK qty0] Boccola flangiata igus GFM-1214 (iglidur G) - radiale + assiale, acquistabile",
        "igus / RS / Misumi / Minetti", 0, 0, "Meccanica", "Fase 1",
        "Versione ACQUISTATA della boccola flangiata, fallback se la stampa multimateriale J260 non regge: foro 12, esterno 14, flangia circa 20 x 1. La flangia fa l'assiale; due per asse, flange verso l'esterno, piantate a pressione nel pezzo mobile. Drop-in stesse quote: Q2FM-1214 (heavy-duty urti/sporco), JFM-1214 (basso attrito).",
        "Famiglia SKU GFM-1214 iglidur G. Lunghezza b1 dal CAD (es. due da 9-10 mm in un mobile da 20 mm). Fornitori multipli verificati 2026-06-03: igus diretto, RS, Misumi IT, Minetti, F.lli Bono, Solema, ERIKS. Qty 0 finche il CAD non da le lunghezze; quantita attesa 8 (2 per asse x 4 assi) solo se si comprano invece di stamparle. Ritegno: interferenza nella sede + flangia di battuta; mai cianoacrilato, al limite Loctite 603/638. Prezzo da verificare a configurazione lunghezza.",
        "https://www.igus.eu/iglide-ibh/flanged-bearings/product-details/iglidur-g-m",
    ),
    (
        "[SECOND SOURCE qty0] AliExpress black shoulder screw listing - old backup source for shoulder screws",
        "AliExpress", 3, 0, "Meccanica", "Fase 1",
        "Backup purchase listing for black shoulder screws. The current first choice is the newer AliExpress listing in the active Ø8/M6 rows below.",
        "Kept as second source only. Do not use the old Ø12/M10 ankle-axis assumption for the current CAD unless the ankle is deliberately redesigned around Ø12 pins again.",
        "https://it.aliexpress.com/item/1005007481484485.html",
    ),
    (
        "[CATALOGO qty0] RS PRO 822-9316 - vite a colletto M10, spallamento diam. 12 x 20 mm",
        "RS Italia", 7.928, 0, "Meccanica", "Fase 1",
        "Esempio industriale acquistabile di vite a spallamento: filetto M10, diametro spallamento 12 mm, lunghezza spallamento 20 mm, acciaio nero classe 12.9.",
        "SKU esatto RS PRO 822-9316. Prezzo verificato 2026-06-02: EUR 31.71 netto per sacchetto da quattro, EUR 7.928 cad. Qty 0: la lunghezza 20 mm e solo un riferimento di catalogo; scegliere la lunghezza effettiva dopo il CAD.",
        "https://it.rs-online.com/web/p/viti-a-colletto/8229316",
    ),
    (
        "[ALT qty0] RS PRO 292-417 - vite a colletto ISO 7379 M10, gambo Ø12 x 60 mm (alternativa industriale al nero AliExpress)",
        "RS Italia", 7.905, 0, "Meccanica", "Fase 1",
        "Riferimento vicino al primo pacco CAD caviglia circa 60 mm: vite ISO 7379 con tratto liscio diametro 12 mm lungo 60 mm, filetto M10 x 16 mm, testa diametro 18 x 8 mm, lunghezza totale 84 mm.",
        "SKU esatto RS PRO 292-417, ISO 7379 gambo Ø12 x 60, filetto M10 x 16, testa Ø18 x 8. ALTERNATIVA industriale (il perno scelto e' ora la vite a colletto nera AliExpress Ø12xM10): fa da pista su cui scorre l'igus e da ritegno. Reso solidale alle orecchie dal serraggio (dado M10 + Loctite 243), non da piantaggio; fit gambo-foro orecchia scorrevole-bloccato (snug), niente interferenza forte nel PA-CF. Qty attesa 4 (un asse ciascuno) + scorte, ma qty 0 finche il CAD non fissa la lunghezza colletto (~60-70). Fornitori alternativi ISO 7379-12-M10: Rubix GN.35185, Elesa, Puntoviti, Berardi, KIPP.",
        "https://it.rs-online.com/web/p/viti-a-colletto/0292417",
    ),
    (
        "[CATALOGO qty0] Motedis 12h6 - albero precisione diam. 12 mm h6 temprato e rettificato",
        "Motedis", 0, 0, "Meccanica", "Fase 1",
        "Alternativa da tagliare a misura quando serve un perno fisso cilindrico senza testa. Utile anche come pista temprata e rettificata se si valuta un cuscinetto HK privo di anello interno.",
        "Codice prodotto Motedis 12h6. Qty 0: prezzo dipendente dalla lunghezza di taglio. Definire lunghezza e ritegno; non sostituisce automaticamente una vite a spallamento.",
        "https://www.motedis.it/it/Albero-di-precisione-12-mm-h6-acciaio-temprato-e-rettificato",
    ),
    (
        "[CATALOGO qty0] Wurth DIN 6325 / ISO 8734 - spina cilindrica temprata diam. 12 mm",
        "Wurth", 0, 0, "Meccanica", "Fase 1",
        "Famiglia industriale di spine cilindriche temprate e rettificate, tolleranza m6. La pagina collegata mostra l'esempio diametro 12 x 20 mm; la famiglia offre altre lunghezze.",
        "Catalogo utile al CAD, qty 0. Wurth segnala che DIN 6325 e stata sostituita da DIN EN ISO 8734. Non scegliere 20 mm solo perche e la variante collegata: misurare prima la larghezza dell'assieme e progettare il ritegno.",
        "https://eshop.wurth.fr/Goupille-cylindrique-DIN-6325-acier-brut-GOUPILLE-CYL-DIN6325-M6-12X20/025201220.sku/fr/FR/EUR/",
    ),
    (
        "[DA DIMENSIONARE qty0] Ritegni perni e supporti giunto caviglia",
        "Amazon / Ruland / piastrina custom", 0, 0, "Meccanica", "Fase 1",
        "Ritegni smontabili dei due assi di rotazione del giunto piede-stinco.",
        "Ripristinato il catalogo storico: assortimento seeger interni/esterni. Prevedere spallamento stampato o inserto metallico da un lato e ritegno rimovibile dall'altro. Non assumere dado M10, seeger, collare o piastrina prima del CAD: il sistema dipende dal tipo di perno e dalle sedi effettive.",
        "https://www.amazon.it/ANELLI-ELASTICI-INTERNI-ESTERNI-ASSORTITI/dp/B09CZKWD5J",
    ),
    (
        "[SCELTO RITEGNO qty0] Dado autobloccante M10 NERO DIN 985 + Loctite 243 - serra assi Ø12xM10 (caviglia + cardano vita)",
        "Amazon / AliExpress", 0.3, 0, "Meccanica", "Fase 1",
        "Ritegno terminale degli assi rotazione Ø12xM10: il dado M10 serra il filetto della vite a colletto e la rende solidale alle orecchie (4 assi caviglia + 2 cardano vita).",
        "Ritegno SCELTO: dado autobloccante M10 NERO (DIN 985, set nylock M3-M16) + Loctite 243. Qty attesa 6 (4 caviglia + 2 cardano vita) + scorte; qty 0 fino a CAD. Variante pulita: filettare in un inserto metallico annegato nell'orecchia lontana, cosi il serraggio reagisce su metallo e non comprime il PA-CF.",
        "https://www.amazon.it/Acciaio-Controdado-Esagonale-Inserto-Autobloccante/dp/B0C8ZCR6B1",
    ),
    (
        "M6 nuts for Ø8/M6 shoulder screws - ankle gimbal + pushrod pivots",
        "Amazon / AliExpress", 0.2, 6, "Meccanica", "Fase 1",
        "Six standard M6 nuts for the selected Ø8/M6 shoulder screws: 2 nuts for the 45 mm ankle gimbal screws and 4 nuts for the 16 mm pushrod rod-end pivot screws. Geometry to reserve in CAD: M6 hex across flats 10 mm, circumscribed hex diameter about 11.55 mm; normal M6 locknut height is about 6 mm.",
        "These M6 nuts retain the shoulder screws only; they are not the pushrod length-adjustment jam nuts. Use locknuts or standard M6 nuts with Loctite 243 after checking that the shoulder, not the threaded section, defines the working width. The nut must clamp the screw stack without crushing the rod-end spherical bearing.",
        "https://www.amazon.it/Acciaio-Controdado-Esagonale-Inserto-Autobloccante/dp/B0C8ZCR6B1",
    ),
    (
        "[CATALOGO qty0] RS PRO 797-6254 - rondella larga M10 DIN 9021 inox, 10.5x30x2.5 mm",
        "RS Italia", 0, 0, "Meccanica", "Fase 1",
        "Rondella larga da valutare sotto testa e dado della vite a spallamento per distribuire il serraggio sulle superfici esterne delle orecchie PA-CF.",
        "SKU esatto RS PRO 797-6254: foro 10.5 mm, esterno 30 mm, spessore 2.5 mm, inox A2, DIN 9021. Qty 0: verificare spazio e quantita dopo CAD. Non usare il serraggio per flettere significativamente le orecchie: il perno e tenuto dal serraggio assiale a quota nominale.",
        "https://it.rs-online.com/web/p/rondelle/7976254",
    ),
    (
        "[CATALOGO qty0] Ruland MSP-12-F - collare split smontabile per perno diam. 12 mm",
        "Ruland", 8.65, 0, "Meccanica", "Fase 1",
        "Collare in due pezzi per ritegno o registro assiale di un perno cilindrico diametro 12 mm quando lo spazio esterno lo consente. Diametro esterno 28 mm, larghezza 11 mm.",
        "SKU esatto MSP-12-F. Prezzo verificato 2026-06-02: USD 9.39 circa EUR 8.65. Qty 0: e un riferimento acquistabile, non la scelta automatica; verificare ingombro esterno e carichi assiali.",
        "https://www.ruland.com/msp-12-f.html",
    ),
    (
        "AliExpress adjustable aluminum M8 pushrod - 140 mm ankle link",
        "AliExpress", 7, 2, "Meccanica", "Fase 1",
        "Adjustable aluminum M8 pushrod/link for the parallel/differential ankle. Selected long variant: 140 mm. CAD body mass estimate: 23.8 g each, excluding the separately listed igubal ends and M8 jam nuts.",
        "Length-dependent estimate, not the incorrect former generic 90 g: 6061-class aluminium tube assumed OD 12 mm, ID 8 mm, density 2.70 g/cm3 gives 0.1696 g/mm x 140 mm = 23.8 g. Confirm the delivered tube OD/ID and whether the advertised 140 mm is body length or eye-to-eye, then replace this estimate with a scale measurement. Turnbuckle adjustment requires one M8 RH and one M8 LH end.",
        "https://it.aliexpress.com/item/1005008935554718.html",
    ),
    (
        "AliExpress adjustable aluminum M8 pushrod - 40 mm ankle link",
        "AliExpress", 7, 2, "Meccanica", "Fase 1",
        "Adjustable aluminum M8 pushrod/link for the parallel/differential ankle. Selected short variant: 40 mm. CAD body mass estimate: 6.8 g each, excluding the separately listed igubal ends and M8 jam nuts.",
        "Length-dependent estimate, not the incorrect former generic 90 g: same assumed OD 12 mm / ID 8 mm 6061-class aluminium tube gives 0.1696 g/mm x 40 mm = 6.8 g. Confirm delivered geometry and enough thread engagement/misalignment margin, then replace with a scale measurement. The selected spherical ends are separate igus RH/LH M8 rows.",
        "https://it.aliexpress.com/item/1005008935554718.html",
    ),
    (
        "[ALT qty0] Testa a snodo SKF SA8E M8 destra, foro 8 mm",
        "SKF", 8, 0, "Meccanica", "Fase 1",
        "Upgrade di precisione lato piede.",
        "Usare insieme a SAL8E e tubo tenditore.",
        "https://www.acorn-ind.co.uk/p/skf/rod-ends-with-male-thread/sa8e-skf/",
    ),
    (
        "[ALT qty0] Testa a snodo SKF SAL8E M8 sinistra, foro 8 mm",
        "SKF", 10, 0, "Meccanica", "Fase 1",
        "Upgrade di precisione lato motore.",
        "Filetti opposti destra/sinistra per la regolazione.",
        "https://www.acorn-ind.co.uk/p/skf/rod-ends-with-male-thread/sal8e-skf/",
    ),
    (
        "[ALT qty0] Tubo tenditore M8 DIN 1478",
        "mbo Osswald", 9, 0, "Meccanica", "Fase 1",
        "Corpo del puntone per upgrade SKF.",
        "",
        "https://www.mbo-osswald.de/en/configurators/joint-rod-configurator",
    ),
    (
        "igus igubal KARM-08 CL / KARM_08_CL_1 - M8 right-hand male rod end, Ø8 bore, ±35°",
        "igus", 0, 2, "Meccanica", "Fase 1",
        "Selected right-hand spherical rod ends for the ankle pushrods: igus igubal KARM-08 CL, model KARM_08_CL_1, male M8 right-hand thread, Ø8 E10 ball bore for the Ø8/M6 shoulder screws, pivot angle ±35°, weight 6.2 g each.",
        "Active user choice 2026-06-27, corrected 2026-06-27 for turnbuckle adjustment: qty 2 right-hand ends. Pair one KARM right-hand end with one KALM left-hand end per pushrod so rotating the aluminum body changes length. Plastic housing igumid G with iglide L280 ball. Loads from igus catalog: 1.7 kN short-term / 0.85 kN continuous in tension. Price is left 0 until the exact igus cart/quote is confirmed.",
        "https://www.igus.com/product?artNr=KARM-08-CL",
    ),
    (
        "igus igubal KALM-08 CL - M8 left-hand male rod end, Ø8 bore, ±35°",
        "igus / ERIKS", 0, 2, "Meccanica", "Fase 1",
        "Selected left-hand spherical rod ends for the ankle pushrods: igus igubal KALM-08 CL family, male M8 left-hand thread, Ø8 E10 ball bore for the Ø8/M6 shoulder screws, target pivot angle ±35° matching the KARM-08 CL geometry.",
        "Active qty 2 as the left-hand mate to the two KARM right-hand ends. Availability must be confirmed before ordering: older igus catalog text says KALM-CL left-hand was in preparation, while distributors list KALM-08-CL-J. If KALM-08-CL cannot be bought, fallback is either keep the stock left-hand metal rod end on the low-angle side or redesign the rod body/adapters; do not replace this with a female KBLM/KBRM part unless the pushrod body changes to male threaded studs.",
        "https://shop.eriks.de/de/waelzlager-gelenklager-und-gelenkkoepfe-gelenkkoepfe/gelenkkopf-wartungsfrei-igumid-g-iglidur-j-aussengewinde-links-serie-kalm-cl-j-pr2079035551789/",
    ),
    (
        "DIN 439 M8 thin jam nut, right-hand thread - pushrod length lock",
        "Accu / Fabory", 0.5, 2, "Meccanica", "Fase 1",
        "Thin right-hand jam nuts for locking the two KARM-08 right-hand rod ends after pushrod length adjustment. Standard DIN 439 / ISO 4035 M8 x 1.25 geometry: height along thread 4.0 mm, across flats 13 mm, circumscribed hex diameter about 15.0 mm.",
        "Use one jam nut on each right-hand rod end. This is M8, not M6, because it locks on the rod-end external thread. Final supplier/finish can be generic DIN 439 A2/A4 or zinc steel; CAD clearance should reserve the 15 mm circumscribed diameter.",
        "https://www.accu.co.uk/thin-hexagon-nuts/73062-HFN-M8-A2",
    ),
    (
        "DIN 439 M8 thin jam nut, left-hand thread - pushrod length lock",
        "Accu / Fabory", 0.5, 2, "Meccanica", "Fase 1",
        "Thin left-hand jam nuts for locking the two KALM-08 left-hand rod ends after pushrod length adjustment. Standard DIN 439 / ISO 4035 M8 x 1.25 left-hand geometry: height along thread 4.0 mm, across flats 13 mm, circumscribed hex diameter about 15.0 mm.",
        "Use one jam nut on each left-hand rod end. A normal right-hand nut will not fit the KALM left-hand thread. CAD clearance should reserve the 15 mm circumscribed diameter and wrench access to the 13 mm flats.",
        "https://accu-components.com/us/left-hand-thread-hex-jam-nuts/73142-HFNL-M8-A2",
    ),
    (
        "[UPGRADE ROLL qty0] Spaziatori conici high-misalignment M8->M6 per rod-end metallici (coppia)",
        "Competition Supplies / McGill Motorsport", 0, 0, "Meccanica", "Fase 1",
        "Coppia di boccole a gradino/cono: parte cilindrica nel foro Ø8 della sfera, cono stretto verso le orecchie, bullone M6 passante. L'occhio tocca il cono invece della faccia larga -> +8-12 gradi/lato = ±20-25 totali sui rod-end metallici standard.",
        "Alternativa economica all'igubal CL per alzare il roll dei rod-end ATTUALI: il perno passa da colletto Ø8 a M6 semplice (meno sezione, ok per ~1-2 kN). Fonti: Competition Supplies 'High misalignment spacer M8 to M6' (coppia, metrico), McGill Motorsport pack 6/10, Midwest Control HMBZC-M8-M6 (USA). Su AliExpress cercare 'heim joint misalignment spacer 8mm'. Qty al CAD.",
        "https://www.competitionsupplies.com/rod-ends-spherical-bearings/rod-end-bearing-accessories/high-misalignment-spacers-metric/high-misalignment-spacer-m8-to-m6-pair",
    ),
    (
        "AliExpress black shoulder screw Ø8 x M6 x 45 mm - ankle gimbal pitch/roll axes",
        "AliExpress", 2, 2, "Meccanica", "Fase 1",
        "Selected shoulder screws for the ankle offset gimbal: Ø8 mm shoulder diameter, M6 thread, 45 mm shoulder length. Use two screws stacked in Z: higher screw = pitch axis, lower screw = roll axis.",
        "FIRST CHOICE listing from user update 2026-06-27, revised after lower-leg CAD screenshot. This is intentionally an offset gimbal, so CAD/simulation must use the measured pitch-roll Z offset rather than an ideal intersecting-axis Cardan approximation. Add Loctite 243 and M6 nut/locknut as listed above.",
        "https://it.aliexpress.com/item/1005007885495357.html",
    ),
    (
        "AliExpress black shoulder screw Ø8 x M6 x 16 mm - pushrod rod-end pivots",
        "AliExpress", 2, 4, "Meccanica", "Fase 1",
        "Selected shoulder screws for the M8 pushrod rod-end pivots: Ø8 mm shoulder diameter, M6 thread, 16 mm shoulder length. The Ø8 shoulder passes through the rod-end spherical bearing.",
        "FIRST CHOICE listing from user update 2026-06-27. The shoulder length must match the printed/metal clevis stack plus running clearance so the nut clamps the shoulder stack, not the spherical bearing.",
        "https://it.aliexpress.com/item/1005007885495357.html",
    ),
    (
        "[CATALOGO qty0] Motedis W8H6 - albero precisione diam. 8 mm h6 temprato e rettificato",
        "Motedis", 0, 0, "Meccanica", "Fase 1",
        "Alternativa da tagliare a misura per il perno trasversale piede diametro 8 mm sul quale si montano le due teste a snodo M8.",
        "Codice prodotto Motedis W8H6: acciaio CF53 temprato e rettificato, tolleranza h6. Qty 0: prezzo dipendente dalla lunghezza di taglio. Progettare distanziali tra le sfere e ritegni laterali.",
        "https://www.motedis.it/it/Albero-di-precisione-8-mm-h6-acciaio-temprato-e-rettificato",
    ),
    (
        "[CATALOGO qty0] Ruland MSP-8-F - collare split smontabile per perno diam. 8 mm",
        "Ruland", 7.67, 0, "Meccanica", "Fase 1",
        "Collare in due pezzi per trattenere lateralmente il perno trasversale piede diametro 8 mm se il CAD lascia spazio. Diametro esterno 18 mm, larghezza 9 mm.",
        "SKU esatto MSP-8-F. Prezzo verificato 2026-06-02: USD 8.33 circa EUR 7.67. Qty 0: valutare due collari oppure un altro ritegno solo dopo aver definito il piede.",
        "https://www.ruland.com/msp-8-f.html",
    ),
    (
        "[DEACTIVATED qty0] Waist roll idle-side pin - black AliExpress shoulder screw Ø12 x M10",
        "AliExpress", 3, 0, "Meccanica", "Fase 3",
        "Deactivated historical waist-roll idle support pin. It belonged to an older direct-roll support concept with a pin and bearings on the side opposite the roll motor.",
        "DEACTIVATED 2026-06-27 after user clarified this idle support is not necessary in the current waist CAD. Keep as historical reference only; reactivate only if CAD later adds an opposite-side waist-roll support.",
        "https://it.aliexpress.com/item/1005007481484485.html",
    ),
    (
        "[DEACTIVATED qty0] 6002-2RS bearing, 15 mm bore (15x32x9) - waist roll idle support",
        "123Bearing", 6, 0, "Meccanica", "Fase 3",
        "Deactivated historical bearing pair for the older waist-roll idle support. This is not part of the current waist CAD and is not required for purchase.",
        "DEACTIVATED 2026-06-27: this belonged to the old idea of an opposite-side idle support for waist roll. User confirmed it is not necessary. Do not buy unless the waist CAD later adds this support.",
        "https://www.123bearing.com/bearing-housing/deep-groove-bearing/single-row/6002-2rs",
    ),
    (
        "Inserti filettati a caldo ottone M3/M4/M5",
        "Prusa / VXB", 25, 1, "Meccanica", "Fase 1",
        "Filetti riutilizzabili nelle parti stampate PA-CF.",
        "",
        "https://www.prusa3d.com/product/threaded-inserts-m4-short-50-pcs/",
    ),
    (
        "Viti assortimento M3/M4/M5 + dadi + rondelle",
        "Amazon", 35, 1, "Meccanica", "Fase 1",
        "Ferramenta per motori, staffe e coperchi.",
        "Link a prodotto specifico. Verificare profondita dei fori ciechi sui motori prima del montaggio e integrare solo le misure mancanti.",
        "https://www.amazon.it/SANTOO-Acciaio-Esagonale-Assortimento-Fissaggio/dp/B07RV2SFX6",
    ),
    (
        "ISO 4762 socket-head cap screw M3 x 10 mm, steel, full thread",
        "MISUMI / Würth / RS", 0.04, 8, "Mechanical", "Phase 1",
        "Eight installed on the two RS05 neck actuators: four per actuator. Thread length is 10 mm; the socket head is not included in this length.",
        "Standard ISO 4762/DIN 912 size. Approximate single-screw mass 0.88 g. Its mass is already included in the RS05 CAD assembly mass so this row has no mass entry and must not be double-counted.",
        "https://it.misumi-ec.com/vona2/detail/110302217940/?HissuCode=CB3-10",
    ),
    (
        "ISO 4762 socket-head cap screw M3 x 15 mm, steel, full thread",
        "MISUMI / Würth / RS", 0.05, 184, "Mechanical", "Phase 1",
        "Installed motor fasteners: 8 per RS06 x 11 actuators plus 12 per RS00 x 8 actuators = 184 screws. Thread length is 15 mm; head excluded.",
        "Standard ISO 4762/DIN 912 size. Approximate single-screw mass 1.11 g. Mass is already included in the RS06 and RS00 CAD assembly masses; do not double-count it in the BOM mass total.",
        "https://it.misumi-ec.com/vona2/detail/110302217940/?HissuCode=CB3-15",
    ),
    (
        "[CATALOG qty0] ISO 4762 socket-head cap screw M3 x 20 mm, steel, full thread",
        "MISUMI / Würth / RS", 0.06, 0, "Mechanical", "Phase 1",
        "Widely available standard M3 length; thread length 20 mm, head excluded.",
        "Catalog option only until a CAD joint needs it. Fractional 7.5 / 12.5 / 17.5 mm M3 lengths are not normal ISO stock sizes and are intentionally not listed.",
        "https://it.misumi-ec.com/vona2/detail/110302217940/?HissuCode=CB3-20",
    ),
    (
        "[CATALOG qty0] ISO 4762 socket-head cap screw M4 x 10 mm, steel, full thread",
        "MISUMI / Würth / RS", 0.05, 0, "Mechanical", "Phase 1",
        "Widely available standard M4 length; thread length 10 mm, head excluded.",
        "Catalog option only until a CAD joint needs it. Fractional 7.5 / 12.5 / 17.5 / 22.5 mm M4 lengths are not normal ISO stock sizes and are intentionally not listed.",
        "https://it.misumi-ec.com/vona2/detail/110302217940/?HissuCode=CB4-10",
    ),
    (
        "ISO 4762 socket-head cap screw M4 x 15 mm, steel, full thread",
        "MISUMI / Würth / RS", 0.06, 201, "Mechanical", "Phase 1",
        "Installed motor fasteners: 6 per RS06 x 11 actuators + 15 per RS04 x 6 actuators + 15 per RS03 x 3 actuators = 201 screws. Thread length is 15 mm; head excluded.",
        "Standard ISO 4762/DIN 912 size. Approximate single-screw mass 2.175 g. Mass is already included in the RS06, RS04 and RS03 CAD assembly masses; do not double-count it in the BOM mass total.",
        "https://it.misumi-ec.com/vona2/detail/110302217940/?HissuCode=CB4-15",
    ),
    (
        "ISO 4762 socket-head cap screw M4 x 20 mm, steel, full thread",
        "MISUMI / Würth / RS", 0.07, 12, "Mechanical", "Phase 1",
        "Six installed on each RS05 neck actuator, two actuators total. Thread length is 20 mm; head excluded.",
        "Standard ISO 4762/DIN 912 size. Approximate single-screw mass 2.85 g. Mass is already included in the RS05 CAD assembly mass; do not double-count it in the BOM mass total.",
        "https://it.misumi-ec.com/vona2/detail/110302217940/?HissuCode=CB4-20",
    ),
    (
        "[CATALOG qty0] ISO 4762 socket-head cap screw M4 x 25 mm, steel, full thread",
        "MISUMI / Würth / RS", 0.08, 0, "Mechanical", "Phase 1",
        "Widely available standard M4 length; thread length 25 mm, head excluded.",
        "Catalog option only until a CAD joint needs it. Use a true standard 20 or 25 mm length instead of an uncommon fractional length.",
        "https://it.misumi-ec.com/vona2/detail/110302217940/?HissuCode=CB4-25",
    ),
    (
        "Loctite 243 frenafiletti medio",
        "Amazon", 10, 1, "Meccanica", "Fase 1",
        "Frenafiletti per le viti soggette a vibrazione.",
        "Link a prodotto specifico; verificare prezzo al checkout.",
        "https://www.amazon.it/Loctite-243-Frenafiletti-resistenza-azione/dp/B003ZUXQIA",
    ),

    (H, "2 - LEG MOTORS - Unitree G1 29-DOF baseline, single RobStride ecosystem"),
    (
        "RobStride 04 - legs: hip pitch/roll + knee (3/leg)",
        "Seeed / RobStride", 235, 6, "Motori", "Fase 1",
        "Axes: hip pitch/roll + knee, 3 per leg. RobStride PDF 2025-06-26 dimensions: OD 120 mm, length 56 mm. Weight: 1.420 kg. RobStride torque: 40 Nm rated, 120 Nm peak.",
        "G1 mode_11 reference: hip pitch/roll and knee 139 Nm. RS04 is the strongest RobStride model but is still 0.86x of the G1 139 Nm reference; accept this knowingly or leave the RobStride range. Hip yaw is RS03 in the current balanced configuration.",
        "https://www.seeedstudio.com/Robostride-04-Actuator-p-6775.html",
    ),
    (
        "RobStride 03 - leg hip yaw (1/leg)",
        "Seeed / RobStride", 214, 2, "Motori", "Fase 1",
        "Axis: hip yaw, 1 per leg. RobStride PDF 2025-06-26 dimensions: OD 98 mm, length 54.1 mm. Weight: 0.900 kg. RobStride torque: 20 Nm rated, 60 Nm peak.",
        "G1 mode_11 reference: hip yaw 88 Nm. This is a mostly vertical yaw axis, so gravity torque is near zero and demand is mainly dynamic. RS03 was chosen over RS06 because the estimated aggressive turn at ~45 kg mass was close to the RS06 36 Nm peak limit. ATTENZIONE 2026-07-18: il CAD corrente monta RS06 (36 Nm picco) su hip yaw; questa riga RS03 resta l'intento di acquisto finche' il SIM GATE non decide: log della coppia hip-yaw in curva su Isaac a ~32+ kg; se satura a 36 Nm si ordina RS03 e si adegua il CAD, altrimenti si declassa questa riga a RS06.",
        "https://www.seeedstudio.com/Robostride-03-Actuator-p-6774.html",
    ),
    (
        "RobStride 06 - ankle pushrod/differential drive A/B (2/leg)",
        "Seeed / RobStride", 200, 4, "Motori", "Fase 1",
        "Physical ankle actuators A/B: 2 motors per leg in the shin, acting through two pushrods. Do not label them as direct pitch/roll motors in CAD: virtual pitch and roll come from geometry and the A/B mixing map. RobStride PDF 2025-06-26 dimensions: OD 88 mm, length 49 mm. Weight: 0.621 kg. RobStride torque: 11 Nm rated, 36 Nm peak.",
        "G1 mode_11 reference: 35 Nm per virtual ankle axis. With two RS06 motors, ideal pitch torque can sum up to 72 Nm peak before linkage losses; roll uses the difference/combined torque through the real linkage matrix. CAD still has to close the crank/foot ratio and motor-to-pitch/roll conditioning.",
        "https://www.seeedstudio.com/Robostride-06-Actuator-p-6668.html",
    ),
    (
        "[ALT qty0] RobStride 00 - lighter ankle option with about 2:1 mechanical advantage (2/leg)",
        "Seeed / RobStride", 116, 0, "Motori", "Fase 1",
        "Light ankle alternative: 2 motors per leg through pushrods. RobStride PDF 2025-06-26 dimensions: OD 57 mm, length 51 mm. Weight: 0.310 kg. RobStride torque: 5 Nm rated, 14 Nm peak.",
        "G1 mode_11 reference: 35 Nm per virtual ankle axis. Only suitable for calm walking with about 2:1 mechanical advantage and verified pushrod forces. Saves 1.244 kg versus four RS06 motors but reduces speed and toe-off margin. Not selected in the balanced configuration.",
        "https://www.seeedstudio.com/Robostride-00-Actuator-p-6664.html",
    ),

    (H, "2b - UPPER BODY - direct serial waist roll+yaw + mode_11 arms + G1-Comp neck"),
    (
        "RobStride 06 - G1 waist yaw",
        "Seeed / RobStride", 200, 1, "Motori sup.", "Fase 3",
        "Axis: waist yaw, vertical motor mounted above the lower waist-roll stage and rotating the torso/yaw assembly. RobStride PDF 2025-06-26 dimensions: OD 88 mm, length 49 mm. Weight: 0.621 kg. RobStride torque: 11 Nm rated, 36 Nm peak.",
        "G1 mode_11 reference: waist yaw 88 Nm. RS06 downgrade checked: this is a mostly vertical yaw axis with near-zero gravity torque; estimated torso twist is about 28 Nm, below the 36 Nm peak. Current CAD order: roll below yaw, no waist pitch, no waist pushrods.",
        "https://www.seeedstudio.com/Robostride-06-Actuator-p-6668.html",
    ),
    (
        "RobStride 03 - direct serial waist roll below yaw",
        "Seeed / RobStride", 210, 1, "Motori sup.", "Fase 3",
        "Axis: waist roll, direct front-back axis mounted below the yaw joint. RobStride PDF 2025-06-26 dimensions: OD 98 mm, length 54.1 mm. Weight: 0.900 kg. RobStride torque: 20 Nm rated, 60 Nm peak.",
        "G1 mode_11 reference: waist roll 35 Nm. Current CAD order from user update 2026-06-27: waist roll below yaw, no waist pitch; torso pitch comes from the hips. Model the serial order explicitly because placing roll below yaw means the yaw assembly rides on the roll joint.",
        "https://www.seeedstudio.com/Robostride-03-Actuator-p-6774.html",
    ),
    (
        "RobStride 06 - proximal shoulder pitch/roll (2/arm)",
        "Seeed / RobStride", 200, 4, "Motori sup.", "Fase 3",
        "Axes: proximal shoulder pitch/roll, 2 per arm. RobStride PDF 2025-06-26 dimensions: OD 88 mm, length 49 mm. Weight: 0.621 kg. RobStride torque: 11 Nm rated, 36 Nm peak.",
        "G1 mode_11 reference: shoulder pitch/roll 25 Nm per axis. With a horizontal arm and 1 kg payload, updated static estimate is about 10.8 Nm: RS06 is almost exactly at continuous rating and exceeds G1 at peak. RS00 would not hold this pose continuously.",
        "https://www.seeedstudio.com/Robostride-06-Actuator-p-6668.html",
    ),
    (
        "[ALT qty0] RobStride 00 - spalla pitch/roll alleggerita (2/braccio)",
        "Seeed / RobStride", 116, 0, "Motori sup.", "Fase 3",
        "Assi: alternativa leggera shoulder pitch/roll. Dimensioni: 57 x 57 x 51 mm. Peso: 0.310 kg. Coppia RobStride: 5 Nm nominali, 14 Nm picco.",
        "Riferimento G1 mode_11: shoulder pitch/roll 25 Nm per asse. Risparmierebbe 1.244 kg sui quattro giunti ma non puo tenere continuativamente il braccio orizzontale con payload 1 kg. Mantenuta solo come alternativa per braccia molto leggere e pose intermittenti.",
        "https://www.seeedstudio.com/Robostride-00-Actuator-p-6664.html",
    ),
    (
        "RobStride 00 - light shoulder yaw (1/arm)",
        "Seeed / RobStride", 116, 2, "Motori sup.", "Fase 3",
        "Axis: shoulder yaw, the most distal shoulder axis. RobStride PDF 2025-06-26 dimensions: OD 57 mm, length 51 mm. Weight: 0.310 kg. RobStride torque: 5 Nm rated, 14 Nm peak.",
        "G1 mode_11 reference: shoulder yaw 25 Nm. Downgrade to RS00 checked: yaw rotates the upper arm around its own axis, so gravity load is near zero in the resting vertical pose; expected demand is about 4-6 Nm. RS00 covers it and stays compact.",
        "https://www.seeedstudio.com/Robostride-00-Actuator-p-6664.html",
    ),
    (
        "[SECONDA SCELTA qty0] RobStride 06 - spalla yaw piu robusta (1/braccio)",
        "Seeed / RobStride", 200, 0, "Motori sup.", "Fase 3",
        "Asse: shoulder yaw, alternativa piu robusta. Dimensioni: 88 x 88 x 49 mm. Peso: 0.621 kg. Coppia RobStride: 11 Nm nominali, 36 Nm picco.",
        "Riferimento G1 mode_11: shoulder yaw 25 Nm. Riattivare se la spalla yaw deve muovere carichi a braccio esteso o serve piu coppia/rigidita. Salto diretto RS00->RS06 (RS02 eliminato: dominato, quasi grosso come RS06 ma meta' coppia).",
        "https://www.seeedstudio.com/Robostride-06-Actuator-p-6668.html",
    ),
    (
        "RobStride 06 - elbow (1/arm)",
        "Seeed / RobStride", 200, 2, "Motori sup.", "Fase 3",
        "Axis: elbow, 1 per arm. RobStride PDF 2025-06-26 dimensions: OD 88 mm, length 49 mm. Weight: 0.621 kg. RobStride torque: 11 Nm rated, 36 Nm peak.",
        "G1 mode_11 reference: elbow 25 Nm. Static estimate is about 4.4 Nm with 1 kg payload and 6.6 Nm with 2 kg; RS06 keeps continuous and dynamic margin. RS00 would save 0.622 kg total but would already sit close to rated torque with 1 kg.",
        "https://www.seeedstudio.com/Robostride-06-Actuator-p-6668.html",
    ),
    (
        "RobStride 00 - uniform 3-axis wrist: roll (1/arm)",
        "Seeed / RobStride", 116, 2, "Motori sup.", "Fase 3",
        "Axis: wrist roll, 1 per arm. RobStride PDF 2025-06-26 dimensions: OD 57 mm, length 51 mm. Weight: 0.310 kg. RobStride torque: 5 Nm rated, 14 Nm peak.",
        "G1 mode_11 reference: wrist roll 25 Nm. User choice: all three wrist axes use RS00 for uniformity, dual encoders and compact 57 mm package. RS00 rated torque can hold about 2 kg static in the hand; gravity torque on roll is near zero when the payload lies on the axis.",
        "https://www.seeedstudio.com/Robostride-00-Actuator-p-6664.html",
    ),
    (
        "[SECONDA SCELTA qty0] RobStride 06 - polso 3 assi (riserva piu robusta)",
        "Seeed / RobStride", 200, 0, "Motori sup.", "Fase 3",
        "Riserva robusta per i 3 assi del polso. Dimensioni: 88 x 88 x 49 mm. Peso: 0.621 kg. Coppia RobStride: 11 Nm nominali, 36 Nm picco.",
        "Riferimento G1 mode_11: polso roll 25 Nm, pitch/yaw 5 Nm. Riserva se servisse molta piu coppia/rigidita al polso; salto RS00->RS06 (RS02 eliminato perche' dominato). Per il polso RS00 resta ampiamente sufficiente.",
        "https://www.seeedstudio.com/Robostride-06-Actuator-p-6668.html",
    ),
    (
        "RobStride 00 - uniform 3-axis wrist: pitch/yaw (2/arm)",
        "Seeed / RobStride", 116, 4, "Motori sup.", "Fase 3",
        "Axes: wrist pitch/yaw, 2 per arm. RobStride PDF 2025-06-26 dimensions: OD 57 mm, length 51 mm. Weight: 0.310 kg. RobStride torque: 5 Nm rated, 14 Nm peak.",
        "G1 mode_11 reference: wrist pitch/yaw 5 Nm per axis. RS00 can hold about 2 kg in the hand with margin and stays uniform with wrist roll. Selected RS00, not RS05: RS05 has only 1.6 Nm rated torque.",
        "https://www.seeedstudio.com/Robostride-00-Actuator-p-6664.html",
    ),
    (
        "[SECONDA SCELTA qty0] RobStride 05 - polso pitch/yaw ultraleggero (2/braccio)",
        "Seeed / RobStride", 100, 0, "Motori sup.", "Fase 3",
        "Assi: wrist pitch/yaw, alternativa ultraleggera. Dimensioni: 46 x 46 x 44 mm. Peso: 0.191 kg. Coppia RobStride: 1.6 Nm nominali, 5.5 Nm picco.",
        "Riferimento G1 mode_11: wrist pitch/yaw 5 Nm: RS05 (5.5 picco) e la taglia esatta e pesa solo 0.191 kg. Alternativa all'RS00 SE il payload in mano resta <1 kg: nominale 1.6 Nm limita il carico continuo. Piu leggera ma meno robusta e senza il margine dell'RS00.",
        "https://www.seeedstudio.com/Robostride-05-Actuator-p-6666.html",
    ),
    (
        "RobStride 05 - G1-Comp neck pan/tilt (2 axes)",
        "Seeed / RobStride", 100, 2, "Motori sup.", "Fase 3",
        "Axes: G1-Comp neck pan/tilt. RobStride PDF 2025-06-26 dimensions: OD 46 mm, length 44 mm. Weight: 0.191 kg. RobStride torque: 1.6 Nm rated, 5.5 Nm peak.",
        "G1-Comp reference: official 2-DOF head, but Unitree does not publish the neck motor torque. RS05 is a light provisional choice to validate, not a declared Unitree equivalence.",
        "https://www.seeedstudio.com/Robostride-05-Actuator-p-6666.html",
    ),
    (
        "Inspire Robots RH56DFX-2L dexterous hand, left, without wrist",
        "Reichelt Italia - ALREADY OWNED (lab)", 0, 1, "Upper body", "Phase 3",
        "Left six-actuator dexterous hand without the Inspire wrist module. Six actuated DOF, 12 moving joints, 24 V supply, RS485 communication, 217.8 mm overall length, about 80.7 mm palm width and 0.540 kg mass.",
        "Exact model RH56DFX-2L. ALREADY OWNED (lab stock, 2026-07-19): counted at EUR 0. Reference Reichelt price 2026-07-11: EUR 8,099.16 including Italian 22% VAT. Product table publishes 2 A peak, while the integration manual recommends provisioning up to 5 A. User decision 2026-07-17: both hands share the single WEHO 24 V rail, sized on the published 2 A figure; bench-measure real hand current, and if it approaches the 5 A provisioning recommendation move to the RSD-300C-24 or Cincon 350 W alternatives. Official docs downloaded 2026-07-18 into hands/: the 2026-02 selection guide confirms RH56DFX = RS485/CAN, DC 24 V +/-10%, quiescent 0.09 A, PEAK 2 A, 540 g. Interface per the RH56 series manual: one GX12 5-pin aviation plug carrying both power and RS485 (1 GND, 2 VCC 24 V, 3 A+, 4 B-, 5 GND); confirm the DFX connector is unchanged and request a DFX-specific manual at order. The local single-mesh STL is a cleaned visual/packaging reference, not a watertight manufacturing solid.",
        "https://www.reichelt.com/it/it/shop/prodotto/rh56dfx_-_mano_robotica_destreggiata_senza_polso_sinistra-426921",
    ),
    (
        "Inspire Robots RH56DFX-2R dexterous hand, right, without wrist",
        "Reichelt Italia - ALREADY OWNED (lab)", 0, 1, "Upper body", "Phase 3",
        "Right six-actuator dexterous hand without the Inspire wrist module. Six actuated DOF, 12 moving joints, 24 V supply, RS485 communication, 217.8 mm overall length, about 80.7 mm palm width and 0.540 kg mass.",
        "Exact model RH56DFX-2R. ALREADY OWNED (lab stock, 2026-07-19): counted at EUR 0. Reference Reichelt price 2026-07-11: EUR 8,099.16 including Italian 22% VAT. Product table publishes 2 A peak, while the integration manual recommends provisioning up to 5 A. User decision 2026-07-17: both hands share the single WEHO 24 V rail, sized on the published 2 A figure; bench-measure real hand current, and if it approaches the 5 A provisioning recommendation move to the RSD-300C-24 or Cincon 350 W alternatives. Official docs downloaded 2026-07-18 into hands/: the 2026-02 selection guide confirms RH56DFX = RS485/CAN, DC 24 V +/-10%, quiescent 0.09 A, PEAK 2 A, 540 g. Interface per the RH56 series manual: one GX12 5-pin aviation plug carrying both power and RS485 (1 GND, 2 VCC 24 V, 3 A+, 4 B-, 5 GND); confirm the DFX connector is unchanged and request a DFX-specific manual at order. The local single-mesh STL is a cleaned visual/packaging reference, not a watertight manufacturing solid.",
        "https://www.reichelt.com/it/it/shop/prodotto/rh56dfx_-_mano_robotica_destreggiata_senza_polso_destra-426913",
    ),

    (H, "3 - ALIMENTAZIONE E SICUREZZA BENCH - necessarie prima del primo power-up"),
    (
        "MEAN WELL RSP-3000-48 (48V 3000W)",
        "DigiKey", 511.50, 1, "Alim. motori", "Fase 1",
        "Alimentatore AC/DC da banco: prende 230 VAC dalla presa e genera il bus motori a 48 VDC, fino a 62.5 A / 3000 W. Ingombro 278 x 177.8 x 63.5 mm, peso 4.0 kg. Non sale a bordo del robot.",
        "SKU esatto RSP-3000-48. Prezzo verificato 2026-06-02: EUR 511.50 netto / EUR 618.92 IVA inclusa su DigiKey. Non assorbe automaticamente la rigenerazione: usare bleeder e prove progressive.",
        "https://www.digikey.com/en/products/detail/mean-well-usa-inc/RSP-3000-48/7706324",
    ),
    (
        "Cavo rete Schuko -> estremita libera H07RN-F 3G1.5, 3 m, IP44",
        "Craft Hardware", 8.20, 1, "Alim. motori", "Fase 1",
        "Cavo da collegare ai morsetti AC L/N/terra del Mean Well RSP-3000-48. Non usare IEC C13: il Mean Well ha morsetti e puo assorbire circa 16 A da rete.",
        "SKU esatto EHK22146. Prezzo verificato 2026-06-02: EUR 10.00 IVA inclusa.",
        "https://www.crafthardware.de/en/products/anschlusskabel-3m-h07rn-f-3g1-5",
    ),
    (
        "Schneider XB5AS8442 - fungo emergenza rosso 40 mm, twist release, 1NC",
        "Industry-Electronics", 31.04, 1, "Sicurezza", "Fase 1",
        "Pulsante di emergenza raggiungibile a mano. Il contatto normalmente chiuso comanda la bobina del contattore: premendo il fungo il contattore cade e toglie il 48 V ai motori.",
        "SKU esatto XB5AS8442. Prezzo verificato 2026-06-02: EUR 31.04 netto / EUR 36.94 IVA inclusa. Non porta direttamente la corrente dei motori.",
        "https://industry-electronics.com/schneider-electric/xb5as8442-mushroom-pushbuttons-nc-40mm-red-emergency-stop-drehentr.-kunst.d22mm-lieske_482705.htm",
    ),
    (
        "[REMOVED qty0] Albright SW80B-10 main DC contactor",
        "Radwell Germany", 117.06, 0, "Sicurezza", "Reference",
        "Previous 93 x 59 x 39 mm, 0.400 kg contactor. Electrically valid but removed from the compact humanoid baseline.",
        "Superseded by the smaller exact TE LEV100A5ANG below.",
        "https://www.radwell.de/en-DE/Buy/ALBRIGHT/ALBRIGHT/SW80B-10",
    ),
    (
        "TE Connectivity KILOVAC LEV100A5ANG - 100 A main DC contactor, 24 V coil",
        "DigiKey / Mouser / Farnell", 150.93, 1, "Sicurezza", "Fase 1",
        "Only onboard high-current disconnect. The normally-open contactor removes battery power from all RobStride motor branches when the hardware e-stop opens its 24 V coil circuit. Body diameter 39.5 mm, mounting-flange width 46.3 mm, total height 57.96 mm; mass 0.190 kg.",
        "Exact TE part LEV100A5ANG / 9-1618389-8: SPST-NO, 100 A continuous, 900 VDC contact class, 24 VDC coil, M5 load terminals. The always-on Thor DC/DC remains upstream so loss of control power drops the motor bus.",
        "https://www.digikey.it/it/products/detail/te-connectivity-aerospace-defense-and-marine/LEV100A5ANG/2362833",
    ),
    (
        "Littelfuse BF1 142.5631.5702 - main fuse 70A 58VDC M5 for compact P45B battery",
        "DigiKey", 4.30, 1, "Sicurezza", "Fase 1",
        "Main slow-blow fuse on the positive line, as close as practical to the 48 V source. Protects the 25 mm2 trunk and is a more credible baseline for the selected compact 45 A continuous / 100 A maximum BMS pack than the previous 125 A fuse.",
        "Exact SKU 142.5631.5702: BF1 M5 70 A, 58 VDC, 1 kA interrupting rating. A full 13S pack reaches 54.6 V, so do not use a 32 V automotive fuse. ORDER GATE: confirm BMS trip curve, maximum-current duration, prospective short-circuit current and fuse coordination with the pack supplier before mobile tests.",
        "https://www.digikey.com/en/products/detail/littelfuse-inc/142-5631-5702/2515910",
    ),
    (
        "Littelfuse 04980921GXM5 - portafusibile MIDI/BF1 inline 58VDC con cover",
        "Mouser", 8, 6, "Sicurezza", "Fase 1",
        "Supporto isolato inline con cover e bulloneria M5 per il fusibile principale e per i cinque rami motore: uno principale, due gambe, vita-collo e due braccia.",
        "SKU esatto 04980921GXM5, qty 6. La pagina ufficiale Littelfuse corrente identifica MIDI 498-IL come portafusibile 58 VDC fino a 200 A; esiste un vecchio PDF 32 V obsoleto. Prezzo verificato 2026-06-02: USD 8.97 cad circa EUR 8 netto. Usare guaina termorestringente e strain relief: non lasciare i portafusibili liberi di vibrare.",
        "https://www.mouser.com/ProductDetail/Littelfuse/04980921GXM5?qs=aOs975IaWlkzQw1Up%2FmjHQ%3D%3D",
    ),
    (
        "Vishay Dale RHA050100R0FE02 - resistenza precarica chassis 100 ohm 50W",
        "DigiKey", 8.75, 1, "Sicurezza", "Fase 1",
        "Resistenza di precarica fissata al pannello metallico: carica lentamente la capacita DC-link distribuita dei 30 attuatori e del cablaggio prima che chiuda il contattore principale, riducendo scintilla e picco di corrente.",
        "SKU esatto RHA050100R0FE02, 100 ohm +/-1%, 50 W, automotive AEC-Q200, in stock verificato 2026-06-02 a USD 9.55 circa EUR 8.75. Corpo circa 50.0 x 21.4 x 16.0 mm, interassi montaggio circa 70.6 mm. A 54.6 V limita la corrente iniziale a 0.546 A e la potenza iniziale a 29.8 W. La capacita totale RobStride non e pubblicata: mantenere inizialmente 10 s e verificare la tensione bus prima della chiusura. Montare sul pannello, non sospesa.",
        "https://www.digikey.com/en/products/detail/vishay-dale/RHA050100R0FE02/15191925",
    ),
    (
        "CIT Relay A2K1CSQ24VDC1.6 - compact precharge relay, 24 V coil",
        "DigiKey", 6.10, 1, "Sicurezza", "Fase 1",
        "Precharge-branch relay: on enable it connects the 100 ohm resistor across the main contactor. After the measured bus reaches the required voltage, the LEV100 closes and bypasses the resistor.",
        "Exact A2K1CSQ24VDC1.6, DigiKey 2449-A2K1CSQ24VDC1.6-ND. Envelope 26.5 x 32.0 x 33.5 mm, 24 VDC coil. Sequencing decision 2026-07-17: the START/latch node energizes this precharge relay immediately while the H3YN-2 on-delay timer counts; the timer contact then closes the LEV100, which bypasses the resistor. The physical e-stop still directly interrupts all coil power. Thor only monitors RobStride VBUS telemetry and gates motor enable in software; it is not part of the safety chain.",
        "https://www.digikey.com/en/products/detail/cit-relay-and-switch/A2K1CSQ24VDC1-6/16687908",
    ),
    (
        "[DESIGN DELIVERABLE - NOT A PURCHASE] SEQ-PWR-01 safety-chain and precharge wiring drawing",
        "Project electrical documentation", 0, 1, "Sicurezza", "Fase 1",
        "Hardware sequencing selected 2026-07-17, no custom PCB: 24 V safety fuse -> latching e-stop NC -> START button with CIT seal-in latch relay -> precharge CIT relay + H3YN-2 on-delay timer -> timer contact -> LEV100 coil. Pressing START begins precharge and the delay; the timer closes the LEV100 on an already-charged bus; releasing the e-stop never restarts the bus, only START does. The deliverable is the released wiring drawing: terminals, wire gauges and colours, TVS placement at all three coils, mounting of latch relay, timer socket and button, and the frozen timer setting.",
        "Set the on-delay from the measured precharge time constant: watch RobStride VBUS telemetry converge on the bench, then set 4-5 tau with margin (initial guidance 10 s). Thor additionally refuses motor enable until telemetry VBUS matches battery voltage, but software is not part of the safety chain. The four purchasable parts are the separate rows below.",
        "https://www.digikey.it/it/products/detail/te-connectivity-aerospace-defense-and-marine/LEV100A5ANG/2362833",
    ),
    (
        "Schneider XB5AA31 - green 22 mm flush START pushbutton, momentary, 1NO",
        "Schneider / RS / distributors", 15.00, 1, "Sicurezza", "Fase 1",
        "Manual START command of the motor-bus power-up sequence, mounted on the outer shell next to the e-stop. Pressing it energizes the seal-in latch, which starts precharge and the on-delay timer. Panel hole diameter 22 mm; same XB5 family as the selected e-stop.",
        "Exact SKU XB5AA31, 1NO momentary. Price is an estimate: verify at order. Behind-panel depth is about 45 mm: verify the exact Schneider drawing before the CAD freeze. Releasing the e-stop must never restart the bus; only this button does, through the latch relay.",
        "https://www.se.com/ww/en/product/XB5AA31/",
    ),
    (
        "CIT Relay A2K1CSQ24VDC1.6 - START seal-in latch relay, 24 V coil",
        "DigiKey", 6.10, 1, "Sicurezza", "Fase 1",
        "Second unit of the same exact relay used for precharge, wired as a seal-in latch: START energizes the coil, one contact holds it in through the e-stop chain, and the latched node feeds the precharge relay coil and the timer. E-stop or loss of 24 V drops the latch, and the bus stays down until START is pressed again.",
        "Exact A2K1CSQ24VDC1.6, same SKU as the precharge relay row: one spare covers both functions. Envelope 26.5 x 32.0 x 33.5 mm, 24 VDC coil. Latched-node load is only the CIT coil, timer supply and LEV100 coil, well under one ampere; add the TVS at the coil.",
        "https://www.digikey.com/en/products/detail/cit-relay-and-switch/A2K1CSQ24VDC1-6/16687908",
    ),
    (
        "Omron H3YN-2 DC24 - miniature multifunction on-delay timer relay, 24 VDC",
        "DigiKey / Mouser / RS", 40.00, 1, "Sicurezza", "Fase 1",
        "Brand-name on-delay element of the precharge sequence: powered from the latched node, it closes the LEV100 coil circuit only after the set delay, so the main contactor always closes on a precharged bus. Miniature MY-relay footprint, plugs into the PYF08A-E socket below; body about 21.5 x 28 x 42 mm plus socket.",
        "Exact model H3YN-2 DC24, multifunction: use mode ON-DELAY, initial setting 10 s, then freeze the value from the measured precharge time constant (4-5 tau). A brand part is deliberate here: a timer that closes early silently defeats precharge and can weld the main contactor. Price is an estimate: verify at order, and verify the exact Omron drawing before the CAD freeze.",
        "https://www.digikey.com/en/products/result?keywords=H3YN-2%20DC24",
    ),
    (
        "Omron PYF08A-E - screw-terminal socket for H3YN-2 timer",
        "DigiKey / Mouser / RS", 5.00, 1, "Sicurezza", "Fase 1",
        "Screw-terminal socket for the plug-in H3YN-2 timer; DIN-rail or two-screw panel mounting. Timer plus socket stand about 80 mm tall: reserve about 25 x 35 x 80 mm standing, or lay the assembly flat.",
        "Exact model PYF08A-E. Price is an estimate: verify at order. Verify the exact Omron drawing before the CAD freeze; add strain relief on the control wires.",
        "https://www.digikey.com/en/products/result?keywords=PYF08A-E",
    ),
    (
        "[REMOVED qty0] Eaton 262684 ETR2-11 DIN precharge timer",
        "RS Italia", 124.23, 0, "Sicurezza", "Reference",
        "Removed from the robot. Thor performs the precharge sequence through the exact compact CIT relay; the e-stop remains hardwired and independent.",
        "Previous envelope 17.5 x 63 x 70 mm and 0.051 kg.",
        "https://it.rs-online.com/web/p/rele-temporizzati/2827115",
    ),
    (
        "[REMOVED qty0] Schneider XB5AG21 keyed motor-enable selector",
        "RS Italia", 38.23, 0, "Sicurezza", "Reference",
        "Removed from the compact robot. Motor re-enable requires software acknowledgement after the latching e-stop is manually reset; no separate heavy panel key switch.",
        "Retained only as a reference if a laboratory later requires keyed access control.",
        "https://it.rs-online.com/web/p/selettori/6096079",
    ),
    (
        "Littelfuse 1.5KE68CA - TVS bidirezionale 58.1V per bobine",
        "DigiKey", 0.65, 0, "Sicurezza", "Reference",
        "No longer used: the compact contactor and precharge relay now use 24 V coils and their suppression is integrated on the project carrier board with parts selected during schematic design.",
        "The old three external 68 V TVS devices belonged to the removed 48 V coil architecture.",
        "https://www.digikey.com/en/products/detail/littelfuse-inc/1-5KE68CA/3909",
    ),
    (
        "Littelfuse 1.5KE33CA - bidirectional TVS for LEV100 and CIT 24 V coils",
        "DigiKey", 0.65, 3, "Sicurezza", "Fase 1",
        "Transient suppressors mounted directly at the three 24 V coil terminals: LEV100 main contactor, CIT precharge relay and CIT START latch relay. They limit switch-off voltage spikes without the slow drop-out of a plain flyback diode, keeping e-stop opening fast.",
        "Exact series part 1.5KE33CA: bidirectional, 28.2 V standoff, clamping about 45.7 V. Qty 3, one per coil (LEV100, precharge CIT, latch CIT), mounted directly at the coil terminals as shown in the SEQ-PWR-01 wiring drawing. Replace the keyword link with the exact distributor link at order time; keep the TVS even if the delivered LEV100 variant documents internal coil suppression.",
        "https://www.digikey.com/en/products/result?keywords=1.5KE33CA",
    ),
    (
        "[MEASUREMENT FALLBACK qty0] ODrive PWR-CLMP1-ST Regen Clamp",
        "ODrive Europe", 89, 0, "Safety", "Reference",
        "Regenerative-energy clamp installed between the switched actuator source and the downstream motor PDU. With the required 70 x 70 mm heat spreader it is rated 80 A forward continuous / 120 A peak and 40 A brake continuous / 80 A peak. Board envelope 66 x 50 x 15.3 mm; CAD reserve 70 x 70 x 20 mm with plate.",
        "Exact SKU PWR-CLMP1-ST. It clamps the downstream bus when it rises about 2.35-2.50 V above the battery, so a full 54.6 V pack is held near 57.1 V, below the documented RobStride 60 V overvoltage fault. Maximum clamp voltage is 58 V, therefore do not use a charger above 54.6 V and validate transients with an oscilloscope. EU price checked 2026-07-12: EUR 89 excluding VAT.",
        "https://eu.odriverobotics.com/shop/odrive-regen-clamp",
    ),
    (
        "[MEASUREMENT FALLBACK qty0] ODrive 70 x 70 mm Regen Clamp heat spreader",
        "ODrive Europe", 12, 0, "Safety", "Reference",
        "Required thermal plate for the selected Regen Clamp. The clamp is only rated 20 A forward in free air but 80 A continuous on this plate, so the plate is not optional for the humanoid motor bus.",
        "Exact ODrive S1 heat-spreader kit, 70 x 70 mm with thermal pad and mounting screws. Clamp plus plate mass is 0.079 kg according to ODrive; mount the plate to a ventilated rigid panel.",
        "https://eu.odriverobotics.com/shop/heat-spreader-plate-for-odrive-s1",
    ),
    (
        "[MEASUREMENT FALLBACK qty0] ARCOL HS50 2R J brake resistor",
        "DigiKey", 10, 0, "Safety", "Reference",
        "Initial external brake resistor for the ODrive Regen Clamp. Overall mounting envelope 72.5 x 29.7 x 14.8 mm; resistor body 49.1 x 14.2 mm. Mount to an aluminum heat-spreading panel, never directly to PA-CF or near the battery.",
        "Exact SKU HS50 2R J, 2 ohm, 50 W. At about 57 V it can carry roughly 28.5 A / 1.6 kW only as a short pulse; 50 W is the continuous thermal rating with the specified heatsink. This is a bring-up choice, not a proven walking rating: log regenerated energy and upgrade the resistor before dynamic walking if measured average or pulse energy exceeds its datasheet limits.",
        "https://www.digikey.com/en/products/detail/ohmite/HS50-2R-J/5307846",
    ),
    (
        "[REJECTED qty0] RobStride Bleeder Module - 64 V activation in 48 V mode",
        "RobStride", 43, 0, "Sicurezza", "Reference",
        "Not selected. RobStride publishes 64 +/-0.5 V activation and 59 +/-0.5 V release in 48 V mode, while the actuator manual documents a 60 V motor overvoltage fault.",
        "The threshold is therefore too high for this 13S/RobStride bus. The 24 V mode threshold is too low. Keep this row only to prevent it being selected again without a revised manufacturer specification.",
        "https://aifitlab.com/products/robstride-bleeder-module",
    ),
    (
        "Eaton Bussmann 16220-2 - 2-pole distribution block, 175 A, 600 V AC/DC",
        "DigiKey", 65, 1, "Motor power", "Phase 1",
        "Exactly one downstream insulated block splits the switched actuator bus into left leg, right leg, waist/neck, left arm and right arm branches. It is not duplicated: the unswitched battery tap for the WEHO compute rail is a simple protected branch upstream of the LEV100.",
        "Exact SKU 16220-2: 76.2 x 50.8 x 25.4 mm, 0.151 kg, 175 A and 600 VDC. One block is sufficient; keep it covered and strain-relieved.",
        "https://www.digikey.com/en/products/detail/eaton-bussmann-electrical-division/16220-2/5449651",
    ),
    (
        "[MEASUREMENT-ONLY qty0] KEMET ALS80A123KE100 - external bulk capacitor 12,000 uF 100 V",
        "DigiKey", 29.40, 0, "Alim. motori", "Reference",
        "Not installed in the compact baseline. RobStride does not specify a central external bulk bank and every actuator has a local integrated driver/DC link. Add external capacitance only if oscilloscope measurements show unacceptable bus droop or high-frequency ripple after the battery, harness and Regen Clamp are installed.",
        "Exact SKU ALS80A123KE100 retained as a measured fallback: cylinder diameter 51 x maximum height 84 mm, 0.350 kg each, screw terminals, 100 V. The previous two-capacitor 24,000 uF bank occupied too much torso volume, added 0.700 kg and increased precharge energy without a measured requirement.",
        "https://www.digikey.com/en/products/detail/kemet/ALS80A123KE100/6872081",
    ),
    (
        "[MEASUREMENT-ONLY qty0] KEMET V4 - vertical 51 mm clamp for optional bulk capacitor",
        "Newark", 5.40, 0, "Alim. motori", "Reference",
        "Mechanical clamp required only if the optional ALS80 capacitor is reactivated after bus measurements.",
        "Exact KEMET V4 / Newark 09WX5727. Never install a large screw-terminal capacitor unsupported or with its safety vent covered.",
        "https://www.newark.com/kemet/v4/clamp-capacitor-51mm/dp/09WX5727",
    ),
    (
        "[DA PROGETTARE qty0] Cover isolante ventilata per PDU, fusibili e condensatori",
        "custom PA-CF / policarbonato", 0, 0, "Alim. motori", "Fase 1",
        "Non-conductive cover preventing accidental contact with the one distribution block, screw terminals, fuses and cable lugs of the 48 V panel.",
        "Obbligatorio prima del collaudo completo. Disegnarlo dopo il layout del pannello elettrico; lasciare accesso manutenzione e ventilazione al Regen Clamp e alla sua resistenza, che devono essere montati su alluminio.",
        "https://www.digikey.com/en/products/detail/eaton-bussmann-electrical-division/16220-2/5449651",
    ),
    (
        "Littelfuse BF1 142.5631.5702 - fusibile ramo gamba 70A 58VDC M5",
        "DigiKey", 4.30, 2, "Sicurezza", "Fase 1",
        "Due fusibili lenti, uno per gamba, sui rispettivi cavi positivi da 16 mm2. Isolano un corto su una gamba senza affidarsi soltanto al fusibile principale.",
        "SKU esatto 142.5631.5702, qty 2. BF1 M5 70 A, 58 VDC slow-blow, prezzo verificato 2026-06-02: USD 4.70 circa EUR 4.30 cad. Il rating e una baseline concreta da verificare con misura corrente e temperatura nelle prove progressive.",
        "https://www.digikey.com/en/products/detail/littelfuse-inc/142-5631-5702/2515910",
    ),
    (
        "Littelfuse BF1 142.5631.5402 - fusibile ramo vita-collo 40A 58VDC M5",
        "DigiKey", 4.30, 1, "Sicurezza", "Fase 3",
        "Fusibile lento del ramo vita-collo sul cavo positivo da 6 mm2.",
        "SKU esatto 142.5631.5402. BF1 M5 40 A, 58 VDC slow-blow, prezzo verificato 2026-06-02: USD 4.70 circa EUR 4.30. Verificare corrente e temperatura durante i test.",
        "https://www.digikey.com/en/products/detail/littelfuse-inc/142-5631-5402/2515916",
    ),
    (
        "Littelfuse BF1 142.5631.5302 - fusibile ramo braccio 30A 58VDC M5",
        "DigiKey", 4.30, 2, "Sicurezza", "Fase 3",
        "Due fusibili lenti, uno per braccio, sui rispettivi cavi positivi da 6 mm2.",
        "SKU esatto 142.5631.5302, qty 2. BF1 M5 30 A, 58 VDC slow-blow, prezzo verificato 2026-06-02: USD 4.70 circa EUR 4.30 cad. Verificare corrente e temperatura durante i test.",
        "https://www.digikey.com/en/products/detail/littelfuse-inc/142-5631-5302/2515908",
    ),
    (
        "Littelfuse 0FHM0002XP - portafusibile MINI inline waterproof comando safety",
        "DigiKey", 9.75, 1, "Sicurezza", "Fase 1",
        "Portafusibile inline dedicato al piccolo ramo 48 V di comando: e-stop, chiave enable, rele precarica, timer e bobina contattore. Il ramo parte dopo il fusibile principale e prima del contattore.",
        "SKU esatto 0FHM0002XP. Prezzo verificato 2026-06-02: USD 10.65 circa EUR 9.75. La serie Littelfuse MINI FHM e dichiarata 32-58 V inline waterproof; questo modello usa due pigtail GXL arancio 12 AWG lunghi circa 94 mm.",
        "https://www.digikey.com/en/products/detail/littelfuse-commercial-vehicle-products/0FHM0002XP/3427089",
    ),
    (
        "Littelfuse 0997002.WXN - fusibile MINI comando safety 2A 58VDC",
        "DigiKey", 0.95, 1, "Sicurezza", "Fase 1",
        "Fusibile dedicato del ramo e-stop, chiave, precarica, timer e bobine. Evita che un guasto nel comando dipenda dal BF1 principale o dal fusibile servizi Thor.",
        "SKU esatto 0997002.WXN, 2 A 58 VDC fast-blow, interrupting rating 1 kA. Prezzo verificato 2026-06-02: USD 1.04 circa EUR 0.95.",
        "https://www.digikey.com/en/products/detail/littelfuse-inc/0997002-WXN/701054",
    ),
    (
        "Littelfuse 0FHM0002XP - waterproof input fuse holder for 24 V converter",
        "DigiKey", 9.75, 1, "Safety", "Phase 1",
        "One input fuse holder for the selected WEHO WH-C482410 24 V converter. The compute rail remains upstream of the actuator contactor so Thor logs an e-stop event.",
        "Exact SKU 0FHM0002XP, 32-58 VDC waterproof holder with two 12 AWG pigtails about 94 mm long.",
        "https://www.digikey.com/en/products/detail/littelfuse-commercial-vehicle-products/0FHM0002XP/3427089",
    ),
    (
        "Littelfuse 0997015.WXN - 15 A 58 VDC MINI input fuse for 24 V converter",
        "DigiKey", 0.95, 1, "Safety", "Phase 1",
        "Input fuse for the selected 240 W converter. At 240 W, 42 V battery and 96% efficiency, worst-case continuous input is about 6.0 A.",
        "Exact SKU 0997015.WXN, 15 A, 58 VDC. The rating leaves converter inrush/startup margin; confirm measured inrush and cable temperature before final release.",
        "https://www.digikey.com/en/products/detail/littelfuse-inc/0997015-WXN/701060",
    ),
    (
        "Littelfuse 0FHM0002XP - 24 V output branch fuse holders for Thor, hands and USB hub",
        "DigiKey", 9.75, 3, "Safety", "Phase 1",
        "Three protected 24 V outputs from the selected WEHO rail: one for Thor, one for both RH56DFX hands and one for the powered USB hub. The baseline e-stop opens only the motor contactor; Thor remains alive to log it.",
        "Exact SKU 0FHM0002XP, qty 3. Use one 10 A fuse for Thor, one 15 A fuse for the hand branch and one 2 A fuse for the USB hub. Keep branch wiring short and mechanically supported.",
        "https://www.digikey.com/en/products/detail/littelfuse-commercial-vehicle-products/0FHM0002XP/3427089",
    ),
    (
        "Littelfuse 0997010.WXN - 10 A 58 VDC MINI fuse for Thor 24 V branch",
        "DigiKey", 0.95, 1, "Sicurezza", "Fase 1",
        "Dedicated output fuse between the 24 V rail and Thor Micro-Fit harness. Thor accepts up to 8 A at 9-28 V; use adequately sized conductors and keep the selected nvpmodel at or below 130 W.",
        "Exact SKU 0997010.WXN. Final fuse coordination must be confirmed from measured Thor boot and workload current.",
        "https://www.digikey.com/en/products/detail/littelfuse-inc/0997010-WXN/701059",
    ),
    (
        "Littelfuse 0997015.WXN - 15 A 58 VDC MINI fuse for both hands at 24 V",
        "DigiKey", 0.95, 1, "Safety", "Phase 3",
        "Output fuse feeding both RH56DFX hands from the shared WEHO 24 V rail. The RH56DFX manual lists 2 A maximum per hand at 24 V; 15 A leaves startup margin, but measure real simultaneous hand current before final fuse release.",
        "Exact SKU 0997015.WXN. Split and individually protect the hands later if measured fault-current behavior or the Inspire manual requires it.",
        "https://www.digikey.com/en/products/detail/littelfuse-inc/0997015-WXN/701060",
    ),
    (
        "Littelfuse 0997002.WXN - 2 A 58 VDC MINI fuse for powered USB hub at 24 V",
        "DigiKey", 0.95, 1, "Sicurezza", "Fase 2",
        "Output fuse for the Waveshare four-port industrial USB hub. Its maximum downstream USB budget is 25 W; 2 A at 24 V leaves conversion and startup margin.",
        "Exact SKU 0997002.WXN. Do not use this branch to power motors or hands.",
        "https://www.digikey.com/en/products/detail/littelfuse-inc/0997002-WXN/701054",
    ),

    (H, "4 - BATTERIA E ALIMENTAZIONE MOBILE - dopo il bench"),
    (
        "Bicycle Motor Works 48V 9Ah Molicel P45B compact battery, 13S2P, 45A/100A BMS",
        "Bicycle Motor Works", 358.70, 1, "Batterie", "Fase 2",
        "Selected compact G1-energy battery format: 13S2P with 26 Molicel P45B 21700 cells, 46.8 V nominal, 54.6 V full, 9 Ah and 421.2 Wh. Integrated balancing/protection BMS, 45 A continuous / 100 A maximum, XT90-S anti-spark discharge and XT60 charge lead. Published envelope 165.1 x 101.6 x 76.2 mm (6.5 x 4 x 3 in); published mass is under 5 lb, so CAD/BOM conservatively use 2.27 kg.",
        "Exact product SKU 10647581026769, USD 409.99 checked 2026-07-11 (EUR 358.70 net budget at 1 EUR = 1.1430 USD; shipping/import excluded). This is smaller than the G1 reference 182 x 120 x 80 mm in every oriented dimension and has exactly the same nominal energy. ORDER GATE: confirm shipment of lithium batteries to Italy, exact finished mass, whether 100 A is peak and for how long, BMS trip curve, short-circuit current, regen-charge current limit, charger and final connector lead lengths. CAD reserve: 170 x 106 x 81 mm plus 35-50 mm cable-bend space at the connector face.",
        "https://www.bicyclemotorworks.com/product-page/48v-94ah-molicel-p45b-lithium-ion-ebike-battery",
    ),
    (
        "[ORDER WITH BATTERY qty0] Supplier-matched 54.6V charger for P45B 13S pack",
        "Bicycle Motor Works / EU pack builder", 0, 0, "Batterie", "Fase 2",
        "Matched CC/CV charger for the selected 13S Li-ion pack, connected to its separate XT60 charge lead. Target charge voltage 54.6 V; charge current must respect the finished BMS and wiring specification.",
        "Do not choose a generic charger before the pack supplier confirms polarity, XT60 sex, recommended current and BMS charge limit. Order the charger and mating lead in the same quotation as the battery.",
        "https://www.bicyclemotorworks.com/product-page/48v-94ah-molicel-p45b-lithium-ion-ebike-battery",
    ),
    (
        "[ORDER WITH BATTERY qty0] AMASS XT90S anti-spark mating connector for pack discharge lead",
        "AMASS / battery supplier", 1.50, 0, "Batterie", "Fase 2",
        "Robot-side mate for the pack's XT90-S discharge connector, crimped/soldered onto the 25 mm2 trunk. This is the physical service disconnect: separate it only with the robot stopped and the LEV100 open.",
        "Confirm the delivered pack's connector gender and lead length before ordering; the anti-spark resistor sits in the male XT90-S half. Order one spare body and heat-shrink. The XT60 charge-side mate belongs to the matched charger quotation (see charger row).",
        "https://www.amass-china.com/",
    ),
    (
        "[TO SELECT qty0] Dual-source 48 V OR-ing stage - battery + grid simultaneously",
        "electrical engineer selection", 0, 0, "Power", "Fase 1",
        "User requirement 2026-07-19: bench operation with BOTH the RSP-3000-48 grid supply AND the battery connected at the same time (no battery drain at the desk, seamless battery takeover). The two sources must NEVER be hard-paralleled: the fixed 48 V supply would float-charge the 13S pack uncontrolled and either source can back-feed the other. An ideal-diode OR-ing stage (one branch per source, common output into the main fuse) is required for this mode.",
        "TO SELECT by the electrical engineer: 60 V-class ideal-diode controller/module per branch (LTC4357/LM5050-class), rated for the bench current (arm bench <= 20 A; the full robot would need a 70 A-class stage). INTERIM SAFE PROCEDURE until it exists: swap sources at the XT90-S connector - battery OR grid, never both plugged in. Bench-verify OR-ing behaviour and inrush before trusting it.",
        "https://www.digikey.com/en/products/result?keywords=ideal+diode+controller+65V",
    ),
    (
        "[EU FALLBACK qty0] Tõuksi Vabrik 48V 9Ah Molicel P45B 13S2P pack with 60A BMS",
        "Tõuksi Vabrik, Estonia", 341.00, 0, "Batterie", "Fase 2",
        "EU-built pack with the same core architecture: 13S2P, 26 Molicel P45B cells, 48 V class, 9 Ah / 421.2 Wh, 60 A BMS, 8 A charger specification and published mass 2.04 kg. Published price EUR 416 including VAT.",
        "Preferred procurement fallback for Italy if Bicycle Motor Works cannot ship. The builder does not publish final dimensions for this configuration: request a maximum finished envelope of 165 x 102 x 76 mm, XT90-S discharge, separate charge lead, BMS trip data and a drawing before ordering. Do not substitute their lower-current 20 A P50B pack.",
        "https://www.xn--tuksivabrik-ffb.ee/batteries/",
    ),
    (
        "[ALT SUPPLIER-CONFIRMATION qty0] Dan-Tech Energy 13S2P 48V 10Ah 60A softpack",
        "Dan-Tech Energy", 284.43, 0, "Batterie", "Fase 2",
        "Very compact EU alternative using Samsung INR21700-50S cells: 13S2P, 48 V nominal, 10 Ah / 480 Wh, 60 A continuous and 80 A peak. Size 280 x 35 x 130 mm, weight 2.2 kg, XT90 output; listed delivery is 7-9 working days.",
        "Price checked 2026-07-11: EUR 347 including 22% VAT. Do not select yet: the same product page says 'XT90 (No BMS)' while also advertising full BMS protection, CAN/RS485/UART and balancing. Ask Dan-Tech for a written quotation for the exact 60 A pack with an installed smart BMS, charger, connector pinout and final dimensions/mass.",
        "https://shop.danenergy.com/it/products/li-ion-battery-softpack-13s2p-48v-10ah-60a",
    ),
    (
        "[REMOVED qty0] Albright ED250B-1 manual battery disconnect",
        "Kit Elec Shop", 91, 0, "Safety", "Reference",
        "Sezionatore manuale di bordo sul positivo batteria per manutenzione e distacco fisico di emergenza. Non sostituisce il contattore automatico SW80B-10 ne il fungo XB5AS8442. Riserva CAD prudente 70 x 70 x 100 mm incluso spazio maniglia; massa BOM 0.468 kg.",
        "SKU esatto ED250B-1. Prezzo verificato 2026-06-02: EUR 91 netto / EUR 109.20 IVA inclusa. Rating 250 A continui, 96 VDC con blowouts. Usarlo come sezionatore a vuoto o emergenza, non come interruttore ordinario sotto carico; verificare la sagoma definitiva dal disegno Albright prima dei fori.",
        "https://www.kit-elec-shop.com/gb/power-relays/4519-ed250b-1-manual-single-pole-emergency-stop-96v-250a.html",
    ),
    (
        "[REF qty0] Unitree G1 original smart battery 13S 46.8V 9Ah",
        "Reichelt / Unitree", 680.33, 0, "Batterie", "Reference",
        "Exact G1 energy and packaging reference: 13S, 46.8 V nominal, 54.6 V full, 9 Ah, 421.2 Wh, 120 x 80 x 182 mm and 2.552 kg listed product weight.",
        "Not selected for the custom robot. Unitree documents load-detection protection: the battery cannot be switched on unless inserted into a G1 and switches off when removed. Reichelt price checked 2026-07-11: EUR 830 including German 19% VAT, in stock; the proprietary enable/load interface makes it a poor standalone source.",
        "https://www.reichelt.com/de/en/shop/product/unitree_g1_battery_9000_mah-421788",
    ),
    (
        "[ALT qty0] ENERprof TN13S5P-50-01 - Li-Ion battery 13S5P 48V 25Ah 100A BMS",
        "ENERprof", 1024.59, 0, "Batterie", "Fase 2",
        "Previous high-endurance baseline: 48 V nominal, 54.6 V full, 1200 Wh, integrated BMS, 100 A continuous and 180 A peak for up to 10 s. Size 280 x 80 x 130 mm, weight 5.2 kg.",
        "Deactivated because it carries 2.85 times the G1 energy and adds about 2.93 kg versus the selected compact P45B candidate. Keep only if measured runtime requires the larger pack. Confirm connectors and BMS behavior before ordering.",
        "https://enerprof.de/en/products/li-ion-akku-softpack-13s5p-48v-25ah-100a",
    ),
    (
        "[ALT qty0] Dan-Tech Energy Softpack 13S5P 48V 25Ah 100A - configurare Smart BMS + AS150U",
        "Dan-Tech Energy", 607.38, 0, "Batterie", "Fase 2",
        "Alternativa pronta in formato minimale termoretraibile: 65 celle cilindriche Samsung INR21700-50S, 1200 Wh, 100 A continui, 200 A picco, 280 x 80 x 130 mm, 5.2 kg.",
        "Pagina prodotto esatta. Prezzo visibile 2026-06-02: EUR 741 IVA inclusa per configurazione base XT90 senza BMS; prima dell'ordine chiedere il totale della variante Smart BMS + AS150U. Non attivare la riga senza BMS.",
        "https://shop.danenergy.com/he-eu/products/li-ion-battery-softpack-13s5p-48v-25ah-100a-1",
    ),
    (
        "[REMOVED qty0] MEAN WELL RSD-500C-24 enclosed DC/DC",
        "DigiKey", 192, 0, "Power", "Reference",
        "Single always-on 24 V rail for Thor, the powered USB hub and both hands. Output 24 V / 19.2 A / 461 W, efficiency about 93%. Envelope 237 x 100 x 41 mm, mass 1.45 kg. It replaces the previous 202 W + 300 W pair and saves about 0.86 kg plus one large enclosure.",
        "Exact SKU RSD-500C-24. Power budget: Thor capped at 130 W + USB hub maximum 25 W + two hands provisioned at 120 W each = 395 W, leaving about 66 W. This margin disappears if Thor is allowed to approach its 8 A input limit, so enforce a <=130 W nvpmodel. Converter is before the motor contactor; the separate Omron relay cuts hand power on e-stop.",
        "https://www.digikey.it/it/products/detail/mean-well-usa-inc/RSD-500C-24/12341362",
    ),
    (
        "WEHO WH-C482410 enclosed DC/DC converter, 48 V to 24 V, 10 A, 240 W",
        "WEHO (manufacturer direct)", 0, 1, "Power", "Phase 1",
        "Selected compact walking configuration: sealed non-isolated DC/DC from the 13S battery to a 24 V / 10 A / 240 W rail for Thor, the powered USB hub, low-power interfaces and, per user decision 2026-07-17, both RH56DFX hands. Envelope 74 x 74 x 32 mm; mass 0.300 kg; 160 mm flying leads.",
        "Exact model WH-C482410. Manufacturer specifies 30-60 V input, 24 V 10 A, 96% efficiency, natural cooling, 250 mVpp ripple with an external 22 uF low-ESR capacitor, 12 A over-current protection and 45 C rated temperature rise. User decision 2026-07-17: the first build powers Thor capped to 130 W plus hub/interfaces AND both RH56DFX hands from this single rail. At the published 2 A per hand the fully coincident worst case is about 241 W versus 240 W rated (12 A over-current protection), over budget only when everything peaks at once. Mitigations: lower the Thor nvpmodel during sustained two-hand work, stagger hand commands in software, and bench-log rail voltage and current with both hands gripping under full GPU load. If measured hand draw approaches Inspire's 5 A provisioning recommendation this converter is undersized: move to RSD-300C-24 or Cincon CHB350. It is a manufacturer-direct generic part: bench-test boot transients, sustained 130 W GPU load, temperature and EMI before locomotion. Quote price and Italy shipping before ordering.",
        "https://www.wehopower.com/product/48v-to-24v-10a-240w-dc-to-dc-converter",
    ),
    (
        "[TO DESIGN qty0] Low-ESR output capacitor >= 22 uF for the WEHO 24 V rail",
        "electrical engineer selection", 0, 0, "Power", "Fase 1",
        "The WEHO datasheet specifies its 250 mVpp output ripple only with an external low-ESR capacitor of at least 22 uF mounted at the converter output. Without it the rail feeding Thor, the hub and the hands is out of specification.",
        "Select a >= 35 V low-ESR polymer or electrolytic part and mount it immediately at the WEHO output terminals; confirm value and ESR from bench ripple measurement at full load. Release together with SEQ-PWR-01. Missing data: measured ripple, lead lengths and mounting.",
        "https://www.wehopower.com/product/48v-to-24v-10a-240w-dc-to-dc-converter",
    ),
    (
        "[ALT qty0] Cincon CHB350-48S24 isolated half-brick DC/DC, 24 V 350 W",
        "DigiKey / Mouser", 139.10, 0, "Power", "Reference",
        "Compact 350 W isolated module, 61.0 x 57.9 x 13.2 mm. It can support Thor plus later hands only with a correctly designed carrier board.",
        "Exact model CHB350-48S24. Not selected for the first walking build because it needs the project carrier below. Keep as a later compact 350 W upgrade after an electrical engineer releases its schematic, thermal design, creepage and connector pinout.",
        "https://www.digikey.com/en/products/detail/cincon-electronics-co-ltd/CHB350-48S24/9684431",
    ),
    (
        "[ALT qty0] UHG-PWR-001 open-source Cincon CHB350 power carrier assembly",
        "Project PCB / JLCPCB", 60, 0, "Power", "Reference",
        "Project-specific carrier required only by the alternate Cincon CHB350 module. CAD reserve 90 x 85 x 30 mm; preliminary mass 0.150 kg.",
        "Not an off-the-shelf product and not needed with the selected WEHO converter. Its exact components must be released by an electrical engineer; do not fabricate it from an incomplete BOM.",
        "https://www.cincon.com/productdownload/CHB350-series-application-note.pdf",
    ),
    (
        "[COMPACT QUOTE-ONLY qty0] Micropower 0060323IP isolated 48 V to 24 V DC/DC, 400 W IP67",
        "Micropower Group", 0, 0, "Batterie", "Reference",
        "Compact industrial alternative: 33-65 V input, 24.5 V output, 400 W, above 96% efficiency, isolated IP67 enclosure, 150 x 93 x 31 mm and 0.82 kg.",
        "Not selected: the current worst-case 24 V budget is 395 W, leaving only 5 W margin, and Micropower publishes no direct retail price or distributor stock. Reconsider only after measured hand/Thor consumption proves a lower continuous requirement and a written Italy quotation is acceptable.",
        "https://micropower-group.com/products/dcdc-converters-chargers/dcdc-converter-isolated/48-24-657",
    ),
    (
        "[REMOVED qty0] Omron G7L-1A-B-CB DC48 hand-power relay",
        "DigiKey", 18.50, 0, "Safety", "Reference",
        "Normally-open relay in the 24 V hand branch. Its 48 V coil is driven by the same hardwired e-stop/key-enable chain as the SW80 contactor, so both hands lose power on e-stop while Thor and the IMU remain alive.",
        "Exact SKU G7L-1A-B-CB DC48, SPST-NO chassis mount, 30 A contact rating, 48 VDC coil. Approximate envelope 52.5 x 33.5 x 55 mm and mass budget 0.09 kg. Verify the manufacturer's DC contact rating and provide a bidirectional coil suppressor before final wiring.",
        "https://www.digikey.com/en/products/detail/omron-electronics-inc-emc-div/G7L-1A-B-CB-DC48/369334",
    ),
    (
        "[ALT qty0] MEAN WELL SD-200C-24 dedicated Thor converter, 202 W",
        "DigiKey", 74.90, 0, "Batterie", "Reference",
        "Previous dedicated-Thor converter: 215 x 115 x 50 mm, 1.117 kg. Valid electrically but not selected because the shared RSD-500C-24 is lighter and removes one large box.",
        "Keep only if the final design returns to completely independent compute and hand converters.",
        "https://www.digikey.com/en/products/detail/mean-well-usa-inc/SD-200C-24/7706499",
    ),
    (
        "[ALT qty0] MEAN WELL RSD-300C-24 dedicated hand converter, 300 W",
        "DigiKey", 118.37, 0, "Batterie", "Reference",
        "Previous dedicated hand converter: 216 x 96.5 x 40 mm, 1.190 kg. Valid electrically but not selected in the shared 24 V architecture.",
        "Reactivate only if the hand load causes unacceptable disturbances on Thor's 24 V rail during measured tests.",
        "https://www.digikey.com/en/products/detail/mean-well-usa-inc/RSD-300C-24/7706243",
    ),

    (H, "5 - CONTROLLO, CAN E CABLAGGIO"),
    (
        "RobStride USB-to-CAN Adapter Type-C (debug ufficiale)",
        "Seeed", 15, 1, "Controllo/CAN", "Fase 1",
        "Configurazione ID, zero, test e aggiornamento firmware RobStride da PC.",
        "Prodotto esatto Seeed. Prezzo verificato 2026-06-02: USD 15. E uno strumento da banco, non il controller realtime del robot.",
        "https://www.seeedstudio.com/Robostride-CAN-USB-Driver-Board-p-6708.html",
    ),
    (
        "Waveshare USB TO 2CH RS485 isolated adapter for RH56DFX hands",
        "Waveshare", 15.74, 1, "Controllo/CAN", "Fase 3",
        "Two independent isolated USB-to-RS485 channels, one per hand, based on FT2232HL. Linux-compatible interface between Thor and the two RH56DFX hand buses. Board size 81.9 x 54 x 32 mm.",
        "Exact Waveshare SKU 27646. Keep left and right hands on separate channels during bring-up. RH56 defaults (manuals in hands/): RS485 115200 bps 8N1, register protocol with 0xEB 0x90 framing or MODBUS RTU, one HAND_ID per hand (assign left=1, right=2). Verify termination, grounding and protocol behavior before integrating the manipulation controller.",
        "https://www.waveshare.com/product/usb-to-2ch-rs485.htm",
    ),
    (
        "Waveshare USB3.2-Gen1-HUB-4U powered industrial 4-port USB 3.2 hub",
        "Waveshare / distributors", 15.74, 1, "Controllo/CAN", "Fase 2",
        "Compact powered hub for exactly three MKS CANable Pro interfaces plus the pelvis IMU. Input 7-36 VDC from the dedicated fused 24 V branch; four USB-A downstream ports and one USB-A upstream lead. Metal enclosure 86.0 x 47.8 x 27.6 mm; CAD mass budget 0.150 kg because the manufacturer does not publish mass.",
        "Exact Waveshare SKU 27837 / USB3.2-Gen1-HUB-4U, USD 17.99 checked 2026-07-12. Up to 5 A total at 5 V across four ports, Linux driver-free. D436 uses one Thor USB-A directly; this hub uses the second USB-A; the dual-RS485 adapter uses a native Thor USB-C port through the exact LINDY cable below.",
        "https://www.waveshare.com/usb3.2-gen1-hub-4u.htm",
    ),
    (
        "LINDY 36940 USB 2.0 Type-C to Type-B cable, 0.5 m, for dual RS485 adapter",
        "Conrad / Reichelt / LINDY", 4.79, 1, "Cablaggio", "Fase 3",
        "Direct data cable from one host-capable Thor USB-C port to the USB-B input of the Waveshare USB TO 2CH RS485 hand adapter. USB 2.0 is sufficient for the two RS485 channels; 0.5 m avoids a long cable coil inside the torso.",
        "Exact LINDY SKU 36940, USB-C male to USB-B male, 0.5 m. This direct connection is what allows the compact four-port hub to serve only the three CAN adapters and the pelvis IMU.",
        "https://www.conrad.it/it/p/lindy-cavo-usb-usb-2-0-spina-usb-c-spina-usb-b-0-50-m-nero-36940-2842258.html",
    ),
    (
        "[OPZIONE qty0] Computer low-level realtime separato per locomozione",
        "da selezionare", 0, 0, "Controllo/CAN", "Fase 1",
        "Supervisore deterministico tra policy e attuatori: legge IMU e feedback giunti, invia setpoint RobStride sui bus CAN, applica limiti, heartbeat, watchdog e transizione sicura in damping/stop. Non sostituisce i loop interni dei motori.",
        "Non comprare inizialmente: baseline prototipo Thor-only con processo realtime isolato, SocketCAN diretto e safety hardware indipendente. Valutare controller separato solo se i test mostrano jitter, saturazione/interfacce CAN insufficienti oppure se serve isolamento dai crash del software AI. Non scegliere Raspberry Pi, MCU o SBC prima di aver misurato frequenza loop, latenza e jitter.",
        "https://docs.nvidia.com/jetson/archives/r38.2/DeveloperGuide/SD/Kernel/RealTimeKernel.html",
    ),
    (
        "Seeed BCCA4011 - cavo XT30 (2+2) straight/right-angle F-F 300 mm per RS06 gambe",
        "Seeed", 7.40, 4, "Cablaggio", "Fase 1",
        "Cavo pronto potenza + CAN per i quattro RS06 delle gambe: due attuatori caviglia per gamba. Due XT30 (2+2)-F, uno diritto e uno a 90 gradi, fili 16AWG potenza e 26AWG segnali, guaina intrecciata.",
        "SKU esatto Seeed 100066605 / BCCA4011. Prezzo verificato 2026-06-02: USD 8 cad, in stock. Comprare prima un campione e validare orientamento, raggio di piega e lunghezza nel CAD. Sostituisce il vecchio BCCA4009, la cui pagina Seeed restituiva 404.",
        "https://www.seeedstudio.com/Power-Cable-XT30-2-2-Female-to-XT30-2-2-Female-300mm-p-6819.html",
    ),
    (
        "Seeed BCCA4011 - cavo XT30 (2+2) straight/right-angle F-F 300 mm per RS00/RS05/RS06 superiori",
        "Seeed", 7.40, 17, "Cablaggio", "Fase 3",
        "Cavo pronto potenza + CAN con un connettore diritto e uno a 90 gradi per i 17 attuatori integrati del corpo superiore e collo: RS06 x7, RS00 x8, RS05 x2.",
        "SKU esatto Seeed 100066605 / BCCA4011. Prezzo verificato 2026-06-02: USD 8 cad, in stock. Quantita coerente con la configurazione bilanciata; per tratte piu lunghe progettare estensioni con strain relief.",
        "https://www.seeedstudio.com/Power-Cable-XT30-2-2-Female-to-XT30-2-2-Female-300mm-p-6819.html",
    ),
    (
        "AMASS XT30UW-F.G.Y - connettore linea potenza RS03/RS04",
        "LCSC", 0.26, 10, "Cablaggio", "Fase 1",
        "Connettore XT30 femmina lato cavo per i nove motori RS03/RS04 selezionati: RS04 x6, RS03 hip yaw x2 e RS03 waist roll x1. Dieci pezzi includono un ricambio. Va saldato al fascio di potenza custom.",
        "SKU esatto LCSC C19268025 / AMASS XT30UW-F.G.Y. Prezzo verificato 2026-06-02: USD 0.2605 cad da 10 pezzi. Il manuale RS04 prescrive lato linea XT30UW-F.",
        "https://www.lcsc.com/product-detail/C19268025.html",
    ),
    (
        "JST GHR-02V-S - housing GH 1.25 mm 2 poli CAN per RS03/RS04",
        "Conrad / DigiKey", 0.05, 10, "Cablaggio", "Fase 1",
        "Housing lato cavo per CAN_H e CAN_L dei nove RS03/RS04 selezionati; dieci pezzi includono un ricambio. Si crimpa con due terminali JST MINI-SSHL-002T-P0.2 per connettore.",
        "SKU esatto JST GHR-02V-S. Prezzo verificato 2026-06-02: EUR 0.05 cad su Conrad. Il manuale RobStride indica genericamente GH1.25-T: prima dell'ordine completo comprare un campione e verificare fisicamente l'accoppiamento, perche esistono cloni non intercambiabili.",
        "https://www.conrad.com/en/p/jst-socket-housing-cable-gh-total-number-of-pins-2-contact-spacing-1-25-mm-ghr-02v-s-1-pc-s-1426140.html",
    ),
    (
        "JST MINI-SSHL-002T-P0.2 - contatto crimp per housing GHR-02V-S",
        "DigiKey", 0.21, 20, "Cablaggio", "Fase 1",
        "Terminale femmina da crimpare ai fili CAN_H e CAN_L e inserire negli housing JST GH lato cavo.",
        "SKU esatto MINI-SSHL-002T-P0.2. Prezzo verificato 2026-06-02: USD 0.242 cad da 10 pezzi, USD 0.2268 da 25. Prevedere scorta per prove di crimpatura.",
        "https://www.digikey.com/en/products/detail/jst-sales-america-inc/MINI-SSHL-002T-P0-2/807861",
    ),
    (
        "Belden 9841LSZH 00100 - bobina 50 m doppino CAN 120 ohm schermato",
        "Rapid Electronics", 425, 1, "Controllo/CAN", "Fase 1",
        "Cavo dati CAN schermato da tagliare per i fasci custom. Il doppino twistato porta CAN_H e CAN_L; la topologia deve restare a bus con derivazioni corte.",
        "Prodotto esatto Belden 9841LSZH 00100, bobina da 50 m. Prezzo verificato 2026-06-02: GBP 365.05 netto, circa EUR 425. La bobina include margine per prototipi e rifacimenti.",
        "https://www.rapidonline.com/belden-9841-lszh-00100-twisted-pair-shielded-cable-120-ohm-black-50m-02-2940",
    ),
    (
        "YAGEO MFR-25FBF52-120R - resistenza terminazione CAN 120 ohm 1%",
        "Mouser", 0.10, 10, "Controllo/CAN", "Fase 1",
        "Resistenza da montare protetta alle due estremita fisiche di ciascun bus CAN. Non metterla su ogni motore.",
        "SKU esatto Mouser 603-MFR-25FBF52-120R. Dieci pezzi per cinque bus: left leg, right leg, left arm, right arm, waist/neck. Thor CAN0/CAN1 may use the J47 selectable onboard terminators at the host end; fit exactly two 120 ohm terminations per physical bus and verify about 60 ohm across CAN_H/CAN_L with power off.",
        "https://www.mouser.com/ProductDetail/YAGEO/MFR-25FBF52-120R?qs=oAGoVhmvjhwezjKtxD8soA%3D%3D",
    ),
    (
        "[DA PROGETTARE qty0] Harness custom RS03/RS04: XT30UW-F + GH1.25 CAN + strain relief",
        "custom", 0, 0, "Cablaggio", "Fase 1",
        "Fascio da costruire dopo il CAD per RS04 gambe, RS03 hip yaw e RS03 waist roll. Usa i connettori acquistabili elencati sopra, cavo potenza dimensionato e doppino CAN.",
        "Non esiste un link a un harness completo RobStride per questo umanoide. Il manuale RS04 definisce i terminali lato cavo; K-Scale conferma che il cablaggio richiede progettazione e strain relief. Per i microcontatti JST GH commissionare preferibilmente crimpatura e collaudo a un cablatore: la pinza ufficiale JST YRS-1590 e elencata come opzione qty 0 ma costa molto. Questa riga resta qty 0 per evitare un costo fittizio.",
        "https://www.robstride.com/assets/product_manual_robStride04-37549d59.pdf",
    ),
    (
        "[DA PROGETTARE qty0] Cablaggio Thor J47 -> CANH/CANL per 2 bus nativi",
        "custom", 0, 0, "Controllo/CAN", "Fase 1",
        "Cablaggio dal connettore J47 del dev kit Thor ai due bus delle gambe. Il dev kit espone fisicamente CANH e CANL: non serve uno SN65HVD230 esterno.",
        "Il mating connector e il pinout del cablaggio vanno verificati sulla documentazione Thor e sul kit fisico prima dell'acquisto. Riga qty 0: non inventare uno SKU.",
        "https://docs.nvidia.com/jetson/archives/r38.2.1/DeveloperGuide/HR/ControllerAreaNetworkCan.html",
    ),
    (
        "Makerbase MKS CANable Pro CANable-MKS 1.0 (STM32F072) isolated USB-CAN adapter",
        "OpenELAB Germany", 15.95, 3, "Controllo/CAN", "Fase 3",
        "Three isolated USB-CAN interfaces supplement Thor's two native CAN controllers, giving five physical 1 Mbps buses. Use the STM32F072 CANable-MKS 1.0-compatible isolated model with candleLight/gs_usb and SocketCAN; do not silently substitute the STM32G431 MKS V2.0 because upstream candleLight firmware does not support it.",
        "Selected mapping at 250 Hz target refresh: native CAN0 left leg (6 motors), native CAN1 right leg (6), USB left arm (7), USB right arm (7), USB waist+neck (4). Conservative extended-frame command+feedback load is about 45-53% per busy bus. Keep RobStride active reporting disabled when each command already returns feedback. PCB reserve about 52 x 16 x 8 mm each plus USB/CAN connector bend space.",
        "https://openelab.de/products/mks-canable-pro-chip",
    ),
    (
        "Nautica Illiano CABATR25 - cavo batteria superflessibile rosso 25 mm2",
        "Nautica Illiano", 7.60, 2, "Cablaggio", "Fase 1",
        "Two metres of main positive cable for battery, main fuse, LEV100 contactor, compact power carrier and downstream distribution block.",
        "SKU esatto CABATR25, rosso 25 mm2, prezzo verificato 2026-06-02: EUR 7.60 netto al metro. Acquisto iniziale con margine; accorciare le tratte dopo il layout del pannello.",
        "https://www.nauticailliano.it/en/product/super-flexible-single-core-flame-retardant-electrical-cable-for-batteries_CABAT.html",
    ),
    (
        "Nautica Illiano CABATN25 - cavo batteria superflessibile nero 25 mm2",
        "Nautica Illiano", 7.30, 2, "Cablaggio", "Fase 1",
        "Due metri di cavo negativo principale da tagliare per sorgente e PDU.",
        "SKU esatto CABATN25, nero 25 mm2, prezzo verificato 2026-06-02: EUR 7.30 netto al metro. Acquisto iniziale con margine; accorciare le tratte dopo il layout del pannello.",
        "https://www.nauticailliano.it/en/product/super-flexible-single-core-flame-retardant-electrical-cable-for-batteries_CABAT.html",
    ),
    (
        "Nautica Illiano CABATR16 - cavo batteria superflessibile rosso 16 mm2",
        "Nautica Illiano", 4.55, 4, "Cablaggio", "Fase 1",
        "Quattro metri di cavo positivo per i due rami gamba protetti ciascuno da BF1 70 A.",
        "SKU esatto CABATR16, rosso 16 mm2, prezzo verificato 2026-06-02: EUR 4.55 netto al metro. Acquisto iniziale con margine per posa e strain relief.",
        "https://www.nauticailliano.it/en/product/super-flexible-single-core-flame-retardant-electrical-cable-for-batteries_CABAT.html",
    ),
    (
        "Nautica Illiano CABATN16 - cavo batteria superflessibile nero 16 mm2",
        "Nautica Illiano", 4.40, 4, "Cablaggio", "Fase 1",
        "Quattro metri di cavo negativo per i due rami gamba.",
        "SKU esatto CABATN16, nero 16 mm2, prezzo verificato 2026-06-02: EUR 4.40 netto al metro. Acquisto iniziale con margine per posa e strain relief.",
        "https://www.nauticailliano.it/en/product/super-flexible-single-core-flame-retardant-electrical-cable-for-batteries_CABAT.html",
    ),
    (
        "Nautica Illiano CABATR06 - cavo batteria superflessibile rosso 6 mm2",
        "Nautica Illiano", 1.75, 6, "Cablaggio", "Fase 3",
        "Sei metri di cavo positivo per vita-collo e due braccia, protetti rispettivamente da BF1 40 A e BF1 30 A.",
        "SKU esatto CABATR06, rosso 6 mm2, prezzo verificato 2026-06-02: EUR 1.75 netto al metro. Acquisto iniziale con margine per posa e strain relief.",
        "https://www.nauticailliano.it/en/product/super-flexible-single-core-flame-retardant-electrical-cable-for-batteries_CABAT.html",
    ),
    (
        "Nautica Illiano CABATN06 - cavo batteria superflessibile nero 6 mm2",
        "Nautica Illiano", 1.75, 6, "Cablaggio", "Fase 3",
        "Sei metri di cavo negativo per vita-collo e due braccia.",
        "SKU esatto CABATN06, nero 6 mm2, prezzo verificato 2026-06-02: EUR 1.75 netto al metro. Acquisto iniziale con margine per posa e strain relief.",
        "https://www.nauticailliano.it/en/product/super-flexible-single-core-flame-retardant-electrical-cable-for-batteries_CABAT.html",
    ),
    (
        "Klauke 704F5 - capocorda rame stagnato per cavo flessibile 25 mm2, foro M5",
        "Heamar", 1.75, 8, "Cablaggio", "Fase 1",
        "M5 lugs for the main BF1 fuse and LEV100 contactor, plus spares for crimp qualification.",
        "SKU esatto Klauke 704F5. Progettato per conduttori fini e superfini classe 5 e 6, rame EN13600 stagnato, vibration-tested DIN EN 61373 class 1B. Prezzo verificato 2026-06-02: GBP 1.46 netto cad circa EUR 1.75.",
        "https://www.heamar.co.uk/klauke-704f5-m5-25mm-f-series-copper-tubular-cable-lug.html",
    ),
    (
        "[REMOVED qty0] Klauke 704F10 lug for ED250B-1",
        "Heamar", 2.10, 0, "Wiring", "Reference",
        "Capicorda per i due terminali M10 del sezionatore ED250B-1 sul tronco positivo da 25 mm2. Due pezzi installati e due di scorta.",
        "SKU esatto Klauke 704F10. Progettato per conduttori fini e superfini classe 5 e 6, rame EN13600 stagnato. Prezzo verificato 2026-06-02: GBP 1.75 netto cad circa EUR 2.10.",
        "https://www.heamar.co.uk/klauke-704f10-m10-25mm-f-series-copper-tubular-cable-lug.html",
    ),
    (
        "[REMOVED qty0] Klauke 704F8 lug for SW80B-10",
        "Heamar", 2.00, 0, "Wiring", "Reference",
        "Cable lugs for the two M8 main terminals of the selected Albright SW80B-10 contactor. Two installed plus two spares for crimp qualification.",
        "Exact Klauke 704F8, 25 mm2, M8, for fine/superfine flexible copper conductors. This row replaces the two extra M10 lugs that belonged to the old SW200 contactor.",
        "https://www.heamar.co.uk/klauke-704f8-m8-25mm-f-series-copper-tubular-cable-lug.html",
    ),
    (
        "Klauke 703F5 - capocorda rame stagnato per cavo flessibile 16 mm2, foro M5",
        "Rapid Electronics", 0.85, 6, "Cablaggio", "Fase 1",
        "Capicorda per i due portafusibili BF1 dei rami gamba. Quattro pezzi installati e due di scorta.",
        "SKU esatto Klauke 703F5. Progettato per conduttori fini e superfini classe 5 e 6, rame stagnato. Prezzo verificato 2026-06-02: GBP 0.693 netto cad da 10 pezzi, BOM prudente EUR 0.85 cad.",
        "https://www.rapidonline.com/klauke-703f5-crimp-cable-lug-180-m5-16mm-1pc-04-6251",
    ),
    (
        "Klauke 101R5 - capocorda DIN rame stagnato 6 mm2, foro M5",
        "Heamar", 0.63, 8, "Cablaggio", "Fase 3",
        "Capicorda per i tre portafusibili BF1 dei rami vita-collo e braccia. Sei pezzi installati e due di scorta.",
        "SKU esatto Klauke 101R5 secondo DIN 46235, compatibile con conduttori classe 1, 2, 5 e 6. Prezzo verificato 2026-06-02: GBP 0.52 netto cad circa EUR 0.63.",
        "https://www.heamar.co.uk/klauke-101r5-m5-6mm-compression-cable-lug-copper-tin-plated.html",
    ),
    (
        "Klauke K05 - crimpatrice esagonale manuale per capicorda tubolari 6-50 mm2",
        "Toolnation", 293.48, 1, "Cablaggio", "Fase 1",
        "Utensile per crimpare correttamente i capicorda tubolari dei cavi 6, 16 e 25 mm2. Non usare una pinza generica per i collegamenti di potenza.",
        "SKU esatto Klauke K05 / 900086131. Prezzo verificato 2026-06-02: EUR 293.48 netto. Range 6-50 mm2, profilo esagonale. Se il laboratorio possiede gia una crimpatrice equivalente certificata per questi capicorda, scalare questa riga.",
        "https://www.toolnation.com/klauke-900086131-k-05-syncro-crimping-pliers-for-tubular-cable-lugs-and-connectors-standard-type-6-50-mm2.html",
    ),
    (
        "[OPZIONE qty0] JST YRS-1590 - pinza ufficiale per contatti GH SSHL-002T-P0.2",
        "DigiKey / JST", 1595, 0, "Cablaggio", "Fase 1",
        "Pinza ufficiale per crimpare i microcontatti JST GH dei fasci CAN RS03/RS04. Non serve se il cablatore fornisce i fasci gia assemblati e collaudati.",
        "SKU esatto JST YRS-1590. DigiKey indicava USD 1736.95 circa EUR 1595 il 2026-06-02. Per quindici motori e normalmente piu sensato commissionare i fasci a un cablatore e richiedere prova di trazione e test continuita, invece di comprare la pinza.",
        "https://media.digikey.com/pdf/Data%20Sheets/JST%20PDFs/YRS-1590_spec.pdf",
    ),
    (
        "Kit guaina termorestringente assortita",
        "Amazon", 20, 1, "Cablaggio", "Fase 1",
        "Isolamento di capicorda e giunzioni. Per i fasci lungo gli arti aggiungere guaina intrecciata della misura definita dal CAD.",
        "Link a prodotto specifico; prezzo BOM prudente da verificare al checkout.",
        "https://www.amazon.it/Guaine-Termorestringenti-Tubi-Termorestringente-fai/dp/B0778D22WM",
    ),
    (
        "Fascette + basette adesive",
        "Amazon", 10, 1, "Cablaggio", "Fase 1",
        "Fissaggio dei fasci cavi.",
        "Link a prodotto specifico; prezzo BOM prudente da verificare al checkout. Non usare basette adesive come unico ritegno sui segmenti mobili.",
        "https://www.amazon.it/Basette-Fascette-Cablaggio-Neutro-Trasparente-Confezione/dp/B09HQYXPHZ",
    ),
    (
        "[WORKSHOP qty0] Generic USB-C / USB-A debug cables",
        "existing lab stock", 0, 0, "Cablaggio", "Reference",
        "Not an onboard purchase row. Device-specific onboard cables are listed separately; use existing lab cables for RobStride and Thor bench debugging.",
        "Kept qty 0 because a generic cable listing is not an exact robot component and cable length/connector orientation depend on the bench layout.",
        "https://www.amazon.it/AmazonBasics-maschio-Type-C-USB-colore/dp/B01GGKYR2O",
    ),

    (H, "5A - MOTOR HARNESS / CAN BUS - manufacture after CAD cable take-off"),
    (
        "Seeed BCCA4011 XT30 (2+2) straight-to-right-angle 300 mm combined motor lead",
        "Seeed Studio", 7.40, 0, "Motor harness", "Reference",
        "Exact four-conductor ready-made motor lead: two 16 AWG silicone power conductors plus two 26 AWG signal conductors in a braided sleeve; 300 +/-15 mm overall. It is a motor lead, not a seven-motor CAN trunk. Use it only after confirming that the selected RobStride connector is the same XT30 (2+2) gender/keying.",
        "Exact manufacturer model BCCA4011 / SKU 100066605. The active RS06/RS00/RS05 cable rows above already use this part. This reference row exists so the electrical engineer sees its actual construction and does not confuse it with a CAN-only cable.",
        "https://www.seeedstudio.com/Power-Cable-XT30-2-2-Female-to-XT30-2-2-Female-300mm-p-6819.html",
    ),
    (
        "[DESIGN DELIVERABLE - NOT A PURCHASE] HAR-ARM-01 arm CAN/power trunk assembly, left and right",
        "Project harness", 0, 1, "Motor harness", "CAD take-off",
        "One routed trunk per arm: a protected power pair sized from the final branch current plus one 120-ohm twisted CAN pair. It must run shoulder-to-wrist with short serviceable motor drops, not seven long radial cables back to the CANable. Use the selected Belden 9841LSZH for CAN; select the exact flexible power-pair cable after CAD lengths, bend radius and current are frozen. With the hands active (2026-07-17) each arm trunk also carries the fused 24 V hand power pair and one RS485 twisted pair to the wrist; include both in the same take-off and drawing.",
        "Electrical-engineer handoff: make a drawing with connector IDs, wire gauge, wire colour, shield termination, branch length, bend radius, strain-relief point and pin-to-pin continuity for every motor. Measure centreline length in CAD, add 10% service slack plus connector bend allowance, then update quantity from metres rather than guessing today.",
        "https://www.belden.com/products/cable/electronic-cable/data-cable/9841",
    ),
    (
        "[DESIGN DELIVERABLE - NOT A PURCHASE] HAR-WST-01 waist/neck CAN/power trunk assembly",
        "Project harness", 0, 1, "Motor harness", "CAD take-off",
        "One short torso trunk serving waist yaw, waist roll and two neck motors. Electrical topology is a CAN backbone with short drops, while 48 V power branches separately from the fused waist/neck source.",
        "Do not use an unmeasured cable length. Route it in CAD with the full waist range, then specify each run centreline plus 10% service slack and a strain-relieved service loop outside rotating joints.",
        "https://www.belden.com/products/cable/electronic-cable/data-cable/9841",
    ),
    (
        "[DESIGN DELIVERABLE - NOT A PURCHASE] JBOX-CAN-01 inline CAN/power branch junction",
        "Project PCB / harness", 0, 1, "Motor harness", "CAD take-off",
        "Small inline branch assembly at each motor location: CAN-H/CAN-L through-trunk plus a short CAN drop to that motor; power is a separately rated branch. This creates a bus topology, not a star. Use one per motor only where the actuator has no CAN pass-through.",
        "Electrical-engineer specification: use a small 2-layer PCB or qualified crimp-splice assembly inside a mechanically supported enclosure. Keep the CAN stub from trunk to motor as short as possible, retain the CAN pair twist to the branch, do not terminate at intermediate motors, and use exactly two 120-ohm terminators per complete bus. Choose the enclosure, PCB terminals and splice SKU only after the actual motor connector and cable OD are verified; no safe universal part number exists.",
        "https://www.ti.com/lit/an/slla270/slla270.pdf",
    ),
    (
        "Seeed XT30 (2+2) Power Separation Board, SKU 100045091",
        "Seeed Studio", 5, 2, "Motor harness", "Fase 1",
        "Breaks one XT30 (2+2) connector into a standard XT30 power connector and a GH1.25 two-pin CAN connector. Activated qty 2 for the MS1 arm bench: junction points to feed/tap power and CAN when daisy-chaining the 7 arm actuators with BCCA4011 leads, and the place to fit the 120 ohm bus terminations.",
        "Not for RS03/RS04 (those use separate XT30 power and JST GH CAN connectors). Verify physical XT30 (2+2) mating with the arm RS06/RS00 before relying on it as the permanent junction; it remains the bench solution until the JBOX-CAN-01 junction is designed.",
        "https://www.seeedstudio.com/XT30-2-2-Power-Separation-Board-p-6707.html",
    ),
    (
        "[DESIGN DELIVERABLE - NOT A PURCHASE] HAR-RS03RS04-01 custom RS03/RS04 power + CAN harness set",
        "Project harness", 0, 1, "Motor harness", "CAD take-off",
        "Custom harness set for RS04 hip/knee motors and RS03 hip-yaw/waist-roll motors. Each motor receives a separate AMASS XT30UW-F.G.Y power drop and JST GHR-02V-S CAN drop from its relevant trunk; both connectors are already listed as purchasable BOM rows.",
        "Electrical-engineer handoff: create one table per motor with source fuse branch, motor CAN bus, CAN ID, XT30 pin polarity, GH pinout, centreline cable length, wire gauge, mating connector, crimp tool and continuity-test result. Do not use the Seeed XT30 (2+2) lead on these motors unless an actual physical test confirms compatibility.",
        "https://www.robstride.com/assets/product_manual_robStride04-37549d59.pdf",
    ),
    (
        "[DESIGN DELIVERABLE - NOT A PURCHASE] HAR-MECH-01 strain relief, grommet and harness mounting plan",
        "Project mechanical/electrical", 0, 1, "Motor harness", "CAD take-off",
        "Defines every fixed clamp, flexible service loop, grommet and moving-joint strain-relief point. Harnesses must never hang from JST/GH contacts or motor connectors.",
        "Electrical-engineer + CAD handoff: assign each clip/grommet an ID and add its exact final part number only after the printed-hole diameter, cable outside diameter, bend radius and joint travel are measured. Use the 3D-printed structure for clamp geometry, but use a soft grommet where the harness crosses an edge.",
        "https://www.igus.eu/info/chainflex-cable-strain-relief",
    ),
    (
        "[DESIGN DELIVERABLE - NOT A PURCHASE] HAR-MAP-01 final motor connector and CAN-ID map",
        "Project documentation", 0, 1, "Motor harness", "CAD take-off",
        "Mandatory manufacturing document mapping every motor to: physical location, RobStride model, CANable/Thor bus, CAN ID, two CAN termination endpoints, power-fuse branch, connector gender, pinout and harness drawing number.",
        "This is a deliverable, not a purchasable part. It prevents duplicate CAN IDs, reversed CAN-H/CAN-L, wrong motor polarity and accidental termination at intermediate motors. Freeze it before buying cut-to-length harnesses.",
        "https://www.ti.com/lit/an/slla270/slla270.pdf",
    ),

    (H, "6 - COMPUTE E SENSORI"),
    (
        "NVIDIA Jetson AGX Thor Developer Kit",
        "Seeed / Arrow - ALREADY OWNED (lab)", 0, 1, "Compute", "Fase 1",
        "Only onboard computer: runs perception, policy, state estimation and the 250 Hz RobStride target-refresh process. Official dev-kit envelope 243.19 x 112.40 x 56.88 mm; approximately 1.94 kg; T5000 module power configurable from 40 to 130 W.",
        "Use PREEMPT_RT, CPU affinity and separate high-priority control process. Thor does not run motor FOC: every RobStride contains its own driver and local current/position/velocity loops. Set a <=130 W nvpmodel; Thor + both hands at their documented 2 A maxima + USB interfaces fit within the 350 W shared 24 V budget, subject to transient bench testing. CAD reserve at least 255 x 125 x 72 mm including connector bends and airflow; do not bury the fan intake/exhaust. Native I/O used here: D436 on USB-A, four-port hub on the second USB-A, dual-RS485 on one USB-C and two leg buses on J47 CAN0/CAN1.",
        "https://www.seeedstudio.com/NVIDIA-Jetson-AGX-Thor-Developer-Kit-p-9965.html",
    ),
    (
        "Waveshare USB TO AUDIO USB sound card, SKU 18833",
        "Waveshare", 7.99, 1, "Audio", "Phase 2",
        "Simple first-iteration robot voice board: one USB 2.0 audio device with an onboard microphone, stereo codec and PH2.0 speaker connector. It records and plays audio under Linux without a special driver; the integrated BTL speaker driver is rated 2.6 W per channel into 4 ohm.",
        "Exact Waveshare part USB TO AUDIO / SKU 18833. Connect it to Thor USB-C #2 through the exact LINDY 41899 adapter below. This board gives basic listening/speaking, not far-field microphone-array quality or acoustic echo cancellation. Keep its microphone opening physically separated from the speaker grille; start with push-to-talk or half-duplex voice behavior.",
        "https://www.waveshare.com/product/usb-to-audio.htm",
    ),
    (
        "PUI Audio AS03604AR bare speaker, 36 mm, 4 ohm, 3 W",
        "Mouser / DigiKey / Farnell", 10.00, 1, "Audio", "Phase 2",
        "Exposed frame-mount speaker for robot speech: 36 mm diameter, 8.8 mm high, 4 ohm, 3 W rated, 88 dB sensitivity. Wire one channel from the Waveshare audio board PH2.0 speaker connector to its solder pads.",
        "Exact manufacturer model AS03604AR, Mouser 665-AS03604AR / DigiKey 668-AS03604AR-ND. The driver has no mounting holes: retain it with a printed circular pocket and separate printed ring or grille, not adhesive alone. Front grille: keep at least 1 mm clear of diaphragm; back: reserve a shallow 36-40 mm diameter cavity. Use thin flexible two-core speaker wire; verify PH2.0 connector gender on the delivered Waveshare board before crimping the harness.",
        "https://eu.mouser.com/ProductDetail/PUI-Audio/AS03604AR?qs=VVKQmw408U%2FBSl17uW5%2FPA%3D%3D",
    ),
    (
        "LINDY 41899 USB-C male to USB-A female adapter for audio board",
        "LINDY / EU distributors", 10.00, 1, "Audio", "Phase 2",
        "Connects the Waveshare USB-A audio-board cable to Thor's free normal USB-C #2 port. USB 2.0 audio is fully compatible with this USB 3.2 adapter.",
        "Exact LINDY 41899, USB-C male to USB-A female, 19 x 11 x 33 mm. Port map after this addition: USB-A #1 = D436; USB-A #2 = four-port hub for three CANable + IMU; USB-C #1 = dual RS485 hands; USB-C #2 = Waveshare audio. The debug USB-C remains reserved for recovery/flashing.",
        "https://www.lindy.eu/USB-3-2-Type-C-to-A-Adapter.htm?pi=41899&websale8=ld0101.ld021102",
    ),
    (
        "[DESIGN DELIVERABLE - NOT A PURCHASE] AUD-MNT-01 speaker pocket, retaining ring and grille",
        "Project mechanical/electrical", 0, 1, "Audio", "CAD take-off",
        "CAD deliverable for the PUI AS03604AR: printed 36.2 mm nominal circular pocket, removable retaining ring or back-clamp, front perforated grille and rear acoustic cavity. Do not put screw heads, grille or hard support against the moving diaphragm.",
        "Use the speaker's 36 mm outside diameter and 8.8 mm height as packaging dimensions; allow at least 1 mm front diaphragm clearance and a serviceable wire exit with strain relief. Final pocket clearance must be adjusted after measuring the physical speaker; do not use adhesive as the sole retention on a vibrating humanoid.",
        "https://puiaudio.com/product/s/AS03604AR",
    ),
    (
        "RealSense D436 depth camera with RGB and IMU",
        "RealSense Store", 309.71, 1, "Sensori", "Fase 1",
        "Compact head perception camera: global-shutter stereo depth, global-shutter RGB and IMU. Envelope 90 x 25 x 25 mm, mass 0.075 kg, USB-C 3.1, two M3 mounting points plus 1/4-20 thread.",
        "Exact SKU 99CWHP. Official price checked 2026-07-11: USD 354 before shipping/import, converted at 1 EUR = 1.1430 USD. The current official D400 CAD archive does not yet contain a D436 file; RealSense states the D436 shares the D435i external dimensions, so use the official D435i model only as a provisional envelope and verify the physical unit before final camera-bracket release.",
        "https://store.realsenseai.com/buy-intel-realsense-depth-camera-d436.html",
    ),
    (
        "Molex 0430250400 Micro-Fit 3.0 2x2 receptacle housing for Thor power",
        "DigiKey", 0.40, 1, "Cablaggio", "Fase 2",
        "Exact mating housing for the Thor developer-kit J74 2x2 Micro-Fit 3.0 power input. NVIDIA pinout looking into the board: pins 1-2 are 24 V power and pins 3-4 are ground.",
        "Use both positive and both ground circuits; do not bridge to a single undersized contact. The completed harness connects the dedicated 10 A 24 V fuse to Thor. Commission the crimping if the correct Molex tooling is not available.",
        "https://www.digikey.com/en/products/detail/molex/0430250400/252497",
    ),
    (
        "Molex 0430300040 Micro-Fit 3.0 female crimp contact, 18 AWG, for Thor power",
        "DigiKey", 0.20, 8, "Cablaggio", "Fase 2",
        "Four contacts are required for the Thor harness and four are spares for crimp qualification. Use 18 AWG flexible copper wire for each of the two 24 V and two ground circuits.",
        "Exact Molex 0430300040, female gold-plated contact for 18 AWG and 1.85 mm maximum insulation diameter. Perform pull, polarity and continuity tests before connecting Thor.",
        "https://www.digikey.com/en/products/detail/molex/0430300040/11503719",
    ),
    (
        "Phidgets MOT0110_0 PhidgetSpatial Precision 3/3/3 pelvis IMU",
        "Phidgets / EU distributors", 91.86, 1, "Sensori", "Fase 1",
        "Selected base IMU for the open-source build: factory-calibrated 3-axis accelerometer +/-16 g, gyroscope +/-2000 deg/s and magnetometer +/-8 G; synchronized timestamps, built-in IMU/AHRS algorithms, USB and Linux Phidget22 support, up to 1 kHz sampling. Enclosed dimensions 38.989 x 37.846 x 13.380 mm; CAD mass budget 0.030 kg.",
        "Exact SKU MOT0110_0, USD 105 with 978 units shown available on 2026-07-12. Mount rigidly on the pelvis/hip base below the articulated waist, with the axes documented, away from high-current cables and motors. For locomotion use gyro+accelerometer fusion; do not trust magnetic yaw near QDD motors without an in-situ calibration. Official mechanical drawing and 3D ZIP are on the product page.",
        "https://www.phidgets.com/?prodid=1205",
    ),
    (
        "Phidgets CBL4011_0 USB-A to Mini-B right-angle cable, 280 mm, for pelvis IMU",
        "Phidgets", 3.06, 1, "Cablaggio", "Fase 1",
        "Short official cable from the MOT0110_0 to the powered USB hub. Right-angle Mini-B reduces bend space at the pelvis IMU; route and clamp it so hip/waist motion cannot pull the connector.",
        "Exact SKU CBL4011_0, USB-A to Mini-B, 280 mm, USD 3.50. If the final hub-to-pelvis distance exceeds 280 mm, substitute the official 600 mm 3036_1 rather than adding an unrestrained extension.",
        "https://www.phidgets.com/?prodid=1248",
    ),
    (
        "[ALT qty0] Xsens MTi-3-DK IMU AHRS development kit",
        "DigiKey / Mouser", 480, 0, "Sensori", "Reference",
        "Higher-cost development alternative. The embedded MTi-3 module is excellent, but the DK is not selected because the Phidgets USB unit is cheaper, enclosed, mechanically documented and easier for universities and makers to reproduce.",
        "Reactivate only if MOT0110 bench testing shows unacceptable bias, vibration sensitivity or latency for the final gait.",
        "https://www.digikey.com/en/products/detail/xsens-technologies-bv/MTI-3-DK/5325385",
    ),
    (
        "[COMPACT THOR ALT qty0] Connect Tech AGX301 Gauntlet carrier for Jetson T5000",
        "Connect Tech", 0, 0, "Compute", "Reference",
        "Compact production-carrier alternative if the 243 mm developer kit cannot fit. Carrier board footprint 155 x 126 mm and supports T5000, USB 3.2, CAN 2.0b, serial, I2C and SPI.",
        "Do not activate until Connect Tech quotes a pre-integrated unit and supplies the complete module+carrier+thermal-solution envelope, mass, input-voltage range and cable set. A bare carrier is not a complete Thor computer and is less reproducible than the developer kit.",
        "https://connecttech.com/product/gauntlet-carrier-board-for-nvidia-jetson-thor/",
    ),

    (H, "7 - RIFERIMENTI DI PROGETTO - qty 0, non sono acquisti"),
    (
        "[REF qty0] Unitree G1 mode_11 URDF ufficiale",
        "Unitree Robotics", 0, 0, "Reference", "Reference",
        "Baseline geometrica e limiti per asse del G1 29 DOF corrente.",
        "Usare origini giunti e mesh come riferimento. L'URDF descrive la cinematica virtuale, non espone il CAD interno del leveraggio caviglia.",
        "https://github.com/unitreerobotics/unitree_ros/blob/master/robots/g1_description/g1_29dof_mode_11.urdf",
    ),
    (
        "[REF qty0] Unitree G1 description README ufficiale",
        "Unitree Robotics", 0, 0, "Reference", "Reference",
        "Elenco modelli G1 e stato aggiornato/deprecato.",
        "mode_11 e la baseline 29 DOF non bloccata e aggiornata.",
        "https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description",
    ),
    (
        "[REF qty0] Unitree G1-Comp pagina ufficiale - testa 2 DOF",
        "Unitree Robotics", 0, 0, "Reference", "Reference",
        "Riferimento ufficiale per aggiungere due motori collo.",
        "La pagina dichiara Head 2 degrees of freedom = 2, ma non pubblica la coppia dei due motori.",
        "https://www.unitree.com/robocup/",
    ),
    (
        "[REF qty0] Unitree G1-EDU Waist Fastener manuale ufficiale",
        "Unitree Robotics", 0, 0, "Reference", "Reference",
        "Riferimento ufficiale per la vita opzionale G1 EDU sbloccabile e bloccabile.",
        "Conferma la vita articolata opzionale; il dettaglio interno del leveraggio va ricostruito in CAD.",
        "https://marketing.unitree.com/article/en/G1/Lumbar_fasteners.html",
    ),
    (
        "[REF qty0] K-Scale K-Bot mechanical docs",
        "K-Scale", 0, 0, "Reference", "Reference",
        "Riferimento open hardware da tenere sotto osservazione.",
        "K-Bot usa solo RobStride ma ha 20 DOF e una caviglia diretta a un asse: non copiare la sua caviglia per la baseline G1.",
        "https://docs.kscale.dev/robots/k-bot/mechanical/",
    ),
    (
        "[REF qty0] K-Scale K-Bot CAD pubblico Onshape",
        "K-Scale", 0, 0, "Reference", "Reference",
        "CAD pubblico per studiare packaging, cablaggio e producibilita.",
        "",
        "https://cad.onshape.com/publications/e15cf8edefacbba3009917c0/",
    ),
]

# Keep every selected/alternative actuator row complete enough for CAD and torque review.
MOTOR_DETAIL_LABELS = (
    ("Dimensions:", "dimensions:", "Dimensioni:"),
    ("Weight:", "Peso:"),
    ("RobStride torque:", "Coppia RobStride:"),
    ("G1", "Riferimento G1"),
)
for item in rows:
    if item[0] == H or item[4] not in ("Motori", "Motori sup."):
        continue
    detail = f"{item[6]} {item[7]}"
    missing = ["/".join(labels) for labels in MOTOR_DETAIL_LABELS if not any(label in detail for label in labels)]
    if missing:
        raise ValueError(f"Dettagli motore mancanti per {item[0]}: {', '.join(missing)}")

# Massa unitaria stimata dei soli componenti che restano sul robot.
MASSA_UNIT = {
    "Cuscinetto 6002": 0.030,
    "Tirante go-kart": 0.120,
    "Rod-end alluminio M8": 0.090,
    "igus igubal KARM-08": 0.0062,
    "igus igubal KALM-08": 0.0062,
    "DIN 439 M8 thin jam nut": 0.002,
    "Perno cardano VITA": 0.040,
    "Puntoni VITA": 0.180,
    "Perno busto condiviso": 0.030,
    "Inserti filettati": 0.050,
    "Viti assortimento": 0.150,
    # CAD assembly masses include exactly the installed motor fasteners listed above.
    # The screw rows intentionally have no mass mapping, avoiding double-counting.
    "RobStride 04": 1.452625,
    "RobStride 03": 0.912625,
    "RobStride 06": 0.642930,
    "RobStride 02": 0.405,
    "RobStride 05": 0.211620,
    "RobStride 00": 0.323320,
    "Schneider XB5AA31": 0.030,
    "Schneider XB4": 0.070,
    "Schneider XB5": 0.059,
    "Omron H3YN": 0.050,
    "Omron PYF08A": 0.030,
    "Albright SW80": 0.400,
    "Albright ED250B": 0.468,
    "TE Connectivity KILOVAC LEV100A5ANG": 0.190,
    "Littelfuse BF1": 0.010,
    "Littelfuse 04980921": 0.030,
    "Vishay Dale RHA050": 0.050,
    "CIT Relay": 0.040,
    "Eaton 262684": 0.051,
    "Littelfuse 1.5KE": 0.001,
    "Littelfuse 0FHM": 0.030,
    "Littelfuse 0997": 0.001,
    "PWR-CLMP1-ST": 0.047,
    "ODrive 70 x 70": 0.032,
    "ARCOL HS50": 0.030,
    "Eaton Bussmann": 0.151,
    "KEMET ALS80": 0.350,
    "KEMET V4": 0.040,
    "Bicycle Motor Works 48V 9Ah Molicel P45B": 2.270,
    "ENERprof TN13S5P": 5.200,
    "MEAN WELL RSD-500C-24": 1.450,
    "Omron G7L": 0.090,
    "WEHO WH-C482410": 0.300,
    "Cincon CHB350-48S24": 0.10339,
    "UHG-PWR-001": 0.150,
    "Inspire Robots RH56DFX-2L": 0.540,
    "Inspire Robots RH56DFX-2R": 0.540,
    "RealSense D436": 0.075,
    "Waveshare USB TO 2CH RS485": 0.050,
    "Waveshare USB3.2-Gen1-HUB-4U": 0.150,
    "Seeed BCCA4011": 0.035,
    "AMASS XT30UW": 0.001,
    "JST GHR": 0.001,
    "JST MINI": 0.001,
    "Makerbase MKS CANable Pro": 0.030,
    "CABATR25": 0.290,
    "CABATN25": 0.290,
    "CABATR16": 0.190,
    "CABATN16": 0.190,
    "CABATR06": 0.085,
    "CABATN06": 0.085,
    "Capicorda": 0.050,
    "Guaina": 0.100,
    "Fascette": 0.050,
    "Cavi USB": 0.100,
    "NVIDIA Jetson": 1.940,
    "Waveshare USB TO AUDIO": 0.055,
    "PUI Audio AS03604AR": 0.0235,
    "LINDY 41899": 0.005,
    "Cavo Micro-fit": 0.100,
    "Phidgets MOT0110_0": 0.030,
    "Phidgets CBL4011_0": 0.020,
    "AliExpress adjustable aluminum M8 pushrod - 140 mm": 0.0238,
    "AliExpress adjustable aluminum M8 pushrod - 40 mm": 0.0068,
}

CAD_3D_BY_ITEM = {
    "Inspire Robots RH56DFX-2L dexterous hand, left, without wrist":
        "file:///Users/artes/Documents/artes/umanoide/cad_reference/RH56DFX-2L_reference.stl",
    "Inspire Robots RH56DFX-2R dexterous hand, right, without wrist":
        "file:///Users/artes/Documents/artes/umanoide/cad_reference/RH56DFX-2R_reference.stl",
    "RealSense D436 depth camera with RGB and IMU":
        "https://dev.realsenseai.com/docs/stereo-depth-camera-d400#cad-files",
    "Phidgets MOT0110_0 PhidgetSpatial Precision 3/3/3 pelvis IMU":
        "https://www.phidgets.com/productfiles/MOT0110/MOT0110_0/Images/MOT0110_0_3D.zip",
    "Bicycle Motor Works 48V 9Ah Molicel P45B compact battery, 13S2P, 45A/100A BMS":
        "https://www.bicyclemotorworks.com/product-page/48v-94ah-molicel-p45b-lithium-ion-ebike-battery",
}

CATEGORY_EN = {
    "Meccanica": "Mechanical",
    "Motori": "Motors",
    "Motori sup.": "Upper motors",
    "Alim. motori": "Motor power",
    "Sicurezza": "Safety",
    "Batterie": "Battery",
    "Controllo/CAN": "Control/CAN",
    "Cablaggio": "Wiring",
    "Sensori": "Sensors",
}

PHASE_EN = {
    "Fase 1": "Phase 1",
    "Fase 2": "Phase 2",
    "Fase 3": "Phase 3",
}

TEXT_REPLACEMENTS = [
    ("TOTALE", "TOTAL"),
    ("Fase", "Phase"),
    ("fase", "phase"),
    ("quantita", "quantity"),
    ("quantità", "quantity"),
    ("righe in grigio", "grey rows"),
    ("alternative o riferimenti", "alternatives or references"),
    ("non contano nei totali", "do not count in totals"),
    ("gia posseduto", "already owned"),
    ("già posseduto", "already owned"),
    ("parti acquistate a bordo", "purchased onboard parts"),
    ("di cui batteria", "of which battery"),
    ("umanoide completo", "complete humanoid"),
    ("gambe e bench", "legs and bench"),
    ("batteria e mobile", "battery and mobile setup"),
    ("corpo superiore", "upper body"),
    ("giunto caviglia", "ankle joint"),
    ("caviglia", "ankle"),
    ("Caviglia", "Ankle"),
    ("piede-stinco", "foot-shin"),
    ("puntoni", "pushrods"),
    ("Puntone", "Pushrod"),
    ("puntone", "pushrod"),
    ("perni", "pins"),
    ("Perni", "Pins"),
    ("perno", "pin"),
    ("Perno", "Pin"),
    ("vite a colletto", "shoulder screw"),
    ("Vite a colletto", "Shoulder screw"),
    ("Dado autobloccante", "Lock nut"),
    ("dado", "nut"),
    ("Dado", "Nut"),
    ("boccola", "bushing"),
    ("Boccola", "Bushing"),
    ("cuscinetto", "bearing"),
    ("Cuscinetto", "Bearing"),
    ("asse", "axis"),
    ("Assi", "Axes"),
    ("Asse", "Axis"),
    ("foro", "bore"),
    ("collo", "neck"),
    ("Collo", "Neck"),
    ("spalla", "shoulder"),
    ("Spalla", "Shoulder"),
    ("gomito", "elbow"),
    ("Gomito", "Elbow"),
    ("polso", "wrist"),
    ("Polso", "Wrist"),
    ("vita", "waist"),
    ("Vita", "Waist"),
    ("gamba", "leg"),
    ("Gamba", "Leg"),
    ("braccio", "arm"),
    ("Braccio", "Arm"),
    ("motori", "motors"),
    ("Motori", "Motors"),
    ("batteria", "battery"),
    ("Batteria", "Battery"),
    ("alimentazione", "power supply"),
    ("Alimentazione", "Power supply"),
    ("cablaggio", "wiring"),
    ("Cablaggio", "Wiring"),
    ("controllo", "control"),
    ("Controllo", "Control"),
    ("sicurezza", "safety"),
    ("Sicurezza", "Safety"),
    ("sensori", "sensors"),
    ("Sensori", "Sensors"),
    ("riferimenti", "references"),
    ("RIFERIMENTI", "REFERENCES"),
    ("scelto", "selected"),
    ("SCELTO", "SELECTED"),
    ("alternativa", "alternative"),
    ("Alternativa", "Alternative"),
    ("ARCHIVIATO", "ARCHIVED"),
    ("DA PROGETTARE", "TO DESIGN"),
    ("DA CONFERMARE", "TO CONFIRM"),
    ("DA DIMENSIONARE", "TO SIZE"),
    ("OPZIONALE", "OPTIONAL"),
    ("SECONDA SCELTA", "SECOND CHOICE"),
    ("Riferimento", "Reference"),
    ("riferimento", "reference"),
    ("Dimensioni", "Dimensions"),
    ("Peso", "Weight"),
    ("Coppia", "Torque"),
    ("nominali", "rated"),
    ("nominale", "rated"),
    ("picco", "peak"),
    ("Prezzo verificato", "Price checked"),
    ("Prodotto esatto", "Exact product"),
    ("SKU esatto", "Exact SKU"),
    ("Verificare", "Check"),
    ("verificare", "check"),
    ("Da validare", "To validate"),
    ("da validare", "to validate"),
    ("Qty attesa", "Expected qty"),
    ("qty attesa", "expected qty"),
    ("Niente", "No"),
    ("niente", "no"),
    ("pezzi", "pcs"),
    ("cad", "each"),
    ("circa", "about"),
    (" senza ", " without "),
    (" con ", " with "),
    (" e ", " and "),
]


def en_text(value):
    if not isinstance(value, str):
        return value
    out = value
    for src, dst in TEXT_REPLACEMENTS:
        if src.strip() and all(ch.isalpha() or ch in "àèéìòùÀÈÉÌÒÙ" for ch in src):
            pattern = rf"(?<![A-Za-zÀ-ÖØ-öø-ÿ]){re.escape(src)}(?![A-Za-zÀ-ÖØ-öø-ÿ])"
            out = re.sub(pattern, dst, out)
        else:
            out = out.replace(src, dst)
    return out


SECTION_OVERRIDES = {
    "3 - ALIMENTAZIONE E SICUREZZA BENCH - necessarie prima del primo power-up":
        "3 - BENCH POWER AND SAFETY - required before first motor power-up",
    "4 - BATTERIA E ALIMENTAZIONE MOBILE - dopo il bench":
        "4 - BATTERY AND MOBILE POWER - after bench validation",
    "5 - CONTROLLO, CAN E CABLAGGIO":
        "5 - CONTROL, CAN AND WIRING",
    "6 - COMPUTE E SENSORI":
        "6 - COMPUTE AND SENSORS",
    "7 - RIFERIMENTI DI PROGETTO - qty 0, non sono acquisti":
        "7 - DESIGN REFERENCES - qty 0, not purchases",
}

ROW_OVERRIDES = {
    "Perno asse ROLL vita = vite a colletto nera AliExpress Ø12 x M10, x1 (schema seriale)": (
        "Waist roll idle-side pin - black AliExpress shoulder screw Ø12 x M10, x1",
        "Direct serial waist roll support pin on the side opposite the motor. This is for the waist idle support, not for the ankle cardan.",
        "Uses the older shoulder-screw listing because this waist support is still Ø12/M10. Length and final retention remain CAD-dependent.",
    ),
    "Cuscinetto 6002-2RS foro 15 mm (15x32x9) - supporto asse roll vita": (
        "6002-2RS bearing, 15 mm bore (15x32x9) - waist roll support",
        "Two bearings for the idle side of the direct waist roll axis.",
        "Robust default with circlip or retaining plate. Validate bearing seats and preload/clearance in CAD.",
    ),
    "Inserti filettati a caldo ottone M3/M4/M5": (
        "Heat-set brass threaded inserts M3/M4/M5",
        "Reusable threads for PA-CF printed parts.",
        "",
    ),
    "Viti assortimento M3/M4/M5 + dadi + rondelle": (
        "M3/M4/M5 screw, nut and washer assortment",
        "General hardware for motors, brackets and covers.",
        "Check blind-hole depths on the motors before assembly and add any missing screw lengths separately.",
    ),
    "Loctite 243 frenafiletti medio": (
        "Loctite 243 medium-strength threadlocker",
        "Threadlocker for screws exposed to vibration.",
        "Use on selected shoulder-screw nuts and structural fasteners after confirming material compatibility.",
    ),
    "MEAN WELL RSP-3000-48 (48V 3000W)": (
        "MEAN WELL RSP-3000-48 bench supply (48 V, 3000 W)",
        "Bench AC/DC supply: 230 VAC input to 48 VDC motor bus, up to 62.5 A / 3000 W. Size 278 x 177.8 x 63.5 mm, weight about 4.0 kg. Not carried onboard.",
        "Exact SKU RSP-3000-48. Keep regenerative-energy tests progressive; this supply does not automatically absorb regen energy.",
    ),
    "Cavo rete Schuko -> estremita libera H07RN-F 3G1.5, 3 m, IP44": (
        "Schuko mains cable -> free ends, H07RN-F 3G1.5, 3 m, IP44",
        "Mains cable for the Mean Well AC input terminals: line, neutral and protective earth. Do not use an IEC C13 cord for this supply.",
        "Exact product link retained. Check plug, cable section and strain relief before first bench power-up.",
    ),
    "Schneider XB5AS8442 - fungo emergenza rosso 40 mm, twist release, 1NC": (
        "Schneider XB5AS8442 - red 40 mm emergency stop, twist release, 1NC",
        "Manual emergency-stop button. Its normally-closed contact drives the contactor coil circuit; pressing it drops the contactor and removes 48 V from the motors.",
        "The e-stop does not carry motor current directly.",
    ),
    "Albright SW200-20 - contattore DC principale con blowouts, bobina 48V": (
        "Albright SW200-20 - main DC contactor with blowouts, 48 V coil",
        "Main DC contactor on the motor-bus positive line. Opens the 48 V bus physically for both bench and battery operation.",
        "Use the blowout version for the full 54.6 V battery bus. Power terminals are M10; do not replace this with a small signal relay.",
    ),
    "Littelfuse 04980921GXM5 - portafusibile MIDI/BF1 inline 58VDC con cover": (
        "Littelfuse 04980921GXM5 - inline MIDI/BF1 fuse holder, 58 VDC, with cover",
        "Insulated inline fuse holder with cover and M5 hardware for the main fuse and branch fuses.",
        "Qty 6 covers: main fuse plus two legs, waist/neck, and two arms. Add heat-shrink and strain relief; do not leave fuse holders unsupported.",
    ),
    "Vishay Dale RHA050100R0FE02 - resistenza precarica chassis 100 ohm 50W": (
        "Vishay Dale RHA050100R0FE02 - chassis precharge resistor, 100 ohm, 50 W",
        "Panel-mounted precharge resistor. It charges the distributed DC-link capacitance of the 30 actuators and harness before the main contactor closes, reducing inrush current and arcing.",
        "At 54.6 V: initial current about 0.546 A and initial power about 29.8 W. Aggregate RobStride capacitance is unpublished, so retain the initial 10 s delay and verify bus voltage before contactor closure.",
    ),
    "CIT Relay A2K1CSQ48VDC1.6 - rele precarica SPDT bobina 48V": (
        "CIT Relay A2K1CSQ48VDC1.6 - precharge relay, SPDT, 48 V coil",
        "Relay for the precharge branch. It connects the 100 ohm resistor in parallel with the main contactor during bus precharge.",
        "Initial precharge current is only about 0.546 A. The main contactor bypasses this branch after the timer delay.",
    ),
    "Eaton 262684 ETR2-11 - temporizzatore ON-delay 24-48VDC per precarica": (
        "Eaton 262684 ETR2-11 - ON-delay timer, 24-48 VDC, for precharge",
        "DIN timer that enables the SW80B-10 contactor coil after the precharge delay.",
        "Set about 10 s initially and measure the bus before first motor enable.",
    ),
    "Schneider XB5AG21 - selettore a chiave enable motori, 2 posizioni mantenute, 1NO": (
        "Schneider XB5AG21 - keyed motor-enable selector, 2 maintained positions, 1NO",
        "Voluntary motor-enable command in series with the e-stop coil circuit. Releasing the e-stop alone must not automatically re-energize the motor bus.",
        "Use as an enable signal, not as a power switch.",
    ),
    "Littelfuse 1.5KE68CA - TVS bidirezionale 58.1V per bobine": (
        "[REMOVED qty0] Littelfuse 1.5KE68CA - bidirectional TVS, 58.1 V, for the removed 48 V coils",
        "Historical row: three 68 V TVS devices at the removed SW80 main-contactor, 48 V precharge-relay and Omron hand-relay coil terminals.",
        "Superseded 2026-07-17 by two 1.5KE33CA devices on the LEV100 and CIT 24 V coils; see the active row.",
    ),
    "ROBSTRIDE Bleeder Module 15-60V, 24/48V mode, 30A continui": (
        "RobStride Bleeder Module, 15-60 V, 24/48 V mode, 30 A continuous",
        "Regenerative clamp module. When motors brake and return energy to the bus, it dissipates energy to prevent bus overvoltage.",
        "Enough for progressive bring-up; dimension actual energy and dissipation before dynamic walking.",
    ),
    "Eaton Bussmann 16220-2 - blocco distribuzione 2 poli, 175A, 600V AC/DC": (
        "Eaton Bussmann 16220-2 - 2-pole distribution block, 175 A, 600 V AC/DC",
        "Main bus distribution block. Receives positive and negative from the contactor/supply and splits the bus into leg, waist/neck, arm and service branches.",
        "Positive motor branches use the BF1 inline fuse holders listed separately.",
    ),
    "KEMET ALS80A123KE100 - condensatore bulk 12000uF 100V a terminali vite": (
        "KEMET ALS80A123KE100 - bulk capacitor 12,000 uF, 100 V, screw terminals",
        "Local 48 V bus capacitance to reduce fast motor-bus transients. Two capacitors in parallel near the distribution block, with ring terminals and very short leads.",
        "100 V rating gives margin above 54.6 V full battery voltage and regen transients. No dedicated power PCB is required; mount with clamps and insulating covers.",
    ),
    "KEMET V4 - clamp verticale 51 mm per condensatore bulk": (
        "KEMET V4 - vertical 51 mm clamp for bulk capacitor",
        "Metal clamp for mounting each bulk capacitor to the electrical panel.",
        "Prevents capacitor mass and vibration from loading the screw terminals. Do not cover the safety vent.",
    ),
    "Littelfuse BF1 142.5631.5702 - fusibile ramo gamba 70A 58VDC M5": (
        "Littelfuse BF1 142.5631.5702 - leg branch fuse, 70 A, 58 VDC, M5",
        "Two slow-blow fuses, one per leg, on the positive 16 mm2 branch cables.",
        "Baseline rating to verify with measured current and cable temperature during progressive tests.",
    ),
    "Littelfuse BF1 142.5631.5402 - fusibile ramo vita-collo 40A 58VDC M5": (
        "Littelfuse BF1 142.5631.5402 - waist/neck branch fuse, 40 A, 58 VDC, M5",
        "Slow-blow fuse on the waist/neck positive 6 mm2 branch.",
        "Verify current and temperature during tests.",
    ),
    "Littelfuse BF1 142.5631.5302 - fusibile ramo braccio 30A 58VDC M5": (
        "Littelfuse BF1 142.5631.5302 - arm branch fuse, 30 A, 58 VDC, M5",
        "Two slow-blow fuses, one per arm, on the positive 6 mm2 branch cables.",
        "Verify current and temperature during tests.",
    ),
    "Littelfuse 0FHM0002XP - portafusibile MINI inline waterproof comando safety": (
        "Littelfuse 0FHM0002XP - waterproof inline MINI fuse holder for safety-control branch",
        "Inline fuse holder for the 24 V safety-control branch: the e-stop chain and the LEV100 contactor and CIT precharge-relay coil circuits.",
        "This branch taps the always-on WEHO 24 V rail: a converter failure de-energizes the contactor coil and drops the motor bus (fail-safe). The e-stop chain must remain hardwired and independent of Thor software.",
    ),
    "Littelfuse 0997002.WXN - fusibile MINI comando safety 2A 58VDC": (
        "Littelfuse 0997002.WXN - MINI fuse for safety-control branch, 2 A, 58 VDC",
        "Dedicated fuse for the e-stop chain and the LEV100/CIT 24 V coil circuits.",
        "Keeps a control fault from relying only on the main fuse.",
    ),
    "Littelfuse 0FHM0002XP - portafusibile MINI inline waterproof servizi": (
        "Littelfuse 0FHM0002XP - waterproof inline MINI fuse holder for service branch",
        "Inline fuse holder for the sixth PDU branch dedicated to services and the Thor DC/DC converter.",
        "Uses integrated 12 AWG pigtails and a 58 VDC MINI fuse.",
    ),
    "Littelfuse 0997010.WXN - fusibile MINI servizi 10A 58VDC": (
        "Littelfuse 0997010.WXN - MINI fuse for services, 10 A, 58 VDC",
        "Fuse for the services and Thor DC/DC branch.",
        "Fits the 0FHM0002XP inline MINI fuse holder.",
    ),
    "ENERprof TN13S5P-50-01 - batteria Li-Ion 13S5P 48V 25Ah BMS 100A": (
        "ENERprof TN13S5P-50-01 - Li-Ion battery 13S5P, 48 V, 25 Ah, 100 A BMS",
        "Mobile pack: 48 V nominal, 54.6 V full, 1200 Wh, integrated BMS, 100 A continuous and 180 A peak for up to 10 s. Size 280 x 80 x 130 mm, weight 5.2 kg.",
        "Exact SKU ENERprof 7713545 / TN13S5P-50-01. Confirm discharge connector and charge connector with ENERprof before ordering.",
    ),
    "Albright ED250B-1 - sezionatore manuale batteria 250A 96VDC con blowouts": (
        "Albright ED250B-1 - manual battery disconnect, 250 A, 96 VDC, with blowouts",
        "Onboard manual disconnect on the battery positive line for maintenance and physical emergency isolation. Conservative CAD reserve 70 x 70 x 100 mm including the handle; BOM mass 0.468 kg.",
        "Does not replace the SW80B-10 automatic contactor or the XB5AS8442 e-stop. Use as a no-load/service disconnect when possible and verify the final mounting outline from the Albright drawing.",
    ),
    "MEAN WELL SD-200C-24 DC/DC 48V -> 24V, 202W, per Thor": (
        "MEAN WELL SD-200C-24 DC/DC, 48 V -> 24 V, 202 W, for Thor",
        "Onboard isolated DC/DC converter: takes the 48 V battery bus and creates the 24 V rail for Thor, 8.4 A / 202 W. Size 215 x 115 x 50 mm, weight 1.117 kg.",
        "Thor accepts 9-28 V DC on Micro-Fit. Do not connect Thor directly to the 48 V bus.",
    ),
    "RobStride USB-to-CAN Adapter Type-C (debug ufficiale)": (
        "RobStride USB-to-CAN Adapter Type-C (official debug tool)",
        "Bench tool for RobStride ID setup, zeroing, test and firmware update from a PC.",
        "Not the realtime robot controller.",
    ),
    "Seeed BCCA4011 - cavo XT30 (2+2) straight/right-angle F-F 300 mm per RS06 gambe": (
        "Seeed BCCA4011 - XT30 (2+2) straight/right-angle F-F 300 mm cable for leg RS06 motors",
        "Ready-made power + CAN cable for the four leg RS06 ankle motors. Two XT30 (2+2)-F ends, one straight and one 90-degree, 16 AWG power and 26 AWG signal wires.",
        "Buy one sample first and validate connector orientation, bend radius and length in CAD.",
    ),
    "Seeed BCCA4011 - cavo XT30 (2+2) straight/right-angle F-F 300 mm per RS00/RS05/RS06 superiori": (
        "Seeed BCCA4011 - XT30 (2+2) straight/right-angle F-F 300 mm cable for upper-body RS00/RS05/RS06",
        "Ready-made power + CAN cable for the 17 integrated upper-body and neck actuators: RS06 x7, RS00 x8, RS05 x2.",
        "Quantity matches the balanced configuration. Longer runs need custom extensions with strain relief.",
    ),
    "AMASS XT30UW-F.G.Y - connettore linea potenza RS03/RS04": (
        "AMASS XT30UW-F.G.Y - power-line connector for RS03/RS04",
        "Cable-side XT30 female connector for the nine selected RS03/RS04 motors: RS04 x6, RS03 hip yaw x2, RS03 waist roll x1. Qty 10 includes one spare.",
        "The RS04 manual specifies XT30UW-F on the line side.",
    ),
    "JST GHR-02V-S - housing GH 1.25 mm 2 poli CAN per RS03/RS04": (
        "JST GHR-02V-S - GH 1.25 mm 2-pin CAN housing for RS03/RS04",
        "Cable-side housing for CAN_H and CAN_L on the nine selected RS03/RS04 motors. Qty 10 includes one spare.",
        "Use with two JST MINI-SSHL-002T-P0.2 crimp contacts per connector. Buy samples first and verify mating with the actual motor.",
    ),
    "JST MINI-SSHL-002T-P0.2 - contatto crimp per housing GHR-02V-S": (
        "JST MINI-SSHL-002T-P0.2 - crimp contact for GHR-02V-S housing",
        "Female crimp terminal for CAN_H/CAN_L wires inserted into the JST GH housing.",
        "Include spares for crimp trials.",
    ),
    "Belden 9841LSZH 00100 - bobina 50 m doppino CAN 120 ohm schermato": (
        "Belden 9841LSZH 00100 - 50 m spool, shielded 120 ohm CAN twisted pair",
        "Shielded CAN data cable to cut for custom harnesses. The twisted pair carries CAN_H and CAN_L; topology should remain bus-like with short stubs.",
        "50 m spool gives margin for prototypes and harness rebuilds.",
    ),
    "YAGEO MFR-25FBF52-120R - resistenza terminazione CAN 120 ohm 1%": (
        "YAGEO MFR-25FBF52-120R - CAN termination resistor, 120 ohm, 1%",
        "Termination resistor mounted at the two physical ends of each CAN bus. Do not place one on every motor.",
        "Qty 10 covers five buses. Fit exactly two per physical bus and verify about 60 ohm across CAN_H/CAN_L with power off.",
    ),
    "MKS Makerbase CANable Pro V2.0 USB-CAN isolato - bus aggiuntivi corpo superiore": (
        "MKS Makerbase CANable Pro V2.0 isolated USB-CAN - additional upper-body buses",
        "Four additional isolated USB-CAN interfaces beyond Thor's two native CAN buses. Supports candleLight/slcan; use candleLight + SocketCAN on Linux when possible.",
        "RobStride needs CAN 2.0B at 1 Mbps; CAN FD remains unused.",
    ),
    "Nautica Illiano CABATR25 - cavo batteria superflessibile rosso 25 mm2": (
        "Nautica Illiano CABATR25 - red super-flexible battery cable, 25 mm2",
        "Two meters of main positive cable for battery, main fuse, LEV100 contactor, compact power carrier and downstream distribution block.",
        "Initial purchase includes margin; shorten after electrical-panel layout.",
    ),
    "Nautica Illiano CABATN25 - cavo batteria superflessibile nero 25 mm2": (
        "Nautica Illiano CABATN25 - black super-flexible battery cable, 25 mm2",
        "Two meters of main negative cable to cut for source and PDU.",
        "Initial purchase includes margin; shorten after electrical-panel layout.",
    ),
    "Nautica Illiano CABATR16 - cavo batteria superflessibile rosso 16 mm2": (
        "Nautica Illiano CABATR16 - red super-flexible battery cable, 16 mm2",
        "Four meters of positive cable for the two leg branches, each protected by a 70 A BF1 fuse.",
        "Initial purchase includes margin for routing and strain relief.",
    ),
    "Nautica Illiano CABATN16 - cavo batteria superflessibile nero 16 mm2": (
        "Nautica Illiano CABATN16 - black super-flexible battery cable, 16 mm2",
        "Four meters of negative cable for the two leg branches.",
        "Initial purchase includes margin for routing and strain relief.",
    ),
    "Nautica Illiano CABATR06 - cavo batteria superflessibile rosso 6 mm2": (
        "Nautica Illiano CABATR06 - red super-flexible battery cable, 6 mm2",
        "Six meters of positive cable for waist/neck and the two arms, protected by 40 A and 30 A BF1 fuses.",
        "Initial purchase includes margin for routing and strain relief.",
    ),
    "Nautica Illiano CABATN06 - cavo batteria superflessibile nero 6 mm2": (
        "Nautica Illiano CABATN06 - black super-flexible battery cable, 6 mm2",
        "Six meters of negative cable for waist/neck and the two arms.",
        "Initial purchase includes margin for routing and strain relief.",
    ),
    "Klauke 704F5 - capocorda rame stagnato per cavo flessibile 25 mm2, foro M5": (
        "Klauke 704F5 - tinned copper lug for flexible 25 mm2 cable, M5 hole",
        "Cable lugs for both sides of the main BF1 fuse holder on the 25 mm2 trunk. Two installed plus two spares.",
        "Designed for fine and superfine conductors, class 5 and 6.",
    ),
    "Klauke 704F10 - capocorda rame stagnato per cavo flessibile 25 mm2, foro M10": (
        "Klauke 704F10 - tinned copper lug for flexible 25 mm2 cable, M10 hole",
        "Cable lugs for the two M10 terminals of ED250B-1 on the 25 mm2 positive trunk. Two installed plus two spares.",
        "Designed for fine and superfine conductors, class 5 and 6.",
    ),
    "Klauke 703F5 - capocorda rame stagnato per cavo flessibile 16 mm2, foro M5": (
        "Klauke 703F5 - tinned copper lug for flexible 16 mm2 cable, M5 hole",
        "Cable lugs for the two leg-branch BF1 fuse holders. Four installed plus two spares.",
        "Use a proper hex crimp, not generic pliers.",
    ),
    "Klauke 101R5 - capocorda DIN rame stagnato 6 mm2, foro M5": (
        "Klauke 101R5 - DIN tinned copper lug, 6 mm2, M5 hole",
        "Cable lugs for the waist/neck and arm branch fuse holders. Six installed plus two spares.",
        "Compatible with conductor classes 1, 2, 5 and 6.",
    ),
    "Klauke K05 - crimpatrice esagonale manuale per capicorda tubolari 6-50 mm2": (
        "Klauke K05 - manual hex crimper for tubular cable lugs, 6-50 mm2",
        "Tool for correctly crimping 6, 16 and 25 mm2 tubular cable lugs. Do not use generic pliers for power wiring.",
        "If the lab already has an equivalent certified crimper for these lugs, subtract this row.",
    ),
    "Kit guaina termorestringente assortita": (
        "Assorted heat-shrink tubing kit",
        "Insulation for cable lugs and joints. Add braided sleeve sizes after CAD/harness routing.",
        "Use only as insulation and bundling support, not as mechanical strain relief by itself.",
    ),
    "Fascette + basette adesive": (
        "Cable ties + adhesive mounts",
        "Cable-bundle fastening.",
        "Do not use adhesive mounts as the only retention on moving segments.",
    ),
    "Cavi USB-C / USB-A": (
        "USB-C / USB-A cables",
        "Debug cables for RobStride, Thor and IMU.",
        "",
    ),
    "NVIDIA Jetson AGX Thor Developer Kit": (
        "NVIDIA Jetson AGX Thor Developer Kit",
        "Only onboard computer for perception, policy, state estimation and the 250 Hz RobStride target-refresh process. Dev-kit size 243.19 x 112.40 x 56.88 mm, approximately 1.94 kg; T5000 module power configurable from 40 to 130 W.",
        "ALREADY OWNED (lab stock, 2026-07-19): counted at EUR 0; reference price EUR 3,300 net. Use PREEMPT_RT and a separate high-priority control process. CAD reserve at least 255 x 125 x 72 mm including cable bends and airflow. Enforce a <=130 W nvpmodel for the shared 24 V power budget.",
    ),
    "Xsens / Movella MTi-3-DK IMU AHRS pelvis": (
        "Xsens / Movella MTi-3-DK IMU AHRS for pelvis",
        "Pelvis IMU for orientation and acceleration feedback.",
        "",
    ),
    # English text for the remaining candidate / archived rows (added 2026-09-21)
    "[ALT qty0] SKF PCM 121420 E - boccola radente PTFE composito 12x14x20 mm": (
        "[ALT qty0] SKF PCM 121420 E - PTFE composite plain bushing 12x14x20 mm",
        "Real example of a thin plain bushing for a 12 mm diameter shaft of the foot-shin joint: bore 12 mm, outer diameter 14 mm, length 20 mm.",
        "Exact SKU SKF PCM121420E. Price verified 2026-06-02: EUR 2.13 net (excluding VAT). Candidate alternative for slow oscillation; qty 0 until CAD, loads, pin-seat fit and axial control are defined.",
    ),
    "[ALT qty0] SKF PCM 121425 E - boccola radente PTFE composito 12x14x25 mm": (
        "[ALT qty0] SKF PCM 121425 E - PTFE composite plain bushing 12x14x25 mm",
        "Longer real example from the same family: bore 12 mm, outer diameter 14 mm, length 25 mm. It shows that a single 25 mm long bushing is a standard component.",
        "Exact SKU SKF PCM121425E. Price verified 2026-06-02: EUR 2.94 net (excluding VAT). Qty 0: the greater length is not automatically better if it introduces misalignment or if the CAD does not provide a correct seat.",
    ),
    "[ALT qty0] igus iglidur Q2SM-1214-20 - boccola polimerica heavy-duty 12x14x20 mm": (
        "[ALT qty0] igus iglidur Q2SM-1214-20 - heavy-duty polymer bushing 12x14x20 mm",
        "Self-lubricating polymer example for a 12 mm diameter shaft: outer diameter 14 mm, length 20 mm. The Q2 material is developed for pivoting applications with dynamic loads, shocks and dirt.",
        "Exact SKU igus Q2SM-1214-20. Price verified 2026-06-02: PLN 25.89 net (excluding VAT), about EUR 6.15. Qty 0: verify surface pressure, wear, seat and tolerances with the igus tool before selection.",
    ),
    "[ALT qty0] igus iglidur Q2FM-1214-12 - boccola flangiata heavy-duty 12x14x12 mm": (
        "[ALT qty0] igus iglidur Q2FM-1214-12 - heavy-duty flanged bushing 12x14x12 mm",
        "Example of a flanged plain bushing for a 12 mm diameter pin: it guides the radial load and provides an integrated axial stop. Dimensions: bore 12 mm, outer diameter 14 mm, length 12 mm, flange diameter 20 mm, 1 mm thick.",
        "Exact SKU igus Q2FM-1214-12. Qty 0: useful if the CAD allows one bushing inserted from each side of the moving part; do not assume that two 12 mm pieces fit in the available width. Q2 is indicated by igus for high loads, shocks, dirt and heavily stressed pivoting applications.",
    ),
    "[ARCHIVIATO qty0] igus GTM-1224-015 - ralla separata (superata: assiale ora nella flangia) 12x24x1.5 mm": (
        "[ARCHIVED qty0] igus GTM-1224-015 - separate thrust washer (superseded: axial now in the flange) 12x24x1.5 mm",
        "Separate plain thrust washer to be located on the central moving part, between it and each outer lug, when the radial bushing has no flange. It puts the axial sliding on a surface designed for the purpose.",
        "Exact SKU igus GTM-1224-015: bore 12 mm, outer diameter 24 mm, thickness 1.5 mm. Price verified 2026-06-02: EUR 1.49 VAT included at Conrad. Qty 0: do not leave it loose between two PA-CF faces. Provide a locating seat and a fixed, smooth, replaceable metal counterface in the lug; define the axial play in the CAD.",
    ),
    "[ARCHIVIATO qty0] SKF HK 1216.2RS - rullini senza anello interno (superato) 12x18x16 mm": (
        "[ARCHIVED qty0] SKF HK 1216.2RS - needle roller bearing without inner ring (superseded) 12x18x16 mm",
        "Compact rolling alternative for the radial load only of the 12 mm diameter pin. It must be housed either in the moving part or in the pair of lugs, not in both at the same time. It has no inner ring to clamp between the shoulders of the lugs.",
        "Exact SKU SKF HK1216.2RS: bore 12 mm, outer diameter 18 mm, length 16 mm, seals on both sides. Availability verified 2026-06-02: 21 pieces, price on quotation. Qty 0: it requires the fixed pin to be a suitable hardened and ground inner raceway; do not automatically let the needle rollers run on a screw or a raw pin. It is not the first choice if you want to clamp shoulders against a true inner ring.",
    ),
    "[ARCHIVIATO qty0] SKF NKI 12/16 - rullini con anello interno (superato dal radente igus flangiato) 12x24x16 mm": (
        "[ARCHIVED qty0] SKF NKI 12/16 - needle roller bearing with inner ring (superseded by the flanged igus plain bushing) 12x24x16 mm",
        "First simple architecture to draw: bearing in the central moving part; separable inner ring clamped between the integrated shoulders of the two PA-CF lugs; outer ring seated in the moving centre. It carries the radial load without requiring metal caps in the lugs.",
        "Exact SKU SKF NKI 12/16: bore 12 mm, outer diameter 24 mm, width 16 mm, inner ring included. Price verified 2026-06-02: EUR 22.15 net (excluding VAT) at Klium. Qty 0 until the CAD. The shoulders must clamp the inner ring without crushing the central moving part; the running clearance is between the moving part and the lugs, not between the shoulders and the inner ring. NKI is not a thrust bearing: if tests show axial contact, add located igus thrust washers or a separate thrust bearing.",
    ),
    "[ARCHIVIATO qty0] SKF AXK 1226 - reggispinta (superato: assiale ora nella flangia) 12x26x2 mm": (
        "[ARCHIVED qty0] SKF AXK 1226 - thrust bearing (superseded: axial now in the flange) 12x26x2 mm",
        "Rolling alternative for axial load: one thrust bearing cage for each side of the central moving part if the CAD requires very low axial friction.",
        "Exact SKU SKF AXK 1226: bore 12 mm, outer diameter 26 mm, thickness 2 mm, dynamic load 9.15 kN and static 30 kN. Price verified 2026-06-02: EUR 4.10 net (excluding VAT) at RS Italia. Qty 0: between printed faces use two hardened AS 1226 washers for each cage.",
    ),
    "[ARCHIVIATO qty0] SKF AS 1226 - ralla temprata per AXK (superato) 12x26x1 mm": (
        "[ARCHIVED qty0] SKF AS 1226 - hardened thrust washer for AXK (superseded) 12x26x1 mm",
        "Hardened axial raceway for the AXK 1226 cage. With PA-CF or polymer faces do not use the printed part directly as the raceway for the needle rollers.",
        "Exact SKU SKF AS1226: bore 12 mm, outer diameter 26 mm, thickness 1 mm. Price and stock verified 2026-06-02: EUR 1.86 net (excluding VAT), 13 pieces available. Qty 0: a complete solution per side takes up 1 + 2 + 1 = 4 mm: AS 1226 + AXK 1226 + AS 1226.",
    ),
    "[ARCHIVIATO qty0] HGI PS 12x18x1 DIN 988 - rasamento di registro (superato) ": (
        "[ARCHIVED qty0] HGI PS 12x18x1 DIN 988 - adjustment shim washer (superseded) ",
        "Metal shim washer to calibrate the residual axial play after choosing the thrust surface. It does not replace an igus plain thrust washer or a hardened raceway for AXK.",
        "Exact SKU HGI12X18X1 / PS12X18X1: bore 12 mm, outer diameter 18 mm, thickness 1 mm. Price and stock verified 2026-06-02: EUR 0.48 net (excluding VAT), 57 pieces. Qty 0: choose the final combination only after measuring the assembly; DIN 988 also exists in finer thicknesses, for example 0.2 mm.",
    ),
    "[ALT DA DIMENSIONARE qty0] Inserti metallici flangiati fissi nelle orecchie caviglia - controfacce per asse diam. 12 mm": (
        "[ALT TO SIZE qty0] Fixed flanged metal inserts in the ankle lugs - counterfaces for 12 mm diam. axis",
        "Two cap-shaped inserts per axis, pressed or located in the outer PA-CF lugs: the inner bore guides or contains the fixed 12 mm diameter pin; the flange facing the central part provides a smooth metal axial counterface for the igus thrust washer.",
        "Alternative to keep documented if the printed central igus bushing is used or if the PA-CF shoulders prove insufficient. Preliminary CAD reference: left lug about 20 mm + central moving part with bushing about 20 mm + right lug about 20 mm = about 60 mm of structural bodies. The caps go on both lugs. Caution: a protruding flange increases the stack; recess it into the lug if you want to stay close to 60 mm. The cap bore guides the pin but does not automatically make it integral with the lugs: also design anti-rotation and axial retention.",
    ),
    "[OPZIONALE UPGRADE qty0] Elesa+Ganter GN.12825 / DIN 172-B12-20-A - controfaccia metallica nell'orecchia, foro 12 L20": (
        "[OPTIONAL UPGRADE qty0] Elesa+Ganter GN.12825 / DIN 172-B12-20-A - metal counterface in the lug, bore 12 L20",
        "Standard candidate for each lug if the central igus bushing is printed: hardened cap-type guide bush, inner bore 12 mm F7, outer diameter 18 mm n6, flange diameter 22 mm, body 20 mm long and flange 4 mm thick.",
        "Exact SKU Elesa+Ganter DIN172-B12-20-A / GN.12825, Verzolla code Y1137. Price and availability verified 2026-06-02: EUR 6.89 each, 5 available. Qty 0: expected quantity if used on both axes and on both ankles = 8 pieces, but activate only after CAD. To keep the about 60 mm reference, recess the 4 mm flange into the lug; also verify counterface, fit in the PA-CF and anti-rotation of the pin.",
    ),
    "[ALT FORNITORE qty0] Otto Ganter 172-B12-20-A - cappello metallico flangiato foro 12 mm, L20": (
        "[ALT SUPPLIER qty0] Otto Ganter 172-B12-20-A - flanged metal cap, bore 12 mm, L20",
        "Second supplier of the same standardized DIN 172-B12-20-A cap: steel, bore 12 mm, outer diameter 18 mm, flange 22 mm, body length 20 mm, flange 4 mm.",
        "Exact product Ganter 172-B12-20-A. Price and delivery verified 2026-06-02: EUR 5.26 net (excluding VAT) each, indicated as shippable in 2-3 working days; B2B sales. Qty 0: sourcing alternative for the same Verzolla component.",
    ),
    "[ALT EQUIVALENTE qty0] KIPP K1022.A1200X20 - cappello metallico flangiato DIN 172 foro 12 mm, L20": (
        "[ALT EQUIVALENT qty0] KIPP K1022.A1200X20 - flanged metal cap DIN 172, bore 12 mm, L20",
        "DIN 172 form A equivalent from another manufacturer for the same preliminary sizing: steel cap-type bush with inner bore 12 mm and length 20 mm.",
        "Exact SKU KIPP K1022.A1200X20. Price and availability verified 2026-06-02: EUR 4.50 net (excluding VAT) / EUR 5.36 VAT included each, indicated as available with delivery in 2-5 days. Qty 0: standard alternative to be verified dimensionally against the KIPP drawing before ordering.",
    ),
    "[SCHEDA qty0] Elesa+Ganter DIN 172-B12-20-A - pagina tecnica TME": (
        "[DATASHEET qty0] Elesa+Ganter DIN 172-B12-20-A - TME technical page",
        "Technical page of a further distributor for the same Ganter cap: hardened steel, inner bore 12 mm, outer diameter 18 mm, flange 22 mm, length 20 mm.",
        "Exact SKU TME DIN172-B12-20-A. Verified 2026-06-02: USD 10.04 about EUR 9.27 each, but TME stock indicated as zero. Keep it as a technical catalogue and as a backup for availability requests, not as an immediate primary supplier.",
    ),
    "[ALT CUSTOM qty0] Boccola radente stampata 3D in igus iglidur i150": (
        "[ALT CUSTOM qty0] 3D printed plain bushing in igus iglidur i150",
        "First printable custom test piece for the 12 mm diameter axes of the foot-shin joint. It allows iterating on length, flange and play. i150 is the easiest igus tribofilament to process.",
        "Material confirmed among those the user is purchasing for comparison. Qty 0: it is not yet the final choice. Validate surface pressure, wear, print orientation, pin finish, tolerances and play; do not automatically assume equivalence with injection-moulded Q2 or SKF metal/PTFE.",
    ),
    "[ALT CUSTOM qty0] Boccola radente stampata 3D in igus iglidur i190": (
        "[ALT CUSTOM qty0] 3D printed plain bushing in igus iglidur i190",
        "Second printable custom test piece for the 12 mm diameter axes of the foot-shin joint. i190 is the candidate to compare when greater mechanical strength and wear resistance are needed.",
        "Material confirmed among those the user is purchasing for comparison. Qty 0: it is not yet the final choice. The filament is sensitive to moisture: follow igus drying and instructions. Validate surface pressure, wear, orientation, tolerances and play.",
    ),
    "[SCELTO PRIMARIO qty0] Boccola STAMPATA multimateriale J260+PA-CF integrale (radiale + flangia assiale)": (
        "[CHOSEN PRIMARY qty0] PRINTED multi-material bushing J260+PA-CF, integral (radial + axial flange)",
        "PRIMARY approach chosen: print the bushing directly integral with the PA-CF moving part in multi-material FDM, with J260 both on the bore (radial) and on the flange faces (axial). No purchase if the print holds up.",
        "J260-PF filament already purchased by the user. igus indicates extrusion ~280 C, bed ~120 C, heated chamber preferable. To be validated specifically: adhesion at the J260/PA-CF interface (main risk of multi-material), print orientation for roundness and bore wear, finish and actual Ø (plan for reaming/calibration), surface pressure, play. Qty 0: handled by the filament, not by an SKU. i150 and i190 remain comparison test pieces.",
    ),
    "[SCELTO FALLBACK qty0] Boccola flangiata igus GFM-1214 (iglidur G) - radiale + assiale, acquistabile": (
        "[CHOSEN FALLBACK qty0] igus GFM-1214 flanged bushing (iglidur G) - radial + axial, purchasable",
        "PURCHASED version of the flanged bushing, fallback if the J260 multi-material print does not hold up: bore 12, outer diameter 14, flange about 20 x 1. The flange handles the axial load; two per axis, flanges facing outwards, press-fitted into the moving part. Drop-in with the same dimensions: Q2FM-1214 (heavy-duty shocks/dirt), JFM-1214 (low friction).",
        "SKU family GFM-1214 iglidur G. Length b1 from the CAD (e.g. two of 9-10 mm in a 20 mm moving part). Multiple suppliers verified 2026-06-03: igus direct, RS, Misumi IT, Minetti, F.lli Bono, Solema, ERIKS. Qty 0 until the CAD gives the lengths; expected quantity 8 (2 per axis x 4 axes) only if they are bought instead of printed. Retention: interference in the seat + stop flange; never cyanoacrylate, at most Loctite 603/638. Price to be verified once the length is configured.",
    ),
    "[CATALOGO qty0] RS PRO 822-9316 - vite a colletto M10, spallamento diam. 12 x 20 mm": (
        "[CATALOGUE qty0] RS PRO 822-9316 - shoulder screw M10, shoulder diam. 12 x 20 mm",
        "Purchasable industrial example of a shoulder screw: M10 thread, shoulder diameter 12 mm, shoulder length 20 mm, black steel class 12.9.",
        "Exact SKU RS PRO 822-9316. Price verified 2026-06-02: EUR 31.71 net (excluding VAT) per bag of four, EUR 7.928 each. Qty 0: the 20 mm length is only a catalogue reference; choose the actual length after the CAD.",
    ),
    "[ALT qty0] RS PRO 292-417 - vite a colletto ISO 7379 M10, gambo Ø12 x 60 mm (alternativa industriale al nero AliExpress)": (
        "[ALT qty0] RS PRO 292-417 - shoulder screw ISO 7379 M10, shank Ø12 x 60 mm (industrial alternative to the black AliExpress one)",
        "Reference close to the first ankle CAD stack of about 60 mm: ISO 7379 screw with a plain section of diameter 12 mm and length 60 mm, thread M10 x 16 mm, head diameter 18 x 8 mm, total length 84 mm.",
        "Exact SKU RS PRO 292-417, ISO 7379 shank Ø12 x 60, thread M10 x 16, head Ø18 x 8. Industrial ALTERNATIVE (the chosen pin is now the black AliExpress shoulder screw Ø12xM10): it acts as the raceway on which the igus slides and as retention. Made integral with the lugs by clamping (M10 nut + Loctite 243), not by press-fitting; shank-to-lug-bore fit sliding-locked (snug), no strong interference in the PA-CF. Expected qty 4 (one axis each) + spares, but qty 0 until the CAD fixes the shoulder length (~60-70). Alternative suppliers ISO 7379-12-M10: Rubix GN.35185, Elesa, Puntoviti, Berardi, KIPP.",
    ),
    "[CATALOGO qty0] Motedis 12h6 - albero precisione diam. 12 mm h6 temprato e rettificato": (
        "[CATALOGUE qty0] Motedis 12h6 - precision shaft diam. 12 mm h6 hardened and ground",
        "Alternative to be cut to size when a headless cylindrical fixed pin is needed. Also useful as a hardened and ground raceway if an HK bearing without inner ring is being considered.",
        "Motedis product code 12h6. Qty 0: price dependent on the cut length. Define length and retention; it does not automatically replace a shoulder screw.",
    ),
    "[CATALOGO qty0] Wurth DIN 6325 / ISO 8734 - spina cilindrica temprata diam. 12 mm": (
        "[CATALOGUE qty0] Wurth DIN 6325 / ISO 8734 - hardened dowel pin diam. 12 mm",
        "Industrial family of hardened and ground dowel pins, tolerance m6. The linked page shows the diameter 12 x 20 mm example; the family offers other lengths.",
        "Catalogue useful for the CAD, qty 0. Wurth notes that DIN 6325 has been replaced by DIN EN ISO 8734. Do not choose 20 mm just because it is the linked variant: first measure the width of the assembly and design the retention.",
    ),
    "[DA DIMENSIONARE qty0] Ritegni perni e supporti giunto caviglia": (
        "[TO SIZE qty0] Pin retainers and supports for the ankle joint",
        "Removable retainers for the two rotation axes of the foot-shin joint.",
        "Historical catalogue restored: assortment of internal/external circlips. Provide a printed shoulder or metal insert on one side and a removable retainer on the other. Do not assume M10 nut, circlip, collar or plate before the CAD: the system depends on the type of pin and on the actual seats.",
    ),
    "[SCELTO RITEGNO qty0] Dado autobloccante M10 NERO DIN 985 + Loctite 243 - serra assi Ø12xM10 (caviglia + cardano vita)": (
        "[CHOSEN RETENTION qty0] BLACK M10 self-locking nut DIN 985 + Loctite 243 - clamps the Ø12xM10 axes (ankle + waist gimbal)",
        "End retention of the Ø12xM10 rotation axes: the M10 nut clamps the thread of the shoulder screw and makes it integral with the lugs (4 ankle axes + 2 waist gimbal).",
        "CHOSEN retention: BLACK M10 self-locking nut (DIN 985, nylock set M3-M16) + Loctite 243. Expected qty 6 (4 ankle + 2 waist gimbal) + spares; qty 0 until CAD. Clean variant: thread into a metal insert embedded in the far lug, so that the clamping reacts on metal and does not compress the PA-CF.",
    ),
    "[CATALOGO qty0] RS PRO 797-6254 - rondella larga M10 DIN 9021 inox, 10.5x30x2.5 mm": (
        "[CATALOGUE qty0] RS PRO 797-6254 - large washer M10 DIN 9021 stainless steel, 10.5x30x2.5 mm",
        "Large washer to be evaluated under the head and nut of the shoulder screw to distribute the clamping over the outer surfaces of the PA-CF lugs.",
        "Exact SKU RS PRO 797-6254: bore 10.5 mm, outer diameter 30 mm, thickness 2.5 mm, stainless steel A2, DIN 9021. Qty 0: verify space and quantity after CAD. Do not use the clamping to significantly bend the lugs: the pin is held by axial clamping at nominal dimension.",
    ),
    "[CATALOGO qty0] Ruland MSP-12-F - collare split smontabile per perno diam. 12 mm": (
        "[CATALOGUE qty0] Ruland MSP-12-F - removable split collar for pin diam. 12 mm",
        "Two-piece collar for retention or axial adjustment of a 12 mm diameter cylindrical pin when the external space allows it. Outer diameter 28 mm, width 11 mm.",
        "Exact SKU MSP-12-F. Price verified 2026-06-02: USD 9.39 about EUR 8.65. Qty 0: it is a purchasable reference, not the automatic choice; verify external envelope and axial loads.",
    ),
    "[ALT qty0] Testa a snodo SKF SA8E M8 destra, foro 8 mm": (
        "[ALT qty0] SKF SA8E rod end M8 right-hand, bore 8 mm",
        "Precision upgrade, foot side.",
        "Use together with SAL8E and turnbuckle tube.",
    ),
    "[ALT qty0] Testa a snodo SKF SAL8E M8 sinistra, foro 8 mm": (
        "[ALT qty0] SKF SAL8E rod end M8 left-hand, bore 8 mm",
        "Precision upgrade, motor side.",
        "Opposite right/left threads for adjustment.",
    ),
    "[ALT qty0] Tubo tenditore M8 DIN 1478": (
        "[ALT qty0] Turnbuckle tube M8 DIN 1478",
        "Pushrod body for the SKF upgrade.",
        "",
    ),
    "[UPGRADE ROLL qty0] Spaziatori conici high-misalignment M8->M6 per rod-end metallici (coppia)": (
        "[ROLL UPGRADE qty0] Conical high-misalignment spacers M8->M6 for metal rod-ends (pair)",
        "Pair of stepped/conical bushings: cylindrical part in the Ø8 bore of the ball, narrow cone towards the lugs, M6 through bolt. The eye touches the cone instead of the wide face -> +8-12 degrees/side = ±20-25 total on standard metal rod-ends.",
        "Low-cost alternative to the igubal CL to raise the roll of the CURRENT rod-ends: the pin goes from Ø8 shoulder to plain M6 (less cross-section, ok for ~1-2 kN). Sources: Competition Supplies 'High misalignment spacer M8 to M6' (pair, metric), McGill Motorsport pack 6/10, Midwest Control HMBZC-M8-M6 (USA). On AliExpress search for 'heim joint misalignment spacer 8mm'. Qty at CAD.",
    ),
    "[CATALOGO qty0] Motedis W8H6 - albero precisione diam. 8 mm h6 temprato e rettificato": (
        "[CATALOGUE qty0] Motedis W8H6 - precision shaft diam. 8 mm h6 hardened and ground",
        "Alternative to be cut to size for the 8 mm diameter foot cross pin on which the two M8 rod ends are mounted.",
        "Motedis product code W8H6: CF53 steel hardened and ground, tolerance h6. Qty 0: price dependent on the cut length. Design spacers between the balls and lateral retainers.",
    ),
    "[CATALOGO qty0] Ruland MSP-8-F - collare split smontabile per perno diam. 8 mm": (
        "[CATALOGUE qty0] Ruland MSP-8-F - removable split collar for pin diam. 8 mm",
        "Two-piece collar to laterally retain the 8 mm diameter foot cross pin if the CAD leaves space. Outer diameter 18 mm, width 9 mm.",
        "Exact SKU MSP-8-F. Price verified 2026-06-02: USD 8.33 about EUR 7.67. Qty 0: evaluate two collars or another retainer only after the foot has been defined.",
    ),
    "ISO 4762 socket-head cap screw M3 x 15 mm, steel, full thread": (
        "ISO 4762 socket-head cap screw M3 x 15 mm, steel, full thread",
        "Installed motor fasteners: 8 per RS06 x 11 actuators plus 12 per RS00 x 8 actuators = 184 screws. Thread length is 15 mm; head excluded.",
        "Standard ISO 4762/DIN 912 size. Approximate single-screw mass 1.11 g. Mass is already included in the RS06 and RS00 CAD assembly masses; do not double-count it in the BOM mass total.",
    ),
    "ISO 4762 socket-head cap screw M4 x 15 mm, steel, full thread": (
        "ISO 4762 socket-head cap screw M4 x 15 mm, steel, full thread",
        "Installed motor fasteners: 6 per RS06 x 11 actuators + 15 per RS04 x 6 actuators + 15 per RS03 x 3 actuators = 201 screws. Thread length is 15 mm; head excluded.",
        "Standard ISO 4762/DIN 912 size. Approximate single-screw mass 2.175 g. Mass is already included in the RS06, RS04 and RS03 CAD assembly masses; do not double-count it in the BOM mass total.",
    ),
    "RobStride 03 - leg hip yaw (1/leg)": (
        "RobStride 03 - leg hip yaw (1/leg)",
        "Axis: hip yaw, 1 per leg. RobStride PDF 2025-06-26 dimensions: OD 98 mm, length 54.1 mm. Weight: 0.900 kg. RobStride torque: 20 Nm rated, 60 Nm peak.",
        "G1 mode_11 reference: hip yaw 88 Nm. This is a mostly vertical yaw axis, so gravity torque is near zero and demand is mainly dynamic. RS03 was chosen over RS06 because the estimated aggressive turn at ~45 kg mass was close to the RS06 36 Nm peak limit. WARNING 2026-07-18: the current CAD mounts RS06 (36 Nm peak) on hip yaw; this RS03 row remains the purchase intent until the SIM GATE decides: log of the hip-yaw torque while turning in Isaac at ~32+ kg; if it saturates at 36 Nm, RS03 is ordered and the CAD is adapted, otherwise this row is downgraded to RS06.",
    ),
    "[ALT qty0] RobStride 00 - spalla pitch/roll alleggerita (2/braccio)": (
        "[ALT qty0] RobStride 00 - lightweight shoulder pitch/roll (2/arm)",
        "Axes: lightweight shoulder pitch/roll alternative. Dimensions: 57 x 57 x 51 mm. Weight: 0.310 kg. RobStride torque: 5 Nm rated, 14 Nm peak.",
        "G1 mode_11 reference: shoulder pitch/roll 25 Nm per axis. It would save 1.244 kg over the four joints but cannot continuously hold the arm horizontal with a 1 kg payload. Kept only as an alternative for very light arms and intermittent poses.",
    ),
    "[SECONDA SCELTA qty0] RobStride 06 - spalla yaw piu robusta (1/braccio)": (
        "[SECOND CHOICE qty0] RobStride 06 - sturdier shoulder yaw (1/arm)",
        "Axis: shoulder yaw, sturdier alternative. Dimensions: 88 x 88 x 49 mm. Weight: 0.621 kg. RobStride torque: 11 Nm rated, 36 Nm peak.",
        "G1 mode_11 reference: shoulder yaw 25 Nm. Reactivate if the shoulder yaw has to move loads with the arm extended or more torque/stiffness is needed. Direct jump RS00->RS06 (RS02 eliminated: dominated, almost as big as RS06 but half the torque).",
    ),
    "[SECONDA SCELTA qty0] RobStride 06 - polso 3 assi (riserva piu robusta)": (
        "[SECOND CHOICE qty0] RobStride 06 - 3-axis wrist (sturdier reserve)",
        "Sturdy reserve for the 3 wrist axes. Dimensions: 88 x 88 x 49 mm. Weight: 0.621 kg. RobStride torque: 11 Nm rated, 36 Nm peak.",
        "G1 mode_11 reference: wrist roll 25 Nm, pitch/yaw 5 Nm. Reserve in case much more torque/stiffness were needed at the wrist; jump RS00->RS06 (RS02 eliminated because dominated). For the wrist RS00 remains amply sufficient.",
    ),
    "[SECONDA SCELTA qty0] RobStride 05 - polso pitch/yaw ultraleggero (2/braccio)": (
        "[SECOND CHOICE qty0] RobStride 05 - ultralight wrist pitch/yaw (2/arm)",
        "Axes: wrist pitch/yaw, ultralight alternative. Dimensions: 46 x 46 x 44 mm. Weight: 0.191 kg. RobStride torque: 1.6 Nm rated, 5.5 Nm peak.",
        "G1 mode_11 reference: wrist pitch/yaw 5 Nm: RS05 (5.5 peak) is the exact size and weighs only 0.191 kg. Alternative to the RS00 IF the payload in the hand stays <1 kg: rated 1.6 Nm limits the continuous load. Lighter but less sturdy and without the margin of the RS00.",
    ),
    "[DA PROGETTARE qty0] Cover isolante ventilata per PDU, fusibili e condensatori": (
        "[TO DESIGN qty0] Ventilated insulating cover for PDU, fuses and capacitors",
        "Non-conductive cover preventing accidental contact with the one distribution block, screw terminals, fuses and cable lugs of the 48 V panel.",
        "Mandatory before full commissioning tests. Design it after the electrical panel layout; leave maintenance access and ventilation for the Regen Clamp and its resistor, which must be mounted on aluminium.",
    ),
    "[REMOVED qty0] Albright ED250B-1 manual battery disconnect": (
        "[REMOVED qty0] Albright ED250B-1 manual battery disconnect",
        "On-board manual disconnect switch on the battery positive for maintenance and emergency physical disconnection. It does not replace the SW80B-10 automatic contactor nor the XB5AS8442 mushroom button. Prudent CAD reserve 70 x 70 x 100 mm including handle space; BOM mass 0.468 kg.",
        "Exact SKU ED250B-1. Price verified 2026-06-02: EUR 91 net (excluding VAT) / EUR 109.20 VAT included. Rating 250 A continuous, 96 VDC with blowouts. Use it as a no-load or emergency disconnect switch, not as an ordinary switch under load; verify the final outline from the Albright drawing before making the holes.",
    ),
    "[ALT qty0] Dan-Tech Energy Softpack 13S5P 48V 25Ah 100A - configurare Smart BMS + AS150U": (
        "[ALT qty0] Dan-Tech Energy Softpack 13S5P 48V 25Ah 100A - configure Smart BMS + AS150U",
        "Ready-made alternative in minimal heat-shrink format: 65 Samsung INR21700-50S cylindrical cells, 1200 Wh, 100 A continuous, 200 A peak, 280 x 80 x 130 mm, 5.2 kg.",
        "Exact product page. Price visible 2026-06-02: EUR 741 VAT included for the base XT90 configuration without BMS; before ordering ask for the total of the Smart BMS + AS150U variant. Do not activate the row without BMS.",
    ),
    "[OPZIONE qty0] Computer low-level realtime separato per locomozione": (
        "[OPTION qty0] Separate low-level realtime computer for locomotion",
        "Deterministic supervisor between policy and actuators: reads IMU and joint feedback, sends RobStride setpoints on the CAN buses, applies limits, heartbeat, watchdog and safe transition to damping/stop. It does not replace the internal loops of the motors.",
        "Do not buy initially: Thor-only prototype baseline with isolated realtime process, direct SocketCAN and independent hardware safety. Evaluate a separate controller only if tests show jitter, saturation/insufficient CAN interfaces, or if isolation from crashes of the AI software is needed. Do not choose Raspberry Pi, MCU or SBC before having measured loop frequency, latency and jitter.",
    ),
    "[DA PROGETTARE qty0] Harness custom RS03/RS04: XT30UW-F + GH1.25 CAN + strain relief": (
        "[TO DESIGN qty0] Custom harness RS03/RS04: XT30UW-F + GH1.25 CAN + strain relief",
        "Harness to be built after the CAD for RS04 legs, RS03 hip yaw and RS03 waist roll. It uses the purchasable connectors listed above, sized power cable and CAN twisted pair.",
        "There is no link to a complete RobStride harness for this humanoid. The RS04 manual defines the cable-side terminals; K-Scale confirms that the wiring requires design and strain relief. For the JST GH micro-contacts, preferably commission crimping and testing to a cable assembler: the official JST YRS-1590 crimping tool is listed as a qty 0 option but is very expensive. This row stays qty 0 to avoid a fictitious cost.",
    ),
    "[DA PROGETTARE qty0] Cablaggio Thor J47 -> CANH/CANL per 2 bus nativi": (
        "[TO DESIGN qty0] Wiring Thor J47 -> CANH/CANL for 2 native buses",
        "Wiring from the J47 connector of the Thor dev kit to the two leg buses. The dev kit physically exposes CANH and CANL: an external SN65HVD230 is not needed.",
        "The mating connector and the pinout of the wiring must be verified against the Thor documentation and the physical kit before purchase. Qty 0 row: do not invent an SKU.",
    ),
    "[REMOVED qty0] Klauke 704F10 lug for ED250B-1": (
        "[REMOVED qty0] Klauke 704F10 lug for ED250B-1",
        "Cable lugs for the two M10 terminals of the ED250B-1 disconnect switch on the 25 mm2 positive trunk. Two pieces installed and two spare.",
        "Exact SKU Klauke 704F10. Designed for fine and extra-fine stranded conductors class 5 and 6, tinned EN13600 copper. Price verified 2026-06-02: GBP 1.75 net (excluding VAT) each about EUR 2.10.",
    ),
    "[OPZIONE qty0] JST YRS-1590 - pinza ufficiale per contatti GH SSHL-002T-P0.2": (
        "[OPTION qty0] JST YRS-1590 - official crimping tool for GH contacts SSHL-002T-P0.2",
        "Official tool for crimping the JST GH micro-contacts of the RS03/RS04 CAN harnesses. Not needed if the cable assembler supplies the harnesses already assembled and tested.",
        "Exact SKU JST YRS-1590. DigiKey indicated USD 1736.95 about EUR 1595 on 2026-06-02. For fifteen motors it is normally more sensible to commission the harnesses to a cable assembler and request a pull test and continuity test, instead of buying the tool.",
    ),
    "[REF qty0] Unitree G1 mode_11 URDF ufficiale": (
        "[REF qty0] Unitree G1 mode_11 official URDF",
        "Geometric baseline and per-axis limits of the current G1 29 DOF.",
        "Use joint origins and meshes as a reference. The URDF describes the virtual kinematics; it does not expose the internal CAD of the ankle linkage.",
    ),
    "[REF qty0] Unitree G1 description README ufficiale": (
        "[REF qty0] Unitree G1 description official README",
        "List of G1 models and updated/deprecated status.",
        "mode_11 is the unlocked and up-to-date 29 DOF baseline.",
    ),
    "[REF qty0] Unitree G1-Comp pagina ufficiale - testa 2 DOF": (
        "[REF qty0] Unitree G1-Comp official page - 2 DOF head",
        "Official reference for adding two neck motors.",
        "The page states Head 2 degrees of freedom = 2, but does not publish the torque of the two motors.",
    ),
    "[REF qty0] Unitree G1-EDU Waist Fastener manuale ufficiale": (
        "[REF qty0] Unitree G1-EDU Waist Fastener official manual",
        "Official reference for the optional G1 EDU waist that can be unlocked and locked.",
        "Confirms the optional articulated waist; the internal detail of the linkage has to be reconstructed in CAD.",
    ),
    "[REF qty0] K-Scale K-Bot mechanical docs": (
        "[REF qty0] K-Scale K-Bot mechanical docs",
        "Open hardware reference to keep under observation.",
        "K-Bot uses only RobStride but has 20 DOF and a direct single-axis ankle: do not copy its ankle for the G1 baseline.",
    ),
}

hdr_font = Font(name="Arial", bold=True, color="FFFFFF")
hdr_fill = PatternFill("solid", fgColor="2F5496")
sec_fill = PatternFill("solid", fgColor="8EA9DB")
sec_font = Font(name="Arial", bold=True, color="1F2A44")
base_font = Font(name="Arial", size=10, color="000000")
alt_font = Font(name="Arial", size=10, color="A6A6A6")
link_font = Font(name="Arial", color="0563C1", underline="single", size=9)
thin = Side(style="thin", color="BBBBBB")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
eur = "\u20ac #,##0.00"

# apply ROW_SPLIT (resolving English overrides first so split names stay English)
_new_rows = []
for _it in rows:
    if _it[0] == H:
        _new_rows.append(_it); continue
    _hit = None
    for _k, _parts in ROW_SPLIT.items():
        if _k in _it[0]:
            _hit = _parts; break
    if _hit is None:
        _new_rows.append(_it); continue
    _nome, _desc, _note = _it[0], _it[6], _it[7]
    if _nome in ROW_OVERRIDES:
        _nome, _desc, _note = ROW_OVERRIDES[_nome]
    for _suf, _q, _ph in _hit:
        _new_rows.append((_nome + _suf, _it[1], _it[2], _q, _it[4], _ph, _desc, _note, _it[8]))
rows = _new_rows

ncol = len(headers)
r = 2
data_rows = []
selected_battery_row = None
for item in rows:
    if item[0] == H:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncol)
        cell = ws.cell(r, 1, en_text(SECTION_OVERRIDES.get(item[1], item[1])))
        cell.font = sec_font
        cell.fill = sec_fill
        cell.alignment = Alignment(horizontal="left", vertical="center")
        ws.row_dimensions[r].height = 20
        r += 1
        continue

    nome, fornitore, costo, unita, categoria, fase, descrizione, note, link = item
    if nome in ROW_OVERRIDES:
        nome, descrizione, note = ROW_OVERRIDES[nome]
    nome = en_text(nome)
    fornitore = en_text(fornitore)
    categoria = CATEGORY_EN.get(categoria, en_text(categoria))
    fase = PHASE_EN.get(fase, en_text(fase))
    descrizione = en_text(descrizione)
    note = en_text(note)
    fase = phase_to(nome, fase)
    # verified common-store equivalents (2026-07-19): REAL product swaps, item+link+supplier
    # together. Rows with no verified big-store equivalent keep their specialist source.
    if "704F5" in nome:
        fornitore = "Bürklin"
        link = "https://www.buerklin.com/en/p/klauke/cable-lugs/704f5/07F1391/"
        note += " [2026-07-19: same exact Klauke part at Bürklin, order no. 07F1391 (big distributor, user pref.); previous source Heamar.]"
    elif "703F5" in nome:
        fornitore = "Bürklin"
        link = "https://www.buerklin.com/en/p/klauke/cable-lugs/703f5/07F1381/"
        note += " [2026-07-19: same exact Klauke part at Bürklin, order no. 07F1381 (~EUR 0.84); previous source Rapid Electronics.]"
    elif "101R5" in nome:
        fornitore = "Bürklin"
        link = "https://www.buerklin.com/en/p/klauke/cable-lugs/101r5/07F2090/"
        note += " [2026-07-19: same exact Klauke part at Bürklin, order no. 07F2090; previous source Heamar.]"
    elif "XB5AS8442" in nome:
        nome = nome.replace("XB5AS8442", "XB4BS8442")
        fornitore = "RS Italia"
        link = "https://it.rs-online.com/web/p/pulsanti-di-arresto-di-emergenza/7951306"
        note += (" [2026-07-19: switched to the METAL-bezel Harmony XB4BS8442 stocked by RS Italia "
                 "(RS 7951306) - same Ø40 red turn-release mushroom, 1NC coding, XB4 = metal version of "
                 "the plastic XB5AS8442 (previous source Industry-Electronics). Verify the 1NC contact "
                 "block on the delivered unit and the RS price at order.]")
    elif "9841" in nome:
        nome = "Belden 9841NH - shielded 120 ohm CAN pair, LSZH, sold per metre (order 50 m)"
        fornitore = "Farnell Italia"
        link = "https://it.farnell.com/belden/9841nh/cable-rs-485-1-pair-lszh-per-m/dp/1891187"
        note += (" [2026-07-19 (user find): moved to Farnell 1891187 - Belden 9841NH is the "
                 "halogen-free LSZH version of the 9841 (RS-485 1 pair), sold PER METRE: order "
                 "50 m. The cost here is still the old Rapid 50 m spool price - verify the "
                 "Farnell per-metre total at order (likely lower) and confirm 120 ohm + shield "
                 "from the 9841NH datasheet. Previous source: Rapid Electronics spool.]")
    elif "Klauke K05" in nome:
        fornitore = "Bürklin"
        link = "https://www.buerklin.com/en/Crimping-pliers-for%C2%A0Tubular-cable-lugs-and-connectors-6-0-50-mm%C2%B2-Klauke-K05/p/05L2734"
        note += (" [2026-07-19: same exact Klauke K05 at Bürklin (order 05L2734) - consolidates "
                 "with the Bürklin lug order; also stocked by RS (stock 398-2270). Previous "
                 "source: Toolnation.]")
    elif "Schuko mains cable" in nome:
        fornitore = "Amazon (generic)"
        link = "https://www.amazon.it/s?k=cavo+H07RN-F+3G1.5+spina+schuko"
        note += (" [2026-07-19: commodity - any H07RN-F 3G1.5, >= 3 m, Schuko plug with free "
                 "ends (or cut a heavy-duty extension cord). Previous exact reference: Craft "
                 "Hardware EHK22146.]")
    elif fornitore == "Nautica Illiano":
        note += (" [Checked 2026-07-19: big-store equivalents exist (e.g. RS: Lapp H01N2-D 760-strand "
                 "super-flex) but only as 50-100 m reels; the per-metre specialist source is kept "
                 "deliberately per the supplier policy.]")
    elif fornitore == "Accu / Fabory":
        note += (" [Checked 2026-07-19: no verified big-store equivalent for the LEFT-hand thin nut; "
                 "specialist source kept. Before ordering, check whether the AliExpress pushrod kit "
                 "already includes RH+LH jam nuts.]")
    if nome.startswith("Bicycle Motor Works 48V 9Ah Molicel P45B"):
        selected_battery_row = r
    ws.cell(r, 1, nome)
    ws.cell(r, 2, fornitore)
    ws.cell(r, 3, costo)
    ws.cell(r, 4, IVA)
    ws.cell(r, 5, f"=C{r}*D{r}")
    ws.cell(r, 6, unita)
    ws.cell(r, 7, f"=(C{r}+E{r})*F{r}")
    ws.cell(r, 14, descrizione)
    ws.cell(r, 15, note)
    ws.cell(r, 16, categoria)
    link_cell = ws.cell(r, 17, link)
    link_cell.hyperlink = link
    ws.cell(r, 18, fase)
    cad_link = CAD_3D_BY_ITEM.get(nome)
    if cad_link:
        ws.cell(r, 20, cad_link).hyperlink = cad_link
    elif categoria in ("Motors", "Upper motors"):
        ws.cell(r, 20, link).hyperlink = link

    massa = next(
        (MASSA_UNIT[key] for key in sorted(MASSA_UNIT, key=len, reverse=True) if key in nome),
        None,
    )
    if massa is not None:
        ws.cell(r, 19, round(massa * unita, 3))

    is_active = isinstance(unita, (int, float)) and unita != 0
    row_font = base_font if is_active else alt_font
    for cc in range(1, ncol + 1):
        cell = ws.cell(r, cc)
        cell.border = border
        cell.alignment = Alignment(vertical="top", wrap_text=(cc in (1, 14, 15)))
        cell.font = row_font
    ws.cell(r, 3).number_format = eur
    ws.cell(r, 4).number_format = "0%"
    ws.cell(r, 5).number_format = eur
    ws.cell(r, 7).number_format = eur
    ws.cell(r, 17).font = link_font if is_active else alt_font
    if ws.cell(r, 20).value:
        ws.cell(r, 20).font = link_font if is_active else alt_font
    if massa is not None:
        ws.cell(r, 19).number_format = "0.000"
    if not is_active:
        ws.row_dimensions[r].hidden = True

    data_rows.append(r)
    r += 1

g_lo, g_hi = data_rows[0], data_rows[-1]
sumr = r + 1


def put(rr, label, formula):
    ws.cell(rr, 1, label).font = Font(name="Arial", bold=True)
    cell = ws.cell(rr, 7, formula)
    cell.number_format = eur
    cell.font = Font(name="Arial", bold=True)


def putmass(rr, label, formula):
    ws.cell(rr, 1, label).font = Font(name="Arial", bold=True)
    cell = ws.cell(rr, 19, formula)
    cell.number_format = "0.000"
    cell.font = Font(name="Arial", bold=True)


put(sumr, "TOTAL complete humanoid", f"=SUM(G{g_lo}:G{g_hi})")
put(sumr + 1, "Phase 1 - arm+hand teleop bench", f'=SUMIF(R{g_lo}:R{g_hi},"Phase 1",G{g_lo}:G{g_hi})')
put(sumr + 2, "  of which NVIDIA Thor (ALREADY OWNED - counted at 0)", f'=SUMIF(A{g_lo}:A{g_hi},"NVIDIA Jetson AGX Thor Developer Kit",G{g_lo}:G{g_hi})')
put(sumr + 3, "Phase 2 - legs and locomotion", f'=SUMIF(R{g_lo}:R{g_hi},"Phase 2",G{g_lo}:G{g_hi})')
put(sumr + 4, "Phase 3 - completion: left arm, waist, neck, mobile", f'=SUMIF(R{g_lo}:R{g_hi},"Phase 3",G{g_lo}:G{g_hi})')
putmass(sumr + 6, "PURCHASED ONBOARD MASS (NO PA-CF frame)", f"=SUM(S{g_lo}:S{g_hi})")
if selected_battery_row is None:
    raise ValueError("Selected battery row not found")
putmass(sumr + 7, "  of which battery", f"=S{selected_battery_row}")

ws.conditional_formatting.add(
    f"A{g_lo}:{get_column_letter(ncol)}{g_hi}",
    FormulaRule(
        formula=[f"AND(ISNUMBER($F{g_lo}),$F{g_lo}=0)"],
        font=Font(name="Arial", size=10, color="AAAAAA", italic=True),
    ),
)
ws.cell(
    sumr + 9,
    1,
    "LEGEND: grey rows = alternatives or references with quantity 0; they do not count in totals and are hidden by default.",
).font = Font(name="Arial", italic=True, color="666666")

for cc in range(1, ncol + 1):
    cell = ws.cell(1, cc)
    cell.font = hdr_font
    cell.fill = hdr_fill
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = border

widths = {
    1: 44, 2: 18, 3: 11, 4: 8, 5: 11, 6: 6, 7: 12, 8: 6, 9: 11, 10: 9,
    11: 9, 12: 8, 13: 30, 14: 58, 15: 52, 16: 14, 17: 36, 18: 10, 19: 11,
    20: 36,
}
for col, width in widths.items():
    ws.column_dimensions[get_column_letter(col)].width = width
ws.auto_filter.ref = f"A1:{get_column_letter(ncol)}{g_hi}"
ws.auto_filter.filterColumn.append(
    FilterColumn(
        colId=5,
        customFilters=CustomFilters(customFilter=[CustomFilter(operator="notEqual", val="0")]),
    )
)
ws.freeze_panes = "A2"
ws.row_dimensions[1].height = 30
for hidden_col in ("H", "I", "J", "K", "L", "M"):
    ws.column_dimensions[hidden_col].hidden = True

def add_premium_sheet(workbook):
    if "MOTORI premium" in workbook.sheetnames:
        del workbook["MOTORI premium"]
    sh = workbook.create_sheet("MOTORI premium")
    # gruppo, modello, DIMENSIONI, marca, qty, picco Nm, peso g cad, prezzo cad, valuta, peso g RobStride attuale, nota
    PREM = [
        ("Anche pitch/roll + ginocchio", "AKE90-8", "Ø107.5 x 43.5 mm", "CubeMars", 6, 170, 1400, 484, "USD", 1420,
         "170 Nm SUPERA il G1 (139 Nm): via lo 0.86x dell'RS04. 9 arcmin, dual enc. NUDO: + driver/encoder."),
        ("Caviglia parallela (2/gamba)", "EC-A4310-P2-36", "~Ø60 mm (n.d. uff. Foxtech)", "Encos", 4, 36, 377, 700, "USD", 621,
         "Baseline RS06 a 1:1 (621 g, Ø88). Encos A4310 = 36 Nm in 377 g e compatto (~Ø60, la scelta di Tien Kung): stessa coppia/potenza dell'RS06 ma -244 g CADAUNO e molto piu' piccolo. Serve SOLO se vuoi caviglia DINAMICA; per solo cammino l'RS00 a riduzione e' piu' leggero/economico (vedi nota)."),
        ("Anca yaw", "EC-A4310-P2-36", "~Ø60 mm (n.d. uff. Foxtech)", "Encos", 2, 36, 377, 700, "USD", 621,
         "36 Nm in 377 g. Margine ampio sui ~28 Nm di girata."),
        ("Vita yaw + roll diretto seriale (schema H2)", "EC-A4310-P2-36", "~Ø60 mm (n.d. uff. Foxtech)", "Encos", 2, 36, 377, 700, "USD", 621,
         "Vita seriale yaw (basso) + roll diretto (alto), niente pitch, niente puntoni. 36 Nm bastano e pesano poco; piu' RL-friendly del parallelo."),
        ("Spalla pitch/roll + gomito", "RS00 (resta RobStride)", "57 x 57 x 51 mm", "RobStride", 6, 14, 310, 116, "EUR", 310,
         "Sotto i ~20 Nm il premium pesa DI PIU' a pari coppia: RobStride resta la scelta leggera. RS00 (Ø57, 310 g, dual enc): l'RS02 e' stato eliminato (dominato)."),
        ("Spalla yaw + polso (x3)", "RS00 (resta RobStride)", "57 x 57 x 51 mm", "RobStride", 8, 14, 310, 116, "EUR", 310,
         "310 g: piu' leggero di qualsiasi premium a questa taglia. Dual encoder. Sotto i 43 mm Encos NON ha nulla -> niente Encos sui piccoli."),
        ("Collo pan/tilt", "RS05 (resta RobStride)", "46 x 46 x 44 mm", "RobStride", 2, 5.5, 191, 100, "EUR", 191,
         "191 g: niente lo batte a ~5 Nm. La testa e' leggera."),
    ]
    heads = ["Giunto", "Modello", "Dimensioni", "Marca", "Qty", "Picco Nm", "Peso g/cad", "Peso tot kg",
             "Prezzo/cad", "Val", "Prezzo tot", "Peso RobStride tot kg", "Delta peso kg", "Note"]
    for c, h in enumerate(heads, 1):
        cell = sh.cell(1, c, h); cell.font = hdr_font; cell.fill = hdr_fill
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    r = 2
    prem_kg = base_kg = usd = eur = 0.0
    for g, mod, dims, br, qty, pk, wt, pr, cur, wt_rs, note in PREM:
        pkg = wt * qty / 1000.0
        bkg = wt_rs * qty / 1000.0
        prem_kg += pkg; base_kg += bkg
        if cur == "USD": usd += pr * qty
        else: eur += pr * qty
        vals = [g, mod, dims, br, qty, pk, wt, round(pkg, 3), pr, cur, pr * qty, round(bkg, 3), round(pkg - bkg, 3), note]
        for c, v in enumerate(vals, 1):
            cell = sh.cell(r, c, v)
            cell.font = base_font
            cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=(c in (1, 2, 3, 14)))
        r += 1
    # riga totali
    sh.cell(r, 1, "TOTALE MOTORI (config vita seriale, 30 assi)").font = sec_font
    sh.cell(r, 8, round(prem_kg, 3)).font = sec_font
    sh.cell(r, 11, f"~ {usd:.0f} USD + {eur:.0f} EUR").font = sec_font
    sh.cell(r, 12, round(base_kg, 3)).font = sec_font
    sh.cell(r, 13, round(prem_kg - base_kg, 3)).font = sec_font
    for c in range(1, 15):
        sh.cell(r, c).fill = sec_fill
    r += 2
    for line in [
        "PREMIUM = mix ottimale: CubeMars AKE90-8 sulle GAMBE (coppia, supera il G1), Encos A4310 dove serve LEGGEREZZA",
        "(caviglia/anca-yaw/vita: 377 g vs 621), RobStride sui piccoli (gia' i piu' leggeri). Confronto vs stessa config",
        "tutta RobStride (RS04 gambe + RS06 nei 36 Nm). Il taglio di peso (~2 kg) viene da Encos, non da CubeMars.",
        "Prezzi: CubeMars retail (cubemars.com/RobotShop/Amazon); Encos a preventivo via Foxtech (meno disponibile).",
        "Gli AKE/Encos ad alta coppia possono essere NUDI (driver+encoder a parte): aggiungere ~150-300 USD/motore se cosi'.",
        "Questa scheda e' un'IPOTESI 'massima qualita'' affiancata al BOM RobStride (foglio umanoide), non sostituisce.",
    ]:
        c = sh.cell(r, 1, line); c.font = Font(name="Arial", size=9, italic=True, color="666666")
        r += 1
    pw = {1: 30, 2: 20, 3: 18, 4: 11, 5: 5, 6: 9, 7: 10, 8: 11, 9: 10, 10: 6, 11: 14, 12: 16, 13: 12, 14: 70}
    for col, w in pw.items():
        sh.column_dimensions[get_column_letter(col)].width = w
    sh.freeze_panes = "A2"
    sh.row_dimensions[1].height = 30


def add_encos_sheet(workbook):
    if "MOTORI Encos (quote)" in workbook.sheetnames:
        del workbook["MOTORI Encos (quote)"]
    sh = workbook.create_sheet("MOTORI Encos (quote)")
    intro = [
        "MOTORI ENCOS - SPEC DA DATASHEET V3.15EAP (numeri REALI, non piu' stime). Tutto planetario.",
        "Fornitore: ENCOS = Nanjing Encos Intelligent Technology (diretto) / Foxtech (store.foxtech.com) / aifitlab.com.",
        "NOME = EC-A[O statore][altezza statore]-[P plan/H arm][stadi]-[RIDUZIONE]. Il numero finale (25, 36) e' la RIDUZIONE, NON la coppia.",
        "O del nome = STATORE; il MODULO reale e' piu' grosso: A6416 -> O88; A4310/A4315 -> O56 (= come RS00 O57!); A2806 -> O44.",
        "DATASHEET: A6416 120Nm/805g/O88; A4310 36Nm/382g/O56; A4315 75Nm/485g/O56; A2806 12Nm/162g/O44. Tutti doppio encoder + cross-roller.",
    ]
    r = 1
    for line in intro:
        c = sh.cell(r, 1, line)
        c.font = Font(name="Arial", size=10, bold=(r == 1), color="000000")
        r += 1
    r += 1
    heads = ["Modello Encos", "O stat.", "O mod ~", "h mm ~", "Riduz.", "Picco Nm", "Nom Nm ~",
             "Peso g", "Qty", "Giunti (nostri 30 DOF)", "Fonte / confidenza"]
    for c, h in enumerate(heads, 1):
        cell = sh.cell(r, c, h); cell.font = hdr_font; cell.fill = hdr_fill
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    head_row = r
    r += 1
    ENCOS = [
        ("EC-A6416-P2-25", "64", "88", "67.5", "25:1", "120", "40", "805", 6,
         "GAMBE: hip pitch x2 + hip roll x2 + knee x2",
         "DATASHEET V3.15 p25: 107/120 RPM, Kt 2.74, backlash 15', cross-roller 3005."),
        ("EC-A4315-P2-36", "43", "56", "69.5", "36:1", "75", "25", "485", 16,
         "MID: caviglia x4 + spalle x6 + gomito x2 + hip yaw x2 + vita x2",
         "DATASHEET V3.15 p14: 109/117 RPM, Kt 2.8, 155 Nm/kg = densita' MAX gamma."),
        ("EC-A2806-P2-36", "28", "44", "44", "36:1", "12", "3", "162", 8,
         "POLSO+COLLO: polso x6 (3 DOF x2) + collo x2. Leggero/veloce (220 RPM).",
         "DATASHEET V3.15 p3: 207/220 RPM, Kt 1.35, 12'. NON a catalogo Foxtech."),
        ("EC-A4310-P2-36 (trial)", "43", "56", "60.5", "36:1", "36", "12", "382", 4,
         "TRIAL CAVIGLIA x4: comprati per PROVARE le caviglie (planetario lento, ok: robot non corre). Baseline caviglia resta A4315.",
         "DATASHEET V3.15 p9: 75/89 RPM, Kt 1.4, 10', 94 Nm/kg. O56 = come RS00."),
        ("[rif] EC-A6408-P2-25", "64", "88", "59.5", "25:1", "60", "~20", "604", 0,
         "riferimento O64 statore corto (meta' coppia di A6416, stesso O88)",
         "search precedente; conferma su p19 datasheet."),
    ]
    tot = 0
    for mod, dst, dmd, h, rid, pk, nom, wt, qty, joints, src in ENCOS:
        if not str(mod).startswith("[rif]"):
            tot += qty
        vals = [mod, dst, dmd, h, rid, pk, nom, wt, (qty if qty else ""), joints, src]
        for c, v in enumerate(vals, 1):
            cell = sh.cell(r, c, v); cell.font = base_font; cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=(c in (10, 11)))
        r += 1
    sh.cell(r, 1, f"TOTALE: {tot} motori acquistati = 30 nel robot (A6416 x6 + A4315 x16 + A2806 x8) + 4 A4310 trial caviglia").font = sec_font
    sh.cell(r, 9, tot).font = sec_font
    for c in range(1, 12):
        sh.cell(r, c).fill = sec_fill
    r += 2
    for line in [
        "SCELTA UTENTE 2026-06-19 = 3 MODELLI: A6416 gambe (pitch/roll/ginocchio) | A4315 mid (caviglia/spalle/gomito/hip-yaw/vita) | A2806 polso+collo.",
        "COLLO -> A2806 (162g) confermato: la testa non chiede 75Nm, si alleggerisce in alto. POLSO+COLLO = A2806 x8.",
        "CAVIGLIA = A4315 (la piu' pesante, tenuta apposta): pitch a puntone PROSSIMALE nello stinco + roll diretto piede. +4x A4310 comprati per PROVARE le caviglie (robot non corre -> ok planetario lento).",
        "GAMBE A6416 vs RS04: A6416 piu' piccolo (O88 vs O106), piu' leggero (805 vs 1420 g = -3.7 kg), +coppia continua (40 vs 30); MA 25:1 vs 9:1 = meno backdrivable.",
        "VESTIZIONE (sensori di coppia) = SERVE: a 25-36:1 la corrente NON da' coppia pulita (attrito gearbox); il dual-encoder interno NON basta su planetario rigido.",
        "  Metodi DIY: (1) flangia estensimetrica full-bridge (rigida, banda alta, incollaggio = arte); (2) SEA molla+encoder (tipo ANYmal/OpenTorque, +protez. impatti); (3) torsione magnetica non-contatto.",
        "  READY-TO-MOUNT (no DIY): Bota Systems Rokubi/PixONE/MiniONE (F/T 6 assi robot-grade, CAN/EtherCAT) | FUTEK / Sunrise Instruments / ME / HBK flangia coppia | NCTE non-contatto.",
        "  ONESTA': vestire ~10-18 giunti e' IL lavoro che RobStride (9:1, corrente=coppia) si risparmia. Prototipare 1 giunto; valutare se vestire solo le gambe.",
        "DA CHIEDERE NELLA QUOTE: prezzo cad Italia A6416/A4315/A2806/A4310, CAD STEP, lead time, MOQ, tensione 48V. Le spec TECNICHE le abbiamo (datasheet).",
    ]:
        c = sh.cell(r, 1, line); c.font = Font(name="Arial", size=9, italic=True, color="666666")
        r += 1
    ew = {1: 22, 2: 7, 3: 8, 4: 8, 5: 8, 6: 9, 7: 9, 8: 8, 9: 6, 10: 44, 11: 30}
    for col, w in ew.items():
        sh.column_dimensions[get_column_letter(col)].width = w
    sh.freeze_panes = f"A{head_row + 1}"


def add_robstride_sheet(workbook):
    if "MOTORI RobStride" in workbook.sheetnames:
        del workbook["MOTORI RobStride"]
    sh = workbook.create_sheet("MOTORI RobStride")
    intro = [
        "MOTORI ROBSTRIDE - configurazione completa (QDD ~9:1, BACKDRIVABLE, dual-encoder, force control via CORRENTE)",
        "Via 'Unitree-like': bassa riduzione -> cammina DINAMICO, niente sensore di coppia (la corrente basta). Reperibile Seeed/AliExpress, economico.",
        "Piu' grosso dell'Encos a pari coppia, ma backdrivable e force-control OUT-OF-THE-BOX (zero sensori, zero DIY).",
    ]
    r = 1
    for line in intro:
        c = sh.cell(r, 1, line); c.font = Font(name="Arial", size=10, bold=(r == 1), color="000000"); r += 1
    r += 1
    heads = [
        "Modello", "O mm", "Riduz.", "Picco Nm", "Nom Nm", "Massa kg",
        "Picco Nm/kg", "Nom Nm/kg", "Picco >10", "Nom >10", "Prezzo cad ~", "Uso attuale", "Fonte",
    ]
    for c, h in enumerate(heads, 1):
        cell = sh.cell(r, c, h); cell.font = hdr_font; cell.fill = hdr_fill
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    head_row = r; r += 1
    ROBS = [
        ("RobStride 04", 110, "9:1", 120, 40, 1.420, "~255 USD", "hip pitch/roll + ginocchia, 6 totali", "https://www.seeedstudio.com/Robostride-04-Actuator-p-6775.html"),
        ("RobStride 03", 106, "9:1", 60, 20, 0.900, "~225 USD", "waist roll, 1 totale", "https://www.seeedstudio.com/Robostride-03-Actuator-p-6774.html"),
        ("RobStride 06", 88, "9:1", 36, 11, 0.621, "~210 USD", "caviglie x4, hip yaw x2, waist yaw x1, shoulder pitch/roll x4, gomiti x2 = 13", "https://www.seeedstudio.com/Robostride-06-Actuator-p-6668.html"),
        ("RobStride 00", 57, "10:1", 14, 5, 0.310, "~125 USD", "shoulder yaw x2 + polsi x6 = 8", "https://www.seeedstudio.com/Robostride-00-Actuator-p-6664.html"),
        ("RobStride 05", 46, "7.75:1", 5.5, 1.6, 0.191, "~110 USD", "collo; non e' un major load-bearing joint", "https://www.seeedstudio.com/Robostride-05-Actuator-p-6666.html"),
    ]
    first_data_row = r
    for mod, dia, rid, pk, nom, mass, pr, joints, source in ROBS:
        vals = [mod, dia, rid, pk, nom, mass, None, None, None, None, pr, joints, source]
        for c, v in enumerate(vals, 1):
            cell = sh.cell(r, c, v); cell.font = base_font; cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=(c in (12, 13)))
        sh.cell(r, 7, f"=D{r}/F{r}")
        sh.cell(r, 8, f"=E{r}/F{r}")
        sh.cell(r, 9, f'=IF(G{r}>10,"PASS","FAIL")')
        sh.cell(r, 10, f'=IF(H{r}>10,"PASS","FAIL")')
        r += 1
    for row in range(first_data_row, r):
        sh.cell(row, 6).number_format = "0.000"
        sh.cell(row, 7).number_format = "0.0"
        sh.cell(row, 8).number_format = "0.0"
    sh.cell(r, 1, "ESITO: tutti i modelli scelti superano >10 Nm/kg al picco; RS05 non lo supera a coppia nominale (8,4 Nm/kg) ed e' limitato al collo.").font = sec_font
    for c in range(1, 14):
        sh.cell(r, c).fill = sec_fill
    r += 2
    for line in [
        "Tutti DUAL-ENCODER. ~9:1 = QDD BACKDRIVABLE -> force control da CORRENTE (come Unitree G1/H2), NIENTE sensore di coppia, NIENTE DIY.",
        "E' la via 'futuribile che cammina bene' a basso sforzo di controllo: piu' dinamico (impatti, terreno) dell'Encos alta-riduzione.",
        "Criterio: coppia specifica = coppia di uscita / massa completa attuatore. Il target dichiarato >10 Nm/kg usa normalmente il picco; qui e' mostrato anche il nominale.",
        "Configurazione bilanciata chiusa 2026-06-20: RS04 x6; RS03 x1 waist roll; RS06 x13; RS00 x8; RS05 x2. Totale 30 attuatori, waist yaw+roll, nessun waist pitch.",
        "vs ENCOS: RobStride piu' GROSSO (RS06 O88 vs A4310 O63; RS04 O106 vs A6416 O88) MA backdrivable e cammina meglio in dinamica (9:1 vs 25-36:1).",
        "Totali completi (tutte le fasi, con ferramenta/cavi/banco): vedi foglio 'umanoide'. Qui solo i motori.",
    ]:
        c = sh.cell(r, 1, line); c.font = Font(name="Arial", size=9, italic=True, color="666666"); r += 1
    rw = {1: 16, 2: 8, 3: 8, 4: 9, 5: 9, 6: 10, 7: 12, 8: 12, 9: 10, 10: 10, 11: 13, 12: 45, 13: 48}
    for col, w in rw.items():
        sh.column_dimensions[get_column_letter(col)].width = w
    sh.freeze_panes = f"A{head_row + 1}"


wb.active = 0
wb.calculation.calcMode = "auto"
wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.save(DST)
print("Salvato:", DST)
print("Righe dati:", len(data_rows), "| range G%d:G%d" % (g_lo, g_hi))
