<template>
  <q-page padding>
    <div class="text-h5 q-mb-md">{{ action }} Fall</div>

    <q-form ref="form" @submit="onSubmit" @reset="onReset">

      <!-- ===================== -->
      <!-- FALL SECTION -->
      <!-- ===================== -->
      <q-card flat bordered class="q-mb-lg">
        <q-card-section class="bg-grey-3">
          <div class="text-subtitle1">Fallinformationen</div>
        </q-card-section>

        <q-card-section>
          <div class="row q-col-gutter-md">

            <div class="col-12 col-md-6">
              <q-select
                filled
                v-model="formData.zustaendige_beratungsstelle"
                :options="BERATUNGSSTELLE_CHOICES"
                label="Zuständige Beratungsstelle"
                :rules="[v => !!v || 'Pflichtfeld']"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-select
                filled
                v-model="formData.informationsquelle"
                :options="INFO_QUELLE_CHOICES"
                label="Informationsquelle"
              />
            </div>

            <div class="col-12" v-if="formData.informationsquelle === 'ANDERE'">
              <q-input
                filled
                type="textarea"
                rows="3"
                v-model="formData.informationsquelle_andere_details"
                label="Andere Quelle - Details"
                :rules="[val => formData.informationsquelle !== 'ANDERE' || (!!val && val.trim() !== '') || 'Details erforderlich']"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-toggle
                v-model="formData.dolmetschung_in_anspruch_genommen"
                label="Wurde Dolmetschung in Anspruch genommen?"
              />
            </div>

            <div class="col-12 col-md-6" v-if="formData.dolmetschung_in_anspruch_genommen">
              <q-input
                filled
                type="number"
                min="0"
                step="0.25"
                v-model="formData.anzahl_dolmetschungen_stunden"
                label="Anzahl der Dolmetschungs-Stunden"
              />
            </div>

            <div class="col-12" v-if="formData.dolmetschung_in_anspruch_genommen">
              <q-input
                filled
                type="textarea"
                rows="2"
                v-model="formData.dolmetschung_sprachen"
                label="Dolmetschungs-Sprachen"
              />
            </div>

            <div class="col-12">
              <q-input
                filled
                type="textarea"
                rows="4"
                v-model="formData.weitere_notizen"
                label="Weitere Notizen"
              />
            </div>

          </div>
        </q-card-section>
      </q-card>

      <!-- ===================== -->
      <!-- PERSONEN SECTION -->
      <!-- ===================== -->
      <q-card flat bordered>
        <q-card-section class="bg-grey-3">
          <div class="text-subtitle1">Personenbezogene Daten</div>
        </q-card-section>

        <q-card-section>
          <div class="row q-col-gutter-md">

            <div class="col-12 col-md-6">
              <q-input
                filled
                v-model="formData.alias"
                label="Alias (eindeutige Kennung)"
                :rules="[v => !!v || 'Pflichtfeld']"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-select
                filled
                v-model="formData.rolle_der_ratsuchenden_person"
                :options="ROLLE_CHOICES"
                label="Rolle"
                :rules="[v => !!v || 'Pflichtfeld']"
              />
            </div>

            <div class="col-12 col-md-4" v-if="!formData.alter_keine_angabe">
              <q-input
                filled
                type="number"
                min="0"
                max="120"
                v-model="formData.alter"
                label="Alter"
              />
            </div>

            <div class="col-12 col-md-4">
              <q-toggle
                v-model="formData.alter_keine_angabe"
                label="Alter: keine Angabe"
              />
            </div>

            <div class="col-12 col-md-4">
              <q-select
                filled
                v-model="formData.geschlechtsidentitaet"
                :options="GESCHLECHT_CHOICES"
                label="Geschlechtsidentität"
              />
            </div>

            <div class="col-12 col-md-4">
              <q-select
                filled
                v-model="formData.sexualitaet"
                :options="SEXUALITAET_CHOICES"
                label="Sexualität"
              />
            </div>

            <div class="col-12 col-md-4">
              <q-select
                filled
                v-model="formData.wohnort"
                :options="WOHNORT_CHOICES"
                label="Wohnort"
              />
            </div>

            <div class="col-12">
              <q-input
                filled
                type="textarea"
                rows="2"
                v-model="formData.wohnort_details"
                label="Wohnort - Details"
              />
            </div>

            <div class="col-12 col-md-4">
              <q-select
                filled
                v-model="formData.staatsangehoerigkeit_deutsch"
                :options="STAATSANGEHOERIGKEIT_CHOICES"
                label="Staatsangehörigkeit deutsch?"
              />
            </div>

            <div class="col-12 col-md-4" v-if="formData.staatsangehoerigkeit_deutsch === 'NICHT_DEUTSCH'">
              <q-input
                filled
                v-model="formData.staatsangehoerigkeit_land"
                label="Staatsangehörigkeit - Land"
              />
            </div>

            <div class="col-12 col-md-4">
              <q-select
                filled
                v-model="formData.berufliche_situation"
                :options="BERUF_CHOICES"
                label="Berufliche Situation"
              />
            </div>

            <div class="col-12 col-md-4">
              <q-select
                filled
                v-model="formData.schwerbehinderung"
                :options="SCHWERBEHINDERUNG_CHOICES"
                label="Schwerbehinderung?"
              />
            </div>

            <div class="col-12 col-md-4" v-if="formData.schwerbehinderung === 'JA'">
              <q-select
                filled
                v-model="formData.form_der_behinderung"
                :options="BEHINDERUNG_CHOICES"
                label="Form der Behinderung"
              />
            </div>

            <div class="col-12 col-md-4" v-if="formData.schwerbehinderung === 'JA'">
              <q-input
                filled
                type="number"
                min="0"
                max="100"
                v-model="formData.grad_der_behinderung"
                label="Grad der Behinderung (GdB)"
              />
            </div>

            <div class="col-12">
              <q-input
                filled
                type="textarea"
                rows="4"
                v-model="formData.personenbezogene_notizen"
                label="Personenbezogene Notizen"
              />
            </div>

          </div>
        </q-card-section>
      </q-card>

      <div class="row q-mt-xl">
        <div class="col-auto">
          <q-btn label="Speichern" color="primary" type="submit" />
        </div>
        <div class="col-auto">
          <q-btn flat label="Zurücksetzen" type="reset" />
        </div>
      </div>

    </q-form>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'

