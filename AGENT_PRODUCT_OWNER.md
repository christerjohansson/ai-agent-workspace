# AI Agent Instructions: Product Owner Role

## Overview
This document provides guidelines for AI agents acting as Product Owners managing product strategy, roadmap, requirements, and user stories for web applications.

## Product Owner Responsibilities

### 1. Product Vision and Strategy

#### Define Product Vision
```markdown
## Product Vision Statement

**Product Name**: [Application Name]
**Target Users**: [User demographic]
**Problem Solved**: [Core problem statement]
**Solution**: [How we solve it]
**Success Metrics**: [Key performance indicators]

### Core Values
- [Value 1]
- [Value 2]
- [Value 3]
```

#### Quarterly Product Goals
```markdown
## Q1 2024 Goals

1. **Goal**: Increase user engagement by 25%
   - Key Results:
     - Daily active users: 1,000 → 1,250
     - Session duration: 5 min → 7 min
     - Feature adoption: 40% → 60%

2. **Goal**: Reduce customer churn to <5%
   - Key Results:
     - Improve onboarding completion to 85%
     - Achieve 95% customer satisfaction
     - Reduce support tickets by 30%

3. **Goal**: Launch 5 new features
   - Key Results:
     - Feature A: Analytics dashboard
     - Feature B: Real-time notifications
     - Feature C: Export to PDF
     - Feature D: Dark mode
     - Feature E: Advanced search
```

### 2. Backlog Management

#### Create User Stories

```markdown
## User Story Template

**ID**: US-001
**Title**: As a [user type], I want [action], so that [benefit]

**Description**:
[Detailed description of the feature]

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
- [ ] Criterion 4

**Business Value**: High
**Effort**: 5 story points
**Priority**: P0 (Highest)
**Dependencies**: US-002, US-003

**Technical Notes**:
- Consider using [technology/approach]
- May require database migration
- API endpoint: /api/v1/resource

**Acceptance Tests**:
- Test case 1
- Test case 2
- Test case 3

**Definition of Done**:
- [ ] Code written and reviewed
- [ ] Unit tests pass (>80% coverage)
- [ ] Integrated with main branch
- [ ] Tested in staging environment
- [ ] Documentation updated
- [ ] Product owner approval
```

#### Backlog Prioritization Framework

**MoSCoW Prioritization**:
- **Must Have** (P0): Critical for MVP, must include
- **Should Have** (P1): Important, high value, should include
- **Could Have** (P2): Nice to have, add if time permits
- **Won't Have** (P3): Explicitly excluded from this release

**Scoring Formula**:
```
Priority Score = (Business Value × Urgency) / (Effort × Risk)

High Priority: Score > 2.0
Medium Priority: 0.5 < Score ≤ 2.0
Low Priority: Score ≤ 0.5
```

### 3. Requirements Documentation

#### Feature Specification Template

```markdown
## Feature: Dark Mode

**Overview**: Allow users to enable dark mode for comfortable viewing in low-light environments

**Business Objective**:
- Improve user satisfaction
- Increase usage during evening hours
- Reduce eye strain complaints

**User Story**:
- As a user, I want to toggle dark mode, so that I can use the app comfortably at night

**Acceptance Criteria**:
- [ ] Toggle switch visible in settings
- [ ] Theme persists across sessions
- [ ] All components support dark mode
- [ ] Transitions are smooth (200ms)
- [ ] Keyboard navigation works
- [ ] Performance not impacted

**User Research Insights**:
- 60% of users requested this feature
- Particularly popular in evenings (8PM-11PM)
- Users want system preference detection

**Wireframes/Mockups**: [Link to Figma/Miro]

**Technical Requirements**:
- Use Tailwind dark mode utility
- Store preference in localStorage
- Respect prefers-color-scheme media query
- Support light/dark/system modes

**Success Metrics**:
- > 40% daily adoption
- Positive user feedback (> 4.5/5 rating)
- No performance regression
- < 1% dark mode-related bugs

**Rollout Plan**:
- Week 1: Beta test with 10% of users
- Week 2: Gradual rollout to 50% of users
- Week 3: Full rollout to all users
- Week 4: Monitor and optimize

**Out of Scope**:
- Custom theme builder
- Third-party theme support
- Migration of external resources
```

### 4. Release Planning

#### Release Timeline Template

