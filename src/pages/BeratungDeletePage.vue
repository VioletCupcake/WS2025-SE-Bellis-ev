<template>
  <q-page padding>

    <!-- Title -->
    <h4>Beratung löschen</h4>

    <!-- Warning Box -->
    <q-banner class="bg-red-1 text-red-10 q-mb-md" rounded inline-actions>
      <div class="text-h6">⚠️ Bestätigung erforderlich</div>
      <div>Möchten Sie diese Beratung wirklich löschen?</div>
    </q-banner>

    <!-- Beratung Information -->
    <q-card flat bordered class="q-pa-md q-mb-md">
      <div class="text-h6 q-mb-sm">Beratungsinformationen</div>

      <q-markup-table separator="horizontal">
        <tbody>
          <tr>
            <td class="text-bold" style="width: 40%">Fall</td>
            <td>
              <q-btn
                flat
                dense
                color="primary"
                :label="fall.alias"
                @click="goToFall(fall.id)"
              />
            </td>
          </tr>

          <tr>
            <td class="text-bold">Datum</td>
            <td>{{ beratung.datum }}</td>
          </tr>

          <tr>
            <td class="text-bold">Durchführungsart</td>
            <td>{{ beratung.durchfuehrungsart }}</td>
          </tr>

          <tr>
            <td class="text-bold">Durchführungsort</td>
            <td>{{ beratung.durchfuehrungsort }}</td>
          </tr>

          <tr v-if="beratung.notizen">
            <td class="text-bold">Notizen</td>
            <td style="white-space: pre-wrap">{{ beratung.notizen }}</td>
          </tr>
        </tbody>
      </q-markup-table>
    </q-card>

    <!-- Info Note -->
    <q-banner class="bg-yellow-2 text-yellow-9 q-mb-lg" rounded>
      <strong>ℹ️ Hinweis:</strong>
      Nach dem Löschen wird die Anzahl der Beratungen für Fall
      "<strong>{{ fall.alias }}</strong>"
      aktualisiert. Diese Aktion kann nicht rückgängig gemacht werden.
    </q-banner>

    <!-- Action Buttons -->
    <div class="row q-gutter-sm">
      <q-btn color="red" label="Beratung löschen" @click="deleteBeratung" />
      <q-btn flat color="grey" label="Abbrechen" @click="goBack" />
    </div>
  </q-page>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import axios from 'axios'

const router = useRouter()

// Mock data — replace with real API calls
const fall = ref({
  id: 12,
  alias: "Mustermann"
})

const beratung = ref({
  datum: "12.01.2025",
  durchfuehrungsart: "Online",
  durchfuehrungsort: "Remote",
  notizen: "Lorem ipsum dolor sit amet..."
})

const deleteBeratung = async () => {
  try {
    await axios.delete(`/api/beratungen/${beratung.value.id}`)
    router.push(`/faelle/${fall.value.id}`)
  } catch (err) {
    console.error(err)
  }
}

const goToFall = (id) => {
  router.push(`/faelle/${id}`)
}

const goBack = () => {
  router.back()
}
</script>
