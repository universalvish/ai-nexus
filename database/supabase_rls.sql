-- ============================================
-- Supabase: Row-Level Security (RLS) Policies
-- ============================================
-- Run these in the Supabase SQL Editor

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_executions ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE security_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- ============================================
-- Users Table Policies
-- ============================================

-- Users can only view their own profile
CREATE POLICY "Users can view own profile" ON users
  FOR SELECT
  USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON users
  FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Only admins can view all users
CREATE POLICY "Admins can view all users" ON users
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM users 
      WHERE id = auth.uid() 
      AND role IN ('admin', 'super_admin')
    )
  );

-- No direct user creation from client
CREATE POLICY "No direct user insert" ON users
  FOR INSERT
  WITH CHECK (false);

-- ============================================
-- Conversations Table Policies
-- ============================================

-- Users can view their own conversations
CREATE POLICY "Users view own conversations" ON conversations
  FOR SELECT
  USING (auth.uid() = user_id);

-- Users can create conversations
CREATE POLICY "Users create conversations" ON conversations
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own conversations
CREATE POLICY "Users update own conversations" ON conversations
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Users can delete their own conversations
CREATE POLICY "Users delete own conversations" ON conversations
  FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================
-- Messages Table Policies
-- ============================================

-- Users can view messages in their conversations
CREATE POLICY "Users view messages in own conversations" ON messages
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM conversations 
      WHERE conversations.id = messages.conversation_id 
      AND conversations.user_id = auth.uid()
    )
  );

-- Users can create messages in their conversations
CREATE POLICY "Users create messages in own conversations" ON messages
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM conversations 
      WHERE conversations.id = conversation_id 
      AND conversations.user_id = auth.uid()
    )
  );

-- ============================================
-- Agents Table Policies
-- ============================================

-- Users can manage their own agents
CREATE POLICY "Users manage own agents" ON agents
  FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- ============================================
-- Subscriptions Table Policies
-- ============================================

-- Users can view their own subscription
CREATE POLICY "Users view own subscription" ON subscriptions
  FOR SELECT
  USING (auth.uid() = user_id);

-- Users can create subscriptions (for upgrades)
CREATE POLICY "Users create subscription" ON subscriptions
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own subscription
CREATE POLICY "Users update own subscription" ON subscriptions
  FOR UPDATE
  USING (auth.uid() = user_id);

-- ============================================
-- Audit Logs Policies
-- ============================================

-- Only admins can view audit logs
CREATE POLICY "Admins view audit logs" ON audit_logs
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM users 
      WHERE id = auth.uid() 
      AND role IN ('admin', 'super_admin')
    )
  );

-- System can insert audit logs
CREATE POLICY "System insert audit logs" ON audit_logs
  FOR INSERT
  WITH CHECK (true);

-- ============================================
-- Security Alerts Policies
-- ============================================

-- Admins can view security alerts
CREATE POLICY "Admins view security alerts" ON security_alerts
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM users 
      WHERE id = auth.uid() 
      AND role IN ('admin', 'super_admin')
    )
  );

-- System can create security alerts
CREATE POLICY "System create security alerts" ON security_alerts
  FOR INSERT
  WITH CHECK (true);

-- Admins can update security alerts
CREATE POLICY "Admins update security alerts" ON security_alerts
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM users 
      WHERE id = auth.uid() 
      AND role IN ('admin', 'super_admin')
    )
  );

-- ============================================
-- Notifications Policies
-- ============================================

-- Users can view their own notifications
CREATE POLICY "Users view own notifications" ON notifications
  FOR SELECT
  USING (auth.uid() = user_id);

-- Users can update their own notifications
CREATE POLICY "Users update own notifications" ON notifications
  FOR UPDATE
  USING (auth.uid() = user_id);

-- System can create notifications
CREATE POLICY "System create notifications" ON notifications
  FOR INSERT
  WITH CHECK (true);

-- ============================================
-- Indexes for Performance
-- ============================================

CREATE INDEX CONCURRENTLY idx_conversations_user_id ON conversations(user_id);
CREATE INDEX CONCURRENTLY idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX CONCURRENTLY idx_agents_user_id ON agents(user_id);
CREATE INDEX CONCURRENTLY idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX CONCURRENTLY idx_audit_logs_action ON audit_logs(action);
CREATE INDEX CONCURRENTLY idx_notifications_user_id ON notifications(user_id);
CREATE INDEX CONCURRENTLY idx_security_alerts_is_resolved ON security_alerts(is_resolved);

-- ============================================
-- Functions
-- ============================================

-- Function to get user role
CREATE OR REPLACE FUNCTION get_user_role()
RETURNS TEXT AS $$
  SELECT role FROM users WHERE id = auth.uid();
$$ LANGUAGE SQL SECURITY DEFINER STABLE;

-- Function to check if user is admin
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM users 
    WHERE id = auth.uid() 
    AND role IN ('admin', 'super_admin')
  );
$$ LANGUAGE SQL SECURITY DEFINER STABLE;

-- Trigger to update conversation timestamp
CREATE OR REPLACE FUNCTION update_conversation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE conversations 
  SET updated_at = NOW() 
  WHERE id = NEW.conversation_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_conversation_on_message
AFTER INSERT ON messages
FOR EACH ROW
EXECUTE FUNCTION update_conversation_timestamp();