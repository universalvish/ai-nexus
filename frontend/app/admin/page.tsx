'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Users, Bot, Shield, CreditCard, Activity, AlertTriangle,
  Settings, Database, Bell, FileText, TrendingUp, Globe,
  Plus, Search, Filter, MoreVertical, Pause, Play, Trash2,
  Eye, Edit2, Download, RefreshCw, Server, Zap
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';

const adminNavItems = [
  { icon: Users, label: 'Users', href: '/admin/users', color: 'violet' },
  { icon: Bot, label: 'AI Agents', href: '/admin/agents', color: 'fuchsia' },
  { icon: Shield, label: 'Security', href: '/admin/security', color: 'red' },
  { icon: CreditCard, label: 'Billing', href: '/admin/billing', color: 'green' },
  { icon: Activity, label: 'Analytics', href: '/admin/analytics', color: 'blue' },
  { icon: Database, label: 'Database', href: '/admin/database', color: 'orange' },
  { icon: Bell, label: 'Notifications', href: '/admin/notifications', color: 'yellow' },
  { icon: FileText, label: 'Logs', href: '/admin/logs', color: 'gray' },
  { icon: Settings, label: 'Settings', href: '/admin/settings', color: 'gray' },
];

const recentUsers = [
  { id: 1, name: 'Alice Johnson', email: 'alice@company.com', plan: 'Pro', status: 'active', joined: '2 hours ago' },
  { id: 2, name: 'Bob Smith', email: 'bob@startup.io', plan: 'Business', status: 'active', joined: '1 day ago' },
  { id: 3, name: 'Carol Williams', email: 'carol@agency.com', plan: 'Free', status: 'inactive', joined: '3 days ago' },
  { id: 4, name: 'David Brown', email: 'david@tech.co', plan: 'Enterprise', status: 'active', joined: '1 week ago' },
];

const systemMetrics = [
  { label: 'Total Users', value: '12,847', change: '+8%', icon: Users },
  { label: 'Active Agents', value: '342', change: '+12%', icon: Bot },
  { label: 'API Requests', value: '2.4M', change: '+15%', icon: Activity },
  { label: 'Revenue (MRR)', value: '$84,290', change: '+10%', icon: TrendingUp },
];

const activeAlerts = [
  { id: 1, type: 'warning', message: 'High API latency detected in US-East region', time: '5 min ago' },
  { id: 2, type: 'info', message: 'Scheduled backup completed successfully', time: '1 hour ago' },
  { id: 3, type: 'success', message: 'New deployment completed to production', time: '2 hours ago' },
];

