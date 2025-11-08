import { marked } from 'marked'

// Configure marked options for enhanced rendering
marked.setOptions({
  breaks: true,
  gfm: true, // GitHub-flavored markdown (tables, strikethrough, task lists, etc.)
  pedantic: false,
})

/**
 * Sanitize HTML to prevent XSS attacks
 * Removes dangerous tags and attributes
 */
function sanitizeHtml(html: string): string {
  try {
    const parser = new DOMParser()
    const doc = parser.parseFromString(html, 'text/html')
    
    // Remove script tags and style tags
    const scripts = doc.querySelectorAll('script, style')
    scripts.forEach(script => script.remove())
    
    // Remove event attributes
    doc.querySelectorAll('*').forEach(element => {
      Array.from(element.attributes).forEach(attr => {
        if (attr.name.toLowerCase().startsWith('on')) {
          element.removeAttribute(attr.name)
        }
      })
    })
    
    return doc.body.innerHTML
  } catch (error) {
    console.error('Error sanitizing HTML:', error)
    return escapeHtml(html)
  }
}

/**
 * Convert markdown text to HTML
 * Supports GitHub-flavored markdown with sanitization
 */
export function renderMarkdown(markdown: string | null | undefined): string {
  if (!markdown || typeof markdown !== 'string') return ''

  try {
    // Parse markdown to HTML
    let html = marked(markdown, { async: false }) as string
    
    // Sanitize the HTML
    html = sanitizeHtml(html)
    
    return html
  } catch (error) {
    console.error('Error rendering markdown:', error)
    // Return escaped plain text on error
    return escapeHtml(markdown)
  }
}

/**
 * Escape HTML special characters
 */
export function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;',
  }
  return text.replace(/[&<>"']/g, (char) => map[char])
}

/**
 * Truncate markdown text while preserving word boundaries
 * Adds ellipsis if truncated
 */
export function truncateMarkdown(markdown: string, maxLength: number = 200): string {
  if (markdown.length <= maxLength) return markdown
  
  // Truncate and find the last space to avoid breaking words
  const truncated = markdown.substring(0, maxLength)
  const lastSpace = truncated.lastIndexOf(' ')
  
  if (lastSpace > maxLength * 0.7) {
    // If last space is reasonably close, truncate there
    return truncated.substring(0, lastSpace) + '...'
  }
  
  // Otherwise just truncate at maxLength
  return truncated + '...'
}

/**
 * Extract plain text from markdown (removes formatting, links, etc.)
 * Useful for previews or summaries
 */
export function extractPlainText(markdown: string | null | undefined): string {
  if (!markdown) return ''
  
  return markdown
    .replace(/^#+\s+/gm, '') // Remove headings
    .replace(/\*\*(.+?)\*\*/g, '$1') // Remove bold
    .replace(/\*(.+?)\*/g, '$1') // Remove italic
    .replace(/\[(.+?)\]\(.+?\)/g, '$1') // Remove links
    .replace(/`(.+?)`/g, '$1') // Remove inline code
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/[_>~\-*|]/g, '') // Remove other markdown chars
    .trim()
}

/**
 * Check if markdown contains code blocks
 */
export function hasCodeBlocks(markdown: string | null | undefined): boolean {
  if (!markdown) return false
  return /```[\s\S]*?```/.test(markdown)
}

/**
 * Count the estimated lines when rendered
 * Useful for layout planning
 */
export function estimateRenderedLines(markdown: string | null | undefined): number {
  if (!markdown) return 0
  
  let estimate = 0
  
  markdown.split('\n').forEach(line => {
    if (line.match(/^#+\s+/)) estimate += 1.5 // Headings
    else if (line.match(/^```/)) estimate += 2 // Code block delimiter
    else if (line.match(/^- |^\* |^\d+\.|^\|/)) estimate += 0.8 // Lists/tables
    else if (line.trim()) estimate += 1
  })
  
  return Math.ceil(estimate)
}
