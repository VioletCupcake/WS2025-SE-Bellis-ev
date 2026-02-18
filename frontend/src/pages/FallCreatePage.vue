<template>
  <q-page padding>
    <div class="text-h5 q-mb-md">{{ action }} Fall</div>

    <q-form ref="form" @submit="onSubmit" @reset="onReset">

     

      <!-- ===================== -->
      <!-- PERSONEN SECTION -->
      <!-- ===================== -->
      <q-card flat bordered class="q-mb-lg">
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

      <!-- ===================== -->
      <!-- GEWALTTAT SECTION -->
      <!-- ===================== -->
      <q-card flat bordered class="q-mb-lg">
        <q-card-section class="bg-grey-3">
          <div class="text-subtitle1">Gewalttat Informationen</div>
        </q-card-section>

        <q-card-section>
          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              <q-input
                filled
                type="number"
                min="0"
                max="120"
                v-model="formData.alter_zum_zeitpunkt_der_tat"
                label="Alter zum Zeitpunkt der Tat"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-toggle
                v-model="formData.alter_tat_keine_angabe"
                label="Keine Angabe"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-input
                filled
                type="date"
                v-model="formData.zeitraum_von"
                label="Zeitraum von"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-input
                filled
                type="date"
                v-model="formData.zeitraum_bis"
                label="Zeitraum bis"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-toggle
                v-model="formData.zeitraum_keine_angabe"
                label="Keine Angabe"
              />
            </div>

            <div class="col-12 col-md-6">
              <q-select
                filled
                v-model="selectedArt"
                :options="GEWALTTAT_ART_CHOICES"
                label="Art der Gewalt"
                emit-value
                map-options
              />
            </div>

            <div class="col-12 col-md-6" v-if="selectedArt?.label === 'ANDERE'">
              <q-input
                filled
                v-model="andereDetails"
                label="Andere Details"
              />
            </div>

            <div class="col-12">
              <q-input
                filled
                type="textarea"
                rows="3"
                v-model="formData.gewalt_notizen"
                label="Notizen"
              />
            </div>

            <div class="col-12">
              <q-btn
                label="Hinzufügen"
                color="primary"
                @click="addGewalttatArt"
              />
            </div>

            <div class="col-12 q-mt-md" v-if="fallArten.length">
              <div class="text-subtitle2">Hinzugefügte Arten:</div>
              <ul>
                <li v-for="f in fallArten" :key="f.id">
                  {{ f.name }} {{ f.details ? `- ${f.details}` : '' }}
                  <q-btn dense flat icon="delete" color="red" @click="removeGewalttatArt(f.id)" />
                </li>
              </ul>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- ===================== -->
      <!-- FOLGE DER GEWALT SECTION -->
      <!-- ===================== -->
      <q-card flat bordered class="q-mb-lg">
        <q-card-section class="bg-grey-3">
          <div class="text-subtitle1">Folge der Gewalt</div>
        </q-card-section>

        <q-card-section>
          <div class="row q-col-gutter-md">

            <div class="col-12 col-md-6">
              <q-select
                filled
                v-model="selectedFolgenCategory"
                :options="FOLGE_DER_GEWAELT_CHOICES"
                label="Kategorie der Folgen"
                emit-value
              />
            </div>

            <div class="col-12 col-md-6 q-mt-md" v-if="selectedFolgenCategory">
              <q-select
                filled
                v-model="selectedFolgenSub"
                :options="getSubOptions(selectedFolgenCategory)"
                label="Optionen"
                use-chips
                multiple
                emit-value
              />
            </div>

            <div class="col-12 q-mt-md" v-for="f in selectedFolgenSub" :key="f">
              <q-input
                v-if="getSubOptions(selectedFolgenCategory).find(o => o.value === f)?.hasFreeText"
                filled
                v-model="fallFolgenInfo[f]"
                :label="getSubOptions(selectedFolgenCategory).find(o => o.value === f)?.label + ' - Details'"
                type="textarea"
                rows="2"
              />
            </div>

            <div class="col-12 q-mt-md">
              <q-btn label="Hinzufügen" color="primary" @click="addFolgenToFall" />
            </div>

            <div class="col-12 q-mt-md" v-if="fallFolgen.length">
              <div class="text-subtitle2">Hinzugefügte Folgen:</div>
              <ul>
                <li v-for="f in fallFolgen" :key="f.value">
                  {{ f.label }} - {{ f.info }}
                  <q-btn dense flat icon="delete" color="red" @click="removeFallFolge(f.value)" />
                </li>
              </ul>
            </div>

          </div>
        </q-card-section>
      </q-card>

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
                :rules="[val => !!val || 'Details erforderlich']"
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
      <!-- FORM ACTIONS -->
      <!-- ===================== -->
      <div class="row q-mt-xl">
        <div class="col-auto">
          <q-btn label="Fall speichern" color="primary" type="submit" />
        </div>
        <div class="col-auto">
          <q-btn flat label="Zurücksetzen" type="reset" />
        </div>
      </div>

    </q-form>
  </q-page>
