# Image Optimization in Next.js

## Definition

Next.js provides an **Image component** (`next/image`) that automatically optimizes images through lazy loading, format conversion (WebP/AVIF), responsive sizing, and blur placeholders. It prevents layout shift and improves Core Web Vitals.

## Why Do We Need It?

1. **Performance** — Optimized images load faster
2. **Core Web Vitals** — Better LCP, CLS, and FCP scores
3. **Bandwidth savings** — Automatic format optimization
4. **Responsive design** — Serve appropriate sizes for different devices
5. **User experience** — Blur placeholders and lazy loading

## How It Works

### Image Optimization Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                NEXT.JS IMAGE OPTIMIZATION                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Image Request                                               │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  <Image src="/photo.jpg" width={800} height={600} /> │    │
│     └─────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  2. Optimization (on-demand or at build)                        │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  - Resize to requested dimensions                    │    │
│     │  - Convert to optimal format (WebP/AVIF)            │    │
│     │  - Compress for web delivery                         │    │
│     │  - Generate responsive variants                      │    │
│     └─────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  3. Caching                                                      │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  - Cache optimized image on CDN                      │    │
│     │  - Serve from cache on subsequent requests           │    │
│     └─────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  4. Delivery                                                     │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  - Serve optimized image to browser                  │    │
│     │  - Use appropriate format for browser                │    │
│     │  - Lazy load if below fold                           │    │
│     └─────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Before vs After Optimization

```
┌─────────────────────────────────────────────────────────────────┐
│              WITHOUT NEXT.JS IMAGE                              │
├─────────────────────────────────────────────────────────────────┤
│  Original: photo.jpg (3.2MB, 4000x3000, JPEG)                  │
│                                                                 │
│  Browser receives:                                              │
│  - Full 3.2MB image                                             │
│  - No format optimization                                       │
│  - No lazy loading                                              │
│  - Layout shift possible                                        │
│                                                                 │
│  Result: Slow loading, high bandwidth, poor UX                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              WITH NEXT.JS IMAGE                                 │
├─────────────────────────────────────────────────────────────────┤
│  Original: photo.jpg (3.2MB, 4000x3000, JPEG)                  │
│                                                                 │
│  Optimized (desktop):                                           │
│  - photo.webp (120KB, 800x600)                                  │
│  - Lazy loaded                                                  │
│  - Blur placeholder shown                                       │
│                                                                 │
│  Optimized (mobile):                                            │
│  - photo.webp (60KB, 400x300)                                   │
│  - Responsive sizing                                             │
│  - AVIF if browser supports                                     │
│                                                                 │
│  Result: Fast loading, minimal bandwidth, great UX              │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Image Usage

```tsx
// app/page.tsx
import Image from 'next/image'

export default function Page() {
  return (
    <div>
      <h1>My Page</h1>
      <Image
        src="/hero.jpg"
        alt="Hero image"
        width={1200}
        height={600}
        priority
      />
    </div>
  )
}
```

### Remote Images

```tsx
// app/page.tsx
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="https://example.com/photo.jpg"
      alt="Remote image"
      width={800}
      height={600}
    />
  )
}
```

```tsx
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
      },
      {
        protocol: 'https',
        hostname: '*.amazonaws.com',
      },
    ],
  },
}
```

### Responsive Images

```tsx
// app/page.tsx
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero image"
      width={1200}
      height={600}
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      style={{ width: '100%', height: 'auto' }}
    />
  )
}
```

### Blur Placeholder

```tsx
// app/page.tsx
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="/photo.jpg"
      alt="Photo with blur"
      width={800}
      height={600}
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRg..."
    />
  )
}
```

### Auto Blur Placeholder

```tsx
// next.config.js
module.exports = {
  images: {
    minimumCacheTTL: 60 * 60 * 24 * 30, // 30 days
  },
}
```

```tsx
// app/page.tsx
import Image from 'next/image'
import heroImg from '@/public/hero.jpg'

export default function Page() {
  return (
    <Image
      src={heroImg}
      alt="Hero with auto blur"
      placeholder="blur"
      // blurDataURL is automatically generated for local images
    />
  )
}
```

### Lazy Loading

```tsx
// app/page.tsx
import Image from 'next/image'

export default function Page() {
  return (
    <div>
      {/* Above the fold - load immediately */}
      <Image
        src="/hero.jpg"
        alt="Hero"
        width={1200}
        height={600}
        priority
      />

      {/* Below the fold - lazy load */}
      <Image
        src="/content.jpg"
        alt="Content"
        width={800}
        height={600}
      />
    </div>
  )
}
```

### Fill Mode

```tsx
// app/page.tsx
import Image from 'next/image'

