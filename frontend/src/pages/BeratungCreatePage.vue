<template>
  <q-page padding class="q-pa-lg">

    <!-- HEADER BAR -->
    <div class="row items-center justify-between q-mb-lg">
      <h4>{{ action }} Beratung</h4>
      <q-btn
        label="Zurück zum Fall"
        color="secondary"
        @click="goBackToFall"
      />
    </div>

    <!-- FALL INFO -->
    <q-card flat bordered class="q-pa-md q-mb-lg bg-grey-2">
      <div>
        <strong>Fall:</strong>
        {{ fall.alias }} ({{ fall.beratungsstelle }})
      </div>
    </q-card>

    <!-- FORM -->
    <q-form @submit="submitForm">

      <!-- Datum -->
      <q-input
        v-model="form.datum"
        type="date"
        label="Datum der Beratung *"
        outlined
        class="q-mb-md"
        :error="!!errors.datum"
        :error-message="errors.datum"
      >
        <template #hint>
          Datum über Kalender-Widget auswählen oder eingeben
        </template>
      </q-input>

      <!-- Durchführungsart -->
      <q-select
        v-model="form.durchfuehrungsart"
        :options="durchfuehrungsarten"
        label="Durchführungsart *"
        outlined
        class="q-mb-md"
        :error="!!errors.durchfuehrungsart"
        :error-message="errors.durchfuehrungsart"
        hint="Persönlich, Video, Telefon, aufsuchend oder schriftlich"
      />

      <!-- Durchführungsort -->
      <q-select
        v-model="form.durchfuehrungsort"
        :options="durchfuehrungsorte"
        label="Durchführungsort *"
        outlined
        class="q-mb-md"
        :error="!!errors.durchfuehrungsort"
        :error-message="errors.durchfuehrungsort"
        hint="Leipzig Stadt, Leipzig Land oder Nordsachsen"
      />

      <!-- Weitere Notizen -->
      <q-input
        v-model="form.weitere_notizen"
        type="textarea"
        outlined
        label="Weitere Notizen"
        autogrow
        class="q-mb-lg"
        hint="Optionale Notizen zur Beratung"
      />

      <!-- Hinweis Info Box -->
      <q-banner class="bg-blue-1 text-blue-9 q-pa-md q-mb-xl">
        <div>
          <strong>ℹ Hinweis:</strong>  
          Nach dem Speichern wird die Anzahl der Beratungen automatisch aktualisiert.
        </div>
      </q-banner>

      <!-- ACTION BUTTONS -->
      <div class="row q-gutter-md">
        <q-btn
          label="Speichern"
          color="positive"
          type="submit"
        />
        <q-btn
          label="Abbrechen"
          color="secondary"
          outline
          @click="goBackToFall"
        />
      </div>

    </q-form>

    <!-- SHOW EXISTING BERATUNG (if editing) -->
    <div v-if="beratung" class="q-mt-xl">
      <q-separator spaced />

      <q-card flat bordered class="q-pa-lg bg-grey-1">
        <h5>Aktuelle Beratungsdaten</h5>

        <q-markup-table dense flat>
          <tbody>
            <tr>
              <th>Datum</th>
              <td>{{ beratung.datum }}</td>
            </tr>
            <tr>
              <th>Durchführungsart</th>
              <td>{{ beratung.durchfuehrungsart }}</td>
            </tr>
            <tr>
              <th>Durchführungsort</th>
              <td>{{ beratung.durchfuehrungsort }}</td>
            </tr>
            <tr v-if="beratung.weitere_notizen">
              <th>Notizen</th>
              <td style="white-space: pre-wrap;">
                {{ beratung.weitere_notizen }}
              </td>
            </tr>
          </tbody>
        </q-markup-table>
      </q-card>
    </div>

  </q-page>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";

export default {
  name: "BeratungCreatePage",

  setup() {
    const route = useRoute();
    const router = useRouter();

    const action = "Neue"; // "Neue Beratung" or "Beratung Bearbeiten"

    const fall = ref({
      alias: "",
      beratungsstelle: ""
    });

    const beratung = ref(null);

    const form = ref({
      datum: "",
      durchfuehrungsart: "",
      durchfuehrungsort: "",
      weitere_notizen: ""
    });

    const errors = ref({});

    const durchfuehrungsarten = [
      "Persönlich",
      "Video",
      "Telefon",
      "Aufsuchend",
      "Schriftlich"
    ];

    const durchfuehrungsorte = [
      "Leipzig Stadt",
      "Leipzig Land",
      "Nordsachsen"
    ];

    const goBackToFall = () => {
      router.push(`/fall/${route.params.fall_id}`);
    };

    const submitForm = async () => {
      errors.value = {};

      try {
        await axios.post("http://localhost:8000/api/beratung/create/", form.value);

        router.push(`/fall/${route.params.fall_id}`);

      } catch (error) {
        if (error.response?.data) {
          errors.value = error.response.data;
        }
      }
    };

    return {
      form,
      errors,
      beratung,
      fall,
      action,
      durchfuehrungsarten,
      durchfuehrungsorte,
      submitForm,
      goBackToFall
    };
  }
};
</script>
