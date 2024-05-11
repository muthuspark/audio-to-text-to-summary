<template>
  <div class="container">
    <nav class="navbar">
      <div class="container">
        <ul class="navbar-list">
          <li class="navbar-item"><a class="navbar-link" href="#"><strong>Speech Synopsis</strong></a></li>
        </ul>
      </div>
    </nav>
    <main>
      <RouterView />
    </main>
    <vue3-confirm-dialog></vue3-confirm-dialog>
  </div>
</template>