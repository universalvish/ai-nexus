export const siteConfig = {
  name: 'AI Nexus',
  description: 'Enterprise AI Operating System',
  url: process.env.NEXT_PUBLIC_SITE_URL || 'https://ainexus.ai',
  ogImage: '/og-image.png',
  links: {
    github: 'https://github.com/ai-nexus',
    docs: '/docs',
  },
};

export const navItems = [
  { title: 'Home', href: '/' },
  { title: 'Features', href: '#features' },
  { title: 'Pricing', href: '#pricing' },
  { title: 'Docs', href: '/docs' },
  { title: 'Blog', href: '/blog' },
];

export const featureItems = [
  {
    title: 'AI Agents',
    description: 'Deploy intelligent agents for customer support, report generation, and business analysis.',
    icon: 'Bot',
  },
  {
    title: 'Real-time Chat',
    description: 'Stream responses with memory and context. Multi-language support with AI moderation.',
    icon: 'MessageSquare',
  },
  {
    title: 'Automation',
    description: 'Build workflows with triggers, scheduling, and queue processing. No code required.',
    icon: 'Zap',
  },
  {
    title: 'Analytics',
    description: 'Track AI usage, revenue, and user metrics. Exportable reports and dashboards.',
    icon: 'BarChart3',
  },
  {
    title: 'Security',
    description: 'Enterprise-grade protection with DDoS mitigation, WAF, and threat monitoring.',
    icon: 'Shield',
  },
  {
    title: 'Billing',
    description: 'Subscription management with trials, invoicing, and usage-based pricing.',
    icon: 'CreditCard',
  },
];

export const pricingPlans = [
  {
    name: 'Free',
    description: 'Perfect for exploring the platform',
    price: 0,
    features: [
      '5 AI conversations per day',
      '1 AI agent',
      'Basic automation',
      'Community support',
      '7-day chat history',
    ],
    cta: 'Get Started',
    popular: false,
  },
  {
    name: 'Pro',
    description: 'For individuals and small teams',
    price: 29,
    features: [
      'Unlimited AI conversations',
      '10 AI agents',
      'Advanced automation',
      'Priority support',
      '30-day chat history',
      'API access',
      'Custom integrations',
    ],
    cta: 'Start Free Trial',
    popular: true,
  },
  {
    name: 'Business',
    description: 'For growing businesses',
    price: 99,
    features: [
      'Everything in Pro',
      'Unlimited AI agents',
      'White-label options',
      'SSO & SAML',
      'Custom AI models',
      'Dedicated support',
      'SLA guarantee',
    ],
    cta: 'Start Free Trial',
    popular: false,
  },
  {
    name: 'Enterprise',
    description: 'For large organizations',
    price: null,
    features: [
      'Everything in Business',
      'Custom deployment',
      'On-premise option',
      'Advanced security',
      'Training & onboarding',
      '24/7 support',
      'Unlimited everything',
    ],
    cta: 'Contact Sales',
    popular: false,
  },
];

export const testimonials = [
  {
    name: 'Sarah Chen',
    role: 'CTO at TechFlow',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop',
    content: 'AI Nexus transformed our customer support. Response times dropped 80% and customer satisfaction increased.',
  },
  {
    name: 'Marcus Johnson',
    role: 'Head of AI at DataCorp',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop',
    content: 'The AI agent capabilities are incredible. We automated 60% of our reporting workflows.',
  },
  {
    name: 'Emily Rodriguez',
    role: 'VP Operations at ScaleUp',
    avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop',
    content: 'Best AI platform we\'ve used. The security features give us confidence to deploy across the enterprise.',
  },
];

export const statsData = [
  { label: 'AI Agents Deployed', value: '10,000+' },
  { label: 'Conversations Daily', value: '1M+' },
  { label: 'Uptime SLA', value: '99.99%' },
  { label: 'Enterprise Clients', value: '500+' },
];

export const footerLinks = {
  product: [
    { title: 'Features', href: '#features' },
    { title: 'Pricing', href: '#pricing' },
    { title: 'Integrations', href: '/integrations' },
    { title: 'Changelog', href: '/changelog' },
  ],
  company: [
    { title: 'About', href: '/about' },
    { title: 'Blog', href: '/blog' },
    { title: 'Careers', href: '/careers' },
    { title: 'Contact', href: '/contact' },
  ],
  resources: [
    { title: 'Documentation', href: '/docs' },
    { title: 'API Reference', href: '/api-docs' },
    { title: 'Status', href: '/status' },
    { title: 'Support', href: '/support' },
  ],
  legal: [
    { title: 'Privacy', href: '/privacy' },
    { title: 'Terms', href: '/terms' },
    { title: 'Security', href: '/security' },
    { title: 'Cookie Policy', href: '/cookies' },
  ],
};