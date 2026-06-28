# Metadata API in Next.js

## Definition

The **Metadata API** in Next.js provides a systematic way to define and manage metadata for your pages, including titles, descriptions, Open Graph images, Twitter cards, and structured data. It supports both static metadata via `metadata` export and dynamic metadata via `generateMetadata`.

## Why Do We Need It?

1. **SEO** — Proper meta tags improve search engine rankings

2. **Social sharing** — Open Graph and Twitter cards control how links appear

3. **Accessibility** — Proper document structure helps screen readers

4. **Branding** — Consistent titles and descriptions across pages

5. **Analytics** — Proper metadata enables tracking and attribution

## How It Works

### Metadata Resolution Flow

```text
┌─────────────────────────────────────────────────────────────────┐
│                    METADATA RESOLUTION                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Layout metadata                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  app/layout.tsx                                          │   │
│  │  export const metadata = { title: 'My App' }            │   │
│  └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼                                                        │
│  Page metadata (extends layout)                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  app/about/page.tsx                                      │   │
│  │  export const metadata = { title: 'About' }             │   │
│  │  → Final title: "About | My App"                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼                                                        │
│  Dynamic metadata (overrides static)                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  app/blog/[slug]/page.tsx                                │   │
│  │  export async function generateMetadata({ params }) {   │   │
│  │    return { title: post.title }                          │   │
│  │  }                                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

### Metadata Types

```text
┌─────────────────────────────────────────────────────────────────┐
│                    METADATA TYPES                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Basic Meta:                                                    │
│  ├─ title                                                      │
│  ├─ description                                                 │
│  ├─ keywords                                                    │
│  ├─ authors                                                     │
│  └─ robots                                                      │
│                                                                 │
│  Open Graph:                                                    │
│  ├─ og:title                                                    │
│  ├─ og:description                                              │
│  ├─ og:image                                                    │
│  ├─ og:url                                                      │
│  ├─ og:type                                                     │
│  └─ og:site_name                                                │
│                                                                 │
│  Twitter:                                                       │
│  ├─ twitter:card                                                │
│  ├─ twitter:title                                               │
│  ├─ twitter:description                                         │
│  └─ twitter:image                                               │
│                                                                 │
│  Other:                                                         │
│  ├─ canonical                                                   │
│  ├─ icons                                                       │
│  ├─ manifest                                                    │
│  └─ other (custom)                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Static Metadata

```tsx
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My Application',
  description: 'A modern web application built with Next.js',
  keywords: ['nextjs', 'react', 'webapp'],
  authors: [{ name: 'John Doe' }],
  robots: {
    index: true,
    follow: true,
  },
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

```

### Page-Specific Metadata

```tsx
// app/about/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company and mission',
}

export default function AboutPage() {
  return (
    <div>
      <h1>About Us</h1>
      <p>We are a company that...</p>
    </div>
  )
}

```

### Open Graph Metadata

```tsx
// app/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Home',
  description: 'Welcome to our application',
  openGraph: {
    title: 'My Application',
    description: 'A modern web application',
    url: 'https://example.com',
    siteName: 'My App',
    images: [
      {
        url: 'https://example.com/og-image.png',
        width: 1200,
        height: 630,
        alt: 'My Application',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
}

```

### Twitter Card Metadata

```tsx
// app/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Home',
  twitter: {
    card: 'summary_large_image',
    title: 'My Application',
    description: 'A modern web application',
    images: ['https://example.com/twitter-image.png'],
    creator: '@username',
  },
}

```

### Dynamic Metadata with generateMetadata

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'

interface Post {
  title: string
  excerpt: string
  coverImage: string
  publishedAt: string
  author: string
}

async function getPost(slug: string): Promise<Post> {
  const res = await fetch(`https://api.example.com/posts/${slug}`)
  return res.json()
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>
}): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
      type: 'article',
      publishedTime: post.publishedAt,
      authors: [post.author],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  }
}

export default async function BlogPost({ params }) {
  const { slug } = await params
  const post = await getPost(slug)

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.excerpt}</p>
    </article>
  )
}

```

### Template Titles

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    default: 'My Application',
    template: '%s | My Application',
    absolute: 'My Application',
  },
}

// app/about/page.tsx
export const metadata: Metadata = {
  title: 'About', // Renders as "About | My Application"
}

```

### Canonical URLs

```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)

  return {
    title: post.title,
    alternates: {
      canonical: `https://example.com/blog/${slug}`,
    },
  }
}

