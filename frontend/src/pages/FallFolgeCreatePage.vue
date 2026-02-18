<template>
  <q-page padding>
    <!-- Header -->
    <div class="row items-center justify-between q-mb-md">
      <h1>{{ action }} Folge der Gewalt</h1>
      <q-btn flat label="Zurück zum Fall" :to="`/fall/${fallId}`" color="secondary" />
    </div>

    <!-- Fall Info -->
    <q-card flat bordered class="q-pa-md q-mb-md">
      <div>
        <strong>Fall:</strong> {{ fall.alias }} ({{ fall.beratungsstelle }})
      </div>
    </q-card>

    <!-- No available folgen alert -->
    <q-banner v-if="noAvailableFolgen" color="amber-3" text-color="amber-10">
      ℹ️ Alle Folgen bereits verknüpft. Sie können bestehende Verknüpfungen bearbeiten oder löschen.
      <q-btn flat label="Zurück zum Fall" :to="`/fall/${fallId}`" class="q-ml-md" color="secondary" />
    </q-banner>

    <!-- Form -->
    <q-form v-else ref="formRef" @submit.prevent="submitForm">
      <!-- Folge selection -->
      <q-select
        v-model="form.folge"
        :options="availableFolgen"
        label="Folge der Gewalt *"
        emit-value
        map-options
        :rules="[val => !!val || 'Bitte eine Folge auswählen']"
        filled
        class="q-mb-md"
      />

      <!-- Weitere Informationen -->
      <q-input
        v-model="form.weitere_informationen"
        type="textarea"
        label="Weitere Informationen"
        filled
        class="q-mb-md"
      />

      <!-- Buttons -->
      <div class="row q-gutter-sm">
        <q-btn type="submit" label="Speichern" color="primary" />
        <q-btn
          v-if="action === 'Hinzufügen'"
          label="Speichern & Weitere hinzufügen"
          color="positive"
          @click="saveAndAddAnother"
        />
        <q-btn flat label="Abbrechen" :to="`/fall/${fallId}`" color="secondary" />
      </div>
    </q-form>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { api } from 'src/services/api'  // your service for API calls

const $q = useQuasar()

// Route param or props
const fallId = ref('') // fill from router: const route = useRoute(); fallId.value = route.params.fallId

const action = ref('Hinzufügen') // or 'Bearbeiten'

const fall = ref({
  alias: '',
  beratungsstelle: '',
  folgen: []
})

const allFolgen = ref([])  // all possible Folgen from API
const availableFolgen = ref([])

const noAvailableFolgen = ref(false)

// Form data
const formRef = ref(null)
const form = ref({
  folge: null,
  weitere_informationen: ''
})

// Load Fall info & Folgen
const fetchFall = async () => {
  try {
    const { data } = await api.get(`/fall/${fallId.value}`)
    fall.value.alias = data.personenbezogene_daten.alias
    fall.value.beratungsstelle = data.zustaendige_beratungsstelle_display
    fall.value.folgen = data.folgen.map(f => f.id)
  } catch (err) {
    $q.notify({ type: 'negative', message: 'Fehler beim Laden des Falls' })
  }
}

const fetchFolgen = async () => {
  try {
    const { data } = await api.get('/folgen/')
    allFolgen.value = data
    filterAvailableFolgen()
  } catch (err) {
    $q.notify({ type: 'negative', message: 'Fehler beim Laden der Folgen' })
  }
}

const filterAvailableFolgen = () => {
  availableFolgen.value = allFolgen.value.filter(
    f => !fall.value.folgen.includes(f.id)
  )
  noAvailableFolgen.value = availableFolgen.value.length === 0
}

onMounted(async () => {
  await fetchFall()
  await fetchFolgen()
})

// Submit handlers
const submitForm = async () => {
  try {
    await api.post(`/fall/${fallId.value}/folge/`, form.value)
    $q.notify({ type: 'positive', message: 'Folge gespeichert!' })
    // Optionally redirect
    window.location.href = `/fall/${fallId.value}`
  } catch (err) {
    $q.notify({ type: 'negative', message: 'Fehler beim Speichern!' })
  }
}

const saveAndAddAnother = async () => {
  try {
    await api.post(`/fall/${fallId.value}/folge/`, form.value)
    $q.notify({ type: 'positive', message: 'Folge gespeichert!' })
    form.value.folge = null
    form.value.weitere_informationen = ''
    await fetchFall() // refresh linked folgen
    filterAvailableFolgen()
  } catch (err) {
    $q.notify({ type: 'negative', message: 'Fehler beim Speichern!' })
  }
}
</script>
