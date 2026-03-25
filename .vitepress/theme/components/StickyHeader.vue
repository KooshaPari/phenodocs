<<<<<<< HEAD
<script setup lang="ts">
import { useData } from 'vitepress'

const { frontmatter } = useData()
</script>

=======
>>>>>>> upstream/main
<template>
  <header class="sticky-header">
    <slot />
  </header>
</template>

<style scoped>
.sticky-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--vp-c-bg);
  border-bottom: 1px solid var(--vp-c-divider);
}
</style>
