# Dremio Task Wizards

This directory contains specialized guides that walk the Agent through complex workflows. Use these wizards to lead the user through a structured best-practice process.

## Available Wizards

- [Semantic Layer Wizard](semantic_layer.md) - *Creating Medallion Architectures (Bronze/Silver/Gold)*
    - Use when: User wants to model data, create views, or organize their lakehouse.
    
- [Reflection Strategy Wizard](reflection_strategy.md) - *Performance Optimization*
    - Use when: User asks about slow queries, dashboards, or "optimization".
    
- [Source Onboarding Wizard](source_onboarding.md) - *Connecting Data*
    - Use when: User wants to connect S3, Postgres, Snowflake, or other sources.

## How to use a Wizard
1.  **Identify Intent**: Match user request to a wizard.
2.  **Discovery**: Ask the "Discovery Phase" questions to gather context.
3.  **Plan**: Use the "Implementation Pattern" to design the solution.
4.  **execute**: Use the tools defined in the "Execution Steps".