</template>

<script setup>
import { ref, reactive } from 'vue'
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
  BEHINDERUNG_CHOICES,
  FOLGE_DER_GEWAELT_CHOICES,
  GEWALTTAT_ART_CHOICES
} from 'src/services/choices.js'

const action = 'Erstellen'
const form = ref(null)

const formData = reactive({
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
  personenbezogene_notizen: '',
  alter_zum_zeitpunkt_der_tat: null,
  alter_tat_keine_angabe: false,
  zeitraum_von: '',
  zeitraum_bis: '',
  zeitraum_keine_angabe: false,
  tatort: '',
  gewalt_notizen: '',
})

const selectedArt = ref(null)
const andereDetails = ref('')
const fallArten = ref([])

const selectedFolgenCategory = ref(null)
const selectedFolgenSub = ref([])
const fallFolgenInfo = reactive({})
const fallFolgen = ref([])

const addGewalttatArt = () => {
  if (!selectedArt.value) return
  if (fallArten.value.find(f => f.id === selectedArt.value.id)) return

  fallArten.value.push({
    id: selectedArt.value.id,
    name: selectedArt.value.label,
    details: selectedArt.value.label === 'ANDERE' ? andereDetails.value : ''
  })

  selectedArt.value = null
  andereDetails.value = ''
}

const removeGewalttatArt = (id) => {
  fallArten.value = fallArten.value.filter(f => f.id !== id)
}

const getSubOptions = (categoryValue) => {
  const cat = FOLGE_DER_GEWAELT_CHOICES.find(c => c.value === categoryValue)
  if (!cat) return []
  return cat.children ? cat.children.map(c => ({ label: c.label, value: c.value, hasFreeText: c.hasFreeText })) : []
}

const addFolgenToFall = () => {
  selectedFolgenSub.value.forEach(f => {
    if (!fallFolgen.value.find(ff => ff.value === f)) {
      const option = getSubOptions(selectedFolgenCategory.value).find(o => o.value === f)
      fallFolgen.value.push({
        value: f,
        label: option.label,
        info: fallFolgenInfo[f] || ''
      })
    }
  })
  selectedFolgenSub.value = []
  selectedFolgenCategory.value = null
  Object.keys(fallFolgenInfo).forEach(k => fallFolgenInfo[k] = '')
}

const removeFallFolge = (value) => {
  fallFolgen.value = fallFolgen.value.filter(f => f.value !== value)
}

const onSubmit = async () => {
  if (!(await form.value.validate())) return
  try {
    const response = await api.post('/fall/create/', formData)
    const fallId = response.id

    for (const f of fallArten.value) {
      await api.post(`/gewalttatarten/`, { art: f.id, details: f.details })
    }
    for (const f of fallFolgen.value) {
      await api.post(`/fall/${fallId}/folgen/`, { folge: f.value, info: f.info })
    }
    form.value.$q.notify({ type: 'positive', message: 'Fall gespeichert!' })
    onReset()
  } catch (err) {
    console.error(err)
    form.value.$q.notify({ type: 'negative', message: 'Fehler beim Speichern!' })
  }
}

const onReset = () => {
  Object.keys(formData.value).forEach(k => {
    if (typeof formData.value[k] === 'boolean') formData.value[k] = false
    else if (typeof formData.value[k] === 'number') formData.value[k] = 0
    else formData.value[k] = ''
  })
  fallFolgen.value = []
}

// Flatten main + subcategories for Quasar select
const folgenOptions = FOLGE_DER_GEWAELT_CHOICES.flatMap(c => 
  c.children
    ? c.children.map(sub => ({ label: `${c.label} → ${sub.label}`, value: sub.value }))
    : { label: c.label, value: c.value }
)

</script>