export default function Page() {
  return (
    <div style={{ position: 'relative', width: '100%', height: '400px' }}>
      <Image
        src="/photo.jpg"
        alt="Photo"
        fill
        style={{ objectFit: 'cover' }}
      />
    </div>
  )
}
```

### Image Gallery

```tsx
// components/image-gallery.tsx
import Image from 'next/image'

interface GalleryImage {
  src: string
  alt: string
  width: number
  height: number
}

export function ImageGallery({ images }: { images: GalleryImage[] }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {images.map((image, index) => (
        <div key={index} className="relative aspect-square">
          <Image
            src={image.src}
            alt={image.alt}
            fill
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            style={{ objectFit: 'cover' }}
            className="rounded-lg"
          />
        </div>
      ))}
    </div>
  )
}
```

### Avatar Component

```tsx
// components/avatar.tsx
import Image from 'next/image'

interface AvatarProps {
  src: string
  alt: string
  size?: 'sm' | 'md' | 'lg'
}

const sizeMap = {
  sm: 32,
  md: 48,
  lg: 64,
}

export function Avatar({ src, alt, size = 'md' }: AvatarProps) {
  const pixelSize = sizeMap[size]

  return (
    <div
      className="relative rounded-full overflow-hidden"
      style={{ width: pixelSize, height: pixelSize }}
    >
      <Image
        src={src}
        alt={alt}
        fill
        sizes={`${pixelSize}px`}
        style={{ objectFit: 'cover' }}
        className="rounded-full"
      />
    </div>
  )
}
```

### Hero Image with Overlay

```tsx
// components/hero.tsx
import Image from 'next/image'

export function Hero() {
  return (
    <div className="relative h-[600px] w-full">
      <Image
        src="/hero-bg.jpg"
        alt="Hero background"
        fill
        priority
        sizes="100vw"
        style={{ objectFit: 'cover' }}
        className="brightness-50"
      />
      <div className="absolute inset-0 flex items-center justify-center">
        <h1 className="text-white text-6xl font-bold">
          Welcome to Our Site
        </h1>
      </div>
    </div>
  )
}
```

### Product Image with Zoom

```tsx
// components/product-image.tsx
'use client'

import { useState } from 'react'
import Image from 'next/image'

export function ProductImage({ src, alt }: { src: string; alt: string }) {
  const [isZoomed, setIsZoomed] = useState(false)

  return (
    <div
      className="relative cursor-zoom-in"
      onMouseEnter={() => setIsZoomed(true)}
      onMouseLeave={() => setIsZoomed(false)}
    >
      <Image
        src={src}
        alt={alt}
        width={isZoomed ? 1600 : 800}
        height={isZoomed ? 1200 : 600}
        style={{
          objectFit: 'contain',
          transition: 'transform 0.3s',
          transform: isZoomed ? 'scale(1.5)' : 'scale(1)',
        }}
        priority
      />
    </div>
  )
}
```

### Responsive Background Image

```tsx
// components/section.tsx
import Image from 'next/image'

export function Section() {
  return (
    <section className="relative h-[500px]">
      <Image
        src="/section-bg.jpg"
        alt="Section background"
        fill
        sizes="100vw"
        style={{ objectFit: 'cover' }}
        priority
      />
      <div className="relative z-10 container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-white">Our Story</h2>
        <p className="text-white mt-4">Content goes here...</p>
      </div>
    </section>
  )
}
```

### Image with Loading States

```tsx
// components/image-with-loading.tsx
'use client'

import { useState } from 'react'
import Image from 'next/image'

export function ImageWithLoading({
  src,
  alt,
  width,
  height,
}: {
  src: string
  alt: string
  width: number
  height: number
}) {
  const [isLoading, setIsLoading] = useState(true)

  return (
    <div className="relative">
      {isLoading && (
        <div
          className="absolute inset-0 bg-gray-200 animate-pulse"
          style={{ width, height }}
        />
      )}
      <Image
        src={src}
        alt={alt}
        width={width}
        height={height}
        onLoadingComplete={() => setIsLoading(false)}
        className={isLoading ? 'opacity-0' : 'opacity-100'}
      />
    </div>
  )
}
```

### Next.js Image Configuration

```tsx
// next.config.js
module.exports = {
  images: {
    // Device sizes for responsive images
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],

    // Image sizes for srcset
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],

    // Allowed remote patterns
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],

    // Formats to use
    formats: ['image/avif', 'image/webp'],

    // Minimum cache TTL (seconds)
    minimumCacheTTL: 60 * 60 * 24 * 30, // 30 days

    // Disable static imports
    disableStaticImages: false,

    // Content security policy
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },
}
```

## Real-World Use Cases

| Use Case | Image Features |
|----------|---------------|
| Hero banners | Priority loading, fill mode, overlay |
| Product galleries | Responsive sizes, lazy loading |
| User avatars | Circular crop, multiple sizes |
| Blog posts | Blur placeholder, responsive |
| Social feeds | Lazy loading, aspect ratios |
| Background images | Fill mode, object-fit |
| Thumbnails | Small sizes, lazy loading |
| Full-screen images | High resolution, zoom |

## Common Mistakes

### 1. Not Setting Width and Height

```tsx
// ❌ BAD: Missing dimensions causes layout shift
<Image src="/photo.jpg" alt="Photo" />

