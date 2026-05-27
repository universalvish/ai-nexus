import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Toaster } from '@/components/ui/toaster';
import { ThemeProvider } from '@/components/theme-provider';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'AI Nexus - Enterprise AI Operating System',
  description: 'A production-grade futuristic AI-powered SaaS ecosystem with autonomous AI agents, automation systems, cybersecurity protections, and enterprise-grade dashboards.',
  keywords: ['AI', 'Artificial Intelligence', 'SaaS', 'Automation', 'Machine Learning', 'Enterprise'],
  authors: [{ name: 'AI Nexus Team' }],
  robots: 'index, follow',
  openGraph: {
    title: 'AI Nexus - Enterprise AI Operating System',
    description: 'Build the future of AI-powered business operations',
    type: 'website',
    locale: 'en_US',
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#030014' },
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}