```

### Multi-Language Metadata

```tsx
// app/[locale]/layout.tsx
export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>
}): Promise<Metadata> {
  const { locale } = await params

  return {
    title: locale === 'en' ? 'Home' : locale === 'es' ? 'Inicio' : 'Accueil',
    description:
      locale === 'en'
        ? 'Welcome to our app'
        : locale === 'es'
        ? 'Bienvenido a nuestra aplicación'
        : 'Bienvenue dans notre application',
    alternates: {
      languages: {
        'en': '/en',
        'es': '/es',
        'fr': '/fr',
      },
    },
  }
}

```

### Icons and Manifest

```tsx
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
    other: {
      rel: 'apple-touch-icon-precomposed',
      url: '/apple-touch-icon-precomposed.png',
    },
  },
  manifest: '/manifest.json',
}

```

### Structured Data (JSON-LD)

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }) {
  const { slug } = await params
  const post = await getPost(slug)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    description: post.excerpt,
    image: post.coverImage,
    datePublished: post.publishedAt,
    author: {
      '@type': 'Person',
      name: post.author,
    },
  }

  return (
    <article>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <h1>{post.title}</h1>
      <p>{post.excerpt}</p>
    </article>
  )
}

```

### Product Structured Data

```tsx
// app/products/[id]/page.tsx
export default async function ProductPage({ params }) {
  const { id } = await params
  const product = await getProduct(id)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.images,
    sku: product.sku,
    brand: {
      '@type': 'Brand',
      name: product.brand,
    },
    offers: {
      '@type': 'Offer',
      url: `https://example.com/products/${product.id}`,
      priceCurrency: 'USD',
      price: product.price,
      availability: 'https://schema.org/InStock',
    },
  }

  return (
    <div>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <h1>{product.name}</h1>
      <p>${product.price}</p>
    </div>
  )
}

```

### Breadcrumb Structured Data

```tsx
// components/breadcrumb.tsx
interface BreadcrumbItem {
  name: string
  url: string
}

export function Breadcrumb({ items }: { items: BreadcrumbItem[] }) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <nav aria-label="Breadcrumb">
        <ol>
          {items.map((item, index) => (
            <li key={item.url}>
              {index < items.length - 1 ? (
                <a href={item.url}>{item.name}</a>
              ) : (
                <span>{item.name}</span>
              )}
            </li>
          ))}
        </ol>
      </nav>
    </>
  )
}

```

### robots.txt Generation

```tsx
// app/robots.ts
import type { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin', '/api'],
      },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  }
}

```

### Sitemap Generation

```tsx
// app/sitemap.ts
import type { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await fetch('https://api.example.com/posts').then(res =>
    res.json()
  )

  const postEntries = posts.map(post => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }))

  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: 'https://example.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    ...postEntries,
  ]
}

```

### Metadata Base URL

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
  title: 'My Application',
  openGraph: {
    title: 'My Application',
    images: ['/og-image.png'], // Resolves to https://example.com/og-image.png
  },
}

```

## Real-World Use Cases

| Use Case | Metadata Type |
|----------|--------------|
| Blog posts | Dynamic OG, Twitter, structured data |
| E-commerce products | Product schema, OG images |
| Landing pages | Custom title, description, OG |
| Documentation | Canonical URLs, breadcrumbs |
| News articles | Article schema, AMP metadata |
| Social sharing | OG and Twitter cards |
| SEO optimization | Robots, sitemap, canonical |

## Common Mistakes

### 1. Not Using metadataBase

```tsx
// ❌ BAD: Relative URLs won't work
export const metadata: Metadata = {
  openGraph: {
    images: ['/og-image.png'], // Won't resolve properly
  },
}

// ✅ GOOD: Use metadataBase
export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
  openGraph: {
    images: ['/og-image.png'], // Resolves to full URL
  },
}

```

### 2. Duplicate Titles

```tsx
// ❌ BAD: Layout and page both define title
// app/layout.tsx
export const metadata: Metadata = { title: 'My App' }

// app/about/page.tsx
export const metadata: Metadata = { title: 'About | My App' } // Duplicates!

// ✅ GOOD: Use template in layout
// app/layout.tsx
export const metadata: Metadata = {
  title: { template: '%s | My App', default: 'My App' },
}

// app/about/page.tsx
export const metadata: Metadata = { title: 'About' } // Just the unique part

```

### 3. Missing OG Images

