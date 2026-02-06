<template>
<q-layout view="lHh Lpr lFf">
<q-header elevated class="bg-primary text-white">
<q-toolbar>
<q-toolbar-title>Fall Manager</q-toolbar-title>
</q-toolbar>
</q-header>


<q-drawer show-if-above side="left" bordered>
<q-list>
<q-item clickable to="/faelle">
<q-item-section>Fälle</q-item-section>
</q-item>
<q-item clickable to="/faelle/neu">
<q-item-section>Neuen Fall erstellen</q-item-section>
</q-item>
</q-list>
</q-drawer>


<q-page-container>
<router-view />
</q-page-container>
</q-layout>
</template>


<script setup>
</script>