export default function AdminPage() {
  const [emergencyStopActive, setEmergencyStopActive] = useState(false);

  const handleEmergencyStop = () => {
    setEmergencyStopActive(!emergencyStopActive);
    // In production, this would trigger emergency shutdown
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Admin Header */}
      <header className="border-b border-white/5 bg-destructive/5">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold flex items-center gap-2">
                <Shield className="w-6 h-6 text-red-400" />
                Admin Control Center
              </h1>
              <p className="text-sm text-muted-foreground">Manage your AI Nexus platform</p>
            </div>
            
            {/* Emergency Stop Button */}
            <Button
              variant={emergencyStopActive ? 'destructive' : 'outline'}
              className={emergencyStopActive ? 'animate-pulse' : ''}
              onClick={handleEmergencyStop}
            >
              <AlertTriangle className="w-4 h-4 mr-2" />
              {emergencyStopActive ? 'Resume AI Systems' : 'Emergency AI Stop'}
            </Button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Admin Sidebar */}
        <aside className="w-64 border-r border-white/5 p-4 min-h-[calc(100vh-73px)]">
          <nav className="space-y-1">
            {adminNavItems.map((item) => (
              <button
                key={item.href}
                className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-muted-foreground hover:text-foreground hover:bg-white/5 transition-all text-left"
              >
                <item.icon className={`w-5 h-5 ${
                  item.color === 'violet' ? 'text-violet-400' :
                  item.color === 'fuchsia' ? 'text-fuchsia-400' :
                  item.color === 'red' ? 'text-red-400' :
                  item.color === 'green' ? 'text-green-400' :
                  item.color === 'blue' ? 'text-blue-400' :
                  item.color === 'orange' ? 'text-orange-400' :
                  item.color === 'yellow' ? 'text-yellow-400' : 'text-gray-400'
                }`} />
                {item.label}
              </button>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {/* System Metrics */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {systemMetrics.map((metric, index) => (
              <motion.div
                key={metric.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 rounded-xl border border-white/5 bg-white/5"
              >
                <div className="flex items-center justify-between mb-2">
                  <metric.icon className="w-5 h-5 text-violet-400" />
                  <Badge variant={metric.change.startsWith('+') ? 'success' : 'destructive'} className="text-xs">
                    {metric.change}
                  </Badge>
                </div>
                <div className="text-2xl font-bold">{metric.value}</div>
                <div className="text-sm text-muted-foreground">{metric.label}</div>
              </motion.div>
            ))}
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            {/* User Management */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle>User Management</CardTitle>
                      <CardDescription>Manage platform users and permissions</CardDescription>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                        <Input placeholder="Search users..." className="pl-9 w-64" />
                      </div>
                      <Button variant="outline" size="icon">
                        <Filter className="w-4 h-4" />
                      </Button>
                      <Button variant="gradient" size="sm">
                        <Plus className="w-4 h-4 mr-2" />
                        Add User
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {recentUsers.map((user, index) => (
                      <motion.div
                        key={user.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.05 }}
                        className="flex items-center justify-between p-4 rounded-lg hover:bg-white/5 transition-colors"
                      >
                        <div className="flex items-center gap-4">
                          <Avatar>
                            <AvatarFallback>{user.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                          </Avatar>
                          <div>
                            <p className="font-medium">{user.name}</p>
                            <p className="text-sm text-muted-foreground">{user.email}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-4">
                          <Badge variant={user.plan === 'Enterprise' ? 'gradient' : user.plan === 'Business' ? 'info' : 'secondary'}>
                            {user.plan}
                          </Badge>
                          <Badge variant={user.status === 'active' ? 'success' : 'secondary'}>
                            {user.status}
                          </Badge>
                          <span className="text-sm text-muted-foreground w-20">{user.joined}</span>
                          <div className="flex gap-1">
                            <Button variant="ghost" size="icon">
                              <Eye className="w-4 h-4" />
                            </Button>
                            <Button variant="ghost" size="icon">
                              <Edit2 className="w-4 h-4" />
                            </Button>
                            <Button variant="ghost" size="icon">
                              <MoreVertical className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* System Status */}
            <div className="space-y-6">
              {/* Active Alerts */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Bell className="w-5 h-5 text-yellow-400" />
                    Active Alerts
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {activeAlerts.map((alert) => (
                      <div key={alert.id} className="flex items-start gap-3 p-3 rounded-lg bg-white/5">
                        <div className={`w-2 h-2 rounded-full mt-2 ${
                          alert.type === 'warning' ? 'bg-yellow-500' :
                          alert.type === 'success' ? 'bg-green-500' : 'bg-blue-500'
                        }`} />
                        <div>
                          <p className="text-sm">{alert.message}</p>
                          <p className="text-xs text-muted-foreground mt-1">{alert.time}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Quick Actions */}
              <Card>
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-2">
                    <Button variant="outline" size="sm">
                      <RefreshCw className="w-4 h-4 mr-2" />
                      Clear Cache
                    </Button>
                    <Button variant="outline" size="sm">
                      <Database className="w-4 h-4 mr-2" />
                      Backup DB
                    </Button>
                    <Button variant="outline" size="sm">
                      <Download className="w-4 h-4 mr-2" />
                      Export Logs
                    </Button>
                    <Button variant="outline" size="sm">
                      <Server className="w-4 h-4 mr-2" />
                      Restart API
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* AI Safety Monitor */}
              <Card className="border-red-500/20">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-red-400">
                    <Shield className="w-5 h-5" />
                    AI Safety Status
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Prompt Injection Protection</span>
                      <Badge variant="success">Active</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Content Moderation</span>
                      <Badge variant="success">Active</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Human Approval Layer</span>
                      <Badge variant="success">Enabled</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Rate Limiting</span>
                      <Badge variant="success">Enabled</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}