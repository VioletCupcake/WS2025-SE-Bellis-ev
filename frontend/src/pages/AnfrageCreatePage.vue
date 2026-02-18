<template>
  <q-page padding>
    <div class="text-h5 q-mb-md">Neue Anfrage erfassen</div>

    <q-form @submit="handleSubmit" @reset="handleReset" ref="formRef">

      <!-- Kontaktart -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section class="bg-grey-3">
          <div class="text-subtitle1">Allgemeine Informationen</div>
        </q-card-section>
        <q-card-section>
          <div class="row q-col-gutter-md">

            <div class="col-12 col-md-6">
              <q-select
                filled
                v-model="form.kontaktArt"
                :options="['Telefon','E-Mail','Persönlich']"
                label="Kontaktart"
                :rules="[v => !!v || 'Pflichtfeld']"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-input
                filled
                type="date"
                v-model="form.datum"
                label="Datum der Anfrage"
                :rules="[v => !!v || 'Pflichtfeld']"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-select
                filled
                v-model="form.anfrageAus"
                :options="['Leipzig Stadt','Leipzig Land','Nordsachsen','Sachsen','andere']"
                label="Anfrage aus"
                :rules="[v => !!v || 'Pflichtfeld']"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-select
                filled
                v-model="form.werHatAngefragt"
                :options="[
                  'Fachkraft','Angehörige:r','Betroffene:r','Anonym',
                  'queer Betroffene:r','queer Fachkraft','queer Angehörige:r','queer anonym',
                  'Fachkraft für Betroffene','Angehörige:r für Betroffene',
                  'Fachkraft für queere Betroffene','Angehörige für queere Betroffene'
                ]"
                label="Wer hat angefragt"
                :rules="[v => !!v || 'Pflichtfeld']"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-select
                filled
                v-model="form.artDerAnfrage"
                :options="[
                  'medizinische Soforthilfe',
                  'Vertrauliche Spurensicherung',
                  'Beratungsbedarf',
                  'zu Rechtlichem',
                  'Sonstiges'
                ]"
                label="Art der Anfrage"
                :rules="[v => !!v || 'Pflichtfeld']"
              />
            </div>

            <!-- Termin vergeben -->
            <div class="col-12 col-md-6">
              <q-toggle
                v-model="form.terminVergeben"
                label="Termin vergeben?"
              />
            </div>

            <div class="col-12 col-md-6" v-if="form.terminVergeben">
              <q-input
                filled
                type="date"
                v-model="form.terminDatum"
                label="Datum des Termins"
              />
            </div>

            <div class="col-12 col-md-6" v-if="form.terminVergeben">
              <q-select
                filled
                v-model="form.terminOrt"
                :options="['Leipzig Stadt','Leipzig Land','Nordsachsen']"
                label="Ort des Termins"
              />
            </div>

            <!-- Dolmetscher -->
            <div class="col-12 col-md-6">
              <q-input
                filled
                type="number"
                min="0"
                v-model="form.dolmetscherStunden"
                label="Dolmetscherstunden"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-input
                filled
                v-model="form.dolmetscherSprachen"
                label="Dolmetscher Sprachen (Komma getrennt)"
              />
            </div>

            <!-- Notizen -->
            <div class="col-12">
              <q-input
                filled
                type="textarea"
                rows="3"
                v-model="form.notizen"
                label="Notizen"
              />
            </div>

          </div>
        </q-card-section>
      </q-card>

      <!-- Form Actions -->
      <div class="row q-mt-lg">
        <div class="col-auto">
          <q-btn label="Anfrage speichern" color="primary" type="submit" />
        </div>
        <div class="col-auto">
          <q-btn flat label="Zurücksetzen" type="reset" />
        </div>
      </div>

    </q-form>

    <div v-if="error" class="text-negative q-mt-md">{{ error }}</div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const formRef = ref(null)
const error = ref('')

const form = ref({
  kontaktArt: '',
  datum: new Date().toISOString().split('T')[0],
  anfrageAus: '',
  werHatAngefragt: '',
  artDerAnfrage: '',
  terminVergeben: false,
  terminDatum: '',
  terminOrt: '',
  notizen: '',
  dolmetscherStunden: '',
  dolmetscherSprachen: ''
})

const handleSubmit = async () => {
  const payload = {
    wie: form.value.kontaktArt,
    datumAnfrage: form.value.datum,
    anfrageAus: form.value.anfrageAus,
    werHatAngefragt: form.value.werHatAngefragt,
    artDerAnfrage: form.value.artDerAnfrage,
    terminVergeben: form.value.terminVergeben,
    terminDatum: form.value.terminVergeben ? form.value.terminDatum : null,
    terminOrt: form.value.terminVergeben ? form.value.terminOrt : null,
    notizen: form.value.notizen,
    dolmetscherStunden: form.value.dolmetscherStunden ? Number(form.value.dolmetscherStunden) : undefined,
    dolmetscherSprachen: form.value.dolmetscherSprachen ? form.value.dolmetscherSprachen.split(',').map(s => s.trim()) : []
  }

  try {
    await axios.post('http://localhost:8000/inquiries/new', payload) // replace with your backend URL
    alert('Anfrage erfolgreich gespeichert!')
    router.push('/dashboard')
  } catch (err) {
    console.error(err)
    error.value = 'Fehler beim Speichern der Anfrage'
  }
}

const handleReset = () => {
  form.value = {
    kontaktArt: '',
    datum: new Date().toISOString().split('T')[0],
    anfrageAus: '',
    werHatAngefragt: '',
    artDerAnfrage: '',
    terminVergeben: false,
    terminDatum: '',
    terminOrt: '',
    notizen: '',
    dolmetscherStunden: '',
    dolmetscherSprachen: ''
  }
  error.value = ''
}
</script>
