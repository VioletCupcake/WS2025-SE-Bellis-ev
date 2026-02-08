<template>
  <q-page padding>
    <h4>Fall bearbeiten: {{ fall.alias }}</h4>

    <q-form @submit="saveFall" class="q-gutter-md">

      <!-- Beratungsstelle -->
      <q-select
        v-model="fall.zustaendige_beratungsstelle"
        :options="beratungsstelleOptions"
        label="Zuständige Beratungsstelle"
        outlined
      />

      <!-- Informationsquelle -->
      <q-select
        v-model="fall.informationsquelle"
        :options="informationsquelleOptions"
        label="Wie hat die Person von der Beratungsstelle erfahren?"
        outlined
        @update:model-value="toggleAndere"
      />

      <!-- ANDERE Details -->
      <q-input
        v-if="showAndere"
        v-model="fall.informationsquelle_andere_details"
        label="Details zur anderen Quelle"
        type="textarea"
        outlined
      />

      <q-separator spaced />

      <!-- Dolmetschungen -->
      <q-input
        v-model.number="fall.anzahl_dolmetschungen_stunden"
        label="Anzahl der Dolmetschungs-Stunden"
        type="number"
        step="0.5"
        min="0"
        outlined
      />

      <q-input
        v-model="fall.dolmetschung_sprachen"
        label="Dolmetschungs-Sprachen"
        type="textarea"
        outlined
      />

      <q-separator spaced />

      <!-- Weitere Notizen -->
      <q-input
        v-model="fall.weitere_notizen"
        label="Weitere Notizen"
        type="textarea"
        outlined
        autogrow
      />

      <!-- Buttons -->
      <div class="row q-gutter-sm">
        <q-btn label="Speichern" color="positive" type="submit" />
        <q-btn label="Abbrechen" color="secondary" flat @click="cancel" />
      </div>

    </q-form>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { api } from "src/services/api"
import { useQuasar } from "quasar"
import { useRoute, useRouter } from "vue-router"

const $q = useQuasar()
const route = useRoute()
const router = useRouter()

const fallId = route.params.id

const fall = ref({
  alias: "",
  zustaendige_beratungsstelle: "",
  informationsquelle: "",
  informationsquelle_andere_details: "",
  anzahl_dolmetschungen_stunden: 0,
  dolmetschung_sprachen: "",
  weitere_notizen: ""
})

const showAndere = ref(false)

const beratungsstelleOptions = [
  { label: "Fachberatungsstelle Leipzig", value: "FBS_1_LE" },
  { label: "Landkreis Nordsachsen", value: "FBS_2_LKNSA" },
  { label: "Landkreis Leipzig", value: "FBS_3_LKLE" }
]

const informationsquelleOptions = [
  { label: "Selbstmeldungen über Polizei", value: "POLIZEI" },
  { label: "Private Kontakte", value: "KONTAKTE" },
  { label: "Beratungsstellen", value: "BERATUNGSSTELLEN" },
  { label: "Internet", value: "INTERNET" },
  { label: "Ämter", value: "AEMTER" },
  { label: "Gesundheitswesen", value: "GESUNDHEITSWESEN" },
  { label: "Rechtsanwälte", value: "RECHTSANWAELTE" },
  { label: "Andere Quelle", value: "ANDERE" },
  { label: "Keine Angabe", value: "KEINE_ANGABE" }
]

function toggleAndere(value) {
  showAndere.value = value === "ANDERE"
}

async function loadFall() {
  try {
    const { data } = await api.get(`/fall/${fallId}`)
    fall.value = data
    toggleAndere(fall.value.informationsquelle)
  } catch {
    $q.notify({ type: "negative", message: "Fehler beim Laden des Falls" })
  }
}

async function saveFall() {
  try {
    await api.put(`/fall/${fallId}/`, fall.value)
    $q.notify({ type: "positive", message: "Fall gespeichert!" })
    router.push(`/fall/${fallId}`)
  } catch {
    $q.notify({ type: "negative", message: "Fehler beim Speichern!" })
  }
}

function cancel() {
  router.push(`/fall/${fallId}`)
}

onMounted(() => loadFall())
</script>
