Smart Inventory & Order Management System

A Flutter application for inventory management with a responsive web build and an Android build. It connects directly to Supabase for authentication and database access.

> This README describes the source found in the supplied project archive. The current code includes sign-in and registration, a dashboard, and product management. The dashboard shows summary data from Supabase. Sidebar items such as Categories, Customers, Orders, Inventory, and Reports currently display a “will be added” message; they are not complete modules yet.

## Current functionality

- **Authentication:** Email and password sign-in, registration, session-aware routing, and sign-out using Supabase Auth.
- **Profile and role lookup:** Reads a user's `full_name` and `role` from the `profiles` table. The app has an admin role check in its auth service. Configure and verify Supabase Row Level Security (RLS) policies for actual data protection; hiding UI controls alone is not authorization.
- **Dashboard:** Displays product, category, customer, and order counts; low-stock count; completed sales total; and recent orders, using records from Supabase.
- **Products:** Lists active products, searches by name or SKU, filters by category, and provides add, edit, and soft-delete operations. Product forms validate required fields and non-negative numeric values.
- **Responsive layouts:** Flutter UI includes desktop and narrow-screen layouts.
- **Platforms:** Flutter project includes Android and Web targets.

## Planned / not included in this archive

The assessment also asks for customer management, order creation with automatic stock updates, stock-in/stock-out workflows, reports, API documentation, and deployed URLs. These are not implemented as complete workflows in the supplied source. In particular, dashboard data is read from existing `customers` and `orders` tables, but dedicated customer and order management screens are not present. The Categories, Customers, Orders, Inventory, and Reports navigation items are placeholders.

There is no separate Django server or custom backend API in this archive. Supabase provides the hosted authentication and database APIs used by the Flutter client. Add and publish any missing modules and their documentation before describing them as complete in the assessment submission.

## Technology

- Flutter / Dart (the `pubspec.yaml` SDK constraint is `^3.14.0`)
- Supabase Flutter client for authentication and database access
- PostgreSQL hosted by Supabase
- `go_router` for navigation
- `fl_chart` is a declared dependency

Use a Flutter SDK compatible with the Dart SDK constraint in `pubspec.yaml`. Check `flutter --version` if dependency resolution fails.

## Project structure

```text
lib/
├── config/                 # Supabase client configuration
├── core/                   # Shared constants and theme
├── features/
│   ├── auth/               # Auth service and login/register screens
│   ├── dashboard/          # Dashboard, data service, models, widgets
│   └── products/           # Product service, model, list and form UI
├── routing/                # GoRouter routes and auth redirects
└── main.dart               # Supabase initialization and app entry point
android/                    # Android application project
web/                        # Flutter Web entry point and icons
```

## Prerequisites

- Flutter SDK and Dart SDK matching `pubspec.yaml`
- Android Studio (Android SDK and emulator) for Android builds
- VS Code with Flutter and Dart extensions (recommended)
- A Supabase project with the required database tables, columns, authentication settings, and RLS policies

## Configure Supabase

The current app reads its Supabase project URL and publishable key from `lib/config/supabase_config.dart`.

1. Create or select the Supabase project used by this app.
2. Confirm that the URL and **publishable/anon client key** in that file belong to the intended project.
3. Never put a Supabase `service_role` key or another privileged secret in a Flutter app. Client app values can be extracted from a distributed build.
4. Enable and test RLS on every exposed table. Write policies that enforce which authenticated users can read or modify each row and role. The supplied archive does not include SQL migrations or policy definitions, so recreate and verify the schema and policies in your Supabase project.
5. Configure email confirmation and password policies in Supabase Auth as appropriate for your demo.

### Tables referenced by the current source

The Dart code expects these Supabase tables and fields. Verify exact types, constraints, foreign keys, and policies against your Supabase project; SQL schema files are not included in the archive.

