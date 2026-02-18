<template>
  <q-layout view="lHh Lpr lFf">


    <!-- DRAWER / SIDEBAR -->
    <q-drawer show-if-above side="left" bordered>
      <q-list padding>

        

        <!-- Fälle -->
        <q-item clickable to="/faelle">
          <q-item-section>Fälle</q-item-section>
        </q-item>

        <!-- Neuen Fall erstellen -->
        <q-item clickable to="/faelle/neu">
          <q-item-section>Neuen Fall erstellen</q-item-section>
        </q-item>

        <!-- Neue Anfrage erstellen -->
        <q-item clickable to="/anfragen/neu">
          <q-item-section>Neue Anfrage erstellen</q-item-section>
        </q-item>

        <!-- Benutzerverwaltung -->
        <q-item clickable to="/users">
          <q-item-section>Benutzer</q-item-section>
        </q-item>

        <!-- Statistiken -->
        <q-item clickable to="/statistics">
          <q-item-section>Statistiken</q-item-section>
        </q-item>

      </q-list>
    </q-drawer>

    <!-- PAGE CONTAINER -->
    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script setup>
</script>
