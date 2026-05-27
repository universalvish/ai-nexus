'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Bot, MessageSquare, BarChart3, Settings, LogOut, Menu, X,
  Sparkles, Plus, History, Star, Zap, ChevronRight, Activity,
  Users, FileText, Clock, TrendingUp
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';

const navItems = [
  { icon: Bot, label: 'AI Agents', href: '/dashboard/agents', color: 'violet' },
  { icon: MessageSquare, label: 'Chat', href: '/dashboard/chat', color: 'fuchsia' },
  { icon: BarChart3, label: 'Analytics', href: '/dashboard/analytics', color: 'blue' },
  { icon: FileText, label: 'Workflows', href: '/dashboard/workflows', color: 'green' },
  { icon: Settings, label: 'Settings', href: '/dashboard/settings', color: 'gray' },
];

const recentChats = [
  { id: 1, title: 'Q4 Financial Report Analysis', time: '2 hours ago', messages: 24 },
  { id: 2, title: 'Customer Support Automation', time: '5 hours ago', messages: 18 },
  { id: 3, title: 'Product Launch Strategy', time: 'Yesterday', messages: 42 },
  { id: 4, title: 'Marketing Campaign Optimization', time: '2 days ago', messages: 31 },
];

const quickStats = [
  { label: 'AI Conversations', value: '127', change: '+12%', icon: MessageSquare },
  { label: 'Tasks Automated', value: '89', change: '+8%', icon: Zap },
  { label: 'Time Saved', value: '24h', change: '+15%', icon: Clock },
  { label: 'Success Rate', value: '98.5%', change: '+2%', icon: TrendingUp },
];