| Table | Fields referenced in the app |
|---|---|
| `profiles` | `id`, `full_name`, `role` |
| `products` | `id`, `name`, `sku`, `category_id`, `description`, `price`, `stock_quantity`, `min_stock`, `image_url`, `is_active`, `created_at`, `updated_at` |
| `categories` | `id`, `name` |
| `customers` | `id` (used for the dashboard count) |
| `orders` | `id`, `order_number`, `total_amount`, `status`, `created_at` |

The dashboard queries the tables above. A `profiles.id` associated with the authenticated user's ID is required for profile loading. Define relationships such as `products.category_id` to `categories.id` in the database if needed by your schema.

## Run locally

Open a terminal in the project root (the folder containing `pubspec.yaml`) and run:

```powershell
flutter doctor
flutter pub get
flutter run
```

For a specific device, list available targets and select one:

```powershell
flutter devices
flutter run -d <device-id>
```

To run in a browser:

```powershell
flutter run -d chrome
```

The app requires working Supabase credentials and the expected schema/policies. If initialization fails or a page shows a database error, first check the project URL/key, table and column names, user profile row, and RLS policies.

## Build

### Android APK

```powershell
flutter build apk --release
```

The APK is generated at:

```text
build/app/outputs/flutter-apk/app-release.apk
```

For a quick local install on a connected Android device:

```powershell
flutter install
```

The Android Gradle file currently uses a debug signing configuration for release builds. That is suitable for a local assessment demo but should be replaced with a properly protected release signing configuration before public distribution.

### Web

```powershell
flutter build web --release
```

The deployable site files are generated in `build/web/`. Upload that directory to a static web host configured for Flutter single-page application routing. Add the live URL below after deployment.

## Application routes

The current GoRouter routes are:

| Route | Screen |
|---|---|
| `/splash` | Splash and session redirect |
| `/login` | Sign-in |
| `/register` | Account registration |
| `/dashboard` | Dashboard |

The product list/form UI exists in the source, but it is not registered as a standalone GoRouter route in the supplied router. Sidebar navigation should be completed and verified before claiming product screens are reachable from the running app.

## API documentation

This app calls Supabase Auth and the Supabase database API directly through `supabase_flutter`; the archive contains no custom REST server, OpenAPI/Swagger file, or Postman collection.

- Supabase project/API URL: configure from your Supabase project dashboard; do not publish privileged keys.
- API reference: TODO — document the Supabase tables and operations used, auth flow, access policies, and example requests/responses, or link to an OpenAPI/Postman collection if you create one.
- Backend API deployment URL: TODO — add the Supabase project URL or state clearly which hosted APIs are used.

## Database diagram

TODO: Add an ER diagram showing profiles, products, categories, customers, orders, and any order line / stock movement tables you create. The supplied archive does not include a database diagram or SQL migrations.

## Submission links

- Source repository: TODO — add the repository URL containing this Flutter project (verify that it points to this project, not a different Django project).
- Live web app: TODO — add deployment URL, or `Not deployed`.
- Android APK / installation instructions: TODO — attach the release APK or add a download link and installation steps.
- Backend/API URL: TODO — add the Supabase project/API URL and relevant documentation.
- Database ER diagram: TODO — add link or repository path.
- API documentation: TODO — add link or repository path.
- Demonstration video: TODO — add a short screen recording link.

## Troubleshooting

- **Supabase initialization error:** Check `lib/config/supabase_config.dart` and verify the project is reachable.
- **Permission or database errors:** Check table names, columns, profile records, and RLS policies in Supabase.
- **Dependency resolution errors:** Check Flutter/Dart versions against `pubspec.yaml`, then run `flutter pub get`.
- **Android device not found:** Start an emulator or connect a device with USB debugging, then run `flutter devices`.

## Repository hygiene

Do not commit generated Flutter directories such as `.dart_tool/` and `build/`. The supplied ZIP contains a `.dart_tool/chrome-device` browser profile. Exclude `.dart_tool/` from future archives and repository uploads; browser profiles may contain local browsing/session data. The project `.gitignore` already lists `.dart_tool/` and `/build/`, so keep those directories out of Git.

## License

No license file was included in the supplied archive. Add a `LICENSE` file if you intend to grant reuse rights.