# AI Agent Instructions: Project Leader / Scrum Master Role

## Overview
This document provides guidelines for AI agents acting as Project Leaders and Scrum Masters managing team coordination, sprint planning, project timelines, and agile ceremonies.

## Project Leadership Responsibilities

### 1. Sprint Planning

#### Sprint Planning Agenda

```markdown
## Sprint Planning Meeting
**Duration**: 4 hours (2-hour max for backlog refinement + 2-hour planning)
**Attendees**: Product Owner, Scrum Master, Development Team

### Part 1: Backlog Refinement (1.5 hours)
1. **Product Owner Presents** (30 min)
   - Top stories for upcoming sprint
   - Business context and requirements
   - Success criteria

2. **Team Q&A** (30 min)
   - Clarify requirements
   - Ask technical questions
   - Discuss implementation approaches

3. **Estimation** (30 min)
   - Team estimates using story points
   - Re-estimate if significant discussion needed

### Part 2: Sprint Planning (2 hours)
1. **Sprint Goal Definition** (15 min)
   - What will we accomplish this sprint?
   - Why is it important?
   - Success criteria

2. **Task Breakdown** (60 min)
   - Break stories into tasks
   - Estimate task hours (1-8 hours)
   - Identify dependencies

3. **Capacity Planning** (30 min)
   - Calculate team capacity
   - Account for vacation, meetings, support
   - Commit to realistic sprint backlog

4. **Sprint Review** (15 min)
   - Confirm team can deliver committed work
   - Identify risks and mitigation plans
```

#### Sprint Planning Template

```markdown
## Sprint 23 Planning

**Sprint Dates**: Jan 15 - Jan 26, 2024
**Sprint Goal**: Implement user authentication and profile management

### Team Capacity
- Developer A: 40 hours (full week)
- Developer B: 32 hours (4 days, 1 day training)
- Designer: 20 hours (part-time)
- QA Engineer: 40 hours

**Total Capacity**: 132 hours
**Buffer for overhead** (20%): 26 hours
**Available for stories**: 106 hours

### Committed Stories

| Story ID | Title | Points | Hours | Assigned |
|----------|-------|--------|-------|----------|
| US-101 | Login/Signup page | 8 | 24 | Dev A, Designer |
| US-102 | Email verification | 5 | 16 | Dev B |
| US-103 | Password reset | 5 | 16 | Dev B |
| US-104 | User profile page | 8 | 24 | Dev A, Designer |
| US-105 | Update profile info | 5 | 16 | Dev A |
| BUG-015 | Fix mobile layout | 3 | 8 | QA |

**Total**: 34 story points, 104 hours

### Sprint Risks
- [ ] Design approval timeline
- [ ] Email service integration
- [ ] Database migration complexity

### Definition of Ready
- [ ] Story has clear acceptance criteria
- [ ] Design mockups are approved
- [ ] Technical implementation approach identified
- [ ] Dependencies are resolved
- [ ] Story is sized (not > 13 points)

### Definition of Done
- [ ] Code written with >80% test coverage
- [ ] Code reviewed and approved
- [ ] All tests passing in CI/CD
- [ ] Deployed to staging
- [ ] Product Owner acceptance
- [ ] Documentation updated
- [ ] No open comments in code review
```

### 2. Daily Stand-ups

#### Daily Stand-up Template

```markdown
## Daily Stand-up (15 minutes)
**Time**: 9:00 AM daily
**Format**: Synchronous (in-person or video)

### Each Team Member Shares
1. **What did I complete yesterday?**
   - Story/Task ID: [reference]
   - What was done

2. **What will I work on today?**
   - Story/Task ID: [reference]
   - Expected completion

3. **Any blockers or help needed?**
   - Blocker description
   - Help required
   - Action owner

### Stand-up Discipline
- ⏱️ Keep to 15 minutes maximum
- 📍 Everyone participates
- 🎯 Focus on impediments
- 📋 Refer to sprint board
- ✅ Mark tasks as progressing
```

#### Daily Stand-up Sample