export default function DashboardPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    localStorage.removeItem('token');
    await new Promise((resolve) => setTimeout(resolve, 500));
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-background flex">
      {/* Mobile Sidebar Toggle */}
      <button
        className="fixed top-4 left-4 z-50 md:hidden p-2 rounded-lg bg-white/10 backdrop-blur-xl border border-white/10"
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
      </button>

      {/* Sidebar */}
      <AnimatePresence>
        <motion.aside
          initial={{ x: -100, opacity: 0 }}
          animate={{ x: sidebarOpen ? 0 : -100, opacity: sidebarOpen ? 1 : 0 }}
          className="fixed md:static inset-y-0 left-0 z-40 w-64 bg-background border-r border-white/5 flex flex-col"
        >
          {/* Logo */}
          <div className="p-6 border-b border-white/5">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 to-fuchsia-600 flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">AI Nexus</span>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center gap-3 px-4 py-3 rounded-xl text-muted-foreground hover:text-foreground hover:bg-white/5 transition-all"
              >
                <item.icon className={`w-5 h-5 ${
                  item.color === 'violet' ? 'text-violet-400' :
                  item.color === 'fuchsia' ? 'text-fuchsia-400' :
                  item.color === 'blue' ? 'text-blue-400' :
                  item.color === 'green' ? 'text-green-400' : 'text-gray-400'
                }`} />
                {item.label}
              </Link>
            ))}
          </nav>

          {/* Upgrade CTA */}
          <div className="p-4">
            <div className="p-4 rounded-xl bg-gradient-to-br from-violet-500/10 to-fuchsia-500/10 border border-violet-500/20">
              <h4 className="font-semibold mb-1">Upgrade to Pro</h4>
              <p className="text-xs text-muted-foreground mb-3">
                Unlock unlimited AI agents and advanced features
              </p>
              <Button size="sm" className="w-full" variant="gradient">
                <Zap className="w-4 h-4 mr-2" />
                Upgrade
              </Button>
            </div>
          </div>

          {/* User Profile */}
          <div className="p-4 border-t border-white/5">
            <div className="flex items-center gap-3">
              <Avatar>
                <AvatarFallback className="bg-gradient-to-br from-violet-500 to-fuchsia-500 text-white">
                  JD
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="font-medium truncate">John Doe</p>
                <p className="text-xs text-muted-foreground truncate">Pro Plan</p>
              </div>
              <button
                onClick={handleLogout}
                className="p-2 rounded-lg hover:bg-white/5 text-muted-foreground"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>
        </motion.aside>
      </AnimatePresence>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <main className="flex-1 p-6 md:p-8 pt-20 md:pt-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold">Welcome back, John</h1>
              <p className="text-muted-foreground">Here&apos;s what&apos;s happening with your AI agents</p>
            </div>
            <Button variant="gradient">
              <Plus className="w-4 h-4 mr-2" />
              New Chat
            </Button>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {quickStats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 rounded-xl border border-white/5 bg-white/5"
              >
                <div className="flex items-center justify-between mb-2">
                  <stat.icon className="w-5 h-5 text-violet-400" />
                  <Badge variant={stat.change.startsWith('+') ? 'success' : 'destructive'} className="text-xs">
                    {stat.change}
                  </Badge>
                </div>
                <div className="text-2xl font-bold">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </motion.div>
            ))}
          </div>

          {/* Main Grid */}
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Recent Chats */}
            <div className="lg:col-span-2">
              <div className="rounded-xl border border-white/5 bg-white/5 p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold">Recent Chats</h2>
                  <Button variant="ghost" size="sm" asChild>
                    <Link href="/dashboard/chat">View all</Link>
                  </Button>
                </div>

                <div className="space-y-3">
                  {recentChats.map((chat, index) => (
                    <motion.div
                      key={chat.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="flex items-center gap-4 p-4 rounded-lg hover:bg-white/5 transition-colors cursor-pointer group"
                    >
                      <div className="w-10 h-10 rounded-lg bg-violet-500/10 flex items-center justify-center">
                        <MessageSquare className="w-5 h-5 text-violet-400" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium truncate group-hover:text-violet-400 transition-colors">
                          {chat.title}
                        </h3>
                        <p className="text-sm text-muted-foreground">{chat.messages} messages</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-muted-foreground">{chat.time}</p>
                      </div>
                      <ChevronRight className="w-5 h-5 text-muted-foreground group-hover:text-violet-400 transition-colors" />
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div>
              <div className="rounded-xl border border-white/5 bg-white/5 p-6">
                <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>

                <div className="space-y-3">
                  <Link href="/dashboard/agents/create" className="block">
                    <div className="flex items-center gap-4 p-4 rounded-lg hover:bg-white/5 transition-colors">
                      <div className="w-10 h-10 rounded-lg bg-violet-500/10 flex items-center justify-center">
                        <Bot className="w-5 h-5 text-violet-400" />
                      </div>
                      <div>
                        <h3 className="font-medium">Create Agent</h3>
                        <p className="text-sm text-muted-foreground">Build a new AI agent</p>
                      </div>
                    </div>
                  </Link>

                  <Link href="/dashboard/workflows/create" className="block">
                    <div className="flex items-center gap-4 p-4 rounded-lg hover:bg-white/5 transition-colors">
                      <div className="w-10 h-10 rounded-lg bg-green-500/10 flex items-center justify-center">
                        <Zap className="w-5 h-5 text-green-400" />
                      </div>
                      <div>
                        <h3 className="font-medium">New Workflow</h3>
                        <p className="text-sm text-muted-foreground">Automate a task</p>
                      </div>
                    </div>
                  </Link>

                  <Link href="/dashboard/analytics" className="block">
                    <div className="flex items-center gap-4 p-4 rounded-lg hover:bg-white/5 transition-colors">
                      <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center">
                        <Activity className="w-5 h-5 text-blue-400" />
                      </div>
                      <div>
                        <h3 className="font-medium">View Analytics</h3>
                        <p className="text-sm text-muted-foreground">Check performance</p>
                      </div>
                    </div>
                  </Link>
                </div>
              </div>

              {/* Active Agents */}
              <div className="rounded-xl border border-white/5 bg-white/5 p-6 mt-6">
                <h2 className="text-xl font-semibold mb-4">Active Agents</h2>

                <div className="space-y-3">
                  {[
                    { name: 'Support Bot', status: 'online', tasks: 24 },
                    { name: 'Report Generator', status: 'online', tasks: 8 },
                    { name: 'Data Analyst', status: 'idle', tasks: 0 },
                  ].map((agent, index) => (
                    <div key={index} className="flex items-center gap-3">
                      <div className="relative">
                        <Avatar>
                          <AvatarFallback className="bg-gradient-to-br from-violet-500 to-fuchsia-500">
                            <Bot className="w-4 h-4" />
                          </AvatarFallback>
                        </Avatar>
                        <div className={`absolute -bottom-1 -right-1 w-3 h-3 rounded-full border-2 border-background ${
                          agent.status === 'online' ? 'bg-green-500' : 'bg-yellow-500'
                        }`} />
                      </div>
                      <div className="flex-1">
                        <p className="font-medium text-sm">{agent.name}</p>
                        <p className="text-xs text-muted-foreground">{agent.tasks} tasks today</p>
                      </div>
                      <Badge variant={agent.status === 'online' ? 'success' : 'warning'} className="text-xs">
                        {agent.status}
                      </Badge>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}