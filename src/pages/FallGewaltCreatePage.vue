<template>
  <q-page padding>

    <h4 class="q-mb-md">Gewalttat hinzufügen</h4>

    <q-form @submit.prevent="submitForm">

      <!-- Alter -->
      <q-input
        v-model="form.alter"
        label="Alter zum Zeitpunkt der Tat"
        type="number"
        filled
        class="q-mb-md"
        hint="Leer lassen für 'keine Angabe'"
      />

      <!-- Zeitraum -->
      <q-input
        v-model="form.zeitraum"
        label="Zeitraum (optional)"
        type="text"
        filled
        class="q-mb-md"
        hint="z. B. 2019–2021"
      />

      <!-- Zahl der Vorfälle -->
      <q-select
        filled
        v-model="form.vorfallOption"
        :options="vorfallOptions"
        label="Zahl der Vorfälle"
        class="q-mb-md"
      />

      <q-input
        v-if="form.vorfallOption === 'genaue_zahl'"
        v-model="form.vorfaelle_genau"
        type="number"
        label="Genaue Anzahl"
        filled
        class="q-mb-md"
      />

      <!-- Anzahl Täter:innen -->
      <q-select
        filled
        v-model="form.taeterOption"
        :options="taeterOptions"
        label="Anzahl Täter:innen"
        class="q-mb-md"
      />

      <q-input
        v-if="form.taeterOption === 'genaue_zahl'"
        v-model="form.taeter_genau"
        type="number"
        label="Genaue Anzahl Täter:innen"
        filled
        class="q-mb-md"
      />

      <!-- Dynamische Täter Felder -->
      <div v-for="(t, index) in form.taeter" :key="index" class="q-pa-md q-mb-md bg-grey-2 rounded-borders">

        <div class="row items-center justify-between q-mb-sm">
          <strong>Täter:in {{ index + 1 }}</strong>
          <q-btn
            color="negative"
            icon="delete"
            flat
            dense
            @click="removeTaeter(index)"
          />
        </div>

        <q-select
          filled
          v-model="t.geschlecht"
          :options="geschlechtOptions"
          label="Geschlecht"
          class="q-mb-md"
        />

        <q-select
          filled
          v-model="t.verhaeltnis"
          :options="verhaeltnisOptions"
          label="Verhältnis zur ratsuchenden Person"
          class="q-mb-md"
        />

        <!-- Gewaltarten Mehrfachauswahl -->
        <q-select
          filled
          multiple
          use-chips
          v-model="t.gewaltarten"
          :options="gewaltartenOptions"
          label="Art der Gewalt"
          class="q-mb-md"
        />

        <q-input
          v-if="t.gewaltarten.includes('andere')"
          v-model="t.gewalt_andere_text"
          label="Andere – genauere Angaben"
          filled
          class="q-mb-md"
        />

        <q-select
          filled
          v-model="t.tatort"
          :options="tatortOptions"
          label="Tatort"
          class="q-mb-md"
        />

        <q-select
          filled
          v-model="t.anzeige"
          :options="anzeigeOptions"
          label="Anzeige"
          class="q-mb-md"
        />

        <q-select
          filled
          v-model="t.medizin"
          :options="medizinOptions"
          label="Medizinische Versorgung"
          class="q-mb-md"
        />

        <q-select
          filled
          v-model="t.vss"
          :options="vssOptions"
          label="Vertrauliche Spurensicherung"
          class="q-mb-md"
        />
      </div>

      <q-btn
        label="Täter:in hinzufügen"
        color="primary"
        outline
        icon="add"
        class="q-mb-lg"
        @click="addTaeter"
      />

      <!-- Kinder -->
      <q-input
        v-model="form.kinder"
        type="number"
        filled
        label="Mitbetroffene Kinder (Zahl)"
        class="q-mb-md"
      />

      <q-input
        v-model="form.kinder_direkt"
        type="number"
        filled
        label="Davon direkt betroffen (Zahl)"
        class="q-mb-md"
      />

      <!-- Notizen -->
      <q-input
        v-model="form.notizen"
        filled
        type="textarea"
        label="Weitere Notizen"
        autogrow
        class="q-mb-md"
      />

      <!-- Submit -->
      <q-btn type="submit" color="primary" label="Speichern" />
    </q-form>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const fallId = route.params.fallId