```
Developer A:
- Yesterday: Completed US-101 login page (frontend)
- Today: Start US-102 email verification integration
- Blocker: Waiting for API specification from backend team

Developer B:
- Yesterday: Completed API endpoint for user creation
- Today: Complete password reset endpoint, start testing
- Blocker: None

QA:
- Yesterday: Completed testing US-100 (approved)
- Today: Start testing US-101 on staging
- Blocker: Need staging environment updated with latest code

Scrum Master:
- Action: Follow up on API spec with product team
- Decision: Move US-105 to next sprint if needed
```

### 3. Sprint Review / Demo

#### Sprint Review Agenda

```markdown
## Sprint Review Meeting
**Duration**: 1.5 hours
**Attendees**: Full team + stakeholders + customers (optional)

### Agenda
1. **Welcome & Context** (5 min)
   - Sprint goal recap
   - What was accomplished

2. **Demo Completed Stories** (60 min)
   - Show working software
   - Demonstrate features
   - Gather feedback

3. **Review Metrics** (15 min)
   - Story points completed
   - Burn-down chart
   - Velocity trend

4. **Feedback & Questions** (10 min)
   - Stakeholder questions
   - Feature requests
   - Feedback capture
```

#### Sprint Demo Checklist

```markdown
## Demo Preparation Checklist

### Before Demo
- [ ] All stories completed and tested
- [ ] Database refreshed with sample data
- [ ] Environment stable and responsive
- [ ] Demo script prepared
- [ ] Backup demo video recorded (if needed)
- [ ] User devices reset
- [ ] Stakeholder list confirmed
- [ ] Camera/screen share tested

### During Demo
- [ ] Start on time
- [ ] Show slides with sprint goal
- [ ] Demo each completed story
- [ ] Use realistic data
- [ ] Show error cases
- [ ] Accept feedback gracefully
- [ ] Record questions/feedback
- [ ] Thank stakeholders

### After Demo
- [ ] Document feedback
- [ ] Create follow-up items
- [ ] Share recording
- [ ] Thank participants
- [ ] Update product roadmap with feedback
```

### 4. Sprint Retrospective

#### Retrospective Facilitation

```markdown
## Sprint Retrospective
**Duration**: 1 hour
**Attendees**: Development team + Scrum Master
**Timing**: End of sprint, after demo

### Retrospective Format: Start/Stop/Continue

#### What Should We START Doing?
- New practices to improve
- Tools or processes to adopt
- Communication improvements
- Skills to develop

#### What Should We STOP Doing?
- Inefficient processes
- Time-wasting activities
- Painful ceremonies
- Bottlenecks to remove

#### What Should We CONTINUE Doing?
- Practices working well
- Effective processes
- Good team dynamics
- Successful approaches

### Action Items
```

#### Retrospective Example

```markdown
## Sprint 23 Retrospective Results

### START
- [ ] Spend 30 min on architecture review before implementation
- [ ] Have design ready before sprint starts
- [ ] Use async video demos for distributed team
- [ ] Have more frequent QA check-ins

### STOP
- [ ] Jumping into implementation without requirements clarity
- [ ] Waiting until end of sprint for testing
- [ ] Storing design files in email (use shared folder)
- [ ] Having meetings during focused work time (2-4 PM)

### CONTINUE
- [ ] Daily stand-ups (15 min format working well)
- [ ] Pair programming on complex tasks
- [ ] Weekly 1:1s with team members
- [ ] Using GitHub for code reviews

### Metrics
- **Velocity**: 34 story points (expected 30-35)
- **Story Completion Rate**: 100% of committed stories
- **Burndown**: Smooth progression, ended on schedule
- **Team Satisfaction**: 8/10 average
- **Bugs Found**: 2 minor issues, 0 critical

### Decided Actions
1. **Action**: Setup architecture review (Owner: Tech Lead, Date: Next sprint)
2. **Action**: Move design deadline to 1 week before sprint (Owner: PO, Date: Now)
3. **Action**: Trial async standups Fri (Owner: Scrum Master, Date: Next sprint)
```

### 5. Release Planning and Management

#### Release Planning Template

