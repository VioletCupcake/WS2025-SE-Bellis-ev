// src/services/choices.js

// ===== Fall choices =====
export const BERATUNGSSTELLE_CHOICES = [
  { value: 'FBS_1_LE', label: 'Fachberatungsstelle für queere Betroffene von sexualisierter Gewalt in der Stadt Leipzig' },
  { value: 'FBS_2_LKNSA', label: 'Fachberatung gegen sexualisierte Gewalt im Landkreis Nordsachsen' },
  { value: 'FBS_3_LKLE', label: 'Fachberatung gegen sexualisierte Gewalt im Landkreis Leipzig' }
]

export const STATUS_CHOICES = [
  { value: 'AKTIV', label: 'Aktiv' },
  { value: 'ARCHIVIERT', label: 'Archiviert' }
]

export const INFO_QUELLE_CHOICES = [
  { value: 'POLIZEI', label: 'Selbstmeldungen über Polizei' },
  { value: 'PRIVATE_KONTAKTE', label: 'Private Kontakte' },
  { value: 'BERATUNGSSTELLEN', label: 'Beratungsstellen' },
  { value: 'INTERNET', label: 'Internet' },
  { value: 'AEMTER', label: 'Ämter' },
  { value: 'GESUNDHEITSWESEN', label: 'Gesundheitswesen (Arzt/Ärztin)' },
  { value: 'RECHTSANWAELTE', label: 'Rechtsanwälte/-anwältinnen' },
  { value: 'ANDERE', label: 'andere Quelle' },
  { value: 'KEINE_ANGABE', label: 'keine Angabe' }
]

// ===== PersonenbezogeneDaten choices =====
export const ROLLE_CHOICES = [
  { value: 'BETROFFENE', label: 'Betroffene:r' },
  { value: 'ANGEHOERIGE', label: 'Angehörige:r' },
  { value: 'FACHKRAFT', label: 'Fachkraft' }
]

export const GESCHLECHT_CHOICES = [
  { value: 'CIS_W', label: 'cis weiblich' },
  { value: 'CIS_M', label: 'cis männlich' },
  { value: 'TRANS_W', label: 'trans weiblich' },
  { value: 'TRANS_M', label: 'trans männlich' },
  { value: 'TRANS_NB', label: 'trans nicht binär' },
  { value: 'INTER', label: 'inter' },
  { value: 'AGENDER', label: 'agender' },
  { value: 'DIVERS', label: 'divers' },
  { value: 'KEINE_ANGABE', label: 'keine Angabe' }
]

export const SEXUALITAET_CHOICES = [
  { value: 'LESBISCH', label: 'lesbisch' },
  { value: 'SCHWUL', label: 'schwul' },
  { value: 'BISEXUELL', label: 'bisexuell' },
  { value: 'ASEXUELL', label: 'asexuell' },
  { value: 'HETEROSEXUELL', label: 'heterosexuell' },
  { value: 'KEINE_ANGABE', label: 'keine Angabe' }
]

export const WOHNORT_CHOICES = [
  { value: 'LEIPZIG_STADT', label: 'Leipzig Stadt' },
  { value: 'LEIPZIG_LAND', label: 'Leipzig Land' },
  { value: 'NORDSACHSEN', label: 'Nordsachsen' },
  { value: 'SACHSEN', label: 'Sachsen' },
  { value: 'DEUTSCHLAND', label: 'Deutschland' },
  { value: 'ANDERE', label: 'andere' },
  { value: 'KEINE_ANGABE', label: 'keine Angabe' }
]

export const STAATSANGEHOERIGKEIT_CHOICES = [
  { value: 'DEUTSCH', label: 'deutsch' },
  { value: 'NICHT_DEUTSCH', label: 'nicht deutsch' }
]

export const BERUF_CHOICES = [
  { value: 'ARBEITSLOS', label: 'arbeitslos' },
  { value: 'STUDIEREND', label: 'studierend' },
  { value: 'BERUFSTAETIG', label: 'berufstätig' },
  { value: 'BERENTET', label: 'berentet' },
  { value: 'AZUBI', label: 'Azubi' },
  { value: 'BERUFSUNFAEHIG', label: 'berufsunfähig' },
  { value: 'KEINE_ANGABE', label: 'keine Angabe' }
]

export const SCHWERBEHINDERUNG_CHOICES = [
  { value: 'JA', label: 'Ja' },
  { value: 'NEIN', label: 'Nein' }
]

export const BEHINDERUNG_CHOICES = [
  { value: 'KOGNITIV', label: 'kognitiv' },
  { value: 'KOERPERLICH', label: 'körperlich' }
]

// ===== Beratung choices =====
export const DURCHFUEHRUNGSART_CHOICES = [
  { value: 'PERSOENLICH', label: 'persönlich' },
  { value: 'VIDEO', label: 'video' },
  { value: 'TELEFON', label: 'telefon' },
  { value: 'AUFSUCHEND', label: 'aufsuchend' },
  { value: 'SCHRIFTLICH', label: 'schriftlich' }
]