const form = ref({
  alter: '',
  zeitraum: '',
  vorfallOption: null,
  vorfaelle_genau: null,
  taeterOption: null,
  taeter_genau: null,
  taeter: [],
  kinder: null,
  kinder_direkt: null,
  notizen: ''
})

const vorfallOptions = [
  { label: 'Einmalig', value: 'einmalig' },
  { label: 'Mehrere', value: 'mehrere' },
  { label: 'Genaue Zahl', value: 'genaue_zahl' },
  { label: 'Keine Angabe', value: 'keine_angabe' }
]

const taeterOptions = [
  { label: '1', value: '1' },
  { label: 'Mehrere', value: 'mehrere' },
  { label: 'Genaue Zahl', value: 'genaue_zahl' },
  { label: 'Keine Angabe', value: 'keine_angabe' }
]

const geschlechtOptions = [
  'Männlich', 'Weiblich', 'Divers', 'Unbekannt'
]

const verhaeltnisOptions = [
  'Unbekannte:r', 'Bekannte:r', 'Partner:in', 'Partner:in ehemalig', 
  'Ehepartner:in oder eingetragene Lebenspartner:in',
  'Andere Familienangehörige', 'Sonstige Personen', 'Keine Angabe'
]

const gewaltartenOptions = [
  { label: 'Sexuelle Belästigung (öffentlich)', value: 'bel_oeffentlich' },
  { label: 'Sexuelle Belästigung (Arbeitsplatz)', value: 'bel_arbeit' },
  { label: 'Sexuelle Belästigung (privat)', value: 'bel_privat' },
  { label: 'Vergewaltigung', value: 'vergewaltigung' },
  { label: 'Versuchte Vergewaltigung', value: 'versuchte_vergewaltigung' },
  { label: 'Sexueller Missbrauch', value: 'missbrauch' },
  { label: 'Missbrauch in Kindheit', value: 'kindheit' },
  { label: 'Sexuelle Nötigung', value: 'noetigung' },
  { label: 'Rituelle Gewalt', value: 'ritueller' },
  { label: 'Zwangsprostitution', value: 'zwangsprostitution' },
  { label: 'Sexuelle Ausbeutung', value: 'ausbeutung' },
  { label: 'Upskirting', value: 'upskirting' },
  { label: 'Catcalling', value: 'catcalling' },
  { label: 'Digitale sexuelle Gewalt', value: 'digital' },
  { label: 'Spiking', value: 'spiking' },
  { label: 'Andere', value: 'andere' },
  { label: 'Keine Angabe', value: 'keine_angabe' }
]

const tatortOptions = [
  'Leipzig', 'Leipzig Land', 'Nordsachsen', 'Sachsen', 'Deutschland', 'Ausland',
  'Auf der Flucht', 'Herkunftsland', 'Keine Angabe'
]

const anzeigeOptions = ['Ja', 'Nein', 'Noch nicht entschieden', 'Keine Angabe']
const medizinOptions = ['Ja', 'Nein', 'Keine Angabe']
const vssOptions = ['Ja', 'Nein', 'Keine Angabe']

const addTaeter = () => {
  form.value.taeter.push({
    geschlecht: null,
    verhaeltnis: null,
    gewaltarten: [],
    gewalt_andere_text: '',
    tatort: null,
    anzeige: null,
    medizin: null,
    vss: null
  })
}

const removeTaeter = (index) => {
  form.value.taeter.splice(index, 1)
}

const submitForm = () => {
  console.log('Submit for Fall ID:', fallId, form.value)
}
</script>