```tsx
// ❌ BAD: No OG image defined
export const metadata: Metadata = {
  title: 'My Page',
  openGraph: {
    title: 'My Page',
    // No image defined!
  },
}

// ✅ GOOD: Always include OG image
export const metadata: Metadata = {
  title: 'My Page',
  openGraph: {
    title: 'My Page',
    images: [
      {
        url: 'https://example.com/og-image.png',
        width: 1200,
        height: 630,
        alt: 'My Page',
      },
    ],
  },
}

```

### 4. Not Generating Dynamic Metadata

```tsx
// ❌ BAD: Static metadata for dynamic content
// app/blog/[slug]/page.tsx
export const metadata: Metadata = {
  title: 'Blog Post', // Same for every post!
  description: 'Read our blog post',
}

// ✅ GOOD: Generate metadata dynamically
export async function generateMetadata({ params }) {
  const post = await getPost(params.slug)
  return {
    title: post.title,
    description: post.excerpt,
  }
}

```

### 5. Ignoring Mobile Metadata

```tsx
// ❌ BAD: Only desktop dimensions
export const metadata: Metadata = {
  openGraph: {
    images: [
      {
        url: 'https://example.com/og.png',
        width: 1200,
        height: 630,
        // No alternative for mobile!
      },
    ],
  },
}

// ✅ GOOD: Include mobile-friendly images
export const metadata: Metadata = {
  openGraph: {
    images: [
      {
        url: 'https://example.com/og-desktop.png',
        width: 1200,
        height: 630,
      },
      {
        url: 'https://example.com/og-mobile.png',
        width: 600,
        height: 314,
      },
    ],
  },
}

```

## Best Practices

1. **Use metadataBase** — Always define for proper URL resolution

2. **Use templates** — Consistent title formatting across pages

3. **Generate dynamic metadata** — For dynamic content pages

4. **Include OG images** — Essential for social sharing

5. **Add structured data** — For rich search results

6. **Generate sitemaps** — Help search engines discover pages

7. **Define robots.txt** — Control crawling behavior

8. **Test metadata** — Use Open Graph debugger tools

9. **Keep descriptions concise** — 150-160 characters optimal
10. **Update metadata** — Keep metadata fresh with content changes

## Performance Considerations

```text
Metadata Performance:

- Static metadata: No runtime cost
- Dynamic metadata: Async data fetching
- generateMetadata: Cached per request
- Structured data: Minimal impact

Optimization:

- Use static metadata when possible
- Cache generateMetadata results
- Minimize structured data size
- Pre-generate metadata for popular pages

```

## Interview Questions

### Beginner (5-10)

1. **What is the Metadata API in Next.js?**
   The Metadata API provides a way to define and manage metadata for pages, including titles, descriptions, Open Graph tags, and structured data.

2. **What is the difference between static and dynamic metadata?**
   Static metadata is defined as a constant export. Dynamic metadata uses `generateMetadata` to compute metadata based on request parameters.

3. **How do you define metadata for a page?**
   Export a `metadata` object or `generateMetadata` function from the page file.

4. **What is Open Graph metadata?**
   Open Graph metadata controls how your page appears when shared on social media (Facebook, LinkedIn, etc.) with title, description, and image.

5. **How do you add structured data to a page?**
   Add a `<script type="application/ld+json">` tag with JSON-LD formatted structured data.

6. **What is a metadata template?**
   A template in layout metadata defines a pattern for page titles, like `%s | My App`, where `%s` is replaced by the page title.

7. **How do you generate a sitemap in Next.js?**
   Create a `sitemap.ts` file that exports a function returning an array of URLs with metadata.

8. **What is metadataBase?**
   The base URL used to resolve relative URLs in metadata, like OG images. It ensures proper absolute URLs.

### Intermediate (5-10)

9. **How do you handle metadata for dynamic routes?**
   Use `generateMetadata` with params to fetch data and return appropriate metadata for each dynamic page.

10. **How do you add Twitter card metadata?**
    Use the `twitter` property in metadata to define card type, title, description, and images.

11. **How do you handle multi-language metadata?**
    Use `generateMetadata` with locale params and `alternates.languages` to define language-specific metadata.

12. **What is canonical URL and why is it important?**
    A canonical URL tells search engines the preferred version of a page, preventing duplicate content issues.

13. **How do you add robots metadata?**
    Use the `robots` property to control indexing and following behavior for search engines.

14. **How do you add icons to your app?**
    Use the `icons` property in metadata to define favicons, Apple touch icons, and other icons.

15. **How do you handle metadata for nested layouts?**
    Each layout can define metadata that extends parent layouts. Page metadata overrides layout metadata.

### Senior (10-15)

16. **Design a comprehensive SEO strategy using Next.js Metadata API.**
    Implement dynamic metadata for all pages, add structured data, generate sitemaps, optimize OG images, and monitor search performance.