// ✅ GOOD: Always set width and height
<Image src="/photo.jpg" alt="Photo" width={800} height={600} />
```

### 2. Using Priority on All Images

```tsx
// ❌ BAD: All images marked as priority
<Image src="/photo1.jpg" alt="1" width={800} height={600} priority />
<Image src="/photo2.jpg" alt="2" width={800} height={600} priority />
<Image src="/photo3.jpg" alt="3" width={800} height={600} priority />

// ✅ GOOD: Only above-the-fold images get priority
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />
<Image src="/content.jpg" alt="Content" width={800} height={600} />
```

### 3. Not Using Remote Patterns

```tsx
// ❌ BAD: Remote image not configured
<Image src="https://example.com/photo.jpg" alt="Photo" width={800} height={600} />
// Error: Invalid src prop

// ✅ GOOD: Configure remote patterns
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'example.com' },
    ],
  },
}
```

### 4. Ignoring Aspect Ratio

```tsx
// ❌ BAD: Incorrect aspect ratio
<Image src="/photo.jpg" alt="Photo" width={800} height={800} />
// Image will be stretched if original is not square

// ✅ GOOD: Match aspect ratio or use fill
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  style={{ objectFit: 'cover' }}
/>
```

### 5. Not Using Blur Placeholder

```tsx
// ❌ BAD: No loading placeholder
<Image src="/photo.jpg" alt="Photo" width={800} height={600} />
// Shows nothing while loading

// ✅ GOOD: Use blur placeholder
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

## Best Practices

1. **Always set width and height** — Prevents layout shift
2. **Use priority for above-the-fold images** — Improves LCP
3. **Implement blur placeholders** — Better loading experience
4. **Configure remote patterns** — For external images
5. **Use responsive sizes** — Serve appropriate sizes
6. **Lazy load below-the-fold images** — Save bandwidth
7. **Use fill mode for backgrounds** — For flexible layouts
8. **Optimize image formats** — Enable WebP/AVIF
9. **Test on different devices** — Verify responsive behavior
10. **Monitor image performance** — Track loading metrics

## Performance Considerations

```
Image Optimization Benefits:
- File size: 30-50% reduction with WebP/AVIF
- Lazy loading: Saves bandwidth for below-fold images
- Responsive sizing: Smaller images on mobile
- Blur placeholders: Better perceived performance
- CDN caching: Fast subsequent loads

Core Web Vitals Impact:
- LCP: Improved with priority loading
- CLS: Prevented with width/height
- FCP: Improved with lazy loading
```

## Interview Questions

### Beginner (5-10)

1. **What is the Next.js Image component?**
   A component that automatically optimizes images through lazy loading, format conversion, and responsive sizing.

2. **How do you use the Image component?**
   Import from `next/image`, provide src, alt, width, and height props.

3. **What is lazy loading?**
   Loading images only when they enter the viewport, saving bandwidth and improving initial load.

4. **What is the blur placeholder?**
   A low-quality image placeholder shown while the full image loads, improving perceived performance.

5. **Why do we need width and height?**
   To prevent layout shift by reserving space before the image loads.

6. **What is priority loading?**
   Loading images immediately without lazy loading, used for above-the-fold images.

7. **How do remote images work?**
   Configure allowed domains in `next.config.js` with `remotePatterns`.

8. **What formats does Next.js support?**
   WebP and AVIF for modern browsers, with JPEG/PNG fallback.

### Intermediate (5-10)

9. **How do you configure image optimization?**
   Use `next.config.js` with `images` property for device sizes, formats, and remote patterns.

10. **What is the fill mode?**
    A mode where the image fills its parent container, useful for responsive backgrounds.

11. **How do you handle responsive images?**
    Use `sizes` prop to define breakpoints and serve appropriate image sizes.

12. **What is the difference between priority and lazy loading?**
    Priority loads immediately, lazy loading defers until the image is in viewport.

13. **How do you optimize images for mobile?**
    Use responsive sizes, smaller dimensions for mobile, and appropriate quality settings.