export const ORT_CHOICES = [
  { value: 'LEIPZIG_STADT', label: 'Leipzig Stadt' },
  { value: 'LEIPZIG_LAND', label: 'Leipzig Land' },
  { value: 'NORDSACHSEN', label: 'Nordsachsen' }
]

// ===== Gewalttat choices =====
export const VORFAELLE_CHOICES = [
  { value: 'EINMALIG', label: 'einmalig' },
  { value: 'MEHRERE', label: 'mehrere' },
  { value: 'GENAUE_ZAHL', label: 'genaue Zahl' },
  { value: 'KEINE_ANGABE', label: 'keine Angabe' }
]

export const TAETERINNEN_ANZAHL_CHOICES = [
  { value: '1', label: '1' },
  { value: 'MEHRERE', label: 'mehrere' },
  { value: 'GENAUE_ZAHL', label: 'genaue Zahl' },
  { value: 'KEINE_ANGABE', label: 'keine Angabe' }
]

export const TATORT_CHOICES = [
  { value: 'LEIPZIG', label: 'Leipzig' },
  { value: 'LEIPZIG_LAND', label: 'Leipzig Land' },
  { value: 'NORDSACHSEN', label: 'Nordsachsen' },
  { value: 'SACHSEN', label: 'Sachsen' },
  { value: 'DEUTSCHLAND', label: 'Deutschland' },
  { value: 'AUSLAND', label: 'Ausland' },
  { value: 'AUF_DER_FLUCHT', label: 'auf der Flucht' },
  { value: 'IM_HERKUNFTSLAND', label: 'im Herkunftsland' },
  { value: 'KEINE_ANGABE', label: 'keine Angabe' }
]

export const ANZEIGE_CHOICES = [
  { value: 'JA', label: 'Ja' },
  { value: 'NEIN', label: 'Nein' },
  { value: 'NOCH_NICHT_ENTSCHIEDEN', label: 'noch nicht entschieden' },
  { value: 'KEINE_ANGABE', label: 'keine Angabe' }
]

export const JA_NEIN_KEINE_ANGABE_CHOICES = [
  { value: 'JA', label: 'Ja' },
  { value: 'NEIN', label: 'Nein' },
  { value: 'KEINE_ANGABE', label: 'keine Angabe' }
]

export const FOLGE_DER_GEWAELT_CHOICES = [
  {
    label: 'Psychische Folgen',
    value: 'PSYCHISCH',
    children: [
      { label: 'Depression', value: 'DEPRESSION' },
      { label: 'Angststörung', value: 'ANGSTSTOERUNG' },
      { label: 'PTBS', value: 'PTBS' },
      { label: 'andere Diagnose', value: 'ANDERE_DIAGNOSE' },
      { label: 'Burn-Out', value: 'BURNOUT' },
      { label: 'Schlafstörungen', value: 'SCHLAFSTOERUNG' },
      { label: 'Sucht/Abhängigkeit', value: 'SUCHT' },
      { label: 'Kommunikationsschwierigkeiten', value: 'KOMMUNIKATION' },
      { label: 'Vernachlässigung alltäglicher Dinge', value: 'VERNACHLAESSIGUNG' }
    ]
  },
  {
    label: 'Körperliche Folgen',
    value: 'KOERPERLICH',
    children: [
      { label: 'Schmerzen', value: 'SCHMERZEN' },
      { label: 'Lähmungen', value: 'LAHMUNGEN' },
      { label: 'Krankheit', value: 'KRANKHEIT' }
    ]
  },
  {
    label: 'Dauerhafte körperliche Beeinträchtigung',
    value: 'DAUERHAFT_KOERPERLICH',
    hasFreeText: true
  },
  { label: 'Finanzielle Folgen', value: 'FINANZIELL' },
  { label: 'Arbeitseinschränkung/Arbeitsunfähigkeit', value: 'ARBEIT' },
  { label: 'Verlust Arbeitsstelle', value: 'VERLUST_ARBEIT' },
  { label: 'Soziale Isolation', value: 'SOZIALE_ISOLATION' },
  {
    label: 'Suizidalität',
    value: 'SUIZIDALITAET'
  },
  {
    label: 'Weiteres',
    value: 'WEITERES',
    hasFreeText: true
  },
  {
    label: 'Keine Angabe',
    value: 'KEINE_ANGABE',
    hasFreeText: true
  }
]

/* Daten zur gewalt*/
const vorfallOptions = [
  "einmalig", "mehrere", "genaue_zahl", "keine_angabe"
]

const taeterAnzahlOptions = [
  "1", "mehrere", "genaue_zahl", "keine_angabe"
]

