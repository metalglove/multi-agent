<template>
  <div class="markdown-renderer" :class="{ 'dark-mode': isDarkMode }">
    <template v-if="content">
      <div v-html="renderedHtml"></div>
    </template>
    <template v-else>
      <span class="text-muted">No content</span>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { renderMarkdown } from '@/utils/markdown'

interface Props {
  content: string | null | undefined
  size?: 'sm' | 'md' | 'lg'
  isDarkMode?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  content: '',
  size: 'md',
  isDarkMode: false,
})

const renderedHtml = computed(() => renderMarkdown(props.content))
</script>

<style scoped>
.markdown-renderer {
  line-height: 1.6;
  color: #333;
  word-break: break-word;
  font-size: 0.95rem;
}

.markdown-renderer.dark-mode {
  color: #e0e0e0;
}

/* Headings */
.markdown-renderer :deep(h1),
.markdown-renderer :deep(h2),
.markdown-renderer :deep(h3),
.markdown-renderer :deep(h4),
.markdown-renderer :deep(h5),
.markdown-renderer :deep(h6) {
  margin: 0.75rem 0 0.5rem 0;
  font-weight: 700;
  line-height: 1.4;
  letter-spacing: -0.01em;
}

.markdown-renderer :deep(h1) {
  font-size: 1.75rem;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 0.5rem;
}

.markdown-renderer.dark-mode :deep(h1) {
  border-bottom-color: #444;
}

.markdown-renderer :deep(h2) {
  font-size: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 0.3rem;
}

.markdown-renderer.dark-mode :deep(h2) {
  border-bottom-color: #333;
}

.markdown-renderer :deep(h3) {
  font-size: 1.25rem;
}

.markdown-renderer :deep(h4) {
  font-size: 1.1rem;
}

.markdown-renderer :deep(h5),
.markdown-renderer :deep(h6) {
  font-size: 1rem;
}

/* Paragraphs */
.markdown-renderer :deep(p) {
  margin: 0.75rem 0;
}

/* Lists */
.markdown-renderer :deep(ul),
.markdown-renderer :deep(ol) {
  margin: 0.75rem 0;
  padding-left: 2rem;
}

.markdown-renderer :deep(li) {
  margin: 0.35rem 0;
  line-height: 1.7;
}

.markdown-renderer :deep(ul > li::marker) {
  color: #667eea;
  font-weight: 600;
}

.markdown-renderer :deep(ol > li::marker) {
  color: #667eea;
  font-weight: 600;
}

.markdown-renderer :deep(li > p) {
  margin: 0.25rem 0;
}

/* Inline Code */
.markdown-renderer :deep(code) {
  background: #f5f5f5;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.85rem;
  color: #d63384;
  border: 1px solid #e9ecef;
}

.markdown-renderer.dark-mode :deep(code) {
  background: #2d2d2d;
  color: #ff7b72;
  border-color: #444;
}

/* Code Blocks */
.markdown-renderer :deep(pre) {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  margin: 1rem 0;
  border-left: 4px solid #667eea;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.markdown-renderer.dark-mode :deep(pre) {
  background: #1e1e1e;
  border-left-color: #764ba2;
}

.markdown-renderer :deep(pre code) {
  background: none;
  padding: 0;
  border: none;
  color: #333;
  font-size: 0.9rem;
  line-height: 1.5;
}

.markdown-renderer.dark-mode :deep(pre code) {
  color: #e0e0e0;
}

/* Blockquotes */
.markdown-renderer :deep(blockquote) {
  border-left: 4px solid #667eea;
  padding-left: 1rem;
  margin: 1rem 0;
  color: #666;
  font-style: italic;
  background: #f9f9f9;
  padding: 0.75rem 1rem;
  border-radius: 4px;
}

.markdown-renderer.dark-mode :deep(blockquote) {
  background: #2d2d2d;
  color: #b0b0b0;
  border-left-color: #764ba2;
}

.markdown-renderer :deep(blockquote > p) {
  margin: 0.5rem 0;
}

/* Links */
.markdown-renderer :deep(a) {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
  border-bottom: 1px dotted transparent;
}

.markdown-renderer :deep(a:hover) {
  color: #764ba2;
  border-bottom-color: #764ba2;
  text-decoration: underline;
}

.markdown-renderer.dark-mode :deep(a) {
  color: #90caf9;
}

.markdown-renderer.dark-mode :deep(a:hover) {
  color: #bbdefb;
  border-bottom-color: #bbdefb;
}

/* Horizontal rules */
.markdown-renderer :deep(hr) {
  border: none;
  border-top: 2px solid #e0e0e0;
  margin: 1.5rem 0;
}

.markdown-renderer.dark-mode :deep(hr) {
  border-top-color: #444;
}

/* Tables */
.markdown-renderer :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1rem 0;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.markdown-renderer.dark-mode :deep(table) {
  border-color: #444;
}

.markdown-renderer :deep(th),
.markdown-renderer :deep(td) {
  border: 1px solid #e0e0e0;
  padding: 0.75rem 1rem;
  text-align: left;
}

.markdown-renderer.dark-mode :deep(th),
.markdown-renderer.dark-mode :deep(td) {
  border-color: #444;
}

.markdown-renderer :deep(th) {
  background: #f8f9fa;
  font-weight: 700;
  color: #333;
}

.markdown-renderer.dark-mode :deep(th) {
  background: #2d2d2d;
  color: #e0e0e0;
}

.markdown-renderer :deep(tbody tr:nth-child(even)) {
  background: #f9f9f9;
}

.markdown-renderer.dark-mode :deep(tbody tr:nth-child(even)) {
  background: #1a1a1a;
}

/* Strong and emphasis */
.markdown-renderer :deep(strong),
.markdown-renderer :deep(b) {
  font-weight: 700;
  color: inherit;
}

.markdown-renderer :deep(em),
.markdown-renderer :deep(i) {
  font-style: italic;
}

/* Delete and insert (strikethrough/underline) */
.markdown-renderer :deep(del),
.markdown-renderer :deep(s) {
  text-decoration: line-through;
  opacity: 0.7;
}

.markdown-renderer :deep(ins),
.markdown-renderer :deep(u) {
  text-decoration: underline;
  text-decoration-color: #667eea;
}

/* Mark/highlight */
.markdown-renderer :deep(mark) {
  background: #fff3cd;
  padding: 0.1rem 0.3rem;
  border-radius: 2px;
}

.markdown-renderer.dark-mode :deep(mark) {
  background: #664d03;
}

/* Utilities */
.text-muted {
  color: #999;
  font-style: italic;
  font-size: 0.9rem;
}

.markdown-renderer.dark-mode .text-muted {
  color: #666;
}
</style>
