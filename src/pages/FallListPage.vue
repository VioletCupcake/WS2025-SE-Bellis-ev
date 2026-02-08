<template>
  <q-page padding>
    <div class="row items-center justify-between q-mb-md">
      <div class="text-h5">Fälle</div>
      <q-btn color="primary" label="Neuen Fall anlegen" to="/faelle/neu" />
    </div>

    <q-card>
      <q-card-section>
        <q-table
          :rows="faelle"
          :columns="columns"
          row-key="id"
          flat
          bordered
        >
          <template v-slot:body-cell-actions="props">
            <q-btn dense flat icon="visibility" color="primary"
                   :to="`/faelle/${props.row.id}/edit`" />
          </template>
        </q-table>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "src/services/api";

const faelle = ref([]);

const columns = [
  { name: "alias", label: "Alias", field: "alias", align: "left" },
  { name: "beratungsstelle", label: "Beratungsstelle", field: "zustaendige_beratungsstelle" },
  { name: "actions", label: "Aktionen", field: "actions" }
];

onMounted(async () => {
  const data = await api.get("/cases/");
  faelle.value = data;
});
</script>