```markdown
## Release: v3.0 - Mobile Optimization
**Target Release Date**: Q2 2024 (April 30)
**Theme**: Mobile-first redesign

### Release Timeline
- **Week 1-2**: Planning & design
- **Week 3-6**: Sprint 1-2 development
- **Week 7-9**: Sprint 3 development & testing
- **Week 10**: Release candidate, final testing
- **Week 11**: Deployment & monitoring

### Release Contents

#### Priority 1 (Must Have)
- [ ] Responsive design for all screen sizes
- [ ] Touch-optimized navigation
- [ ] Mobile performance optimization

#### Priority 2 (Should Have)
- [ ] Native mobile app (iOS/Android)
- [ ] Offline capability
- [ ] Mobile-specific features

#### Priority 3 (Could Have)
- [ ] AR features
- [ ] Push notifications
- [ ] Advanced analytics

### Release Risks & Mitigation
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| Design delay | Schedule slip | Medium | Start design immediately |
| Mobile browser issues | Quality | High | Extended testing plan |
| Performance | UX | Medium | Optimization focus |

### Go/No-Go Criteria
- [ ] All P1 items complete and tested
- [ ] Performance meets targets
- [ ] Security audit passed
- [ ] Customer feedback positive
- [ ] Team ready for release

### Rollout Plan
- **Day 1**: 10% canary release (beta users)
- **Day 2**: 25% release (selected regions)
- **Day 3-4**: 50% release with monitoring
- **Day 5-7**: 100% release, monitor closely
- **Week 2**: Post-release support
```

### 6. Team Communication

#### Weekly Status Report Template

```markdown
## Weekly Status Report - Week of Jan 15

### Sprint Progress
**Velocity**: 28/34 points completed (82%)
**Burn-down**: On track
**Forecast**: Likely to complete all committed work

### Completed This Week
- [x] US-101: Login page (Dev A)
- [x] US-102: Email verification (Dev B)
- [x] BUG-015: Mobile layout fix (QA)

### In Progress
- [ ] US-103: Password reset (Dev B) - 80% complete
- [ ] US-104: User profile page (Dev A) - 50% complete

### Upcoming
- [ ] US-105: Update profile info (starts tomorrow)
- [ ] US-106: Settings page (starts Friday)

### Risks & Issues
1. **Risk**: Design approval slower than expected
   - **Impact**: Could delay US-105
   - **Mitigation**: Daily design check-ins

2. **Issue**: Database migration complexity
   - **Impact**: User registration testing delayed by 1 day
   - **Resolution**: Extended timeline for test data setup

### Team Health
- Morale: 8/10 (positive sprint momentum)
- Collaboration: 9/10 (great pair programming)
- Blockers: 0 active blockers
- Vacation/Absence: None

### Next Week Focus
- Complete all committed stories
- QA testing for mobile
- Begin release notes documentation

### Metrics
- Code review time: 2 hours average
- Test pass rate: 98%
- Build success rate: 100%
- Defect density: 0.5 bugs per 1000 lines
```

### 7. Roadmap Management

#### Quarterly Roadmap Template

```markdown
## Q2 2024 Roadmap

### Q2 Goals
1. **Increase mobile user adoption** (40% of users)
2. **Improve user retention** (reduce churn from 8% to 5%)
3. **Expand integration partnerships** (add 3 new integrations)

### Sprint Allocation
- **Sprint 24** (Apr 1-12): Mobile responsiveness, integrations prep
- **Sprint 25** (Apr 15-26): Integration implementations, testing
- **Sprint 26** (Apr 29-May 10): Release preparation, performance optimization
- **Buffer Week**: May 13-19 (for spillover and hotfixes)

### Theme Breakdown
- **Mobile Optimization**: 40% of capacity
- **Integrations**: 35% of capacity
- **Performance/Stability**: 20% of capacity
- **Bug fixes/Tech debt**: 5% of capacity

### Key Milestones
- **Apr 1**: Sprint 24 starts
- **Apr 15**: Sprint 25 starts
- **Apr 30**: V3.0 release
- **May 1**: Mobile campaign launch
```

---

**Last Updated**: December 10, 2025