17. **How would you implement automated OG image generation?**
    Use Vercel OG or Sharp to generate images dynamically based on page content, and cache them for performance.

18. **Explain the relationship between Metadata API and Core Web Vitals.**
    Proper metadata improves SEO ranking factors, which correlate with Core Web Vitals. Good metadata also improves click-through rates.

19. **How do you handle metadata for large-scale applications?**
    Use templates, generate metadata from CMS data, implement metadata caching, and validate metadata programmatically.

20. **Design a metadata validation system.**
    Create schemas for metadata, validate at build time, test with social media debuggers, and monitor for metadata issues.

21. **How would you implement metadata for an e-commerce platform?**
    Generate product schema, dynamic OG images with product photos, price information, and availability status.

22. **Design a metadata management system for a CMS.**
    Create metadata templates, auto-generate from content, allow custom overrides, and validate before publishing.

23. **How do you handle metadata for internationalized applications?**
    Use hreflang tags, locale-specific metadata, and country-targeted content with proper canonical URLs.

24. **Design a system for A/B testing metadata.**
    Generate variant-specific metadata, track performance by variant, and implement statistical significance testing.

25. **How would you implement metadata analytics?**
    Track metadata changes, monitor search performance, measure social sharing metrics, and alert on metadata issues.

### FAANG-style (5-10)

26. **Design a metadata system for millions of pages.**
    Use static generation for popular pages, dynamic generation for long-tail, implement metadata caching, and optimize for crawl budget.

27. **How would you implement machine learning for metadata optimization?**
    Use ML to generate titles/descriptions, predict click-through rates, optimize for search intent, and A/B test results.

28. **Design a metadata pipeline for real-time content.**
    Stream metadata updates, implement cache invalidation, handle breaking news metadata, and ensure freshness.

29. **How would you implement metadata at global scale?**
    Use CDN caching, implement regional metadata, handle timezone differences, and optimize for local search.

30. **Design a metadata system with privacy compliance.**
    Implement GDPR-compliant metadata, handle consent-based tracking, and respect user privacy preferences.

### Follow-ups (5-10)

31. **What are the limitations of the Metadata API?**
    Dynamic metadata requires server-side execution, some properties are browser-dependent, and structured data validation is manual.

32. **How does Metadata API affect performance?**
    Static metadata has no impact. Dynamic metadata adds server-side execution time. Structured data adds minimal payload.

33. **What is the future of the Metadata API?**
    Better validation tools, automated optimization, AI-generated metadata, and improved social media integration.

34. **How do you test metadata?**
    Use Open Graph debugger, Google Rich Results Test, validate structured data, and check social media previews.

35. **What security considerations apply to metadata?**
    Never expose sensitive information, validate metadata inputs, and sanitize user-generated metadata.

36. **How do you handle metadata for single-page applications?**
    Use the Metadata API for initial load, implement dynamic metadata updates with useEffect, and handle client-side routing.

37. **What are alternatives to the Metadata API?**
    Next/head component (deprecated), manual HTML meta tags, and third-party SEO libraries.

38. **How do you monitor metadata in production?**
    Track metadata changes, monitor search console, test with validation tools, and set up alerts for issues.

## Summary

| Feature | Metadata API |
|---------|-------------|
| Static | `export const metadata = {...}` |
| Dynamic | `export async function generateMetadata()` |
| Basic | title, description, keywords |
| Open Graph | og:title, og:description, og:image |
| Twitter | twitter:card, twitter:title, twitter:image |
| Structured | JSON-LD in script tags |
| Sitemap | `sitemap.ts` export |
| Robots | `robots.ts` export |

## Cheat Sheet

```yaml
Static metadata:
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
}

Dynamic metadata:
export async function generateMetadata({ params }): Promise<Metadata> {
  const data = await fetchData(params.id)
  return { title: data.title }
}

Layout template:
title: { template: '%s | MyApp', default: 'MyApp' }

Structured data:
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }} />

Sitemap:
export default function sitemap(): MetadataRoute.Sitemap { [...] }

Robots:
export default function robots(): MetadataRoute.Robots { [...] }

```

## References & Learn More

- [Next.js Docs: Metadata](https://nextjs.org/docs/app/building-your-application/optimizing/metadata)
- [generateMetadata API](https://nextjs.org/docs/app/api-reference/functions/generate-metadata)
- [OpenGraph and Twitter Cards](https://nextjs.org/docs/app/building-your-application/optimizing/metadata#open-graph-and-twitter-cards)
