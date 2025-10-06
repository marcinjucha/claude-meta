# Create or Extend iOS + TCA Feature

Create new feature or extend existing one following TCA + Clean Architecture patterns.

**Scope**: Creates production code only (Store, View, Use Case, Service, Repository, Models).
**Testing**: Use `/test` command separately to generate comprehensive tests.

**Creating New Feature:**
- TCA Store with @ObservableState and Actions
- SwiftUI View with proper bindings
- Use Case for business logic orchestration
- Service if combining multiple repositories
- Repository for data access (optional)
- Models with proper types
- Navigation integration
- Complete test coverage

**Extending Existing Feature:**
- Add new state properties and actions
- Implement new business logic in Use Case
- Add new UI components to View
- Update navigation if needed
- Add new data access methods to Repository
- Extend models with new properties
- Update tests for new functionality

**Generated Components (New Feature):**
- Feature Store (`FeatureNameStore.swift`)
- Feature View (`FeatureNameView.swift`)
- Use Case (`FeatureNameUseCase.swift`)
- Service (if multi-repository, `FeatureNameService.swift`)
- Repository (if data access needed, `FeatureNameRepository.swift`)
- Models (`FeatureNameModels.swift`)

**Note**: Use `/test` command to generate tests for created features.

**Best Practices Applied:**
- @ObservableState for state management
- BindingReducer() for form bindings
- @Dependency (DependencyKey for shared services in same file, Use Cases use makeWithDeps only)
- makeWithDeps factory for testing
- Proper cancellation IDs
- Publisher patterns (not TaskGroups)
- Design system integration (Colors, L10n, .defaultFont())
- Accessibility support
- Navigation setup

> **Detailed Guides**: See .cursor/rules for comprehensive patterns:
> - Architecture Essentials (Clean Architecture, layer responsibilities)
> - TCA Essentials (State, Actions, Effects patterns)
> - Critical Patterns (safety rules, common pitfalls)
> - Localization Rules (L10n naming conventions)
> - TCA Testing Best Practices (testing patterns, pitfalls)

**Localization:**
- Adds L10n keys to appropriate Localizable.strings
- Generates SwiftGen constants structure
- No hardcoded strings

**Testing:**
Tests are generated separately using `/test` command.
> See `/test` command for comprehensive test generation.

**File Locations:**
- Views: `DigitalShelf/Screens/FeatureName/`
- Use Cases: `Modules/Sources/Core/UseCases/`
- Services: `Modules/Sources/Core/Services/`
- Repositories: `Modules/Sources/Persistence/Repositories/`
- Models: `Modules/Sources/Model/`
- Tests: `Modules/Tests/`

**Agent Used:** May invoke `tca-developer`, `ios-architect`, and `ios-swiftui-designer`.

## Usage
```
/feature [feature_name_or_path] [change_description]
```

## Parameters
- `feature_name_or_path`: Feature name for new feature (e.g., "ProductDetail") OR path to existing feature file (required)
- `change_description`: Description of what to create or change:
  - For NEW feature: complexity level (see below)
  - For EXISTING feature: what to add/change (e.g., "add search functionality", "add offline support", "refactor actions")

**Feature Complexity Levels:**
- `simple`: View + Store only (no data layer)
  - Static screens (About, Help)
  - Simple dialogs/alerts
  - UI components without business logic

- `standard`: View + Store + Use Case (default)
  - Basic business logic
  - Single data source (1 repository)
  - Examples: User Profile, Settings

- `complex`: Full stack with Service + multiple Repositories
  - Combines multiple data sources
  - Complex business logic orchestration
  - Examples: Route Planning (routes + history + store data)

- `form`: Form with validation and bindings
  - Input fields with validation
  - Bindings and error handling
  - Examples: Login, Registration, Edit Profile

- `list`: List view with search/filter/sort
  - ScrollView/List with data
  - Search, filter, sort capabilities
  - Examples: Product List, Route List

- `detail`: Detail view with navigation from list
  - Navigation from parent list
  - Display single object details
  - Examples: Product Detail, Route Detail

## Examples
```
# Create new feature
/feature ProductDetail standard

# Create form with validation
/feature UserProfile form

# Extend existing feature
/feature DigitalShelf/Screens/RouteList/RouteListStore.swift add filtering by status

# Add new functionality
/feature Modules/Sources/Features/Mapping/MappingStore.swift add pause/resume capability
```
