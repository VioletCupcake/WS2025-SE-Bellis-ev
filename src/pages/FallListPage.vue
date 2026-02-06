<template>
<q-page padding>
<h4>Fall-Liste</h4>
<q-table :rows="rows" :columns="columns" />
</q-page>
</template>


<script setup>
import { ref } from 'vue'
import { api } from 'boot/axios'


const rows = ref([])
const columns = [
{ name: 'id', label: 'ID', field: 'id' },
{ name: 'fallnummer', label: 'Fallnummer', field: 'fallnummer' },
{ name: 'datum', label: 'Datum', field: 'datum' }
]


api.get('/faelle').then(r => rows.value = r.data)
</script>