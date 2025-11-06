#!/usr/bin/env python3
"""
Generate a realistic test PDF with biweekly status updates for entity extraction testing.

This creates a 6-month status document with three teams, multiple people, and various projects.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime, timedelta


def generate_test_status_pdf(filename="test_status_report.pdf"):
    """
    Generate a comprehensive test PDF with 6 months of biweekly status updates.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          leftMargin=0.75*inch, rightMargin=0.75*inch,
                          topMargin=0.75*inch, bottomMargin=0.75*inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2C3E50',
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#34495E',
        spaceAfter=12,
        spaceBefore=12
    )

    team_style = ParagraphStyle(
        'TeamHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor='#16A085',
        spaceAfter=8,
        spaceBefore=16
    )

    project_style = ParagraphStyle(
        'ProjectHeading',
        parent=styles['Heading4'],
        fontSize=12,
        textColor='#2980B9',
        spaceAfter=6,
        spaceBefore=10
    )

    body_style = styles['BodyText']

    story = []

    # Title page
    story.append(Paragraph("Company Biweekly Status Report", title_style))
    story.append(Paragraph("May 2024 - October 2024", styles['Heading3']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Internal Team Updates", styles['Normal']))
    story.append(PageBreak())

    # Define team data
    teams_data = {
        "Engineering": {
            "members": [
                {"name": "Sarah Chen", "role": "Senior Software Engineer", "hard_skills": ["React", "TypeScript", "Node.js", "GraphQL"], "soft_skills": ["mentoring", "code review"]},
                {"name": "Marcus Rodriguez", "role": "Backend Engineer", "hard_skills": ["Python", "FastAPI", "PostgreSQL", "Redis"], "soft_skills": ["problem solving", "documentation"]},
                {"name": "Priya Sharma", "role": "DevOps Engineer", "hard_skills": ["AWS", "Docker", "Kubernetes", "Terraform"], "soft_skills": ["automation", "collaboration"]},
                {"name": "James Kim", "role": "Full Stack Developer", "hard_skills": ["Vue.js", "Django", "MySQL", "REST APIs"], "soft_skills": ["adaptability", "technical writing"]}
            ],
            "projects": [
                "API Migration Project",
                "Customer Dashboard Redesign",
                "Infrastructure Modernization"
            ]
        },
        "Product": {
            "members": [
                {"name": "Emily Thompson", "role": "Senior Product Manager", "hard_skills": ["Figma", "SQL", "Analytics"], "soft_skills": ["strategic thinking", "stakeholder management", "leadership"]},
                {"name": "David Park", "role": "Product Designer", "hard_skills": ["Sketch", "Adobe XD", "Prototyping"], "soft_skills": ["user research", "visual communication"]},
                {"name": "Aisha Williams", "role": "Product Analyst", "hard_skills": ["Tableau", "Python", "A/B Testing"], "soft_skills": ["data analysis", "presentation skills"]}
            ],
            "projects": [
                "Mobile App Feature Roadmap",
                "User Onboarding Optimization",
                "Analytics Dashboard Enhancement"
            ]
        },
        "Business Operations": {
            "members": [
                {"name": "Robert Chen", "role": "Operations Manager", "hard_skills": ["Excel", "Salesforce", "Project Management"], "soft_skills": ["team leadership", "process optimization", "communication"]},
                {"name": "Lisa Martinez", "role": "Business Analyst", "hard_skills": ["Power BI", "SQL", "Financial Modeling"], "soft_skills": ["analytical thinking", "reporting"]},
                {"name": "Tom Anderson", "role": "Customer Success Lead", "hard_skills": ["Zendesk", "CRM Systems"], "soft_skills": ["customer communication", "relationship building", "training"]}
            ],
            "projects": [
                "Q3 Revenue Planning",
                "Customer Retention Program",
                "Sales Process Automation"
            ]
        }
    }

    # Status updates for 12 biweekly periods (6 months)
    status_updates = [
        # Period 1 - May 1-14, 2024
        {
            "period": "May 1-14, 2024",
            "Engineering": [
                {
                    "project": "API Migration Project",
                    "team": ["Sarah Chen", "Marcus Rodriguez"],
                    "update": "Sarah Chen led the initial architecture planning for migrating our REST API to GraphQL. Marcus Rodriguez completed the database schema redesign to support the new API structure. Sarah mentored Marcus on GraphQL best practices and TypeScript implementation patterns.",
                    "next_steps": "Begin implementing core GraphQL resolvers using Node.js and TypeScript. Marcus will set up PostgreSQL connection pooling."
                },
                {
                    "project": "Infrastructure Modernization",
                    "team": ["Priya Sharma"],
                    "update": "Priya Sharma completed the AWS infrastructure audit and created Terraform templates for our staging environment. She automated deployment workflows using Docker and configured Kubernetes clusters.",
                    "next_steps": "Deploy staging environment and begin migration testing. Set up Redis caching layer."
                }
            ],
            "Product": [
                {
                    "project": "Mobile App Feature Roadmap",
                    "team": ["Emily Thompson", "David Park"],
                    "update": "Emily Thompson conducted stakeholder interviews and defined Q3 priorities. David Park created initial wireframes in Figma for the new feature set. Emily demonstrated strong leadership in aligning cross-functional teams.",
                    "next_steps": "Complete user research with Aisha Williams. Finalize prototypes in Adobe XD."
                }
            ],
            "Business Operations": [
                {
                    "project": "Q3 Revenue Planning",
                    "team": ["Robert Chen", "Lisa Martinez"],
                    "update": "Robert Chen led the quarterly planning kickoff with sales and finance teams. Lisa Martinez built financial models in Excel and created Power BI dashboards for revenue tracking. Robert's process optimization skills improved meeting efficiency by 30%.",
                    "next_steps": "Present findings to executive team. Begin Salesforce integration for pipeline tracking."
                }
            ]
        },
        # Period 2 - May 15-28, 2024
        {
            "period": "May 15-28, 2024",
            "Engineering": [
                {
                    "project": "API Migration Project",
                    "team": ["Sarah Chen", "Marcus Rodriguez", "James Kim"],
                    "update": "The team completed 40% of GraphQL resolver implementation. Marcus Rodriguez optimized PostgreSQL queries, reducing response time by 25%. James Kim joined the project to help with REST API deprecation planning. Sarah conducted code reviews and pair programming sessions with James.",
                    "next_steps": "Complete remaining resolvers. James will document API migration guide for clients."
                },
                {
                    "project": "Customer Dashboard Redesign",
                    "team": ["James Kim"],
                    "update": "James Kim began frontend work using Vue.js for the new dashboard. Implemented responsive layouts and integrated with existing Django backend using REST APIs.",
                    "next_steps": "Connect to new GraphQL endpoints once available. Add real-time updates using WebSockets."
                }
            ],
            "Product": [
                {
                    "project": "User Onboarding Optimization",
                    "team": ["Emily Thompson", "Aisha Williams"],
                    "update": "Aisha Williams analyzed user onboarding data using Python and Tableau, identifying a 35% drop-off at step 3. Emily Thompson prioritized fixes based on A/B testing results. Aisha's analytical skills were crucial in identifying key bottlenecks.",
                    "next_steps": "Design improved onboarding flow. Coordinate with Sarah Chen on implementation timeline."
                }
            ],
            "Business Operations": [
                {
                    "project": "Customer Retention Program",
                    "team": ["Tom Anderson", "Lisa Martinez"],
                    "update": "Tom Anderson launched the retention program pilot with 50 at-risk customers using Zendesk workflows. Lisa Martinez created SQL queries to identify churn patterns and track program effectiveness. Tom's relationship building skills resulted in 20% improvement in customer satisfaction scores.",
                    "next_steps": "Expand program to 200 customers. Integrate CRM data with analytics dashboard."
                }
            ]
        },
        # Period 3 - May 29 - June 11, 2024
        {
            "period": "May 29 - June 11, 2024",
            "Engineering": [
                {
                    "project": "API Migration Project",
                    "team": ["Sarah Chen", "Marcus Rodriguez", "James Kim"],
                    "update": "Completed 75% of GraphQL migration. Marcus Rodriguez implemented Redis caching strategy, improving API performance by 40%. Sarah Chen finalized TypeScript type definitions. James Kim completed migration documentation with technical writing support. The team's collaboration was excellent.",
                    "next_steps": "Final testing and security audit. Begin client communication about deprecation timeline."
                },
                {
                    "project": "Infrastructure Modernization",
                    "team": ["Priya Sharma", "Marcus Rodriguez"],
                    "update": "Priya Sharma deployed the new Kubernetes cluster to production. Marcus helped with PostgreSQL migration to AWS RDS. Priya's automation scripts reduced deployment time by 60%. They worked together on Docker container optimization.",
                    "next_steps": "Monitor production performance. Set up auto-scaling policies."
                }
            ],
            "Product": [
                {
                    "project": "Mobile App Feature Roadmap",
                    "team": ["Emily Thompson", "David Park", "Aisha Williams"],
                    "update": "David Park completed high-fidelity prototypes in Figma. Aisha Williams conducted user testing sessions with 30 participants and analyzed feedback data. Emily Thompson presented roadmap to executives, demonstrating strong presentation skills and strategic thinking.",
                    "next_steps": "Begin development sprint planning with engineering team. Emily to coordinate with Sarah Chen."
                }
            ],
            "Business Operations": [
                {
                    "project": "Sales Process Automation",
                    "team": ["Robert Chen", "Tom Anderson"],
                    "update": "Robert Chen mapped existing sales workflows and identified automation opportunities in Salesforce. Tom Anderson provided customer success insights to improve handoff processes. Robert's process optimization reduced manual data entry by 45%.",
                    "next_steps": "Implement Salesforce automation rules. Train sales team on new processes."
                }
            ]
        },
        # Period 4 - June 12-25, 2024
        {
            "period": "June 12-25, 2024",
            "Engineering": [
                {
                    "project": "API Migration Project",
                    "team": ["Sarah Chen", "Marcus Rodriguez"],
                    "update": "Successfully completed API migration! Sarah Chen led the final security audit and Marcus Rodriguez handled the production deployment. Zero downtime achieved. The team celebrated this major milestone. Sarah's mentoring throughout the project was invaluable.",
                    "next_steps": "Monitor production metrics. Begin deprecation of old REST endpoints in 60 days."
                },
                {
                    "project": "Customer Dashboard Redesign",
                    "team": ["James Kim", "Sarah Chen"],
                    "update": "James Kim integrated the dashboard with new GraphQL API. Sarah Chen provided code review and helped optimize React component rendering. Implemented real-time updates using WebSockets and Node.js. James's adaptability was key to meeting tight deadlines.",
                    "next_steps": "User acceptance testing. Performance optimization for large datasets."
                }
            ],
            "Product": [
                {
                    "project": "Analytics Dashboard Enhancement",
                    "team": ["Aisha Williams", "Emily Thompson"],
                    "update": "Aisha Williams designed new analytics views using Tableau and Python for data processing. Emily Thompson gathered requirements from executive team. Aisha's data analysis revealed previously unknown user behavior patterns.",
                    "next_steps": "Coordinate with James Kim on dashboard frontend integration."
                }
            ],
            "Business Operations": [
                {
                    "project": "Q3 Revenue Planning",
                    "team": ["Robert Chen", "Lisa Martinez"],
                    "update": "Lisa Martinez completed final financial models showing 15% projected growth. Robert Chen presented to board of directors with excellent communication skills. Implemented Power BI dashboards for real-time revenue tracking.",
                    "next_steps": "Monthly review cadence established. Monitor actuals vs. forecast."
                }
            ]
        },
        # Period 5 - June 26 - July 9, 2024
        {
            "period": "June 26 - July 9, 2024",
            "Engineering": [
                {
                    "project": "Customer Dashboard Redesign",
                    "team": ["James Kim", "Priya Sharma"],
                    "update": "James Kim completed UAT with 95% approval rating. Priya Sharma set up production deployment pipeline using Docker and Kubernetes. They collaborated on performance testing, achieving sub-200ms load times. James used Vue.js and Django effectively.",
                    "next_steps": "Production launch scheduled for next period. Final accessibility audit."
                },
                {
                    "project": "Infrastructure Modernization",
                    "team": ["Priya Sharma"],
                    "update": "Priya Sharma completed AWS infrastructure migration. All services now running on Kubernetes with Terraform-managed infrastructure. Implemented automated backups and disaster recovery procedures. Her automation expertise saved 15 hours per week of manual operations.",
                    "next_steps": "Documentation and knowledge transfer to team. Cost optimization review."
                }
            ],
            "Product": [
                {
                    "project": "User Onboarding Optimization",
                    "team": ["Emily Thompson", "David Park", "Aisha Williams"],
                    "update": "David Park designed the new onboarding flow in Adobe XD. Aisha Williams set up A/B testing framework. Emily Thompson coordinated launch with marketing team, showing strong stakeholder management. The new design reduced steps from 7 to 4.",
                    "next_steps": "Development implementation with engineering team. Launch A/B test."
                }
            ],
            "Business Operations": [
                {
                    "project": "Customer Retention Program",
                    "team": ["Tom Anderson", "Lisa Martinez"],
                    "update": "Tom Anderson expanded program to 200 customers with 32% reduction in churn. Lisa Martinez tracked KPIs using SQL and Power BI. Tom's training sessions with customer success team improved response times by 40%. His customer communication skills were exceptional.",
                    "next_steps": "Scale to all at-risk customers. Automate outreach workflows in Zendesk."
                }
            ]
        },
        # Period 6 - July 10-23, 2024
        {
            "period": "July 10-23, 2024",
            "Engineering": [
                {
                    "project": "Customer Dashboard Redesign",
                    "team": ["James Kim", "Sarah Chen", "Priya Sharma"],
                    "update": "Successful production launch! James Kim led the deployment. Sarah Chen monitored system performance. Priya Sharma managed infrastructure scaling. The new React-based dashboard achieved 99.9% uptime in first week. Great team collaboration throughout the project.",
                    "next_steps": "Gather user feedback. Plan feature enhancements for Q3."
                },
                {
                    "project": "Mobile API Development",
                    "team": ["Marcus Rodriguez", "Sarah Chen"],
                    "update": "Started new project for mobile app backend. Marcus Rodriguez designed FastAPI architecture. Sarah Chen provided GraphQL integration guidance. Marcus used Python and PostgreSQL for core services. Initial API endpoints completed.",
                    "next_steps": "Security testing. Documentation for mobile team."
                }
            ],
            "Product": [
                {
                    "project": "Mobile App Feature Roadmap",
                    "team": ["Emily Thompson", "David Park"],
                    "update": "Emily Thompson finalized Q3 feature priorities with leadership approval. David Park completed Figma designs for priority features. Strong strategic thinking demonstrated in prioritization process. Ready for engineering kickoff.",
                    "next_steps": "Sprint planning with Sarah Chen's team. Begin development in August."
                }
            ],
            "Business Operations": [
                {
                    "project": "Sales Process Automation",
                    "team": ["Robert Chen", "Lisa Martinez"],
                    "update": "Robert Chen implemented Salesforce automation workflows reducing sales cycle by 20%. Lisa Martinez created financial impact analysis showing $200K annual savings. Robert's leadership in change management ensured smooth adoption.",
                    "next_steps": "Advanced automation phase. Integrate with marketing tools."
                }
            ]
        },
        # Period 7 - July 24 - Aug 6, 2024
        {
            "period": "July 24 - August 6, 2024",
            "Engineering": [
                {
                    "project": "Mobile API Development",
                    "team": ["Marcus Rodriguez", "James Kim"],
                    "update": "Marcus Rodriguez completed authentication endpoints using FastAPI and JWT tokens. James Kim built admin panel with Vue.js for API management. Marcus demonstrated strong problem-solving skills in handling edge cases. They used Redis for session management.",
                    "next_steps": "Load testing with 10K concurrent users. Rate limiting implementation."
                },
                {
                    "project": "Infrastructure Modernization",
                    "team": ["Priya Sharma", "Marcus Rodriguez"],
                    "update": "Priya Sharma optimized AWS costs by 30% through right-sizing and reserved instances. Marcus helped migrate remaining services to Kubernetes. Priya's automation using Terraform and Docker streamlined operations significantly.",
                    "next_steps": "Implement advanced monitoring with Prometheus. Cost optimization phase 2."
                }
            ],
            "Product": [
                {
                    "project": "Analytics Dashboard Enhancement",
                    "team": ["Aisha Williams", "Emily Thompson", "James Kim"],
                    "update": "James Kim integrated Aisha's Tableau designs into the main dashboard. Aisha Williams added Python-based data processing for real-time metrics. Emily Thompson coordinated with executives on custom views. Excellent collaboration across product and engineering.",
                    "next_steps": "User training sessions. Add predictive analytics features."
                }
            ],
            "Business Operations": [
                {
                    "project": "Customer Retention Program",
                    "team": ["Tom Anderson"],
                    "update": "Tom Anderson scaled program to all customers using automated Zendesk workflows. Achieved 40% improvement in customer satisfaction. His relationship building and communication skills were critical to success. CRM integration completed.",
                    "next_steps": "Build predictive churn model with Aisha Williams. Expand to enterprise customers."
                }
            ]
        },
        # Period 8 - Aug 7-20, 2024
        {
            "period": "August 7-20, 2024",
            "Engineering": [
                {
                    "project": "Mobile API Development",
                    "team": ["Marcus Rodriguez", "Sarah Chen", "Priya Sharma"],
                    "update": "Marcus Rodriguez completed load testing - API handles 15K concurrent users. Sarah Chen conducted security audit using industry best practices. Priya Sharma configured auto-scaling in Kubernetes. The team used PostgreSQL, Redis, and FastAPI to build a robust system.",
                    "next_steps": "Production deployment. Monitor performance metrics."
                },
                {
                    "project": "Data Pipeline Modernization",
                    "team": ["Marcus Rodriguez", "Aisha Williams"],
                    "update": "Started collaboration on modernizing data pipelines. Marcus Rodriguez built Python scripts for ETL processes. Aisha Williams provided analytics requirements. Initial pipeline processing 500K records daily.",
                    "next_steps": "Add real-time streaming with Apache Kafka. Optimize SQL queries."
                }
            ],
            "Product": [
                {
                    "project": "User Onboarding Optimization",
                    "team": ["Emily Thompson", "Aisha Williams", "David Park"],
                    "update": "Aisha Williams reported A/B test results: 45% improvement in completion rate! Emily Thompson approved rollout to 100% of users. David Park made design refinements based on user research. Outstanding results from strong team collaboration.",
                    "next_steps": "Full rollout next week. Plan onboarding v2 features."
                }
            ],
            "Business Operations": [
                {
                    "project": "Q4 Planning",
                    "team": ["Robert Chen", "Lisa Martinez", "Emily Thompson"],
                    "update": "Robert Chen led cross-functional Q4 planning sessions. Lisa Martinez built financial forecasts in Excel and Power BI. Emily Thompson provided product roadmap inputs. Robert's leadership and process optimization ensured alignment across teams.",
                    "next_steps": "Executive presentation scheduled. Finalize team budgets in Salesforce."
                }
            ]
        },
        # Period 9 - Aug 21 - Sept 3, 2024
        {
            "period": "August 21 - September 3, 2024",
            "Engineering": [
                {
                    "project": "Mobile API Development",
                    "team": ["Marcus Rodriguez", "Priya Sharma"],
                    "update": "Production launch successful! Marcus Rodriguez monitored API performance - 99.99% uptime. Priya Sharma managed infrastructure scaling. The FastAPI backend with PostgreSQL and Redis is performing excellently. Mobile team integration complete.",
                    "next_steps": "Add advanced features. Optimize database queries for large datasets."
                },
                {
                    "project": "Data Pipeline Modernization",
                    "team": ["Marcus Rodriguez", "Aisha Williams", "Priya Sharma"],
                    "update": "Marcus Rodriguez implemented Apache Kafka for real-time streaming. Aisha Williams integrated pipeline with Tableau for live dashboards. Priya configured Kubernetes jobs for batch processing. Processing 2M records daily now. Strong technical collaboration.",
                    "next_steps": "Add machine learning model integration. Performance tuning."
                }
            ],
            "Product": [
                {
                    "project": "Mobile App Feature Roadmap",
                    "team": ["Emily Thompson", "David Park", "Sarah Chen"],
                    "update": "Engineering sprint started. Sarah Chen's team began implementing priority features using React Native and TypeScript. David Park provided design assets from Figma. Emily Thompson managed stakeholder updates with excellent communication skills. Development tracking in Jira.",
                    "next_steps": "Complete sprint 1 features. User testing in two weeks."
                }
            ],
            "Business Operations": [
                {
                    "project": "Sales Process Automation",
                    "team": ["Robert Chen", "Tom Anderson", "Lisa Martinez"],
                    "update": "Robert Chen rolled out phase 2 automation in Salesforce. Tom Anderson integrated customer success workflows. Lisa Martinez tracked ROI - $350K annual savings achieved. Robert's training program ensured 95% team adoption. Excellent cross-team collaboration.",
                    "next_steps": "Marketing automation integration. Advanced reporting in Power BI."
                }
            ]
        },
        # Period 10 - Sept 4-17, 2024
        {
            "period": "September 4-17, 2024",
            "Engineering": [
                {
                    "project": "Data Pipeline Modernization",
                    "team": ["Marcus Rodriguez", "Priya Sharma"],
                    "update": "Marcus Rodriguez completed ML model integration using Python scikit-learn. Priya Sharma optimized Docker containers reducing processing time by 50%. The pipeline now handles 3M records daily with Apache Kafka and PostgreSQL. Impressive technical achievement.",
                    "next_steps": "Add predictive analytics. Cost optimization for AWS infrastructure."
                },
                {
                    "project": "Platform Security Enhancement",
                    "team": ["Sarah Chen", "Priya Sharma"],
                    "update": "New security project initiated. Sarah Chen conducted security assessment across all services. Priya Sharma implemented AWS security best practices. They used security scanning tools and Terraform for infrastructure hardening. TypeScript type safety improvements made.",
                    "next_steps": "Penetration testing. Security training for engineering team."
                }
            ],
            "Product": [
                {
                    "project": "Mobile App Feature Roadmap",
                    "team": ["David Park", "Aisha Williams"],
                    "update": "David Park conducted user testing sessions with prototype in Adobe XD. Aisha Williams analyzed user behavior data revealing key insights. Made design iterations based on feedback. User research methodology was thorough and data-driven.",
                    "next_steps": "Finalize designs for sprint 2. Coordinate with Sarah Chen on technical feasibility."
                }
            ],
            "Business Operations": [
                {
                    "project": "Customer Success Expansion",
                    "team": ["Tom Anderson", "Robert Chen"],
                    "update": "Tom Anderson launched enterprise customer success program. Robert Chen designed operational processes and Zendesk workflows. Tom's relationship building resulted in 3 major account expansions. CRM tracking shows 25% increase in upsell opportunities.",
                    "next_steps": "Hire additional team members. Scale processes to support growth."
                }
            ]
        },
        # Period 11 - Sept 18 - Oct 1, 2024
        {
            "period": "September 18 - October 1, 2024",
            "Engineering": [
                {
                    "project": "Platform Security Enhancement",
                    "team": ["Sarah Chen", "Priya Sharma", "Marcus Rodriguez"],
                    "update": "Sarah Chen led penetration testing with external vendor. Priya Sharma patched identified vulnerabilities in Kubernetes and Docker configs. Marcus Rodriguez updated API authentication using modern JWT practices in FastAPI. All critical issues resolved. Strong security focus demonstrated.",
                    "next_steps": "Security training rollout. Implement continuous security scanning."
                },
                {
                    "project": "Mobile API Development",
                    "team": ["James Kim", "Marcus Rodriguez"],
                    "update": "James Kim added new features requested by mobile team using Vue.js admin panel. Marcus Rodriguez optimized PostgreSQL queries improving performance by 35%. They collaborated on GraphQL schema updates. Redis caching strategy enhanced.",
                    "next_steps": "Add webhook support. API versioning implementation."
                }
            ],
            "Product": [
                {
                    "project": "Analytics Dashboard Enhancement",
                    "team": ["Aisha Williams", "Emily Thompson"],
                    "update": "Aisha Williams launched predictive analytics features using Python machine learning models. Emily Thompson presented insights to executives showing strong presentation skills. Tableau dashboards now include churn prediction and revenue forecasting. Executive team very impressed.",
                    "next_steps": "Add custom alert system. Integrate with email notifications."
                }
            ],
            "Business Operations": [
                {
                    "project": "Q4 Planning",
                    "team": ["Robert Chen", "Lisa Martinez", "Emily Thompson"],
                    "update": "Robert Chen finalized Q4 operational plans. Lisa Martinez completed budget allocations in Excel and Salesforce. Emily Thompson aligned product roadmap with business goals. Robert's strategic thinking and leadership were crucial. Cross-functional alignment achieved.",
                    "next_steps": "Monthly review cadence. Track OKRs in project management system."
                }
            ]
        },
        # Period 12 - Oct 2-15, 2024
        {
            "period": "October 2-15, 2024",
            "Engineering": [
                {
                    "project": "Mobile App Feature Roadmap",
                    "team": ["Sarah Chen", "James Kim", "Marcus Rodriguez"],
                    "update": "Sarah Chen's team completed sprint 2 features using React Native, TypeScript, and Node.js. James Kim handled frontend components. Marcus Rodriguez built supporting backend APIs with FastAPI. Beta testing with 50 users showing excellent results. Great team collaboration.",
                    "next_steps": "Fix beta feedback issues. Plan for public launch in November."
                },
                {
                    "project": "Data Pipeline Modernization",
                    "team": ["Marcus Rodriguez", "Priya Sharma", "Aisha Williams"],
                    "update": "Final optimizations complete. Marcus Rodriguez implemented cost-saving measures reducing AWS spend by 25%. Priya Sharma automated monitoring with Prometheus and Docker. Aisha Williams validated data quality. Pipeline now processes 5M records daily with Apache Kafka, PostgreSQL, and Python. Outstanding technical achievement.",
                    "next_steps": "Documentation. Knowledge transfer sessions for team."
                }
            ],
            "Product": [
                {
                    "project": "User Onboarding Optimization",
                    "team": ["Emily Thompson", "David Park"],
                    "update": "Emily Thompson initiated v2 planning based on data insights. David Park explored new design patterns in Figma. Strategic thinking applied to next generation onboarding experience. Research phase for Q1 2025 features.",
                    "next_steps": "User interviews. Competitive analysis. Prototype testing."
                }
            ],
            "Business Operations": [
                {
                    "project": "Annual Planning 2025",
                    "team": ["Robert Chen", "Lisa Martinez", "Tom Anderson"],
                    "update": "Robert Chen kicked off 2025 planning with all departments. Lisa Martinez started financial modeling for three growth scenarios using Power BI and Excel. Tom Anderson provided customer insights for planning. Robert's leadership and process optimization skills ensuring efficient planning process.",
                    "next_steps": "Complete departmental inputs. Executive strategy session in November."
                }
            ]
        }
    ]

    # Generate content for each biweekly period
    for idx, period_data in enumerate(status_updates, 1):
        # Period header
        story.append(Paragraph(f"Biweekly Update #{idx}: {period_data['period']}", heading_style))
        story.append(Spacer(1, 0.2*inch))

        # Engineering team
        story.append(Paragraph("Engineering Team", team_style))
        for project in period_data.get("Engineering", []):
            story.append(Paragraph(f"<b>Project:</b> {project['project']}", project_style))
            story.append(Paragraph(f"<b>Team:</b> {', '.join(project['team'])}", body_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>Update:</b> {project['update']}", body_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>Next Steps:</b> {project['next_steps']}", body_style))
            story.append(Spacer(1, 12))

        # Product team
        story.append(Paragraph("Product Team", team_style))
        for project in period_data.get("Product", []):
            story.append(Paragraph(f"<b>Project:</b> {project['project']}", project_style))
            story.append(Paragraph(f"<b>Team:</b> {', '.join(project['team'])}", body_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>Update:</b> {project['update']}", body_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>Next Steps:</b> {project['next_steps']}", body_style))
            story.append(Spacer(1, 12))

        # Business Operations team
        story.append(Paragraph("Business Operations Team", team_style))
        for project in period_data.get("Business Operations", []):
            story.append(Paragraph(f"<b>Project:</b> {project['project']}", project_style))
            story.append(Paragraph(f"<b>Team:</b> {', '.join(project['team'])}", body_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>Update:</b> {project['update']}", body_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>Next Steps:</b> {project['next_steps']}", body_style))
            story.append(Spacer(1, 12))

        # Page break after each period (except last)
        if idx < len(status_updates):
            story.append(PageBreak())

    # Build PDF
    doc.build(story)
    print(f"✓ Generated test PDF: {filename}")
    print(f"  - 12 biweekly periods (May - October 2024)")
    print(f"  - 3 teams: Engineering, Product, Business Operations")
    print(f"  - 10 team members with diverse skills")
    print(f"  - 15+ projects across 6 months")
    print(f"\nRun extraction with:")
    print(f"  python extract_entities_mvp.py {filename}")


if __name__ == "__main__":
    generate_test_status_pdf()
