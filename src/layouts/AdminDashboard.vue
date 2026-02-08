<template>
  <q-page padding class="bg-grey-1">
    <!-- Header -->
    <div class="text-center q-mb-xl">
      <h1 class="text-h3 q-mb-sm">Admin Dashboard</h1>
      <p class="text-subtitle2 text-grey-8">
        Volle Kontrolle über alle Module.
      </p>
    </div>

    <!-- Action Cards Grid -->
    <div class="row q-col-gutter-lg q-row-gutter-lg">
      <!-- Neue Anfrage -->
      <div class="col-12 col-sm-6 col-lg-3">
        <q-card
          flat bordered
          class="q-pa-md flex flex-col items-center hover-card cursor-pointer"
          @click="$router.push('/anfragen/neu')"
        >
          <q-icon name="add_circle" size="80px" class="text-primary q-mb-md"/>
          <div class="text-h6 q-mb-xs text-center">Neue Anfrage</div>
          <div class="text-subtitle2 text-center text-grey-7">
            Legen Sie eine neue Anfrage an.
          </div>
        </q-card>
      </div>

      <!-- Neuer Fall -->
      <div class="col-12 col-sm-6 col-lg-3">
        <q-card
          flat bordered
          class="q-pa-md flex flex-col items-center hover-card cursor-pointer"
          @click="$router.push('/faelle/neu')"
        >
          <q-icon name="folder" size="80px" class="text-primary q-mb-md"/>
          <div class="text-h6 q-mb-xs text-center">Neuer Fall</div>
          <div class="text-subtitle2 text-center text-grey-7">
            Erstellen Sie einen neuen Beratungsfall.
          </div>
        </q-card>
      </div>

      <!-- Alle Fälle -->
      <div class="col-12 col-sm-6 col-lg-3">
        <q-card
          flat bordered
          class="q-pa-md flex flex-col items-center hover-card cursor-pointer"
          @click="$router.push('/faelle')"
        >
          <q-icon name="people" size="80px" class="text-primary q-mb-md"/>
          <div class="text-h6 q-mb-xs text-center">Alle Fälle</div>
          <div class="text-subtitle2 text-center text-grey-7">
            Sehen und verwalten Sie alle Fälle.
          </div>
        </q-card>
      </div>

      <!-- Benutzerverwaltung -->
      <div class="col-12 col-sm-6 col-lg-3">
        <q-card
          flat bordered
          class="q-pa-md flex flex-col items-center hover-card cursor-pointer"
          @click="$router.push('/users')"
        >
          <q-icon name="manage_accounts" size="80px" class="text-primary q-mb-md"/>
          <div class="text-h6 q-mb-xs text-center">Users</div>
          <div class="text-subtitle2 text-center text-grey-7">
            Verwalten Sie Benutzer und Rollen.
          </div>
        </q-card>
      </div>

      <!-- Statistiken -->
      <div class="col-12 col-sm-6 col-lg-3">
        <q-card
          flat bordered
          class="q-pa-md flex flex-col items-center hover-card cursor-pointer"
          @click="$router.push('/statistics')"
        >
          <q-icon name="bar_chart" size="80px" class="text-primary q-mb-md"/>
          <div class="text-h6 q-mb-xs text-center">Statistiken</div>
          <div class="text-subtitle2 text-center text-grey-7">
            Relevante Statistiken und Reports abrufen.
          </div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
</script>

<style>
.hover-card:hover {
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
  transform: translateY(-4px);
  transition: all 0.2s ease-in-out;
}
</style>