const geschlechtOptions = [
  "m", "w", "divers", "unbekannt", "keine_angabe"
]

const verhaeltnisOptions = [
  "Unbekannte:r",
  "Bekannte:r",
  "Partner:in",
  "Partner:in ehemalig",
  "Ehepartner:in / Lebenspartner:in",
  "Familienangehörige",
  "Sonstige",
  "Keine Angabe"
]

const gewaltartenOptions = [
  "sexuelle Belästigung – öffentlicher Raum",
  "sexuelle Belästigung – Arbeitsplatz",
  "sexuelle Belästigung – Privat",
  "Vergewaltigung",
  "Versuchte Vergewaltigung",
  "Sexueller Missbrauch",
  "Sexueller Missbrauch in der Kindheit",
  "Sexuelle Nötigung",
  "Rituelle Gewalt",
  "Zwangsprostitution",
  "Sexuelle Ausbeutung",
  "Upskirting",
  "Catcalling",
  "Digitale sexuelle Gewalt",
  "Spiking",
  "Andere",
  "Keine Angabe"
]

const tatortOptions = [
  "Leipzig", "Leipzig Land", "Nordsachsen", "Sachsen",
  "Deutschland", "Ausland", "auf der Flucht", "Herkunftsland",
  "Keine Angabe"
]




// ===========================
// Zahl der Vorfälle
// ===========================
export const ZAHL_DER_VORFAELLE_CHOICES = [
  { label: 'Einmalig', value: 'EINMALIG' },
  { label: 'Mehrere', value: 'MEHRERE' },
  { label: 'Genaue Zahl', value: 'GENAUE_ZAHL' },
  { label: 'Keine Angabe', value: 'KEINE_ANGABE' }
]

// ===========================
// Anzahl Täter:innen
// ===========================
export const ANZAHL_TAETERINNEN_CHOICES = [
  { label: '1', value: '1' },
  { label: 'Mehrere', value: 'MEHRERE' },
  { label: 'Genaue Zahl', value: 'GENAUE_ZAHL' },
  { label: 'Keine Angabe', value: 'KEINE_ANGABE' }
]

// ===========================
// Täter:in Beziehung zur Ratsuchenden Person
// ===========================
export const TAETER_BEZIEHUNG_CHOICES = [
  { label: 'Unbekannte:r', value: 'UNBEKANNT' },
  { label: 'Bekannte:r', value: 'BEKANNT' },
  { label: 'Partner:in', value: 'PARTNER' },
  { label: 'Partner:in ehemalig', value: 'PARTNER_EHEMALIG' },
  { label: 'Ehepartner:in oder eingetragene:r Lebenspartner:in', value: 'EHEPARTNER_LP' },
  { label: 'Andere Familienangehörige', value: 'ANDERE_FAMILIE' },
  { label: 'Sonstige Personen', value: 'SONSTIGE' },
  { label: 'Keine Angabe', value: 'KEINE_ANGABE' }
]

// ===========================
// Art der Gewalt (Mehrfachauswahl)
// ===========================
export const GEWALTTAT_ART_CHOICES = [
  { label: 'Sexuelle Belästigung – im öffentlichen Raum', value: 'SEXUELLE_BELAESTIGUNG_OEFFENTLICH' },
  { label: 'Sexuelle Belästigung – am Arbeitsplatz', value: 'SEXUELLE_BELAESTIGUNG_ARBEIT' },
  { label: 'Sexuelle Belästigung – im Privaten', value: 'SEXUELLE_BELAESTIGUNG_PRIVAT' },
  { label: 'Vergewaltigung', value: 'VERGEWALTIGUNG' },
  { label: 'Versuchte Vergewaltigung', value: 'VERSUCHTE_VERGEWALTIGUNG' },
  { label: 'Sexueller Missbrauch', value: 'SEXUELLER_MISSBRAUCH' },
  { label: 'Sexueller Missbrauch in der Kindheit', value: 'SEXUELLER_MISSBRAUCH_KINDHEIT' },
  { label: 'Sexuelle Nötigung', value: 'SEXUELLE_NOETIGUNG' },
  { label: 'Rituelle Gewalt', value: 'RITUELLE_GEWAELT' },
  { label: 'Zwangsprostitution', value: 'ZWANGSPROSTITUTION' },
  { label: 'Sexuelle Ausbeutung', value: 'SEXUELLE_AUSBEUTUNG' },
  { label: 'Upskirting', value: 'UPSKIRTING' },
  { label: 'Catcalling', value: 'CATCALLING' },
  { label: 'Digitale sexuelle Gewalt', value: 'DIGITALE_SEXUELLE_GEWAELT' },
  { label: 'Spiking', value: 'SPIKING' },
  { label: 'Andere', value: 'ANDERE' },
  { label: 'Keine Angabe', value: 'KEINE_ANGABE' }
];