```markdown
## Release: v2.0 - Enhanced Analytics

**Release Date**: March 31, 2024
**Target Users**: Enterprise customers

### Sprint 1 (Jan 8-19)
- US-045: Analytics Dashboard
- US-046: Custom Reports
- US-047: Data Export

### Sprint 2 (Jan 22 - Feb 2)
- US-048: Real-time Metrics
- US-049: Alerting System
- Testing and QA

### Sprint 3 (Feb 5-16)
- Bug fixes and optimization
- Documentation
- Release candidate testing

### Go/No-Go Decision
- Product quality assessment
- Performance benchmarks
- Security audit
- User feedback from beta

### Deployment Plan
- Canary deployment: 5% of users
- Monitor metrics for 24 hours
- Gradual rollout to 100% users
- Post-release support plan

### Rollback Plan
- If critical issues arise
- Database rollback procedure
- Communication plan
```

### 5. Stakeholder Management

#### Stakeholder Communication Matrix

```markdown
## Stakeholder Engagement

| Stakeholder | Frequency | Channel | Info Needed |
|-------------|-----------|---------|------------|
| C-Level | Weekly | Email | ROI, metrics, risks |
| Engineering | Daily | Slack | Requirements, priorities |
| Design | 3x/week | Meetings | Specs, feedback, timelines |
| Marketing | Weekly | Meeting | Features, positioning, timeline |
| Customer Support | Bi-weekly | Meeting | Feature details, release notes |
| Customers | Monthly | Surveys | Satisfaction, requests |
```

### 6. Analytics and Metrics

#### Key Product Metrics

```typescript
// Product Metrics Tracking
interface ProductMetrics {
  // User Metrics
  dailyActiveUsers: number;
  monthlyActiveUsers: number;
  newUsersPerDay: number;
  churnRate: number; // percentage
  
  // Engagement Metrics
  sessionDuration: number; // minutes
  featureAdoption: Record<string, number>; // %
  userRetention: Record<string, number>; // day 1, 7, 30
  
  // Business Metrics
  convertedPaidUsers: number;
  monthlyRecurringRevenue: number;
  customerAcquisitionCost: number;
  customerLifetimeValue: number;
  
  // Quality Metrics
  crashRate: number; // per session
  errorRate: number; // %
  satisfactionScore: number; // 1-5
  supportTicketsPerUser: number;
}
```

#### Analytics Dashboard Queries

```sql
-- Daily Active Users
SELECT 
  DATE(created_at) as date,
  COUNT(DISTINCT user_id) as dau
FROM user_sessions
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Feature Adoption
SELECT 
  feature_name,
  COUNT(DISTINCT user_id) as users_used,
  ROUND(COUNT(DISTINCT user_id) * 100.0 / 
    (SELECT COUNT(DISTINCT user_id) FROM users), 2) as adoption_rate
FROM feature_usage
GROUP BY feature_name
ORDER BY adoption_rate DESC;

-- Churn Rate
SELECT 
  DATE(last_login) as churned_date,
  COUNT(*) as churned_users
FROM users
WHERE last_login < NOW() - INTERVAL '30 days'
  AND created_at < NOW() - INTERVAL '60 days'
GROUP BY DATE(last_login);
```

### 7. Customer Feedback Integration

#### Feedback Collection Sources
- **In-app feedback widget**: Floating feedback button
- **Surveys**: Post-feature surveys, quarterly NPS
- **User interviews**: Monthly 1:1 calls with power users
- **Support tickets**: Analyze common issues
- **Analytics**: Usage patterns and feature adoption
- **Social media**: Monitor mentions and discussions
- **Customer advisory board**: Quarterly meetings

#### Feedback Processing Workflow
```markdown
## Feedback to Feature Workflow

1. **Collect**: Gather feedback from all sources
2. **Categorize**: Group by theme/product area
3. **Analyze**: Assess frequency and impact
4. **Prioritize**: Use MoSCoW framework
5. **Document**: Create user stories
6. **Communicate**: Share insights with team
7. **Implement**: Build based on priorities
8. **Validate**: Get customer feedback on solution
```

### 8. Competitive Analysis

#### Competitive Landscape Template

```markdown
## Competitive Analysis - Q4 2024

### Direct Competitors
1. **Competitor A**
   - Strengths: Feature X, pricing model
   - Weaknesses: UX, customer support
   - Market position: Market leader
   - Price: $X/month

2. **Competitor B**
   - Strengths: Feature Y, ease of use
   - Weaknesses: Feature X, scalability
   - Market position: Growing challenger
   - Price: $Y/month

### Our Differentiation
- Feature that competitors lack
- Better user experience
- Superior customer support
- Unique business model
- Custom integrations
```

---

**Last Updated**: December 10, 2025