14. **How do you handle image aspect ratios?**
    Use `objectFit` with `cover` or `contain`, or use `fill` mode with aspect ratio containers.

15. **What is CDN caching for images?**
    Optimized images are cached on the CDN, serving them faster on subsequent requests.

### Senior (10-15)

16. **Design an image optimization strategy for an e-commerce platform.**
    Use priority for product images, blur placeholders for galleries, responsive sizes for different devices, and CDN caching.

17. **How would you implement image optimization at scale?**
    Use Vercel Image Optimization or custom image processing pipeline, implement CDN caching, and monitor performance.

18. **Explain the image optimization pipeline.**
    Image request → Resize → Convert format → Compress → Cache → Deliver.

19. **How do you handle user-uploaded images?**
    Process on upload, generate multiple sizes, convert to WebP/AVIF, and store optimized versions.

20. **Design a system for dynamic image generation.**
    Use server-side image processing, generate thumbnails, create social media previews, and cache results.

21. **How would you implement image optimization for AMP pages?**
    Use AMP-compatible image formats, implement preloading, and follow AMP image guidelines.

22. **Explain the relationship between image optimization and Core Web Vitals.**
    Optimized images improve LCP (faster loading), CLS (no layout shift), and FCP (faster first paint).

23. **How do you handle images in Server Components?**
    Use the Image component normally, it works in both Server and Client Components.

24. **Design an image CDN architecture.**
    Implement edge caching, on-demand optimization, format negotiation, and responsive delivery.

25. **How would you implement image analytics?**
    Track loading performance, monitor format usage, measure bandwidth savings, and optimize based on data.

### FAANG-style (5-10)

26. **Design a global image optimization system.**
    Use edge computing, implement geo-distributed caching, handle format negotiation, and optimize for latency.

27. **How would you implement machine learning for image optimization?**
    Use ML for quality assessment, adaptive compression, content-aware cropping, and format selection.

28. **Design an image system for social media.**
    Generate platform-specific sizes, optimize for sharing, implement preview generation, and handle different formats.

29. **How would you implement image optimization for video thumbnails?**
    Extract frames, generate multiple thumbnails, optimize for preview, and cache results.

30. **Design a system for accessibility with images.**
    Implement alt text generation, provide text alternatives, ensure contrast, and support screen readers.

### Follow-ups (5-10)

31. **What are the limitations of Next.js Image component?**
    Requires width/height, remote images need configuration, and some features are Vercel-only.

32. **How does image optimization affect build time?**
    Local images are processed at build time, increasing build duration. Remote images are processed on-demand.

33. **What is the future of image optimization in Next.js?**
    Better format support, improved caching, and more configuration options.

34. **How do you test image optimization?**
    Use Lighthouse, check network tab for format, verify lazy loading, and test on different devices.

35. **What security considerations apply to images?**
    Validate remote URLs, prevent image-based attacks, and implement content security policy.

36. **How do you handle images in offline mode?**
    Cache images with Service Workers, implement fallback images, and handle network failures.

37. **What are alternatives to Next.js Image component?**
    HTML img tag, lazy loading libraries, and CDN image optimization services.

38. **How do you monitor image performance in production?**
    Track loading times, monitor format usage, measure bandwidth, and alert on issues.

## Summary

| Feature | Next.js Image |
|---------|--------------|
| Component | `next/image` |
| Lazy loading | Automatic (except priority) |
| Format | WebP/AVIF automatic |
| Responsive | Sizes prop |
| Blur | Placeholder prop |
| Fill | Fill mode for backgrounds |
| CDN | Automatic caching |

## Cheat Sheet

```
Basic usage:
import Image from 'next/image'
<Image src="/photo.jpg" alt="Photo" width={800} height={600} />

Priority (above fold):
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />

Blur placeholder:
<Image src="/photo.jpg" alt="Photo" width={800} height={600}
  placeholder="blur" blurDataURL="data:image/jpeg;base64,..." />

Responsive:
<Image src="/photo.jpg" alt="Photo" width={800} height={600}
  sizes="(max-width: 768px) 100vw, 50vw" />

Fill mode:
<div style={{ position: 'relative', width: '100%', height: '400px' }}>
  <Image src="/photo.jpg" alt="Photo" fill style={{ objectFit: 'cover' }} />
</div>

Remote images:
next.config.js → images.remotePatterns

Configuration:
next.config.js → images.deviceSizes, imageSizes, formats
```

## References & Learn More

- [Next.js Docs: Image](https://nextjs.org/docs/app/building-your-application/optimizing/images)
- [Image Optimization Guide](https://nextjs.org/docs/app/building-your-application/optimizing/images)
- [Web Performance: Image Optimization](https://web.dev/fast/#optimize-your-images)