import {
  QCardSection,
  QSelect,
  QInput,
  QToggle,
  QCard,
  QBtn,
  QForm,
  QPage
} from 'quasar'

import { api } from 'src/services/api.js'
import {
  BERATUNGSSTELLE_CHOICES,
  INFO_QUELLE_CHOICES,
  ROLLE_CHOICES,
  GESCHLECHT_CHOICES,
  SEXUALITAET_CHOICES,
  WOHNORT_CHOICES,
  STAATSANGEHOERIGKEIT_CHOICES,
  BERUF_CHOICES,
  SCHWERBEHINDERUNG_CHOICES,
  BEHINDERUNG_CHOICES
} from 'src/services/choices.js'

const action = 'Erstellen'

const form = ref(null)

const formData = ref({
  zustaendige_beratungsstelle: '',
  informationsquelle: '',
  informationsquelle_andere_details: '',
  dolmetschung_in_anspruch_genommen: false,
  anzahl_dolmetschungen_stunden: 0,
  dolmetschung_sprachen: '',
  weitere_notizen: '',

  alias: '',
  rolle_der_ratsuchenden_person: '',
  alter: null,
  alter_keine_angabe: false,
  geschlechtsidentitaet: 'KEINE_ANGABE',
  sexualitaet: 'KEINE_ANGABE',
  wohnort: '',
  wohnort_details: '',
  staatsangehoerigkeit_deutsch: '',
  staatsangehoerigkeit_land: '',
  berufliche_situation: '',
  schwerbehinderung: '',
  form_der_behinderung: '',
  grad_der_behinderung: null,
  personenbezogene_notizen: ''
})

const onSubmit = async () => {
  if (!(await form.value.validate())) return

  try {
    await api.post('/fall/create/', formData.value)

    // Reset validation (but keep form data if you want)
    form.value.resetValidation()

    // Success notification
    form.value.$q.notify({
      type: 'positive',
      message: 'Fall gespeichert!'
    })

    // Optionally, reset the form data completely
    Object.keys(formData.value).forEach(key => {
      if (typeof formData.value[key] === 'boolean') {
        formData.value[key] = false
      } else if (typeof formData.value[key] === 'number') {
        formData.value[key] = 0
      } else {
        formData.value[key] = ''
      }
    })
    
  } catch (error) {
    // Log error for debugging
    console.error('Fehler beim Speichern des Falls:', error)

    // Show error notification
    form.value.$q.notify({
      type: 'negative',
      message: 'Fehler beim Speichern!'
    })
  }
}


const onReset = () => {
  Object.keys(formData.value).forEach(k => {
    if (typeof formData.value[k] === 'boolean') formData.value[k] = false
    else if (typeof formData.value[k] === 'number') formData.value[k] = 0
    else formData.value[k] = ''
  })
}
</script>
